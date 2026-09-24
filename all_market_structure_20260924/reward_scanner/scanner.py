"""Fixed-window public research scanner. Never sends or constructs API orders."""
import concurrent.futures as cf,hashlib,json,time,urllib.request,urllib.error,urllib.parse
from pathlib import Path
from policy import admission,evaluate,stamp
ROOT=Path(__file__).resolve().parent;BASE='https://api.elections.kalshi.com/trade-api/v2'

def get(job):
    name,path,params=job
    assert path in ('/incentive_programs','/markets','/markets/orderbooks','/markets/trades')
    url=BASE+path+'?'+urllib.parse.urlencode(params);raw=b'';status=None;error=None;sent=time.time_ns()
    try:
        with urllib.request.urlopen(url,timeout=12) as r:status=r.status;raw=r.read()
    except urllib.error.HTTPError as e:status=e.code;raw=e.read();error=type(e).__name__
    except Exception as e:error=type(e).__name__+': '+str(e)
    rec={'url':url,'sent_ns':sent,'received_ns':time.time_ns(),'status':status,'error':error,'sha256':hashlib.sha256(raw).hexdigest(),'raw':raw.decode(errors='replace')}
    (ROOT/'capture'/f'{name}.json').write_text(json.dumps(rec)+'\n')
    try:d=json.loads(rec['raw']) if status==200 else {}
    except ValueError:d={}
    if not isinstance(d,dict):d={}
    print(name,status,error,flush=True);return name,d,rec['received_ns']

def main():
    freeze=json.loads((ROOT/'FREEZE.json').read_text())
    for f,h in freeze['sha256'].items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
    (ROOT/'capture').mkdir();started=time.monotonic();start=json.loads((ROOT/'START.json').read_text())['frozen_start_ns']/1e9
    selected={};first_alerts={};cycles=[];missed=[]
    for cycle in range(15):
        due=stamp('2026-09-24T04:56:00Z')+cycle*60
        if time.time()>due+30:missed.append(cycle);continue
        while time.time()<due:time.sleep(min(20,due-time.time()))
        catalog=[];cursor=None;catalog_ok=True
        for page in range(2):
            params={'status':'active','type':'liquidity','limit':10000}
            if cursor:params['cursor']=cursor
            _,data,ns=get((f'{cycle:02d}_catalog_{page}','/incentive_programs',params))
            if not isinstance(data.get('incentive_programs'),list):catalog_ok=False
            catalog+=data.get('incentive_programs',[]);cursor=data.get('next_cursor')
            if not cursor:break
        current={p['id']:p for p in catalog};possible=[p for p in catalog if admission(p,start,ns/1e9)]
        def rank(p):return (stamp(p['start_date']),-(p['period_reward']/10000/2/((stamp(p['end_date'])-stamp(p['start_date']))/3600))/(float(p['target_size_fp'])*.01),p['market_ticker'],p['id'])
        cap=False
        for p in sorted(possible,key=rank):
            t=p['market_ticker']
            if t in selected:continue
            if len(selected)>=300:cap=True;break
            selected[t]=p
        active={t:current[p['id']] for t,p in selected.items() if p['id'] in current and admission(current[p['id']],start,ns/1e9,new=False)}
        panel={'cycle':cycle,'scheduled_ns':int(due*1e9),'catalog_ok':catalog_ok,'catalog_cursor_remaining':bool(cursor),'selection_cap_applied':cap,'catalog_count':len(catalog),'selected_before_books_ns':time.time_ns(),'programs':list(selected.values()),'active_tickers':list(active)}
        (ROOT/f'SELECTION_{cycle:02d}.json').write_text(json.dumps(panel,indent=2)+'\n')
        tickers=list(active);jobs=[]
        for i in range(0,len(tickers),50):
            ts=tickers[i:i+50];jobs.extend([(f'{cycle:02d}_books_{i}','/markets/orderbooks',[('tickers',t) for t in ts]),(f'{cycle:02d}_metadata_{i}','/markets',{'tickers':','.join(ts),'limit':1000})])
        books={};meta={};times={}
        with cf.ThreadPoolExecutor(max_workers=4) as ex:
            for name,data,receipt in ex.map(get,jobs):
                if '_books_' in name:
                    for b in data.get('orderbooks',[]):books[b['ticker']]=b.get('orderbook_fp');times[b['ticker']]=receipt
                else:
                    for m in data.get('markets',[]):meta[m['ticker']]=m
        rows=[]
        for t,p in selected.items():
            fresh=active.get(t);row=evaluate(t,fresh or p,meta.get(t),books.get(t),times.get(t))
            row['program_currently_listed']=p['id'] in current;row['program_terms_changed']=p['id'] in current and current[p['id']]!=p
            rows.append(row)
        ranked=sorted([r for r in rows if r['buffered_alert']],key=lambda r:(-r['plans'][1]['cushion_over_principal'],r['ticker']))
        for r in ranked:first_alerts.setdefault(r['ticker'],{'cycle':cycle,'row':r})
        frame={'cycle':cycle,'rows':rows,'ranked_alerts':[r['ticker'] for r in ranked]};cycles.append(cycle)
        (ROOT/f'FRAME_{cycle:02d}.json').write_text(json.dumps(frame,indent=2)+'\n')
        (ROOT/'FIRST_ALERTS.json').write_text(json.dumps(first_alerts,indent=2)+'\n')
        print(json.dumps({'cycle':cycle,'selected':len(selected),'active':len(active),'buffered_alerts':len(ranked),'ever_alerted':len(first_alerts)}),flush=True)
    tape=[]
    def trade_pages(t):
        pages=[];cursor=None
        for i in range(2):
            params={'ticker':t,'limit':1000}
            if cursor:params['cursor']=cursor
            _,data,ns=get((f'trades_{t}_{i}','/markets/trades',params));pages.append({'received_ns':ns,'data':data});cursor=data.get('cursor')
            if not cursor:break
        return {'ticker':t,'pages':pages,'cursor_remaining':bool(cursor)}
    with cf.ThreadPoolExecutor(max_workers=4) as ex:tape=list(ex.map(trade_pages,list(first_alerts)[:20]))
    (ROOT/'TRADES.json').write_text(json.dumps(tape,indent=2)+'\n')
    (ROOT/'RUN.json').write_text(json.dumps({'cycles':cycles,'missed_scheduled_cycles':missed,'elapsed_seconds':time.monotonic()-started,'selected_programs':len(selected),'first_alerts':len(first_alerts),'trade_tickers':len(tape),'orders_submitted':0,'realized_pnl':None},indent=2)+'\n')
    print('BOUNDED SCANNER FINISHED',flush=True)

if __name__=='__main__':main()
