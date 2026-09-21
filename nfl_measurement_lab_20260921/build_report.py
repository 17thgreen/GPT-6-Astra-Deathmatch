import json
from datetime import datetime,timezone,timedelta
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def load(name):return json.loads((ROOT/name).read_text())
def fmt(x,n=2):return 'unavailable' if x is None else f'{x:,.{n}f}'


def main():
    q1=load('results/q1_development_summary.json');q3=load('results/q3_development_summary.json')
    historical=load('results/historical_markout_summary.json')['summaries']
    registry=load('HOLDOUT_MANIFEST.json');gate=load('results/holdout_status.json')
    verification=load('results/verification.json');assert verification['all_checks_passed']
    first=registry['holdout_games'][0];last=registry['holdout_games'][-1]
    freeze_deadline=datetime.fromisoformat(first['kickoff'])-timedelta(days=7)
    rows=[]
    for name,r in [('Earlier Q1 development capture',q1),('New Q3 development capture',q3)]:
        rows.append('| '+name+' | '+fmt((r['last_book']-r['first_book'])/60)+' | '+str(r['book_snapshots'])+' | '+
            str(r['deduplicated_trades'])+' | '+str(r['shadow_joins'])+' | '+str(r['full_service_joins'])+' |')
    hist=[]
    for name,key in [('Existing Q1 router','q1_route'),('Q2 completion controller','pair_complete')]:
        for h in (120,300,600):
            v=historical[key][str(h)]
            hist.append('| '+name+' | '+str(h//60)+' | '+str(v['games'])+' | '+fmt(100*v['contract_coverage_fraction'])+'% | '+
                fmt(v['midpoint_change_cents'],5)+' | '+fmt(v['fee_adjusted_midpoint_markout_cents'],5)+' |')
    marks=[]
    for h in (30,60,300):
        v=q3['shadow_markouts'][str(h)]
        marks.append('| '+str(h)+' | '+str(v['n'])+' | '+fmt(v['mean_midpoint_change_cents'],5)+' | '+fmt(v['mean_midpoint_less_fill_cents'],5)+' |')
    missing_identity=sum(g['event'] is None for g in registry['holdout_games'])
    context=load('results/queue_context.json')['q3_development']
    queue_rows=[]
    for r in context:
        queue_rows.append('| '+r['event'].split('26SEP')[1]+' | '+('More than 12h' if r['regime']=='early_over_12h' else 'Final 12h')+' | '+
            fmt(r['median_depth'])+' | '+fmt(r['reference_assumption'])+' | '+str(r['above_reference'])+' / '+str(r['joins'])+' |')
    early=next(r for r in context if r['regime']=='early_over_12h')
    text=f'''# NFL queue measurement Q3 — results and future evaluation

September 21, 2026. **Measurement improved; no new profit improvement is established.**
The existing router and Q2 completion controller remain unchanged. This round
adds availability-aware features, censored quote/queue observations, post-fill
price diagnostics and a reserved future cohort. No live orders were placed.

## What the new measurements establish

| Development panel | Observed book span, minutes | Book snapshots | Deduplicated trade records | Nonoverlapping shadow joins per leg | Full 250-contract shadow service |
|---|---:|---:|---:|---:|---:|
{chr(10).join(rows)}

Both panels observe the same two NFL events: NYG–LAR and ATL–GB. They are
development measurements, not independent games or holdout results. Trade
counts include a trailing-hour initialization and overlapping queries after
deduplication, so they are not counts of trades during only the displayed span.
The new capture stopped after its bounded run; no recorder remains operating.
Both panels were analyzed under Q3's new nonoverlapping, gap-censored definition;
their join counts are not the overlapping join counts from the earlier Q1 report.

The prior replay uses different queue assumptions before and during the final
twelve hours. Preserve that distinction when describing today's depth:

| Event | Pregame interval | Median displayed entry depth | Corresponding Q2 queue assumption | Entries above that assumption |
|---|---|---:|---:|---:|
{chr(10).join(queue_rows)}

This is a descriptive breakdown added after the measurements to retain the
existing execution regimes, not a new performance filter. These fresh public
observations do not replace historical queues and are not our order's actual
queue position. One early-window game cannot establish an NFL-wide depth model.
The early-window depth ranged from {fmt(early['minimum_depth'])} to
{fmt(early['maximum_depth'])} contracts across the eight fresh-join observations,
illustrating why a single constant is fragile.

There were {q3['depth_intervals']} comparable same-price depth intervals;
{q3['intervals_with_unexplained_decline']} showed a decline not explained by the
recorded exact-price prints in the receipt-time interval. Cancellations,
snapshot timing, late publication and additions can all affect this residual.
It is **not credited as queue advancement** for our hypothetical order.

## Price persistence and service censoring

The new sample contains {q3['quote_spells']} displayed-price spells. Their median
observed unchanged duration is {fmt(q3['median_observed_spell_seconds'])} seconds.
{q3['left_censored_spells']} are left censored and {q3['right_censored_spells']} are
right censored. End reasons: {json.dumps(q3['spell_end_reasons'],sort_keys=True)}.
These values do not estimate uninterrupted individual-order lifetimes. Price
can change and return between polls; observed changes are located within an
interval, and a gap above 30 seconds breaks observation.

Of {q3['tape_complete_joins']} joins covered by exhausted trade pagination,
{q3['any_service_joins']} received any modeled service and {q3['full_service_joins']}
received all 250 contracts. {q3['full_horizon_observed']} have a full ten-minute
observation horizon; {q3['censored_before_full']} were cut short before full
service. **Do not divide all unfilled joins by all joins and call that a
ten-minute failure probability.** Censored waits are not completed failures.
An additional {q3['shadow_joins']-q3['tape_complete_joins']} joins lack tape coverage
through their entire observed endpoint and are excluded from service counts;
they remain in the delivered labels, rather than becoming zero-fill outcomes.

The model subtracts the initial displayed quantity from subsequent exact-price
opposite-taker volume, then applies 50% participation, with a .25-second assumed
arrival delay. It gives no credit for cancellations. Those assumptions do not
provide a strict upper/lower fill bound: actual arrival depth, order identity,
transient prices and the market's response to a hypothetical order are unknown.

## Price movement after historical hypothetical fills

These diagnostics use the **same previously examined 31 games**, the 3,300
assumed early queue and the two saved Q2 fill ledgers. They introduce no new
backtest profit figure. The completion controller traded only ten of those
games. Each observation is weighted by contracts, and games are also reported
separately in the data package.

| Policy | Horizon, minutes | Games with fills observed | Contract coverage | Midpoint change after fill, cents | Future midpoint less fill price and entry fee, cents |
|---|---:|---:|---:|---:|---:|
{chr(10).join(hist)}

At five minutes the router's average midpoint change is approximately −0.01¢,
and its fee-adjusted midpoint markout is approximately +0.10¢ per contract.
This suggests execution quality and throughput deserve priority before adding
a directional filter, **within this development sample**. These small averages
do not establish absence of adverse selection. Minute data miss short-lived
moves, and the fill set itself depends on the replay's assumptions.

Midpoint markout is not an executable exit value or completed profit; it omits
the future offset/exit fee and any cost of crossing the spread. The policies
select different fills, so their averages are not a controlled causal estimate
of improved trade quality. At ten minutes, the completion policy's positive
volume-weighted movement coexists with an equal-game mean of
{fmt(historical['pair_complete']['600']['equal_game_mean_midpoint_change_cents'],5)}¢,
another reason to preserve per-game concentration diagnostics.

Future candles are used only as outcome measurements. A candle must have been
available by the target time under Q2's unchanged 60-second publication delay,
must describe a time after the fill and must be at most 120 seconds old. Missing
observations stay missing. These data cannot resolve a five-second markout.

## Forward shadow-fill markouts

| Horizon, seconds | Eligible first-service observations | Mean midpoint change, cents | Mean midpoint less hypothetical fill price, cents |
|---|---:|---:|---:|
{chr(10).join(marks)}

These labels require fresh books and no observation gap above 30 seconds through
the horizon. They are conditional on modeled first service, not actual fills,
and the two-event sample cannot calibrate actual execution probabilities.

Feature records count only trades received before their decision time. That is
an observed subset, particularly during initialization or delayed pagination;
zero received matching volume does not establish zero total market flow. A
future fitted model will also need an explicit available-history completeness
feature before interpreting the projection as a forecast.

The new capture recorded {q3['errors']} terminal request/pagination errors.
Median successful book HTTP duration was {fmt(q3['median_http_seconds'])} seconds;
the 95th percentile was {fmt(q3['p95_http_seconds'])}. Median per-market
observation gap was {fmt(q3['median_observation_gap'])} seconds and the maximum
was {fmt(q3['max_observation_gap'])}. These are workspace-to-endpoint durations,
not exchange matching latency. A cursor-exhausted response does not guarantee
that no additional prints will be published later.

## Reserved evaluation and current status

**{gate['completed_games']} of 32 future games have completed evaluation. Status:
{gate['status']}.** No new model is trained, promoted or deployed.

The registry selects the first 32 schedule identities whose full seven-day
windows start after protocol freeze, excluding the 31 historical games and both
forward development events. Its schedule runs from {first['game_id']}
({first['kickoff']}) through {last['game_id']} ({last['kickoff']}).
{missing_identity} venue event identities remain unresolved and must be verified.
The schedule snapshot can change; dated amendments are required, and games
cannot be silently replaced or dropped based on outcomes.

The candidate must be frozen **before {freeze_deadline.isoformat()}**, the first
reserved window's scheduled start. If that deadline is missed, this registry
is ineligible for that candidate; select a new future registry before accessing
its outcomes. The structural gate rejects absent code/settings/data hashes,
development overlap, duplicate or missing identities, partial windows,
unresolved inventory and unshared/reset bankrolls. Passing that checklist only
makes an independently audited comparison eligible; it does not establish
profitability or live executability.

The full-window evaluation requires an operating recorder on a durable host.
This package contains a bounded collector and measurement/evaluation tools;
it does not create an unattended service or claim that future capture is active.

## Decision and handoff

Keep Q1 as the current profit benchmark. Retain Q2 as the inventory-efficiency
alternative. Use the new receipt-aware features and censored service labels to
collect a larger development set before fitting a completion model. Any later
candidate should price the cost of waiting and failed completion using observed
quote persistence and adverse movement, then face the frozen future comparison.
The present data do not justify a new entry threshold or replacing either engine.

**Validation:** 23 focused tests passed. Both public captures and frozen files
passed hash checks. {verification['historical_markout_rows']:,} historical markout
rows passed availability/age checks and aggregate reconciliation. Shadow joins
were checked for per-leg nonoverlap, queue subtraction, delayed information and
censoring. All compressed inputs and outputs were read through EOF. These are
measurement controls, not evidence that hypothetical fills occurred.

The kit contains code, input extracts, both public samples, separate feature and
label records, per-game historical diagnostics, frozen protocol/registry,
verification and a file-hash manifest. It reproduces offline with the Python
standard library; see README.md.

Official references: [public orderbook representation](https://docs.kalshi.com/api-reference/market/get-market-orderbook),
[public trades and pagination](https://docs.kalshi.com/api-reference/market/get-trades),
and [authenticated own-order queue position](https://docs.kalshi.com/api-reference/orders/get-order-queue-position).
Public displayed depth and authenticated own-order queue position are different
measurements; the latter requires an order and account authentication.
'''
    (ROOT/'NFL_Measurement_Results.md').write_text(text)
    print('Report written:',len(text.split()),'words')


if __name__=='__main__':main()
