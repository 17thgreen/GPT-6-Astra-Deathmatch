# AMS-001: all-market structural opportunity discovery

Scope approved: all Kalshi market families, including event contracts and perpetuals.
Research only; public GET acquisition, no orders or account mutations. This is a new
lane; existing Q6/Q7 branches and experiments are not modified or selected here.

## Mechanisms
1. External-information stale quotes (taker).
2. Delayed interpretation of official observations and releases (taker).
3. Price contradictions across verified payoff relationships (taker/hedged).
4. Incentive-driven quote replenishment and temporary inventory pressure (taker).
5. Reward-aware passive quoting (maker comparator, not the search boundary).

## First bounded acquisition, frozen before market observations
Catalog event series without a category restriction and margin markets separately.
Get active incentives using documented endpoints. Maximum five pages per catalog,
1000 records per page where supported. A cursor remaining at the bound is incomplete,
not an exhaustive universe. Preserve errors, receipt clocks, exact URLs and raw bytes.
No fee/rebate assumption from another account or product is admitted.

For event-book feasibility: use categories actually returned by the series catalog.
Within each category sort series lexicographically by ticker; try the first five
until one returns open markets. Take the first two markets sorted by ticker from
that response. This is a reproducible access sample, NOT an economic ranking or a
representative census. Preserve skipped/failed series. Cap 24 sampled event markets;
if exceeded round-robin categories in lexical order. Request three sequential books
per sampled market, depth 10. No claim of continuous quote survival between polls.
For perps: first four market tickers sorted lexicographically; three depth-10 books.
If metadata access fails, retain the failure; do not invent instruments.

## Measurements and interpretation
Count categories, series, markets returned, incentive types, two-sided/empty books,
response RTT and observed top-of-book changes. Event bids-only books are converted
via complement: YES ask=1-best NO bid; NO ask=1-best YES bid. Decimal arithmetic.
Never synthesize a missing side. Perpetual order books require a separate adapter;
never apply event payout $1 or reciprocal-book logic to perps.
REST RTT is measured from this research host. It is NOT venue order-entry latency,
feed lag, latency rank, or quote age. No profitability claim from discovery.
Missing authenticated WS means subsecond quote survival is NOT MEASURED.

## Next economic study design
Admit instruments by observable structure and available ground truth, not sport.
Timestamp external feeds and Kalshi streams locally with wall and monotonic clocks;
retain exchange timestamps separately. Reconstruct snapshots+deltas, sequence gaps,
reconnects and content changes. Abort scoring across unknown book intervals.
Signals may use only information already received. Delay grid: 10/25/50/100/250/500/
1000/2000/5000 ms; these are sensitivity values until attainable latency is measured.
All signals retained; executable depth after delay, partial/missed fills and hedge
failure modeled. A quote disappearance is not credited as our fill. Outcomes with
unknown execution remain unscored. No independent reuse of depth across bots/signals.
Contract relationships require explicit settlement-source/time/payoff verification.
Event binary fair value is not the external asset price; perps require basis/funding.
Report gross discrepancy, entry+exit/hedge costs, slippage, inventory losses, rewards
and realized net separately. Rebate-unverified base case = no rebate. No order-level
PnL without an execution model; no return forecasts from midpoint markouts.

## Selection and stop rules
Discovery picks no winning strategy. Follow-up hypotheses freeze before outcomes.
Reject an economic candidate if no positive net survives measured latency and costs,
or if required account terms or payoff equivalence cannot be established. Preserve
zero/negative outcomes. Compare independent dates/regimes after discovery selection.
Activity volume, recurring size, and missing account IDs cannot prove wash trading.

## Limits
No credentials supplied for this lane. No account fee schedule verified. Do not
search unrelated files for credentials. No always-on service is launched. A bounded
capture is research data collection, not user-owned forward trading validation.

### Acquisition implementation detail (before first observation)
Use recommended external-api host. If transport/HTTP fails, try documented legacy
api.elections host once, retaining both receipts; no other retries. All requests
bounded by 12-second timeout. Catalog series and margin endpoints have no documented
pagination parameters: omit unsupported limits there. Incentives use limit=1000.
