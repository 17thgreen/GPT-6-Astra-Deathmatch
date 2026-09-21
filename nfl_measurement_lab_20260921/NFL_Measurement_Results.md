# NFL queue measurement Q3 — results and future evaluation

September 21, 2026. **Measurement improved; no new profit improvement is established.**
The existing router and Q2 completion controller remain unchanged. This round
adds availability-aware features, censored quote/queue observations, post-fill
price diagnostics and a reserved future cohort. No live orders were placed.

## What the new measurements establish

| Development panel | Observed book span, minutes | Book snapshots | Deduplicated trade records | Nonoverlapping shadow joins per leg | Full 250-contract shadow service |
|---|---:|---:|---:|---:|---:|
| Earlier Q1 development capture | 19.66 | 476 | 4326 | 54 | 0 |
| New Q3 development capture | 11.98 | 424 | 5006 | 16 | 0 |

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
| 21NYGLAR | Final 12h | 4,680,789.16 | 1,327,847.00 | 4 / 8 |
| 24ATLGB | More than 12h | 240,087.06 | 3,300.00 | 6 / 8 |

This is a descriptive breakdown added after the measurements to retain the
existing execution regimes, not a new performance filter. These fresh public
observations do not replace historical queues and are not our order's actual
queue position. One early-window game cannot establish an NFL-wide depth model.
The early-window depth ranged from 83.46 to
386,528.39 contracts across the eight fresh-join observations,
illustrating why a single constant is fragile.

There were 840 comparable same-price depth intervals;
69 showed a decline not explained by the
recorded exact-price prints in the receipt-time interval. Cancellations,
snapshot timing, late publication and additions can all affect this residual.
It is **not credited as queue advancement** for our hypothetical order.

## Price persistence and service censoring

The new sample contains 8 displayed-price spells. Their median
observed unchanged duration is 718.68 seconds.
8 are left censored and 8 are
right censored. End reasons: {"capture_end": 8}.
These values do not estimate uninterrupted individual-order lifetimes. Price
can change and return between polls; observed changes are located within an
interval, and a gap above 30 seconds breaks observation.

Of 8 joins covered by exhausted trade pagination,
0 received any modeled service and 0
received all 250 contracts. 8 have a full ten-minute
observation horizon; 0 were cut short before full
service. **Do not divide all unfilled joins by all joins and call that a
ten-minute failure probability.** Censored waits are not completed failures.
An additional 8 joins lack tape coverage
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
| Existing Q1 router | 2 | 31 | 100.00% | -0.00777 | 0.10604 |
| Existing Q1 router | 5 | 31 | 92.46% | -0.00988 | 0.10237 |
| Existing Q1 router | 10 | 31 | 92.06% | -0.00795 | 0.10441 |
| Q2 completion controller | 2 | 10 | 100.00% | -0.00547 | 0.07656 |
| Q2 completion controller | 5 | 10 | 98.88% | 0.00031 | 0.08240 |
| Q2 completion controller | 10 | 10 | 99.37% | 0.01973 | 0.10178 |

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
-0.00186¢,
another reason to preserve per-game concentration diagnostics.

Future candles are used only as outcome measurements. A candle must have been
available by the target time under Q2's unchanged 60-second publication delay,
must describe a time after the fill and must be at most 120 seconds old. Missing
observations stay missing. These data cannot resolve a five-second markout.

## Forward shadow-fill markouts

| Horizon, seconds | Eligible first-service observations | Mean midpoint change, cents | Mean midpoint less hypothetical fill price, cents |
|---|---:|---:|---:|
| 30 | 0 | unavailable | unavailable |
| 60 | 0 | unavailable | unavailable |
| 300 | 0 | unavailable | unavailable |

These labels require fresh books and no observation gap above 30 seconds through
the horizon. They are conditional on modeled first service, not actual fills,
and the two-event sample cannot calibrate actual execution probabilities.

Feature records count only trades received before their decision time. That is
an observed subset, particularly during initialization or delayed pagination;
zero received matching volume does not establish zero total market flow. A
future fitted model will also need an explicit available-history completeness
feature before interpreting the projection as a forecast.

The new capture recorded 0 terminal request/pagination errors.
Median successful book HTTP duration was 6.43 seconds;
the 95th percentile was 9.91. Median per-market
observation gap was 6.52 seconds and the maximum
was 18.11. These are workspace-to-endpoint durations,
not exchange matching latency. A cursor-exhausted response does not guarantee
that no additional prints will be published later.

## Reserved evaluation and current status

**0 of 32 future games have completed evaluation. Status:
INSUFFICIENT.** No new model is trained, promoted or deployed.

The registry selects the first 32 schedule identities whose full seven-day
windows start after protocol freeze, excluding the 31 historical games and both
forward development events. Its schedule runs from 2026_03_PHI_CHI
(2026-09-29T00:15:00+00:00) through 2026_05_BUF_LA (2026-10-13T00:15:00+00:00).
31 venue event identities remain unresolved and must be verified.
The schedule snapshot can change; dated amendments are required, and games
cannot be silently replaced or dropped based on outcomes.

The candidate must be frozen **before 2026-09-22T00:15:00+00:00**, the first
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
passed hash checks. 44,067 historical markout
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
