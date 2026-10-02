# Q6S5 KXMLBSPREAD STRATEGY-FILL / PnL PATH — FREEZE KERNEL (one knob `fill_model`)

**File date convention:** `2026-09-25` = kick date (Conductor kick stamped 2026-09-25T02:24:30-04:00). **Actually frozen / declared pre-outcome at:** `2026-09-29T16:52:00-04:00` (ET).  
**Owner:** R&D Variants (freeze; implement only after Conductor ACCEPT) → Simulator → Examiner  
**Status:** FROZEN — FREEZE_ONLY. Awaiting Conductor **ACCEPT + IMPLEMENT GO**. No cloud agent, no PR, no live Kalshi HTTP, no orders, no `admit.py` until then.  
**Parent packet:** `Q6S5-KXMLBSPREAD-FEEQUEUE-HARNESS` (series KXMLBSPREAD only)  
**Freeze ID:** `Q6S5-KXMLBSPREAD-STRATEGY-FILL`  
**Feature family:** **`strategy_fill_pnl_path`** (Q6S5-MLBSPREAD-STRATEGY-FILL), orthogonal to the existing `analysis_slice` family. It is not F1/F2/F3, not S1 KXMLBGAME ML, not Q6-000, not Cap-SR, and not Q6S1.  
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch` (PR59 squash-merge `cb8957d7086c9ab82a1d25090bf90d6c17fbc217`: I checked it read-only on GitHub. Parent is `f349ffa8…` and it was committed 2026-09-25 02:22:35 ET.)  
**Proposed lab dir:** `kalshi_q6s5_kxmlbspread_strategy_fill_lab_20260925/`. It has **not** been created. It gets created at implement, after ACCEPT.

## Authority and kick

| Item | Path | sha256 | Verify |
|---|---|---|---|
| Conductor KICK | `packets/CONDUCTOR_KICK_VARIANTS_Q6S5_STRATEGY_FILL_FREEZE_2026-09-25.json` | `dc19794bdb8e26c3a3f4fe86eadc9bec1b02db97d508fca9426e3c3eddfb6bc8` | MATCH |
| Authority: Conductor ACCEPT Examiner trades-join ITERATE-3 | `packets/CONDUCTOR_ACCEPT_EXAMINER_Q6S5_KXMLBSPREAD_TRADES_JOIN_ITERATE_2026-09-25.json` | `ac713e5fcbdda218d98e88bf4faab340204d8ad47dc9f0613d3762feca69b50d` | MATCH (= queue `authority_sha256`, = MAXIMIZE 0220ET cite) |
| Authority: Conductor QUEUE | `packets/CONDUCTOR_QUEUE_Q6S5_STRATEGY_FILL_FREEZE_AFTER_Q6S1_2026-09-25.json` | kick cites `08aa54de2b47314e9d27342c1bf3824400d3c434770d339f2e3c253ee90084f6`; **on disk `7472b8ac01fd906577c49eb4d96b8fd5dbb2d7766c5a87fa86e47b3bffad2c61`** | **MISMATCH (gap)**. The on-disk queue has post-kick fields (`not_kicked_yet=false`, `kicked_at_et`, `kick_packet`, `kick_sha256`). No file anywhere under `/workspace/lab` hashes to `08aa54de…`, and there is no `_prev` copy. I have not recreated it. |
| Authority: Conductor MERGE PR59 | `packets/CONDUCTOR_MERGE_Q6S1_KXATPMATCH_INVENTORY_REPROOF_PR59_2026-09-25.json` | `ef037c2c628f98a4db87fc05ffefb6a985ab525fcdfcd5ec84e003ef46f8098f` | MATCH (= MAXIMIZE 0224ET cite); merge commit `cb8957d7…` exists on GitHub |
| Latest MAXIMIZE pin | `packets/MAXIMIZE_PIN_2026-09-25_0224ET.md` / `.json` | `2eac2200cb03d958a7bc047749809373cf20535ec49ac273bf341aabdd038612` / `bdae9cd790131e68192f07766300fdd12a754ec691fd1c1a2bf2fab8eb6a875a` | pinned |
| Prior MAXIMIZE pin | `packets/MAXIMIZE_PIN_2026-09-25_0220ET.md` / `.json` | `cd0831180b2673aa8184659354ba703d8a59629ca216f7f01a7f44c94f293aa9` / `f23653fbf0ac82e6dc66dcf058553057ea7bcafae069d7b35d5f31e04321a6c5` | pinned |

## Existing pins carried (kick `pin_existing`), re-hashed on box 2026-09-29

| Pin | Path on disk | Expected sha256 | Result |
|---|---|---|---|
| measured READY | `lab/astra-capture/q6s5-kxmlbspread/measured/READY_NOT_SCORED.json` | `0617d540763d71a813672c9f9aa6766072c8461a1290c124b89e9fb3f2bf5de2` | **MATCH** |
| trades READY | `lab/astra-capture/q6s5-kxmlbspread/trades_fills_2026-09-25/COLLECTOR_READY_TRADES_NOT_SCORED.json` | `57194f272ab6bbe7a4d116c1fd4aabd5199e3a02a6cd96ed5cc6b7bd4bafb867` | **MATCH** |
| FEE_PIN | `lab/governance/astra/packets/EXAMINER_FEE_PIN_Q6S5_KXMLBSPREAD_LIVE_SERIES_2026-09-25.json` | `9c0f3554eedc582ed4bed940575bf7ee6c0540ce5134140c5ea19e7c458d2b6a` | **MATCH** |
| Examiner trades-join SCORE | `lab/governance/astra/packets/EXAMINER_SCORE_Q6S5_KXMLBSPREAD_TRADES_JOIN_2026-09-25.json` | `a18f2ad2f704d10ec526ccd2808edf8088f88de307ff8b3fe9845fa14ddde05a` | **MATCH** |

Context pins (all re-hashed): Q6S5 harness freeze `4f65dcdf536755b9f7dc2449c2dcd90b2df74cdf99a441b676f1a71c4d709c6e` (MATCH) · harness ACCEPT `5adc42f9c9533238a2187aafe7593bdf1b8cdec6d12b8d3e9b12cb5ab29000fc` (MATCH) · trades-join SCORECARD `e3eeb1a07fddc08824a02a78a68b7f4aba69d77d8cbe5edb0b970bc61c69a9d1` (MATCH vs ACCEPT) · SIMULATOR_READY trades-join `5b47dea926a57e3f1c424e8df62f56ef9b1f02eea87bdd426b4e9248c21465f4` · Examiner ACK of ACCEPT `8fd52262d14c7eb74f0b77dc093a667100d25681c700515d74a910bb6457e8f9` · CLOCK_ADMIT `f73bbaf3faaaa73186a233bfc21699d8ee3c47779253902ccc86159b3cbd7422` · panel_admitted `e36de2d1ce6286dff90d25f2fae680170c8a469c443c1beed974ffe80383fba1` (admitted_at 2026-09-25T04:37:47Z; 6 events / 12 markets) · Q6S1 freeze `d86f7a402ea63fb132d80480f844a954fe9061a27b9b6bed125f9785ae64640e` (pattern only) · v1.2 template `56bcf6269a42031d9d90496e9a65c2292321aed2165033f6fb44ff8cc4d6b1cc` (MATCH) / md `ad1dd2834652b8e9be331ddf2f3ec900ea587efb042251fde6452532b2e36394` · p16 PDF `7e55bc260526aa5088ee31f74475851219ab2cd7f19fdd2f0dd5e9f998c8b45e` · feebook `22371178cb2663250b4762f328069571c48cb551` FIXED · rails `6a28e0d6254327ea4e6451c781bec56215ac6cac` FIXED.

## New constraint: ADMIT-1 capture gap (Conductor, Sep 29)

| Item | Path | sha256 | Status |
|---|---|---|---|
| Conductor RULING (ADMIT-1 outage gap + weather/card03) | `packets/CONDUCTOR_RULING_ADMIT1_OUTAGE_GAP_WEATHER_CARD03_RELAUNCH_2026-09-29.json` | `ac7cfe63623ca342ab5b4285ff58382a8138b58fb6cd8e95310a5d30d90304f2` | **PINNED (present; prefix `ac7cfe63…` matches)** |
| Collector gap record (cited by ruling) | `lab/astra-capture/prospective/ADMIT1_OUTAGE_GAP_2026-09-27_to_2026-09-29.json` | `4f2a5e2693f809e592238c0bf58ecac93f982fb8809c98ca81e51a41d8a65198` | **PINNED (MATCH vs ruling `gap_record.sha256`)** |

The ruling makes this gap permanent, from `2026-09-27T13:31:52Z` to `2026-09-29T20:39:41Z` (about 55.1 h), with **no backfill, no interpolation, and no re-admit**.

**Exclusion rule for this packet (strict, fail-closed):**
1. **Enforced exclusion window:** `[2026-09-27T00:00:00Z, 2026-09-30T04:00:00Z)`. This is a calendar superset of the ruling's exact gap and covers all of Sep 27–29 in both UTC and ET. Any **capture, book, trade, market-status or settlement record** whose timestamp falls in this window is **excluded**. That covers book `captured_utc`/filename stamp, trade `created_time`, market GET `captured_utc`, and the settlement GET `captured_utc` plus `settlement_ts`/determination time. The narrower ruling window is recorded as `ruling_gap_utc` for reference. This packet-local over-exclusion does not change the ruling's "post-relaunch capture scorable as normal" for ADMIT-1 itself.
2. **Closed input manifest:** the runner may read only the sha-pinned inputs in `SOURCE_PINS.json` and must check each sha256 before reading. A mismatch is a hard fail. Nothing is filled in to cover a gap.
3. **Per-row filter:** every row goes through the window check. Rows inside the window are dropped and counted in `excluded_admit1_window_n` (by source: books / trades / markets / settlement). None are imputed.
4. **ADMIT-1 recorder DB is refused as input:** `lab/astra-capture/prospective/capture.sqlite` belongs to a different panel and must never be read by this packet.
5. **Pre-run assertion:** all currently pinned Q6S5 inputs lie in `[2026-09-23T22:06:01Z, 2026-09-25T06:03:02Z]`. That is the trade `created_time` min through the trades-capture end, with books `20260925T044415Z..20260925T053406Z`. So the expected `excluded_admit1_window_n = 0` for the current pins. Any non-zero count must be reported, not hidden.
6. **Future settled re-GET** (Collector-owned, public GET-only, not Variants) is admissible only if its `captured_utc` is outside the window and it is pinned by amendment before the run.
7. **Required unit test:** a synthetic row timestamped inside the window must be rejected.

## Why this knob

Examiner ITERATE-3 (`a18f2ad2…`) classified 11,744 native public trades, but `maker_vs_taker_roi_delta` and `fresh_vs_stale_gap` stayed null because **no strategy fill/PnL series exists** and invented fills are refused. The Conductor queue/kick asks for one orthogonal knob that can produce a strategy fill + PnL series against measured books plus public trades **without inventing fills**. `fill_model` is that knob: it declares **where fills come from**, and nothing else.

## Intent (one knob)

Keep feebook + rails FIXED, keep panel_admitted (6/12), measured books and public trades exactly as pinned, keep the fixed strategy below, and keep the arms. Vary **only** `fill_model`.

**One knob only:** `fill_model` ∈ {`public_trade_through_conservative`, `mechanic_demo_observed`}

| Value | Fill source | On-disk availability | Label | Counts toward KEEP (v1.2) |
|---|---|---|---|---|
| `public_trade_through_conservative` | **MODEL**. Maker legs: a pinned public trade from `trades_fills_2026-09-25` prints **strictly through** our resting price **after** the displayed queue-ahead at placement is conservatively used up (rule below). Taker legs: the displayed touch in the pinned measured orderbook snapshot at receipt time. | **AVAILABLE** (measured books: 29 dated orderbook snapshots; public tape 11,744 trades / 12 tickers; both sha-pinned) | `simulated` / tag `replay`; always labeled MODEL, never an observed fill | **No.** Per v1.2 `simulated_fills.counts_toward_keep=false`, it is reported in `simulated_fills` and not in `common_scorecard.fill_rate`. **Not overridden.** |
| `mechanic_demo_observed` | **OBSERVED on Kalshi demo only.** These are fills from The Mechanic's own resting path (rest→poll→cancel on `demo-api.kalshi.co`) on **KXMLBSPREAD** tickers. Mechanic-owned and explicit. Variants places nothing. | **UNAVAILABLE.** No Mechanic demo KXMLBSPREAD artifact exists on disk. Existing Mechanic demo artifacts (`packets/r3_p2_queue_position/…`) are R3-P2 KXNFLGAME/KXNFLSPREAD queue/trade-step samples only. In the two main series files, no row has `fill_count>0`. | `demo`. The value stays declared, and its cells stay **null / UNAVAILABLE**. Nothing is invented and nothing is borrowed from other series. | Only demo/shadow/live fills are eligible for `common_scorecard.fill_rate` under v1.2. Eligible **if and when** a Mechanic demo artifact is pinned by amendment. |

**Why I chose these values:** `public_trade_through_conservative` is the only value that can produce a strategy fill/PnL series from data already pinned on disk without inventing fills. Every maker fill needs a real public print through our price, and every taker fill needs a real displayed level. The rule is deliberately stricter than price-time priority requires: a strictly-through print already implies our level was cleared, and I also require displayed queue-ahead to be used up with no credit for cancels. That biases fill rate **down**, not up. `mechanic_demo_observed` is the only non-model source that fits the house rules (demo only, Mechanic-owned). I kept it declared so the knob does not need a new freeze once a Mechanic artifact lands, but it is not usable today. I rejected Lee-Ready tick-rule inference, mid-crossing heuristics, "touch = fill" for resting orders, and any fill-probability or queue model fitted on outcomes, because each of them either infers trade direction or invents fills.

## Fixed strategy (not a knob; declared pre-outcome)

There is no forecasting signal in this packet (the harness freeze had Strategy=None). To measure execution/fill economics **without adding a directional model**, which would be a new signal and in S1/Q6-000 retune territory, the strategy is **symmetric, two-sided, 1 contract, at the touch, held to settlement**:

- **Universe:** the 12 panel_admitted KXMLBSPREAD markets (`e36de2d1…`), verbatim. No other series.
- **Placement instants:** each dated measured orderbook snapshot `(ticker, captured_utc)` under `measured/raw/orderbooks/`, but **only** if the latest measured market GET for that ticker at or before `captured_utc` shows `status == "active"`. Finalized, determined or closed markets get no placement. The undated "latest" copies are duplicates and are ignored.
- **Maker legs (per placement × side ∈ {yes, no}):** a 1-contract post-only limit bid at the **best displayed bid** for that side (`orderbook_fp.yes_dollars` / `no_dollars`), joining the **back** of the queue. `queue_ahead = displayed size at that price in the snapshot`. **Cancel/replace:** the order is cancelled (model) at the next measured snapshot of the same ticker. So at most one live maker order per (ticker, side) at any time, and the same prints are never reused across our orders. The last order rests until the earliest of: a market GET showing status ≠ active, or the per-ticker trades request `ts_utc` (tape end) in `trades_fills_2026-09-25/requests.jsonl`. An unfilled order ends unfilled, with zero position and no PnL.
- **Taker legs (per placement × side):** buy 1 contract at the **displayed best ask** for that side (= 1 − best opposite bid), at `captured_utc`. This needs a displayed opposite-bid size ≥ 1. If there is no displayed opposite bid, there is no taker fill (null, not invented).
- **Hold to settlement.** No exits, no sizing changes, no parameter search.

## `public_trade_through_conservative`: exact maker rule

For a resting **YES** bid at price `p` placed at `t0` (use NO / `no_price_dollars` symmetrically for a resting NO bid):
1. **Receipt-time information set:** only the snapshot at `t0`, plus public trades with `created_time > t0` and before the order's cancel time. Trades at or before `t0` are ignored (no lookahead or backfill).
2. **Our-side prints:** native `taker_side == "no"` (taker sells YES and hits YES bids; equivalently `taker_book_side == "ask"` per Mechanic `R3_P2_TRADE_STEP_FILL_LABEL_v1`). If a row's native taker fields disagree, the row is excluded. **Lee-Ready REFUSED.** No direction is ever inferred.
3. **Conservative queue depletion:** `cum` = sum of `count_fp` over our-side prints with `yes_price_dollars ≤ p` since `t0`. No credit is given for cancels or modifies ahead of us. Displayed fractional sizes are used as-is.
4. **Fill:** at the **first** our-side print with `yes_price_dollars < p` (strictly through) at which `cum` (including that print) is ≥ `queue_ahead + 1`. Fill quantity = 1, fill price = **p** (our limit, not the through price), fill time = that print's `created_time`.
5. **Labels on every modeled fill row:** `fill_source="MODEL:public_trade_through_conservative"`, `observed=false`, `tag="replay"`. **Stated assumptions:** price-time priority holds; our order joins at the back; no hidden liquidity or latency advantage; the public tape is complete for our window (429 gaps and empty tickers such as `TBPHI-TB2` count as no prints and are never imputed).

## PnL arithmetic (packet-local; not the v1.2 `net_pnl` formula)

For each filled contract with an **observed** settlement: `pnl = settle_value − fill_price − fee`, with `settle_value = $1.00` if our side matches the observed `result`, else `$0`.
- **Settlement source:** measured raw/markets GET bodies with `status == "finalized"` and a non-empty `result` (on disk now for 6 of 12: HOUATH ×2, LAASEA ×2, SDLAD ×2). The 6 Sep-25 markets (PITDET, TBPHI, NYMWSH ×2 each) have **no settlement on disk**. Their positions are `unresolved_inventory`, and their PnL is **null** unless a Collector settled re-GET is pinned by amendment (ADMIT-1 window rule applies).
- **Fee:** `feebook.order_fee(role, 1, price)` @ `22371178…`, using **only** the FEE_PIN-observed series terms `fee_type=quadratic`, `fee_multiplier=0.5`. The maker role resolves through `feebook.resolve_terms`, and this freeze does not assert its value. Label **CACHE_NOT_R1P1** (see Fee).
- **Arm metrics:** `maker_vs_taker_roi_delta` = ROI(maker legs) − ROI(taker legs), where ROI = Σpnl / Σ(fill_price + fee) over resolved filled contracts. `fresh_vs_stale_gap` = ROI(content_fresh placements) − ROI(stale placements), using the rails `content_fresh_flag` at the placement snapshot.
- v1.2 `common_scorecard.net_pnl_*` stays null because its formula is `pending_definition` and must not be invented. Rewards are not modeled (no rewards thesis).

## Arms (kept exactly)

| Arm | analysis_slice | Role under `fill_model` |
|---|---|---|
| **Q6S5A0** | `maker_vs_taker_native` | Splits the fill/PnL series into maker legs vs taker legs; produces `maker_vs_taker_roi_delta` |
| **Q6S5A1** | `content_fresh_vs_stale_bin` | Splits placements by rails `content_fresh_flag` at the placement snapshot; produces `fresh_vs_stale_gap` |

Grid = 2 arms × 2 `fill_model` values. Cells for `mechanic_demo_observed` stay **null / UNAVAILABLE**. All cells stay **null** until the run is Examiner-scored.

## Fee

The FEE_PIN (`9c0f3554…`) observed `fee_type=quadratic`, `fee_multiplier=0.5` in GET `/series/KXMLBSPREAD` (captured 2026-09-25T04:41:35Z), but **`feebook_formula_id` = null**. So the fee is **CACHE-LABELED / `CACHE_NOT_R1P1`**, with `fee_honest=false` and `claim_as_live_R1P1=false`. **Not R1-P1.** Stresses: `fees_2x` and `one_tick_worse` (one tick = $0.01 against our side on every fill), both declared pre-outcome.

## Dead-card / live-pin overlap (named)

| Card / pin | Handling |
|---|---|
| **Invent fills / PnL** | **REFUSED.** It is the nearest dead card. Every fill is either a MODEL tied to a real public print or displayed level, or a pinned demo observation. |
| **S1 KXMLBGAME ML retune** | **FORBIDDEN.** Spread-only; no ML signal and no directional model. |
| **Q6-000 retune** | **FORBIDDEN.** Pointer only (scoreboard Q6-000 / Arm D KEEP +$345.24 / +6.90%, unchanged). |
| **Cap-SR reopen** | **FORBIDDEN** |
| **Refiner routing** | **NONE.** This is a measurement ITERATE path, not strategy rehab. |
| **Q6S1 retune** | **FORBIDDEN.** PR59 merged; Examiner-owned. |
| Card 06 open-window | CLOSED; do not reopen |
| Q6S5 `analysis_slice` harness | Parent; arms reused verbatim; not retuned |
| Lee-Ready | **REFUSED** |

## Scorecard fields (null now)

`results`, `pnl`, `maker_vs_taker_roi_delta`, `fresh_vs_stale_gap`, `fill_rate_simulated`, `filled_contracts_simulated`, `requested_contracts_simulated`, `unresolved_inventory`, `settled_join_n`, `n_books`, `excluded_admit1_window_n`, plus the per-cell arm ROI. All stay **null** until an Examiner-scored run. Prior ITERATE-3 counts (11,744 / 6 / 12) are pins, **not** copied into this scorecard.

**Examiner scorecard v1.2 stub** (template `56bcf626…`), following the Q6S1 pattern: scorecard / verdict / common_scorecard (11 metrics) / simulated_fills / stress_sensitivity / executable_dollars_per_day / study_label / `preregistration_checklist.gate_status` are all **null** (`measured=false`). Declared pre-outcome:
- `simulated_fills.fill_model_ref` = this freeze
- `counts_toward_keep=false`, not overridden
- `study_label` stays null; Variants proposes "historical replay" for the MODEL value, and the label is owned by Examiner/Archivist
- controls: `no_trade` applies (PnL 0 baseline); `market_only` and `simple_model` do not apply (no forecast)
- calibration: `emits_probabilities=false`
- no rewards thesis
- no default overrides

## p16 preregistration checklist

Source: the v1.2 `preregistration_checklist` block (PDF p16, "Minimum preregistration"). Q6S5 is not a card 01-04 study; I completed the checklist under the Conductor all-new-freeze rule. Declared pre-outcome at 2026-09-29T16:52:00-04:00. Examiner `gate_status` is null.

| # | Item | Status | Evidence |
|---|---|---|---|
| 1 | market_universe | **satisfied** | panel_admitted 6 events / 12 markets `e36de2d1…`; KXMLBSPREAD only |
| 2 | exclusions | **satisfied** | KXMLBSPREAD only; non-active markets at placement excluded; ADMIT-1 window `[2026-09-27T00:00Z, 2026-09-30T04:00Z)` excluded; ADMIT-1 `capture.sqlite` refused; conflicting native taker fields excluded; no S1/Q6-000/Cap-SR/Q6S1 |
| 3 | receipt_time_information_set | **satisfied** | book snapshot at `t0` plus trades with `created_time > t0` only; sha-pinned inputs |
| 4 | fee_regime | **satisfied** | feebook @22371178 with FEE_PIN terms quadratic×0.5; CACHE_NOT_R1P1; fees_2x stress |
| 5 | order_timing | **satisfied** | placement at each eligible measured snapshot; maker cancel/replace at next snapshot or tape end or status ≠ active; taker at `t0` |
| 6 | sizing | **satisfied** | 1 contract per leg per side; fixed |
| 7 | fill_model | **satisfied** | one knob, 2 values, rules above; demo value UNAVAILABLE |
| 8 | stopping_rules | **satisfied** | freeze-before-implement; ACCEPT before cloud; single cloud; Examiner HOLD_PRE_PR; hold to settlement; unresolved stays null |
| 9 | evaluation_metrics | **satisfied** | arm ROI delta / gap + simulated_fills + stresses + v1.2 nulls |
| 10 | limit_candidate_variants | **satisfied** | one knob `fill_model` × 2 values; arms Q6S5A0/A1 unchanged |
| 11 | log_every_attempted_variant | **satisfied** | only the 2 values are declared; any other value needs a new freeze |
| 12 | separate_discovery_tuning_evaluation_periods | **missing** | No untouched evaluation period exists. The only pinned books/trades (2026-09-25) were already seen by Simulator/Examiner for classification counts, though not fills or PnL. No parameter is tuned (all are fixed a priori), but a clean holdout would need new post-freeze capture outside the ADMIT-1 window. |

Counts: satisfied 11, n/a 0, missing 1.

## Integrity (Clock gate)

- Commit the pinned bytes **verbatim**, with digests checked by `sha256sum`. **No labeled recreations.** Never recreate the queue `08aa54de…` bytes.
- `digest_all_match_claimed=false`. Absent items:
  - queue bytes `08aa54de…`
  - Mechanic demo KXMLBSPREAD artifact
  - KXMLBSPREAD `formula_id`
  - Sep-25 settlements for 6/12 markets
  - Archivist fee/account-version manifest
  - untouched evaluation period
  - ADMIT-1 capture from 2026-09-27T13:31:52Z to 2026-09-29T20:39:41Z (permanent, by ruling)
- RULE-FROZEN-EDIT-PREV-BYTES-001: this freeze **creates only new files**. No already-frozen file was edited, so there was no `_prev` write.

## Merge gates

Units green at implement, including the ADMIT-1 window rejection test, the lookahead test, the Lee-Ready refusal test and the no-invent test. `results`/`pnl`/arm ROI stay null until Examiner. Examiner HOLD_PRE_PR moves to READY NOT_SCORED only after PR branch sha verify + merge. **HOLD for Conductor ACCEPT: no CloudAgent, no PR, no `admit.py`, no live Kalshi HTTP, no orders.**

## Refuse binds

invent fills/PnL · Lee-Ready · live orders · Variants demo orders (Mechanic only) · dual-cloud · claim CACHE as R1-P1 · S1 KXMLBGAME ML retune · Q6-000 retune · Cap-SR reopen · Refiner routing · Q6S1 retune · `admit.py` · reading ADMIT-1 `capture.sqlite` · any data in the ADMIT-1 window · backfill/interpolate · editing prior SCORE/ACCEPT/FEE_PIN/HOLD/READY bytes · counting simulated fills toward KEEP
