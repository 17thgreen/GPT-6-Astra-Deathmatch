# All-market research map — 2026-09-24

The search unit is a mechanism with a measurable information source, not a sport.
All rows below are hypotheses; no row is an established profitable strategy.

| Mechanism | Candidate families | Information needed | First falsification |
|---|---|---|---|
| External-price lead/lag | Crypto, metals, commodities, financial thresholds; perps separately | Independent executable reference, venue book deltas, receipt clocks | Edge gone after our delay, fees and hedge/basis costs |
| Official-release interpretation | Economic data, weather, precisely sourced outcomes | Original release and revision policy, settlement source/time, rules | Release does not determine contract or book responds before receipt |
| Payoff implication violation | Same-source/time threshold ladders across any category | Proven A implies B; buy YES B + NO A depth cost | Net floor <= cost or second leg not executable |
| Exhaustive outcome basket | Mutually exclusive, exhaustive event outcomes | Proof of exhaustiveness and exceptional settlements | Missing outcome, divergent cancellation rules or depth failure |
| Incentive-driven replenishment | Any incentivized event market or perp | Program eligibility and active period, repeated book changes | Pattern not predictive out of sample or consumed before arrival |
| Inventory pressure and recovery | Any family with observable temporary order imbalance | Cross-book reference and executable unwind | Imbalance conveys real information rather than temporary pressure |
| Reward-aware making | Eligible market periods | Qualifying depth, competition, own score share, inventory | Rewards fail to cover adverse selection and exit costs |

## Interface findings (documentation, not account access verification)
- Public event catalogs and GET books support structure discovery. They do not
  establish message-by-message quote lifetime or our order execution speed.
- Event WebSocket sessions require authentication, including public-data channels.
  L2 reconstruction needs snapshots, sequence checks, deltas and resnapshot after gaps.
- Perps use separate REST/WS/FIX surfaces and bids/asks; event books use YES/NO bids.
  Keep quantities, contract multipliers, funding and reference price scales separate.
- Official docs advertise CF Benchmarks 5Hz reference ticks for five crypto indices,
  plus a per-second feed for additional indices. Publication rate is NOT an observed
  speed advantage. A Kalshi-relayed reference is not an independent leading feed.
- The documented Pyth feed covers metals/commodity references and lists $1,000/month
  with seven free days. No subscription or trial started. Prefer admissible free
  independent sources for initial work; account entitlement remains unverified.
- REST and FIX share rate-limit budgets: FIX is not a throttle bypass. Current docs
  describe explicit-shard write budgets and event-driven bursting. We have not
  verified the user's tier. No rate limit or live order settings were changed.
- PrivateLink is documented for Premier+ and WS VPC peering for Prime+. These are
  upgrade options only if a measured latency-profit curve justifies their cost;
  eligibility, cost and attainable performance have not been established.
- Incentive API amounts are centi-cents (divide by 10,000 for dollars), not cents.
  The listing is not evidence that our account qualifies or that payment is final.

## Next admitted measurement
Once a usable receipt stream exists, compare price discrepancies at the same local
information cutoff. Stress 10–5000 ms decision-to-arrival delay, full executable
entry/hedge depth, both fees, cancellation race, concurrent depth consumption,
partial-fill inventory, financing and adverse exit. A bounded REST scan never
substitutes for this measurement. Retain every signal, not only trades later marked
profitable. Report observations and model assumptions separately.

Special cases: event probabilities need a calibrated probability model; spot prices
cannot be compared directly to binary prices. Nested-payoff proofs avoid forecasting
but not leg risk. Perp-vs-spot pricing needs basis, funding, collateral and hedge
account availability. Post-release certainty requires exact rules and revision logic.

## Sources read
- https://docs.kalshi.com/llms.txt
- https://docs.kalshi.com/getting_started/api_environments.md
- https://docs.kalshi.com/getting_started/quick_start_websockets.md
- https://docs.kalshi.com/api-reference/incentive-programs/get-incentives.md
- https://docs.kalshi.com/margin.md
- https://docs.kalshi.com/margin-rest/market/get-markets.md
- https://docs.kalshi.com/margin-rest/market/get-market-orderbook.md
- https://docs.kalshi.com/websockets/cfbenchmarks-value-5hz.md
- https://docs.kalshi.com/websockets/pyth-value.md
- https://docs.kalshi.com/websockets/orderbook-updates.md
- https://docs.kalshi.com/getting_started/rate_limits.md
- https://docs.kalshi.com/fix/connectivity.md
- https://docs.kalshi.com/api-reference/orders/create-order-v2.md
