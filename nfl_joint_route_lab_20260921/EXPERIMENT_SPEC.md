# Q8: profitable pair access through joint routing

Specified before implementation and outcomes, 2026-09-21. User mandate: improve
queue access, profitability and market breadth; user owns forward validation.
Q7 remains the control. Same 31 reused development games, no new evidence cohort.

## Question and fixed arms

Can considering actual route pairs recover profitable access or improve completed
net profit over Q7's independently selected, subsequently guarded routes?

- `router_on`: unchanged Q7 GuardedRouter.
- `rescue`: use the unchanged Q7 decision whenever its independently chosen pair
  passes. When that pair fails, enumerate every available opposite-direction pair
  and select a positive-margin pair if one exists. Otherwise use exact Q7 fallback.
- `joint`: enumerate positive-margin pairs on every existing refresh; otherwise
  use exact Q7 fallback. Score = chosen_margin * min(leg services). Service is the
  inherited trailing-flow heuristic, NOT a fill probability. Retain an eligible
  pair consisting of two current same-price, noncanceling orders unless the best
  pair exceeds its score by the inherited 1.25 ratio (+1e-15 tolerance).

Both variants rank eligible pairs by descending score, ascending total cost,
then sorted route keys. The incumbent pair uses that same ranking. A rescue is
subject to the same pair-incumbent retention rule. No flow-positive requirement;
zero-flow ties use cost and keys. Margin is exactly Q7's fee/buffer expression.
Candidate prices, queue assumptions, trailing windows, 60s refresh, order sizing,
limits, outstanding reservations, delayed cancellations and exits are unchanged.
No queue reduction, new inside quotes, invented queue-cancellation credit, size
increase, immediate post-fill refresh, or simultaneous bots.

## Matrix, accounting and diagnostics

Three arms x queues 3300/10000 x equal submit/cancel delays .25/5s = 12 scenarios.
Each alternative has one shared $5000 account; desired order, hard event exposure
and assumed total exit depth remain 250. T-7d to T-3h, five-minute winddown,
last-12h queue 1327847.005, inherited fees and receipt-time semantics remain fixed.

Verify input and source hashes before/after; independently reconcile all 12
financial ledgers, fee rounding, positions, exits and deadlines. Four Q7 controls
must match exact uncompressed fill/order ledger hashes and financial summaries.
Report P&L, weeks, exclusion of best two games, inventory-hours, maker/taker
volume, route changes, orders and pair decisions. Pair decisions are repeated
observations, NOT independent opportunities or money saved. Queue service scores
are diagnostics, not execution guarantees. Retain failures and unresolved runs.

A variant is eligible as a development candidate only if it is flat, positive
and strictly beats Q7 in all four settings, improves both primary week totals,
is positive excluding its best two primary games, and has <=1.25x Q7 inventory
hours in every setting. If both pass, prefer rescue (smaller behavioral change).
If neither passes retain Q7, regardless of any isolated best result. No post-result
tuning, capital/exit increases, season claims or live deployment in this test.

## Separate portability build

Implement a pure payoff-vector compatibility checker and explicit market-profile
requirements. Test three-way draws, mismatched thresholds and fractional special
settlement; only fully complementary state payouts can enter this two-direction
kernel. Document actual series/rules/fees and adaptation priorities. No claim of
non-NFL P&L or automatic event admission follows from profile or algebra tests.

Commit specification first, implementation/tests/freeze next, verified results
last. Preserve all prior frozen experiment files unchanged.
