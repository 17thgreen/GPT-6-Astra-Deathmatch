"""Twelve bounded prospective public-data cycles; no financial actions."""
import concurrent.futures as cf,hashlib,json,sys,time,urllib.request,urllib.error,urllib.parse
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parent
BASE='https://api.elections.kalshi.com/trade-api/v2'
sys.path.insert(0,str(ROOT.parent/'reward_census'));from census import score,stamp
sys.path.insert(0,str(ROOT.parent/'reward_tape'));from tape import compatible

def admitted(p,start,now):
    try:
        a=stamp(p['start_date']);b=stamp(p['end_date']);target=float(p['target_size_fp']);pool=p['period_reward']/10000
        return not p.get('paid_out') and target>0 and pool>0 and a>=start and a<=now<b and 0<b-a<=7200 and (pool/2/((b-a)/3600))/(target*.01)>=1
    except (KeyError,ValueError,ZeroDivisionError):return False

def get(job):
    name,path,params=job;assert path.startswith('/markets') or path=='/incentive_programs'
    url=BASE+path+'?'+urllib.parse.urlencode(params);raw=b'';status=None;error=None;sent=time.time_ns()
    try:
        with urllib.request.urlopen(url,timeout=12) as r:status=r.status;raw=r.read()
    except urllib.error.HTTPError as e:status=e.code;raw=e.read();error=type(e).__name__
    except Exception as e:error=type(e).__name__
    rec={'url':url,'sent_ns':sent,'received_ns':time.time_ns(),'status':status,'error':error,'sha256':hashlib.sha256(raw).hexdigest(),'raw':raw.decode(errors='replace')}
    (ROOT/'capture'/f'{name}.json').write_text(json.dumps(rec)+'\n')
    try:d=json.loads(rec['raw']) if status==200 else {}
    except ValueError:d={}
    if not isinstance(d,dict):d={}
    print(name,status,error,flush=True);return name,d,rec['received_ns']

def main():
    (ROOT/'capture').mkdir();start=time.monotonic();frozen=json.loads((ROOT/'START.json').read_text())['frozen_start_ns']/1e9
    selected={};frames=[];trades=[]
    for cycle in range(12):
        due=start+60*cycle
        while time.monotonic()<due:time.sleep(min(30,due-time.monotonic()))
        if time.monotonic()-start>=780:break
        catalog=[];cursor=None
        for page in range(2):
            params={'status':'active','type':'liquidity','limit':10000}
            if cursor:params['cursor']=cursor
            _,d,ns=get((f'{cycle:02d}_catalog_{page}','/incentive_programs',params));catalog.extend(d.get('incentive_programs',[]));cursor=d.get('next_cursor')
            if not cursor:break
        current={p['id']:p for p in catalog}
        possible=[p for p in catalog if admitted(p,frozen,ns/1e9)]
        def rank(p):return (stamp(p['start_date']),-(p['period_reward']/10000/2/((stamp(p['end_date'])-stamp(p['start_date']))/3600))/(float(p['target_size_fp'])*.01),p['market_ticker'],p['id'])
        for p in sorted(possible,key=rank):
            if len(selected)>=30:break
            selected.setdefault(p['market_ticker'],p)
        selection={'cycle':cycle,'selected_before_books_ns':time.time_ns(),'programs':list(selected.values()),'catalog_count':len(catalog),'cursor_remaining':bool(cursor),'new_programs_passing_gates':len(possible)}
        (ROOT/f'SELECTION_{cycle:02d}.json').write_text(json.dumps(selection,indent=2)+'\n')
        active=[t for t,p in selected.items() if p['id'] in current and stamp(current[p['id']]['end_date'])>ns/1e9]
        books={};metadata={};book_ns={};jobs=[]
        if active:
            jobs=[(f'{cycle:02d}_books','/markets/orderbooks',[('tickers',t) for t in active]),(f'{cycle:02d}_metadata','/markets',{'tickers':','.join(active),'limit':1000})]
        with cf.ThreadPoolExecutor(max_workers=4) as ex:
            for name,data,receipt in ex.map(get,jobs):
                if name.endswith('_books'):
                    for b in data.get('orderbooks',[]):books[b['ticker']]=b.get('orderbook_fp',{});book_ns[b['ticker']]=receipt
                else:
                    for m in data.get('markets',[]):metadata[m['ticker']]=m
        rows=[]
        for t,p in selected.items():
            fresh=current.get(p['id']);row=score(t,fresh or p,metadata.get(t),books.get(t),book_ns.get(t))
            row['program_currently_listed']=fresh is not None;row['program_terms_changed']=fresh is not None and fresh!=p;rows.append(row)
        frame={'cycle':cycle,'catalog_received_ns':ns,'catalog_cursor_remaining':bool(cursor),'selected_count':len(selected),'rows':rows}
        frames.append(frame);(ROOT/f'FRAME_{cycle:02d}.json').write_text(json.dumps(frame,indent=2)+'\n')
        print(json.dumps({'cycle':cycle,'selected':len(selected),'quote_candidates':sum(r.get('quote',{}).get('would_rest',False) for r in rows),'priority_candidates':sum(r.get('quote',{}).get('priority',False) for r in rows)}),flush=True)
    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        jobs=[('trades_'+t,'/markets/trades',{'ticker':t,'limit':1000}) for t in selected]
        for i in range(0,len(jobs),4):
            if time.monotonic()-start>=780:break
            for name,data,ns in ex.map(get,jobs[i:i+4]):
                t=name[len('trades_'):];p=selected[t];detail=[]
                for x in data.get('trades',[]):
                    assert x.get('ticker')==t
                    detail.append({'trade':x,'within_program':stamp(p['start_date'])<=stamp(x['created_time'])<stamp(p['end_date']),
                                   'compatible_yes_bid':compatible(x,'yes'),'compatible_no_bid':compatible(x,'no')})
                trades.append({'ticker':t,'usable':isinstance(data.get('trades'),list),'cursor_remaining':bool(data.get('cursor')),'received_ns':ns,'detail':detail})
    out={'elapsed_seconds':time.monotonic()-start,'selected_programs':list(selected.values()),'frames':frames,'trades':trades,'realized_pnl':None,'hypothetical_fills':None}
    (ROOT/'RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'complete_cycles':len(frames),'selected':len(selected),'trade_pages':len(trades),'elapsed_seconds':out['elapsed_seconds']}),flush=True)

if __name__=='__main__':main()
