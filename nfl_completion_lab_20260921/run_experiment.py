import argparse,gzip,hashlib,json,time
from pathlib import Path
from dataclasses import replace
from concurrent.futures import ProcessPoolExecutor,as_completed
from replay_v2 import Config
from completion_policy import CompletionReplay
from load_data import ROOT,load_week,load_all

def run_one(name,events,markets,config,mode):
    start=time.monotonic();r=CompletionReplay(markets,config,mode)
    end=max(m['kickoff']-10800 for m in markets.values())+300
    for row in events:
        if row['at']>end:break
        if row.get('kind')=='quote':r.on_quote(row)
        else:r.on_trade(row)
    s=r.finish(end);s.update(scenario=name,seconds=time.monotonic()-start,
        evidence='FROZEN_POLICY_COUNTERFACTUAL_REPLAY_WITH_UNOBSERVED_HISTORICAL_QUEUES')
    s['maker_fills_at_or_after_cutoff']=sum(f['kind']=='maker' and f['at']>=markets[f['ticker']]['kickoff']-10800 for f in r.fills)
    s['positive_games']=sum(g['flat'] and g['cashflow']>0 for g in s['per_game'])
    ranked=sorted((g['cashflow'] for g in s['per_game']),reverse=True)
    s['pnl_excluding_top_two_games']=sum(ranked[2:]) if s['all_flat'] else None
    volume=s['maker_contracts']+s['taker_contracts']
    s['net_cents_per_traded_contract']=100*s['completed_strategy_pnl']/volume if volume and s['completed_strategy_pnl'] is not None else None
    (ROOT/'results'/f'{name}.json').write_text(json.dumps(s,indent=2,allow_nan=False))
    with gzip.open(ROOT/'results'/f'{name}_fills.jsonl.gz','wt') as out:
        for f in r.fills:out.write(json.dumps(f,separators=(',',':'))+'\n')
    return s

def main():
    p=argparse.ArgumentParser();p.add_argument('--week1-only',action='store_true');args=p.parse_args()
    frozen=json.loads((ROOT/'FROZEN_SPEC.json').read_text())
    for name,digest in frozen['sha256'].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:raise ValueError('Frozen spec changed')
    for name,digest in json.loads((ROOT/'BASELINE_HASHES.json').read_text()).items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:raise ValueError('Baseline changed')
    cohorts={'week1':load_week('week1')} if args.week1_only else load_all()
    cases=[]
    for cohort,(events,markets,data) in cohorts.items():
        queues=[('q291',290.595),('q3300',3300),('q10000',10000)]
        if cohort=='combined':queues.append(('q100000',100000))
        for label,queue in queues:
            cfg=replace(Config(),quote_source='candles',liquidation_lead_seconds=300,queue_early=queue)
            for mode in ['q1_route','pair_gate','pair_complete']:
                name=cohort+'_'+label+'_'+mode;cases.append((name,events,markets,cfg,mode))
    out=dict(cohorts={k:v[2] for k,v in cohorts.items()},scenarios={})
    summary=ROOT/'results'/('week1_summary.json' if args.week1_only else 'experiment_summary.json')
    with ProcessPoolExecutor(max_workers=3) as pool:
        tasks={pool.submit(run_one,*case):case[0] for case in cases}
        for future in as_completed(tasks):
            s=future.result();out['scenarios'][s['scenario']]=s
            print(s['scenario'],'pnl',s['completed_strategy_pnl'],'unresolved',s['unresolved_contracts'],flush=True)
            summary.write_text(json.dumps(out,indent=2,allow_nan=False))
    print('DONE',len(cases),'cases',flush=True)

if __name__=='__main__':main()
