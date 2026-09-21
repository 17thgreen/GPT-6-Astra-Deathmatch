"""Post-result execution sensitivities; see POST_RESULT_DIAGNOSTICS.md."""
from dataclasses import replace
from concurrent.futures import ProcessPoolExecutor,as_completed
import json
from run_suite import ROOT,load_capture
from run_candle_suite import load_quotes,run_one
from replay_v2 import Config


def main():
    rows,markets,_=load_capture();quotes,_=load_quotes();events=rows+quotes
    events.sort(key=lambda r:(r['at'],0 if r.get('kind')=='quote' else 1,r.get('trade_id',r['ticker'])))
    base=replace(Config(),quote_source='candles')
    cases={'candles_baseline_regression':base,
           'candles_early_queue3300':replace(base,queue_early=3300),
           'candles_exit_depth50':replace(base,assumed_exit_depth=50),
           'candles_winddown5m':replace(base,liquidation_lead_seconds=300)}
    results={}
    with ProcessPoolExecutor(max_workers=3) as pool:
        jobs={pool.submit(run_one,n,c,events,markets):n for n,c in cases.items()}
        for task in as_completed(jobs):
            name=jobs[task];s=task.result();results[name]=s
            print(name,'pnl',s['completed_strategy_pnl'],'bounds',s['terminal_payout_bounds'],'unresolved',s['unresolved_contracts'],flush=True)
    original=json.loads((ROOT/'results/candles_profile_fixed.json').read_text())
    assert abs(results['candles_baseline_regression']['completed_strategy_pnl']-original['completed_strategy_pnl'])<1e-8
    (ROOT/'results/post_diagnostics_summary.json').write_text(json.dumps({'status':'POST_RESULT_DIAGNOSTICS_NOT_HOLDOUT','scenarios':results},indent=2,allow_nan=False))


if __name__=='__main__':main()
