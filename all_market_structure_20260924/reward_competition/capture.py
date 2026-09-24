"""Bounded public GET acquisition. Selection is written before books."""
import concurrent.futures as cf,hashlib,json,time,urllib.request,urllib.error,urllib.parse
from pathlib import Path
from model import admitted,analyze,stamp
ROOT=Path(__file__).resolve().parent
BASE='https://api.elections.kalshi.com/trade-api/v2'

def get(job):
    name,path,params=job
    assert path in ('/markets','/markets/orderbooks','/incentive_programs')
    url=BASE+path+'?'+urllib.parse.urlencode(params);raw=b'';status=None;error=None;sent=time.time_ns()
    try:
        with urllib.request.urlopen(url,timeout=12) as r:status=r.status;raw=r.read()
    except urllib.error.HTTPError as e:status=e.code;raw=e.read();error=type(e).__name__
    except Exception as e:error=type(e).__name__
    rec={'url':url,'sent_ns':sent,'received_ns':time.time_ns(),'status':status,'error':error,'sha256':hashlib.sha256(raw).hexdigest(),'raw':raw.decode(errors='replace')}
    (ROOT/'capture'/f'{name}.json').write_text(json.dumps(rec)+'\n')
    try:data=json.loads(rec['raw']) if status==200 else {}
    except ValueError:data={}
    if not isinstance(data,dict):data={}
    print(name,status,error,flush=True);return name,data,rec['received_ns']

def main():
    frozen=json.loads((ROOT/'FREEZE.json').read_text())
    for f,h in frozen['sha256'].items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
    (ROOT/'capture').mkdir();start=time.monotonic();frames=[];first_terms={}
    for cycle in range(3):
        due=start+45*cycle
        while time.monotonic()<due:time.sleep(min(20,due-time.monotonic()))
        if time.monotonic()-start>=240:break
        catalog=[];cursor=None
        for page in range(2):
            params={'status':'active','type':'liquidity','limit':10000}
            if cursor:params['cursor']=cursor
            _,data,ns=get((f'{cycle}_catalog_{page}','/incentive_programs',params));catalog+=data.get('incentive_programs',[]);cursor=data.get('next_cursor')
            if not cursor:break
        possible=[p for p in catalog if admitted(p,ns/1e9)]
        def rank(p):return (-(p['period_reward']/10000/2/((stamp(p['end_date'])-stamp(p['start_date']))/3600))/(float(p['target_size_fp'])*.01),p['market_ticker'],p['id'])
        unique={}
        for p in sorted(possible,key=rank):unique.setdefault(p['market_ticker'],p)
        selected=dict(list(unique.items())[:300]);tickers=list(selected)
        panel={'cycle':cycle,'catalog_count':len(catalog),'eligible_unique':len(unique),'selection_cap_applied':len(unique)>300,'cursor_remaining':bool(cursor),'selected_before_books_ns':time.time_ns(),'programs':list(selected.values())}
        (ROOT/f'SELECTION_{cycle}.json').write_text(json.dumps(panel,indent=2)+'\n')
        jobs=[]
        for i in range(0,len(tickers),50):
            ts=tickers[i:i+50];jobs.extend([(f'{cycle}_books_{i}','/markets/orderbooks',[('tickers',t) for t in ts]),(f'{cycle}_metadata_{i}','/markets',{'tickers':','.join(ts),'limit':1000})])
        books={};meta={};times={}
        with cf.ThreadPoolExecutor(max_workers=4) as ex:
            for i in range(0,len(jobs),4):
                if time.monotonic()-start>=240:break
                for name,data,receipt in ex.map(get,jobs[i:i+4]):
                    if '_books_' in name:
                        for b in data.get('orderbooks',[]):books[b['ticker']]=b.get('orderbook_fp');times[b['ticker']]=receipt
                    else:
                        for m in data.get('markets',[]):meta[m['ticker']]=m
        rows=[]
        for t,p in selected.items():
            row=analyze(t,p,meta.get(t),books.get(t),times.get(t));key=p['id'];first_terms.setdefault(key,p)
            row['program_terms_changed']=p!=first_terms[key];rows.append(row)
        frame={'cycle':cycle,'catalog_received_ns':ns,'rows':rows};frames.append(frame)
        (ROOT/f'FRAME_{cycle}.json').write_text(json.dumps(frame,indent=2)+'\n')
        counts={c:sum(r['class']==c for r in rows) for c in sorted({r['class'] for r in rows})}
        print(json.dumps({'cycle':cycle,'selected':len(rows),'counts':counts}),flush=True)
    (ROOT/'RUN.json').write_text(json.dumps({'cycles':len(frames),'elapsed_seconds':time.monotonic()-start,'realized_pnl':None,'orders_submitted':0},indent=2)+'\n')

if __name__=='__main__':main()
