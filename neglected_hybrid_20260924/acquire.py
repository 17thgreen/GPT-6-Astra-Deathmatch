"""Bounded, GET-only NH-001 public evidence acquisition. Standard library only."""
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse, hashlib, json, re, threading, time
import urllib.request, urllib.error, urllib.parse

BASE='https://api.elections.kalshi.com/trade-api/v2'
DECISIONS=['2024-10-29T16:00:00+00:00','2024-11-04T16:00:00+00:00']
LOCK=threading.Lock()

def get(url, root, label):
    """No retry, no authentication, retain HTTP failures and exact raw bytes."""
    path=root/(label+'.json');receipt=root/(label+'.receipt.json')
    if path.exists() and receipt.exists():
        previous=json.loads(receipt.read_text())
        if previous['url']!=url:raise ValueError('Cache URL mismatch')
        if previous.get('sha256')!=hashlib.sha256(path.read_bytes()).hexdigest():raise ValueError('Cache hash mismatch')
        if previous.get('status')==200:return json.loads(path.read_text())
        return None
    info={'url':url,'started_at':datetime.now(timezone.utc).isoformat()}
    body=b''
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'NH-001-public-research/1.0'})
        with urllib.request.urlopen(req,timeout=20) as r:
            body=r.read(20_000_001)
            info.update(status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'))
        if len(body)>20_000_000:raise ValueError('Response exceeds bounded size')
    except urllib.error.HTTPError as e:
        body=e.read();info.update(status=e.code,error=str(e))
    except Exception as e:info.update(status=None,error=str(e))
    info.update(received_at=datetime.now(timezone.utc).isoformat(),bytes=len(body),sha256=hashlib.sha256(body).hexdigest())
    path.write_bytes(body);receipt.write_text(json.dumps(info,indent=2)+'\n')
    if info.get('status')!=200:return None
    try:return json.loads(body)
    except Exception:
        info['parse_error']='not_json';receipt.write_text(json.dumps(info,indent=2)+'\n');return None

def collect(root, series_file):
    root.mkdir(parents=True,exist_ok=True)
    series=json.loads(series_file.read_text())['series']
    pattern=r'(HOUSE(?:PARTY-?)?[A-Z]{2}(?:[0-9]{1,2}|AL)|SENATE(?:PARTY-?)?[A-Z]{2})'
    tickers=sorted({r['ticker'] for r in series if re.fullmatch(pattern,r['ticker'])})
    (root/'panel.json').write_text(json.dumps({'source':str(series_file),'series_tickers':tickers,
       'selection':'2024 individual House/Senate party race; names only, no outcomes or volume filter'},indent=2))
    def one(ticker):
        time.sleep(.3)
        url=BASE+'/historical/markets?'+urllib.parse.urlencode({'series_ticker':ticker,'limit':1000})
        x=get(url,root,'markets_'+ticker)
        if not x:return ticker,[], 'request_failed'
        if x.get('cursor'):return ticker,[], 'pagination_not_complete'
        rows=[m for m in x.get('markets',[]) if re.search(r'-24(?:-|$)',m['ticker'])]
        return ticker,rows,'complete'
    metadata=[];status=[]
    with ThreadPoolExecutor(max_workers=2) as pool:
        jobs=[pool.submit(one,t) for t in tickers]
        for i,f in enumerate(as_completed(jobs)):
            t,rows,s=f.result();metadata.extend(rows);status.append({'series':t,'status':s,'markets_2024':len(rows)})
            if (i+1)%20==0:print(json.dumps({'metadata_done':i+1,'total':len(tickers),'markets_2024':len(metadata)}),flush=True)
    metadata.sort(key=lambda r:r['ticker'])
    (root/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    (root/'admission_requests.json').write_text(json.dumps(status,indent=2)+'\n')
    # A D suffix is only a acquisition selector; normalization separately checks
    # affirmative title and rules before accepting Democratic-party semantics.
    candidates=[m for m in metadata if m['ticker'].endswith('-D')]
    def candles(job):
        m,d=job;t=int(datetime.fromisoformat(d).timestamp())
        url=BASE+'/historical/markets/'+m['ticker']+'/candlesticks?'+urllib.parse.urlencode({'start_ts':t-7200,'end_ts':t,'period_interval':60})
        time.sleep(.3)
        x=get(url,root,'quotes_'+m['ticker']+'_'+d[:10])
        return {'ticker':m['ticker'],'decision':d,'success':x is not None,'candles':x.get('candlesticks',[]) if x else []}
    quotes=[]
    with ThreadPoolExecutor(max_workers=2) as pool:
        for f in as_completed([pool.submit(candles,(m,d)) for m in candidates for d in DECISIONS]):quotes.append(f.result())
    quotes.sort(key=lambda r:(r['ticker'],r['decision']))
    (root/'quotes.json').write_text(json.dumps(quotes,indent=2)+'\n')
    print(json.dumps({'series':len(tickers),'metadata':len(metadata),'dem_suffix_markets':len(candidates),'quote_requests':len(quotes),'successful_quote_requests':sum(q['success'] for q in quotes)}),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('series_file',type=Path)
    a=p.parse_args();collect(a.root,a.series_file)
