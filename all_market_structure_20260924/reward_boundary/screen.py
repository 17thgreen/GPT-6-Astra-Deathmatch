"""Whole-price-level candidate sizing on retained public books only."""
import collections,hashlib,importlib.util,json,zipfile
from decimal import Decimal as D,ROUND_FLOOR
from pathlib import Path
ROOT=Path(__file__).resolve().parent
_s=importlib.util.spec_from_file_location('ams009_model',ROOT.parent/'reward_competition/model.py')
model=importlib.util.module_from_spec(_s);_s.loader.exec_module(model)
INPUTS={};FRACTIONS=tuple(map(D,('.05','.10','.25','.50','1.00','1.10')))

def read(p):INPUTS[str(p.relative_to(ROOT.parent))]=hashlib.sha256(p.read_bytes()).hexdigest();return json.loads(p.read_text())
def receipt(p):
    r=read(p);assert hashlib.sha256(r['raw'].encode()).hexdigest()==r['sha256']
    return (json.loads(r['raw']) if r['status']==200 else {}),r['received_ns']
def paid(g):
    x=D(str(g)).quantize(D('.01'),rounding=ROUND_FLOOR);return x if x>=1 else D(0)

def whole_share(b,target,discount,side,qty):
    orders={s:list(b[s])+([(D('.01'),qty,True)] if s==side else []) for s in model.SIDES}
    detail={s:model.score_side(orders[s],target,discount,'whole_level') for s in model.SIDES}
    qualified=all(v is not None for v in detail.values())
    return {'qualified':qualified,'overall_share':sum(x['own_share'] for x in detail.values())/2 if qualified else 0,'own_side':detail[side]}

def cases(p,m,raw,ns):
    if not m or raw is None or not model.admitted(p,ns/1e9):return []
    if p.get('max_reward_per_account') is not None:return []
    if m.get('status') not in ('active','open') or ns/1e9>=model.stamp(m['close_time']):return []
    ranges=m.get('price_ranges',[])
    if not(m.get('price_level_structure')=='linear_cent' and len(ranges)==1 and D(ranges[0]['start'])==0 and D(ranges[0]['end'])==1 and D(ranges[0]['step'])==D('.01')):return []
    try:b=model.depth(raw);target=D(p['target_size_fp']);discount=D(p['discount_factor_bps'])/10000
    except (ValueError,TypeError,KeyError):return []
    best={s:max((v for v,q,o in b[s]),default=D(0)) for s in model.SIDES}
    if best['yes']+best['no']>=1 or not 0<=discount<=1:return []
    totals={s:sum((q for v,q,o in b[s]),D(0)) for s in model.SIDES}
    duration=model.stamp(p['end_date'])-model.stamp(p['start_date']);remaining=min(model.stamp(p['end_date']),model.stamp(m['close_time']))-ns/1e9
    budget=p['period_reward']/10000*remaining/duration*.5;out=[]
    for side in model.SIDES:
        other='no' if side=='yes' else 'yes'
        if totals[other]<target or best[other]+D('.01')>=1:continue
        for f in FRACTIONS:
            q=target*f;base=whole_share(b,target,discount,side,q)
            if not base['qualified'] or base['overall_share']<=0:continue
            changed={s:list(b[s]) for s in model.SIDES};top=best[other]
            removed=sum(qty for v,qty,o in changed[other] if v==top);changed[other]=[(v,qty,o) for v,qty,o in changed[other] if v<top]
            newbest=max((v for v,qty,o in changed[other]),default=D(0));price=D('.02') if newbest+D('.02')<1 else D('.01')
            changed[side].append((price,target/5,False));stress=whole_share(changed,target,discount,side,q)
            principal=q*D('.01');fees=q/1000;base_reward=paid(budget*base['overall_share']);stress_reward=paid(budget*stress['overall_share'])
            cushion=min(base_reward,stress_reward)-principal-fees
            out.append({'ticker':p['market_ticker'],'event_ticker':m.get('event_ticker'),'program_id':p['id'],'book_received_ns':ns,'pool_dollars':p['period_reward']/10000,'side':side,'fraction':str(f),'quantity':str(q),'classification':'supported_level' if totals[side]>=target else 'gap_completion',
                'public_same_price_quantity':str(sum(qty for v,qty,o in b[side] if v==D('.01'))),'public_better_price_quantity':str(sum(qty for v,qty,o in b[side] if v>D('.01'))),'public_side_total':str(totals[side]),
                'principal':float(principal),'fee_stress_reserve':float(fees),'base':base,'stress':stress,'removed_opposite_quantity':str(removed),'competitor_price':str(price),'competitor_quantity':str(target/5),
                'base_half_uptime_reward':float(base_reward),'stressed_half_uptime_reward':float(stress_reward),'conditional_cushion':float(cushion),'cushion_over_principal':float(cushion/principal),'passes':cushion>0})
    return out

def census_inputs():
    root=ROOT.parent/'reward_census';panel=read(root/'PANEL.json');books={};meta={};times={}
    for path in sorted((root/'capture').glob('books_*.json')):
        d,ns=receipt(path)
        for b in d.get('orderbooks',[]):books[b['ticker']]=b.get('orderbook_fp');times[b['ticker']]=ns
    for path in sorted((root/'capture').glob('metadata_*.json')):
        d,_=receipt(path)
        for m in d.get('markets',[]):meta[m['ticker']]=m
    for p in panel['programs']:
        t=p['market_ticker'];ns=times.get(t)
        if ns is not None:yield 'AMS-005',None,p,meta.get(t),books.get(t),ns

def frame_inputs(dirname,label):
    root=ROOT.parent/dirname
    for path in sorted(root.glob('FRAME_*.json')):
        frame=read(path);cycle=frame['cycle'];prefix=f'{cycle:02d}' if dirname in ('reward_replication','reward_scanner') else str(cycle)
        books={};meta={};times={}
        for f in sorted((root/'capture').glob(prefix+'_books*.json')):
            d,ns=receipt(f)
            for b in d.get('orderbooks',[]):books[b['ticker']]=b.get('orderbook_fp');times[b['ticker']]=ns
        for f in sorted((root/'capture').glob(prefix+'_metadata*.json')):
            d,_=receipt(f)
            for m in d.get('markets',[]):meta[m['ticker']]=m
        for r in frame['rows']:
            t=r['ticker'];ns=times.get(t)
            if ns is not None:yield label,cycle,r['program'],meta.get(t),books.get(t),ns

def main():
    for f,h in read(ROOT/'FREEZE.json')['sha256'].items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
    if not (ROOT.parent/'reward_scanner/RUN.json').exists():raise RuntimeError('AMS-010 capture must finish before this overlay')
    allcases=[];observations=collections.Counter();sources=[census_inputs(),frame_inputs('reward_replication','AMS-007'),frame_inputs('reward_competition','AMS-009'),frame_inputs('reward_scanner','AMS-010 exploratory overlay')]
    for gen in sources:
        for label,cycle,p,m,b,ns in gen:
            if model.admitted(p,ns/1e9):observations[label]+=1
            for case in cases(p,m,b,ns):case.update(source=label,cycle=cycle);allcases.append(case)
    with (ROOT/'CASES.jsonl').open('w') as f:
        for r in allcases:f.write(json.dumps(r)+'\n')
    best={}
    for r in allcases:
        if not r['passes']:continue
        key=(r['source'],r['cycle'],r['ticker'],r['side'])
        if key not in best or (r['cushion_over_principal'],-r['principal'])>(best[key]['cushion_over_principal'],-best[key]['principal']):best[key]=r
    summary={'designation':'reused development data and exploratory AMS-010 overlay; never an execution record','observations_by_source':dict(observations),'candidate_quantity_cases':len(allcases),'passing_quantity_cases':sum(r['passes'] for r in allcases),
        'supported_cases':sum(r['classification']=='supported_level' for r in allcases),'passing_supported_cases':sum(r['passes'] and r['classification']=='supported_level' for r in allcases),
        'best_per_side_observation':list(best.values()),'realized_pnl':None}
    (ROOT/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n');(ROOT/'INPUT_HASHES.json').write_text(json.dumps(INPUTS,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k!='best_per_side_observation'},indent=2))
    grouped=collections.Counter((r['source'],r['classification']) for r in best.values());print('best passing groups',dict(grouped))

if __name__=='__main__':main()
