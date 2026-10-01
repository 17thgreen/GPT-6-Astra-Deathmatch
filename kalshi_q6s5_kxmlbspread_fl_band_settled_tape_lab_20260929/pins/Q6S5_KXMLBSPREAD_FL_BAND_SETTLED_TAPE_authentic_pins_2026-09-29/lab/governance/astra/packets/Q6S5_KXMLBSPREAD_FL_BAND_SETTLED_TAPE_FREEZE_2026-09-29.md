# Q6S5 KXMLBSPREAD FL-BAND SETTLED-TAPE — FREEZE KERNEL (one knob `price_band`)

**File date:** `2026-09-29`. **Frozen / declared pre-outcome at:** `2026-09-29T17:26:35-04:00` (ET). No band ROI, maker return, or settlement-joined number has been computed by anyone for this packet. I only checked field presence (`status`, non-empty `result`, `close_time`, `settlement_ts`) and taker-field value domains. I did not read or print any `result` value.
**Owner:** R&D Variants (freeze; implement only after Conductor ACCEPT) → Simulator → Examiner
**Status:** FROZEN — FREEZE_ONLY. Awaiting Conductor **ACCEPT + IMPLEMENT GO**. No cloud agent, no PR, no live Kalshi HTTP, no orders, no `admit.py` until then.
**Parent packet:** `Q6S5-KXMLBSPREAD-FEEQUEUE-HARNESS` (series KXMLBSPREAD only)
**Freeze ID / experiment id:** `Q6S5-KXMLBSPREAD-FL-BAND-SETTLED-TAPE`
**Feature family:** **`settled_tape_fl_band`** (Q6S5-MLBSPREAD-FL-BAND). It is orthogonal to the Q6S5 `analysis_slice` family (PR58) and the `fill_model` family (PR60). It is not F1/F2/F3, not S1 KXMLBGAME ML, not Q6-000, not Cap-SR, and not Q6S1. It is the first real-data run of the R3-P3 "post-fee ROI by 10¢ band / maker vs taker" measurement object, which was frozen 2026-09-22 (`0ed69714…`) and has stayed null because the R3-P3 panel never admitted a settled trade.
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`, main `12e760f5bd3b622d8f0d70a74c28655464e2b93c` (PR60 squash, per Conductor MERGE `3486a2fe…`; I checked it read-only with a clone).
**Proposed lab dir:** `kalshi_q6s5_kxmlbspread_fl_band_settled_tape_lab_20260929/`. It has **not** been created. It gets created at implement, after ACCEPT, as the **sole** Variants cloud and only once PR60's cloud (`bc-c45d800a…`) is closed.

## Selection: why this probe (Variants leftover survey, 2026-09-29)

Step 1: I found no same-day Conductor ACCEPT/KICK/QUEUE that names an unfiled Variants freeze. The 2026-09-29 packets are the Q6S5 strategy-fill ACCEPTs `c6f95b32…` / `a5398129…`, reconcile `0f33a94c…`, MERGE PR60 `3486a2fe…`, MAXIMIZE 1655ET, the ADMIT-1 ruling `ac7cfe63…` + erratum `31da5974…`, and the Examiner C1 note `fe5ba611…`. All of them are filed or are not addressed to Variants.

Step 2: ranked leftovers (held, blocked, and done waves excluded):

| Rank | Candidate | Data it needs | Why ranked here |
|---|---|---|---|
| **1 (PICK)** | **Q6S5 FL-band settled-tape** (`price_band`) | **Nothing new.** Uses 11,723 public prints (Collector per-ticker metadata) on the 6 Q6S5 panel markets that are already `finalized` with non-empty `result` in the pinned measured GETs. Everything is sha-pinned. | This is the largest honestly scorable body on disk. It answers the question the maker bakeoff lacks: **where in price the maker edge sits.** It needs no invented fills and no new GET, it sits outside the ADMIT-1 window, and it is not held. |
| 2 | Q6S5 strategy-fill follow-on knob (e.g. maker `quote_offset` join vs improve-1¢, or `cancel_horizon`) | Examiner score of PR60 first. A Collector settled re-GET for the 6 Sep-25 markets is also needed, and their `close_time` 2026-09-28T22:40/45Z falls **inside** the ADMIT-1 exclusion window. | The strategy-fill placements are starved. Only the 6 Sep-25 markets were `active` at book time, and they have 21 prints in total. Stacking a second Variants knob before Examiner READY/score would tune on an unscored wave. |
| 3 | ETH-RJ `KXETH15M` settled-resolution join | A new Scout/Collector settled re-GET under ADMIT-1 429 contention. | Sequenced behind ATP-RJ by MERGE PR54 `d02674a0…` ("ETH-RJ unfrozen until measured settled_join_n or documented blocker"). No packet documents that blocker, and ATP post-ACCEPT settlements are still `[]` per ACK `b9824df1…`. It is join-gate plumbing, so little money is at stake. |

Excluded: PM-008 / weather / card03 (HELD, MAXIMIZE 1655ET). R3-P2 v2 (needs a new Mechanic demo series, EXAMINER_SCORE `e66d2636…`). Q6S3 (DEFER, 429) / Q6S4 (HOLD, thin) / Q6S2 (C2 reinforce only), per the sports screen ACCEPT `2aefbc17…`. C1 PIT@CLE (NOT_SCORED). Card 06 (CLOSED). All `-RJ` waves already done.

## Authority and context pins (re-hashed on box 2026-09-29)

| Item | Path | sha256 | Verify |
|---|---|---|---|
| Conductor MERGE PR60 (latest main) | `packets/CONDUCTOR_MERGE_Q6S5_KXMLBSPREAD_STRATEGY_FILL_PR60_2026-09-29.json` | `3486a2fe71da0be40a3cb6202abcc30e1783515180e20f594b3c25b034414bef` | MATCH |
| Latest MAXIMIZE pin | `packets/MAXIMIZE_PIN_2026-09-29_1655ET.md` / `.json` | `50d78b7cb2aa40b5e77312b1b9ac28394ff356e6a5937c3f76b7597bc661b357` / `86e99d7df05774ef393b716f5f5adc7b0ffe6963e3e683a3baa586a9aa8daa39` | pinned |
| Conductor ACCEPT strategy-fill (implementation) | `packets/CONDUCTOR_ACCEPT_VARIANTS_Q6S5_STRATEGY_FILL_FREEZE_2026-09-29.json` | `c6f95b32a9224a6beede1a8c0e3d7f0a5a4530cc8b3d0b9d997995f65d64f8f3` | MATCH |
| Conductor ACCEPT strategy-fill (companion rulings) | `packets/CONDUCTOR_ACCEPT_Q6S5_KXMLBSPREAD_STRATEGY_FILL_FREEZE_2026-09-29.json` | `a5398129aa45c5dee5fdd15656a252bb6c460d00e4f5b06360ce522de0f968b4` | MATCH |
| Conductor RECONCILE (sole cloud) | `packets/CONDUCTOR_RECONCILE_Q6S5_STRATEGY_FILL_DUAL_ACCEPT_SOLE_CLOUD_2026-09-29.json` | `0f33a94c970eec6a9863041396071c78ce64b58abc8a7ab91f48062fbfc052b0` | MATCH |
| Sibling freeze (house format) | `packets/Q6S5_KXMLBSPREAD_STRATEGY_FILL_FREEZE_2026-09-25.md` | `9f50ba19694083c774bbe2a6cff491d1a2f81ed3a6f9cc21a3641a938c84955d` | MATCH |
| Parent harness freeze / ACCEPT | `packets/Q6S5_KXMLBSPREAD_FEEQUEUE_HARNESS_FREEZE_2026-09-25.md` / `packets/CONDUCTOR_ACCEPT_Q6S5_KXMLBSPREAD_FEEQUEUE_HARNESS_2026-09-25.json` | `4f65dcdf536755b9f7dc2449c2dcd90b2df74cdf99a441b676f1a71c4d709c6e` / `5adc42f9c9533238a2187aafe7593bdf1b8cdec6d12b8d3e9b12cb5ab29000fc` | MATCH |
| Examiner trades-join SCORE ITERATE-3 / scorecard | `packets/EXAMINER_SCORE_Q6S5_KXMLBSPREAD_TRADES_JOIN_2026-09-25.json` / `packets/EXAMINER_SCORECARD_Q6S5_KXMLBSPREAD_TRADES_JOIN_2026-09-25.md` | `a18f2ad2f704d10ec526ccd2808edf8088f88de307ff8b3fe9845fa14ddde05a` / `e3eeb1a07fddc08824a02a78a68b7f4aba69d77d8cbe5edb0b970bc61c69a9d1` | MATCH |
| Conductor ACCEPT Examiner ITERATE-3 | `packets/CONDUCTOR_ACCEPT_EXAMINER_Q6S5_KXMLBSPREAD_TRADES_JOIN_ITERATE_2026-09-25.json` | `ac713e5fcbdda218d98e88bf4faab340204d8ad47dc9f0613d3762feca69b50d` | MATCH |
| FEE_PIN (live /series body) | `packets/EXAMINER_FEE_PIN_Q6S5_KXMLBSPREAD_LIVE_SERIES_2026-09-25.json` | `9c0f3554eedc582ed4bed940575bf7ee6c0540ce5134140c5ea19e7c458d2b6a` | MATCH |
| Clock ADMIT | `packets/CLOCK_ADMIT_Q6S5_KXMLBSPREAD_2026-09-25.md` | `f73bbaf3faaaa73186a233bfc21699d8ee3c47779253902ccc86159b3cbd7422` | MATCH (= capture copy) |
| R3-P3 FL freeze kernel (band lineage) | `packets/R3-P3_FL_MAKER_TAKER_BANDS_FREEZE_KERNEL_2026-09-22.md` | `0ed697149136acb3aa840aeeb79d11c8f6ef80f37ce4dd692a3cb690212206a7` | MATCH (= registry `parent kernel`) |
| R3-P3 10¢ band registry (pre-registered 2026-09-23T00:12:45Z) | `packets/r3_p3_fl_maker_taker/bands_registry_10c.json` | `0860cbe28d28ecc6142ddf6f1ebb67792084264ed82e0b4d868c3b3138ea5312` | MATCH (= capture copy) |
| R3-P3 Adversary refuse-bind | `packets/R3-P3_ADVERSARY_REFUSE_BIND_2026-09-22.md` | `6b6690cd6bf3b7e4833919a8f16be497027902ca726d22a64ef4bde2b29d5636` | binds carried |
| R3-P3 Examiner scorecard stub | `packets/EXAMINER_SCORECARD_STUB_R3-P3_FL_MAKER_TAKER_2026-09-22.md` | `d67348b92d925aaae104779e4855f75fa460058894912af072a03c5ec315de1d` | NOT_SCORED (settled N=0) |
| v1.2 scorecard template json / md | `templates/EXAMINER_KALSHI_SCORECARD_TEMPLATE_v1.2.json` / `.md` | `56bcf6269a42031d9d90496e9a65c2292321aed2165033f6fb44ff8cc4d6b1cc` / `ad1dd2834652b8e9be331ddf2f3ec900ea587efb042251fde6452532b2e36394` | MATCH |
| p16 source PDF | `research/KALSHI_EDGE_RESEARCH_2026-09-24.pdf` | `7e55bc260526aa5088ee31f74475851219ab2cd7f19fdd2f0dd5e9f998c8b45e` | pinned |
| RULE-FROZEN-EDIT-PREV-BYTES-001 | `registry/RULE_FROZEN_EDIT_PREV_BYTES_2026-09-24.md` | `f0aab7d15ca78a097644008db02013eae3a56cb81b2a6aef2cfe6faf21e3e6d1` | pinned |
| Ranking evidence | MERGE PR54 / ACK ATP-RJ probe / sports screen ACCEPT / R3-P2 SCORE | `d02674a0c91430fcf98ba50e921cf097ade4caa27e28ff080aff806dd80de8fb` / `b9824df125ddca21691b3241b5c0d5ea6801ae61659c1ae3922d7ca17b9649ab` / `2aefbc1712a0389d65f565439d5599a7275688e872e8bc67d5c6dde3b1cd81f8` / `e66d2636c771c43e9ea7ff9838a5233eb951e0e3a5e1f01ed800af1a760cf593` | pinned |

Feebook `22371178cb2663250b4762f328069571c48cb551` FIXED · rails `6a28e0d6254327ea4e6451c781bec56215ac6cac` FIXED (rails are not used by this packet).

## ADMIT-1 capture gap (Conductor, Sep 29)

| Item | Path | sha256 | Status |
|---|---|---|---|
| Conductor RULING | `packets/CONDUCTOR_RULING_ADMIT1_OUTAGE_GAP_WEATHER_CARD03_RELAUNCH_2026-09-29.json` | `ac7cfe63623ca342ab5b4285ff58382a8138b58fb6cd8e95310a5d30d90304f2` | PINNED |
| Conductor ERRATUM (card03 window) | `packets/CONDUCTOR_ERRATUM_CARD03_GAP_WINDOW_2026-09-29.json` | `31da5974867ee6230928b641e4a939171bce44260a4b87ee9161ffc8f30477d9` | PINNED (card03 only; ruling otherwise unchanged) |
| Collector gap record | `lab/astra-capture/prospective/ADMIT1_OUTAGE_GAP_2026-09-27_to_2026-09-29.json` | `4f2a5e2693f809e592238c0bf58ecac93f982fb8809c98ca81e51a41d8a65198` | PINNED (MATCH vs ruling) |

**Exclusion rule (strict, fail-closed):**
1. **Enforced exclusion window:** `[2026-09-27T00:00:00Z, 2026-09-30T04:00:00Z)`. Any trade `created_time`, market GET `captured_utc` (filename stamp), `close_time`, or `settlement_ts` inside the window is excluded. The ruling's exact gap `2026-09-27T13:31:52Z → 2026-09-29T20:39:41Z` is recorded as `ruling_gap_utc` for reference only.
2. **Closed input manifest:** the runner reads only the sha-pinned `inputs_core` and `inputs_raw` in `SOURCE_PINS.json` and checks each sha256 before reading. Any mismatch is a hard fail. Nothing is backfilled or interpolated.
3. **Per-row filter:** excluded rows are counted in `excluded_admit1_window_n` (by source: trades / markets / settlement). None are imputed.
4. **ADMIT-1 `lab/astra-capture/prospective/capture.sqlite` is REFUSED as input** and is never opened.
5. **Pre-run assertion:** in-scope trades span `2026-09-23T22:06:01Z..2026-09-25T05:07:00Z` (Collector per-ticker metadata). The 6 in-scope settlement GETs were captured `20260925T051602Z..051942Z`, with `settlement_ts` from `2026-09-25T04:32:18Z` to `05:08:48Z`. So the expected `excluded_admit1_window_n = 0` for in-scope rows. Any non-zero count must be reported.
6. **The 6 Sep-25 panel markets are permanently out of scope for this packet.** Their pinned GETs show `status=active`, no result, and `close_time` `2026-09-28T22:40:00Z`/`22:45:00Z`, which is **inside** the window. Any settlement for them would fall in the window and is fail-closed excluded here. No amendment path, no re-GET.
7. **Required unit test:** a synthetic trade row inside the window, and a synthetic settlement inside the window, must both be rejected.

## Intent (one knob)

Keep everything fixed: the panel (`e36de2d1…`), the pinned public trade tape, the pinned settlement GETs, the band registry, and the fee pin. Vary **only** `price_band`, the price band of the **taker-purchased side** of each public print. For each band, measure the realized settlement return of the **passive (maker) counterparty** of real public prints.

**Not a strategy.** No Astra orders, no Astra fills, no Astra PnL. The observations are other participants' executed public prints, joined ex-post to observed settlement. Astra `results` / `pnl` / v1.2 `net_pnl_*` stay null. This is pricing / adverse-band **measurement**. It is labeled `public_counterparty_realized`, never `pnl`.

**One knob only:** `price_band` ∈ {`Q6S5FL0`, `Q6S5FL1`, `Q6S5FL2`}. Each value is a union of R3-P3 pre-registered 10¢ bands (`0860cbe2…`), applied to `p_taker` (below) by the registry's lo/hi inclusivity. No rebinning, ever.

| Arm | Label | `p_taker` range | Registry bands | Maker counterparty holds |
|---|---|---|---|---|
| **Q6S5FL0** | `longshot_taker` | `[0.00, 0.20)` | b00, b01 | the favorite side at `1 − p_taker` ∈ (0.80, 1.00] |
| **Q6S5FL1** | `mid` | `[0.20, 0.80)` | b02–b07 | the opposite side at (0.20, 0.80] |
| **Q6S5FL2** | `favorite_taker` | `[0.80, 1.00]` | b08, b09 | the longshot side at `1 − p_taker` ∈ [0.00, 0.20] |

## Row construction (declared pre-outcome)

- **Universe:** the 6 panel_admitted KXMLBSPREAD markets whose latest pinned measured market GET shows `status == "finalized"` with non-empty `result`. These are `KXMLBSPREAD-26SEP242140HOUATH-{ATH2,HOU2}`, `KXMLBSPREAD-26SEP242140LAASEA-{LAA2,SEA2}` and `KXMLBSPREAD-26SEP242210SDLAD-{LAD2,SD2}`: 3 events, all "wins by over 1.5 runs". No other series and no other markets.
- **Rows:** every public trade in the pinned raw pages for those 6 tickers. Collector-published counts are 497 / 2,557 / 1,105 / 1,173 / 4,144 / 2,247, for **11,723** in total. These are pins, not results.
- **Native side only:** `s = taker_outcome_side` ∈ {yes, no}. A row is used only if `taker_side == taker_outcome_side` and (`s=yes` ⇔ `taker_book_side=bid`; `s=no` ⇔ `taker_book_side=ask`), consistent with the Mechanic `R3_P2_TRADE_STEP_FILL_LABEL_v1` usage in the sibling freeze. Any other combination is excluded and counted. **Lee-Ready REFUSED**; direction is never inferred.
- **Taker price:** `p_taker = yes_price_dollars` if `s=yes`, else `no_price_dollars`. A row is excluded if `|yes_price_dollars + no_price_dollars − 1| > 1e-9`.
- **Exclusions (counted, never imputed):** `is_block_trade == true`. `created_time ≥ close_time` of the same pinned market GET (post-close prints). Rows in the ADMIT-1 window. A market whose `result ∉ {yes, no}` is excluded as a whole.
- **Weight:** `q = count_fp` (decimal contracts, as published).
- **Settlement:** `Y_s = 1` if `result == s` else `0` (observed field in the pinned GET). `settlement_ts` is read as-is and never invented.
- **Information set:** band assignment uses only the print's own price at its own `created_time`. Settlement is used only as the ex-post label. No row selection depends on outcome or on later prints.

## Metrics (all null now)

Per arm `A`:
- `maker_gross_return_usd[A] = Σ q · ((1 − Y_s) − (1 − p_taker))` = `Σ q · (p_taker − Y_s)`
- `maker_capital_usd[A] = Σ q · (1 − p_taker)`
- `maker_gross_roi[A] = maker_gross_return_usd[A] / maker_capital_usd[A]`
- `taker_gross_roi[A] = Σ q · (Y_s − p_taker) / Σ q · p_taker`
- `n_trades[A]`, `contracts[A]`, `n_markets[A]`, `n_events[A]`

**Primary (H1):** `maker_gross_roi_delta_FL0_minus_FL1 = maker_gross_roi[FL0] − maker_gross_roi[FL1]`.
**Secondary (H2):** `maker_gross_roi_delta_FL2_minus_FL1`.
**Descriptive:** `maker_gross_roi` by each of the 10 registry bands; per-market and per-event arm tables.
**Fee-labeled secondary (CACHE_NOT_R1P1):** `maker_net_roi_cache[A]`. The fee is `feebook.order_fee(role, q, price)` @ `22371178…`, using only the FEE_PIN-observed terms `fee_type=quadratic`, `fee_multiplier=0.5`. Maker role resolves via `feebook.resolve_terms`, and this freeze does not assert the value. `taker_net_roi_cache[A]` is the same with the taker fee.

The primary metric is **gross (pre-fee)** on purpose. It needs no fee claim, which keeps it clear of the R3-P3 Adversary refuse "fee-honest post-fee ROI without R1-P1". Post-fee numbers are CACHE-labeled secondary only.

**Robustness (pre-registered):** leave-one-event-out (3 values) and leave-one-market-out (6 values) of both deltas. Stresses: `one_tick_worse`, which charges the maker $0.01/contract (capital +$0.01, return −$0.01), and `fees_2x` on the CACHE secondary.

**Not in scope:** Mincer–Zarnowitz regression (R3-P3 object 1). Event-clustered inference with 3 clusters is not meaningful, so it stays `null` / `NOT_IN_SCOPE`. `executable_dollars_per_day` stays null (not our executions).

## Hypothesis and reading rule (written before outcomes)

- **H1 (favorite–longshot bias, maker side):** `maker_gross_roi_delta_FL0_minus_FL1 > 0`. Passive counterparties to longshot-buying takers earn more per dollar at risk than mid-band counterparties. The Bürgi–Deng–Whelan "+2.6% maker ≥50¢" figure is a **hypothesis only, not Astra evidence** (Adversary bind).
- **H2:** `maker_gross_roi_delta_FL2_minus_FL1 ≤ 0`. Counterparties to favorite-buying takers (makers holding longshots) do no better than mid.
- **Variants-proposed reading (Examiner owns the verdict):** `supports_H1` if the full-sample delta > 0 **and** ≥2 of 3 leave-one-event-out deltas > 0. `contradicts_H1` if the full-sample delta ≤ 0 **and** ≥2 of 3 LOEO deltas ≤ 0. Otherwise `inconclusive`. **Verdict ceiling ITERATE:** measurement only, no KEEP, `counts_toward_keep=false`. `contradicts_H1` supports a KILL of the FL-band maker thesis **for KXMLBSPREAD only**.
- **Power caveat (declared):** realized return within a market hinges on a single binary outcome, and the 6 markets come from 3 games (HOU2/ATH2 etc. are same-game siblings). The effective sample is 3 events, not 11,723 prints. That is why the verdict ceiling is ITERATE and why LOEO is required.
- **Money path if `supports_H1`:** the next one-knob freeze would put a band filter on the Q6S5 maker leg (quote only the favorite side against longshot takers). That needs an untouched post-freeze settled set (see p16 item 12). No retune of Q6-000.

## Fee

FEE_PIN `9c0f3554…` observed `fee_type=quadratic`, `fee_multiplier=0.5` (GET `/series/KXMLBSPREAD`, captured 2026-09-25T04:41:35Z), and `feebook_formula_id` = null. So the fee label is **CACHE-LABELED / `CACHE_NOT_R1P1`**, with `fee_honest=false` and `claim_as_live_R1P1=false`. **Not R1-P1.** The primary metric is fee-free.

## Dead-card / live-pin overlap (named)

| Card / pin | Handling |
|---|---|
| **Invent fills / PnL** | **REFUSED.** No Astra fills exist or are modeled. The observations are real public prints with observed settlement, labeled `public_counterparty_realized`. |
| R3-P3 FL maker/taker | **Lineage, not a reopen.** Registry bands reused verbatim, and the Adversary refuse-bind is carried (paper EV hypothesis-only, no Lee-Ready, no fee-honest label without R1-P1). |
| Q6S5 `analysis_slice` (PR58) / `fill_model` (PR60) | Siblings; not retuned, not re-run. |
| **S1 KXMLBGAME ML retune** | **FORBIDDEN** (spread series only; no ML signal). |
| **Q6-000 retune** | **FORBIDDEN.** Scoreboard Q6-000 / Arm D KEEP +$345.24 / +6.90%, unchanged. |
| Cap-SR / Q6S1 / Refiner | **FORBIDDEN / NONE** |
| Card 06 open-window | CLOSED |
| Lee-Ready | **REFUSED** |

## Scorecard fields (null now)

`results`, `pnl`, `maker_gross_roi` (per arm and per band), `taker_gross_roi`, both deltas, LOEO/LOMO vectors, `maker_net_roi_cache`, `taker_net_roi_cache`, `n_trades`, `contracts`, `n_markets`, `n_events`, `excluded_admit1_window_n`, `excluded_post_close_n`, `excluded_block_n`, `excluded_taker_conflict_n`, `excluded_price_inconsistent_n`, `reading` all stay **null** until an Examiner-scored run.

**Examiner scorecard v1.2 stub** (template `56bcf626…`) is in `EXAMINER_SCORECARD_STUB_*.json/.md`. Scorecard / verdict / common_scorecard (11 metrics) / simulated_fills / stress_sensitivity / executable_dollars_per_day / study_label / `preregistration_checklist.gate_status` are all **null** (`measured=false`). Declared settings:
- `simulated_fills`: **n/a**, since no fills are modeled (`fill_model_ref` null); `counts_toward_keep=false`
- controls: `no_trade` does not apply (not a strategy)
- `market_only`: applies in the sense that price is the implied probability, so band ROI **is** the market-only calibration residual
- `simple_model`: n/a
- calibration `emits_probabilities=false`; no rewards thesis
- `study_label` null; Variants proposes "historical replay" (retrospective public tape), owned by Examiner/Archivist

## p16 preregistration checklist

Source: the v1.2 `preregistration_checklist` block (PDF p16). Declared pre-outcome at `2026-09-29T17:26:35-04:00`. Examiner `gate_status` null.

| # | Item | Status | Evidence |
|---|---|---|---|
| 1 | market_universe | **satisfied** | 6 finalized panel_admitted markets (3 events) of `e36de2d1…`; KXMLBSPREAD only |
| 2 | exclusions | **satisfied** | 6 Sep-25 markets (no result; close_time in ADMIT-1 window); post-close prints; block trades; native-field conflicts; price-inconsistent rows; ADMIT-1 window; ADMIT-1 `capture.sqlite` refused |
| 3 | receipt_time_information_set | **satisfied** | band from the print's own price at `created_time`; settlement only as ex-post label; sha-pinned inputs |
| 4 | fee_regime | **satisfied** | primary gross (fee-free); secondary feebook@22371178 with FEE_PIN quadratic×0.5, CACHE_NOT_R1P1; fees_2x |
| 5 | order_timing | **n/a** | no Astra orders; public prints only |
| 6 | sizing | **n/a** | no Astra sizing; rows weighted by published `count_fp` |
| 7 | fill_model | **n/a** | no Astra fills modeled or claimed |
| 8 | stopping_rules | **satisfied** | freeze-before-implement; ACCEPT before cloud; single cloud after PR60 cloud closes; single pass over closed manifest; no reruns with altered bands |
| 9 | evaluation_metrics | **satisfied** | primary/secondary deltas, per-band table, LOEO/LOMO, stresses, v1.2 nulls |
| 10 | limit_candidate_variants | **satisfied** | one knob `price_band` × 3 values, fixed from the 2026-09-23 registry |
| 11 | log_every_attempted_variant | **satisfied** | only the 3 arms plus the 10-band descriptive; any other cut needs a new freeze |
| 12 | separate_discovery_tuning_evaluation_periods | **missing** | No untouched evaluation set. These prints were already seen by Simulator/Examiner for side-classification counts (ITERATE-3), though never joined to settlement by band. No parameter is tuned (bands date from 2026-09-23). A clean holdout would need post-freeze settled KXMLBSPREAD markets captured outside the ADMIT-1 window, by Collector, via amendment. |

Counts: satisfied 8, n/a 3, missing 1.

## Integrity (Clock gate)

- Commit pinned bytes **verbatim**, with digests checked by `sha256sum`. No labeled recreations.
- Clock: panel admitted at `2026-09-25T04:37:47Z`. Most in-scope prints **predate** admission: this is a retrospective public tape, not prospective capture. Precedent: ITERATE-3 (`a18f2ad2…`) scored all 11,744 native prints, and the RJ waves used already-settled markets. The study label must be "historical replay", never "prospective". **Conductor ask:** confirm admissibility.
- `digest_all_match_claimed=true` for every pin cited here. `measured/DIGESTS.txt` lists a `STATUS.json` hash that has since drifted (already recorded in the sibling SOURCE_PINS). `STATUS.json` is not an input.
- Absent (declared, not recreated): Examiner-pinned KXMLBSPREAD `formula_id`; untouched evaluation set; settlements of the 6 Sep-25 markets (permanently out of scope here); Archivist fee/account-version manifest; ADMIT-1 capture in the ruling gap.
- RULE-FROZEN-EDIT-PREV-BYTES-001: this freeze **creates only new files**. No frozen file was edited, so there was no `_prev` write.

## Merge gates

Units must be green at implement, including: ADMIT-1 window rejection (trade and settlement), post-close exclusion, Lee-Ready refusal / native-field conflict exclusion, closed-manifest sha fail-closed, a band-assignment boundary test at 0.20 / 0.80 / 1.00 per registry inclusivity, and no-invent (a market without a result produces no row). `results` / all metrics stay null until Examiner. Examiner HOLD_PRE_PR → READY NOT_SCORED only after PR branch sha verify + merge. **HOLD for Conductor ACCEPT: no CloudAgent, no PR, no `admit.py`, no live Kalshi HTTP, no orders.**

## Refuse binds

invent fills/PnL/settlement_ts/markets/depth · label public-counterparty return as Astra PnL · Lee-Ready · live orders · Variants demo orders · dual-cloud · claim CACHE as R1-P1 or "fee-honest" · paper EV as Astra evidence · rebin after outcomes · S1 KXMLBGAME ML retune · Q6-000 retune · Cap-SR reopen · Refiner routing · Q6S1 retune · `admit.py` · reading ADMIT-1 `capture.sqlite` · any data in the ADMIT-1 window · backfill/interpolate · re-GET of Sep-25 settlements for this packet · lookahead in row selection · editing prior SCORE/ACCEPT/FEE_PIN/HOLD/READY bytes · KEEP from this measurement
