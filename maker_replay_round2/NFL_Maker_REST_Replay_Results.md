# NFL moneyline maker: public REST replay results

September 21, 2026. This extends the earlier maker audit with recovered public data, a new replay implementation, and measured comparisons. The repository's maker code was unchanged between the previous pinned commit `f4ad8e8` and newly reviewed head `0217e505`.

**The strategy remains worth researching, but its apparent return depends heavily on getting near the front of the queue.** A replay using historical bid/ask candles earns a simulated **+$681.73 on $5,000** under the original queue profile. Increasing only the early queue assumption from 290.595 to 3,300 contracts reduces that to **+$44.55**. That is a **93.5% reduction**. Both figures are unvalidated simulation estimates.

The useful improvement is now specific: use actual quote observations, measure queue and aggressor flow separately for each equivalent team leg, reserve risk across the whole game, and begin liquidation before the hard cutoff. A more complicated winner model is not the next bottleneck to solve.

**The missing trade-data problem is resolved for a fixed cohort.** Public REST, without an account API key, supplied all sixteen games in NFL season 2026 week one, with both team tickers. Selection was by schedule, not by profitability. The package includes:

- **387,258 pregame trades** from T−7 days through T−3 hours, with pagination exhausted for every ticker.
- **3,860 additional trades** in the five minutes after each deadline. These let the unchanged legacy engine encounter its stop condition; the repaired engine admits no new maker fills at or after the cutoff.
- **173,074 historical one-minute bid/ask candle observations** across 32 tickers. There are 143,918 absent minute slots; those are recorded as missing, not filled in or described as confirmed outages.
- Event metadata, hashed capture manifests, simulation fills, per-game ledgers and all code needed to rerun the new models offline.

This is one NFL week of outcomes, observed across overlapping pregame windows spanning September 3–14 UTC. The games had already appeared in the repository's research. Hundreds of thousands of prints do not create hundreds of thousands of independent games or an untouched holdout. [Public trade endpoint](https://docs.kalshi.com/api-reference/market/get-trades), [historical bid/ask candles](https://docs.kalshi.com/api-reference/market/get-market-candlesticks).

**The same-cohort comparisons are below.** Each uses one shared $5,000 account. All rows remain conditional on simulated fills, unobserved historical queue/depth, and assumed execution timing.

| Run | Simulated net P&L | Return on shared $5,000 | Flat at deadline in simulation? |
|---|---:|---:|---|
| Unchanged repository engine, exact 7d→3h policy | **+$1,027.47** | +20.55% | Reports flat under its original rules |
| Repaired engine, historical bid/ask candles, original queue profile | **+$681.73** | +13.63% | Yes, all 16 games |
| Same candle model, inventory-direction filter | **+$217.84** | +4.36% | Yes, all 16 games |
| Same candle baseline, early queue raised to 3,300 | **+$44.55** | +0.89% | Yes, all 16 games |
| Same candle baseline, liquidation starts five minutes earlier | **+$684.64** | +13.69% | Yes, all 16 games |
| Same candle baseline, total assumed exit depth limited to 50 | **No completed P&L** | — | No: 689.89 contracts unresolved |

The queue increase, exit-depth stress and five-minute wind-down are explicitly labeled **post-result diagnostics**. The original baseline and direction-filter comparisons were specified before their results were run. No model or threshold was fitted to this week's outcomes. The baseline rerun after adding the optional wind-down produced the same $681.73 to the calculation's precision.

Comparing the unchanged engine with the new one measures a bundle of changes: clock handling, joint reservations, latency assumptions, fee rounding, quote inputs and exit controls. It does not establish how many dollars any one defect contributed. The earlier +32.2% artifact used a different tape and is not the comparison row above.

**Using trade age as book age throws away useful information.** At 172,203 comparable minute-end observations, at least one inferred side's last trade was over five minutes old **74.8%** of the time. Yet the inferred bid/ask price pair differed from the historical candle close only **2.93%** of the time. A quiet side can retain a valid resting quote without a recent trade.

The repaired print-proxy baseline ends with $269.48 of net cash gain plus 250 unresolved contracts. Its terminal payout bounds are $269.48–$519.48, before any future exit fee. It is not a completed T−3h result. The candle model supplies independent bid/ask observations and finishes flat under the assumed exit liquidity. This is a source-quality improvement: a stale last trade is not sufficient evidence that the actual order book is stale.

For trading decisions, the candle model uses only closing bid/ask values **after the minute ends plus an assumed 60-second publication delay**. It never uses intraminute highs/lows to manufacture fills. The quote-source audit compares values at minute end only as an ex-post diagnostic; it is not used as a same-minute signal. Actual historical publication and receipt times remain unknown.

**The economic margin is much smaller than the bankroll percentage suggests.** The $681.73 baseline trades approximately 947,421 contracts and pays $3,851.20 in fees. Its net margin is **0.07196¢ per traded contract**. The higher-early-queue case earns only **0.02830¢ per contract**. An additional average cost of that size would erase the corresponding simulated profit, holding the hypothetical fills fixed.

Nine of sixteen games are positive in the candle baseline. Its two largest contributors account for approximately 82% of net profit; removing both leaves **+$121.82**. That is better than a result wholly dependent on one game, but it is still one short, previously examined cohort. I do not assign a profitability confidence interval or annualize the return.

**Current public books directly challenge the uniform thin-queue assumption.** I selected the next two eligible NFL events by schedule and captured their public order books. Both were more than twelve hours before kickoff, so the old profile would assign 290.595 contracts ahead to newly joined quotes.

| Current event | Observed smallest best-level queue | Observed largest best-level queue |
|---|---:|---:|
| New York Giants–Los Angeles Rams | 4,782.24 | 7,936,255.35 |
| Atlanta–Green Bay | 504.55 | 61,806.23 |

Across the two events' eight YES/NO best-price levels, **seven exceeded 3,300 contracts**. These are a small present-day snapshot, not historical queue measurements and not a representative distribution. I did not substitute them into the historical replay. They do demonstrate why a forward bot must read the actual level for its particular ticker and side. Current top-level depth is an initial queue approximation, not a prediction of how much volume will remain ahead as other orders cancel or arrive. [Order-book responses](https://docs.kalshi.com/getting_started/orderbook_responses), [queue priority](https://docs.kalshi.com/api-reference/orders/get-order-queue-position).

The four equivalent team legs can have very different prices and queues. A cheaper equivalent purchase can sit behind millions of contracts while a slightly dearer one sits behind thousands. Price alone does not select the best route; queue size alone does not either, because aggressor flow differs between legs. The useful next model estimates completion time and expected offset cost using **queue ahead relative to incoming matching flow**, with cancellation and adverse-price-move uncertainty.

**The inventory filter did not earn promotion.** It produced more positive individual games, 11 versus 9, but reduced aggregate simulated profit from $681.73 to $217.84. Both reached the 250-contract maximum exposure at some point. That is a useful reminder that a higher share of winning games does not establish a better maker. The filter blocks new quotes in the current inventory direction and cancels such resting orders; it is not a guaranteed exchange reduce-only order, and opposite-side fills may overshoot zero. A full completion-value controller remains untrained.

**The five-minute wind-down is a practical improvement to the operating rule.** It begins cancelling and exiting before the hard T−3h deadline and retries once per minute, while retaining one total exit-depth budget per game. It finished flat with $684.64, only $2.91 above the baseline. That difference is not evidence of extra alpha. Its value is that it creates time to deal with cancellations and failed exits without paying a visible large cost in this particular replay.

Reducing assumed exit depth to 50 contracts leaves 689.89 contracts unresolved. The model reports terminal payout bounds of **$364.28–$1,054.17**, not a completed-strategy profit or a confidence interval. Taker sweeps themselves still assume immediate execution against the latest available quote source; actual submission delay, slippage and depth must be measured before treating simulated flatness as attainable.

**The implementation now has 19 passing tests.** They cover the four original defects, deadline processing without arriving trades, cancellation races, cash shared across games, all fill orderings for a four-leg risk scenario, cross-ticker pair accounting, partial-fill fee accumulation, fixed-point rounding, quote-source isolation, unresolved exits, and an exit budget that cannot be reused on retries. In the candle baseline there are zero maker fills at or after cutoff, and simulated event exposure stays within 250 contracts apart from floating-point display noise.

Recovered event metadata confirms two mutually exclusive team markets, `MECNET`, and the 50¢ tie rule for this cohort. This supports the payoff identity raised in the first audit. It does not by itself verify the entire exchange collateral-release engine or all postponement/cancellation cases. Current series metadata reports multiplier 1 with maker fees; the sampled first event has no listed fee overrides. The model's fixed period fees remain an assumption because this work did not reconstruct a complete account-specific historical fee ledger. The new fee accumulator follows the currently documented balance-precision mechanics. [Event metadata](https://docs.kalshi.com/api-reference/events/get-event), [fee rounding](https://docs.kalshi.com/getting_started/fee_rounding).

**My research ranking stays the same.** NFL pregame making remains first, college-football synchronized price shopping second, and NFL early-price movement as a maker signal third. The repo's new weather calibration study is worth tracking, but pooled, repeated prints from a small collection of city-days do not establish independent forecast calibration or attainable maker fills. It does not displace those priorities yet.

For the next maker version, I would retain the repaired execution and the five-minute wind-down as a research candidate, use current public book observations for each leg, and replace the static queue profile with a model of queue consumption and pair completion. The included `record_public_books.py` was exercised successfully without a Kalshi key and records bounded REST snapshots with request/receipt timestamps. No recorder or bot has been left running. Historical captures are preserved so the comparisons can be reproduced without another download.

The evidence has advanced from conflicting saved summaries to a reproducible experiment on real trades and quote observations. It supports continued research. **It does not yet support sizing a live strategy from the $681 headline.**
