# AMENDMENT B: CARD01 NH-002-H House-only prospective freeze (pre-outcome, disclosed)

**Filed:** 2026-09-25T00:15:13Z (20:15:13 ET 2026-09-24). Author: Deep Research. **Pre-outcome:** no 2026 House race has been decided. The confirm set is untouched.

**Amends:**
- `packets/CARD01_HOUSE_ONLY_PROSPECTIVE_FREEZE_2026-09-24.md` (sha256 `c31724463d81747702910a2d5296c2fc21d2a1dbc594727b26ac3d894b55ec59`, frozen 23:52:48Z)
- Amendment A (`4e36d0db5728148d5bb4688fd8626eca9907a8933747f85e0bc17ede0ac0936b`, 23:59:50Z)

**Triggered by:**
- the Adversary leakage check `packets/ADVERSARY_CARD01_NH002H_LEAKAGE_CHECK_2026-09-24.md` (sha256 `9be7f027…91fb`);
- the Archivist source gate `packets/ARCHIVIST_SOURCE_GATE_ELECTINDEX_CARD01_2026-09-24.md` (sha256 `fb29ae5c94e357b0d4d6058d3c99a06697239542a61856005c058d4893a61310`, ruling **APPROVED_HASH_ONLY**);
- the Conductor instructions (including the Conductor refinement of 2026-09-24 ~20:10 ET, which governs where the two conflict).

**What this amendment leaves unchanged:**
- the universe (92 races, `UNIVERSE_2026_HOUSE_FROZEN.json` `d8af7451…8ca6`);
- the pre-commit (`2968f389…e77e`);
- the w grid {0.25, **0.5 headline**, 1.0} and the w = 0 control;
- the decision time 2026-11-02T22:00Z;
- the headline statistic (paired Brier D at w = 0.5 over all admitted races);
- the bootstrap (state-cluster, 10,000 resamples, seed 20261102);
- the entry gate (p_hybrid − price − fee − 2c > 3c);
- PASS (i)/(ii) and REJECT (a)–(d) logic;
- the controls.

**No new variant, forecaster, weight, source or decision time is added.**

---

## (a) National-miss statistic and recentering: exact definition (clarifies freeze §6 step 1)

**Problem:** freeze §6 step 1 says "subtract its own across-race mean logit error". Against 0/1 outcomes, logit(y) is undefined, so the rule was ambiguous (Adversary flag).

The exploratory script `EXPLORE_DIAG_national_factor_recentered_2253c03c.py` (sha256 `feffec5104882174031b43026e629e45771925c05272ee6e51b927dd5dafd144`):
- was written **after** the freeze, at 19:53 ET;
- is **not a pinned artifact** and defines nothing for scoring;
- is kept unchanged, with a byte copy at `…py.pre-20260925T001140Z`.

**Definition (governs scoring):**
- **Arms:** p_w = w·p_model + (1−w)·p_market, for w ∈ {0, 0.25, 0.5, 1.0}.
- **Descriptive national miss per forecaster (reported, all arms):** **M_f = mean_i (p_f,i − y_i).** This is the Conductor's statistic: the mean signed error of the forecast probability against 0/1 outcomes. Positive values mean Democrats were over-forecast.
- **Recentering (the operation used for PASS (ii)/REJECT (b)):** a uniform Bernoulli-likelihood logit shift per forecaster:
  - δ_f = argmax_δ Σ_i [ y_i log σ(ℓ_i+δ) + (1−y_i) log(1−σ(ℓ_i+δ)) ], where ℓ_i = logit(clip(p_f,i)), clip to [1e-4, 1−1e-4], and σ is the logistic function.
  - p̃_f,i = σ(ℓ_i + δ_f).
- **Justification for the Bernoulli shift:**
  - Its score equation is exactly Σ_i (p̃_f,i − y_i) = 0. It therefore sets the Conductor's statistic M_f to zero for the recentered forecasts.
  - It keeps every probability inside (0,1). A plain additive shift p − M_f can leave [0,1] and would need ad-hoc clipping.
  - It is parameter-free and applied identically to every arm, including the market.
- **Solver:**
  - Bisection on g(δ) = Σ_i (y_i − σ(ℓ_i+δ)), which is strictly decreasing, over [−10, 10] for 60 iterations (interval width < 1e-16).
  - If every y is identical there is no interior root. δ is then set to the bound and `boundary = true` is reported.
- **Recentered statistic:** D_rc(w) = mean_i [ (p̃_w,i − y_i)² − (p̃_0,i − y_i)² ].
  - CI: the frozen state-cluster bootstrap (10,000 resamples, seed 20261102, random.Random).
  - **δ_f is re-estimated inside every resample, for every arm.**
  - Percentile interval: lo = sorted[250], hi = sorted[9749].
- **Decision use (unchanged logic):**
  - PASS (ii) holds iff the recentered 95% CI of D_rc(0.5) lies wholly below 0.
  - REJECT (b) holds iff the recentered CI includes 0.
- **What recentering does and does not do:** recentering removes **only a uniform (same-in-logit-for-every-race) national shift**. It does not remove correlated misses that differ by district type, region or incumbency. The stress row below covers part of that.
- **Vote-share residual:** not used. Certified vote shares for all 92 races are not guaranteed at scoring. The scoring input is Kalshi settlement (0/1).

**Pinned implementation:** `packets/card01_hybrid_forecast/amendment_b/NH002H_AMENDMENT_B_national_miss.py`, **sha256 `049368f942741ff4a63acad328a49ff256252587d6c65f1e7e6d65d6101781f2`**.
- It is standard library only, deterministic, and makes no network calls.
- Input is a JSON file of rows {race_id, state, mapping_status, p_market, p_model, y} plus optional signals.
- If the script and this text ever disagree, this text governs and the Examiner flags the discrepancy.
- It must be committed and externally anchored **before any outcome** (see "Anchoring" below).

**Checks done before filing (none uses 2026 outcomes):**
- `amendment_b/SELFTEST_unit_checks.py` (`a06f1e23…8567`, synthetic data):
  - the recentered M_f is 0 to within 1e-9 for all arms;
  - the boundary flag works.
- `amendment_b/SELFTEST_SYNTHETIC_input.json` (`b16ba92b…cf65e`) → `SELFTEST_SYNTHETIC_output.json` (`0e93e153…82f23`): full end-to-end run (~74 s).
- `amendment_b/EXPLORATION_2024_house_primary_crosscheck_{input,output}.json` is **EXPLORATION**. It uses 2024 preserved-control rows (NH-001A House, 19 races, 2024-11-04T22Z) read-only; nothing is re-scored or altered.
  - The point estimates reproduce feffec51 exactly: δ_market −0.326 (feffec51 c = +0.326), δ_hybrid −0.243, and D_rc = −0.02760.
  - The CIs differ as expected, because of re-estimation within each resample and the seed. Recentered: this script gives [−0.04547, −0.00163]; feffec51 gave [−0.04831, −0.00398].
  - Mathematically it is the same estimator as feffec51's calibration-in-the-large bisection (δ = −c). The differences are:
    - (1) δ is re-estimated within each resample (feffec51 fixed δ on the full sample);
    - (2) the seed is 20261102 (feffec51 used 20240924);
    - (3) raw D uses unclipped p;
    - (4) the solver range and iteration count are pinned here.

### Correlated-swing stress row (secondary, non-gating; as instructed by the Conductor)

- **Swing grid:** S = {−0.50, −0.25, 0, +0.25, +0.50} logit, where positive means toward Democrats.
  - The grid brackets the 2024 exploration national shift of the market (~0.33 logit), which is design input only.
- **Computation:** for every signal selected by the frozen entry gate at the decision snapshot:
  - q_i(s) = σ(logit(p_0.5,i) + s);
  - expected gross per contract = q − price (D YES) or (1 − q) − price (D NO), summed over signals;
  - net = gross − Σ fee, **only** when every fee is from the Archivist manifest (see (c)). Otherwise net = `BLOCKED_FEE_UNVERIFIED`.
  - Report `n_sign_flips_vs_s0` and `share_sign_flips_vs_s0` (signals whose expected gross EV sign differs from the s=0 baseline).
- The row is descriptive. It cannot PASS or REJECT anything.

## (b) ElectIndex methodology regime (hash-only)

- **Baseline regime R0:** methodology asset `https://electindex.com/wp-content/themes/electindex/assets/forecasts/eifc-info.js` (served as `?ver=1.9.989`). sha256 `caaff53e739413a8340f0addbec7136ec1995195291cab61889a94c1286ea87f`, fetched by the Adversary 2026-09-25 00:05Z.
  - There is no `/methodology/` URL (404). The human-readable view is `https://electindex.com/forecasts/#info`.
  - R0 **already includes** the 21 September 2026 additions (§5, "not re-run") and the §7 late-cycle boost. The boost "phases in over the final six weeks, so forecasts published through 22 September 2026 are unchanged".
  - The boost's scheduled phase-in is **drift within R0**, not a regime change. It moves forecasts by design during the capture window, and this is disclosed.
- **Capture:** one GET per day of that asset. Store the hash, HTTP status/Date, bytes and fetched_at only. Raw bytes go to `/workspace/lab/evidence_private/electindex/…` and never to git or governance.
  - This **requires an Archivist pin extension**, because the current pin covers only `races_summary.csv`. Until the extension is granted, no methodology capture runs, and the regime is reported as `UNMONITORED` for any unmonitored interval.
  - Optionally, the repo README is captured via raw.githubusercontent under the same extension.
- **Regime rule:**
  - Any sha256 change starts a new regime R1, R2, … and is logged with its first-seen date.
  - The scoring snapshot's regime is reported.
  - If the regime changed between the freeze and the decision snapshot, the headline stays as frozen (latest admissible snapshot). The following are added as **sensitivity** results:
    - (i) results using the latest captured snapshot from before the change (subject to the frozen 7-day max-age rule; otherwise reported as unavailable);
    - (ii) the headline split by regime of the snapshot used.
  - A regime change by itself never voids the freeze.

## (c) Fee: BLOCKED until the Archivist manifest

- The pinned R1-P1 feebook (`22371178…`) `series_fee_table.stub.json` has `"overrides": {}`. House series would therefore silently fall back to 0.07·p·(1−p) (Adversary flag).
- **Ruling:** the true `fee_type` and `fee_multiplier` for `KXHOUSERACE` **and every legacy series used by Amendment A** must be fetched from the Kalshi series endpoint **by the Collector** and entered in the Archivist fee/account manifest **before any outcome**.
- **Until then:** the after-cost numbers are **BLOCKED**, not computed with the fallback. This covers the net P&L, the stress-row net and the signal set itself, because the fee enters the entry gate.
- The 0.07·p·(1−p) figure stays a labeled sensitivity only, as frozen.
- **Preliminary, not admitted:** the saved series list received 23:34Z (`live_get_2026-09-24/series_list_*.json`) shows `fee_type: quadratic` and `fee_multiplier: 1` for `KXHOUSERACE` and all 35 legacy series (including both `HOUSEMI7` and `HOUSEPARTY-MI07`). This is not a manifest entry.

## (d) Split by mapping status (anti-attrition)

Report n, states, D_raw, D_rc and both CIs (same bootstrap, with δ re-estimated within group), and the M_f per arm, separately for:
- **M1:** races resolved to a `KXHOUSERACE` `-D` contract (58 at freeze);
- **M2:** races resolved to a legacy per-district series under Amendment A (up to 34);
- **M3:** races unverified, unresolved or excluded at the decision time (no `-D` contract found, or a §5 exclusion). These are **counted, with a reason per race**, and not scored.

**Rules for the split:**
- The **headline stays as frozen** (all admitted races).
- M1/M2 are secondary.
- Dropped competitive seats cannot flatter the headline unseen. If M3 > 0, the Examiner reports the M3 races' decision-time market mids and forecast gaps next to the headline.

## (e) Source quality: ElectIndex track record = IN-SAMPLE and UNCHECKED, not validation

Source: `https://electindex.com/wp-content/themes/electindex/assets/forecasts/eifc-trackrecord.js`.
- Fetched once at 2026-09-25 00:11:23Z (HTTP 200, 41,859 B, Last-Modified Wed, 23 Sep 2026 17:54:15 GMT).
- sha256 `6aed2d13d845ce7ea27cef2806d5a26f957de88c75f45a90c63a1861385bb0d1`, which matches the Adversary's hash.
- Raw bytes are stored privately only.

The file presents two records. Quoted strings:
- **"Old Forecast / Published for 2022 & 2024":** "The forecasts ElectIndex (then MapWise) actually published for 2022 and 2024, scored against the results as they were called at the time."
- **"Current Forecast":** "The current 2026 model re-run on each past cycle", described as "A backtest of today's model, not a forecast that was published at the time". House maps cover 2004–2024.
- The numeric scores (Brier, hit rate, margin error) are rendered from a separate data bundle that we did **not** fetch. **No number is recorded or relied on.**

**Classification for this card:**
- The **2004–2024 backtest is IN-SAMPLE**: the 2026 model was built with those outcomes known.
- The **2022/2024 published record** comes from predecessor (MapWise) models and was self-reported. For the 2026 model it is also **IN-SAMPLE**, because those outcomes were known when the 2026 model was built.
- Its publication-time status is **UNCHECKED**: no archived snapshots were compared.
- Both are self-published on a product page, i.e. **marketing-grade**. **Neither is validation.**
- ElectIndex enters NH-002-H only as a pre-registered comparator whose 2026 performance is what is tested.

**Gate status for D1 (source map updated):**
- (a) licence/storage: **APPROVED_HASH_ONLY** (Archivist);
- (b) market-independence: **documented independent; code unaudited** (`src/model` is not public);
- (c) track record: **in-sample/unchecked**;
- gates (b)/(c) remain open for the Archivist to close.

## Recorded constraints and disclosures

1. **Archivist capture pin (verbatim terms):**
   - exactly `GET https://raw.githubusercontent.com/ElectIndex/26_us_forecast_data/main/output/races_summary.csv`, once per UTC day at a fixed time declared before the first capture;
   - curl, UA `Astra-Collector/1.0 (read-only research capture; card01-NH002-H)`, attempt = 1, no retries; a non-200 is logged and the day stays missing;
   - raw file to `/workspace/lab/evidence_private/electindex/card01-nh002-house/<YYYY-MM-DD>/races_summary.csv`, log to `/workspace/lab/astra-capture/card01-nh002-house/electindex_capture_log.jsonl`;
   - git or governance receive only the hash, URL, timestamps, status/Date, bytes and `race_code`+`dem_prob` for the 92 races;
   - ToS re-read weekly (current "Last updated September 1, 2026"); live or published use needs a re-gate under ToS §06.
2. **Source probe:** the four `source_probe_electindex/` files (~19:45 ET) are **PRE_FREEZE design input only**. They are never a capture record or a scoring snapshot. The first admissible capture must postdate both 23:52:48Z and the Archivist ruling. The Archivist recommends relocating those raw files to evidence_private; that is the Archivist's or Steward's action.
3. **Adversary caveats:**
   - (i) ElectIndex independence is documentary only; the code is unaudited.
   - (ii) "Pre-commit written before any 2026 price was viewed" is **ASSERTED, not verified**. Recovered predecessor files containing 2026 books for KXHOUSERACE-AL01/**AL02**/AL03-26-D (captured 05:20Z; AL-02 in universe, bid/ask 0.28/0.29) landed on the box at 19:43:53 ET, ~5 min before the pre-commit (19:48:37 ET).
     - The w grid is verified to predate all 2026 prices (SPEC commit 7daf8665, 04:53:45Z).
     - The universe is verified price-independent by mechanical reproduction.
     - A ledger footnote has been added.
   - (iii) Governance timestamps are not externally anchored (see Anchoring).
   - (iv) Legacy-series attrition and depth are unmeasured; hence split (d).

## Anchoring

`/workspace/lab/governance` is not a git repository. The hash set in the card01 LEDGER/MANIFEST (this amendment, the pinned script, the .pre and .reconstructed copies) must be committed or externally anchored by the Archivist/Steward **before 2026-11-02T22:00Z and before any race outcome**. Deep Research does not push.

## p16 checklist delta (v1.2 §J; statuses remain null for the Examiner)

| # | Item | Change |
|---|---|---|
| 3 | Information set | + methodology-regime monitoring (b) and Archivist capture pin (verbatim above); source_probe = pre-freeze only |
| 4 | Fees/fills | House fee **BLOCKED** until the Archivist manifest holds series-endpoint fee_type/multiplier (c); fallback is sensitivity only |
| 9 | Metrics/tests | Recentering defined exactly (a) + pinned script hash; correlated-swing stress row (secondary); M1/M2/M3 mapping split (d); regime split if applicable (b) |
| 11 | Variant log | No new variants. Attempted-variant count unchanged (0 new) |

All other items are unchanged.

## Collector request (Deep Research makes no Kalshi GETs; ≤3 rpm, ≥20 s spacing per the Collector budget Addendum 1)

- `GET /trade-api/v2/series/KXHOUSERACE`
- `GET /trade-api/v2/series/<T>` for T in: HOUSEAZ1, HOUSEAZ2, HOUSEAZ6, HOUSECA22, HOUSECO3, HOUSECO8, HOUSEFL13, HOUSEIA3, HOUSEME2, HOUSEMI4, HOUSEMI7, HOUSEPARTY-MI07, HOUSEMI10, HOUSEMT1, HOUSENC1, KXHOUSENC11, HOUSENE2, HOUSENH1, HOUSENJ7, HOUSENY17, HOUSEOH9, HOUSEPA1, HOUSEPA7, HOUSEPA8, HOUSEPA10, KXHOUSETX9, HOUSETX15, KXHOUSETX32, HOUSETX34, KXHOUSETX35, HOUSEVA1, HOUSEVA2, HOUSEWA3, HOUSEWI1, HOUSEWI3 (35 requests)
- Fields to record: `fee_type`, `fee_multiplier`, `contract_terms_url`, `last_updated_ts`, plus the HTTP status/Date and sha256 of the body.
- Collector-owned, already open (not new): legacy-series open-markets checks for the Amendment A mapping, and `CONTROLS` (never captured).
