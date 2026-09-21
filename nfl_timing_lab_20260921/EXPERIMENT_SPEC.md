# Q4 frozen size and entry-timing experiment

Development only: the same 31 previously examined NFL games (16 Week 1,
15 Week 2), one chronological shared $5,000 account. No new holdout result and
no live orders. The Q1 router and Q2 accounting engine are copied unchanged.

## Primary matrix

Compare desired order sizes 10, 25, 50 and 250 contracts across five entry
policies: full T−7d to T−3h, T−7d to T−3d, T−3d to T−1d, T−24h to T−12h,
and T−12h to T−3h. Run each at early queues 3,300 and 10,000: 40 cases.
The last-twelve-hour queue remains 1,327,847.005. These are hypothetical queue
assumptions, not estimates inferred from current books.

The shared cash, 250-contract event exposure cap, 250-contract assumed total
exit-depth budget, maker/taker coefficients .0175/.07, .0001 balance precision,
.25-second order/cancel delays, 50% post-queue participation, minute-candle
quotes delayed 60 seconds, 300-second freshness and five-minute final winddown
are unchanged. Decreasing order size does not decrease the event exposure cap.
Replenished orders rejoin the queue; no free priority is granted to added size.

Time bands restrict **new entry**. At the end of a band, cancel opening orders
with the existing acknowledgment delay and keep bounded offsetting quotes for
inventory. Inventory can remain until the common final T−3h deadline. Thus a
band's P&L is attributable to its entry policy, not exclusively earned inside
that band. Start/end boundary clock events fire even without a public print.
The final five-minute winddown remains in force. After-band completion preserves
pending-order reservations and can overshoot during acknowledgment races; it
must not silently clip a fill or relax the 250-contract event cap.

## Secondary stability candidate

Four additional cases: size 25, entry windows full and T−7d to T−3d, at both
queues. Use Q2's joint entry gate and inventory-completion controller, replacing
its fixed 600-second service projection with a price-stability budget:
H = min(1800, max(120, observed unchanged bid/ask age)), further limited by the
entry-window end and final entry stop for new entries; inventory offsets use
the final entry stop. Reset observed age on any bid/ask change,
invalid quote or observation gap over 180 seconds. Only information available
at the decision is used; no future quote lifetime enters the rule. Unknown
stability starts at the 120-second floor. This is a fixed heuristic, **not a
fitted competing-risk model or calibrated probability of execution**. It may
reject profitable opportunities, just as Q2 did. No threshold tuning follows.

## Event-cap sensitivity requested before the experiment ran

Hold order size at 25 and use the full entry window. Compare event exposure
caps 25, 50, 100, 250 and 500 at each early queue. Cap 250 is already in the
primary matrix; eight additional runs bring the total to 52. Leave the assumed
total liquidation capacity at 250 even when the event cap is 500. Unclosed
inventory remains unresolved and cannot be called completed profit. The bankroll
and all other settings are unchanged. This separates the order-size lever from
the maximum inventory/reservation lever. These are additional exploratory
comparisons, not replacements for the predeclared candidates below.

## Predeclared decision

The primary candidate is size 25 in T−7d to T−3d, chosen before this run's
results. Its stability variant is the secondary candidate. For a research
promotion, a candidate must beat the 250-contract full-window router's pooled
completed net P&L at queue 3,300, have positive paired P&L differences in BOTH
week contributions of that same pooled account, have no greater unhedged
contract-hours, and have positive completed P&L under queue 10,000. All cases
must be flat to report completed P&L. Week contributions are not independently
reset accounts or independent validation. Other matrix winners are exploratory
discoveries; they cannot substitute for a failed predeclared candidate.

Report all 52 cases, per-game cashflows, inventory hours, median/p90 time to
offset, peak reserved cash, maker/taker volume, fully filled submitted orders,
and P&L excluding the two best games. Do not annualize, linearly scale small
orders to a larger bankroll, or count fills as independent samples.

## Collection and untouched evaluation

Build a public-GET-only recorder with finite sessions, durable append files,
an exclusive writer lock, atomic checkpoints, trade overlap/deduplication,
receipt timestamps, bounded requests, pagination exhaustion and explicit gaps.
It can repeat sessions on a user-controlled durable host; the workspace cannot
establish an unattended multiweek service by leaving a transient process alive.
Test a real stop/restart against the existing two-game development panel.

Do not collect or inspect the reserved future cohort as development data.
Freeze any selected candidate before its full trading windows start. The prior
Q3 registry is only usable if that deadline and identity/coverage requirements
are met; otherwise declare a new future cohort. No empty registry is a passed
forward test. Actual own-order queue calibration remains unavailable without
authenticated account/order evidence.
