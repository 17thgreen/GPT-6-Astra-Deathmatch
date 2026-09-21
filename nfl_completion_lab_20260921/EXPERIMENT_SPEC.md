# Completion-aware queue experiment Q2 — frozen before new policy outcomes

2026-09-21. Research only; no live orders or account access.

## Cohorts and controls

Week one: the same previously examined 16 games. Week two: all 15 games whose T−3h cutoff plus five-minute postlude is complete at the timestamp in COHORT_SELECTION.json. Monday NYG–LAR is excluded by time, not by outcome. Week two has appeared in older repository aggregates, so call this expanded-cohort validation, not an untouched holdout. Freeze all new policy rules before running either cohort. Collect both team tickers, all public trades and minute closing bid/ask candles for T−7 days through cutoff+5 minutes.

Each isolated cohort starts with one shared $5,000 account. Also run both cohorts together chronologically on ONE $5,000 account, because their seven-day observation windows overlap; never add two isolated-cohort returns and call that the combined bankroll result.

Keep Q1's accounting, fees, collateral assumption, 250-contract order/exposure limit, .5 post-queue participation, 60s refresh, .25s submit/cancel delay, 300s maximum quote age, 60s assumed candle publication delay, five-minute wind-down, and 250-contract assumed total exit depth. Early queues 290.595, 3,300 and 10,000; last-twelve-hour queue stays 1,327,847.005. Run 100,000 early queue only on the combined cohort as a stress. All prices remain at observed best bids; no inside-spread price improvement.

## Three policies, no threshold search

1. `q1_route`: unchanged Q1 fee-margin × service-fraction router, including 25% switching hurdle.
2. `pair_gate`: evaluate the four combinations of complementary event directions jointly. For each candidate, use strictly prior trailing-hour matching flow and remaining incumbent queue (or the assumed new-order queue). Project usable size over H=min(600 seconds, time left before entry stop) as floor_to_cent(max(0, rate*H − queue) * .5), capped at 250. Queue must be consumed BEFORE projected service begins; this is a deterministic steady-flow projection, not a probability. Pair size is the smaller projected capacity of its legs, at least one contract. Require positive fee-inclusive pair margin, including .0001 per-leg per-contract fee-rounding allowance and one .0001 account unit per leg divided by pair size. Rank projected pair dollars = margin × pair size. Keep a viable incumbent pair unless the challenger exceeds its score by 25%. If no viable pair, cancel entry orders and abstain. Existing inventory still receives an offset quote, even if the entry gate fails, rather than being abandoned.
3. `pair_complete`: same gate while flat, then stop adding inventory in the current direction and work only the offset while inventory is nonzero. Bound desired offset size by actual inventory minus other pending offset orders. React after fills; retain cancellation/resize acknowledgment delays, reservations and race exposure. This is an event-level research controller, not an exchange-native cross-ticker reduce-only guarantee. Offset route ranks projected service first, then fee-inclusive price; keep a valid incumbent unless a challenger improves positive service score by >25%, or improves price when both service projections are zero. Offset quotes do not require a profitable pair with past inventory: closing a losing position must remain possible.

The pair gate checks projected quantities on both legs at current quotes. It does not make two fills atomic, fit a probabilistic forecast, or prove the second quote will persist after the first fills. Trailing flow can fail to predict future flow. Partial fills, quote changes and cancellation races remain possible.

## Fixed matrix and decision

Run all three policies × three early queues × week1/week2/combined = 27 cases; add three combined-cohort cases at early queue 100,000 = 30 total. Primary comparison is early queue 3,300. No policy or parameter changes after results are opened. A candidate earns further consideration only if it improves completed net P&L over Q1 at the primary queue in BOTH isolated cohorts and in the pooled account, with its inventory costs and traded volume disclosed. A lower loss or zero activity is not a profitable strategy. Report other queues even if they reverse the ranking.

Report completed P&L only when flat and every selected game's window is complete; otherwise residual positions and payout bounds. Also report per-game concentration, fees, volume, maker/taker split, paired holding times, unhedged contract-hours, entry abstention, deadline and risk checks, and completion-order overshoot during pending acknowledgments. Hash all input captures and the spec. Verify Q1 week-one regression against saved Q1 outputs. No annualization or independent-observation count based on prints.

Missing historical per-leg queue, actual receipt latency and executable exit depth remain binding limitations. Today's snapshots are never backcast. No live-profit claim even if the new simulations improve.
