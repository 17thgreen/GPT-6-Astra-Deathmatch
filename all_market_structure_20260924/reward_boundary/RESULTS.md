# AMS-011: smaller orders at already qualifying levels

The formal price-level clarification supports a refinement of the same reward
strategy. See ../SOURCE_UPDATE_20260924.md. We tested six predeclared size fractions
using whole-level scoring on 55 retained AMS-005, 320 AMS-007, 115 AMS-009 and 262
AMS-010 observations. Old data is reused development evidence; the AMS-010 overlay
was specified after capture began and is exploratory, separate from its primary.

There were 873 baseline-qualified quantity alternatives; 260 passed the combined
budget stress. Of 516 supported-level alternatives, 43 passed. These are repeated
size/snapshot cases, not independent opportunities. Selecting the best ratio per
side and snapshot left 16 supported observations in **three distinct market-side/
program combinations across two hourly events**, all Miami temperature. AMS-005
and AMS-009 had no passing cases under this time/competition test.

Each example below is the first passing supported observation for its side and
period. The chosen size was 100 contracts at one cent: $1 principal plus a ten-cent
fee stress. The stress removes the best public opposite level, adds 200 rival
contracts at two cents and reduces future qualifying time to 50%. It applies the
cent rounding and $1 minimum payout. Sufficient opposite depth must remain.

| Period / strike | Side | Existing one-cent quantity | Stressed remaining reward | Cushion after principal and fee reserve |
|---|---|---:|---:|---:|
| 1am EDT / T79.99 | YES | 1060 | $1.56 | $0.46 |
| 2am EDT / T79.99 | YES | 1000 | $1.63 | $0.53 |
| 2am EDT / T76.99 | NO | 1080 | $1.52 | $0.42 |

The first row reuses AMS-007; the others overlay AMS-010. The 2am T76.99 setup
passed in seven observations, ending with $1.43 modeled reward and $0.33 cushion.
The 2am T79.99 supported setup appeared in one observation, then lost supporting
depth, became a gap candidate, and later a one-cent bid would cross. The state
must be re-evaluated dynamically. These are conditional budgets, not paid credits
or forecasts. Ranking maximizes cushion/principal, not absolute dollar profit;
CASES.jsonl retains all size alternatives for that separate sizing decision.

Kalshi's execution queue documentation specifies price-time priority. Our inference
is that a later order at the same qualifying price can earn proportionally while
earlier orders have execution priority. Individual queue position and actual fill
protection were not measured. Earlier orders can cancel or be consumed by a large
trade. Source: https://docs.kalshi.com/api-reference/orders/get-order-queue-position

The tape supplies counterevidence to any claim that cheap quotes never fill:
2am T79.99 traded 300 YES contracts at one cent at 05:04:03.403137, after its
supported observation. T76.99 traded 327.05 NO contracts at one cent between
05:04:22 and 05:08:11. These are other participants' trades; no fill is assigned
to our absent quotes. Book disappearance is not classified as execution.

The potential benefit is smaller principal and an execution buffer from genuine
existing orders. Tradeoffs include lower dollar capacity, reliance on that depth,
minimum payouts and event concentration. No daily-income extrapolation is made.

Five focused tests passed before scoring, covering full-level inclusion,
same-price ordering invariance, boundary exclusion, reference discount, supported
classification and opposite-depth loss. Frozen source/import hashes and used
receipt hashes verified. Source freeze: ecb3786661c37767a1caac443df36bded5c01f2d.

Next selector refinement: distinguish gap completion from supported participation,
compare sizes on reward-per-dollar and absolute cushion, and monitor the depth
and reference price supporting eligibility. This stays within liquidity rewards.
ARCHIVE.json identifies replay evidence and dependencies. No account action,
claimed order survival, credited rewards, hypothetical fills or realized profit.
