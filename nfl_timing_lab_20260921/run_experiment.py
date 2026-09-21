import gzip,hashlib,heapq,json,multiprocessing,os,time
from concurrent.futures import ProcessPoolExecutor,as_completed
from dataclasses import replace
from pathlib import Path
from replay_v2 import Config
from timing_policy import TimingReplay,BANDS

ROOT=Path(__file__).resolve().parent
EVENTS=None;MARKETS=None;WEEKS=None


def checked_inputs():
    global EVENTS,MARKETS,WEEKS
    manifest=json.loads((ROOT/'inputs/manifest.json').read_text())
    for name,digest in manifest['sha256'].items():
        assert hashlib.sha256((ROOT/'inputs'/name).read_bytes()).hexdigest()==digest,name
    with gzip.open(ROOT/'inputs/events.jsonl.gz','rt') as f:EVENTS=[json.loads(line) for line in f]
    MARKETS=json.loads((ROOT/'inputs/markets.json').read_text());WEEKS=json.loads((ROOT/'inputs/week_membership.json').read_text())
    return manifest['cohort']


def atomic_json(path,value):
    temporary=path.with_suffix(path.suffix+'.partial')
    temporary.write_text(json.dumps(value,indent=2,allow_nan=False));temporary.replace(path)


def save_rows(path,rows):
    temporary=path.with_suffix(path.suffix+'.partial')
    with gzip.open(temporary,'wt') as out:
        for row in rows:out.write(json.dumps(row,separators=(',',':'))+'\n')
    temporary.replace(path)


def one(case):
    queue,size,band,variant,cap=case;name=f'q{queue}_s{size}_{band}_{variant}_cap{cap}';began=time.monotonic()
    config=replace(Config(),order_size=size,exposure_cap=cap,queue_early=queue,quote_source='candles',liquidation_lead_seconds=300)
    r=TimingReplay(MARKETS,config,band,variant);boundaries=[]
    if band!='full':
        for event in r.groups:
            start,end=r.entry_bounds(event)
            boundaries.extend([dict(at=start,kind='boundary',event=event),
                               dict(at=end-config.cancel_delay_seconds,kind='boundary',event=event)])
    key=lambda row:(row['at'],0 if row.get('kind')=='quote' else 1 if row.get('kind')=='boundary' else 2,row.get('trade_id',row.get('ticker',row.get('event',''))))
    stream=heapq.merge(EVENTS,sorted(boundaries,key=key),key=key) if boundaries else EVENTS
    end=max(m['kickoff']-10800 for m in MARKETS.values())+300
    for row in stream:
        if row['at']>end:break
        if row.get('kind')=='quote':r.on_quote(row)
        elif row.get('kind')=='boundary':r.on_boundary(row['event'],row['at'])
        else:r.on_trade(row)
    result=r.finish(end)
    result.update(scenario=name,elapsed_seconds=time.monotonic()-began,
        evidence='52_CASE_DEVELOPMENT_MATRIX_HYPOTHETICAL_EXECUTION_NOT_HOLDOUT',
        maker_fills_at_or_after_cutoff=sum(f['kind']=='maker' and f['at']>=MARKETS[f['ticker']]['kickoff']-10800 for f in r.fills))
    result['week_contributions']={week:sum(g['cashflow'] for g in result['per_game'] if WEEKS[g['event']]==week) for week in ['week1','week2']}
    ranked=sorted((g['cashflow'] for g in result['per_game']),reverse=True)
    result['pnl_excluding_top_two_games']=sum(ranked[2:]) if result['all_flat'] else None
    result['positive_games']=sum(g['flat'] and g['cashflow']>0 for g in result['per_game'])
    volume=result['maker_contracts']+result['taker_contracts']
    result['net_cents_per_traded_contract']=100*result['completed_strategy_pnl']/volume if volume and result['completed_strategy_pnl'] is not None else None
    save_rows(ROOT/'results'/f'{name}_fills.jsonl.gz',r.fills)
    save_rows(ROOT/'results'/f'{name}_orders.jsonl.gz',r.order_records.values())
    atomic_json(ROOT/'results'/f'{name}.json',result)
    return result


def main():
    frozen=json.loads((ROOT/'FROZEN_EXPERIMENT.json').read_text())
    for name,digest in frozen['sha256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    for name,digest in json.loads((ROOT/'BASELINE_HASHES.json').read_text()).items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    cohort=checked_inputs();cases=[]
    for queue in [3300,10000]:
        cases.extend((queue,size,band,'route',250) for size in [250,50,25,10] for band in BANDS)
        cases.extend((queue,25,band,'stable',250) for band in ['full','d7_d3'])
        cases.extend((queue,25,'full','route',cap) for cap in [25,50,100,500])
    assert len(cases)==52
    result=dict(cohort=cohort,scenarios={})
    with ProcessPoolExecutor(max_workers=3,mp_context=multiprocessing.get_context('fork')) as pool:
        futures=[pool.submit(one,case) for case in cases]
        for future in as_completed(futures):
            r=future.result();result['scenarios'][r['scenario']]=r
            atomic_json(ROOT/'results/experiment_summary.json',result)
            print(r['scenario'],'pnl',r['completed_strategy_pnl'],'residual',r['unresolved_contracts'],flush=True)
    print('DONE',len(cases),'cases',flush=True)


if __name__=='__main__':main()
