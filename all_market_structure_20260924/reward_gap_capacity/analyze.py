"""Retained missing-depth capacity and conditional capital sensitivities."""
import collections
import hashlib
import importlib.util
import json
from decimal import Decimal as D
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def module(name, path):
    spec=importlib.util.spec_from_file_location(name, path)
    obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj)
    return obj


inputs=module('boundary_inputs', ROOT.parent/'reward_boundary/screen.py')
policy=module('gap_policy', ROOT.parent/'reward_scanner/policy.py')
PRINCIPAL, RESERVE, REWARD=D(11), D('1.10'), D('16.36')


def ledger(orders, failed_fraction):
    n, f=D(orders), D(str(failed_fraction))
    if n<0 or not 0<=f<=1:raise ValueError('invalid input')
    capital, reserve=n*PRINCIPAL, n*RESERVE
    reward=n*(1-f)*REWARD;net=reward-capital-reserve
    return dict(order_sets=int(n), zero_reward_fraction=float(f),
                zero_reward_equivalent_orders=float(n*f), quote_capital=float(capital),
                fee_reserve=float(reserve), funded=float(capital+reserve), reward=float(reward),
                net_cushion=float(net), return_on_5000_pct=float(net/5000*100))


def batches(rows):
    groups=collections.defaultdict(dict)
    for row in rows:
        key=(row['source'], row['cycle'], row['book_received_ns'])
        identity=(row['ticker'], row['program_id'])
        if identity in groups[key]:assert groups[key][identity]==row
        groups[key][identity]=row
    result=[]
    for key, values in groups.items():
        plans=list(values.values())
        def total(field):return float(sum(D(str(r[field])) for r in plans))
        result.append(dict(source=key[0], cycle=key[1], book_received_ns=key[2],
                           order_sets=len(plans), side_orders=sum(len(r['quantity']) for r in plans),
                           principal=total('principal'), reserve=total('reserve'), reward=total('reward'),
                           cushion=total('cushion'), tickers=[r['ticker'] for r in plans],
                           events=sorted({r['event_ticker'] for r in plans})))
    return sorted(result, key=lambda r:r['book_received_ns'])


def main():
    for name, sha in json.loads((ROOT/'FREEZE.json').read_text())['sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha, name
    readers=[inputs.census_inputs(), inputs.frame_inputs('reward_replication','AMS-007'),
             inputs.frame_inputs('reward_competition','AMS-009'),
             inputs.frame_inputs('reward_scanner','AMS-010')]
    admitted=collections.Counter();evaluated=collections.Counter();passed=[];events={}
    for reader in readers:
        for source, cycle, p, m, book, ns in reader:
            if not inputs.model.admitted(p,ns/1e9):continue
            admitted[source]+=1
            row=policy.evaluate(p['market_ticker'],p,m,book,ns)
            if row.get('plans'):evaluated[source]+=1
            if not row['buffered_alert']:continue
            plan=row['plans'][1]
            r=dict(source=source,cycle=cycle,book_received_ns=ns,ticker=p['market_ticker'],
                   program_id=p['id'],event_ticker=m['event_ticker'],quantity=plan['quantity'],
                   start_date=p['start_date'],end_date=p['end_date'],remaining_minutes=row['remaining_minutes'],
                   principal=plan['principal'],reserve=plan['fee_stress_reserve'],
                   reward=plan['conservative_half_uptime_reward'],cushion=plan['conditional_cushion'])
            passed.append(r)
            events.setdefault(r['event_ticker'],{})[(r['ticker'],r['program_id'])]=r
    groups=batches(passed)
    by_event={}
    for event, unique in events.items():
        event_rows=[r for r in passed if r['event_ticker']==event]
        event_groups=batches(event_rows)
        first={}
        for r in sorted(event_rows,key=lambda r:r['book_received_ns']):
            first.setdefault((r['ticker'],r['program_id']),r)
        by_event[event]=dict(unique_pools=len(unique), passing_observations=len(event_rows),
                            max_coobserved_sets=max(r['order_sets'] for r in event_groups),
                            max_coobserved_principal=max(r['principal'] for r in event_groups),
                            first_candidates=list(first.values()),passing_batches=event_groups)
    original=json.loads((ROOT.parent/'reward_scanner/FIRST_ALERTS.json').read_text())
    # The source reproduction is verified separately against frozen FRAME rows;
    # this read hashes the original first-alert artifact as an additional pointer.
    inputs.INPUTS['reward_scanner/FIRST_ALERTS.json']=hashlib.sha256((ROOT.parent/'reward_scanner/FIRST_ALERTS.json').read_bytes()).hexdigest()
    reference=[r for r in passed if r['source']=='AMS-010' and r['cycle']==7 and r['ticker']=='KXTEMPMIAH-26SEP2402-T80.99']
    assert len(reference)==1 and D(str(reference[0]['reward']))==REWARD and D(str(reference[0]['principal']))==PRINCIPAL
    scenarios=['0','.1','.2','.25','.3','.5','1']
    summary=dict(designation='reused descriptive replay; no hypothetical execution or loss-rate estimate',
                 admitted_observations_by_source=dict(admitted), baseline_plan_observations_by_source=dict(evaluated),
                 passing_observations=len(passed), unique_passing_pools=sum(len(x) for x in events.values()),
                 passing_hourly_events=len(events),
                 max_coobserved_sets=max((r['order_sets'] for r in groups),default=0),
                 max_coobserved_side_orders=max((r['side_orders'] for r in groups),default=0),
                 max_coobserved_principal=max((r['principal'] for r in groups),default=0),
                 by_event=by_event, illustrative_reference=reference[0],
                 all_in_5000_scenarios=[ledger(413,f) for f in scenarios],
                 all_in_5000_unallocated_cash=2.70,
                 quote_only_5000_scenario=ledger(454,0),
                 zero_reward_break_even_fraction=float(1-(PRINCIPAL+RESERVE)/REWARD),
                 measured_loss_rate=None, realized_pnl=None)
    (ROOT/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    (ROOT/'INPUT_HASHES.json').write_text(json.dumps(inputs.INPUTS,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k not in ('by_event','illustrative_reference')},indent=2))
    for event,data in by_event.items():
        print(event,json.dumps({k:v for k,v in data.items() if k not in ('first_candidates','passing_batches')}))


if __name__=='__main__':main()
