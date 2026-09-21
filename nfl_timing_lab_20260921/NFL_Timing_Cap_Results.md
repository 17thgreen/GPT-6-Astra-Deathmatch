# NFL size, timing and event-cap experiment Q4

September 21, 2026. **The existing 250-contract-order / 250-contract-cap router
remains the highest-profit completed strategy in this frozen 52-case development
experiment**, at both tested queue assumptions. None of the predeclared candidates
passes the research-promotion rule. No live orders were placed.

The useful new finding is that **order size and event inventory cap must be
examined together**. With 25-contract orders, tightening the cap from 250 to 25
changes simulated completed net P&L from −$89.83
to +$26.70. Increasing the cap to 500 instead
leaves 4,343.01 contracts unresolved across games
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
| 25 | +$26.70 | +$1.44 | 68,303 | 236.04 | 0.00 |
| 50 | +$19.62 | −$10.06 | 134,951 | 828.95 | 0.00 |
| 100 | −$10.07 | −$30.70 | 260,759 | 2,090.33 | 0.00 |
| 250 | −$89.83 | −$88.80 | 532,054 | 5,844.15 | 0.00 |
| 500 | Unresolved | Unresolved | 775,889 | 6,847.44 | 4,343.01 |

At the 3,300 queue, the 25/25 configuration earns
+$19.87 from Week 1 games and
+$6.83 from Week 2 games in the pooled
account. At queue 10,000 its total shrinks to
+$1.44; this remains thin
and assumption-sensitive. It does not outperform the 250/250 benchmark's
+$201.52 at queue 3,300 or
+$10.35 at queue 10,000.

Smaller quotes do not automatically keep inventory small: the bot can repeatedly
fill the same direction until it reaches the event cap. Here, order size 25 with
cap 250 produces 5,844.15 taker closing contracts,
versus 236.04 with cap 25. This shows why the cap is a
material economic control. The model also sends replenished orders to the back
of the queue; smaller quotes can therefore lose useful priority sooner. These
mechanisms are consistent with the result, not independently isolated causal
proof about live execution.

The cap-500 cases are unresolved at both queue assumptions. Their cashflows and
terminal-payout bounds are retained in JSON. They are not counted as profitable,
loss-making completed strategies, or omitted from the experiment.

## Size and entry-window comparisons

**Assumed early queue 3,300; event cap 250**

| Entry window | 10 contracts | 25 contracts | 50 contracts | 250 contracts |
|---|---:|---:|---:|---:|
| Full seven-day window | −$101.40 | −$89.83 | −$43.87 | +$201.52 |
| 7 to 3 days | −$9.99 | −$11.00 | −$17.15 | +$21.34 |
| 3 to 1 day | −$32.43 | −$32.09 | −$12.04 | +$102.89 |
| 24 to 12 hours | −$50.52 | −$73.26 | −$49.93 | +$79.72 |
| 12 to 3 hours | −$0.72 | −$1.79 | −$3.58 | −$17.90 |

**Assumed early queue 10,000; event cap 250**

| Entry window | 10 contracts | 25 contracts | 50 contracts | 250 contracts |
|---|---:|---:|---:|---:|
| Full seven-day window | −$54.00 | −$88.80 | −$83.75 | +$10.35 |
| 7 to 3 days | −$0.57 | −$1.39 | −$1.33 | +$1.52 |
| 3 to 1 day | −$16.70 | −$33.43 | −$36.90 | −$18.15 |
| 24 to 12 hours | −$26.10 | −$44.34 | −$56.61 | +$2.71 |
| 12 to 3 hours | −$1.08 | −$2.69 | −$5.38 | −$26.88 |

These are **entry windows**, not forced exit times. After a selected entry band
ends, opening orders are canceled and bounded offset quotes manage any remaining
inventory until the common T−3h deadline. Profit and inventory time can therefore
extend beyond the named band. At the final window, the five-minute winddown still
applies. Boundary events fire even when no public trade arrives.

The primary hypothesis—25-contract orders entered 7 to 3 days before kickoff—
earns −$11.00 at queue 3,300. Its stability
variant earns +$0.00
with no trading. Neither supports that proposed early-entry approach on these
data. Zero activity is not a demonstrated profitable edge.

The strongest restricted entry band at queue 3,300 is 250-contract orders 3 to
1 day before kickoff, earning +$102.89.
Under queue 10,000 the same setup earns
−$18.15. Selecting a band after
viewing this matrix is exploratory, and the stress reversal is a reason against
promoting that selection.

## Secondary price-stability/completion bundle

| Entry window | Early queue | Completed net P&L | Unhedged contract-hours | Taker closing contracts |
|---|---:|---:|---:|---:|
| Full seven-day window | 3,300 | +$21.23 | 1,318 | 6.17 |
| Full seven-day window | 10,000 | +$3.46 | 377 | 13.56 |
| 7 to 3 days | 3,300 | +$0.00 | 0 | 0.00 |
| 7 to 3 days | 10,000 | +$0.00 | 0 | 0.00 |

The bundle uses Q2's joint entry gate and inventory completion, with a fixed
heuristic budget based on previously observed unchanged bid/ask prices: at least
120 seconds, at most 1,800 seconds, reduced by the entry deadline. Price changes,
invalid quotes or an observation gap above 180 seconds reset the age. Earlier
clock decisions cannot see a subsequently received quote.

The full-window version earns +$21.23
with 1,318 unhedged contract-hours at
queue 3,300. It is an inventory-efficiency alternative, not a profit improvement.
The bundle changes gating and completion as well as the time budget; this matrix
does not isolate the causal contribution of stability alone. It is **not a
trained competing-risk model or a calibrated fill probability**.

## Completion and capital diagnostics

| Configuration, full window and early queue 3,300 | Net P&L | Median paired-unit holding time, minutes | Peak cash reserved for orders | Pairing completed by maker fills | Orders fully filled to submitted size |
|---|---:|---:|---:|---:|---:|
| Benchmark: order 250 / cap 250 | +$201.52 | 16.01 | 4,001.97 | 98.62% | 1976 / 42986 |
| Order 25 / cap 250 | −$89.83 | 393.01 | 585.93 | 81.36% | 2352 / 54352 |
| Order 25 / cap 25 | +$26.70 | 12.79 | 403.97 | 98.87% | 1920 / 42052 |
| Stability/completion bundle: order 25 / cap 250 | +$21.23 | 3.60 | 192.58 | 99.92% | 572 / 958 |

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

The real run history contains 3 sessions, including
2 completed sessions using the same database. It contains
60 book responses and
4,930 distinct public trades, with
1 failed response(s) preserved and
2 recorded restart gap(s). SQLite integrity and checkpoint
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
