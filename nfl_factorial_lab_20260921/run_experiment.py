import gzip,hashlib,json,multiprocessing,time,itertools,traceback
from concurrent.futures import ProcessPoolExecutor,as_completed
from dataclasses import replace
from pathlib import Path
from replay_v2 import Config
from adaptive_policy import AdaptiveReplay
from factorial_policy import FactorialReplay,Factors
ROOT=Path(__file__).resolve().parent
EVENTS=MARKETS=WEEKS=None

def atomic_json(path,value):
    tmp=path.with_suffix(path.suffix+'.partial');tmp.write_text(json.dumps(value,indent=2,allow_nan=False));tmp.replace(path)
def save_rows(path,rows):
    tmp=path.with_suffix(path.suffix+'.partial')
    with gzip.open(tmp,'wt') as f:
        for row in rows:f.write(json.dumps(row,separators=(',',':'))+'\n')
    tmp.replace(path)
def checked_inputs():
    global EVENTS,MARKETS,WEEKS
    manifest=json.loads((ROOT/'inputs/manifest.json').read_text())
    for name,digest in manifest['sha256'].items():assert hashlib.sha256((ROOT/'inputs'/name).read_bytes()).hexdigest()==digest,name
    with gzip.open(ROOT/'inputs/events.jsonl.gz','rt') as f:EVENTS=[json.loads(line) for line in f]
    MARKETS=json.loads((ROOT/'inputs/markets.json').read_text());WEEKS=json.loads((ROOT/'inputs/week_membership.json').read_text())
    return manifest['cohort']
def one(case):
    q,delay,label=case;name=f'q{q}_d{delay:g}_{label}';began=time.monotonic()
    cfg=replace(Config(),queue_early=q,quote_source='candles',liquidation_lead_seconds=300,
                order_delay_seconds=delay,cancel_delay_seconds=delay)
    r=AdaptiveReplay(MARKETS,cfg,'baseline') if label=='baseline' else FactorialReplay(MARKETS,cfg,Factors(*(b=='1' for b in label)))
    end=max(m['kickoff']-10800 for m in MARKETS.values())+300
    for row in EVENTS:
        if row['at']>end:break
        if row.get('kind')=='quote':r.on_quote(row)
        else:r.on_trade(row)
    result=r.finish(end)
    result.update(scenario=name,elapsed_seconds=time.monotonic()-began,evidence='Q6_REUSED_31_GAME_DEVELOPMENT_FACTORIAL_HYPOTHETICAL_EXECUTION')
    result['week_contributions']={w:sum(g['cashflow'] for g in result['per_game'] if WEEKS[g['event']]==w) for w in ['week1','week2']}
    ranked=sorted((g['cashflow'] for g in result['per_game']),reverse=True)
    result['pnl_excluding_top_two_games']=sum(ranked[2:]) if result['all_flat'] else None
    result['positive_games']=sum(g['flat'] and g['cashflow']>0 for g in result['per_game'])
    result['maker_fills_at_or_after_cutoff']=sum(f['kind']=='maker' and f['at']>=MARKETS[f['ticker']]['kickoff']-10800 for f in r.fills)
    for suffix,rows in [('fills',r.fills),('orders',r.order_records.values()),('decisions',r.decisions)]:save_rows(ROOT/'results'/f'{name}_{suffix}.jsonl.gz',rows)
    atomic_json(ROOT/'results'/f'{name}.json',result)
    return result

def main():
    frozen=json.loads((ROOT/'FROZEN_EXPERIMENT.json').read_text())
    for mapping in [frozen['sha256'],json.loads((ROOT/'BASELINE_HASHES.json').read_text())]:
        for name,digest in mapping.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    out=dict(cohort=checked_inputs(),scenarios={},failures={})
    labels=['baseline']+[''.join(map(str,bits)) for bits in itertools.product([0,1],repeat=3)]
    cases=[(q,d,label) for q in [3300,10000] for d in [.25,5] for label in labels]
    with ProcessPoolExecutor(max_workers=3,mp_context=multiprocessing.get_context('fork')) as pool:
        futures={pool.submit(one,case):case for case in cases}
        for future in as_completed(futures):
            try:r=future.result()
            except Exception as exc:
                q,d,label=futures[future];name=f'q{q}_d{d:g}_{label}'
                failure=dict(scenario=name,status='FAILED_NO_COMPLETED_PNL',traceback=''.join(traceback.format_exception(exc)))
                out['failures'][name]=failure;atomic_json(ROOT/'results'/f'{name}_failure.json',failure)
                atomic_json(ROOT/'results/experiment_summary.json',out);print('FAILED',name,str(exc),flush=True);continue
            out['scenarios'][r['scenario']]=r
            atomic_json(ROOT/'results/experiment_summary.json',out)
            print(r['scenario'],'pnl',r['completed_strategy_pnl'],'residual',r['unresolved_contracts'],'seconds',round(r['elapsed_seconds']),flush=True)
    print('DONE',len(out['scenarios']),'completed;',len(out['failures']),'failed',flush=True)
    if out['failures']:raise RuntimeError('Some scenarios failed; inspect retained failure records')
if __name__=='__main__':main()
