# Research candidate policy: enter early, price competition explicitly

Development specification derived from AMS-005/007/009. This is a candidate
ranking and quote-mechanics policy, not a validated strategy or an enabled order
system. Keep all market categories eligible within this reward mechanism.

1. Discover a current positive short reward pool and verify the target, discount,
   price grid, program end and market close from fresh public data.
2. Rebuild each side from a sequenced public book. Missing data is unavailable,
   not empty liquidity. Resynchronize after sequence gaps. Minute-spaced reads
   establish opportunities but cannot drive a quoting controller.
3. Compute genuine resting one-cent bids that complete only deficient sides.
   Prefer early reward windows; do not count reward budget from before entry.
4. Calculate the score after inserting our actual proposed quantities. Include
   existing better-priced depth and the one-fifth-target reference. Compare
   conservative target-capped allocation against the boundary-level sensitivity.
5. Inspect depth at the best opposite quote, not only its price. Run both fixed
   same-price competition and removal of the best opposite level followed by
   a feasible 200-contract two-cent competitor. Report the rival's size relative
   to target; 200 contracts is a development stress, not a universal constant.
6. Compare conditional remaining rewards at 50% qualifying time with full
   one-order-set principal plus the stated fee stress. This is a rejection rule,
   not an expected-profit estimate. A qualifying order may fill immediately.
7. Evaluate exact completion and a 10%-of-target buffer. The buffer tolerates
   some own fills; it does not protect against arbitrary opponent cancellations,
   price competition, or falling opposite depth. Never silently replenish.
8. Track positions and risk by underlying event. Six strikes sharing a temperature
   observation are correlated. Separate pools may add reward capacity, but
   duplicating bots in one pool does not add external reward budget.

Illustration using the observed $100, roughly 57.7-minute period and 1000 target:
the stronger competition/50%-uptime stress needs about 38.1 minutes remaining
without a buffer, or 41.9 minutes with 100 extra contracts. Those are conditional
entry thresholds for these terms. They are not instructions to trade late if
competition happens to be absent in a single snapshot.

The immediate engineering focus is a read-only early-window scanner emitting
reward time remaining, target completion size, reference-price sensitivity,
opposite top-level depth, event concentration and clearly conditional score.
Its output must not label projected rewards as P&L. Account payout reconciliation
and execution remain separate from this research. No live risk limits changed.
