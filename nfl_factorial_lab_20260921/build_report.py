import json,itertools
from pathlib import Path
ROOT=Path(__file__).resolve().parent
LABELS=[''.join(map(str,x)) for x in itertools.product([0,1],repeat=3)]

def read(name):return json.loads((ROOT/name).read_text())
def money(v):return 'Unresolved' if v is None else ('+' if v>=0 else '−')+f'${abs(v):,.2f}'
def num(v):return f'{v:,.0f}'
def main():
    s=read('results/experiment_summary.json')['scenarios'];effects=read('results/factor_effects.json');selection=read('results/selection.json')
    verification=read('results/verification.json');assert verification['all_checks_passed']
    get=lambda label,q=3300,d=.25:s[f'q{q}_d{d:g}_{label}']
    funding={r['scenario']:r['funding_diagnostics'] for r in verification['cases']}
    selected=selection['selected'];primary=effects['q3300_d0.25'];full=get('111');base=get('baseline');off=get('000')
    matrix=['| F/P/R | Extra flow gate | Offset cash earmark | Portfolio ranking | Queue 3,300; .25s | Queue 3,300; 5s | Queue 10,000; .25s | Queue 10,000; 5s |','|---|---|---|---|---:|---:|---:|---:|']
    for label in ['baseline']+LABELS:
        flags=['—']*3 if label=='baseline' else ['On' if b=='1' else 'Off' for b in label]
        vals=[money(get(label,q,d)['completed_strategy_pnl']) for q,d in [(3300,.25),(3300,5),(10000,.25),(10000,5)]]
        matrix.append('| '+' | '.join([label]+flags+vals)+' |')
    attribution=['| Contribution to 111 minus original router | Queue 3,300; .25s | Queue 3,300; 5s | Queue 10,000; .25s | Queue 10,000; 5s |','|---|---:|---:|---:|---:|']
    for key,label in [('common_machinery_vs_original','Common allocator machinery'),('flow','Additional flow gate'),('protection','Cash earmark'),('ranking','Portfolio ranking'),('full_vs_original','Total improvement')]:
        vals=[]
        for q,d in [(3300,.25),(3300,5),(10000,.25),(10000,5)]:
            e=effects[f'q{q}_d{d:g}'];vals.append(money(e[key] if key in e else e['shapley'][key]))
        attribution.append('| '+' | '.join([label]+vals)+' |')
    main_table=['| Component | Mean on-minus-off, primary scenario | Range across four primary contrasts | Positive contrasts across all 16 contexts |','|---|---:|---:|---:|']
    for f,label in [('flow','Extra flow gate'),('protection','Cash earmark'),('ranking','Portfolio ranking')]:
        contrasts=[r['delta'] for r in primary['conditional_effects'][f]]
        all_contrasts=[r['delta'] for e in effects.values() for r in e['conditional_effects'][f]]
        main_table.append(f"| {label} | {money(primary['main_effects'][f])} | {money(min(contrasts))} to {money(max(contrasts))} | {sum(v>1e-8 for v in all_contrasts)} / 16 |")
    screens=['| F/P/R | Enabled factors | Passes all declared criteria? | Worst P&L retention versus 111 | Failed criteria |','|---|---:|---|---:|---|']
    for label,r in selection['screening'].items():
        failed=', '.join(k for k,v in r['conditions'].items() if not v) or 'None'
        ratio='—' if r['worst_retention_ratio'] is None else f"{100*r['worst_retention_ratio']:.1f}%"
        screens.append(f"| {label} | {r['enabled']} | {'Yes' if r['eligible'] else 'No'} | {ratio} | {failed} |")
    if selected:
        chosen=get(selected);kept=', '.join(f for f,on in zip(['extra flow gate','cash earmark','portfolio ranking'],selected) if on=='1') or 'none of the three optional factors'
        headline=f"The predeclared rule selects **{selected}**, retaining **{kept}**, for further shadow research."
        choice=f'''The selected primary case earns **{money(chosen['completed_strategy_pnl'])}**, versus
{money(base['completed_strategy_pnl'])} for the original router and
{money(full['completed_strategy_pnl'])} for the full111 policy. Its week
contributions are {money(chosen['week_contributions']['week1'])} and
{money(chosen['week_contributions']['week2'])}. Removing its two best games leaves
{money(chosen['pnl_excluding_top_two_games'])}. Unhedged contract-hours are
{num(chosen['unhedged_contract_hours'])}, versus {num(base['unhedged_contract_hours'])}
for the original router; taker closing volume is {chosen['taker_contracts']:,.2f}
contracts. Peak order reservations are ${chosen['max_reserved_cash']:,.2f}.
These inventory metrics are not monetary drawdown or maximum-loss estimates.'''
    else:
        headline='**No combination passes the predeclared simplification screen.**'
        choice='No shadow candidate was selected; retain all outcomes and investigate on fresh data before further tuning.'
    text=f'''# NFL allocation mechanism study Q6

September 21, 2026. {headline}

This study separates three optional features of the Q5 allocator: a two-sided
observed-flow admission gate (F), cash earmarking for inventory offsets (P), and
cross-game opportunity ranking with incumbent preference (R). It evaluates all
eight on/off combinations, plus the original router, under four queue/latency
scenarios: **36 runs of the same31 previously examined games, two weeks and one
shared$5,000 account per alternative**. None is an independently validated live
strategy. Zero fresh holdout games have completed in this study.

{choice}

## Results of all eight combinations

{chr(10).join(matrix)}

The delay shown applies to both order submission and cancellation. Early queue
assumptions are3,300 or10,000; the last12h queue remains1,327,847.005. Desired
order size, hard event exposure/reservation cap, and total assumed exit depth
remain250. Entries run fromT−7d toT−3h, with five-minute final winddown.
All cases use the same historical quotes, trades, fees and account precision.
No multi-bot competition or independent-wallet multiplication is simulated.

## The control that prevents a misleading conclusion

**000 is not the original router.** It still uses ten-minute event-budget
updates, proportional quote sizing, a pair-margin cushion, the inherited
within-game route selection and the common inventory-offset quantity floor.
Actual cash, pending-order reservations, event limits and cancellation delays
remain enforced. Turning P off removes only the additional cash earmark;
turning F off does not remove all uses of flow from the inherited router.

At the primary assumption, 000 earns {money(off['completed_strategy_pnl'])},
compared with {money(base['completed_strategy_pnl'])} for the original router.
That difference, {money(primary['common_machinery_vs_original'])}, belongs to the
**common allocator machinery as a bundle**, not automatically to F, P or R.
The three optional factors jointly change 000 into111 by
{money(primary['full_minus_all_off'])}.

A retrospective read of the primary000 decision log finds
{funding['q3300_d0.25_000']['shortfall_rebalances']} budget updates with a funding
shortfall out of {funding['q3300_d0.25_000']['rebalances']} updates. This diagnostic
counts requested target budgets, not executable fills or actual idle capital.
The full111 policy has funding shortfalls in
{funding['q3300_d0.25_111']['shortfall_rebalances']} of its
{funding['q3300_d0.25_111']['rebalances']} updates. Its additional earmark thus
changes which targets can be funded even while all arms retain the same actual
cash-reservation safeguards; the contrast tables measure the resulting policy
outcomes, not a universal benefit or cost of protecting cash.

A separate post-result synthetic probe identifies a concrete possible mechanism:
the original router scores a route against the cheapest possible opposite leg,
but can select two more expensive routes whose combined cost exceeds the paired
payout. In the probe it selects a pair costing$1.10 per$1 payout. The common
allocator rejects that chosen pair. This illustrates the added joint-margin
check; it does not measure how much historical P&L it caused. The probe source
and result are included, and no new strategy or threshold was added to the matrix.
The common allocator also changes timing and sizing, so its mechanisms remain
bundled. A follow-up isolated joint-margin-gate test would distinguish them.

## Which components account for the difference?

The following allocation of effects averages each component's contribution over
all six orders in which the three factors could be added (Shapley attribution).
The three factor contributions sum to111−000; adding the common-machinery
residual reproduces111−original. It is an exact accounting of these model runs,
not a live causal-effect estimate. Interactions are shared across their members.

{chr(10).join(attribution)}

A second view averages each component's on-minus-off contrast over all four
settings of the other two components. These main effects need not sum to the
full improvement when interactions exist.

{chr(10).join(main_table)}

Primary pairwise interactions (averaged over the remaining factor) are:
flow×protection {money(primary['pairwise_interactions']['flow × protection'])},
flow×ranking {money(primary['pairwise_interactions']['flow × ranking'])}, and
protection×ranking {money(primary['pairwise_interactions']['protection × ranking'])}.
The three-way interaction is {money(primary['three_way_interaction'])}.
All conditional contrasts and all four scenario decompositions are retained in
results/factor_effects.json. A sign change across settings means a feature's
value depends on the rest of the policy; it should not be called universally
helpful or harmful from one result.

## Selection was fixed before results

To qualify, an arm must finish flat and positive, beat the original router at
all four queue/latency settings, improve both primary week contributions, remain
positive without its best two primary games, and keep inventory contract-hours
within1.25× the original router in every scenario. It must also retain at least
95% of111 P&L in every scenario. Then select the fewest enabled factors; ties
use the highest worst-scenario retention ratio, then ascending bit label.

The95% threshold is an engineering tolerance, not a statistical noninferiority
claim. Fewer flags means simpler within this allocator framework, not necessarily
fewer total rules than the original router. No parameters were retuned after
viewing the matrix, and the selection is not a production promotion.

{chr(10).join(screens)}

SHADOW_CANDIDATE_FREEZE.json records the selected flags, exact code/input hashes,
common configuration, stress assumptions and selection record. That file is an
immutable research handoff for the delivered version; it does not launch or
operate a collector or trading service.

## Verification and limitations

94 preregistered unit tests passed, plus the separate synthetic probe described
above. The tests cover inherited accounting, partial fills, delayed
cancels/resizes, queue priority, factor isolation, missing flow, timer causality,
and known analytical main/interaction/Shapley effects. The36 fill/order/decision
ledgers were independently checked for cash, fees, paired payouts, exposure,
exit-depth use, deadlines, order quantities, week attribution and factor/budget
rules. Frozen-source and input hashes match; all compressed ledgers read through
EOF. Ten prior Q5 cases reproduce both their financial aggregates and exact
uncompressed fill/order ledger hashes: four original-router cases, four111
cases and two110 neutral controls.

These checks establish reproducibility, not actual historical execution. Queue
positions, cancellations ahead, quote timing, market impact, exit liquidity,
fee history and netting/collateral mechanics remain execution assumptions.
Inventory contract-hours measure quantity and time, not cash drawdown. Comparing
36 versions on repeatedly examined31games does not create new evidence or36
independent samples. Only two weeks are represented; no precise confidence
interval or p-value is supplied as evidence of a durable live edge.

The inherited execution engine is unchanged. Q5's small-wallet reservation
failure and two-cent capital-control workaround are not silently introduced
into this5k factorial study. Assertions remain enabled, and failures cannot
be presented as completed P&L. No real orders were placed.

## Fresh-data next step

Use the frozen selected configuration alongside the original router and full111
on an admitted fresh cohort, preserving the same receipt stream, budget, risk
limits and conservative queue treatment. The existing32-game schedule-only
reservation and admission protocol are supplied. Most venue IDs remain
unresolved; continuous book capture has not been deployed. The first reserved
window starts2026-09-22T00:15UTC. A missed full window must be marked incomplete;
replacement requires a new pre-outcome schedule admission.

No always-on recorder is running, and this task has not created fresh future
outcomes. Establish durable collection before treating the selected candidate
as a prospective test. Combining additional strategies or wallets now would
introduce new variables before this mechanism is checked on unseen games.
'''
    # Space compact numerical references in prose without touching table labels or code identifiers.
    for old,new in [('full111','full 111'),('costing$1.10 per$1','costing $1.10 per $1'),('primary000','primary 000'),('same31','same 31'),('shared$5,000','shared $5,000'),('full111','full 111'),('are3,300 or10,000','are 3,300 or 10,000'),('last12h','last 12h'),('remains1,327,847','remains 1,327,847'),('remain250','remain 250'),('fromT−7d toT−3h','from T−7d to T−3h'),('into111','into 111'),('to111−000','to 111−000'),('reproduces111−original','reproduces 111−original'),('within1.25','within 1.25'),('of111','of 111'),('The95%','The 95%'),('The36','The 36'),('four111','four 111'),('two110','two 110'),('examined31games','examined 31 games'),('or36','or 36'),('this5k','this $5k'),('existing32-game','existing 32-game'),('starts2026-09-22T00:15UTC','starts 2026-09-22 at 00:15 UTC')]:text=text.replace(old,new)
    (ROOT/'NFL_Allocation_Factorial_Results.md').write_text(text)
    print(json.dumps(dict(selected=selected,words=len(text.split())),indent=2))
if __name__=='__main__':main()
