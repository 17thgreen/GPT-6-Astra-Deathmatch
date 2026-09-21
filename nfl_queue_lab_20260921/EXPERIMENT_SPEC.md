# Queue experiment Q1 — frozen before new strategy results

2026-09-21. Development research; no live orders. All 16 previously examined 2026 NFL week-one games and their original, hash-checked public trade/candle captures. No new holdout claim.

## Common controls

One $5,000 account; 250-contract desired order and worst-case event exposure cap; joint cash reservations; 50% hypothetical participation after queue consumption; 250-contract total assumed liquidation capacity per event; 0.25s submit/cancel delays; 60s reevaluation; historical closing quotes available after a 60s assumed publication delay, at most 300s old. T−7 days to T−3 hours, with entry stopped and liquidation started five minutes before the latter deadline. Fixed maker/taker fee coefficients .0175/.07 and .0001 account precision. Preserve the baseline's stated collateral and taker-exit assumptions. All parameters are research choices, not fitted estimates.

The repaired baseline ALREADY retains same-price orders. No credit for implementing that feature again. Run its earlier wind-down result as an exact regression check.

## Primary comparisons

Run each policy with early queue 290.595 and 3,300, keeping the original last-12-hours queue 1,327,847.005 unchanged:

1. `preserve`: unchanged baseline behavior.
2. `churn60`: cancel orders at the next reevaluation once their resting age reaches 60s, then replace only through the normal refresh loop. This deliberately bad counterfactual measures queue loss AND interruption, not pure priority loss alone.
3. `route`: select one team-market leg for each event payoff direction, using only earlier trailing-60-minute eligible aggressor volume. Rank estimated net maker-pair margin times a bounded 10-minute service fraction; include current queue remaining for incumbents, or assumed initial queue for new orders. Service fraction = min(1, flow_rate * 600 / (queue + desired_size / .5)). It is a ranking heuristic, NOT a calibrated fill probability. Keep an incumbent unless the challenger score is >1.25 times incumbent score. No positive margin means no new route. Cancel before allocating replacement exposure; pending orders stay reserved. With zero service scores, retain an eligible incumbent or choose cheapest fee-inclusive leg.
4. `improve_exit`: baseline routing; move an inventory-offsetting quote inward by at most one cent only with a >=2-cent spread and a strictly passive resulting price. Quantity is capped by unmatched inventory after reservations for other offset orders. Every remaining FIFO entry lot must leave >=0.1 cent per paired unit after modeled maker fees and conservative rounding allowance. No improvement of flat-inventory entry quotes. Existing cancellation races remain modeled.
5. `combined`: route plus improve_exit.

For `improve_exit` and `combined`, repeat both early-queue regimes with 250 hypothetical competing contracts at a newly improved price instead of zero. These four race cases are mandatory sensitivity checks, not candidates selected after results.

## Evidence restrictions

Historical per-leg depth is missing. Do not backcast current snapshots into September 3–14. Routing simulations inherit assumed queues; improvement inserts a hypothetical quote into a tape generated without it. Unobserved competing quotes, market response and actual publication/receipt latency prevent claiming executable improvement. No realistic profitability claim from the largest simulated P&L.

Only trades timestamped strictly before a routing decision enter its flow estimate. Future quotes may be used for explicitly ex-post markouts, never decisions. Missing markouts are counted rather than filled in.

## Outputs and validation

Report completed P&L only if all windows complete and inventory is flat; otherwise payout bounds and residuals. Report traded size, fees, cancellation count, paired-unit holding times, 1/5-minute signed price movement after maker fills, improvement usage, game concentration, and deadline/exposure checks. Regression against earlier wind-down result, plus meaningful tests of priority retention, causal flow, route switching/cancel reservations, no crossing, inventory/fee gate and race queues.

## Public REST measurement

Bounded 120 rounds about five seconds apart on the same next two schedule-selected events previously sampled: NYG–LAR September 21 and ATL–GB September 24. Record both team books with request/receipt times and raw responses. Capture trailing-hour public trades initially and overlapping incremental intervals every sixth round, with complete pagination or explicit error. Evaluate per-leg depth/eligible flow, quote persistence, hypothetical join service and routing choices. This short observation is instrumentation evidence, not a week-long strategy return. Public snapshots cannot reveal whether canceled size was ahead of a hypothetical order, and cannot measure our own exact queue position without an authenticated resting order.
