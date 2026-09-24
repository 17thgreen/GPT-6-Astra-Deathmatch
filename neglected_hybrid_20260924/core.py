"""NH-001: causal joins, forecast scoring, and a labeled quoted-cost screen.

No network access or order placement. Inputs use probabilities/dollar prices in
[0, 1], timezone-aware ISO timestamps, and canonical race identifiers.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
import argparse
import json
import math
import random
from pathlib import Path

ARMS = {'market': 0.0, 'model': 1.0, 'hybrid_50': 0.5, 'hybrid_25': 0.25}
DECISIONS = ['2024-10-29T16:00:00Z', '2024-11-04T16:00:00Z']

def instant(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if dt.tzinfo is None:
        raise ValueError('Timezone required')
    return dt.astimezone(timezone.utc)

def probability(x) -> float:
    v = float(x)
    if not math.isfinite(v) or not 0 <= v <= 1:
        raise ValueError('Probability/price outside [0,1]')
    return v

def forecast_asof(rows, decision):
    t = instant(decision)
    eligible = []
    for r in rows:
        # Availability is the conservative upper bound on public availability,
        # not a date inside an unproven retrospective reconstruction.
        at = instant(r['available_at'])
        if r.get('provenance_status') != 'contemporaneous':
            continue
        probability(r['p_dem'])
        if t-timedelta(days=7) <= at <= t-timedelta(hours=24):
            eligible.append(r)
    if not eligible:
        return None
    latest = max(instant(r['available_at']) for r in eligible)
    ties = [r for r in eligible if instant(r['available_at']) == latest]
    if len({float(r['p_dem']) for r in ties}) != 1:
        raise ValueError('Conflicting latest forecasts')
    return ties[0]

def quote_asof(rows, decision):
    t = instant(decision)
    eligible=[]
    for r in rows:
        at=instant(r['observed_at'])
        if not t-timedelta(hours=1) <= at <= t:
            continue
        if r.get('yes_bid') is None or r.get('yes_ask') is None:
            continue
        bid,ask=probability(r['yes_bid']),probability(r['yes_ask'])
        # At the 2024 cent grid, 0/1 quotes are absent-side boundary values,
        # not an executable free contract or an informative two-sided midpoint.
        if bid > ask or bid <= 0 or ask >= 1:
            continue
        # Null or absent quantity is never replaced with fabricated depth.
        eligible.append(r)
    if not eligible:
        return None
    latest=max(instant(r['observed_at']) for r in eligible)
    ties=[r for r in eligible if instant(r['observed_at']) == latest]
    if len({(float(r['yes_bid']),float(r['yes_ask'])) for r in ties}) != 1:
        raise ValueError('Conflicting latest quotes')
    return ties[0]

def fee(price):
    p=probability(price)
    return 0.07*p*(1-p)  # unrounded illustrative standard taker fee

def trade(q, bid, ask, outcome, extra_cost=0.02, reserve=0.03):
    q,bid,ask=map(probability,(q,bid,ask))
    if bid>ask or outcome not in (0,1):
        raise ValueError('Invalid book/outcome')
    choices=[]
    for side,prob,price,payout in [('yes',q,ask,outcome),('no',1-q,1-bid,1-outcome)]:
        cost=price+fee(price)+extra_cost
        choices.append({'side':side,'price':price,'fee':fee(price),'execution_buffer':extra_cost,
                        'capital':cost,'expected_net':prob-cost,'payout':payout,
                        'net':payout-cost})
    best=max(choices,key=lambda r:(r['expected_net'],r['side']=='yes'))
    return best if best['expected_net'] > reserve + 1e-12 else None

def logloss(p,y):
    p=min(.999,max(.001,probability(p)))
    return -(y*math.log(p)+(1-y)*math.log(1-p))

def mean(xs):
    return sum(xs)/len(xs) if xs else None

def interval_by_state(rows,field,iterations=10000):
    groups=defaultdict(list)
    for r in rows:groups[r['state']].append(r[field])
    keys=sorted(groups)
    if len(keys)<2:return None
    rng=random.Random(20260924)
    vals=[]
    for _ in range(iterations):
        sampled=[x for k in rng.choices(keys,k=len(keys)) for x in groups[k]]
        vals.append(mean(sampled))
    vals.sort()
    return [vals[int(.025*(iterations-1))],vals[int(.975*(iterations-1))]]

def summarize(rows):
    output={}
    for arm in ARMS:
        trades=[r['arms'][arm]['trade'] for r in rows if r['arms'][arm]['trade']]
        net=sum(t['net'] for t in trades)
        capital=sum(t['capital'] for t in trades)
        best=sorted([t['net'] for t in trades if t['net']>0],reverse=True)[:2]
        states=sorted({r['state'] for r in rows})
        diffrows=[dict(state=r['state'],diff=r['arms'][arm]['brier']-r['arms']['market']['brier']) for r in rows]
        leave=[]
        for s in states:
            subset=[r for r in diffrows if r['state']!=s]
            if subset:leave.append(mean([r['diff'] for r in subset]))
        losses=[-t['net'] for t in trades if t['net']<0]
        output[arm]={
            'brier':mean([r['arms'][arm]['brier'] for r in rows]),
            'log_loss':mean([r['arms'][arm]['log_loss'] for r in rows]),
            'brier_delta_vs_market':mean([r['diff'] for r in diffrows]),
            'state_bootstrap_95_conditional_on_one_election':interval_by_state(diffrows,'diff'),
            'leave_one_state_out_brier_delta_range':[min(leave),max(leave)] if leave else None,
            'signals':len(trades),'hypothetical_net_dollars':net,'capital_dollars':capital,
            'hypothetical_return_on_capital':net/capital if capital else None,
            'extra_1c_cost_same_trades_net':net-.01*len(trades),
            'extra_3c_cost_same_trades_net':net-.03*len(trades),
            'excluding_best_two_winners_net':net-sum(best),
            'largest_loss_share':max(losses)/sum(losses) if losses else None,
        }
    output['no_trade']={'signals':0,'capital_dollars':0,'hypothetical_net_dollars':0}
    return output

def evaluate(data, decisions=DECISIONS):
    races=data['races']; forecasts=data['forecasts']; quotes=data['quotes']
    if len({r['race_id'] for r in races}) != len(races):
        raise ValueError('Duplicate race would double-count a terminal outcome')
    if len({r['ticker'] for r in races}) != len(races):
        raise ValueError('Duplicate market ticker')
    fg,qg=defaultdict(list),defaultdict(list)
    for r in forecasts:fg[r['race_id']].append(r)
    for r in quotes:qg[r['race_id']].append(r)
    horizons=[]
    for decision in decisions:
        rows=[];excluded=[]
        for race in sorted(races,key=lambda r:r['race_id']):
            rid=race['race_id']
            def reject(reason):excluded.append({'race_id':rid,'reason':reason})
            if race.get('mapping_status')!='verified_democratic_party_yes':
                reject('unverified_contract_mapping');continue
            if race.get('outcome_dem') not in (0,1) or not race.get('resolution_source'):
                reject('missing_verified_outcome');continue
            if instant(race['open_at'])>instant(decision) or instant(race['close_at'])<=instant(decision):
                reject('not_open_at_decision');continue
            f=forecast_asof(fg[rid],decision)
            if f is None:reject('no_eligible_contemporaneous_forecast');continue
            quote=quote_asof(qg[rid],decision)
            if quote is None:reject('no_fresh_two_sided_quote');continue
            pm=probability(f['p_dem']); bid=probability(quote['yes_bid']);ask=probability(quote['yes_ask'])
            market=(bid+ask)/2;y=race['outcome_dem']
            row={'race_id':rid,'ticker':race['ticker'],'state':race['state'],'decision':decision,
                 'forecast_available_at':f['available_at'],'forecast_source':f['source'],
                 'quote_observed_at':quote['observed_at'],'quote_kind':quote.get('kind'),
                 'p_model':pm,'p_market':market,'bid':bid,'ask':ask,'outcome_dem':y,'arms':{}}
            for arm,w in ARMS.items():
                p=w*pm+(1-w)*market
                row['arms'][arm]={'p':p,'brier':(p-y)**2,'log_loss':logloss(p,y),
                                  'trade':trade(p,bid,ask,y)}
            rows.append(row)
        summary=summarize(rows) if rows else None
        primary=summary['hybrid_50'] if summary else None
        support=bool(primary and primary['brier_delta_vs_market']<0 and primary['hypothetical_net_dollars']>0)
        horizons.append({'decision':decision,'admitted_races':len(rows),'states':len({r['state'] for r in rows}),
                         'excluded':excluded,'exclusion_counts':dict(Counter(r['reason'] for r in excluded)),
                         'summary':summary,'competitive_subset':summarize([r for r in rows if .1<=r['p_market']<=.9]) if rows else None,
                         'historical_support_screen':support,'minimum_20_race_breadth_met':len(rows)>=20,'rows':rows})
    return {'study':'NH-001','mode':'RETROSPECTIVE_QUOTED_COST_SCREEN_NOT_EXECUTION',
            'live_validation':False,'historical_fee_verified':False,
            'warning':'One election; state intervals omit national common-factor risk. Quotes lack depth. No assumed fills.',
            'horizons':horizons}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('dataset',type=Path);p.add_argument('output',type=Path)
    a=p.parse_args();result=evaluate(json.loads(a.dataset.read_text()))
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'output':str(a.output),'counts':[r['admitted_races'] for r in result['horizons']]}))
if __name__=='__main__':main()
