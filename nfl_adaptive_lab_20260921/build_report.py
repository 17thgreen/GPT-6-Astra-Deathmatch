import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def read(name):return json.loads((ROOT/name).read_text())
def money(x):return 'Unresolved' if x is None else ('+' if x>=0 else '−')+f'${abs(x):,.2f}'
def num(x):return f'{x:,.0f}'

def main():
    s=read('results/experiment_summary.json')['scenarios']
    diag=read('results/allocation_diagnostic_summary.json')['scenarios']
    cap=read('results/capital_controls_summary.json')['scenarios']
    verified=read('results/verification.json');assert verified['all_checks_passed']
    def get(mode,q=3300,d=.25):return s[f'q{q}_d{d:g}_{mode}']
    labels={'baseline':'Existing router','inventory':'Conditional inventory targets','patience':'Flow/markout patience','allocation':'Capital-allocation bundle'}
    table=['| Policy | Queue 3,300; 0.25s | Queue 3,300; 5s | Queue 10,000; 0.25s | Queue 10,000; 5s |','|---|---:|---:|---:|---:|']
    for mode,label in labels.items():table.append('| '+label+' | '+' | '.join(money(get(mode,q,d)['completed_strategy_pnl']) for q,d in [(3300,.25),(3300,5),(10000,.25),(10000,5)])+' |')
    decisions={}
    for mode in ['inventory','patience','allocation']:
        a=get(mode);b=get('baseline');conditions={}
        conditions['beats_baseline_all_four']=all(get(mode,q,d)['completed_strategy_pnl'] is not None and get(mode,q,d)['completed_strategy_pnl']>get('baseline',q,d)['completed_strategy_pnl'] for q in [3300,10000] for d in [.25,5])
        conditions['positive_net_all_four']=all(get(mode,q,d)['completed_strategy_pnl'] is not None and get(mode,q,d)['completed_strategy_pnl']>0 for q in [3300,10000] for d in [.25,5])
        conditions['flat_all_four']=all(get(mode,q,d)['all_flat'] for q in [3300,10000] for d in [.25,5])
        conditions['improves_both_primary_weeks']=all(a['week_contributions'][w]>b['week_contributions'][w] for w in ['week1','week2'])
        conditions['primary_positive_excluding_best_two']=a['pnl_excluding_top_two_games'] is not None and a['pnl_excluding_top_two_games']>0
        conditions['inventory_hours_within_limit']=all(get(mode,q,d)['unhedged_contract_hours']<=1.25*get('baseline',q,d)['unhedged_contract_hours'] for q in [3300,10000] for d in [.25,5])
        decisions[mode]=dict(status='DEVELOPMENT_CHALLENGER' if all(conditions.values()) else 'RESEARCH_NOT_PROMOTED',conditions=conditions)
    (ROOT/'results/promotion_decision.json').write_text(json.dumps(decisions,indent=2))
    b=get('baseline');a=get('allocation');i=get('inventory');p=get('patience')
    diagnostics=['| Primary scenario: queue 3,300, 0.25s | Net P&L | Week 1 | Week 2 | Excluding best two games | Unhedged contract-hours | Taker contracts | Peak order reservations |','|---|---:|---:|---:|---:|---:|---:|---:|']
    for mode,label in labels.items():
        r=get(mode);diagnostics.append('| '+label+' | '+' | '.join([money(r['completed_strategy_pnl']),money(r['week_contributions']['week1']),money(r['week_contributions']['week2']),money(r['pnl_excluding_top_two_games']),num(r['unhedged_contract_hours']),f"{r['taker_contracts']:,.2f}",f"${r['max_reserved_cash']:,.2f}"])+' |')
    neutral=['| Early queue, 0.25s | Ranked allocation | Neutral allocation | Ranked minus neutral |','|---|---:|---:|---:|']
    for q in [3300,10000]:
        ranked=get('allocation',q)['completed_strategy_pnl'];n=diag[f'q{q}_d0.25_allocation_neutral']['completed_strategy_pnl']
        neutral.append(f'| {q:,} | {money(ranked)} | {money(n)} | {money(ranked-n)} |')
    capitals=['| Single shared account | Completed simulated net | Net / initial cash | Peak order reservations |','|---|---:|---:|---:|']
    for value in [1000,4000,5000]:
        r=cap[f'q3300_d0.25_baseline_cash{value}'];pnl=r['completed_strategy_pnl']
        capitals.append(f"| ${value:,} | {money(pnl)} | {100*pnl/value:.2f}% | ${r['max_reserved_cash']:,.2f} |" if pnl is not None else f'| ${value:,} | Unresolved | — | — |')
    text=f'''# NFL adaptive-control experiments Q5

September 21, 2026. **The capital-allocation bundle is the only one of the three
predeclared candidates to pass the development screen.** It earns
{money(a['completed_strategy_pnl'])} versus {money(b['completed_strategy_pnl'])}
for the unchanged router under the primary queue/latency assumption: an increase
of {money(a['completed_strategy_pnl']-b['completed_strategy_pnl'])}
({100*(a['completed_strategy_pnl']/b['completed_strategy_pnl']-1):.1f}%).
It remains ahead in all four queue/latency scenarios. This is a development
challenger, **not a live-profitability claim or a promoted production strategy**.

The important qualification is that neutral allocation also performs well.
The result supports further work on the entire eligibility/funding/offset-cash
bundle; it does not establish that our profit-per-dollar-hour ranking is the
source of the gain.

All main comparisons reuse the same **31 games, two weeks, one shared $5,000
account**, from T−7d through T−3h with five-minute final winddown. These games
have been examined repeatedly. There are zero completed new holdout games.
No orders were sent to Kalshi.

## The frozen 16-case matrix

{chr(10).join(table)}

Order and cancel delays both take the displayed value. Five seconds is an
execution sensitivity, not measured venue order latency. Both queues are
hypothetical early-window assumptions; the final-12h queue stays 1,327,847.005.
All 16 cases completed flat; total exit-depth allowance stayed 250 per game.

## What each experiment taught us

**1. Conditional inventory targets.** Trailing opposing flow determines a soft
25–250 target while the hard exposure/reservation cap stays 250. Target changes
include all pending orders, and reductions acknowledge after the normal delay.
It earns less than the baseline in the primary case, with a negative Week 2.
It reduces primary inventory duration by
{100*(1-i['unhedged_contract_hours']/b['unhedged_contract_hours']):.1f}%
and beats the baseline under the deeper queue. That is an inventory-risk tradeoff,
not an overall profit improvement. Status: {decisions['inventory']['status']}.

**2. Flow/markout patience.** Only order retention/admission changes; sizing,
routing and hard limits stay fixed. Previously received five-minute price
markouts, directional flow and queue depletion determine when an entry-side
order stays or cancels. The candidate loses profit relative to baseline in all
four cases, and is negative in the deeper-queue/slow-delay case. Primary new
orders rise from {num(b['metrics']['new_orders'])} to
{num(p['metrics']['new_orders'])}; there are
{num(p['metrics'].get('patience_expired_decisions',0))} patience-expiry decisions
versus {num(p['metrics'].get('adverse_markout_decisions',0))} adverse-markout veto
decisions. This is consistent with excessive churn; the run does not separately
identify the effects of every component. No post-result thresholds were tuned.
Status: {decisions['patience']['status']}.

**3. Capital allocation.** Every ten minutes, protect cash for net-inventory
offsets, admit only pairs with positive earlier flow on both sides, and rank
prospective paired profit per estimated reserved cash-hour. Retained queues and
an incumbent bonus discourage switching. Cancellations release neither cash
nor exposure before acknowledgment. The bundle improves both primary week
contributions and remains positive excluding its two best games. Primary
inventory duration falls {100*(1-a['unhedged_contract_hours']/b['unhedged_contract_hours']):.1f}%.
Status: {decisions['allocation']['status']}.

{chr(10).join(diagnostics)}

Contract-hours measure quantity and duration, not dollars at risk or drawdown.
Peak order reservations exclude money already spent on inventory. Excluding the
two best games is a concentration diagnostic, not a new untouched sample.

## Does ranking explain the gain?

After observing the allocation result, we added and separately froze two
**post-result diagnostics**. They keep the allocation arm's eligibility,
protection, cash budgets and timing, but replace its adjusted ranking value with
constant 1 and tie-break by event ID. They remove both value ranking and the
explicit incumbent multiplier. Actual queue retention/loss still applies.

{chr(10).join(neutral)}

Ranking helps at queue 3,300 and hurts at 10,000 relative to this deterministic
neutral ordering. Most of the improvement against the original router survives
without it. We therefore cannot attribute the full gain to superior opportunity
ranking, and do not promote the neutral diagnostic as a newly optimized winner.
The next mechanism study should separate flow eligibility, offset-cash protection
and funding order on fresh data with controls declared before outcomes.

## Four or five $1,000 bots: what this does and does not answer

Four wallets imply $4,000 total; five imply $5,000. Identical bots do not create
four independent copies of the available fills. They need one common queue and
trade-volume simulator. Different settings help only if their net contributions
complement each other after competition for fills and separate-wallet constraints.

For an immediate partial answer, we ran **single-account capital controls** on
the same 31 games, queue 3,300 and .25-second delays. They keep the baseline
250-order/250-event-cap policy and each reserve an additional $0.02 idle buffer.

{chr(10).join(capitals)}

Simulated profits can be reinvested, so peak reservations can temporarily exceed
initial capital. Reservations remain bounded by the account cash at that moment.

These figures are not results for one isolated game, nor for four/five bots.
**Do not multiply the $1,000 result by four or five.** The account sees the full
historical stream; independent replays would reuse the same liquidity. A proper
comparison fixes aggregate capital, exposure and exit depth. Four independent
250-event limits could permit 1,000 contracts; five could permit 1,250. That is a
larger risk budget, not evidence of a better strategy.

The initial unbuffered $1,000 control halted when the reservation guard found
cash $114.55130000000185 versus reservations $114.55132385499999. The original
code, frozen specification and traceback are retained. No completed outcome was
available. The separately frozen recovery gives all three funding levels the
same two-cent buffer; it does not relax the guard, clip fills, or change fee formulas. This
is a workaround for tight reservation headroom, not a complete repair/audit of
the inherited reservation arithmetic. The buffered $5,000 result differs from
the untouched primary baseline by
{money(cap['q3300_d0.25_baseline_cash5000']['completed_strategy_pnl']-b['completed_strategy_pnl'])}.

See MULTIBOT_EXPERIMENT_DESIGN.md for a shared-queue multi-wallet design. That
simulator has not been implemented or validated in this package. The present
result supports researching coordinated shared capital; it does not establish
that splitting capital across wallets improves profitability.

## Verification and reproducibility

The primary policies, runner, tests, specification and input manifest were
hashed before primary outcomes. Capital controls and the neutral-ranking
diagnostic have separate timestamps, freezes and provenance. The failed first
capital run is preserved; neither it nor the diagnostics is quietly folded into
the original 16-case claim. There are 21 completed runs: 16 primary, 2 neutral
allocation diagnostics and 3 buffered capital controls.

76 execution/policy unit tests pass, plus focused checks of the neutral control
and cash buffer. All 21 saved fill/order ledgers were independently recomputed,
including per-fill fixed-point fees, cash, paired payouts, positions, latency,
cutoffs, order sizes, exit-depth use, weekly contributions and decision budgets.
Both untouched primary baseline cases reproduce the Q2 financial aggregates
within 1e−7. Frozen-source and input hashes pass; compressed ledgers read through
EOF. The package retains every case, including losing strategies.

Remaining limitations include historical queue positions, cancellation allocation,
minute-quote timing, executable exit depth, fees and collateral-release mechanics,
and the market's response to hypothetical orders. The smaller capital assertion
is an additional reason to retain reservation checks in any future implementation.
Passing internal tests does not validate these execution assumptions.

The prior +$1,027.47 figure used the original engine, 16 games and queue near 291;
it is not contradicted by this 31-game, queue 3,300/10,000 comparison.

## Fresh-data status

The earlier 32-game schedule reservation and a forward-admission protocol are
included. Most venue IDs remain unresolved and complete capture is not secured.
The first reserved window starts September 22, 2026 at 00:15 UTC; missing it must be
recorded as incomplete, not reconstructed as a full-window holdout. No outcomes
from that cohort were read for this experiment. No always-on collector is
running, and no durable host or order-enabled service was deployed here.

Retain the existing production-status boundary: a development challenger is
eligible for further shadow research, not live trading. Do not combine these
three controllers based on the same reused sample.
'''
    (ROOT/'NFL_Adaptive_Results.md').write_text(text)
    print(json.dumps(dict(words=len(text.split()),decisions=decisions),indent=2))

if __name__=='__main__':main()
