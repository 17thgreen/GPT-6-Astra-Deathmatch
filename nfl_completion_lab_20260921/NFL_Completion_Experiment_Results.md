# NFL completion experiment Q2 — 31-game comparison

September 21, 2026. Research only; no live orders placed. This extends Q1 with **15 completed Week 2 games**, **290,614 newly captured public trades**, and **191,914 minute bid/ask observations**. The experiment now covers **31 games and 62 team markets** across two NFL weeks.

**Neither new candidate passes the frozen promotion rule.** Do not replace the previous router with either candidate on these results.

**Primary comparison: assumed early queue of 3,300 contracts**

| Cohort | Previous Q1 router | Joint entry gate | Gate + inventory completion |
|---|---:|---:|---:|
| week1, 16 games | +$154.07 | +$17.09 | +$55.32 |
| week2, 15 games | +$47.46 | −$9.24 | +$2.32 |
| combined, 31 games | +$201.52 | +$7.85 | +$57.63 |

The isolated week-one and week-two rows each start with one $5,000 account. The **combined row runs all 31 games chronologically on ONE shared $5,000 bankroll**. Their seven-day trading windows overlap, so adding the isolated rows does not establish the pooled result. This is the same T−7 days to T−3 hours policy, with a five-minute liquidation lead.

**What changed**

Q1 chooses an entry route partly from its own queue and matching flow. Its service score can be positive even when projected incoming volume would not consume the queue during the score’s horizon. The new gate first subtracts queue ahead, then projects service; it requires both directions of a potential pair to have capacity and a positive margin after modeled fees and rounding allowances. Pair quantity is limited by the slower leg. It retains an incumbent pair unless a challenger’s projected pair dollars improve by more than 25%.

The completion variant additionally stops adding exposure in the current inventory direction and concentrates on an offset after a fill. It accounts for other pending offset orders and keeps cancellation/resize acknowledgment delays. Existing inventory still receives an offset quote if the entry gate fails, even when closing means a loss. Neither candidate improves its price inside the spread.

These are **steady-flow projections, not calibrated execution probabilities**. They cannot make fills atomic or guarantee the offset quote will remain available. A ten-minute projection horizon, capped by the entry deadline, is a fixed research choice rather than an optimized parameter. A gate can reject eventual profitable trades if flow later accelerates or a quote remains attractive much longer than ten minutes.

**Queue sensitivity on the pooled 31-game account**

| Assumed early queue | Previous Q1 router | Joint entry gate | Gate + inventory completion |
|---|---:|---:|---:|
| 290.595 | +$2,262.46 | +$344.66 | +$623.05 |
| 3,300 | +$201.52 | +$7.85 | +$57.63 |
| 10,000 | +$10.35 | +$0.70 | +$5.16 |
| 100,000 | −$45.38 | +$0.00 | +$0.00 |

Only the early queue changes. The original last-twelve-hour queue remains 1,327,847.005 contracts throughout. All these queues are assumptions; no present-day snapshot is substituted for a historical queue. A policy that achieves zero activity or avoids a loss has not thereby established a profitable market-making strategy.

**Inventory and completion costs at queue 3,300, pooled account**

| Policy | Maker contracts | Unhedged contract-hours | Median paired-unit holding time, minutes | Taker exit contracts | Offset-instruction overshoot contracts |
|---|---:|---:|---:|---:|---:|
| Previous Q1 router | 357,442 | 667,959 | 16.01 | 2,477.87 | 0.00 |
| Joint entry gate | 24,418 | 17,665 | 6.92 | 777.68 | 0.00 |
| Gate + inventory completion | 49,753 | 1,564 | 2.25 | 8.37 | 0.00 |

Holding time runs from a unit’s acquisition until its FIFO offset; it is not the queue wait before its first fill. Contract-hours measure the amount and duration of unhedged inventory, not dollars reserved for resting orders or maximum drawdown. Reducing either metric is a useful operational change, but does not automatically compensate for lost profit.

There is a useful secondary finding: **the completion controller reduces unhedged contract-hours by 99.77% and earns 2.07 times as much net per traded contract**, while lowering total profit from +$201.52 to +$57.63. This is a substantial inventory-efficiency tradeoff, not a pass of the frozen profit-promotion rule. It warrants separate research as an operating mode when limiting inventory is the objective. Contract-hours are not a calibrated risk measure, and the return cannot be scaled linearly by the freed inventory capacity; eligible opportunities are limited.

An offset instruction can still overshoot during acknowledgment races. The model records that excess rather than silently clipping fills. This research controller is not an exchange-native cross-ticker reduce-only guarantee. The same worst-case 250-contract event exposure bound remains in force.

Joint entry gate abstained on 654,068 of 659,427 entry checks (99.2%). Gate + inventory completion abstained on 652,633 of 655,087 entry checks (99.6%). These repeated decision checks are not independent trials or unique trading opportunities.

**Concentration and economic margin**

| Policy, pooled queue 3,300 | Positive games | P&L excluding two largest game contributors | Net cents per traded contract | Modeled fees paid |
|---|---:|---:|---:|---:|
| Previous Q1 router | 19 / 31 | +$31.46 | 0.05599 | +$1,437.48 |
| Joint entry gate | 6 / 31 | −$12.40 | 0.03114 | +$114.01 |
| Gate + inventory completion | 10 / 31 | +$17.40 | 0.11582 | +$208.13 |

Two NFL weeks remain a small and correlated sample. The added week was selected by schedule and completed pregame window, but had appeared in previous repository aggregate research. It is an expanded-cohort check, **not a pristine holdout**. No annualization, profitability confidence interval or independent-sample claim based on the number of prints is made.

**Reconciling earlier figures**

The original repository engine’s **+$1,027.47** and Q1 router’s **+$1,060.62** referred to the original **16-game Week 1 cohort** under the original early queue of 290.595. Q1’s **+$154.07** referred to those same 16 games with the early queue raised to 3,300. The 31-game figures above add games and are identified accordingly. The three repeated Q1 Week 1 regressions match their saved results within 1e−7.

**Data and execution controls**

The new cohort contains 288,551 pre-cutoff trades and 2,063 postlude trades, with pagination exhausted for all 30 tickers. It has 105,266 absent candle-minute slots; missing slots are not interpolated or labeled confirmed outages. Together with Week 1, the package contains 681,732 public trade records and 364,988 minute quote records. Raw captures, metadata and hashes are included.

The Monday NYG–LAR game is excluded because its T−3h cutoff had not passed at cohort freeze, not because of a trading outcome. Market membership, two-team MECNET structure, linear-cent grid and 50-cent tie rules are checked. These checks do not fully validate special-event settlement and collateral-release mechanics.

The new rules and 30-case matrix were frozen before their results. The original accounting engine and Q1 router remain byte-for-byte unchanged. Common assumptions include .25-second submit/cancel delays, 60-second refresh, minute candles available after a 60-second assumed publication delay, a 300-second quote-age cap, .5 participation after queue consumption, .0175/.07 maker/taker fee coefficients, .0001 balance precision and 250-contract total assumed liquidation capacity per game.

Historical per-leg queues, actual quote/trade receipt latency, market response to hypothetical orders, account-specific fee history, complete collateral mechanics and executable exit depth remain unverified. All 30 scenarios finish flat under the model’s assumed exit capacity. Simulated flatness is conditional on those exit assumptions.

**Validation and handoff**

41 unit tests pass, including the earlier execution controls, strictly prior flow, queue subtraction, two-leg admission, remaining-order size, deadline shrinkage, inventory rescue and pending-acknowledgment overshoot. All 30 ledgers were recomputed from saved fills, checking cash, fees, netting, exposure and deadline compliance. Input and frozen-code hashes were checked. No bot or recorder is left running.

The first integrity check found one truncated compressed fill ledger. That case was regenerated using unchanged frozen code and inputs; every summary field except runtime matched exactly. The recovery record is included in `results/artifact_recovery.json`, and the regenerated ledger passed the same independent checks.

The next substantial improvement should be judged using measured queue progression, quote lifetime and adverse movement after fills, with policies frozen before evaluation. More selective rules should be evaluated on both net profit and the capital/inventory they occupy; the simulation must not be optimized simply to recover a preferred headline return.

Official mechanics and data references: [public trades and pagination](https://docs.kalshi.com/api-reference/market/get-trades), [historical minute bid/ask candles](https://docs.kalshi.com/api-reference/market/get-market-candlesticks), [price-time queue position](https://docs.kalshi.com/api-reference/orders/get-order-queue-position).

**All isolated-cohort comparisons**

| Cohort | Early queue | Previous Q1 router | Joint entry gate | Gate + inventory completion |
|---|---:|---:|---:|---:|
| week1 | 290.595 | +$1,060.62 | +$259.13 | +$427.83 |
| week1 | 3,300 | +$154.07 | +$17.09 | +$55.32 |
| week1 | 10,000 | +$19.60 | +$6.03 | +$5.51 |
| week2 | 290.595 | +$1,201.84 | +$85.53 | +$195.22 |
| week2 | 3,300 | +$47.46 | −$9.24 | +$2.32 |
| week2 | 10,000 | −$9.25 | −$5.33 | −$0.35 |
