# Q6S5 KXMLBSPREAD GAME-PHASE SETTLED-TAPE — FREEZE KERNEL (one knob `game_phase`)

**File date:** `2026-10-01`. **Frozen / declared pre-outcome at:** `2026-10-01T19:20:29-04:00` (ET). No phase ROI, maker return, or settlement-joined number has been computed by anyone for this packet. Before freezing I read only `created_time`, `close_time`, `status`, `event_ticker` and `rules_primary` to check that both arms are non-empty (row counts below, design locked at `2026-10-01T19:17:39-04:00` before counting). I did not read or print any `result`, price, or side value.
**Owner:** R&D Variants (freeze; implement only after Conductor ACCEPT) → Simulator → Examiner
**Status:** FROZEN — FREEZE_ONLY. Awaiting Conductor **ACCEPT + IMPLEMENT GO**. No cloud agent, no PR, no live Kalshi HTTP, no orders, no `admit.py` until then. No ACCEPT or ping file is written by this packet.
**Parent packet:** `Q6S5-KXMLBSPREAD-FEEQUEUE-HARNESS` (series KXMLBSPREAD only)
**Freeze ID / experiment id:** `Q6S5-KXMLBSPREAD-GAME-PHASE-SETTLED-TAPE`
**Feature family:** **`settled_tape_game_phase`**. It is orthogonal to the three knobs already tested on the Q6S5 panel: `analysis_slice` (PR58), `fill_model` (PR60) and `price_band` (PR61). It is not F1/F2/F3, not S1 KXMLBGAME ML, not Q6-000, not Cap-SR, and not Q6S1.
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`, main `d7558fc4b92256c68eaea66b9700021206de0a2d` (PR61 squash, per Conductor MERGE `469de237…`). I checked it read-only with a clone. PR61 lab `results/` holds only `ADMITTED_AT_ARM_COUNTS.json` (counts), `EMPTY_RESULTS.json` and `UNIT_RESULTS.md`. No FL-band outcome value is published, so this freeze is not conditioned on any FL-band result.
**Proposed lab dir:** `kalshi_q6s5_kxmlbspread_game_phase_settled_tape_lab_20261001/`. It has **not** been created. It gets created at implement, after ACCEPT, as the **sole** Variants cloud. Both PR61 clouds (`bc-74da3094`, `bc-7ada1737`) are finished per MERGE PR61.

## Selection: why this probe (Variants leftover survey, 2026-10-01)

Step 1: I found no same-day Conductor ACCEPT/KICK/QUEUE that names an unfiled Variants freeze. The 2026-10-01 packets are the FL-band ACCEPT `8e4fbac7…`, the MAXIMIZE pin 1848ET `a3f2d636…`/`59e4bbea…`, the IN_SAMPLE_DEV ruling `09763030…` and MERGE PR61 `469de237…`. All of them are filed or are not addressed to Variants.

Step 2: leftover list (done waves excluded):

| # | Candidate | Status | Blocked by / data | Evidence |
|---|---|---|---|---|
| **1 (PICK)** | **Q6S5 game-phase settled-tape** (`game_phase`: pregame vs in-play) | **FREEZABLE NOW** | Nothing new. It uses the same 11,723 sha-pinned prints and 6 finalized market GETs as FL-band. Scheduled first pitch comes from pinned `rules_primary`, cross-checked with `event_ticker`. All data sits outside the ADMIT-1 window and none of it is held. | SOURCE_PINS (90 FL-band pins re-hashed 2026-10-01, 0 mismatches); feasibility counts below |
| 2 | Q6S5 strategy-fill follow-on knob (`quote_offset` / `cancel_horizon`) | BLOCKED | Needs an Examiner score of PR60 (still READY_NOT_SCORED `85cdd05c…`). The 6 Sep-25 settlements are permanently out of scope (close_time 2026-09-28T22:40/45Z is inside the window). The 21 active-market prints leave placements starved. | MERGE PR60 `3486a2fe…`; ACCEPT `c6f95b32…` absent_pins |
| 3 | ETH-RJ `KXETH15M` settled-resolution join | BLOCKED | Sequenced behind ATP-RJ measured `settled_join_n` (MERGE PR54 `d02674a0…`). ATP post-ACCEPT settlements are `[]` (ACK `b9824df1…`), and no newer ATP settlement is on disk (`astra-capture/atp-kxatpmatch/` is unchanged since 2026-09-24). Owner: Collector/Variants ATP measure-mode run. | MERGE PR54; ACK ATP-RJ; ETH freeze `9cae3bad…` |
| 4 | KXMLBSPREAD untouched holdout (p16 item 12) | APPROVED, QUEUED | Queued behind weather, card03 and the Q6S5 settlement fetch. Needs new post-freeze Collector capture, and none is on disk. | user/Conductor queue; FL-band absent_pins |
| 5 | PM-008 / weather Phase B / card03 | HELD | ADMIT-1 429 storm (gate: 30 min with zero new 429s) | MAXIMIZE 1848ET; RULING `ac7cfe63…`; ERRATUM `31da5974…` |
| 6 | R3-P2 v2 queue-position | BLOCKED | Needs a new Mechanic demo series | EXAMINER_SCORE `e66d2636…` |
| 7 | Q6S3 KXNFLANYTD / Q6S4 KXBUNDESLIGAGAME / Q6S2 KXNHLGAME | DEFER / HOLD / reinforce-only | 429; thin OI; C2 reinforce only. No tape on disk. | sports screen ACCEPT `2aefbc17…` |
| 8 | S2 / R2-P4 KXNFLSPREAD(+TOTAL) | GATED | "TRY after C1 PIT@CLE". C1 PIT@CLE is NOT_SCORED (ADMIT-1 gap). No tape on disk. | EXAMINER_NOTE `fe5ba611…`; SCOUT_TRIAGE |
| 9 | Card 06 company-KPI / card 10 sub-variants / card 01 house | NOT A VARIANTS KNOB NOW | Census found no OPEN-WINDOW family (MIXED = NO_BUILD). Card 10 sub-variants are backlog with no data. Card 01 is prospective (other seat). | SCOUT_CARD06_COMPANY_KPI; CEM-…-002 |

**Why #1 over doing nothing:** the question it answers is decision-relevant and still open. Does the passive counterparty's realized return differ between pregame prints and in-play prints? In-play takers can trade on live game state faster than resting quotes update, which is the classic adverse-selection channel for a sports maker. The answer tells the queued untouched holdout which maker restriction to test, before any holdout data exists. On readiness, the data is identical to the ACCEPTED FL-band packet (`8e4fbac7…`), so it needs no new GET, no Collector time and no 429 budget. **Information value is moderate, not high:** this is the 4th knob on the same 3 events, so the verdict ceiling stays ITERATE. Read the multiplicity caveat below.

## Authority and context pins (re-hashed on box 2026-10-01)

| Item | Path | sha256 | Verify |
|---|---|---|---|
| Conductor MERGE PR61 (latest main d7558fc4) | `packets/CONDUCTOR_MERGE_Q6S5_KXMLBSPREAD_FL_BAND_SETTLED_TAPE_PR61_2026-10-01.json` | `469de2376ae413f66684df26c08656e705a7fb5a0a1d128a4270d789c841df32` | MATCH |
| Latest MAXIMIZE pin | `packets/MAXIMIZE_PIN_2026-10-01_1848ET.md` / `.json` | `a3f2d63698727458d6b59522ec52239534e399666cc9ccbc2376cdd124b86b15` / `59e4bbeaa9ba1e13df49633794d3b5b43deb0dd16342a6e40688acdd6f6af323` | pinned |
| Conductor ACCEPT FL-band (sibling) | `packets/CONDUCTOR_ACCEPT_VARIANTS_Q6S5_FL_BAND_SETTLED_TAPE_FREEZE_2026-10-01.json` | `8e4fbac7d0426bc67c1f53fb8057a382fe46da738bd701cb970a9812a6dc2a3b` | MATCH |
| Conductor RULING IN_SAMPLE_DEV (precedent) | `packets/CONDUCTOR_RULING_Q6S5_FL_BAND_IN_SAMPLE_DEV_LABEL_2026-10-01.json` | `09763030c67df066f2b59346200813e181777670cd46fcee6b8877a6dd74d754` | MATCH |
| Sibling freeze (house format) + its packet | `packets/Q6S5_KXMLBSPREAD_FL_BAND_SETTLED_TAPE_FREEZE_2026-09-29.md` / `.../FROZEN_EXPERIMENT.json` / `.../SOURCE_PINS.json` | `fb6540f52ed5f819ccf6e80bf0cf7eb6d951e065416b9d550fead0c6d06043fa` / `66819a4144ab0ed16fa73295357aebe5c200dee7d7ca393296d80965313f86f4` / `ab8ab6a7570da5099dffe001b92c07cc68bbf9efba2729407763a84d5485da0b` | MATCH |
| Conductor MERGE PR60 / Examiner READY_NOT_SCORED PR60 | `packets/CONDUCTOR_MERGE_Q6S5_KXMLBSPREAD_STRATEGY_FILL_PR60_2026-09-29.json` / `packets/EXAMINER_READY_NOT_SCORED_Q6S5_KXMLBSPREAD_STRATEGY_FILL_PR60_2026-09-25.json` | `3486a2fe71da0be40a3cb6202abcc30e1783515180e20f594b3c25b034414bef` / `85cdd05c3333da3eb373212d1bb4647729f6586185d518288df417e8de963698` | MATCH |
| Parent harness freeze / ACCEPT | `packets/Q6S5_KXMLBSPREAD_FEEQUEUE_HARNESS_FREEZE_2026-09-25.md` / `packets/CONDUCTOR_ACCEPT_Q6S5_KXMLBSPREAD_FEEQUEUE_HARNESS_2026-09-25.json` | `4f65dcdf536755b9f7dc2449c2dcd90b2df74cdf99a441b676f1a71c4d709c6e` / `5adc42f9c9533238a2187aafe7593bdf1b8cdec6d12b8d3e9b12cb5ab29000fc` | MATCH |
| Examiner trades-join SCORE ITERATE-3 / scorecard | `packets/EXAMINER_SCORE_Q6S5_KXMLBSPREAD_TRADES_JOIN_2026-09-25.json` / `packets/EXAMINER_SCORECARD_Q6S5_KXMLBSPREAD_TRADES_JOIN_2026-09-25.md` | `a18f2ad2f704d10ec526ccd2808edf8088f88de307ff8b3fe9845fa14ddde05a` / `e3eeb1a07fddc08824a02a78a68b7f4aba69d77d8cbe5edb0b970bc61c69a9d1` | MATCH |
| FEE_PIN (live /series body) | `packets/EXAMINER_FEE_PIN_Q6S5_KXMLBSPREAD_LIVE_SERIES_2026-09-25.json` | `9c0f3554eedc582ed4bed940575bf7ee6c0540ce5134140c5ea19e7c458d2b6a` | MATCH |
| Clock ADMIT / panel admitted | `packets/CLOCK_ADMIT_Q6S5_KXMLBSPREAD_2026-09-25.md` / `lab/astra-capture/q6s5-kxmlbspread/panel_admitted.json` | `f73bbaf3faaaa73186a233bfc21699d8ee3c47779253902ccc86159b3cbd7422` / `e36de2d1ce6286dff90d25f2fae680170c8a469c443c1beed974ffe80383fba1` | MATCH |
| R3-P3 10¢ band registry (stratifier only; never rebinned) | `packets/r3_p3_fl_maker_taker/bands_registry_10c.json` | `0860cbe28d28ecc6142ddf6f1ebb67792084264ed82e0b4d868c3b3138ea5312` | MATCH |
| R3-P3 Adversary refuse-bind | `packets/R3-P3_ADVERSARY_REFUSE_BIND_2026-09-22.md` | `6b6690cd6bf3b7e4833919a8f16be497027902ca726d22a64ef4bde2b29d5636` | binds carried |
| Sibling-desk review (dead-card overlap) | `packets/SIBLING_DEATHMATCH_REVIEW_2026-09-22.md` | `7cf177c13db42cd940d3a4effd3b78583493526a2b21e9b7e2d5f3086a5d790e` | pinned |
| v1.2 scorecard template json / md | `templates/EXAMINER_KALSHI_SCORECARD_TEMPLATE_v1.2.json` / `.md` | `56bcf6269a42031d9d90496e9a65c2292321aed2165033f6fb44ff8cc4d6b1cc` / `ad1dd2834652b8e9be331ddf2f3ec900ea587efb042251fde6452532b2e36394` | MATCH |
| p16 source PDF | `research/KALSHI_EDGE_RESEARCH_2026-09-24.pdf` | `7e55bc260526aa5088ee31f74475851219ab2cd7f19fdd2f0dd5e9f998c8b45e` | pinned |
| RULE-FROZEN-EDIT-PREV-BYTES-001 | `registry/RULE_FROZEN_EDIT_PREV_BYTES_2026-09-24.md` | `f0aab7d15ca78a097644008db02013eae3a56cb81b2a6aef2cfe6faf21e3e6d1` | pinned |
| Ranking evidence | MERGE PR54 / ACK ATP-RJ / ETH freeze / ETH MERGE PR36 / sports screen ACCEPT / R3-P2 SCORE / C1 note | `d02674a0…` / `b9824df1…` / `9cae3bad…` / `e94ca449…` / `2aefbc17…` / `e66d2636…` / `fe5ba611…` | pinned |

Feebook `22371178cb2663250b4762f328069571c48cb551` FIXED · rails `6a28e0d6254327ea4e6451c781bec56215ac6cac` FIXED (rails are not used by this packet).

## ADMIT-1 capture gap

| Item | Path | sha256 | Status |
|---|---|---|---|
| Conductor RULING | `packets/CONDUCTOR_RULING_ADMIT1_OUTAGE_GAP_WEATHER_CARD03_RELAUNCH_2026-09-29.json` | `ac7cfe63623ca342ab5b4285ff58382a8138b58fb6cd8e95310a5d30d90304f2` | PINNED |
| Conductor ERRATUM (card03 window) | `packets/CONDUCTOR_ERRATUM_CARD03_GAP_WINDOW_2026-09-29.json` | `31da5974867ee6230928b641e4a939171bce44260a4b87ee9161ffc8f30477d9` | PINNED (card03 only) |
| Collector gap record | `lab/astra-capture/prospective/ADMIT1_OUTAGE_GAP_2026-09-27_to_2026-09-29.json` | `4f2a5e2693f809e592238c0bf58ecac93f982fb8809c98ca81e51a41d8a65198` | PINNED |

**Exclusion rule (strict, fail-closed; identical to the FL-band sibling):**
1. **Enforced exclusion window:** `[2026-09-27T00:00:00Z, 2026-09-30T04:00:00Z)`. Any trade `created_time`, market GET `captured_utc` (filename stamp), `close_time`, or `settlement_ts` inside the window is excluded. The ruling's exact gap `2026-09-27T13:31:52Z → 2026-09-29T20:39:41Z` is recorded as `ruling_gap_utc` for reference only. **No backfill, no interpolation, ever.**
2. **Closed input manifest:** the runner reads only the sha-pinned `inputs_core` and `inputs_raw` in `SOURCE_PINS.json` and checks each sha256 before reading. Any mismatch is a hard fail.
3. **Per-row filter:** excluded rows are counted in `excluded_admit1_window_n` (by source: trades / markets / settlement). None are imputed.
4. **ADMIT-1 `lab/astra-capture/prospective/capture.sqlite` is REFUSED as input** and is never opened.
5. **Pre-run assertion:** in-scope trades span `2026-09-23T22:06:01Z..2026-09-25T05:07:00Z`. The settlement GETs were captured `20260925T051602Z..051942Z`, with `settlement_ts` `2026-09-25T04:32:18Z..05:08:48Z`. So expected `excluded_admit1_window_n = 0`, and any non-zero count must be reported.
6. **The 6 Sep-25 panel markets are permanently out of scope** (status active in their pinned GETs, no result, close_time in the window). No re-GET.
7. **Required unit test:** a synthetic trade inside the window and a synthetic settlement inside the window must both be rejected.

## Intent (one knob)

Keep everything fixed: the panel (`e36de2d1…`), the pinned public trade tape, the pinned settlement GETs, the row rules of the FL-band sibling, and the fee pin. Vary **only** `game_phase`, which says whether the public print happened before or after the game's scheduled first pitch. For each phase, measure the realized settlement return of the **passive (maker) counterparty** of real public prints.

**Not a strategy.** No Astra orders, fills or PnL. Observations are labeled `public_counterparty_realized`, never `pnl`. Astra `results` / `pnl` / v1.2 `net_pnl_*` stay null.

**One knob only:** `game_phase` ∈ {`Q6S5GP0`, `Q6S5GP1`}.

| Arm | Label | Rule on the print's own `created_time` | Meaning |
|---|---|---|---|
| **Q6S5GP0** | `pregame` | `created_time < scheduled_start_utc` | the print happened before scheduled first pitch |
| **Q6S5GP1** | `inplay` | `scheduled_start_utc ≤ created_time < close_time` | the print happened at or after scheduled first pitch and before market close |

**`scheduled_start_utc` (declared, pre-outcome, static contract text):** parse the pinned measured market GET `rules_primary` with the regex `originally scheduled for (Mon) (D), (YYYY) at (H):(MM) (AM|PM) EDT`, convert EDT (UTC−4) to UTC, and require equality with the `event_ticker` time code `YYMONDDHHMM` read as ET. A mismatch or a missing pattern is a **hard fail** (no fallback, no guess). Declared values: `KXMLBSPREAD-26SEP242140HOUATH` → `2026-09-25T01:40:00Z`, `KXMLBSPREAD-26SEP242140LAASEA` → `2026-09-25T01:40:00Z`, `KXMLBSPREAD-26SEP242210SDLAD` → `2026-09-25T02:10:00Z`. These are parsed static fields, not results. `occurrence_datetime` / `expected_expiration_time` (`04:40Z`) are **not** used: they mark expected game end, which is the +3h mismatch the Scout pinned. `close_time` is used only as the post-close exclusion boundary (same as FL-band) and never to assign a phase before the game ends.

**Proxy caveat (declared):** the scheduled start is a proxy for the actual first pitch. A delay would put a few true-pregame prints into GP1, which mixes the arms and pulls the delta toward 0 (conservative). Getting the actual first pitch would need a new external or live GET, which is refused here. The `start_shift_plus_30m` stress (below) bounds this.

## Feasibility counts (pre-exclusion row counts; NOT results)

These were counted from `created_time` vs `scheduled_start_utc` / `close_time` only, after the design lock and before any outcome read:

| Market | GP0 rows | GP1 rows | post-close rows |
|---|---|---|---|
| HOUATH-ATH2 | 22 | 475 | 0 |
| HOUATH-HOU2 | 498 | 2,057 | 2 |
| LAASEA-LAA2 | 50 | 1,054 | 1 |
| LAASEA-SEA2 | 386 | 785 | 2 |
| SDLAD-LAD2 | 836 | 3,308 | 0 |
| SDLAD-SD2 | 73 | 2,173 | 1 |
| **Total** | **1,865** | **9,852** | **6** (sum 11,723 = Collector total) |

Both arms are non-empty in all 6 markets and all 3 events. Native-side, block, price-consistency and window exclusions are applied at implement and counted there.

## Row construction (declared pre-outcome; FL-band sibling rules verbatim except the knob)

- **Universe:** the 6 panel_admitted KXMLBSPREAD markets whose latest pinned measured market GET shows `status == "finalized"` with non-empty `result`: `KXMLBSPREAD-26SEP242140HOUATH-{ATH2,HOU2}`, `KXMLBSPREAD-26SEP242140LAASEA-{LAA2,SEA2}`, `KXMLBSPREAD-26SEP242210SDLAD-{LAD2,SD2}`. That is 3 events, all "wins by over 1.5 runs".
- **Rows:** every public trade in the pinned raw pages for those 6 tickers (Collector total 11,723; this is a pin, not a result).
- **Native side only:** `s = taker_outcome_side`. A row is used only if `taker_side == taker_outcome_side` and (`s=yes` ⇔ `taker_book_side=bid`; `s=no` ⇔ `taker_book_side=ask`). Any other combination is excluded and counted. **Lee-Ready REFUSED.**
- **Taker price:** `p_taker = yes_price_dollars` if `s=yes`, else `no_price_dollars`. A row is excluded if `|yes+no−1| > 1e-9`.
- **Exclusions (counted, never imputed):** `is_block_trade`; `created_time ≥ close_time` (post-close); ADMIT-1 window; any market with `result ∉ {yes,no}` (whole market).
- **Weight:** `q = count_fp`. **Settlement:** `Y_s = 1` if `result == s`, else 0. `settlement_ts` is read as-is.
- **Information set:** the phase uses only the print's own `created_time` and static contract text. Settlement is used only as the ex-post label. No row selection depends on outcome or on later prints.
- **Clock flags (per Conductor ruling `09763030…` precedent):** every row carries the boolean `pre_admitted_at = created_time < 2026-09-25T04:37:47Z` (strict). Every row, the summary and the scorecard carry `evidence_class = "IN_SAMPLE_DEV"`. Pre/post admitted_at counts are reported per arm (counts only).

## Metrics (all null now)

Per arm `A` (same formulas as the FL-band sibling):
- `maker_gross_return_usd[A] = Σ q · (p_taker − Y_s)`; `maker_capital_usd[A] = Σ q · (1 − p_taker)`; `maker_gross_roi[A] = return / capital`
- `taker_gross_roi[A] = Σ q · (Y_s − p_taker) / Σ q · p_taker`
- `n_trades[A]`, `contracts[A]`, `n_markets[A]`, `n_events[A]`, `pre_admitted_at_n[A]`, `post_admitted_at_n[A]`

**Primary (H1):** `maker_gross_roi_delta_GP1_minus_GP0 = maker_gross_roi[GP1] − maker_gross_roi[GP0]` (gross, fee-free).
**Secondary (price-band confound control, price_band held FIXED, not varied):** `maker_gross_roi_delta_GP1_minus_GP0_within_FL1` uses only rows with `p_taker ∈ [0.20, 0.80)` (registry bands b02–b07 of `0860cbe2…`, applied verbatim, no rebin). In-play prices drift toward 0/1, so a raw GP1−GP0 gap could just be the FL-band effect showing up again. This stratum holds price fixed. **No FL0/FL1/FL2 delta is computed in this packet**, because price_band is not re-measured.
**Descriptive:** per-market and per-event GP0/GP1 tables.
**Fee-labeled secondary (CACHE_NOT_R1P1):** `maker_net_roi_cache[A]` / `taker_net_roi_cache[A]` via `feebook.order_fee(role, q, price)` @ `22371178…` with FEE_PIN terms only (`quadratic`, `0.5`). The maker role resolves via `feebook.resolve_terms`, and this freeze does not assert the value.

**Robustness (pre-registered):** leave-one-event-out (3 values) and leave-one-market-out (6 values) of the primary and the secondary.
**Stresses (pre-registered; never selected as an arm):** `one_tick_worse` (maker charged $0.01/contract: capital +0.01, return −0.01); `start_shift_plus_30m` (recompute the primary with `scheduled_start_utc + 30 min` as the boundary; one value only, for delay robustness); `fees_2x` on the CACHE secondary.
**Not in scope:** Mincer–Zarnowitz; event-clustered inference (3 clusters); `executable_dollars_per_day` (not our executions); intra-game state (score/inning), which is not on disk and would need an external feed.

## Hypothesis and reading rule (written before outcomes)

- **H1 (in-play adverse selection on passive counterparties):** `maker_gross_roi_delta_GP1_minus_GP0 < 0`. Resting liquidity hit during the game earns less per dollar at risk than resting liquidity hit pregame, because in-play takers act on live game state.
- **Variants-proposed reading (Examiner owns the verdict):** `supports_H1` if the full-sample primary < 0 **and** ≥2 of 3 LOEO primaries < 0. `contradicts_H1` if the full-sample primary ≥ 0 **and** ≥2 of 3 LOEO primaries ≥ 0. Otherwise `inconclusive`. **Confound cap:** if the within-FL1 secondary has the opposite sign to the primary, the reading is capped at `inconclusive_price_confounded`.
- **Verdict ceiling ITERATE:** measurement only. No KEEP, `counts_toward_keep=false`, `promote=false`, evidence_class `IN_SAMPLE_DEV`.
- **Power / multiplicity caveat (declared):** **effective n = 3 events** (6 same-game-sibling markets), not 11,723 prints. Each market feeds both arms, so the GP1−GP0 contrast is within-market, but realized return still rests on 3 game outcomes. This is the **4th** pre-registered knob on these same 3 events (analysis_slice, fill_model, price_band, game_phase). Any single "supports" reading has inflated family-wise false-positive odds and is hypothesis-generating only. The confirmatory test belongs on the approved untouched KXMLBSPREAD holdout.
- **Money path:** if `supports_H1`, the next one-knob freeze would put a `pregame_only` restriction on the Q6S5 maker leg, evaluated **only** on the untouched holdout (p16 item 12), never on this tape. Named prior: the sibling desk lists "MLB pregame MM" as dead (`SIBLING_DEATHMATCH_REVIEW` `7cf177c1…`, Claude STRATEGY_BOARD). So `supports_H1` would also point toward a KILL of the KXMLBSPREAD maker leg, not a build, and the Conductor decides. If `contradicts_H1`, in-play passive liquidity is not worse here, which differs from the sibling's pregame-only framing. No retune of Q6-000 either way.

## Fee

FEE_PIN `9c0f3554…` observed `fee_type=quadratic`, `fee_multiplier=0.5`, `feebook_formula_id` = null → **CACHE-LABELED / `CACHE_NOT_R1P1`**, `fee_honest=false`, `claim_as_live_R1P1=false`. **Not R1-P1.** The primary metric is fee-free.

## Dead-card / live-pin overlap (named)

| Card / pin | Handling |
|---|---|
| **Invent fills / PnL** | **REFUSED.** Real public prints with observed settlement only. |
| Q6S5 `price_band` (PR61) | **Sibling, not repeated.** It is used only as a fixed stratifier (FL1 stratum) for confound control. No FL deltas, no rebin. |
| Q6S5 `analysis_slice` (PR58) incl. `content_fresh_vs_stale_bin` | Nearest overlap. Freshness is a rails book-snapshot content flag, while game_phase is the print's time relative to scheduled first pitch. Different object; not retuned. |
| Q6S5 `fill_model` (PR60) | Sibling; not retuned, not re-run. |
| Sibling desk "MLB pregame MM" (STRATEGY_BOARD dead) | Named prior (see money path). This packet is measurement, not an MM build. |
| R3-P3 FL Adversary bind | Carried (paper EV hypothesis-only; no Lee-Ready; no fee-honest without R1-P1). |
| **S1 KXMLBGAME ML retune** | **FORBIDDEN** |
| **Q6-000 retune** | **FORBIDDEN.** Scoreboard Q6-000 / Arm D KEEP +$345.24 / +6.90%, unchanged. |
| Cap-SR / Q6S1 / Refiner | **FORBIDDEN / NONE** |
| Lee-Ready | **REFUSED** |

## Scorecard fields (null now)

`results`, `pnl`, `maker_gross_roi` / `taker_gross_roi` per arm, primary and secondary deltas, LOEO/LOMO vectors, stresses, `maker_net_roi_cache`, `taker_net_roi_cache`, `n_trades`, `contracts`, `n_markets`, `n_events`, `pre_admitted_at_n`, `post_admitted_at_n`, `excluded_*_n`, `reading` all stay **null** until an Examiner-scored run.

**Examiner scorecard v1.2 stub** (template `56bcf626…`) is in `EXAMINER_SCORECARD_STUB_*.json/.md`. All values are null (`measured=false`). Declared: `simulated_fills` n/a (`counts_toward_keep=false`); controls `market_only` applies (price is the implied probability), `no_trade` / `simple_model` n/a; calibration `emits_probabilities=false`; no rewards thesis; `study_label` null, Variants proposes "historical replay"; `evidence_class` `IN_SAMPLE_DEV`.

## p16 preregistration checklist

Source: v1.2 `preregistration_checklist` (PDF p16). Declared pre-outcome at `2026-10-01T19:20:29-04:00`. Examiner `gate_status` null.

| # | Item | Status | Evidence |
|---|---|---|---|
| 1 | market_universe | **satisfied** | 6 finalized panel_admitted markets (3 events) of `e36de2d1…`; KXMLBSPREAD only |
| 2 | exclusions | **satisfied** | 6 Sep-25 markets; post-close prints; block trades; native-field conflicts; price-inconsistent rows; ADMIT-1 window; `capture.sqlite` refused; rules_primary/ticker start mismatch = hard fail |
| 3 | receipt_time_information_set | **satisfied** | phase from the print's own `created_time` vs static scheduled start; settlement only as ex-post label; sha-pinned closed manifest |
| 4 | fee_regime | **satisfied** | primary gross; secondary feebook@22371178 FEE_PIN quadratic×0.5 CACHE_NOT_R1P1; fees_2x |
| 5 | order_timing | **n/a** | no Astra orders |
| 6 | sizing | **n/a** | rows weighted by published `count_fp` |
| 7 | fill_model | **n/a** | no Astra fills |
| 8 | stopping_rules | **satisfied** | freeze-before-implement; ACCEPT before cloud; sole Variants cloud; single pass over closed manifest; no rerun with an altered boundary |
| 9 | evaluation_metrics | **satisfied** | primary/secondary deltas; LOEO/LOMO; stresses; v1.2 nulls |
| 10 | limit_candidate_variants | **satisfied** | one knob `game_phase` × 2 values; boundary fixed at scheduled first pitch; +30m is a stress, not an arm |
| 11 | log_every_attempted_variant | **satisfied** | only 2 arms + FL1-stratum secondary + per-market/event descriptive; any other cut needs a new freeze |
| 12 | separate_discovery_tuning_evaluation_periods | **missing** | no untouched evaluation set; same tape as ITERATE-3 counts, PR60 and PR61 (all unscored for outcome); no tuned parameter; holdout = approved KXMLBSPREAD untouched holdout (queued) |

Counts: satisfied 8, n/a 3, missing 1.

## Integrity (Clock gate)

- Pinned bytes are committed **verbatim** and checked with `sha256sum`. No labeled recreations. The authentic pin bundle is in `/workspace` (see digest).
- Clock: panel admitted at `2026-09-25T04:37:47Z`. Most prints predate admission, so this is a retrospective public tape → `IN_SAMPLE_DEV` / "historical replay", never "prospective" (precedent ruling `09763030…`).
- `digest_all_match_claimed=true` for every pin cited. `measured/DIGESTS.txt` lists a drifted `STATUS.json` hash (already recorded); `STATUS.json` is not an input.
- Absent (declared, not recreated): Examiner-pinned KXMLBSPREAD `formula_id`; untouched evaluation set; Sep-25 settlements (out of scope); actual first-pitch times (no external GET); Archivist fee/account-version manifest; ADMIT-1 capture in the ruling gap.
- RULE-FROZEN-EDIT-PREV-BYTES-001: this freeze **creates only new files**. No frozen file was edited, so there was no `_prev` write.

## Merge gates

Units green at implement, including: ADMIT-1 window rejection (trade and settlement); post-close exclusion; Lee-Ready refusal / native-field conflict exclusion; closed-manifest sha fail-closed; **phase boundary test** (a print at exactly `scheduled_start_utc` is GP1; one at −1 µs is GP0); **rules_primary ↔ event_ticker mismatch hard-fails**; missing-pattern hard-fails; `pre_admitted_at` strict-< boundary test; `evidence_class=IN_SAMPLE_DEV` present on rows, summary and card; FL1 stratum uses registry inclusivity verbatim; no-invent (a market without a result produces no row). `results` / all metrics stay null until Examiner. Examiner HOLD_PRE_PR → READY NOT_SCORED only after PR branch sha verify + merge. **HOLD for Conductor ACCEPT: no CloudAgent, no PR, no `admit.py`, no live Kalshi HTTP, no orders.**

## Refuse binds

invent fills/PnL/settlement_ts/first-pitch times/markets/depth · label public-counterparty return as Astra PnL · Lee-Ready · live orders · Variants demo orders · dual-cloud · claim CACHE as R1-P1 or "fee-honest" · paper EV as Astra evidence · rebin R3-P3 registry · re-measure price_band / fill_model / analysis_slice · move the phase boundary after outcomes · S1 KXMLBGAME ML retune · Q6-000 retune · Cap-SR reopen · Refiner routing · Q6S1 retune · `admit.py` · reading ADMIT-1 `capture.sqlite` · any data in the ADMIT-1 window · backfill/interpolate · external/live GET for first-pitch times · lookahead in row selection · editing prior SCORE/ACCEPT/FEE_PIN/HOLD/READY bytes · KEEP from this measurement
