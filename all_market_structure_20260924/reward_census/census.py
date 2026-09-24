"""Bounded public-data census. Contains no account or order routes."""
import concurrent.futures as cf
import datetime as dt
from decimal import Decimal as D
import hashlib,json,sys,time,urllib.request,urllib.error,urllib.parse
from pathlib import Path

ROOT=Path(__file__).resolve().parent
BASE='https://api.elections.kalshi.com/trade-api/v2'
sys.path.insert(0,str(ROOT.parent/'depth_survey'))
from survey import classify,stamp

def request(job):
    name,path,params=job
    assert path.startswith('/markets') or path=='/incentive_programs'
    url=BASE+path+'?'+urllib.parse.urlencode(params)
    wall=time.time_ns();raw=b'';status=None;error=None
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AMS-005-public-research'}),timeout=12) as r:
            status=r.status;raw=r.read()
    except urllib.error.HTTPError as e:status=e.code;raw=e.read();error=type(e).__name__
    except Exception as e:error=type(e).__name__
    rec={'url':url,'sent_ns':wall,'received_ns':time.time_ns(),'status':status,'error':error,
         'sha256':hashlib.sha256(raw).hexdigest(),'raw':raw.decode(errors='replace')}
    (ROOT/'capture'/f'{name}.json').write_text(json.dumps(rec)+'\n')
    try:data=json.loads(rec['raw']) if status==200 else {}
    except ValueError:data={}
    if not isinstance(data,dict):data={}
    print(name,status,error,flush=True)
    return name,data,rec['received_ns']

def score(t,p,m,b,ns):
    row={'ticker':t,'program':p,'book_received_ns':ns,'class':'unavailable'}
    if not m or not b or not ns:return row
    row.update({'title':m.get('title'),'rules_primary':m.get('rules_primary'),'rules_secondary':m.get('rules_secondary'),
                'close_time':m.get('close_time'),'expected_expiration_time':m.get('expected_expiration_time')})
    if m.get('status') not in ('active','open') or not stamp(p['start_date'])<=ns/1e9<min(stamp(p['end_date']),stamp(m['close_time'])):
        row['class']='outside_open_window';return row
    try:row.update(classify(b,p['target_size_fp']))
    except (KeyError,ValueError,TypeError):return row
    if row['class'] not in ('yes_short','no_short') or len(row['empty_sides'])!=1:return row
    side=row['empty_sides'][0];other='yes' if side=='no' else 'no'
    best=max((D(a) for a,q in b[other+'_dollars']),default=D(0))
    ranges=m.get('price_ranges',[])
    linear=m.get('price_level_structure')=='linear_cent' and len(ranges)==1 and D(ranges[0]['start'])==0 and D(ranges[0]['end'])==1 and D(ranges[0]['step'])==D('.01')
    rests=linear and D('.01')+best<1
    duration=(stamp(p['end_date'])-stamp(p['start_date']))/3600
    remain=max(0,min(stamp(p['end_date']),stamp(m['close_time']))-ns/1e9)/3600
    rate=p['period_reward']/10000/duration/2;principal=float(D(p['target_size_fp'])*D('.01'))
    row['quote']={'side':side,'price':'0.01','quantity':p['target_size_fp'],'opposite_best_bid':str(best),
                  'linear_cent_verified':linear,'would_rest':rests,'principal':principal,'ideal_rate':rate,
                  'remaining_hours':remain,'ideal_remaining_gross':rate*remain if rests else None,
                  'hours_to_match_full_loss':principal/rate,'priority':rests and rate*remain>principal,
                  'ideal_rate_per_principal':rate/principal}
    return row

def main():
    start=time.monotonic();(ROOT/'capture').mkdir()
    programs=[];cursor=None
    for i in range(2):
        params={'status':'active','type':'liquidity','limit':10000}
        if cursor:params['cursor']=cursor
        _,data,ns=request((f'catalog_{i}','/incentive_programs',params));programs.extend(data.get('incentive_programs',[]));cursor=data.get('next_cursor')
        if not cursor:break
    selected={}
    for p in sorted(programs,key=lambda p:p['id']):
        if p.get('paid_out') or D(p.get('target_size_fp','0'))<=0 or p['period_reward']<=0:continue
        if stamp(p['start_date'])<=ns/1e9<stamp(p['end_date']):selected.setdefault(p['market_ticker'],p)
    tickers=sorted(selected)[:6000]
    panel={'catalog_count':len(programs),'catalog_cursor_remaining':bool(cursor),'eligible_unique_markets':len(selected),
           'market_cap_applied':len(selected)>6000,'selected_before_books_ns':time.time_ns(),'programs':[selected[t] for t in tickers]}
    (ROOT/'PANEL.json').write_text(json.dumps(panel,indent=2)+'\n')
    (ROOT/'PANEL_SHA256.txt').write_text(hashlib.sha256((ROOT/'PANEL.json').read_bytes()).hexdigest()+'\n')
    if not tickers:raise RuntimeError('no eligible catalog; raw response retained')
    _,probe,probe_ns=request(('probe','/markets/orderbooks',[('tickers',t) for t in tickers[:2]]))
    if not isinstance(probe.get('orderbooks'),list) or {b.get('ticker') for b in probe['orderbooks']}!=set(tickers[:2]):
        (ROOT/'BLOCKED.json').write_text(json.dumps({'reason':'batch probe unavailable or wrong schema','data':probe},indent=2)+'\n')
        print('CENSUS BLOCKED');return
    books={};meta={};times={};jobs=[]
    for i in range(0,len(tickers),50):
        ts=tickers[i:i+50]
        jobs.extend([(f'books_{i}','/markets/orderbooks',[('tickers',t) for t in ts]),
                     (f'metadata_{i}','/markets',{'tickers':','.join(ts),'limit':1000})])
    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        for i in range(0,len(jobs),4):
            if time.monotonic()-start>=300:break
            for name,data,ns in ex.map(request,jobs[i:i+4]):
                if name.startswith('books_'):
                    for b in data.get('orderbooks',[]):books[b['ticker']]=b.get('orderbook_fp',{});times[b['ticker']]=ns
                else:
                    for m in data.get('markets',[]):meta[m['ticker']]=m
    rows=[score(t,selected[t],meta.get(t),books.get(t),times.get(t)) for t in tickers]
    candidates=sorted([r for r in rows if r.get('quote',{}).get('priority')],key=lambda r:(-r['quote']['ideal_rate_per_principal'],r['ticker']))
    counts={c:sum(r['class']==c for r in rows) for c in sorted({r['class'] for r in rows})}
    result={'panel_summary':{k:v for k,v in panel.items() if k!='programs'},'selected':len(tickers),'counts':counts,
            'one_empty_side_other_meets':sum('quote' in r for r in rows),
            'one_cent_rests':sum(r.get('quote',{}).get('would_rest',False) for r in rows),
            'priority_candidates':len(candidates),'elapsed_seconds':time.monotonic()-start,'rows':rows}
    (ROOT/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    follow={'created_ns':time.time_ns(),'designation':'selected after census, before follow-up observations','rows':candidates[:10]}
    (ROOT/'FOLLOWUP_PANEL.json').write_text(json.dumps(follow,indent=2)+'\n')
    (ROOT/'FOLLOWUP_PANEL_SHA256.txt').write_text(hashlib.sha256((ROOT/'FOLLOWUP_PANEL.json').read_bytes()).hexdigest()+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))

def followup():
    panel=json.loads((ROOT/'FOLLOWUP_PANEL.json').read_text());rows=panel['rows'];out=[];start=time.monotonic()
    assert hashlib.sha256((ROOT/'FOLLOWUP_PANEL.json').read_bytes()).hexdigest()==(ROOT/'FOLLOWUP_PANEL_SHA256.txt').read_text().strip()
    if not rows:return
    for rnd in (1,2):
        if rnd==2:time.sleep(30)
        if time.monotonic()-start>=120:break
        jobs=[]
        for row in rows:
            t=row['ticker'];path='/markets/'+urllib.parse.quote(t,safe='')
            jobs.extend([(f'follow{rnd}_book_{t}',path+'/orderbook',{'depth':0}),(f'follow{rnd}_meta_{t}',path,{})])
        received={}
        with cf.ThreadPoolExecutor(max_workers=4) as ex:
            for i in range(0,len(jobs),4):
                if time.monotonic()-start>=120:break
                for name,data,ns in ex.map(request,jobs[i:i+4]):received[name]=(data,ns)
        for row in rows:
            t=row['ticker'];bd,bns=received.get(f'follow{rnd}_book_{t}',({},None));md,_=received.get(f'follow{rnd}_meta_{t}',({},None))
            scored=score(t,row['program'],md.get('market'),bd.get('orderbook_fp'),bns);scored['round']=rnd;out.append(scored)
    (ROOT/'FOLLOWUP_RESULTS.json').write_text(json.dumps({'rows':out,'elapsed_seconds':time.monotonic()-start},indent=2)+'\n')
    print('follow-up rows',len(out))

if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='followup':followup()
    else:main()
