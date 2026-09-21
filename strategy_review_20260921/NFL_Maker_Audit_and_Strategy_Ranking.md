# NFL maker audit and next research priorities

Reviewed September 21, 2026. Repository: `17thgreen/Claude-SportsBetting-Competition-to-the-Death`, branch `claude/kind-hamilton-gdfr9q`, pinned commit `f4ad8e8bfba2db2a5e8e1ecf80f935424f60f175`.

**Keep the NFL moneyline maker as research priority #1. Neither its early +32% simulation nor the later negative headline establishes its executable profitability.** The experiments differ, the later headline averages game-level ratios, and its 2026 sample contains unfinished trading windows. There are also reproducible execution defects. Repairing those is more valuable than adding complexity to the quoting formula immediately.

This review recalculates committed simulation records and tests the actual source on synthetic counterexamples. It does **not** rerun the full trade tape, recover historical order books, or report achieved trading returns. The raw capture database is not in the source snapshot available for this review. No orders or remote repository changes were made. Artifact provenance does not reliably identify which output belongs to “Fable 5.1” versus Opus; the comparisons below identify experiments instead.

## The three I would investigate next

These are ranked by research value for this lab, not by predicted investment return. The second and third adapt mechanisms from sportsbook studies to Kalshi; their historical results are not Kalshi results.

| Rank | Research track | Evidence and reason to prioritize | Principal unresolved issue |
|---|---|---|---|
| **1** | **NFL moneyline market making, T−7 days through T−3 hours** | Direct fit to your objective; substantial existing code and trade records; conflicting conclusions can partly be reconciled from saved artifacts. Improving execution would benefit every future maker. | Realistic queue fills, incomplete windows, shared capital, unmatched inventory and forced exits. |
| **2** | **College-football price shopping, adapted into a synchronized reference-price strategy** | The model-plus-best-price study reports +13.7% across 1,317 historical holdout bets; its documented exclusion of Nitrogen/Cloudbet retains +9.1% across 918. That is stronger historical evidence than another generic winner model. | Untimestamped offshore closing snapshots may be stale or unavailable simultaneously. No demonstrated Kalshi execution edge. |
| **3** | **NFL early-line movement, first as a maker quote-adjustment signal** | The simple linear model reports +0.58 points of average closing-line value on 119 validation selections. This targets a price change before kickoff and could help the maker avoid taking inventory before an adverse revision. | Spread points are not moneyline cents. Input availability at the opener is unverified; realized ROI is only +1.7%, with a reported 95% interval of −12.3% to +15.9%. |

For #2, start by matching the *same contract payoff*: team, handicap, overtime, push, cancellation and tie rules. Compare executable Kalshi prices with simultaneously received, de-vigged reference prices. Do not compare a spread directly with a moneyline or treat a stale closing quote as available. Run price shopping against identical selections at a single reference price; this separates selection value from execution value. The separate “sharp-reference” college strategy has weaker robustness: excluding the two crypto books leaves +5.7% on 241 bets with an interval crossing zero. It is not the same result as the +9.1% model-plus-shopping study.

The college holdout was opened twice after missing Pinnacle lines poisoned the first model fit; the repository records the repair. Preserve that disclosure. The +13.7% total was verified against its saved summary; the +9.1% exclusion comes from the repository’s documented analysis, not a fresh bet-level recomputation here. [College results and limitations](https://github.com/17thgreen/Claude-SportsBetting-Competition-to-the-Death/blob/f4ad8e8bfba2db2a5e8e1ecf80f935424f60f175/docs/16_phase2_results.md).

For #3, freeze the existing linear model as the first baseline. Only 41.2% of its validation selections had strictly positive CLV; the positive average reflects the sizes of moves, so this is not a high-hit-rate signal. Audit QB, injury and other feature publication times. For the maker, predict a future executable price within the allowed window, especially T−3 hours, rather than using kickoff close as an exit the strategy cannot take. Fit any spread-to-moneyline conversion on earlier data and score incremental value against the same maker without that signal. [Saved validation experiment](https://github.com/17thgreen/Claude-SportsBetting-Competition-to-the-Death/blob/f4ad8e8bfba2db2a5e8e1ecf80f935424f60f175/artifacts/experiments/validation_nfl_ml_line_move_linear_only_20260920T055327_19dbde/summary.json).

Weather making is next on the watchlist: the quoted +0.85% size-weighted result is a lead, but attributing every favorable public print to an attainable maker fill is insufficient. The latest board rejects naive weather favorite buying and naive BTC contract-price panic fading. External-spot crypto lag is a different hypothesis requiring synchronized spot, exchange receipt times and the actual settlement reference. Economics needs a new data pipeline. I would not put those ahead of the three above, or reopen generic sports pickers just because the strategy survey is more optimistic than the newer tests. [Current board](https://github.com/17thgreen/Claude-SportsBetting-Competition-to-the-Death/blob/f4ad8e8bfba2db2a5e8e1ecf80f935424f60f175/STRATEGY_BOARD.md).

## Why the maker reports disagree

### They do not evaluate the same strategy

| Item | Early exact-window artifact | Later 315-game validation |
|---|---|---|
| Trading window | Explicit row: start 7 days, stop 3 hours | Policy fingerprint: start 7 days, flatten 60 seconds before kickoff |
| Capital | $5,000 shared portfolio; also a $10,000 case | Independent $5,000 account for every game |
| Sample | Early, previously examined 2026 tape | 267 games in NFL season 2025; 48 in season 2026, including future games |
| Prominent statistic | +$1,611.27 / +32.225% at $5,000 | Mean of per-game cents-per-contract ratios |
| Interpretation | In-sample simulation under the original execution assumptions | Per-game diagnostic; not a shared-bankroll return |

The $10,000 exact-window row earns +$1,735.64, or +17.356%. Doubling the simulated bankroll barely increases absolute profit: capacity and the opportunity set matter. The window artifact lacks a complete run manifest, so the precise contribution of each configuration change cannot be reconstructed from it alone. Summing independent-window or independent-game profits does not produce a continuous $5,000 strategy return. [Exact-window artifact](https://github.com/17thgreen/Claude-SportsBetting-Competition-to-the-Death/blob/f4ad8e8bfba2db2a5e8e1ecf80f935424f60f175/artifacts/experiments/diagnostics/paper_mm_quote_window.json), [validation runner](https://github.com/17thgreen/Claude-SportsBetting-Competition-to-the-Death/blob/f4ad8e8bfba2db2a5e8e1ecf80f935424f60f175/scripts/run_mm_validation.py).

### The negative headline is not aggregate profit per contract

Let game profit be Pᵢ dollars and contracts traded be Vᵢ. These answer different questions:

- Average game ratio: mean(100 × Pᵢ / Vᵢ), excluding games with no ratio.
- Contract-weighted ratio: 100 × sum(Pᵢ) / sum(Vᵢ).

Both can be useful. Neither should be presented as the other. The first gives a tiny-volume game the same weight as a very active game.

| Saved simulation cohort | Games | Mean game ratio, ¢ | Contract-weighted, ¢ | Sum of game P&Ls |
|---|---:|---:|---:|---:|
| 2025, “measured” queue | 267 | +0.2427 | **+0.2669** | +$46,012.02 |
| 2026, “measured” queue | 48 | **−0.0404** | **+0.0937** | +$2,653.65 |
| 2026, queue 3,300 | 48 | −0.2631 | **+0.0710** | +$494.19 |
| 2026, “measured” queue, T−3h reached | 31 | +0.0680 | **+0.0913** | +$2,454.62 |
| 2026, queue 3,300, T−3h reached | 31 | +0.0498 | **+0.0758** | +$504.49 |

**These are recalculations of the original simulated fills, not corrected trading returns.** Filtering completed cohorts does not change the original T−1-minute policy into your T−3-hour strategy. “Measured” describes the repository’s queue scenario, which extrapolates a snapshot; it is not a record of this bot’s historical queue positions. [Source per-game records](https://github.com/17thgreen/Claude-SportsBetting-Competition-to-the-Death/blob/f4ad8e8bfba2db2a5e8e1ecf80f935424f60f175/artifacts/experiments/diagnostics/paper_mm_validation.json).

The contract-weighted edge is lower in 2026 than 2025, but it does not cross below zero in this saved ledger. The latest board already says 48 games are insufficient to call decay; the stronger “edge largely gone” language in `docs/27` is not supported by this comparison. Causation by market maturity is unestablished.

### Seventeen games were still inside the intended trading window

At artifact generation, **2026-09-21 02:33:29 UTC**, 17 of the 48 season-2026 games had not reached T−3h. End-of-tape liquidation therefore cuts these strategies off before their planned horizon. The 31 games that had reached T−3h span just **two NFL weeks**, one still incomplete. That is too little independent contemporary evidence for a confident profitability estimate.

The original week bootstrap groups by ISO week *number*, merging the same week across different years, then drops groups with fewer than three games. It reports 20 blocks. The audit identifies 23 distinct NFL season/week groups across all records, versus 24 ISO year/week groups. NFL week is preferable because late Sunday games fall on Monday in UTC. A bootstrap positive fraction of 1.0 is not a posterior probability that an executable edge exists. The supplied audit withholds an interval for the two-week contemporary completed cohort.

### A window-level queue assumption creates a major mismatch

The `3_to_24h` fleet run selects queue depth once at its 13.5-hour midpoint. It then applies **290.595 contracts** across that entire window. The same snapshot-based regime model uses **1,327,847.005 contracts** inside 12 hours: a **4,569× difference**.

This proves a mismatch between the window runner and its regime assumptions, not that every real game has a million-contract queue. Both numbers come from one September 20 snapshot. The late-pregame scenario’s spectacular simulated profit is especially sensitive to this issue. Resolve depth at the actual decision time and price level; include wide sensitivity bounds when historical depth is missing. [Window runner](https://github.com/17thgreen/Claude-SportsBetting-Competition-to-the-Death/blob/f4ad8e8bfba2db2a5e8e1ecf80f935424f60f175/scripts/run_windowed_fleet.py).

## Four execution defects reproduced

The supplied script executes the unchanged policy and execution classes, and the unchanged replay function bodies isolated from database imports. These are synthetic counterexamples, not estimates of historical P&L impact.

| Defect | Observed counterexample | Required correction |
|---|---|---|
| Matching precedes cutoff cancellation | A resting order receives **50 maker contracts at exactly T−3h** | Process deadline events before simulated matching. In an exchange adapter, initiate cancellation early enough for acknowledgment and retain risk reservations until acknowledged. |
| Same-price replacement ignores size reduction | Request to reduce **100 → 5** leaves **100** resting | Honor reductions; treat additional size as a separate priority decision under exchange amendment rules. |
| Event cap checks existing exposure, not remaining capacity | Exposure **200**, cap **250**, yet another **250** is quoted: possible exposure **450** | Reserve worst-case exposure jointly across all outstanding legs and pending cancellations. |
| Invalid inferred book leaves old quotes active | Crossed inferred book is rejected, but an old quote subsequently fills **50 contracts** | Cancel and block on invalid/stale/sequence-broken data; resume only after a valid book and risk check. |

Other unresolved execution assumptions include last-print-derived quotes without a freshness limit, end-of-tape flattening at stale prices without available depth, cash checked at fill rather than reserved across open orders, and automatic immediate collateral release across sibling markets. Verify settlement equivalence and the event’s collateral-return settings; do not infer reusable cash solely from eventual payout equivalence. The event API exposes the relevant metadata. [Event schema](https://docs.kalshi.com/api-reference/events/get-event).

Kalshi publishes YES and NO bids, from which opposite-side asks can be derived. A previous trade price is not an order-book snapshot. Queue priority is price then time, and an authenticated endpoint reports queue position for an existing order. The replay’s participation percentage is a modeling assumption, not a measured queue entitlement. [Order-book documentation](https://docs.kalshi.com/getting_started/orderbook_responses), [queue-position documentation](https://docs.kalshi.com/api-reference/orders/get-order-queue-position).

## How I would sharpen the NFL strategy

**Optimize the expected outcome of an initial fill, including the probability and cost of completing its offset before T−3h.** Inventory skew alone does not address whether the opposite leg is likely to arrive.

For a transparent two-scenario approximation, let q be completion probability, g the net profit if paired, and L the loss if an unmatched position must be exited. Then:

`EV per initial fill = q × g − (1 − q) × L`

`Break-even completion probability = L / (g + L)`

Illustration: buy YES at 49¢ and offset with a maker NO fill at 50¢. With fee coefficients 0.0175 maker and 0.07 taker, before rounding and other costs, the paired gain is only **0.125175¢**. If instead the NO must be bought at 51¢ as a taker, the loss is **2.186625¢**. Break-even completion is approximately **94.6%**, even before an adverse price move. This is an illustrative calculation, not an estimated completion rate or strategy return. The cited schedule lists NFL-game multipliers of one. [July 2026 fee schedule](https://kalshi.com/docs/kalshi-fee-schedule.pdf).

That calculation is per initially filled unit and its eventual offset. The audit ledger’s per-contract denominator counts both traded legs; do not compare the two denominators directly.

Actual fees require account-specific balance precision, per-order rounding accumulation and dated series/event settings. The current API documentation distinguishes direct and non-direct members and describes rounding rebates across an order’s fills. A fixed cent-ceiling approximation is not sufficient for all present accounts. Historical runs need the fee rules applicable then, not today’s schedule applied backward. [Fee rounding](https://docs.kalshi.com/getting_started/fee_rounding).

The model should estimate **q and conditional exit loss together**. Fast opposite-side fills and benign price moves are not independent. Model time to offset with censoring at the fixed horizon, and include price band, actual queue ahead, book imbalance, recent aggressor flow, inventory, time remaining, reference-price changes and receipt latency. Restrict input features to information available at the decision. Start with a simple regularized model; do not optimize a large parameter grid on the same two weeks.

I would make six changes in this order:

1. **Make the exact window an invariant.** Admit new quotes only from T−7 days inclusive to T−3 hours exclusive. Use timer events even when no trades arrive. Separate “stop opening exposure,” “cancel outstanding orders,” and “finish liquidation”; if the objective is flat by T−3h, liquidation must start earlier. Preserve the actual kickoff schedule revision known at each time.
2. **Make inventory a game-level problem.** Aggregate all verified equivalent payoff legs. Reserve cash and directional headroom for every possible subset of outstanding fills, including pending cancels. A desired offset that has not filled is not a hedge. Allocate the same shared bankroll across games.
3. **Admit quotes based on conservative net value.** Use a lower estimate of pairing value after conditional markouts, forced-exit depth, fees and capital time. Permit one-sided quoting, smaller size, stepping away or no quote. Do not assume every book offers enough gross spread to cover costs.
4. **Preserve valuable queue position.** Compare the expected cost of leaving a stale quote with the value lost by cancelling and rejoining. A fixed 60-second refresh is not automatically optimal. Respect actual price grids and amendment priority rules.
5. **Use price movement as a protective signal.** Test track #3 as a small, separately measured adjustment to reservation price and order size. Shrink it toward zero unless timestamped validation shows improvement. Do not treat historical CLV as an executable hedge.
6. **Measure conditional execution.** Record markouts on fills the simulator could plausibly receive, not on all public prints. Track completion times, unmatched positions, forced-exit losses, stale-book exposure, cancelled-order late fills, and capital tied up. Public book replay can bound hypothetical fills; it cannot establish the exact queue history of an order that never existed.

## The next experiment, specified before running

Run one continuous, event-time-ordered portfolio with **$5,000 shared cash**, the exact T−7d/T−3h horizon, dated fees and complete game windows. Keep the $10,000 case as a predeclared capacity check. Do not splice independently funded windows together. For incomplete windows, report open inventory separately; do not label end-of-tape marks as completed strategy P&L.

| Comparison | Question it resolves |
|---|---|
| Corrected fixed-quote baseline | Does any original signal survive execution and accounting repairs? |
| Baseline plus joint inventory reservations/skew | Does exposure control improve the return/risk tradeoff? |
| Previous variant plus completion/exit-value admission | Does selective quoting improve net value beyond merely reducing volume? |
| Previous variant plus frozen early-price-movement signal | Does the directional overlay add incremental value? |

Use identical data, cash and execution assumptions for each comparison. Account for each variant’s different orders and queue age; do not grant identical fills to different quotes. Evaluate timestamp and cancellation delays, plausible queue bounds, historical fee uncertainty, and depth-constrained exits without selecting whichever case looks best.

Treat all records already used to choose rules as development evidence. The run’s `HISTORICAL_OUT_OF_SAMPLE` label does not make a repeatedly examined dataset untouched. Fit on earlier development data, choose a small number of variants on a separate chronological validation block, then freeze a future evaluation block. Group inference by NFL season/week, keep both sides of a game together, report the count of independent weeks, and avoid stopping because cumulative P&L first turns positive. Two contemporary weeks cannot support a useful claim of robustness.

Report total net P&L, P&L per contract, mean and median game outcomes, weekly P&L, return on the actual shared bankroll, peak cash committed, inventory duration and worst forced exits. A strategy passes only if positive net value persists under credible fill/latency/exit assumptions and does not depend on unfinished windows or a few exceptional games. A numerical sample-size target should follow a variance/power calculation on corrected development data; choosing an arbitrary game count now would imply precision we do not have.

## What is delivered and what remains unmeasured

The companion audit kit contains:

- `audit_maker.py`: recomputes all cohort/weighting results, fixes NFL week grouping and records source hashes.
- `reproduce_defects.py`: reproduces the four defects against pinned, unchanged source function bodies.
- `quote_guards.py`: research primitives for window/book admission, joint risk and cash reservations, downsizing, and pair economics. These are not integrated exchange execution code. Cancellation acknowledgment, precision/lot rounding, fee history and payoff validation remain caller responsibilities.
- `test_review.py`: **8 passing tests**, including the four original counterexamples, deadline boundaries, invalid/stale book rejection and exhaustive fill-subset risk checks for the test scenario.
- `results/`: machine-readable recalculations, derived per-game audit rows and defect evidence.
- `fetch_sources.py` and `SOURCE_MANIFEST.json`: restore the exact required private-repository source files from an existing clone or authenticated GitHub CLI, checking hashes. Repository-backed files are not duplicated in this delivery.

The important missing measurement is still **a corrected, depth-aware, continuous replay or forward paper evaluation of the exact seven-day-to-three-hour strategy**. The committed summaries cannot provide that. This audit establishes why the existing verdicts are not comparable, identifies concrete defects to repair, and supplies a testable improvement path; it does not replace the missing execution evidence with another optimistic ROI.
