# NFL queue experiment Q1: routing improves the model, execution remains unvalidated

September 21, 2026. Completed research on the same **16 NFL week-one games**, **32 team markets**, and **one shared $5,000 account**. No live orders were placed.

**The new router is the strongest candidate from this experiment.** At an assumed early queue of 3,300 contracts, it raises simulated net P&L from **+$46.64 to +$154.07**. At the original early queue of 290.595, it raises the comparable result from **+$684.64 to +$1,060.62**. Selective one-cent price improvement reduces P&L in both comparisons and does not earn promotion.

The router does **not** establish a durable or executable edge. Increasing the hypothetical early queue to 10,000 leaves only **+$19.60**; at 100,000 it loses **$16.10**. Current public books contain several much larger queues, although current observations cannot reconstruct historical queues. With the 3,300 queue, removing the two best games leaves the router **$16.00 negative**.

**Reconciling the original $1,000-plus result**

The original repository engine simulated **+$1,027.47 on these same 16 games and the shared $5,000 bankroll**. That number has not been withdrawn. It used the original execution/accounting model. The repaired model previously produced +$681.73, or +$684.64 when liquidation began five minutes early. The new router's comparable figure under that same queue profile is +$1,060.62.

The $46.64 and $154.07 figures are a separate comparison with the **early queue increased to 3,300**. They should never be presented as replacing the original engine's output without identifying that change. Comparing the original engine directly with the new router bundles multiple execution fixes and a new policy; it is not a clean router-only ablation.

**What was frozen and held constant**

Fourteen primary scenarios were specified in `EXPERIMENT_SPEC.md` before new outcomes. All use T−7 days through T−3 hours, with new entries stopped and liquidation begun five minutes before the deadline; 250-contract desired orders and maximum event exposure; .25-second assumed submit/cancel delays; 50% hypothetical participation after queue consumption; shared cash reservations; .0175 maker/.07 taker fee coefficients; and a total assumed 250-contract exit budget per event. The original last-twelve-hour queue remains **1,327,847.005** in every row. Only the earlier queue changes between columns.

| Primary policy | Early queue 290.595 | Early queue 3,300 |
|---|---:|---:|
| Preserve existing orders | +$684.64 | +$46.64 |
| Cancel/repost after 60 seconds | +$245.05 | -$41.41 |
| Route by pair margin and eligible flow | +$1,060.62 | +$154.07 |
| Improve offsetting quote by one cent | +$672.84 | +$44.93 |
| Route plus price improvement | +$1,040.17 | +$152.68 |
| Price improvement; 250 competing contracts | +$673.19 | +$43.95 |
| Combined; 250 competing contracts | +$1,040.05 | +$152.29 |

All primary scenarios finish flat in the simulation. Historical depth, actual matching priority, market response to our hypothetical orders, historical quote receipt times and executable exit liquidity remain unobserved. Fees and immediate cross-market collateral release retain the preceding experiment's assumptions. Minute candle closes become available only after an assumed 60-second publication delay. No intraminute high/low is used to manufacture a fill.

**What the router actually changes**

The preserving baseline already keeps an order when its desired price is unchanged. The churn scenario deliberately cancels it after 60 seconds of resting age; it measures both priority loss and resulting interruption. Its poor performance is evidence against that behavior within this model, not evidence that the old baseline had this defect.

For each of the two complementary game exposures, the router compares the two possible team-market legs. It uses fee-inclusive maker-pair margin and strictly earlier trailing-hour trade volume that could reach the quoted price. The ranking multiplies margin by a bounded ten-minute queue-service fraction. **This fraction is a heuristic, not a calibrated fill probability.** Incumbents receive credit for already-consumed queue; a challenger must exceed their score by 25%. Pending cancels continue to reserve cash and event exposure. YES-bid/NO-ask representations within a single market are never treated as separate queues.

After seeing the primary results, a separately declared mechanism check removed the flow multiplier while retaining the remaining route rules. Margin-only routing produced **+$96.73** with the 3,300 queue, versus +$154.07 with flow ranking. The corresponding thin-queue figures were +$966.62 and +$1,060.62. Thus both equivalent-leg price selection and flow ranking contributed in this cohort. These are post-result diagnostics, not independent confirmation.

| Queue stress, declared after primary results | Preserve | Router |
|---|---:|---:|
| 10,000 | -$29.20 | +$19.60 |
| 100,000 | -$35.40 | -$16.10 |

The stress levels are hypothetical scenarios. They were not estimated from, or backcast using, current books. Their purpose is to show that calling 3,300 contracts sufficiently conservative would be unsupported.

**Completion quality and concentration**

At queue 3,300, routing increases maker volume from **155,299.04 to 228,203.98 contracts**. Volume-weighted median time to pair an acquired unit falls from **18.96 to 10.49 minutes**. This measures time from acquisition to its FIFO offset, not waiting time before the first fill.

Total unhedged contract-hours nevertheless increase **13.4%**, as more inventory is traded. Faster pairing therefore does not mean less aggregate inventory exposure. Eight of sixteen routed games are positive. Removing the two largest contributors gives **-$16.00**. Net margin is only **0.06719 cents per traded contract**; an additional average cost of that size would erase the simulated profit, holding fills fixed.

Five-minute signed midpoint movement after fills is slightly less adverse for routing, but uses delayed minute observations and is a descriptive diagnostic. Coverage, missing observations and fee-adjusted markouts are recorded in each result JSON; markouts are not realized strategy profit. No confidence interval, annualized return or new holdout claim is made from this already-examined week.

**Why price improvement is not promoted**

The tested rule moves an inventory-offsetting quote inward by one cent only with a spread of at least two cents, while remaining passive against the observed quote. It reserves for other offset orders and requires every unmatched FIFO entry lot to leave at least 0.1 cent after modeled maker fees and a rounding allowance. A second version puts 250 hypothetical competing contracts at that new price. Neither version beats routing alone. Orders inserted inside a historical spread are especially counterfactual because the observed tape was generated without them.

**Public REST observations**

The capture contains **476 book snapshots** across four team markets, from **2026-09-21 14:21:45 UTC through 2026-09-21 14:41:24 UTC**, a span of **19.7 minutes**. It also recovered **4,326 distinct public trades**, including the trailing-hour warm-up; that trade count is not all activity during the book-observation span. The events were selected by schedule before these observations: NYG–LAR on September 21 and ATL–GB on September 24.

| Team-market leg | Smallest observed top-level size | Median | Largest |
|---|---:|---:|---:|
| Sep 21NYGLAR-LAR YES | 631,007.56 | 638,730.93 | 638,841.09 |
| Sep 21NYGLAR-LAR NO | 8,403,047.32 | 8,408,672.04 | 8,450,622.98 |
| Sep 21NYGLAR-NYG YES | 466,476.85 | 466,582.11 | 479,620.10 |
| Sep 21NYGLAR-NYG NO | 10,512,577.79 | 10,528,465.35 | 10,557,824.81 |
| Sep 24ATLGB-ATL YES | 737.22 | 757.87 | 2,010.72 |
| Sep 24ATLGB-ATL NO | 295,149.60 | 364,755.82 | 368,846.83 |
| Sep 24ATLGB-GB YES | 27.47 | 49.70 | 131,731.46 |
| Sep 24ATLGB-GB NO | 5.49 | 351,781.51 | 374,789.37 |

These are visible sizes at the best price, not exact positions for an owned order. NYG–LAR was inside its last twelve hours before kickoff; ATL–GB was still several days out. Queue size and incoming matching flow vary sharply between equivalent legs. A large queue may clear quickly if flow is high or orders ahead cancel; a small queue can remain idle. Public aggregate size changes do not reveal which cancellations were ahead of a hypothetical order.

There were **0 spreads of at least two cents in 476 observations**. The short capture therefore gives no observed room for the tested one-cent passive improvement. Of **900 overlapping hypothetical joins**, **10** received any modeled service and **0** reached 250 contracts within the evaluated observation segment. These assume no beneficial cancellation ahead, end at a detected price change, a data gap, ten minutes or coverage end, and are not actual fills or independent trials. Transient changes between snapshots remain unknown.

Median successful book-request round trip was **5.01 seconds**, with a **9.68-second 95th percentile**. There were **8 explicitly recorded request failures**. Later completed trade requests covered the failed trade intervals; missing book snapshots remain missing. These are this workspace's HTTP/proxy measurements, not matching-engine latency. The original sequential recorder was interrupted once and resumed using four independent concurrent GETs; raw records and the interruption are retained. Median same-ticker observation gap was 5.62 seconds and maximum gap 136.73 seconds. This is not an uninterrupted exchange feed, and the .25-second simulation latency remains an assumption.

**Decision and next validation gate**

Retain order preservation and advance equivalent-payoff routing to forward research. Keep passive price improvement disabled by default on this evidence. Before promoting live execution, replace static per-leg queue assumptions with measured service and explicit abstention when a queue is unlikely to clear before the quote becomes unattractive or the deadline arrives. The present score ranks routes; it does not yet estimate that completion probability reliably.

Public REST can continue measuring books and trades. Exact queue position for an owned resting order is available through authenticated REST; this task had no account credentials and placed no orders. Even with authentication, queue position and good execution cannot guarantee profitable fills.

**Reproducibility**

The package contains the frozen specifications, unchanged prior engine, new policies, all historical public inputs, raw new REST observations, complete hypothetical fill ledgers and results. **35 unit tests pass**, covering the earlier execution defects plus causal flow, priority retention, pending-cancel reservations, routing, FIFO gating, non-crossing improvement and receipt-time availability. All **20 scenario ledgers** were independently reconciled from saved fills; the prior +$684.6409 baseline matched within 1e−7. Every case reports zero maker fills at or after cutoff and respects the 250-contract event bound within floating-point tolerance. The completed capture's hash was verified. No bot or recorder is left running.

Official source references: [price-time priority and authenticated queue position](https://docs.kalshi.com/api-reference/orders/get-order-queue-position), [order modification and quantity increases](https://docs.kalshi.com/fix/order-entry), [public orderbook mechanics](https://docs.kalshi.com/getting_started/orderbook_responses), [public trades](https://docs.kalshi.com/api-reference/market/get-trades).

**Per-game comparison at the 3,300 early queue**

| Event | Preserve | Router |
|---|---:|---:|
| 26SEP09NESEA | +$63.42 | +$114.82 |
| 26SEP10SFLAR | +$26.31 | +$55.25 |
| 26SEP13BALIND | -$4.31 | +$1.92 |
| 26SEP13ATLPIT | -$2.00 | -$0.36 |
| 26SEP13CHICAR | -$8.05 | -$10.50 |
| 26SEP13BUFHOU | -$26.58 | -$26.61 |
| 26SEP13CLEJAC | +$2.80 | +$0.95 |
| 26SEP13NYJTEN | -$3.65 | -$5.87 |
| 26SEP13NODET | +$2.71 | +$10.84 |
| 26SEP13TBCIN | -$5.00 | -$2.40 |
| 26SEP13ARILAC | -$8.67 | -$7.62 |
| 26SEP13MIALV | -$1.75 | -$15.65 |
| 26SEP13GBMIN | +$4.07 | +$8.56 |
| 26SEP13WASPHI | -$18.91 | -$19.15 |
| 26SEP13DALNYG | +$12.04 | +$19.02 |
| 26SEP14DENKC | +$14.20 | +$30.88 |
