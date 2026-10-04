# ADVERSARY: Card 01 NH-002-H Amendment B, pre-outcome advisory review (2026-10-03 ET)

**Seat:** The Adversary "KALSHI" (Astra Drift Guard). **ADVISORY ONLY.** This packet blocks nothing and votes on nothing. It changes no frozen file or parameter. No live orders were placed and no messages were sent. No 2026 outcome was used, because none exists.
**Target:** Amendment B `packets/CARD01_HOUSE_ONLY_PROSPECTIVE_FREEZE_2026-09-24_AMENDMENT_B.md` (sha256 `ee6af37c…c2c6`), accepted by the Conductor (`CONDUCTOR_ACCEPT_CARD01_NH002H_AMENDMENT_B_2026-09-24.json`, sha256 `74c5d49c…bd23`). The Conductor asked for review of the national-miss definition and the correlated-swing stress.
**Tags:** [V] verified · [I] inferred · [H] hypothesis · [A] assumption · [U] unknown.
**Q6-`000`: unchanged.**
**Written:** 2026-10-03T17:08-04:00 ET.

---

## Verdict (top line): **ADVISORY_FLAGS**

The national-miss definition is now well-defined. The pinned script matches the amendment text on every scoring-relevant point, and it is deterministic. On toy data it recovers a known uniform shift exactly and gives δ = 0 in the zero-shift case [V].

There are no leaks and no fabrication. Nothing here should reopen the ACCEPT. Eleven fixes are worth pinning **before 2026-11-02T22:00Z / any outcome**, in priority order:

| # | Flag | Sev. | Owner (suggested) | Fix to pin pre-outcome |
|---|---|---|---|---|
| AF-1 | **PASS (ii) and REJECT (b) are not complements.** PASS (ii) needs the recentered CI wholly below 0. REJECT (b) fires only if that CI *includes* 0. If the recentered CI is wholly **above** 0 (the hybrid is worse after recentering), neither fires. If the raw CI is then also wholly below 0, REJECT (a) does not fire either, and the verdict falls to (c)/(d), which are fee-BLOCKED (AF-2). The result is an undefined verdict that would be interpreted after outcomes. | MED | Conductor / Deep Research | Restate REJECT (b) as "recentered CI **upper bound ≥ 0**" (mirrors REJECT (a); exact complement of PASS (ii)). |
| AF-2 | **REJECT (c)/(d) cannot be evaluated while the fee is BLOCKED.** Amendment B blocks the signal set itself, because the fee enters the entry gate, so taker P&L and top-1 share have no input. "Any one means REJECT" has no rule for BLOCKED. | MED | Conductor | Pre-declare: if the fee manifest is not ADOPTED at scoring, the verdict is capped at **forecast-only** (PASS-FORECAST / REJECT on (a)/(b)). (c)/(d) are reported as `BLOCKED_FEE_UNVERIFIED`, and no after-cost, trading or KEEP claim is made. |
| AF-3 | **ElectIndex capture has stalled since 2026-09-26.** The box log has no methodology-asset or `races_summary.csv` capture after 2026-09-26T20:17Z. The scheduler pid 453207 is not running. Under Amendment B (b), 09-27 → now is `UNMONITORED`, and the frozen 7-day max-age rule will need a fresh snapshot by 11-01. | MED (ops) | Collector / Archivist | Restart under the existing pin and log the gap as UNMONITORED with dates. Do not backfill. |
| AF-4 | **The script cannot tell where a fee came from.** The stress-row `expected_net` is computed whenever every fee is *numeric*, so a 0.07 fallback typed as a number yields a "net" figure (toy T9). BLOCKED is enforced by process only. | LOW-MED | Variants / Examiner | Require a `fee_source` field equal to the adopted manifest id, or an Examiner attestation in the result packet. Otherwise report BLOCKED. |
| AF-5 | **Boundary hits inside the bootstrap are neither counted nor reported.** In small or skewed splits (M2), resamples where every y is identical set δ = ±10 and distort D_rc. Toy: an 8-race / 7-win group hit the boundary in 34.4% of resamples. | LOW | Variants / Examiner | Report `n_boundary_resamples` per arm and block. Pre-declare that a split CI with more than 5% boundary resamples is labelled `UNSTABLE_SPLIT`; this is descriptive only, and the headline is unaffected. |
| AF-6 | **The text and the code disagree on when `boundary` is set.** The text says the bound is used only "if every y is identical". The code also returns the bound with `boundary=true` when y is mixed but the root lies outside [−10, 10] (toy A). This is practically unreachable [I]. But "this text governs" means any discrepancy found after outcomes would force new code after outcomes. | LOW | Deep Research | Add one pre-outcome erratum sentence: "δ is set to the bound (`boundary=true`) whenever g has no root in [−10, 10]." |
| AF-7 | **The swing stress has no pre-declared reading rule, and it can vanish silently.** If no signals are passed, the script emits `NO_SIGNALS_SUPPLIED` and the row disappears. The row is outcome-free, but it is not yet scheduled to be frozen at decision time. | LOW-MED | Examiner / Conductor | See §2 recommendations R1–R4. |
| AF-8 | **The upstream code is not pinned.** The input builder (snapshot → rows `{p_market, p_model, mapping_status, y}`) and the entry-gate / signal-list code are not pinned. No such script was found under `governance/astra` or `astra-capture` (name search). | LOW-MED | Variants | Pin and anchor the builder and gate code (by hash) before the 11-02 decision snapshot. |
| AF-9 | **Card 01 `_prev` gap: one file.** `card01_hybrid_forecast/MANIFEST.md` moved from `16f96d3d…` (the value in the LEDGER hash register and the public extract) to `f22df25b…` with no copy of the `16f96d3d` bytes anywhere on the box. That makes it **UNVERIFIED_BYTES_MISSING** under the rule. Materiality is low: it is an index file with no scoring parameter [I]. Separately, the 2026-09-24 session used in-place `.pre-20260925T001140Z` copies rather than `_prev/<sha>.<name>`. That is a format deviation the Archivist accepted; the bytes are intact. | LOW | Archivist / Deep Research | Record `MANIFEST.md 16f96d3d→f22df25b` as UNVERIFIED_BYTES_MISSING (index-only) or reconstruct it. Optionally mirror the `.pre` copies into `_prev/` (copy only; delete nothing). |
| AF-10 | **The fee evidence has a small coverage hole.** Only `KXHOUSERACE` (among the 36) has a per-series endpoint GET. The 35 legacy series rest on the series-*list* responses. `HOUSEVA2` is missing from the Scout's derived `house_series_fee_fields.csv`, though the raw series list shows it as `quadratic`/1. | LOW | Scout / Archivist | Add HOUSEVA2 to the derived table. State whether series-list fields satisfy Amendment B's "series endpoint" wording. |
| AF-11 | **The interpreter version is not recorded in the output.** Determinism was verified on CPython 3.13.5. `random.Random` / `choices` streams are stable across recent CPython [I], but this is not pinned. | LOW | Variants | Emit `sys.version` in the result JSON. |

---

## 0. Hash verification (re-hashed 2026-10-03 ~16:55–17:00 ET)

| Artifact | sha256 (box, now) | Matches | Tag |
|---|---|---|---|
| Amendment B `.md` | `ee6af37cef95f1e468d28e5b06750caaca8b1706ec11ed5cf5cdce460524c2c6` | ACCEPT json, LEDGER register, public extract | [V] |
| Pinned script `amendment_b/NH002H_AMENDMENT_B_national_miss.py` | `049368f942741ff4a63acad328a49ff256252587d6c65f1e7e6d65d6101781f2` | ACCEPT, LEDGER, extract, exp2 `FROZEN_EXPERIMENT.json` | [V] |
| Base freeze | `c31724463d81747702910a2d5296c2fc21d2a1dbc594727b26ac3d894b55ec59` | Anchor manifest, ACCEPT | [V] |
| Amendment A | `4e36d0db5728148d5bb4688fd8626eca9907a8933747f85e0bc17ede0ac0936b` | Anchor manifest, ACCEPT | [V] |
| Earlier Adversary check | `9be7f027a79af1807f9ac0579efffc63465aec5f66af4625976b8b24801691fb` | Amendment B cites `9be7f027…91fb` | [V] |
| Archivist anchor `CARD01_HASH_ANCHOR_MANIFEST_2026-09-24.json` | `e1d019b5385981730eb2dd1c9b718d40a0a675af2fa0545f202c58005f1b11cd` | Identical in the astra-science clone; the file is on `origin/main` (commit `0cbe603`) | [V] |
| Pre-commit / universe | `2968f389…e77e` / `d8af7451…8ca6` | Anchor manifest | [V] |
| Conductor ACCEPT | `74c5d49c0452ce97def7b36129ba362ebc4387627b93d5611bb67c5f8dfcbd23` | — | [V] |
| `feffec51…` EXPLORE_DIAG | `feffec51…d144` (`.pre` copy byte-identical) | Explicitly **NOT pinned** (Amendment B §(a); Archivist index) | [V] |

**Anchoring notes:**
- The anchor manifest (recorded 20:10:43 ET 09-24) predates Amendment B (20:15:13 ET) and does **not** list it [V].
- Amendment B, the script, the self-tests, the 2024 cross-check and the `.pre` copies are hash-anchored by `LEDGER_HASH_REGISTER_EXTRACT_2026-09-24.json` (`03f9c193…`). The extract is on local `origin/main` via commit `47f0ec5` "(PR56)", dated 2026-09-24T17:28:54-07:00 (= 20:28:54 ET). [V] for the local clone. That the date is server-side is [I]; git dates can be client-set.

## 1. National-miss definition and recentering

**1.1 Definition [V].**
- M_f = mean_i(p_f,i − y_i) is computed for **every arm** w ∈ {0, 0.25, 0.5, 1.0}, including the market (w = 0), as `M_raw`. It uses unclipped p, consistent with the text.
- It is computed again within the KXHOUSERACE and LEGACY splits.
- y = 1 iff the `-D` contract settled YES, so positive M_f means Democrats were over-forecast. Text and code agree.

**1.2 Bernoulli-MLE uniform logit shift: the specification is complete [V].**

| Element | Amendment text | Code | Match |
|---|---|---|---|
| Objective | argmax_δ Σ[y log σ(ℓ+δ) + (1−y) log(1−σ(ℓ+δ))] | Root of the score g(δ) = Σ(y − σ(ℓ+δ)) | ✔ |
| Clip | [1e-4, 1−1e-4] before logit | `EPS=1e-4`; `logit()` clips | ✔ |
| Solver | Bisection over [−10, 10], 60 iterations | Same; width 20/2^60 ≈ 1.7e-17 | ✔ |
| Ties | Not stated | `g(mid)==0` → upper half (deterministic, immaterial) | ✔ (deterministic) |
| No interior root | Bound and `boundary=true` "if every y identical" | Bound and `boundary=true` whenever g(−10) ≤ 0 or g(10) ≥ 0, which includes mixed-y roots beyond ±10 | **Superset → AF-6** |
| Logistic stability | — | Branch-stable `sig()` | ✔ |
| Recentered prob | σ(ℓ+δ_f) | Same | ✔ |
| Blend then shift | p_w blended first, then shifted by δ_w | Same | ✔ |
| D_rc | mean[(p̃_w−y)² − (p̃_0−y)²] | Same | ✔ |
| CI | State-cluster bootstrap, 10,000 resamples, `random.Random(20261102)`, δ re-estimated in **every** resample for **every** arm, lo = sorted[250], hi = sorted[9749] | Same; indices computed as [250, 9749] | ✔ |
| Split | δ re-estimated within group | Same | ✔ |

The log-likelihood is strictly concave in δ (g is strictly decreasing), so any interior root is unique and bisection converges to it deterministically [V math, [I] numerically]. With the frozen universe the forecasts lie in [0.10, 0.90], and Kalshi mids lie inside (0, 1). Clipping therefore never binds in practice, and the gap between unclipped M_f and clipped δ is nil [I].

**1.3 Toy runs** (scratch only: `/workspace/scratch_nh002h_adv/`, on a byte copy of the pinned script, sha `049368f9…` re-verified; synthetic data only; **no number below is a result**) [V]:

| Test | Outcome |
|---|---|
| T1 zero-shift (Σp = Σy exactly) | δ = −6.1e-17, boundary false → **zero recovered** |
| T2 exact recovery, soft labels y = σ(ℓ+δ₀), δ₀ ∈ {−1.5, −0.5, −0.326, 0, 0.25, 0.5, 2.0} | \|δ̂ − δ₀\| ≤ 5.6e-17 for all → **known shift recovered exactly** |
| T3 0/1 outcomes, n = 200,000, δ₀ ∈ {−0.5, 0, +0.5} | δ̂ = −0.4967 / −0.0005 / +0.4988 (sampling noise only) |
| T4 sign link | M_raw = +0.0537 ↔ δ = −0.2795; recentered M = −3.8e-18 |
| T5 p exactly 0 and 1 | No crash; clip applied |
| T6 all y = 1 / all y = 0 | (+10, true) / (−10, true) ✔. Mixed y, root > 10 → (+10, true) (AF-6) |
| T7 row permutation | δ identical (diff 0.0) |
| T8 a +0.6 logit bias added to the market only (model = truth) | δ_market shifts by exactly −0.600. D_raw(0.5) = −0.0071 → D_rc(0.5) = +0.0005, and D_rc(1.0) = −3e-18: **recentering removes the gain that came purely from the uniform market bias**, as intended |
| Full script, toy 92-row input (58/30/4) with 3 signals: run 1, run 2, and run 3 on row-permuted input | All three outputs are **byte-identical** (`6fdcb8b9…146b`); ~91 s per run |

Scratch hashes: `unit_tests.py` `8636bf13…`, out `a8c87ffc…`; `make_toy.py` `28f5c762…`; `toy_input.json` `a111f897…`; `gap_and_boundary.py` `96363efd…`, out `b30eb7a3…`.

**1.4 Does REJECT (b) still make sense?**
- It is the right *kind* of test, and it is applied consistently. D_raw and D_rc come from the **same** state resamples, with the same seed and δ re-estimated per resample, so the recentered CI carries the uncertainty of δ itself [V]. That is stricter than feffec51, which fixed δ.
- The wording "CI includes 0" leaves the wholly-above-0 case unassigned (**AF-1**).
- I searched for a realistic toy case (raw CI < 0 and recentered CI > 0) over 39 seeds and did **not** find one. The gap is logical [V text], and its likelihood is [H] low. It is still a free post-outcome choice and costs one sentence to close.

**1.5 Can the definition be chosen or interpreted after outcomes?**
- M_f is descriptive. Only δ (via D_rc) gates [V].
- feffec51 is excluded [V].
- The solver, bounds, iteration count, seed and resample count are fixed in code and text [V].
- Remaining channels:
  - (i) the "text governs" clause combined with AF-6;
  - (ii) the undefined verdict cell (AF-1, AF-2);
  - (iii) the unpinned input builder and signal gate (AF-8). Which rows are marked `UNRESOLVED`, and which mid is used, are decided upstream of the pinned script.
- The script also routes any unexpected `mapping_status` string, or a null y/price on a mapped race, into `UNRESOLVED_or_unscorable` without saying why [V]. Amendment B (d) requires a reason per race from the Examiner. Recommend an assert on the status vocabulary.

**1.6 M_f on the probability scale vs recentering on the logit scale: not a problem [V/I].**
- The MLE score equation *is* Σ(p̃ − y) = 0, so the logit-scale shift sets the probability-scale statistic to exactly zero (all arms, |M_rc| ≤ 1e-17 in the toys) [V].
- sign(δ) = −sign(M_f) because g is monotone [V].
- Magnitudes are not interchangeable across forecasters: the same M_f needs a different δ depending on how spread out p is [I]. Since M_f does not gate, it is enough that the script reports δ next to M_f, which it does [V].
- Recentering is in-sample by design (δ is fit on the outcomes it is scored on). It removes only a uniform logit shift, which the text states [V].

## 2. Correlated-swing stress

**2.1 Specification [V]:**
- **Grid:** S = {−0.50, −0.25, 0, +0.25, +0.50} logit, positive toward D. Fixed in the text and as `SWING_GRID` in the pinned code.
- **Applied to:** the **probabilities**, not the outcomes. q = σ(logit(clip(p_0.5)) + s) uses the raw headline hybrid (not recentered), uniformly to **every gate-selected signal**.
- **Output:** expected gross per contract under the swung hybrid, the net (or `BLOCKED_FEE_UNVERIFIED`), and the count and share of sign flips against s = 0.
- **No randomness:** no seed is needed, and the row is deterministic [V].
- **Outcome-free:** it uses only decision-snapshot data [V]. It can therefore be computed, and frozen, **before** any outcome [I].

**2.2 Limits [V/I]:**
- It stresses only the hypothetical P&L book (~9 expected signals; the freeze says P&L has almost no power). It does **not** stress the gating Brier statistic.
- The Brier headline's exposure to a *uniform* national miss is handled by recentering (REJECT (b)). Exposure to non-uniform correlated misses (district type, region, incumbency) is covered by neither; the amendment says so [V].
- The ±0.5 grid is anchored on one 2024 exploration (~0.33 logit market shift). Whether it brackets a plausible 2026 national miss is **[U]**.
- While the fee is BLOCKED, the real signal set is BLOCKED (Amendment B (c)), so the row **cannot currently run on the real book** [I].
- If the signal list is omitted, the row silently becomes `NO_SIGNALS_SUPPLIED` [V].

**2.3 Is non-gating acceptable?** Yes, with a reporting rule. One election is one national draw, and the P&L has almost no power, so gating on it would add noise rather than protection. But it should not be possible to drop the row or reinterpret it after outcomes. **Recommendations (do not block):**
- **R1. Freeze at decision time.** The Examiner emits the stress row at 2026-11-02T22:00Z from the decision snapshot and hash-anchors it before any race is called. This is outcome-free, so it is cheap.
- **R2. Fragility label (pre-declared).** Any PASS-FORECAST write-up or P&L figure carries `FRAGILE_NATIONAL_SWING` if, at s = −0.5 or +0.5, either (a) total expected gross ≤ 0 or (b) `share_sign_flips_vs_s0` ≥ 0.5. The label sits next to the headline and the verdict is unchanged.
- **R3. Defect rule.** `NO_SIGNALS_SUPPLIED` while the gate selected ≥ 1 signal is a reporting defect, not an absent row. If the fee is still BLOCKED, the row is reported as `BLOCKED_FEE_UNVERIFIED` (signal set unavailable). It is not omitted.
- **R4. Optional, declared now or never.** Add reporting-only rows at ±1.0 logit, and a descriptive D_raw/D_rc split by a pre-named district attribute (for example the ElectIndex rating bucket at freeze). Neither may gate.

## 3. Flags (b)–(e): present in the text as described?

| Flag | In Amendment B text | Status now | Tag |
|---|---|---|---|
| (a) national miss | §(a): M_f = mean(p − y); Bernoulli-MLE recentering; feffec51 "**not a pinned artifact**" | As in §1 | [V] |
| (b) methodology regime | §(b): R0 = `caaff53e…87f` (`eifc-info.js`), daily hash-only capture, R1/R2 rule, sensitivity rows, never voids the freeze | Hook ran 2026-09-25 and 09-26, both R0 (`changed_vs_R0=false`). **No capture after 09-26; scheduler not running (AF-3).** 09-27 → now = UNMONITORED | [V] |
| (c) fee BLOCKED | §(c): after-cost **BLOCKED** (net P&L, stress net and the signal set); 0.07 is sensitivity only; series-endpoint fee_type/multiplier into the Archivist manifest | Fee ADDENDUM_02 (`44a69092…`) is stamped `quadratic`/M=1 but still **DRAFT_NOT_ADOPTED**, member_type **OPEN**. Its own text says Card 01 after-cost KEEP is not unblocked. The Conductor ACCEPT says ADDENDUM_02 "remains blocking". **BLOCKED stands.** Text prevents fee-honest claims. Code does not enforce it (AF-4). The verdict path is undefined (AF-2) | [V] |
| (d) mapping split | §(d): M1/M2/M3; headline stays all-admitted; M3 counted with reasons, plus mids and gaps if M3 > 0 | Script implements M1/M2 with δ re-estimated within group. M3 is a count only, so reasons and mids are an Examiner duty | [V] |
| (e) track record | §(e): 2004–2024 backtest **IN-SAMPLE**; 2022/24 published record IN-SAMPLE and **UNCHECKED**; marketing-grade; "No number is recorded or relied on" | As described | [V] |

## 4. RULE-FROZEN-EDIT-PREV-BYTES-001 check (card 01)

The rule was adopted around 20:09 ET on 2026-09-24 (`registry/RULE_FROZEN_EDIT_PREV_BYTES_2026-09-24.md`, `f0aab7d1…`).

| File | Edit | Prior bytes | Status | Tag |
|---|---|---|---|---|
| Freeze, Amendment A, Amendment B, script, pre-commit, universe | None (hashes match the anchors) | n/a | Clean | [V] |
| Decision packet `58c44c4f→d59c2642` | 20:05:19 ET, **before** the rule | Byte-exact `.reconstructed-58c44c4f` (re-hash matches) | Pre-rule; resolved by reconstruction (Archivist: DOCS_ONLY_VERIFIED_BY_RECONSTRUCTION) | [V] |
| Decision packet `d59c2642→c0c1aa66`; `FROZEN_EXPERIMENT.json` `4b90eedc→44cb582f`; LEDGER `e3d44bfb→d8ddfda7`; README `11556199→938b503e`; SOURCE_MAP `29ca593a→2b38699d`; MANIFEST `4a757483→16f96d3d` | ~20:11:40 ET, **after** the rule | In-place `*.pre-20260925T001140Z`. All re-hash to the LEDGER register values | **Format deviation** (not `_prev/<sha>.<name>`). The Archivist accepted it ("Acceptable"). Bytes intact | [V] |
| MANIFEST `16f96d3d→f22df25b` | After the hash register was written (disclosed in LEDGER "post-register re-hash" and in Steward HYGIENE) | **None.** No file with sha `16f96d3d…` was found on the box (filesystem search of card01 `MANIFEST.md*`); there is no `_prev/` in `card01_hybrid_forecast/` | **UNVERIFIED_BYTES_MISSING** (index-only; low materiality) → AF-9 | [V] |
| `card01_exp2_census/*` + exp2 kernel + exp2 ACK brief | None (all 10 entries of `HASH_REGISTER_2026-09-24.txt` match) | n/a | Clean | [V] |
| Any card01 file modified after the 2026-10-01 23:12 restore | None found by mtime | — | Clean (mtime-based; [I]) | [V]/[I] |

## Not done / limits

- No real 2026 inputs were run, because none exist. All numbers in §1.3 are synthetic.
- The full 10,000-resample toy runs used the frozen seed on toy data only. The REJECT-gap search used 2,000 resamples (toy speed) and is labelled as such.
- ElectIndex was not re-fetched. Capture status comes from the box log only. Whether a capture runs elsewhere is [U].
- No shared or frozen file was edited. The only governance writes are this packet and one register line.
