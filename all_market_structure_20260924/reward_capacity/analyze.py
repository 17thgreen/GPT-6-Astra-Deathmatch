"""Descriptive fixed-size capacity; no execution or loss-probability estimator."""
import collections
import hashlib
import importlib.util
import json
from decimal import Decimal as D
from pathlib import Path

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('boundary', ROOT.parent/'reward_boundary/screen.py')
boundary = importlib.util.module_from_spec(spec)
spec.loader.exec_module(boundary)
PRINCIPAL, RESERVE, ILLUSTRATIVE_REWARD = D('2.50'), D('.25'), D('3.71')


def ledger(n, failed_fraction, reward=ILLUSTRATIVE_REWARD):
    """Deterministic severity scenario. Fractional counts denote portfolio weights."""
    n, f, reward = D(str(n)), D(str(failed_fraction)), D(str(reward))
    if n < 0 or not 0 <= f <= 1 or reward < 0:
        raise ValueError('invalid scenario input')
    stake, reserve = n*PRINCIPAL, n*RESERVE
    gross = n*(1-f)*reward
    net = gross-stake-reserve
    return dict(orders=int(n), failure_fraction=float(f), zero_reward_equivalent_orders=float(n*f),
                quote_capital=float(stake), fee_reserve=float(reserve), reward=float(gross),
                net_cushion=float(net), roi_quote_pct=float(net/stake*100) if stake else None,
                roi_funded_pct=float(net/(stake+reserve)*100) if stake else None)


def concurrent(cases):
    """Exact-response grouping, one side per market/program, no repeated-period sum."""
    groups = collections.defaultdict(dict)
    for r in cases:
        if not r['passes']:
            continue
        batch = (r['source'], r['cycle'], r['book_received_ns'])
        market = (r['ticker'], r['program_id'])
        prev = groups[batch].get(market)
        if prev is None or (r['conditional_cushion'], r['side']) > (prev['conditional_cushion'], prev['side']):
            groups[batch][market] = r
    return [dict(source=k[0], cycle=k[1], book_received_ns=k[2], orders=len(v),
                 quote_capital=round(sum(r['principal'] for r in v.values()), 2),
                 reward=round(sum(min(r['base_half_uptime_reward'], r['stressed_half_uptime_reward']) for r in v.values()), 2),
                 fee_reserve=round(sum(r['fee_stress_reserve'] for r in v.values()), 2),
                 cushion=round(sum(r['conditional_cushion'] for r in v.values()), 2),
                 candidates=[dict(ticker=r['ticker'], side=r['side'], classification=r['classification']) for r in v.values()])
            for k, v in sorted(groups.items(), key=lambda kv: (kv[0][0], kv[0][2]))]


def fixed_cases(p, m, raw, ns):
    previous = boundary.FRACTIONS
    try:
        boundary.FRACTIONS = (D(250)/D(p['target_size_fp']),)
        rows = boundary.cases(p, m, raw, ns)
        for row in rows:
            assert D(row['quantity']) == 250
        return rows
    finally:
        boundary.FRACTIONS = previous


def main():
    freeze = json.loads((ROOT/'FREEZE.json').read_text())
    for path, expected in freeze['sha256'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == expected, path
    cases, records = [], []
    readers = [boundary.census_inputs(), boundary.frame_inputs('reward_replication', 'AMS-007'),
               boundary.frame_inputs('reward_competition', 'AMS-009'),
               boundary.frame_inputs('reward_scanner', 'AMS-010 exploratory overlay')]
    counts = collections.Counter()
    for reader in readers:
        for source, cycle, p, m, b, ns in reader:
            admitted = boundary.model.admitted(p, ns/1e9)
            counts[source] += bool(admitted)
            rows = fixed_cases(p, m, b, ns)
            end = boundary.model.stamp(p['end_date'])
            duration = (end-boundary.model.stamp(p['start_date']))/60
            close = boundary.model.stamp(m['close_time']) if m else end
            for row in rows:
                row.update(source=source, cycle=cycle, duration_minutes=duration,
                           remaining_minutes=(min(end, close)-ns/1e9)/60)
                share = min(row['base']['overall_share'], row['stress']['overall_share'])
                rate = D(str(row['pool_dollars']))*D(str(share))/D(str(duration))
                row['constant_score_qualifying_minutes_to_cover_stake_and_reserve'] = float((PRINCIPAL+RESERVE)/rate) if rate else None
                row['roi_quote_pct'] = round(row['conditional_cushion']/float(PRINCIPAL)*100, 6)
                row['roi_funded_pct'] = round(row['conditional_cushion']/float(PRINCIPAL+RESERVE)*100, 6)
            cases.extend(rows)
            records.append(dict(source=source, cycle=cycle, ticker=p['market_ticker'], program_id=p['id'],
                                ns=ns, admitted=admitted, ended=ns/1e9 >= min(end, close),
                                metadata_present=m is not None, book_present=b is not None,
                                states={r['side']:r for r in rows}))
    passed = [r for r in cases if r['passes']]
    first = {}
    for r in sorted(passed, key=lambda r:r['book_received_ns']):
        first.setdefault((r['program_id'], r['ticker'], r['side']), r)
    tracks = []
    for key, r in first.items():
        later = sorted([x for x in records if (x['program_id'], x['ticker']) == key[:2]
                        and x['ns'] >= r['book_received_ns']], key=lambda x:x['ns'])
        states = []
        for x in later:
            candidate = x['states'].get(key[2])
            status = ('missing_capture' if not x['metadata_present'] or not x['book_present'] else
                      'program_ended' if x['ended'] else
                      'outside_admission' if not x['admitted'] else
                      'no_baseline_qualifying_quote' if candidate is None else
                      'positive_cushion' if candidate['passes'] else 'nonpositive_cushion')
            states.append(dict(source=x['source'], cycle=x['cycle'], ns=x['ns'], status=status,
                               cushion=candidate['conditional_cushion'] if candidate else None))
        tracks.append(dict(program_id=key[0], ticker=key[1], side=key[2], first=r, later_observed_states=states))
    batches = concurrent(cases)
    known = [r for r in cases if r['source']=='AMS-010 exploratory overlay' and r['cycle']==7
             and r['ticker']=='KXTEMPMIAH-26SEP2402-T79.99' and r['side']=='yes']
    assert len(known)==1 and D(str(known[0]['stressed_half_uptime_reward'])) == ILLUSTRATIVE_REWARD
    scenario_fractions = ['0', '.10', '.20', '.25', '.30', '.50', '1']
    output = dict(designation='reused descriptive evidence; counterfactual scaling, no actual orders',
                  eligible_observations_by_source=dict(counts),
                  baseline_qualified_fixed_quote_observations=len(cases),
                  positive_cushion_observations=len(passed),
                  nonpositive_cushion_observations=len(cases)-len(passed),
                  by_source={s:dict(baseline=sum(r['source']==s for r in cases),
                                    passing=sum(r['source']==s for r in passed)) for s in counts},
                  unique_passing_program_sides=len(first),
                  unique_passing_events=sorted({r['event_ticker'] for r in passed}),
                  passing_classifications=dict(collections.Counter(r['classification'] for r in passed)),
                  max_coobserved_orders=max((r['orders'] for r in batches), default=0),
                  passing_batches=batches, tracks=tracks, illustration=known[0],
                  quote_capital_5000_scenarios=[ledger(2000, f) for f in scenario_fractions],
                  all_in_5000_scenarios=[ledger(1818, f) for f in scenario_fractions],
                  all_in_5000_unallocated_cash=.50,
                  zero_profit_failure_fraction=float(1-(PRINCIPAL+RESERVE)/ILLUSTRATIVE_REWARD),
                  realized_pnl=None, measured_loss_rate=None)
    (ROOT/'SUMMARY.json').write_text(json.dumps(output, indent=2)+'\n')
    (ROOT/'INPUT_HASHES.json').write_text(json.dumps(boundary.INPUTS, indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k not in ('passing_batches','tracks','illustration')}, indent=2))


if __name__ == '__main__':
    main()
