import gzip,hashlib,json,multiprocessing,time
from concurrent.futures import ProcessPoolExecutor,as_completed
from dataclasses import replace
from pathlib import Path
from replay_v2 import Config
from adaptive_policy import AdaptiveReplay,MODES

ROOT=Path(__file__).resolve().parent
EVENTS=None;MARKETS=None;WEEKS=None

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
    queue,delay,mode=case;name=f'q{queue}_d{delay:g}_{mode}';began=time.monotonic()
    cfg=replace(Config(),queue_early=queue,quote_source='candles',liquidation_lead_seconds=300,
                order_delay_seconds=delay,cancel_delay_seconds=delay)
    replay=AdaptiveReplay(MARKETS,cfg,mode)
    end=max(m['kickoff']-10800 for m in MARKETS.values())+300
    for row in EVENTS:
        if row['at']>end:break
        if row.get('kind')=='quote':replay.on_quote(row)
        else:replay.on_trade(row)
    result=replay.finish(end)
    result.update(scenario=name,elapsed_seconds=time.monotonic()-began,
        evidence='Q5_REUSED_DEVELOPMENT_31_GAMES_HYPOTHETICAL_EXECUTION')
    result['week_contributions']={w:sum(g['cashflow'] for g in result['per_game'] if WEEKS[g['event']]==w) for w in ['week1','week2']}
    ranked=sorted((g['cashflow'] for g in result['per_game']),reverse=True)
    result['pnl_excluding_top_two_games']=sum(ranked[2:]) if result['all_flat'] else None
    result['positive_games']=sum(g['flat'] and g['cashflow']>0 for g in result['per_game'])
    result['maker_fills_at_or_after_cutoff']=sum(f['kind']=='maker' and f['at']>=MARKETS[f['ticker']]['kickoff']-10800 for f in replay.fills)
    for suffix,rows in [('fills',replay.fills),('orders',replay.order_records.values()),('decisions',replay.decisions)]:
        save_rows(ROOT/'results'/f'{name}_{suffix}.jsonl.gz',rows)
    atomic_json(ROOT/'results'/f'{name}.json',result)
    return result

def main():
    frozen=json.loads((ROOT/'FROZEN_EXPERIMENT.json').read_text())
    for mapping in [frozen['sha256'],json.loads((ROOT/'BASELINE_HASHES.json').read_text())]:
        for name,digest in mapping.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    result=dict(cohort=checked_inputs(),scenarios={})
    cases=[(q,d,m) for q in [3300,10000] for d in [.25,5] for m in MODES]
    with ProcessPoolExecutor(max_workers=3,mp_context=multiprocessing.get_context('fork')) as pool:
        futures=[pool.submit(one,case) for case in cases]
        for future in as_completed(futures):
            r=future.result();result['scenarios'][r['scenario']]=r
            atomic_json(ROOT/'results/experiment_summary.json',result)
            print(r['scenario'],'pnl',r['completed_strategy_pnl'],'residual',r['unresolved_contracts'],'seconds',round(r['elapsed_seconds']),flush=True)
    print('DONE',len(cases),'cases',flush=True)

if __name__=='__main__':main()
