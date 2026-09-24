"""Bounded unauthenticated GET discovery; receipt data, never fills."""
import concurrent.futures as cf
import gzip,hashlib,json,time,urllib.request,urllib.error,urllib.parse
from pathlib import Path
from collections import defaultdict,Counter
from core import event_top,number
ROOT=Path(__file__).resolve().parent
BASES=['https://external-api.kalshi.com/trade-api/v2','https://api.elections.kalshi.com/trade-api/v2']

def get(path,params=None):
    if not (path in ('/series','/markets','/margin/markets','/incentive_programs') or
            path.startswith('/markets/') and path.endswith('/orderbook') or
            path.startswith('/margin/markets/') and path.endswith('/orderbook')):
        raise ValueError('not a public data route')
    receipts=[]
    for base in BASES:
        url=base+path+('?' + urllib.parse.urlencode(params) if params else '')
        start=time.time_ns(); mono=time.monotonic_ns();status=None;error=None;raw=b''
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AMS-001-public-research'}),timeout=12) as r:
                status=r.status;raw=r.read()
        except urllib.error.HTTPError as e:status=e.code;raw=e.read();error=str(e)
        except Exception as e:error=repr(e)
        rec=dict(url=url,sent_ns=start,received_ns=time.time_ns(),rtt_ms=(time.monotonic_ns()-mono)/1e6,status=status,error=error,
                 sha256=hashlib.sha256(raw).hexdigest(),raw=raw.decode('utf-8',errors='replace'))
        receipts.append(rec)
        if error is None:
            try:return json.loads(raw),receipts
            except Exception as e:rec['error']='JSON: '+str(e)
    return None,receipts

def catalog(path,key,params=None):
    out=[];rs=[];cursor=None;seen=set();complete=False
    for page in range(5):
        query=dict(params or {})
        if cursor:query['cursor']=cursor
        data,r=get(path,query);rs.extend(r)
        if data is None:break
        if not isinstance(data.get(key),list):
            rs[-1]['schema_error']='missing list '+key;break
        out.extend(data[key]);cursor=data.get('next_cursor') or data.get('cursor')
        if not cursor:complete=True;break
        if cursor in seen:break
        seen.add(cursor)
    return out,rs,dict(complete=complete,next_cursor=cursor,count=len(out))

def pick_category(item):
    category,series=item;rs=[];attempts=[]
    for s in sorted(series,key=lambda s:s['ticker'])[:5]:
        d,r=get('/markets',dict(series_ticker=s['ticker'],status='open',limit=1000));rs+=r
        ms=d.get('markets',[]) if d else []
        attempts.append(dict(series=s['ticker'],returned=len(ms),cursor=d.get('cursor') if d else None,success=d is not None))
        if ms:return category,sorted(ms,key=lambda m:m['ticker'])[:2],rs,attempts
    return category,[],rs,attempts

def books(item):
    product,ticker=item;rs=[];tops=[]
    path=('/margin' if product=='perp' else '')+'/markets/'+urllib.parse.quote(ticker,safe='')+'/orderbook'
    for i in range(3):
        d,r=get(path,{'depth':10});rs+=r
        if d is None:tops.append(dict(poll=i,status='REQUEST_FAILED'));continue
        try:
            if product=='event':top=event_top(d)
            else:
                book=d['orderbook']; bid=[(number(p),number(q)) for p,q in book['bids'] if number(q)>0];ask=[(number(p),number(q)) for p,q in book['asks'] if number(q)>0]
                top=dict(bid=str(max(p for p,q in bid)) if bid else None,ask=str(min(p for p,q in ask)) if ask else None,two_sided=bool(bid and ask))
            tops.append(dict(poll=i,status='OK',received_ns=r[-1]['received_ns'],**top))
        except Exception as e:tops.append(dict(poll=i,status='SCHEMA_FAILED',error=repr(e)))
    return dict(product=product,ticker=ticker,polls=tops),rs

def main():
    out=ROOT/'capture'
    if out.exists():raise SystemExit('capture exists; preserve it')
    out.mkdir();receipts=[];catalogs={};states={}
    specs=[('series','/series','series',{}),('perps','/margin/markets','markets',{}),('incentives','/incentive_programs','incentive_programs',{'status':'active','limit':1000})]
    with cf.ThreadPoolExecutor(max_workers=3) as ex:
        futures={ex.submit(catalog,p,k,q):name for name,p,k,q in specs}
        for f in cf.as_completed(futures):
            name=futures[f];rows,rs,state=f.result();catalogs[name]=rows;receipts+=rs;states[name]=state
    print('CATALOGS',states,flush=True)
    categories=defaultdict(list)
    for s in catalogs['series']:
        for c in (s.get('categories') or [s.get('category') or 'Uncategorized']):categories[c].append(s)
    samples={};attempts={}
    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        for c,ms,rs,a in ex.map(pick_category,sorted(categories.items())):
            samples[c]=ms;receipts+=rs;attempts[c]=a
    chosen=[];seen=set()
    for i in range(2):
        for c in sorted(samples):
            if len(samples[c])>i and samples[c][i]['ticker'] not in seen and len(chosen)<24:
                m=samples[c][i];seen.add(m['ticker']);chosen.append(m)
    work=[('event',m['ticker']) for m in chosen]+[('perp',m['ticker']) for m in sorted(catalogs['perps'],key=lambda m:m['ticker'])[:4]]
    measurements=[]
    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        for measurement,rs in ex.map(books,work):measurements.append(measurement);receipts+=rs
    for name,data in [('catalogs',catalogs),('receipts',receipts)]:
        with gzip.open(out/(name+'.json.gz'),'wt') as f:json.dump(data,f,sort_keys=True)
    ok=[r['rtt_ms'] for r in receipts if r['error'] is None]
    summary=dict(status='DISCOVERY_ONLY',catalog_states=states,category_counts={k:len(v) for k,v in sorted(categories.items())},
        category_attempts=attempts,selected_event_metadata=chosen,books=measurements,
        incentive_types=dict(Counter(x.get('incentive_type','missing') for x in catalogs['incentives'])),
        request_count=len(receipts),http_status_counts=dict(Counter(str(r['status']) for r in receipts)),
        successful_rest_rtt_ms_sorted=sorted(ok),quote_survival=None,order_latency=None,pnl=None,
        limitations=['lexical access sample, not profitability ranking','three REST observations are not continuous survival','no authenticated feed or account fee verification'])
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir()}
    (out/'SHA256.json').write_text(json.dumps(hashes,indent=2)+'\n')
    print(json.dumps({k:summary[k] for k in ['status','category_counts','incentive_types','request_count','http_status_counts']}),flush=True)
if __name__=='__main__':main()
