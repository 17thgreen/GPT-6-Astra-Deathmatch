# AMENDMENT C: CARD01 NH-002-H House-only prospective freeze: pins for the Adversary ADVISORY_FLAGS on Amendment B (pre-outcome, docs-only)

**Dated:** 2026-10-03 (ET). **Filed:** 2026-10-03T21:12Z (17:12 ET). **Author:** Deep Research.
**Status:** **`AWAITING_CONDUCTOR_ACCEPT`**
**Pre-outcome:** no 2026 House race has been decided or called. The election is 2026-11-03. No race outcome, settlement, call or 2026 price was used to write this text. Every pin below is fixed now, before the decision snapshot **2026-11-02T22:00Z**, and none is chosen from outcomes.
**Docs-only:** this amendment writes no code and edits no code. It makes no Kalshi API call, places no order, and states no number, P&L or result.

---

## 0. Header lineage

| Artifact | Path | sha256 | Role |
|---|---|---|---|
| Base freeze | `packets/CARD01_HOUSE_ONLY_PROSPECTIVE_FREEZE_2026-09-24.md` | `c31724463d81747702910a2d5296c2fc21d2a1dbc594727b26ac3d894b55ec59` | Amended (unchanged byte-for-byte) |
| Amendment A | `packets/CARD01_HOUSE_ONLY_PROSPECTIVE_FREEZE_2026-09-24_AMENDMENT_A.md` | `4e36d0db5728148d5bb4688fd8626eca9907a8933747f85e0bc17ede0ac0936b` | Amended (unchanged byte-for-byte) |
| Amendment B (**ACCEPTED**) | `packets/CARD01_HOUSE_ONLY_PROSPECTIVE_FREEZE_2026-09-24_AMENDMENT_B.md` | `ee6af37cef95f1e468d28e5b06750caaca8b1706ec11ed5cf5cdce460524c2c6` | Amended (unchanged byte-for-byte) |
| Conductor ACCEPT of B | `packets/CONDUCTOR_ACCEPT_CARD01_NH002H_AMENDMENT_B_2026-09-24.json` | `74c5d49c0452ce97def7b36129ba362ebc4387627b93d5611bb67c5f8dfcbd23` | **Stands.** Not reopened by this text |
| Pinned script | `packets/card01_hybrid_forecast/amendment_b/NH002H_AMENDMENT_B_national_miss.py` | `049368f942741ff4a63acad328a49ff256252587d6c65f1e7e6d65d6101781f2` | **Unchanged** by this text |
| Adversary review (trigger) | `packets/ADVERSARY_CARD01_AMENDMENT_B_REVIEW_2026-10-03.md` | `271ec099481ca35a57e4605b28abeff78d2660b6fd2657044666d45bcb728f01` | Verdict ADVISORY_FLAGS; this amendment pins AF-1, AF-2, AF-5, AF-6, AF-7, AF-10, AF-11 |
| Decision packet (at drafting) | `packets/CARD01_NEGLECTED_HYBRID_DECISION_PACKET_2026-09-24.md` | `c0c1aa66f104e3f102228a7a8e16f205977afbee63928f30a6954ec46707a82c` | Context; pointer to this amendment added separately under RULE-FROZEN-EDIT-PREV-BYTES-001 |

All seven hashes above were re-computed on the box at drafting time and match.

**What Amendment C supersedes:** exactly the sentences quoted as "old wording" in §C1 and §C2 below, and nothing else. It supersedes no other clause, file, amendment or acceptance. Amendments A and B, the base freeze and the Conductor ACCEPT of B remain in force except for those quoted sentences.

**What Amendment C leaves unchanged:** no number, threshold, universe, weight, knob, seed, resample count, solver range, iteration count, swing grid, entry gate, decision time, source, control, fee pin or rails pin changes, except as listed in §C1–§C7. In particular:
- the universe (92 races, `UNIVERSE_2026_HOUSE_FROZEN.json` `d8af7451…8ca6`) and the pre-commit (`2968f389…e77e`);
- the knob w ∈ {0.25, **0.5 headline**, 1.0} and the w = 0 control;
- the decision snapshot 2026-11-02T22:00Z;
- the headline statistic (paired Brier D at w = 0.5 over all admitted races);
- the bootstrap (state-cluster, 10,000 resamples, `random.Random(20261102)`, lo = sorted[250], hi = sorted[9749]);
- the Bernoulli-MLE recentering (clip [1e-4, 1−1e-4], bisection over [−10, 10], 60 iterations);
- the frozen swing grid S = {−0.50, −0.25, 0, +0.25, +0.50} logit;
- the entry gate (p_hybrid − price − fee − 2c > 3c);
- PASS (i)/(ii) and REJECT (a), (c), (d) wording;
- fee status: after-cost remains **BLOCKED** (Amendment B §(c)).

**No new variant, forecaster, weight, source, universe member or decision time is added.** Attempted-variant count: unchanged (0 new).

## Pin classification

| Pin | Flag | Kind | Effect on any PASS/REJECT outcome |
|---|---|---|---|
| C1 | AF-1 | **Rule change (gap closure)** | Assigns the previously unassigned case (recentered CI wholly above 0) to REJECT (b). Every case the old wording decided is decided identically |
| C2 | AF-6 | **Erratum** (text conformed to script 049368f9) | None. The code's behavior is unchanged; only the text now describes it correctly |
| C3 | AF-5 | **Reporting addition** | None (descriptive count) |
| C4 | AF-7 | **Reporting and labelling rule** (non-gating) | None on PASS/REJECT. Adds a pre-declared label, a freeze-at-snapshot obligation and a defect rule |
| C5 | AF-2 | **Rule addition (verdict scope)** | Defines the verdict while (c)/(d) are fee-BLOCKED. Caps claims at forecast-only. Does not change (a)/(b) |
| C6 | AF-10 | **Clarification** (fee-status table completeness) | None. No fee value is stated or admitted |
| C7 | AF-11 | **Reporting addition** | None |

---

## C1. AF-1: REJECT (b) restated as "recentered CI upper bound ≥ 0" (rule change, gap closure)

**Problem (Adversary AF-1):** PASS (ii) and REJECT (b) are not complements. If the recentered CI lies wholly **above** 0, neither fires; if the raw CI is also wholly below 0, REJECT (a) does not fire either, and the verdict falls to (c)/(d), which are fee-BLOCKED. That leaves an undefined verdict that could be interpreted after outcomes.

**Old wording (Amendment B §(a), "Decision use (unchanged logic)", second bullet), verbatim:**
> REJECT (b) holds iff the recentered CI includes 0.

**New wording (governs), verbatim:**
> REJECT (b) holds iff the upper bound of the recentered 95% CI of D_rc(0.5) is ≥ 0, i.e. hi = sorted[9749] of the 10,000 bootstrap values of D_rc(0.5) satisfies hi ≥ 0.

**Same reading applied to the base freeze (base file unchanged):** the base freeze states the same test twice with the same "includes 0" wording: §9 "Operationalized" item "(b) The recentered (common-factor) CI includes 0." and §6 "National common-factor diagnostic" step 3 "If the recentered CI includes 0, the verdict is "common-factor only"." Both are read with the new wording: the condition is "recentered CI upper bound ≥ 0", and the §6 step-3 label "common-factor only" is attached whenever REJECT (b) fires under the new wording.

**Resulting decision structure (no other change):**

| Test | Holds iff | Complement |
|---|---|---|
| PASS (i) | raw CI upper bound of D(0.5) < 0 | REJECT (a): raw CI upper bound ≥ 0 |
| PASS (ii) | recentered CI upper bound of D_rc(0.5) < 0 (Amendment B: "wholly below 0") | REJECT (b): recentered CI upper bound ≥ 0 (**this pin**) |

PASS (ii) and REJECT (b) are now exact complements, mirroring PASS (i) / REJECT (a).

**Why it is not outcome-chosen:** the new wording agrees with the old in every case the old wording decided (CI wholly below 0: neither old nor new fires; CI containing 0, including an endpoint exactly at 0: both fire). The only change is the previously unassigned wholly-above-0 case, which is assigned to REJECT: a hybrid that is worse than the market after recentering is not a pass. This follows the Adversary's proposed fix verbatim in substance.

## C2. AF-6: erratum on when `boundary` is set (erratum; matches script 049368f9)

**Old wording (Amendment B §(a), "Solver", second bullet), verbatim:**
> If every y is identical there is no interior root. δ is then set to the bound and `boundary = true` is reported.

**New wording (governs), verbatim:**
> δ is set to the bound (`boundary = true`) whenever g has no root in [−10, 10]. Formally, exactly as in script 049368f9: if g(−10) ≤ 0 then δ = −10 and `boundary = true`; otherwise, if g(10) ≥ 0 then δ = +10 and `boundary = true`; otherwise δ is found by the 60-iteration bisection and `boundary = false`. Every y identical is one such case (all y = 1 gives δ = +10; all y = 0 gives δ = −10). A mixed-y sample whose root lies beyond ±10 is another.

**Script citation** (`NH002H_AMENDMENT_B_national_miss.py`, sha256 `049368f9…81f2`, function `delta_mle`):
- line 53: `lo, hi = -10.0, 10.0`
- line 54: `if g(lo) <= 0: return lo, True`
- line 55: `if g(hi) >= 0: return hi, True`
- lines 56–60: the 60-iteration bisection, returning `(lo + hi) / 2, False`.

**Notes:**
- Because g is continuous and strictly decreasing, the formal condition differs from the plain-English "no root in [−10, 10]" only in the measure-zero case of a root exactly at ±10. There the script returns the bound with `boundary = true`, and the formal (script) condition governs.
- The script docstring (line 21: "If all y equal (no interior root) delta is set to the bound and flagged boundary=true.") carries the same narrower wording. The script is not edited. This erratum governs over the docstring.
- After this erratum the text and the pinned code agree on the boundary rule, so the Amendment B clause "If the script and this text ever disagree, this text governs" can no longer force new code after outcomes on this point.
- No behavior, number or output of script 049368f9 changes.

## C3. AF-5: report the count of bootstrap resamples that hit the boundary (reporting addition)

The scoring output must report, for each block (`all_admitted`, `split_KXHOUSERACE`, `split_LEGACY`) and for each arm w ∈ {0, 0.25, 0.5, 1.0}:
- **`n_boundary_resamples`**: the number of the 10,000 bootstrap resamples in which the δ re-estimated for that arm in that resample returned `boundary = true` (per §C2);
- alongside the existing point-estimate `boundary` flag, which stays as is.

This count is descriptive. It changes no CI, no statistic and no verdict. Script 049368f9 computes these flags inside `boot()` (via `stats()`, line 87) but discards them (lines 88–89 keep only D_raw and D_rc); Variants adds the count (see Implementation note). A block with n = 0 reports no count. If the count is missing from the output, that is a reporting defect; it does not alter the verdict.

The Adversary's optional `UNSTABLE_SPLIT` label (> 5% boundary resamples) is **not** adopted by this amendment.

## C4. AF-7: swing stress frozen at the decision snapshot, hash-anchored, with a pre-declared fragility label (reporting and labelling rule, non-gating)

**C4.1 Freeze at the snapshot.** The correlated-swing stress row (Amendment B §(a), "Correlated-swing stress row") is computed **at the 2026-11-02T22:00Z decision snapshot**, from decision-snapshot inputs only:
- p_0.5,i = 0.5·p_model,i + 0.5·p_market,i for each admitted race;
- the signal list selected by the frozen entry gate at that snapshot (race_id, side, price, fee status);
- the frozen grid S = {−0.50, −0.25, 0, +0.25, +0.50} plus the informational rows in §C4.4.

It uses no outcome. The Examiner emits it, computes its sha256, and sends the sha256 together with the UTC timestamp of hashing to the Archivist for the hash register, **before any race in the 92-race universe is called** (by any Designated Media Source or by a Kalshi determination). A stress row anchored after the first universe race call is not the frozen row; it may be shown only as labelled late and cannot clear the defect in §C4.3.

**C4.2 Pre-declared label `FRAGILE_NATIONAL_SWING`.** The label is set iff, in the frozen row, at s = −0.5 **or** s = +0.5, either:
- (a) `expected_gross` (summed over all gate-selected signals) ≤ 0; or
- (b) `share_sign_flips_vs_s0` ≥ 0.5 (at least half of the signals flip expected-gross sign versus s = 0, with sign defined as in script 049368f9 line 115: > 0 versus ≤ 0).

The label is placed next to the headline in any PASS-FORECAST write-up and next to any P&L figure. It is **non-gating**: it changes no PASS or REJECT. If neither condition holds at s = ±0.5, the status is `NOT_FRAGILE_AT_PM0.5`.

**C4.3 A missing row is a reporting defect, not a pass.**
- If the gate selected ≥ 1 signal and the frozen row is absent, unanchored before the first universe race call, or reads `NO_SIGNALS_SUPPLIED`, the stress status is `REPORTING_DEFECT` and the fragility status is `FRAGILE_NOT_CLEARED_REPORTING_DEFECT`. It may never be read as `NOT_FRAGILE_AT_PM0.5`. The defect is stated next to the headline.
- If the fee is BLOCKED at the snapshot, the signal set itself is BLOCKED (Amendment B §(c)). The row is then still emitted and anchored at the snapshot, with status `BLOCKED_FEE_UNVERIFIED` (signal set unavailable). It is not omitted. The fragility status is `NOT_EVALUATED_FEE_BLOCKED`, and under §C5 no P&L or tradeable claim is made.
- If the gate (with an admissible fee) selected zero signals, the row is emitted and anchored with status `NO_SIGNALS_SELECTED`, together with the anchored gate output showing zero. There is no P&L figure for the label to attach to.

**C4.4 ±1.0 logit rows: YES, reported, informational only.** It is declared now that rows at s = −1.0 and s = +1.0 logit are computed with the same formula and reported in the same frozen, anchored output. They are **informational only**: they **cannot trigger and cannot clear `FRAGILE_NATIONAL_SWING`**, they cannot PASS or REJECT anything, and they are not part of the frozen grid S, which is unchanged. Only the s = ±0.5 rows are read for the label.

**C4.5 Unchanged:** the stress row remains secondary and non-gating, as in Amendment B and the Conductor ACCEPT. The net column remains `BLOCKED_FEE_UNVERIFIED` until §C5's condition is lifted.

## C5. AF-2: forecast-only verdict while REJECT (c)/(d) cannot be evaluated (rule addition, verdict scope)

**Problem (Adversary AF-2):** REJECT (c) (taker P&L at ask, and under one-tick-worse stress) and REJECT (d) (top-1 share / drop-best-two) need the gate-selected signal set and fees. While the fee is BLOCKED (Amendment B §(c)), they have no input, and "any one means REJECT" has no rule for BLOCKED.

**Pin (governs):**
- While the fee is BLOCKED, REJECT (c) and REJECT (d) are reported as **`BLOCKED_FEE_UNVERIFIED`**. They count neither as fired nor as cleared.
- The verdict is then **`FORECAST_ONLY_FEE_BLOCKED`**, evaluated on REJECT (a)/(b) and PASS (i)/(ii) only:
  - `FORECAST_ONLY_FEE_BLOCKED: PASS-FORECAST` iff PASS (i) and PASS (ii) both hold (equivalently, neither REJECT (a) nor REJECT (b), per §C1);
  - `FORECAST_ONLY_FEE_BLOCKED: REJECT` iff REJECT (a) or REJECT (b) holds, with the firing item(s) named. A REJECT on (a)/(b) is final regardless of fee status.
- Under `FORECAST_ONLY_FEE_BLOCKED`, **no after-cost, net, executable, tradeable, capacity-as-profit or KEEP claim is allowed** in any write-up, summary or index entry. Gross or hypothetical P&L figures, if shown, carry `BLOCKED_FEE_UNVERIFIED`.
- "Fee BLOCKED" has the meaning already frozen in Amendment B §(c) and the Conductor ACCEPT: the Archivist fee/account manifest does not hold series-endpoint `fee_type`/`fee_multiplier` for `KXHOUSERACE` and every legacy series used, in an adopted entry. A draft or not-adopted entry (for example ADDENDUM_02, currently `DRAFT_NOT_ADOPTED`) is BLOCKED. Per Amendment B §(c), the entry must exist before any outcome; this amendment adds no new path to unblock (c)/(d).

## C6. AF-10: HOUSEVA2 added to the Card 01 fee-status table (clarification)

The Scout's derived `packets/scout_house_fee_2026-09-24/raw/kalshi/house_series_fee_fields.csv` lists 35 of the 36 Card 01 series and omits **HOUSEVA2** (VA-02; its raw series-list title is "VA-02", unlike the "House …" titles of the others). HOUSEVA2 is in the Amendment A mapping list and in the Amendment B Collector request. It is added here with the same status as every other series. **No fee value is stated, invented or admitted.** The Scout's file is not edited by this amendment.

| # | Series | Race(s) (Amendment A) | In Scout derived CSV | Card 01 fee status |
|---:|---|---|---|---|
| 1 | KXHOUSERACE | 58 races with an open `-D` contract | yes | BLOCKED / UNVERIFIED |
| 2 | HOUSEAZ1 | AZ-01 | yes | BLOCKED / UNVERIFIED |
| 3 | HOUSEAZ2 | AZ-02 | yes | BLOCKED / UNVERIFIED |
| 4 | HOUSEAZ6 | AZ-06 | yes | BLOCKED / UNVERIFIED |
| 5 | HOUSECA22 | CA-22 | yes | BLOCKED / UNVERIFIED |
| 6 | HOUSECO3 | CO-03 | yes | BLOCKED / UNVERIFIED |
| 7 | HOUSECO8 | CO-08 | yes | BLOCKED / UNVERIFIED |
| 8 | HOUSEFL13 | FL-13 | yes | BLOCKED / UNVERIFIED |
| 9 | HOUSEIA3 | IA-03 | yes | BLOCKED / UNVERIFIED |
| 10 | HOUSEME2 | ME-02 | yes | BLOCKED / UNVERIFIED |
| 11 | HOUSEMI4 | MI-04 | yes | BLOCKED / UNVERIFIED |
| 12 | HOUSEMI7 | MI-07 | yes | BLOCKED / UNVERIFIED |
| 13 | HOUSEPARTY-MI07 | MI-07 | yes | BLOCKED / UNVERIFIED |
| 14 | HOUSEMI10 | MI-10 | yes | BLOCKED / UNVERIFIED |
| 15 | HOUSEMT1 | MT-01 | yes | BLOCKED / UNVERIFIED |
| 16 | HOUSENC1 | NC-01 | yes | BLOCKED / UNVERIFIED |
| 17 | KXHOUSENC11 | NC-11 | yes | BLOCKED / UNVERIFIED |
| 18 | HOUSENE2 | NE-02 | yes | BLOCKED / UNVERIFIED |
| 19 | HOUSENH1 | NH-01 | yes | BLOCKED / UNVERIFIED |
| 20 | HOUSENJ7 | NJ-07 | yes | BLOCKED / UNVERIFIED |
| 21 | HOUSENY17 | NY-17 | yes | BLOCKED / UNVERIFIED |
| 22 | HOUSEOH9 | OH-09 | yes | BLOCKED / UNVERIFIED |
| 23 | HOUSEPA1 | PA-01 | yes | BLOCKED / UNVERIFIED |
| 24 | HOUSEPA7 | PA-07 | yes | BLOCKED / UNVERIFIED |
| 25 | HOUSEPA8 | PA-08 | yes | BLOCKED / UNVERIFIED |
| 26 | HOUSEPA10 | PA-10 | yes | BLOCKED / UNVERIFIED |
| 27 | KXHOUSETX9 | TX-09 | yes | BLOCKED / UNVERIFIED |
| 28 | HOUSETX15 | TX-15 | yes | BLOCKED / UNVERIFIED |
| 29 | KXHOUSETX32 | TX-32 | yes | BLOCKED / UNVERIFIED |
| 30 | HOUSETX34 | TX-34 | yes | BLOCKED / UNVERIFIED |
| 31 | KXHOUSETX35 | TX-35 | yes | BLOCKED / UNVERIFIED |
| 32 | HOUSEVA1 | VA-01 | yes | BLOCKED / UNVERIFIED |
| 33 | **HOUSEVA2** | **VA-02** | **no (added here)** | **BLOCKED / UNVERIFIED** |
| 34 | HOUSEWA3 | WA-03 | yes | BLOCKED / UNVERIFIED |
| 35 | HOUSEWI1 | WI-01 | yes | BLOCKED / UNVERIFIED |
| 36 | HOUSEWI3 | WI-03 | yes | BLOCKED / UNVERIFIED |

**Notes:**
- "BLOCKED / UNVERIFIED" means: no adopted Archivist manifest entry holds a series-endpoint `fee_type`/`fee_multiplier` for that series (Amendment B §(c)). Preliminary series-list fields remain "preliminary, not admitted", exactly as Amendment B §(c) already records for all 35 legacy series. That includes HOUSEVA2, whose raw series-list record (`card01_hybrid_forecast/collector_mapping_get_2026-09-24/raw/0003_20260925T000716.537Z_series_list_Elections_http200.body`) is consistent with the others; it is not a manifest entry.
- Whether series-*list* fields can satisfy Amendment B's "series endpoint" wording (Adversary AF-10, second part) is **not decided here**. Until the Conductor decides it, they do not.

## C7. AF-11: record the interpreter version and platform (reporting addition)

The scoring output JSON must record:
- `python_version`: the exact string `sys.version`;
- `platform`: the exact string `platform.platform()` (standard library `platform` module).

These are descriptive provenance. They change no computation. The Adversary verified determinism on CPython 3.13.5; that observation is not a pin of the version. If either field is missing, that is a reporting defect, not a change to the verdict.

---

## Not pinned by this amendment

AF-3 (ElectIndex capture stall; Collector/Archivist), AF-4 (`fee_source` field / Examiner attestation; Variants/Examiner), AF-8 (pin the upstream input builder and entry-gate code before the snapshot; Variants), AF-9 (card01 `MANIFEST.md` `16f96d3d` bytes missing; Archivist), the optional `UNSTABLE_SPLIT` label (AF-5), and the optional pre-named district-attribute split (§2 R4) are **not** addressed here. Their owners are as suggested in the Adversary review. Nothing here prevents them from being pinned separately before the snapshot.

## Validity condition

These pins exist to be fixed before any outcome. Amendment C takes effect only on a Conductor ACCEPT issued before 2026-11-02T22:00Z. If it is not accepted by then, it lapses and Amendment B governs unchanged.

## Implementation note for Variants (code follows only after Conductor ACCEPT)

- **Script 049368f9 is unchanged by this text** and stays pinned. Any implementation is a **new** file with its own sha256, committed and externally anchored before 2026-11-02T22:00Z (as Amendment B "Anchoring" requires for the pinned script). Deep Research writes no code.
- For every key that script 049368f9 already emits, the new code must reproduce 049368f9's values exactly on `amendment_b/SELFTEST_SYNTHETIC_input.json`. The Examiner checks this.
- Code is needed for: §C3 `n_boundary_resamples` (per block, per arm); §C7 `python_version` and `platform`; §C4 an **outcome-free** stress entry point.
- **§C4 entry point is required.** Script 049368f9 cannot emit the stress row before outcomes: `main()` passes only scored rows (lines 124–125: rows need non-null `y`) to `stress()` (line 134), and `stress()` looks signals up in those rows (lines 105 and 109). With every `y` null at the snapshot this raises `KeyError` (checked on a scratch byte copy with synthetic rows; no real input). The new entry point must compute the identical formula (`stress()`, lines 103–119: q = σ(logit(clip(p_0.5)) + s), gross, net or `BLOCKED_FEE_UNVERIFIED`, sign flips versus s = 0) from snapshot inputs without `y`. It adds the informational s = ±1.0 rows, labelled informational; emits the §C4 status vocabulary (`OK`, `BLOCKED_FEE_UNVERIFIED`, `NO_SIGNALS_SELECTED`, `REPORTING_DEFECT`) and the fragility status from §C4.2 using s = ±0.5 only; and never substitutes placeholder outcomes.
- **No code is needed for:** §C1 and §C5 (verdict rules applied by the Examiner; the script emits CIs, not verdicts); §C2 (erratum; the code already behaves this way); §C6 (documentation).

## p16 checklist delta (v1.2 §J; statuses remain null for the Examiner)

| # | Item | Change |
|---|---|---|
| 4 | Fees/fills | Fee-status table completed with HOUSEVA2 (C6); verdict capped at `FORECAST_ONLY_FEE_BLOCKED` while (c)/(d) are BLOCKED (C5) |
| 9 | Metrics/tests | REJECT (b) = recentered CI upper bound ≥ 0 (C1); boundary erratum (C2); `n_boundary_resamples` (C3); stress row frozen at snapshot with `FRAGILE_NATIONAL_SWING` and informational ±1.0 rows (C4); `python_version`/`platform` (C7) |
| 11 | Variant log | No new variants. Attempted-variant count unchanged (0 new) |

All other items are unchanged.

## Changelog

- **2026-10-03 17:12 ET (21:12Z):** Amendment C drafted and frozen by Deep Research in response to the Adversary review `271ec099…8f01` (ADVISORY_FLAGS). It pins AF-1, AF-6, AF-5, AF-7, AF-2, AF-10 and AF-11, is additive, edits no frozen freeze or amendment file and no code, and has status `AWAITING_CONDUCTOR_ACCEPT`.
