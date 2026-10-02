# VARIANTS HOLDOUT PRE-REGISTRATION ADDENDUM — Q6S5 KXMLBSPREAD UNTOUCHED CAPTURE (FL1 mid-band maker / FL2 avoidance)

**Status:** `DRAFT_PENDING_CONDUCTOR_ACCEPT`. Design only. No capture exists yet, no row has been read, and no number below is a result.
**Filed by:** R&D Variants ("KALSHI"), Astra/Kalshi desk. **Drafted at:** `2026-10-01T19:37-04:00` (ET).
**Addendum ID (proposed):** `Q6S5-KXMLBSPREAD-HOLDOUT-PREREG-v0`. **Parent packet:** `Q6S5-KXMLBSPREAD-FEEQUEUE-HARNESS`. **Series:** KXMLBSPREAD only.
**Addressed to:** Conductor (ACCEPT owner). cc Examiner (owns the read and the verdict), Collector (owns the capture), Clock (owns `holdout_admitted_at`), Archivist.
**Scope:** This is the confirmatory pre-registration that the KILL accept `be235777…` routes to the queued untouched holdout: "pre-register FL1-mid maker and H2 extreme-band avoidance there". It does not start, schedule, reorder or shape the Collector capture. It is not a 5th knob on the 3 Sep-24 games (UNIVERSE CAP respected). It does not touch the in-flight game-phase implement.
**Tags:** `[H]` = Variants proposal or judgment the Conductor may change **before** ACCEPT. Untagged = copied from pinned files.

---

## 1. Pins (sha256 re-hashed on box 2026-10-01 ~19:35 ET; all MATCH)

| Item | Path (under `lab/governance/astra/`) | sha256 |
|---|---|---|
| Conductor ACCEPT of Examiner KILL (FL-band, PR61) | `packets/CONDUCTOR_ACCEPT_EXAMINER_KILL_Q6S5_KXMLBSPREAD_FL_BAND_PR61_2026-10-01.json` | `be2357773ca7a842e6896676e3ba0291f40ef8e0b8f997d46f7124d4b2705229` |
| Examiner SCORE (FL-band, PR61) | `packets/EXAMINER_SCORE_Q6S5_KXMLBSPREAD_FL_BAND_SETTLED_TAPE_PR61_2026-10-01.json` | `2e74f17b1307b8b57f33a6475cd7ce8af48c470099478cadfb07877b0d70745f` |
| Examiner SCORECARD (FL-band, PR61) | `packets/EXAMINER_SCORECARD_Q6S5_KXMLBSPREAD_FL_BAND_SETTLED_TAPE_PR61_2026-10-01.md` | `1bdb1d9c1e6272a4b95a5080e4681858859e69a053f69e32b9b85b7d9e44c386` |
| FL-band FREEZE (band bytes source) | `packets/Q6S5_KXMLBSPREAD_FL_BAND_SETTLED_TAPE_FREEZE_2026-09-29.md` | `fb6540f52ed5f819ccf6e80bf0cf7eb6d951e065416b9d550fead0c6d06043fa` |
| FL-band FROZEN_EXPERIMENT (in-sample events + Sep-25 exclusion list) | `packets/Q6S5_KXMLBSPREAD_FL_BAND_SETTLED_TAPE/FROZEN_EXPERIMENT.json` | `66819a4144ab0ed16fa73295357aebe5c200dee7d7ca393296d80965313f86f4` |
| Conductor ACCEPT FL-band freeze | `packets/CONDUCTOR_ACCEPT_VARIANTS_Q6S5_FL_BAND_SETTLED_TAPE_FREEZE_2026-10-01.json` | `8e4fbac7d0426bc67c1f53fb8057a382fe46da738bd701cb970a9812a6dc2a3b` |
| Conductor RULING IN_SAMPLE_DEV label | `packets/CONDUCTOR_RULING_Q6S5_FL_BAND_IN_SAMPLE_DEV_LABEL_2026-10-01.json` | `09763030c67df066f2b59346200813e181777670cd46fcee6b8877a6dd74d754` |
| Game-phase FREEZE (not scored; not touched) | `packets/Q6S5_KXMLBSPREAD_GAME_PHASE_SETTLED_TAPE_FREEZE_2026-10-01.md` | `5beba803f3f6d33410409acc23ad3b782be62dc8829a0f54584e1da8ac18575a` |
| Conductor ACCEPT game-phase freeze | `packets/CONDUCTOR_ACCEPT_VARIANTS_Q6S5_GAME_PHASE_SETTLED_TAPE_FREEZE_2026-10-01.json` | `08d23b363d72b8c8599772ee6fc6736cb90f13e8ed814b12c59b58fd5c7dc91e` |
| R3-P3 10¢ band registry (verbatim; never rebinned) | `packets/r3_p3_fl_maker_taker/bands_registry_10c.json` | `0860cbe28d28ecc6142ddf6f1ebb67792084264ed82e0b4d868c3b3138ea5312` |
| R3-P3 FL freeze kernel (registry parent) | `packets/R3-P3_FL_MAKER_TAKER_BANDS_FREEZE_KERNEL_2026-09-22.md` | `0ed697149136acb3aa840aeeb79d11c8f6ef80f37ce4dd692a3cb690212206a7` |
| ADMIT-1 gap RULING | `packets/CONDUCTOR_RULING_ADMIT1_OUTAGE_GAP_WEATHER_CARD03_RELAUNCH_2026-09-29.json` | `ac7cfe63623ca342ab5b4285ff58382a8138b58fb6cd8e95310a5d30d90304f2` |
| FEE_PIN KXMLBSPREAD (/series body) | `packets/EXAMINER_FEE_PIN_Q6S5_KXMLBSPREAD_LIVE_SERIES_2026-09-25.json` | `9c0f3554eedc582ed4bed940575bf7ee6c0540ce5134140c5ea19e7c458d2b6a` |
| Scorecard template v1.2 | `templates/EXAMINER_KALSHI_SCORECARD_TEMPLATE_v1.2.json` | `56bcf6269a42031d9d90496e9a65c2292321aed2165033f6fb44ff8cc4d6b1cc` |
| Study class labels (p16 vocabulary) | `registry/STUDY_CLASS_LABELS_2026-09-24.md` | `8f36bf10ff45dab31011d1e61dfb951fff1021ad7104aa6cef5f874d2f09e8c6` |
| RULE-FROZEN-EDIT-PREV-BYTES-001 | `registry/RULE_FROZEN_EDIT_PREV_BYTES_2026-09-24.md` | `f0aab7d15ca78a097644008db02013eae3a56cb81b2a6aef2cfe6faf21e3e6d1` |

Feebook `22371178cb2663250b4762f328069571c48cb551` FIXED. Main at drafting: `d7558fc4b92256c68eaea66b9700021206de0a2d` (PR61 squash, MERGE `469de237…`).

## 2. What the in-sample tape showed (copied from Examiner SCORE `2e74f17b…`; IN_SAMPLE_DEV, hypothesis-generating only)

Pre-cutoff (`pre_admitted_at`, strict `<` 2026-09-25T04:37:47Z; 10,680 rows), gross fee-free `pre.arms.<arm>.maker_gross_roi`:
FL0 `0.0396` (≈+0.040) · FL1 `0.1443` (+0.144) · FL2 `−0.2838` (−0.284).
`primary.pre_value` (FL0−FL1) `−0.1048` → `reading = contradicts_H1` → **KILL** (KXMLBSPREAD FL-band H1 only). `secondary.pre_value` (FL2−FL1) `−0.4282`.
Per-game FL1 maker gross ROI (`pre.per_game.*.arms.Q6S5FL1.maker_gross_roi`): HOUATH −0.081, LAASEA +0.371, SDLAD +0.218 (2 of 3 > 0). Per-game FL2−FL1 (`delta_FL2_minus_FL1`): HOUATH +1.42, LAASEA −0.84, SDLAD −1.14 (2 of 3 < 0).
`multiplicity.context`: smallest attainable one-sided sign-test p with 3 games = 0.125, above Bonferroni α/4 = 0.0125. `effective_n_games = 3`, `family_size = 4`.
These numbers chose H_a / H_b below. **They are not evidence for them.** Selecting a hypothesis from the in-sample tape is the reason it must be confirmed on rows nobody has seen.

## 3. Holdout definition

### 3.1 Ordering gate (pre-registration precedes capture) `[H]`
- The holdout is valid for confirmatory use **only if** the Conductor ACCEPT of this addendum (sha-stamped) is filed **before** the Clock stamps `holdout_admitted_at` for the Collector's new KXMLBSPREAD holdout panel.
- If the capture is admitted first, the holdout is reclassified `IN_SAMPLE_DEV`. It then counts toward nothing, and this addendum must be re-filed against a later admission.
- Any amendment after `holdout_admitted_at` that touches §3 to §6 voids confirmatory status, unless the amendment is filed before any outcome join and the Examiner certifies that no outcome was seen.

### 3.2 Source
- **Only** the queued, Conductor-approved, Collector-owned KXMLBSPREAD untouched capture. Collector owns the GET schedule, budget and timing. Variants requests nothing.
- Inputs: the holdout panel file + Clock ADMIT stamp, the Collector per-ticker trade pages, and the Collector settlement market GETs. All are sha-pinned in a closed manifest and read fail-closed on sha mismatch (same discipline as fb6540f5 §ADMIT-1 rule 2).
- **Refused as input:** ADMIT-1 `lab/astra-capture/prospective/capture.sqlite`; the in-sample bundle `63b5d981…`; every Sep-24/Sep-25 pinned GET; any backfill.

### 3.3 Eligible games (unit of analysis = game = event_ticker)
A KXMLBSPREAD event is eligible iff **all** of the following hold:
1. It is in the holdout panel admitted at `holdout_admitted_at`.
2. Its scheduled first pitch (`scheduled_start_utc`, parsed from pinned `rules_primary` with the regex in game-phase freeze 5beba803 and cross-checked against the `event_ticker` time code; a mismatch or missing pattern is a hard fail) is **strictly after** `holdout_admitted_at`. `[H]` This makes both pregame and in-play prints capturable, which the game-phase fold-in slot (§7) needs.
3. It is **not** one of the 3 in-sample games (all strikes/markets of each are excluded): `KXMLBSPREAD-26SEP242140HOUATH`, `KXMLBSPREAD-26SEP242140LAASEA`, `KXMLBSPREAD-26SEP242210SDLAD`. Their markets were `-{ATH2,HOU2}`, `-{LAA2,SEA2}`, `-{LAD2,SD2}` (fb6540f5 "Row construction"; FROZEN_EXPERIMENT `66819a41…` `events`).
4. It is **not** one of the 6 Sep-25 panel markets ruled permanently out of scope: `KXMLBSPREAD-26SEP251840PITDET-{DET2,PIT2}`, `KXMLBSPREAD-26SEP251840TBPHI-{PHI2,TB2}`, `KXMLBSPREAD-26SEP251845NYMWSH-{NYM2,WSH2}`. Wording: FL-band ACCEPT `8e4fbac7…` `implement_scope.universe` = "6 finalized panel_admitted markets / 3 events; 11,723 pinned prints; **6 Sep-25 markets out of scope**", and `absent_pins_acknowledged` = "Sep-25 settlements 6/12 out of scope for this freeze". Ruling `09763030…` `sep25_markets` = "permanently out of scope for FL-band; no re-GET under this experiment". Freeze fb6540f5 rule 6 = "permanently out of scope … No amendment path, no re-GET". `[H]` For hygiene the holdout also excludes **every** market of those 3 Sep-25 events (any strike), plus any event dated on or before `26SEP29`.
5. At least one primary-strike market (§3.4) of the event is `status == "finalized"` with `result ∈ {yes, no}` in a Collector settlement GET whose `captured_utc` is ≥ `holdout_admitted_at` and outside the ADMIT-1 window.

### 3.4 Eligible markets and rows
- **Primary strike `[H]`:** only the 1.5-run spread markets (ticker suffix `<TEAM>2`, rules "wins by over 1.5 runs"). This matches the in-sample universe, which was 1.5-run markets only. Other strikes (`<TEAM>3`, `<TEAM>4`, …), if the panel admits them, are a **pre-declared descriptive** table and never enter the decision.
- **Post-admitted_at only:** a row is eligible only if `created_time ≥ holdout_admitted_at`, i.e. `pre_admitted_at = false` under the strict-`<` rule of ruling 09763030. Rows with `pre_admitted_at = true` are counted and reported, **never** pooled, and never count toward any verdict.
- **ADMIT-1 window, permanent, no backfill:** `[2026-09-27T00:00:00Z, 2026-09-30T04:00:00Z)`. Any trade `created_time`, market GET `captured_utc`, `close_time` or `settlement_ts` inside it excludes the row/market (counted in `excluded_admit1_window_n`). No backfill, interpolation or re-admit (ruling `ac7cfe63…`).
- **Row rules (verbatim from fb6540f5, "Row construction"):** native side only (`s = taker_outcome_side`, usable only if `taker_side == taker_outcome_side` and `s=yes ⇔ taker_book_side=bid`, `s=no ⇔ taker_book_side=ask`). **Lee-Ready REFUSED.** `p_taker = yes_price_dollars` if `s=yes` else `no_price_dollars`. Exclude `|yes+no−1| > 1e-9`, `is_block_trade`, `created_time ≥ close_time`, and whole markets with `result ∉ {yes,no}`. Weight `q = count_fp`. `Y_s = 1` if `result == s` else 0. `settlement_ts` is read as-is and never invented.

### 3.5 Untouched discipline
- No seat joins `result` to any holdout row before the single Examiner read (§5.6).
- Before the read, Collector/Clock may publish **counts only**: eligible games, markets, and rows per arm and per `pre_admitted_at` flag, in the format of PR61 `ADMITTED_AT_ARM_COUNTS.json`. Prices may be used for band counts. Results may not.
- Variants does not look at holdout rows at any point before the Examiner SCORE.

### 3.6 Minimum sample (pre-registered; no read below it) `[H]`
- **`n_min = 30` eligible finalized games**, each with FL1 `maker_capital_usd > 0` in its primary-strike rows. Below 30 the status is `NOT_SCORED_INSUFFICIENT_N`: no outcome join, no partial look, no verdict.
- **Single read:** at the first Collector capture-close stamp where the eligible count is ≥ 30, Examiner reads **once** over the eligible games at that stamp. There are no interim looks and no optional stopping. Games finalized after that stamp are not added.
- **Justification (exact binomial; one-sided sign test at α = 0.05):**

| n games | reject if S ≥ | exact size | power π=0.60 | π=0.667 | π=0.70 | π=0.75 | π=0.80 |
|---|---|---|---|---|---|---|---|
| 20 | 15 | 0.021 | 0.13 | 0.30 | 0.42 | 0.62 | 0.80 |
| 24 | 17 | 0.032 | 0.19 | 0.43 | 0.56 | 0.77 | 0.91 |
| **30** | **20** | **0.049** | **0.29** | **0.59** | **0.73** | **0.89** | **0.97** |
| 40 | 26 | 0.040 | 0.32 | 0.66 | 0.81 | 0.95 | 0.99 |

  π = true probability that a game's FL1 maker gross ROI is > 0. The in-sample 2/3 is an optimistic, winner's-curse-inflated guide.
  - n = 30 is the smallest round value with about 0.7 power at π = 0.70 and about 0.9 at π = 0.75.
  - n = 20 would give a coin-flip-or-worse test at plausible π.
  - n = 30 also clears the Bonferroni-4 shadow (§6), since the smallest attainable p at n = 30 is 9e-10.
- **Feasibility caveat `[H]`, unverified, no schedule GET made:**
  - Capture cannot start before the queue clears (weather → card03 → Q6S5 settlement fetch).
  - The MLB regular season is believed to have ended around the ADMIT-1 window, so eligible 2026 games may be postseason only. That could be fewer than 30, and KXMLBSPREAD postseason listing is unverified.
  - If 30 is not reached, the holdout **stays sealed** and continues into the next season's games under this same addendum. There is no early read and no lowering of `n_min` after capture starts.

## 4. Hypotheses (bands identical to fb6540f5 bytes; registry 0860cbe2 verbatim)

| Arm | `p_taker` range | Registry bands | Maker holds |
|---|---|---|---|
| Q6S5FL0 | `[0.00, 0.20)` | b00, b01 | favorite side at `1−p_taker ∈ (0.80, 1.00]` |
| **Q6S5FL1** | **`[0.20, 0.80)`** | b02–b07 | opposite side at (0.20, 0.80] |
| **Q6S5FL2** | **`[0.80, 1.00]`** | b08, b09 (b09 hi-inclusive) | longshot side at `1−p_taker ∈ [0.00, 0.20]` |

- **H_a (primary):** FL1 mid-band passive (maker) counterparty gross ROI > 0: `maker_gross_roi[Q6S5FL1] > 0`.
- **H_b (secondary):** FL2 maker gross ROI is below FL1: `maker_gross_roi[Q6S5FL2] − maker_gross_roi[Q6S5FL1] < 0`.
- FL0 and FL0−FL1 are reported **descriptively only** (H1 is KILLED, accept `be235777…`, and is not re-tested here).

## 5. Metric, test, alpha, decision rule

### 5.1 Metric (exactly the Examiner's definition; field names from SCORE `2e74f17b…`)
- `maker_gross_return_usd[A] = Σ q·(p_taker − Y_s)`
- `maker_capital_usd[A] = Σ q·(1 − p_taker)`
- `maker_gross_roi[A] = maker_gross_return_usd[A] / maker_capital_usd[A]`. Gross, fee-free. This is the SCORE's `primary.definition`: "maker_gross_roi[A] = Σ q·(p_taker − Y_s) / Σ q·(1 − p_taker); gross, fee-free". It is the same as `method.independent_recompute.method` "maker ROI = Σq(p−Y)/Σq(1−p)".
- Reported in the SCORE's field layout: `arms.<arm>.{maker_gross_roi, maker_gross_return_usd, maker_capital_usd, maker_net_roi_cache, taker_gross_roi, taker_net_roi_cache, contracts, n_trades, n_markets, n_events, pnl:null, results:null}` and `per_game.<event>.arms.<arm>.maker_gross_roi`, plus `delta_FL2_minus_FL1` per game and pooled. `taker_gross_roi[A] = Σ q·(Y_s − p_taker) / Σ q·p_taker`.
- **Per-game statistic:** `r_g = per_game[g].arms.Q6S5FL1.maker_gross_roi` (pooled over game g's eligible primary-strike rows). `d_g = per_game[g].arms.Q6S5FL2.maker_gross_roi − r_g`.

### 5.2 Directional reading (mirrors the Examiner-applied fb6540f5 rule, with game in place of event)
- `supports_H_a`: pooled `arms.Q6S5FL1.maker_gross_roi > 0` **and** ≥ ⌈2/3·n⌉ of the n leave-one-game-out (LOGO) pooled values > 0.
- `contradicts_H_a`: pooled ≤ 0 **and** ≥ ⌈2/3·n⌉ LOGO values ≤ 0.
- Otherwise `inconclusive`.

### 5.3 Test
- One-sided **exact sign test** across games. This is the inferential frame the Examiner cited in `multiplicity.context`.
- `S_a = #{g : r_g > 0}`. Games with `r_g == 0` exactly are dropped. `n' = n − ties`. `p_a = P(Bin(n', 0.5) ≥ S_a)`.
- For H_b, over games with both FL1 and FL2 `maker_capital_usd > 0`: `S_b = #{g : d_g < 0}`, `p_b = P(Bin(n_b', 0.5) ≥ S_b)`. If `n_b' < 20` `[H]`, H_b is descriptive only.
- **Reported, not decisive:** a game-cluster bootstrap one-sided 95% lower bound on pooled FL1 maker gross ROI (B = 10,000, resample games with replacement, seed `20261001`) `[H]`.

### 5.4 Alpha and multiplicity (see §6)
One-sided α = 0.05 under fixed-sequence gatekeeping, H_a → H_b (→ H_c only if §7 adds one).

### 5.5 Robustness and stresses (pre-registered)
- LOGO; leave-one-series-out (postseason series group repeated matchups) `[H]`.
- `one_tick_worse`: maker charged $0.01/contract (capital +0.01, return −0.01), as in fb6540f5.
- `fees_2x` on the CACHE secondary.
- Non-primary strikes (descriptive).
- The `pre_admitted_at = true` rows, reported separately, never pooled.

### 5.6 Decision rule and verdict mapping (Examiner owns the verdict; single read)

| Verdict | Condition (all on gross, fee-free primary-strike rows) | Effect |
|---|---|---|
| `NOT_SCORED_INSUFFICIENT_N` | eligible n < 30 at every capture-close stamp so far | holdout stays sealed; no outcome join |
| **KEEP** (measurement; `promote=false`) | `supports_H_a` **and** `p_a ≤ 0.05` **and** pooled FL1 `maker_gross_roi` under `one_tick_worse` > 0 | Confirms the FL1 mid-band maker thesis for KXMLBSPREAD as a **measurement**. It opens (does not run) a one-knob money-path freeze: an FL1-only maker band filter on the Q6S5 maker leg, demo/shadow first. **Not a scoreboard KEEP.** v1.2: KEEP is judged on Astra P&L without rewards, and these are public counterparties' prints (`public_counterparty_realized`) with `pnl` null. Q6-000 is not retuned. |
| **KILL** (scope: FL1 mid-band maker thesis, KXMLBSPREAD only) | `contradicts_H_a` **and** `S_a ≤ n'/2` | the FL1 maker leg on KXMLBSPREAD is closed; combined with the H1 KILL, the FL-band maker family on KXMLBSPREAD goes to cemetery review |
| **ITERATE** | anything else (e.g. directionally positive with `p_a > 0.05`, or significant but fails `one_tick_worse`, or `inconclusive`) | no money path; any re-test needs a new untouched set |

**H_b label (only if KEEP on H_a, by fixed sequence):** `p_b ≤ 0.05` → `H_b_confirmed`, and the money-path freeze excludes maker quoting against FL2 takers. Otherwise `H_b_not_confirmed`. If H_a is not KEEP, H_b is descriptive only and gets no inferential label. H_b never changes the H_a verdict.

### 5.7 Fees and reporting
- Fees stay **`CACHE_NOT_R1P1`**: feebook `22371178…` `order_fee(role, q, price)` with FEE_PIN `9c0f3554…` terms only (`fee_type=quadratic`, `fee_multiplier=0.5`). `fee_honest=false`, `claim_as_live_R1P1=false`.
- If the Collector's holdout capture includes a new `/series/KXMLBSPREAD` body with different terms, Examiner reports both, and the label stays CACHE unless an Examiner-pinned `formula_id` exists.
- **Gross and net are both reported side by side** (`maker_gross_roi` and `maker_net_roi_cache` per arm, pooled and per game). The decision uses gross only.
- `results`/`pnl` stay null. `common_scorecard` metrics stay null with reasons, as in SCORE `2e74f17b…`.

### 5.8 Labels (proposed) `[H]`
- `evidence_class = HOLDOUT_UNTOUCHED`; `study_label = "prospective shadow"` (frozen before outcome, recorded forward, no orders; registry `8f36bf10…`).
- `label = public_counterparty_realized`; `counts_toward_keep` (strategy scoreboard) `= false`; `promote = false`; `live_promotion = false`.

## 6. Multiplicity
- **In-sample universe (3 Sep-24 games):** `family_size = 4` (analysis_slice PR58, fill_model PR60, price_band PR61, game_phase pending) per ACCEPT `08d23b36…` and SCORE `2e74f17b…`. All four are IN_SAMPLE_DEV, make no inferential claim, and act only as hypothesis selectors.
- **Holdout confirmatory family:** {H_a primary, H_b secondary, and H_c only if added by §7 before the read}.
- **Correction `[H]`:** fixed-sequence (hierarchical) gatekeeping at one-sided α = 0.05: H_a first; H_b only if H_a is KEEP; H_c only if H_b is confirmed. This controls the family-wise error ≤ 0.05 in the strong sense.
- **Bonferroni-4 shadow (reported, non-decisive):** the card also states whether `p_a ≤ 0.0125` (α/4 for the 4 in-sample knobs that generated candidates). If the Conductor prefers it as the binding α, it must say so **in the ACCEPT**, before `holdout_admitted_at`. At n = 30 that needs S_a ≥ 22 (exact size 0.0081).
- No other holdout cut (FL0, other strikes, per-band b00–b09, pre-admitted rows) carries an inferential claim.

## 7. Game-phase fold-in slot (placeholder; no numbers now)
- The game-phase knob (freeze `5beba803…`, ACCEPT `08d23b36…`; GP0 pregame = print < scheduled first pitch, GP1 = first pitch ≤ print < close; **scheduled start is a PROXY for actual first pitch**) is being implemented now and is **not scored**. Nothing here depends on its outcome.
- **Fold-in occurs only after** an Examiner SCORE of game-phase lands **and** the Conductor accepts it. The fold-in amendment must be filed and sha-stamped **before any holdout outcome join**, and preferably before `holdout_admitted_at`. If it arrives after an outcome join, GP strata on the holdout are descriptive only.
- **Pre-declared conditional rules (mechanical; chosen now):**
  - **R1:** game-phase reading `supports_H1` (GP1−GP0 < 0, in-play worse) and not price-confounded → add **H_c: FL1 maker gross ROI within GP0 (pregame) > 0** as the third step of the fixed sequence.
  - **R2:** GP1 / in-play FL1 is directionally positive in the scored game-phase output (within-FL1 maker gross ROI in GP1 > 0, or `contradicts_H1` with the within-FL1 secondary ≥ 0) → add **H_c: FL1 maker gross ROI within GP1 (in-play) > 0** as a **stratified secondary**, third in the fixed sequence.
  - **R3:** `inconclusive`, `inconclusive_price_confounded`, or the needed field is absent from the SCORE → GP strata on the holdout are **descriptive only**; no H_c.
- **Never:** promote any GP stratum to primary; choose between R1/R2/R3 after seeing holdout data; move the phase boundary (it stays scheduled first pitch parsed per 5beba803; `start_shift_plus_30m` only as a stress); fetch actual first-pitch times.
- The H_c test is the same as §5.3 (per-game sign test within the stratum), with the same `n_min` logic applied to games with stratum capital > 0.

## 8. Explicit refuses
No Kalshi or other market GETs by Variants · no orders (live or demo) · **never run `admit.py`** · **never open ADMIT-1 `capture.sqlite`** · no Lee-Ready · no Q6-000 retune · no S1 KXMLBGAME ML retune · no rebin of registry 0860cbe2 · no 5th knob on the 3 Sep-24 games · no use of the in-sample tape toward KEEP · no re-GET of the Sep-25 markets · no backfill or interpolation of the ADMIT-1 window · no interim look or lowering of `n_min` · no invented fills, PnL, depth, markets, first-pitch times or settlement timestamps · no cloud agent, PR or git push from this addendum · `results = null`, `pnl = null`.

## 9. Integrity
- This addendum creates only new files: this `.md` and its `.json` twin. No frozen file was edited and no `_prev` write was needed (RULE-FROZEN-EDIT-PREV-BYTES-001).
- It is **not** added to any MANIFEST of a frozen packet dir.
- No holdout row exists, so none was read. Inputs read to draft: only the pinned governance files in §1.
- Conductor asks:
  1. ACCEPT or amend the `[H]` items: n_min = 30; primary strike = 1.5-run; `scheduled_start > holdout_admitted_at`; fixed-sequence vs Bonferroni-4 binding; label `HOLDOUT_UNTOUCHED`; leave-one-series-out.
  2. Confirm the ordering gate (§3.1) with Clock and Collector.
