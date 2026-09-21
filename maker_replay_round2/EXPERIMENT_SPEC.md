# Frozen diagnostic specification

Written before running any new P&L comparisons in this package, September 21, 2026.

- Cohort: all 16 NFL games in season 2026, week 1, selected from the earlier audit's schedule keys. These games were already used in repository research; this is NOT an untouched holdout.
- Input: both team tickers, public REST trades from T−7 days through T−3h, cursor pagination exhausted, duplicate trade IDs removed. Exclude block trades. Capture an additional five minutes after the deadline solely to let the unchanged legacy engine observe its stop condition; the repaired engine refuses new maker exposure at the deadline.
- Main model: $5,000 shared bankroll, 250-contract desired order size and event exposure cap, 50% post-queue participation, 60-second refresh, separate per-side print ages capped at 300 seconds, fixed 250ms submit/cancel delays, .01-contract quantity increments, .0001-dollar direct-member balance precision.
- Quote source: last opposite-direction public prints. These are proxies, not actual historical quotes. Queue depth and available exit depth are unobserved; all results are counterfactual sensitivity estimates.
- Queue scenarios: repository snapshot profile (290.595 early; 1,327,847.005 inside 12h); flat 3,300; flat 290.595 as an explicitly optimistic sensitivity. Never select whichever assumption produces the best P&L.
- Exit: attempt one sweep at each game's T−3h using both fresh proxy sides and a TOTAL assumed game depth of 250. Stress with depth 50. If exit is unavailable or incomplete, leave inventory unresolved and report payout bounds, not a completed-profit number. Capture end itself never triggers a fabricated flatten.
- Control: unchanged repository replay, exact T−7d/T−3h policy, same $5,000 and tape, repository queue profile. Its fees, event loop, cash behavior and terminal flatten remain unchanged; comparing it with the new engine measures a bundle of changes and does not isolate any single correction.
- Candidate: stop adding same-direction exposure when inventory is nonzero; cancel outstanding risk-increasing orders with the same delay and retain their reservations until acknowledgment. This is a simple de-risking candidate, not a fitted completion model.
- Additional fee sensitivity: .01-dollar non-direct-member balance precision.
- Report: captures and failures, maker/taker volume, fees, cash/risk invariants, unresolved inventory, per-game outcomes, and terminal payout bounds. One week is insufficient for a robust profitability interval. No annualization and no capital commitment recommendation.
- No hyperparameter search or selection on these outcomes. Further cases must be labeled post-result diagnostics.

## Source extension before any P&L runs

A public REST probe confirmed that historical one-minute **bid and ask** candles are recoverable. Add two cases using these quote closes instead of trade-derived quotes: the profile baseline and the inventory-direction filter. Only a candle's closing bid/ask are used, and only after its end plus a fixed 60-second publication delay. Intraminute high/low values are never used for orders or fills. The delay is an assumption, not measured historical receipt time. Missing or null quote observations remain missing. Actual historical queue depth and executable exit depth are still absent. Candle coverage is recorded separately. A timer and a quote arrival sharing a timestamp may cause an extra cancel/requote; this deterministic convention is preserved across cases.
