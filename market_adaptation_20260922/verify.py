"""Reuse independent M2 financial audit with declared M3 cutoff anchors."""
import gzip
import hashlib
import json
from pathlib import Path
from extend import ROOT, M2
import verify_replay as accounting


def rows(path):
    with gzip.open(path,'rt') as f:
        return [json.loads(x) for x in f]


def main():
    accounting.ROOT=ROOT
    summary=json.loads((ROOT/'results/summary.json').read_text())
    assert len(summary['scenarios'])==32 and not summary['failures']
    checks=[];controls=[]
    for name,result in summary['scenarios'].items():
        markets={t:dict(m,kickoff=result['engine_clock_anchors'][t])
                 for t,m in result['actual_schedules'].items()}
        checks.append(accounting.verify(name,result,markets))
        for f in rows(ROOT/'results'/f'{name}_fills.jsonl.gz'):
            actual=result['actual_schedules'][f['ticker']]['kickoff']
            assert f['at'] <= actual-result['cutoff_minutes']*60+1e-6
        for o in rows(ROOT/'results'/f'{name}_orders.jsonl.gz'):
            m=result['actual_schedules'][o['ticker']]
            assert max(m['listed_at'],m['kickoff']-604800)<=o['submitted_at']
            assert o['active_at'] < m['kickoff']-result['cutoff_minutes']*60-300-result['config']['cancel_delay_seconds']
        if result['cutoff_minutes']==180 and result['queue_profile']=='nfl':
            q=int(result['config']['queue_early']);d=result['config']['order_delay_seconds']
            prior=f"{result['sport']}_q{q}_d{d:g}"
            old=json.loads((M2/'results'/f'{prior}.json').read_text())
            for key in ['completed_strategy_pnl','maker_contracts','taker_contracts','unhedged_contract_hours','min_cash','max_reserved_cash']:
                accounting.close(result[key],old[key],1e-7)
            matches={suffix:rows(ROOT/'results'/f'{name}_{suffix}.jsonl.gz')==rows(M2/'results'/f'{prior}_{suffix}.jsonl.gz')
                     for suffix in ('fills','orders')}
            assert all(matches.values()),name
            controls.append(dict(scenario=name,exact_matches=matches))
    assert len(controls)==8
    from run import check_freeze
    check_freeze()
    out=dict(all_passed=True,ledger_audits=checks,exact_M2_controls=controls,frozen_hashes_match=True)
    (ROOT/'results/verification.json').write_text(json.dumps(out,indent=2))
    print('PASS: 32 independent financial audits and 8 exact M2 fill/order controls')


if __name__=='__main__':main()
