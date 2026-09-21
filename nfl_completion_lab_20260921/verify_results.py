"""Recompute financial ledgers and frozen-code regression; no network."""
import gzip,hashlib,json
from collections import defaultdict
from pathlib import Path
from load_data import load_all

ROOT=Path(__file__).resolve().parent

def main():
    summary=json.loads((ROOT/'results/experiment_summary.json').read_text());scenarios=summary['scenarios']
    assert len(scenarios)==30
    frozen_sets=[json.loads((ROOT/'FROZEN_CODE.json').read_text()),
                 json.loads((ROOT/'BASELINE_HASHES.json').read_text()),
                 json.loads((ROOT/'FROZEN_SPEC.json').read_text())['sha256']]
    for hashes in frozen_sets:
        for name,digest in hashes.items():
            assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    cohorts=load_all();checked=[]
    for name,s in scenarios.items():
        individual=json.loads((ROOT/'results'/f'{name}.json').read_text())
        assert {k:v for k,v in individual.items() if k!='seconds'}=={k:v for k,v in s.items() if k!='seconds'},name
        cohort=name.split('_')[0];markets=cohorts[cohort][1]
        cash=5000.;net=defaultdict(float);fees=0.;units=0.;paired=0.;count=0;late=0;last=float('-inf')
        with gzip.open(ROOT/'results'/f'{name}_fills.jsonl.gz','rt') as f:
            for line in f:
                r=json.loads(line);count+=1
                assert r['at']>=last;last=r['at']
                assert r['size']>0 and 0<r['price']<1 and r['fee']>=0
                expected=min(abs(net[r['event']]),r['size']) if net[r['event']]*r['direction']<0 else 0
                assert abs(r['paired']-expected)<1e-6
                cash+=r['paired']-r['size']*r['price']-r['fee']
                net[r['event']]+=r['direction']*r['size'];units+=r['size'];paired+=r['paired'];fees+=r['fee']
                assert abs(cash-r['cash_after'])<1e-6 and cash>=-1e-7
                assert abs(net[r['event']]-r['inventory_after'])<1e-6
                assert abs(net[r['event']])<=250.000001
                if r['kind']=='maker' and r['at']>=markets[r['ticker']]['kickoff']-10800:late+=1
        assert late==0 and s['maker_fills_at_or_after_cutoff']==0
        assert count==s['fills'] and abs(fees-s['metrics'].get('fees',0))<1e-6
        assert abs(units-s['maker_contracts']-s['taker_contracts'])<1e-5
        residual=sum(abs(v) for v in net.values())
        assert abs(residual-s['unresolved_contracts'])<1e-6
        if s['completed_strategy_pnl'] is not None:
            assert residual<.009 and abs(cash-5000-s['completed_strategy_pnl'])<1e-6
        assert abs(units-2*paired-residual)<1e-5
        checked.append(dict(scenario=name,passed=True,fills=count,residual=residual))
    regression=json.loads((ROOT/'Q1_REGRESSION_REFERENCE.json').read_text());differences={}
    for name,expected in regression.items():
        differences[name]={}
        for key,value in expected.items():
            diff=scenarios[name][key]-value;differences[name][key]=diff
            assert abs(diff)<1e-7,(name,key,diff)
    result=dict(checked_scenarios=checked,q1_regression_differences=differences,
        cohort_counts=summary['cohorts'],all_checks_passed=True,
        note='Internal ledger/causality controls do not validate counterfactual execution.')
    (ROOT/'results/verification.json').write_text(json.dumps(result,indent=2))
    print('PASS 30 ledgers, original Q1 regressions and all input hashes')

if __name__=='__main__':main()
