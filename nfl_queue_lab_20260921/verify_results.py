"""Reconcile delivered fills and financial constraints; no network access."""
import gzip,hashlib,json,math
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def main():
    main=json.loads((ROOT/'results/queue_suite_summary.json').read_text())['scenarios']
    extra=json.loads((ROOT/'results/mechanism_summary.json').read_text())
    stress=json.loads((ROOT/'results/queue_stress_summary.json').read_text())
    scenarios={**main,**extra,**stress};checked=[]
    frozen=json.loads((ROOT/'FROZEN_INPUTS.json').read_text())
    for name,digest in frozen['sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    assert len(main)==14 and len(extra)==2 and len(stress)==4
    assert abs(main['q291_preserve']['completed_strategy_pnl']-frozen['prior_winddown_pnl'])<1e-7
    for name,s in scenarios.items():
        cash=s['config']['starting_cash'];net=defaultdict(float);last=-math.inf;fees=0.;count=0;units=0.
        with gzip.open(ROOT/'results'/f'{name}_fills.jsonl.gz','rt') as f:
            for line in f:
                row=json.loads(line);count+=1
                assert row['at']>=last;last=row['at']
                assert row['size']>0 and 0<row['price']<1 and row['fee']>=0
                cash+=row['paired']-row['size']*row['price']-row['fee']
                net[row['event']]+=row['direction']*row['size'];fees+=row['fee'];units+=row['size']
                assert abs(cash-row['cash_after'])<1e-6
                assert abs(net[row['event']]-row['inventory_after'])<1e-6
                assert abs(net[row['event']])<=250.000001
        assert all(abs(v)<1e-6 for v in net.values())
        assert s['all_flat'] and s['maker_fills_at_or_after_cutoff']==0
        assert abs(cash-5000-s['completed_strategy_pnl'])<1e-6
        assert abs(fees-s['metrics']['fees'])<1e-6 and count==s['fills']
        assert abs(units-s['maker_contracts']-s['taker_contracts'])<1e-5
        assert abs(units-2*s['metrics']['paired_units'])<1e-5
        checked.append(dict(scenario=name,fills=count,pnl=s['completed_strategy_pnl'],passed=True))
    cap=json.loads((ROOT/'forward/capture_summary.json').read_text())
    raw=[json.loads(line) for line in (ROOT/'forward/observations.jsonl').read_text().splitlines()]
    observed_errors=[r for r in raw if r['kind']=='error']
    assert len(observed_errors)==len(cap['errors'])
    for expected,actual in zip(cap['errors'],observed_errors):
        assert all(actual[k]==v for k,v in expected.items())
    assert hashlib.sha256((ROOT/'forward/observations.jsonl').read_bytes()).hexdigest()==cap['sha256']
    # A later complete trade request must recover any failed interval. Book gaps remain missing.
    trade_coverage={}
    for ticker in cap['tickers']:
        intervals=sorted((r['params']['min_ts'],r['params']['max_ts']) for r in raw
            if r['kind']=='trades' and r['ticker']==ticker and not r['body'].get('cursor'))
        assert intervals
        end=intervals[0][1]
        for start,stop in intervals[1:]:
            assert start<=end,(ticker,'trade coverage gap',end,start)
            end=max(end,stop)
        trade_coverage[ticker]=[intervals[0][0],end]
    output=dict(scenarios=checked,baseline_regression_passed=True,forward_hash_passed=True,
        recorded_capture_errors=len(observed_errors),trade_interval_coverage=trade_coverage,
        note='Verifies internal accounting and constraints; does not validate hypothetical fills or historical queue assumptions.')
    (ROOT/'results/verification.json').write_text(json.dumps(output,indent=2))
    print('PASS',len(checked),'complete ledgers, baseline regression, and forward capture hash')

if __name__=='__main__':main()
