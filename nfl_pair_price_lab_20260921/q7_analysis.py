"""Predeclared Q7 selection and post-fill diagnostics; never imported by a policy."""
import bisect
import gzip
import json
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parent
ARMS=['router_off','router_on','allocator_off','allocator_on']


def selection(scenarios):
    checks={}
    for q in [3300,10000]:
        for delay in [.25,5]:
            prefix=f'q{q}_d{delay:g}_'
            base,candidate,reference=(scenarios[prefix+a] for a in ['router_off','router_on','allocator_on'])
            p,b,ref=(x['completed_strategy_pnl'] for x in [candidate,base,reference])
            checks[prefix+'flat_positive']=candidate['all_flat'] and p is not None and p>0
            checks[prefix+'beats_router']=p is not None and b is not None and p>b
            checks[prefix+'retains_allocator']=p is not None and ref is not None and ref>0 and p>=.95*ref
            checks[prefix+'inventory_limit']=candidate['unhedged_contract_hours']<=1.25*base['unhedged_contract_hours']
    base=scenarios['q3300_d0.25_router_off'];candidate=scenarios['q3300_d0.25_router_on']
    for week in ['week1','week2']:
        checks[week+'_improvement']=candidate['week_contributions'][week]>base['week_contributions'][week]
    x=candidate['pnl_excluding_top_two_games']
    checks['positive_without_best_two']=x is not None and x>0
    return dict(selected='router_on' if all(checks.values()) else None,
                retained_candidate='router_on' if all(checks.values()) else 'Q6_000',
                checks=checks,failed=[k for k,v in checks.items() if not v],
                status='DEVELOPMENT_SHADOW_CANDIDATE_ONLY',fresh_games=0)


def differences(scenarios):
    out={}
    for q in [3300,10000]:
        for delay in [.25,5]:
            prefix=f'q{q}_d{delay:g}_';p={a:scenarios[prefix+a]['completed_strategy_pnl'] for a in ARMS}
            if any(x is None for x in p.values()):
                out[prefix[:-1]]=dict(pnl=p,status='UNRESOLVED_NO_COMPLETE_CONTRAST');continue
            router=p['router_on']-p['router_off'];allocator=p['allocator_on']-p['allocator_off']
            out[prefix[:-1]]=dict(pnl=p,guard_effect_router=router,guard_effect_allocator=allocator,
                interaction=allocator-router,architecture_effect_guard_off=p['allocator_off']-p['router_off'],
                architecture_effect_guard_on=p['allocator_on']-p['router_on'])
    return out


def fill_markout(fill,times,quotes):
    target=fill['at']+300;i=bisect.bisect_right(times,target)-1
    if i<0:return None
    quote=quotes[i]
    if not (fill['at']<quote['asof']<=target and target-quote['asof']<=120 and
            0<quote['bid']<quote['ask']<1):return None
    initial=fill.get('outcome_mid_at_fill')
    if initial is None:return None
    midpoint=(quote['bid']+quote['ask'])/2
    mark=midpoint if fill['outcome']=='yes' else 1-midpoint
    return dict(change=mark-initial,entry_fee_mark=mark-fill['price']-fill['fee']/fill['size'],
                quote_received_at=quote['at'],quote_asof=quote['asof'],target=target)


def markouts(scenarios):
    quotes=defaultdict(list)
    with gzip.open(ROOT/'inputs/events.jsonl.gz','rt') as f:
        for line in f:
            row=json.loads(line)
            if row.get('kind')=='quote':quotes[row['ticker']].append(row)
    times={t:[x['at'] for x in rows] for t,rows in quotes.items()}
    out={}
    for name in scenarios:
        totals=defaultdict(lambda:dict(total=0.,covered=0.,change_sum=0.,entry_fee_sum=0.,adverse_size=0.))
        with gzip.open(ROOT/'results'/f'{name}_fills.jsonl.gz','rt') as f:
            for line in f:
                fill=json.loads(line)
                if fill['kind']!='maker':continue
                g=totals[fill['event']];qty=fill['size'];g['total']+=qty
                m=fill_markout(fill,times.get(fill['ticker'],[]),quotes.get(fill['ticker'],[]))
                if m is None:continue
                g['covered']+=qty;g['change_sum']+=qty*m['change'];g['entry_fee_sum']+=qty*m['entry_fee_mark']
                if m['change']<0:g['adverse_size']+=qty
        aggregate={k:sum(v[k] for v in totals.values()) for k in ['total','covered','change_sum','entry_fee_sum','adverse_size']}
        def finalize(g):
            return dict(**g,coverage=g['covered']/g['total'] if g['total'] else None,
                midpoint_change_cents=100*g['change_sum']/g['covered'] if g['covered'] else None,
                entry_fee_markout_cents=100*g['entry_fee_sum']/g['covered'] if g['covered'] else None,
                adverse_fraction=g['adverse_size']/g['covered'] if g['covered'] else None)
        out[name]=dict(aggregate=finalize(aggregate),per_game={e:finalize(g) for e,g in totals.items()})
    return out


def money(x):return 'Unresolved' if x is None else f'${x:+,.2f}'


def main():
    summary=json.loads((ROOT/'results/experiment_summary.json').read_text())
    verify=json.loads((ROOT/'results/verification.json').read_text())
    assert verify['all_checks_passed'] and len(summary['scenarios'])==16 and not summary['failures']
    scenarios=summary['scenarios'];selected=selection(scenarios);effects=differences(scenarios);marks=markouts(scenarios)
    for name,value in [('selection',selected),('effects',effects),('markouts',marks)]:
        (ROOT/'results'/f'{name}.json').write_text(json.dumps(value,indent=2,allow_nan=False))
    lines=['# Q7 chosen-pair price study','',
        'Same 31 repeatedly examined games, two weeks and one shared $5,000 account per alternative. '
        'All returns below are completed hypothetical historical net after modeled fees. Zero fresh validation games.', '',
        '| Architecture / guard | Queue 3,300; .25s | Queue 3,300; 5s | Queue 10,000; .25s | Queue 10,000; 5s |',
        '|---|---:|---:|---:|---:|']
    for arm in ARMS:
        lines.append('| '+arm+' | '+' | '.join(money(scenarios[f'q{q}_d{d:g}_{arm}']['completed_strategy_pnl']) for q in [3300,10000] for d in [.25,5])+' |')
    lines+=['','## Within-simulator contrasts','',
        '| Scenario | Guard effect, router | Guard effect, allocator | Interaction |',
        '|---|---:|---:|---:|']
    for name,e in effects.items():
        lines.append('| '+name+' | '+' | '.join(money(e.get(k)) for k in ['guard_effect_router','guard_effect_allocator','interaction'])+' |')
    lines+=['','The interaction is allocator guard effect minus router guard effect. The guard uses existing '
        'refresh timing in the router and existing ten-minute budget timing in the allocator. '
        'These are policy effects within the same simulator, not live causal-effect estimates.','',
        '## Predeclared selection','',
        f"Selected simpler router: **{selected['selected'] or 'NONE'}**. Retained shadow research candidate: **{selected['retained_candidate']}**.",
        'Failed criteria: '+(', '.join(selected['failed']) or 'none')+'.',
        'The 95% retention test is an engineering tolerance, not statistical noninferiority or live promotion.','',
        '## Primary scenario diagnostics','',
        '| Arm | Week 1 | Week 2 | Without best two | Inventory contract-hours | Taker contracts | Residual |',
        '|---|---:|---:|---:|---:|---:|---:|']
    for arm in ARMS:
        r=scenarios['q3300_d0.25_'+arm]
        lines.append(f"| {arm} | {money(r['week_contributions']['week1'])} | {money(r['week_contributions']['week2'])} | {money(r['pnl_excluding_top_two_games'])} | {r['unhedged_contract_hours']:,.0f} | {r['taker_contracts']:,.2f} | {r['unresolved_contracts']:,.2f} |")
    lines+=['','Inventory contract-hours are not monetary drawdown. Residual inventory is excluded from completed profit.','',
        '## Five-minute adverse movement diagnostics','',
        '| Arm, primary scenario | Contract coverage | Midpoint change, cents | Entry-fee-adjusted midpoint markout, cents | Adverse fraction |',
        '|---|---:|---:|---:|---:|']
    for arm in ARMS:
        m=marks['q3300_d0.25_'+arm]['aggregate']
        if m['covered']:
            lines.append(f"| {arm} | {m['coverage']:.2%} | {m['midpoint_change_cents']:.5f} | {m['entry_fee_markout_cents']:.5f} | {m['adverse_fraction']:.2%} |")
        else:lines.append(f'| {arm} | unavailable | unavailable | unavailable | unavailable |')
    lines+=['','Marks use only quotes received by fill+300 seconds, with post-fill asof time and at most '
        '120 seconds of age. Missing quotes remain missing. These are midpoint diagnostics, not executable '
        'exit prices; they omit exit fees. Different policies select different fill populations.','',
        '## Verification and limits','',
        'All sixteen financial ledgers reconcile independently, including fixed-point fees, paired payouts, '
        'cash, positions, deadlines, quantities, exit capacity and week contributions. All eight unchanged '
        'Q6 controls match exact uncompressed fill/order hashes and financial aggregates. Source/input '
        'hashes are frozen and checked; new guard decisions were independently inspected. '
        'See results/verification.json and results/unit_tests.txt.', '',
        'Historical queue position, cancellation allocation, publication and order latency, fee history, '
        'collateral/netting, market response and executable exit liquidity remain assumptions. '
        'No live orders, fresh holdout completion or continuous recorder deployment occurred. '
        'The prior full-window reservation begins 2026-09-22T00:15Z and cannot be backdated.', '']
    (ROOT/'Q7_RESULTS.md').write_text('\n'.join(lines))
    print(json.dumps(dict(selection=selected,effects=effects),indent=2))


if __name__=='__main__':main()
