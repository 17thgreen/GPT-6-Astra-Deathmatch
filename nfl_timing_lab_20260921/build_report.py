import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
BAND_NAMES={'full':'Full seven-day window','d7_d3':'7 to 3 days','d3_d1':'3 to 1 day','h24_h12':'24 to 12 hours','h12_h3':'12 to 3 hours'}


def read(name):return json.loads((ROOT/name).read_text())
def money(v):return 'Unresolved' if v is None else ('+' if v>=0 else '−')+f'${abs(v):,.2f}'
def number(v,n=2):return '—' if v is None else f'{v:,.{n}f}'


def main():
    result=read('results/experiment_summary.json');cases=result['scenarios'];assert len(cases)==52
    assert read('results/verification.json')['all_checks_passed']
    capture=read('results/collector_verification.json')
    def get(q=3300,size=250,band='full',variant='route',cap=250):return cases[f'q{q}_s{size}_{band}_{variant}_cap{cap}']
    base=get();passing=[];decision=[]
    for variant in ['route','stable']:
        r=get(size=25,band='d7_d3',variant=variant);stress=get(q=10000,size=25,band='d7_d3',variant=variant)
        checks=dict(pooled_profit=r['completed_strategy_pnl'] is not None and r['completed_strategy_pnl']>base['completed_strategy_pnl'],
            both_week_differences=all(r['week_contributions'][w]>base['week_contributions'][w] for w in ['week1','week2']),
            inventory_no_greater=r['unhedged_contract_hours']<=base['unhedged_contract_hours'],
            positive_queue_stress=stress['completed_strategy_pnl'] is not None and stress['completed_strategy_pnl']>0)
        if all(checks.values()):passing.append(variant)
        decision.append(dict(candidate=variant,checks=checks,passes=all(checks.values())))
    (ROOT/'results/promotion_decision.json').write_text(json.dumps(dict(passing_candidates=passing,details=decision),indent=2))
    caps=[]
    for cap in [25,50,100,250,500]:
        r=get(size=25,cap=cap);stress=get(q=10000,size=25,cap=cap)
        caps.append('| '+str(cap)+' | '+money(r['completed_strategy_pnl'])+' | '+money(stress['completed_strategy_pnl'])+' | '+
            number(r['unhedged_contract_hours'],0)+' | '+number(r['taker_contracts'])+' | '+number(r['unresolved_contracts'])+' |')
    matrix=[]
    for q in [3300,10000]:
        table=['| Entry window | 10 contracts | 25 contracts | 50 contracts | 250 contracts |','|---|---:|---:|---:|---:|']
        for band,label in BAND_NAMES.items():table.append('| '+label+' | '+' | '.join(money(get(q=q,size=s,band=band)['completed_strategy_pnl']) for s in [10,25,50,250])+' |')
        matrix.append('**Assumed early queue '+f'{q:,}'+'; event cap 250**\n\n'+'\n'.join(table))
    stable=[]
    for band in ['full','d7_d3']:
        for q in [3300,10000]:
            r=get(q=q,size=25,band=band,variant='stable')
            stable.append('| '+BAND_NAMES[band]+' | '+f'{q:,}'+' | '+money(r['completed_strategy_pnl'])+' | '+number(r['unhedged_contract_hours'],0)+' | '+number(r['taker_contracts'])+' |')
    diagnostic=[]
    for label,r in [('Benchmark: order 250 / cap 250',base),('Order 25 / cap 250',get(size=25)),
                    ('Order 25 / cap 25',get(size=25,cap=25)),('Stability/completion bundle: order 25 / cap 250',get(size=25,variant='stable'))]:
        median=r['pair_holding_time_seconds']['weighted_median']
        diagnostic.append('| '+label+' | '+money(r['completed_strategy_pnl'])+' | '+number(median/60 if median is not None else None)+' | '+
            number(r['max_reserved_cash'])+' | '+number(100*r['passive_pairing_fraction'] if r['passive_pairing_fraction'] is not None else None)+'% | '+
            str(r['fully_filled_submitted_orders'])+' / '+str(r['submitted_maker_orders'])+' |')
    primary=get(size=25,band='d7_d3');small=get(size=25);tight=get(size=25,cap=25);large=get(size=25,cap=500)
    stable_full=get(size=25,variant='stable')
    complete_runs=[r for r in capture['runs'] if r['status']=='complete']
    text=f'''# NFL size, timing and event-cap experiment Q4

September 21, 2026. **The existing 250-contract-order / 250-contract-cap router
remains the highest-profit completed strategy in this frozen 52-case development
experiment**, at both tested queue assumptions. None of the predeclared candidates
passes the research-promotion rule. No live orders were placed.

The useful new finding is that **order size and event inventory cap must be
examined together**. With 25-contract orders, tightening the cap from 250 to 25
changes simulated completed net P&L from {money(small['completed_strategy_pnl'])}
to {money(tight['completed_strategy_pnl'])}. Increasing the cap to 500 instead
leaves {number(large['unresolved_contracts'])} contracts unresolved across games
under the unchanged assumed exit depth. It has no completed-profit figure.

All comparisons below use the same **31 games (16 Week 1, 15 Week 2), one shared
$5,000 account**, the original T−7d through T−3h mandate, and five-minute final
winddown. These games have been examined repeatedly; the results are development
evidence, not new holdout validation. Fees are included under the unchanged
simulation assumptions.

## Event cap: direct answer to the added question

Order size stays at 25 and entries remain allowed throughout the full window.
Only the event exposure cap changes. The 250-contract assumed total liquidation
budget per game does **not** increase with the cap.

| Event cap | Net P&L, early queue 3,300 | Net P&L, early queue 10,000 | Unhedged contract-hours at 3,300 | Taker closing contracts at 3,300 | Unresolved contracts at 3,300 |
|---|---:|---:|---:|---:|---:|
{chr(10).join(caps)}

At the 3,300 queue, the 25/25 configuration earns
{money(tight['week_contributions']['week1'])} from Week 1 games and
{money(tight['week_contributions']['week2'])} from Week 2 games in the pooled
account. At queue 10,000 its total shrinks to
{money(get(q=10000,size=25,cap=25)['completed_strategy_pnl'])}; this remains thin
and assumption-sensitive. It does not outperform the 250/250 benchmark's
{money(base['completed_strategy_pnl'])} at queue 3,300 or
{money(get(q=10000)['completed_strategy_pnl'])} at queue 10,000.

Smaller quotes do not automatically keep inventory small: the bot can repeatedly
fill the same direction until it reaches the event cap. Here, order size 25 with
cap 250 produces {number(small['taker_contracts'])} taker closing contracts,
versus {number(tight['taker_contracts'])} with cap 25. This shows why the cap is a
material economic control. The model also sends replenished orders to the back
of the queue; smaller quotes can therefore lose useful priority sooner. These
mechanisms are consistent with the result, not independently isolated causal
proof about live execution.

The cap-500 cases are unresolved at both queue assumptions. Their cashflows and
terminal-payout bounds are retained in JSON. They are not counted as profitable,
loss-making completed strategies, or omitted from the experiment.

## Size and entry-window comparisons

{(chr(10)*2).join(matrix)}

These are **entry windows**, not forced exit times. After a selected entry band
ends, opening orders are canceled and bounded offset quotes manage any remaining
inventory until the common T−3h deadline. Profit and inventory time can therefore
extend beyond the named band. At the final window, the five-minute winddown still
applies. Boundary events fire even when no public trade arrives.

The primary hypothesis—25-contract orders entered 7 to 3 days before kickoff—
earns {money(primary['completed_strategy_pnl'])} at queue 3,300. Its stability
variant earns {money(get(size=25,band='d7_d3',variant='stable')['completed_strategy_pnl'])}
with no trading. Neither supports that proposed early-entry approach on these
data. Zero activity is not a demonstrated profitable edge.

The strongest restricted entry band at queue 3,300 is 250-contract orders 3 to
1 day before kickoff, earning {money(get(band='d3_d1')['completed_strategy_pnl'])}.
Under queue 10,000 the same setup earns
{money(get(q=10000,band='d3_d1')['completed_strategy_pnl'])}. Selecting a band after
viewing this matrix is exploratory, and the stress reversal is a reason against
promoting that selection.

## Secondary price-stability/completion bundle

| Entry window | Early queue | Completed net P&L | Unhedged contract-hours | Taker closing contracts |
|---|---:|---:|---:|---:|
{chr(10).join(stable)}

The bundle uses Q2's joint entry gate and inventory completion, with a fixed
heuristic budget based on previously observed unchanged bid/ask prices: at least
120 seconds, at most 1,800 seconds, reduced by the entry deadline. Price changes,
invalid quotes or an observation gap above 180 seconds reset the age. Earlier
clock decisions cannot see a subsequently received quote.

The full-window version earns {money(stable_full['completed_strategy_pnl'])}
with {number(stable_full['unhedged_contract_hours'],0)} unhedged contract-hours at
queue 3,300. It is an inventory-efficiency alternative, not a profit improvement.
The bundle changes gating and completion as well as the time budget; this matrix
does not isolate the causal contribution of stability alone. It is **not a
trained competing-risk model or a calibrated fill probability**.

## Completion and capital diagnostics

| Configuration, full window and early queue 3,300 | Net P&L | Median paired-unit holding time, minutes | Peak cash reserved for orders | Pairing completed by maker fills | Orders fully filled to submitted size |
|---|---:|---:|---:|---:|---:|
{chr(10).join(diagnostic)}

Pair holding time starts with acquiring a unit and ends with its FIFO offset;
it is not time waiting for the first fill. Maker pairing is measured by paired
units, not by independent trades. Fully filled orders refers to their original
submitted size; a later size reduction does not count as filling that original
quantity. Peak order reservations exclude cash already spent on inventory.
Contract-hours measure quantity and duration, not monetary drawdown. Complete
per-game results, per-order records, and P&L excluding the two best games are
included for every case.

## Execution assumptions and verification

The common engine retains .25-second submit/cancel delays, .5 participation
after queue consumption, .0175/.07 maker/taker fee coefficients, .0001 balance
precision, one shared $5,000 bankroll, and a 250-contract total assumed exit-depth
budget per game. Historical quotes are minute closes with a 60-second assumed
publication delay and a 300-second freshness cap. Early queues are assumptions;
the final-twelve-hour queue stays 1,327,847.005 in every scenario. Present-day
depth is never substituted for historical depth.

Historical per-order queue position, cancellation allocation, actual receipt
and order latency, market response to hypothetical orders, fee history,
collateral-release mechanics and executable exit depth remain unverified.
Smaller caps do not repair these evidence limitations.

The 52-case rules, code and input manifest were frozen before results; the cap
sweep was added in response to the user's question **before execution began**.
55 strategy/execution tests and 9 collector tests passed. All 52 saved order and
fill ledgers were independently recomputed, checking cash, fees, netting,
inventory bounds, deadlines, order quantities and per-game/week totals. The
unchanged full-window 250/250 router exactly reproduces both Q2 regression
comparisons within 1e−7. Frozen and input hashes match; compressed ledgers were
read through EOF. Passing internal checks is not proof of executable profit.

The original +$1,027.47 figure concerned the original engine, 16 games and the
original early queue near 291. This report uses 31 games and early queues 3,300
or 10,000. It does not revise that original scenario's output.

## Restartable public collection

A GET-only SQLite recorder now preserves raw responses, first receipt/commit
times, unique trade IDs, cursor-exhausted coverage intervals and atomic trade
watermarks. It uses an exclusive writer lock and records restart gaps. An
incomplete or conflicting trade response cannot move the checkpoint forward.
The final sweep waits past the last book's fractional-second timestamp before
closing trade coverage; missing books are never backfilled with invented data.

The real run history contains {len(capture['runs'])} sessions, including
{len(complete_runs)} completed sessions using the same database. It contains
{capture['response_counts'].get('book',0):,} book responses and
{capture['distinct_trades']:,} distinct public trades, with
{capture['failed_responses']} failed response(s) preserved and
{capture['restart_gaps']} recorded restart gap(s). SQLite integrity and checkpoint
checks pass. The initial metadata requests timed out; a documented collector-only
change raised the timeout from 10 to 20 seconds. Trading code and settings did
not change.

Docker Compose configuration is supplied for a durable host. It has
not been deployed here; the bounded sessions are stopped, and **continuous
collection is not currently running**. The included two-game panel is development
data. The reserved future cohort remains pending, with no completed forward
evaluation. Its identity, freeze-deadline and full-window requirements still
apply; a missed deadline requires a newly declared future cohort before outcomes
are examined. No account credentials or live orders were used.

Official data references: [public trades and pagination](https://docs.kalshi.com/api-reference/market/get-trades),
[public orderbook](https://docs.kalshi.com/api-reference/market/get-market-orderbook),
and [event metadata](https://docs.kalshi.com/api-reference/events/get-events).
'''
    (ROOT/'NFL_Timing_Cap_Results.md').write_text(text)
    print('Report written:',len(text.split()),'words; passing predeclared candidates:',passing)


if __name__=='__main__':main()
