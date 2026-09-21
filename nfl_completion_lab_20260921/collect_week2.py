"""Resumable public GET-only capture for the frozen additional cohort."""
import gzip,hashlib,json,time
from pathlib import Path
from datetime import datetime,timezone
from urllib.request import Request,urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError,URLError
from concurrent.futures import ThreadPoolExecutor,as_completed

ROOT=Path(__file__).resolve().parent
DATA=ROOT/'inputs/week2'
BASE='https://api.elections.kalshi.com/trade-api/v2/'

def get(path,params):
    url=BASE+path+'?'+urlencode(params)
    for retry in range(6):
        try:
            with urlopen(Request(url,headers={'User-Agent':'NFLCompletionResearch/1.0'}),timeout=25) as r:return json.load(r)
        except HTTPError as e:
            if e.code not in (429,500,502,503,504) or retry==5:raise
        except (URLError,TimeoutError):
            if retry==5:raise
        time.sleep(min(2**retry,8))

def hashfile(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def metadata(game):
    d=DATA/game['event'];d.mkdir(exist_ok=True)
    p=d/'event.json'
    if not p.exists():p.write_text(json.dumps(get('events/'+game['event'],{'with_nested_markets':'true'}),indent=2))
    j=json.loads(p.read_text());e=j['event'];ms=j.get('markets') or e.get('markets',[])
    if len(ms)!=2 or e.get('collateral_return_type')!='MECNET' or not e.get('mutually_exclusive'):
        raise ValueError('Unverified event structure')
    for m in ms:
        if m.get('price_level_structure')!='linear_cent' or '$0.50' not in m.get('rules_secondary',''):
            raise ValueError('Unverified price/tie rules')
    return [(game,m['ticker']) for m in ms]

def capture(game,ticker):
    d=DATA/game['event'];manifest=d/(ticker+'.manifest.json')
    if manifest.exists():
        old=json.loads(manifest.read_text())
        if all(hashfile(DATA/old[k]['path'])==old[k]['sha256'] for k in ('trades','candles')):return old
    kickoff=int(datetime.fromisoformat(game['kickoff']).timestamp());start=kickoff-604800;end=kickoff-10800+300
    tradefile=d/(ticker+'.trades.jsonl.gz');candlefile=d/(ticker+'.candles.jsonl.gz')
    ids=set();cursor=None;seen=set();pages=0;count=0;precutoff=0;postlude=0
    with gzip.open(str(tradefile)+'.partial','wt') as f:
        while True:
            params=dict(ticker=ticker,min_ts=start,max_ts=end,limit=1000,is_block_trade='false')
            if cursor:params['cursor']=cursor
            body=get('markets/trades',params);pages+=1
            for t in body.get('trades',[]):
                if t.get('is_block_trade'):raise ValueError('Block trade in filtered capture')
                if t['ticker']!=ticker:raise ValueError('Ticker mismatch')
                at=datetime.fromisoformat(t['created_time'].replace('Z','+00:00')).timestamp()
                if not start<=at<=end:raise ValueError('Out-of-window trade')
                if t['trade_id'] in ids:continue
                ids.add(t['trade_id']);count+=1
                if at<kickoff-10800:precutoff+=1
                else:postlude+=1
                f.write(json.dumps(t,separators=(',',':'))+'\n')
            cursor=body.get('cursor')
            if not cursor:break
            if cursor in seen or pages>=2000:raise ValueError('Unfinished pagination')
            seen.add(cursor)
            if pages%25==0:print(ticker,'trade pages',pages,flush=True)
    Path(str(tradefile)+'.partial').replace(tradefile)
    candles={};requests=0;lo=start
    while lo<end:
        hi=min(end,lo+3*86400)
        body=get('series/KXNFLGAME/markets/'+ticker+'/candlesticks',dict(start_ts=lo,end_ts=hi,period_interval=1));requests+=1
        for c in body.get('candlesticks',[]):
            at=c['end_period_ts']
            if not start<=at<=end:raise ValueError('Out-of-window candle')
            if at in candles and candles[at]!=c:raise ValueError('Conflicting boundary candle')
            candles[at]=c
        lo=hi
    with gzip.open(str(candlefile)+'.partial','wt') as f:
        for at in sorted(candles):f.write(json.dumps(candles[at],separators=(',',':'))+'\n')
    Path(str(candlefile)+'.partial').replace(candlefile)
    item=dict(event=game['event'],ticker=ticker,kickoff=game['kickoff'],start=start,end=end,
        metadata_sha256=hashfile(d/'event.json'),retrieved_at=datetime.now(timezone.utc).isoformat(),
        trades=dict(path=str(tradefile.relative_to(DATA)),sha256=hashfile(tradefile),count=count,
                    precutoff=precutoff,postlude=postlude,pages=pages,pagination_exhausted=True),
        candles=dict(path=str(candlefile.relative_to(DATA)),sha256=hashfile(candlefile),count=len(candles),
                     requests=requests,missing_minutes=sorted(set(range(start,end+1,60))-set(candles))))
    manifest.write_text(json.dumps(item,indent=2))
    print(ticker,'complete',count,'trades',len(candles),'candles',flush=True)
    return item

def main():
    cohort=json.loads((DATA/'cohort.json').read_text());tasks=[];result=dict(markets=[],failures=[])
    with ThreadPoolExecutor(max_workers=4) as pool:
        for job in as_completed([pool.submit(metadata,g) for g in cohort]):tasks.extend(job.result())
        pending={pool.submit(capture,g,t):t for g,t in tasks}
        for job in as_completed(pending):
            try:result['markets'].append(job.result())
            except Exception as e:result['failures'].append(dict(ticker=pending[job],error=repr(e)))
            (DATA/'capture_manifest.json').write_text(json.dumps(result,indent=2))
    print('DONE',len(result['markets']),'markets; failures',result['failures'],flush=True)
    if result['failures'] or len(result['markets'])!=30:raise SystemExit(1)

if __name__=='__main__':main()
