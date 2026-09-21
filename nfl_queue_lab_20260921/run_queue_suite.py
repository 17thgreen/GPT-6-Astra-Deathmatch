"""Run all preregistered cases on the same already-examined historical cohort."""
import bisect, gzip, hashlib, json, time
from pathlib import Path
from dataclasses import replace
from concurrent.futures import ProcessPoolExecutor, as_completed
from run_suite import load_capture
from run_candle_suite import load_quotes
from replay_v2 import Config
from queue_policies import QueueReplay, Policy

ROOT=Path(__file__).resolve().parent

def markouts(fills, quotes):
    books={}
    for q in quotes:
        if 0<q['bid']<q['ask']<1:
            times, mids=books.setdefault(q['ticker'],([],[]))
            times.append(q['at']);mids.append((q['bid']+q['ask'])/2)
    out={}
    for horizon in (60,300):
        qty=0.; delta=0.; gross=0.;missing=0.;eligible=0.
        for f in fills:
            if f['kind']!='maker':continue
            eligible+=f['size']
            times,mids=books.get(f['ticker'],([],[]));at=f['at']+horizon
            i=bisect.bisect_left(times,at)
            if i==len(times) or times[i]>at+120 or 'outcome_mid_at_fill' not in f:
                missing+=f['size'];continue
            mid=mids[i] if f['outcome']=='yes' else 1-mids[i]
            qty+=f['size'];delta+=(mid-f['outcome_mid_at_fill'])*f['size']
            gross+=(mid-f['price'])*f['size']-f['fee']
        out[str(horizon)]=dict(covered_contracts=qty,missing_contracts=missing,
             coverage_fraction=qty/eligible if eligible else None,
             signed_mid_move_cents=100*delta/qty if qty else None,
             fee_adjusted_markout_cents=100*gross/qty if qty else None,
             note='Ex-post markout at next available delayed candle within 120s of horizon; excludes exit fee, not realized P&L.')
    return out

def run_one(name, config, policy, events, markets, quotes):
    start=time.monotonic();r=QueueReplay(markets,config,policy)
    end=max(m['kickoff']-10800 for m in markets.values())+300
    for row in events:
        if row['at']>end:break
        if row.get('kind')=='quote':r.on_quote(row)
        else:r.on_trade(row)
    s=r.finish(end);s.update(scenario=name,seconds=time.monotonic()-start,
         evidence='DEVELOPMENT_COUNTERFACTUAL_FIXED_TAPE_UNOBSERVED_HISTORICAL_DEPTH')
    s['maker_fills_at_or_after_cutoff']=sum(f['kind']=='maker' and f['at']>=markets[f['ticker']]['kickoff']-10800 for f in r.fills)
    s['maker_markouts']=markouts(r.fills,quotes)
    total=s['maker_contracts']+s['taker_contracts']
    s['net_cents_per_traded_contract']=100*s['completed_strategy_pnl']/total if total and s['completed_strategy_pnl'] is not None else None
    s['positive_games']=sum(g['flat'] and g['cashflow']>0 for g in s['per_game'])
    game_pnl=sorted((g['cashflow'] for g in s['per_game']),reverse=True)
    s['pnl_excluding_top_two_games']=sum(game_pnl[2:]) if s['all_flat'] else None
    (ROOT/'results'/f'{name}.json').write_text(json.dumps(s,indent=2,allow_nan=False))
    with gzip.open(ROOT/'results'/f'{name}_fills.jsonl.gz','wt') as f:
        for row in r.fills:f.write(json.dumps(row,separators=(',',':'))+'\n')
    return s

def main():
    frozen=json.loads((ROOT/'FROZEN_INPUTS.json').read_text())
    for name,digest in frozen['sha256'].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:raise ValueError('Frozen input changed')
    rows,markets,trade_meta=load_capture();quotes,quote_meta=load_quotes()
    events=rows+quotes
    events.sort(key=lambda r:(r['at'],0 if r.get('kind')=='quote' else 1,r.get('trade_id',r['ticker'])))
    base=replace(Config(),quote_source='candles',liquidation_lead_seconds=300)
    cases=[]
    for label,q in [('q291',290.595),('q3300',3300)]:
        for policy in ['preserve','churn60','route','improve_exit','combined']:
            cases.append((label+'_'+policy,replace(base,queue_early=q),Policy(name=policy)))
        for policy in ['improve_exit','combined']:
            cases.append((label+'_'+policy+'_race250',replace(base,queue_early=q),Policy(name=policy,inside_race_queue=250)))
    result=dict(trade_data=trade_meta,quote_data=quote_meta,scenarios={})
    with ProcessPoolExecutor(max_workers=3) as pool:
        tasks={pool.submit(run_one,n,c,p,events,markets,quotes):n for n,c,p in cases}
        for task in as_completed(tasks):
            s=task.result();result['scenarios'][s['scenario']]=s
            print(s['scenario'],'pnl',s['completed_strategy_pnl'],'inside',s['metrics'].get('improved_filled_contracts',0),'seconds',round(s['seconds'],1),flush=True)
            (ROOT/'results/queue_suite_summary.json').write_text(json.dumps(result,indent=2,allow_nan=False))
    actual=result['scenarios']['q291_preserve']['completed_strategy_pnl']
    if abs(actual-frozen['prior_winddown_pnl'])>1e-7:raise AssertionError(('Baseline regression',actual,frozen['prior_winddown_pnl']))
    print('BASELINE REGRESSION PASS',actual,flush=True)

if __name__=='__main__':main()
