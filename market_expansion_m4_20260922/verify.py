"""Financial audit, temporal/cap checks and exact unchanged M3 controls."""
from m4_common import ROOT, M3, read, save, lines
import m4_audit as audit
from m4_run import check_freeze, specifications


def main():
    summary=read(ROOT/'results/summary.json')
    expected={c['name']:c for c in specifications()}
    assert len(expected)==80
    assert set(summary['scenarios']).isdisjoint(summary['failures'])
    assert set(summary['scenarios'])|set(summary['failures'])==set(expected)
    assert all(f.get('blocked') for f in summary['failures'].values())
    checks,controls=[],[]
    for name,result in summary['scenarios'].items():
        case=expected[name]
        assert result['specification']==case
        config=result['config']
        assert config['order_size']==config['exposure_cap']==case['size']
        assert (config['maker_coefficient'],config['taker_coefficient'])==tuple(result['coefficients'])
        assert config['queue_early']==case['queue']
        assert config['cancel_delay_seconds']==config['order_delay_seconds']==case['delay']
        schedules=result['actual_schedules']
        market_map={t:dict(m,kickoff=result['engine_clock_anchors'][t]) for t,m in schedules.items()}
        checks.append(audit.verify(name,result,market_map))
        fills=list(lines(ROOT/'results'/f'{name}_fills.jsonl.gz'))
        orders=list(lines(ROOT/'results'/f'{name}_orders.jsonl.gz'))
        for fill in fills:
            m=schedules[fill['ticker']]
            assert max(m['listed_at'],m['kickoff']-604800)<=fill['at']<=m['kickoff']-case['cutoff']*60+1e-6
        for order in orders:
            m=schedules[order['ticker']]
            assert max(m['listed_at'],m['kickoff']-604800)<=order['submitted_at']
            assert order['active_at']<m['kickoff']-case['cutoff']*60-300-case['delay']
            if case['complete_first'] and abs(order['inventory_at_submission'])>=.01:
                assert order['direction']*order['inventory_at_submission']<0
                assert order['submitted_quantity']<=abs(order['inventory_at_submission'])+1e-6
        if case['cohort']=='development' and case['size']==250 and not case['complete_first']:
            prior=f"{case['sport']}_t30_constant_q{case['queue']}_d{case['delay']:g}"
            old=read(M3/'results'/f'{prior}.json')
            for key in ('completed_strategy_pnl','maker_contracts','taker_contracts','unhedged_contract_hours','min_cash','max_reserved_cash'):
                audit.close(result[key],old[key],1e-7)
            matches=dict(fills=fills==list(lines(M3/'results'/f'{prior}_fills.jsonl.gz')),
                         orders=orders==list(lines(M3/'results'/f'{prior}_orders.jsonl.gz')))
            assert all(matches.values()),name
            controls.append(dict(scenario=name,exact_matches=matches))
    assert len(controls)==8
    check_freeze()
    out=dict(all_executed_passed=True,financial_audits=checks,exact_controls=controls,
             blocked_scenarios=list(summary['failures']),all_80_slots_accounted=True,frozen_hashes_match=True)
    save(ROOT/'results/verification.json',out)
    print('PASS',len(checks),'financial ledgers;',len(controls),'exact M3 controls;',len(summary['failures']),'explicitly blocked slots')


if __name__=='__main__':main()
