# NFL adaptive-control experiments Q5

September 21, 2026. **The capital-allocation bundle is the only one of the three
predeclared candidates to pass the development screen.** It earns
+$342.76 versus +$201.52
for the unchanged router under the primary queue/latency assumption: an increase
of +$141.24
(70.1%).
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

| Policy | Queue 3,300; 0.25s | Queue 3,300; 5s | Queue 10,000; 0.25s | Queue 10,000; 5s |
|---|---:|---:|---:|---:|
| Existing router | +$201.52 | +$198.41 | +$10.35 | +$0.32 |
| Conditional inventory targets | +$162.13 | +$157.97 | +$27.71 | +$25.87 |
| Flow/markout patience | +$159.87 | +$157.49 | +$2.10 | −$4.09 |
| Capital-allocation bundle | +$342.76 | +$340.99 | +$67.55 | +$62.43 |

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
78.8%
and beats the baseline under the deeper queue. That is an inventory-risk tradeoff,
not an overall profit improvement. Status: RESEARCH_NOT_PROMOTED.

**2. Flow/markout patience.** Only order retention/admission changes; sizing,
routing and hard limits stay fixed. Previously received five-minute price
markouts, directional flow and queue depletion determine when an entry-side
order stays or cancels. The candidate loses profit relative to baseline in all
four cases, and is negative in the deeper-queue/slow-delay case. Primary new
orders rise from 42,986 to
97,899; there are
59,577 patience-expiry decisions
versus 23 adverse-markout veto
decisions. This is consistent with excessive churn; the run does not separately
identify the effects of every component. No post-result thresholds were tuned.
Status: RESEARCH_NOT_PROMOTED.

**3. Capital allocation.** Every ten minutes, protect cash for net-inventory
offsets, admit only pairs with positive earlier flow on both sides, and rank
prospective paired profit per estimated reserved cash-hour. Retained queues and
an incumbent bonus discourage switching. Cancellations release neither cash
nor exposure before acknowledgment. The bundle improves both primary week
contributions and remains positive excluding its two best games. Primary
inventory duration falls 19.1%.
Status: DEVELOPMENT_CHALLENGER.

| Primary scenario: queue 3,300, 0.25s | Net P&L | Week 1 | Week 2 | Excluding best two games | Unhedged contract-hours | Taker contracts | Peak order reservations |
|---|---:|---:|---:|---:|---:|---:|---:|
| Existing router | +$201.52 | +$154.07 | +$47.46 | +$31.46 | 667,959 | 2,477.87 | $4,001.97 |
| Conditional inventory targets | +$162.13 | +$178.25 | −$16.12 | +$20.07 | 141,422 | 999.39 | $2,391.51 |
| Flow/markout patience | +$159.87 | +$149.37 | +$10.50 | +$4.62 | 499,676 | 1,861.53 | $4,048.81 |
| Capital-allocation bundle | +$342.76 | +$217.13 | +$125.63 | +$178.27 | 540,358 | 1,987.49 | $3,911.32 |

Contract-hours measure quantity and duration, not dollars at risk or drawdown.
Peak order reservations exclude money already spent on inventory. Excluding the
two best games is a concentration diagnostic, not a new untouched sample.

## Does ranking explain the gain?

After observing the allocation result, we added and separately froze two
**post-result diagnostics**. They keep the allocation arm's eligibility,
protection, cash budgets and timing, but replace its adjusted ranking value with
constant 1 and tie-break by event ID. They remove both value ranking and the
explicit incumbent multiplier. Actual queue retention/loss still applies.

| Early queue, 0.25s | Ranked allocation | Neutral allocation | Ranked minus neutral |
|---|---:|---:|---:|
| 3,300 | +$342.76 | +$328.35 | +$14.42 |
| 10,000 | +$67.55 | +$78.52 | −$10.97 |

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

| Single shared account | Completed simulated net | Net / initial cash | Peak order reservations |
|---|---:|---:|---:|
| $1,000 | +$89.12 | 8.91% | $1,111.97 |
| $4,000 | +$201.21 | 5.03% | $3,939.19 |
| $5,000 | +$201.52 | 4.03% | $4,001.97 |

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
+$0.00.

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
