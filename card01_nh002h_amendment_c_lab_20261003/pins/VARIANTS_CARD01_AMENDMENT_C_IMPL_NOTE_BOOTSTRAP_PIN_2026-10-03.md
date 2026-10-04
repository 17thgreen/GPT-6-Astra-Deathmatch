# IMPLEMENTATION NOTE: CARD01 NH-002-H (Amendment C), bootstrap draw-method and draw-order pin (pre-outcome, docs-only)

**Dated:** 2026-10-03 (ET). **Status:** `DRAFT, AWAITING_CONDUCTOR_ACCEPT` (not filed; the filer adds the filed timestamp).
**Kind:** **implementation note, no change to gates/thresholds/verdict rules/estimand.** It only resolves ambiguity. It changes no number, seed, resample count, percentile index, universe, weight, knob, solver, swing grid, entry gate, decision time, fee status or PASS/REJECT wording. It is not a re-freeze and not an amendment.
**Pre-outcome:** no 2026 House race has been decided. Nothing here was chosen from outcomes, prices or results. The only computation behind it is a scratch run of a byte copy of script 049368f9 on the **synthetic** `SELFTEST_SYNTHETIC_input.json` (§4). No real input was used.
**Validity:** takes effect only on a Conductor ACCEPT issued before **2026-11-02T22:00Z**. If it is not accepted by then, it lapses, and the frozen texts plus script 049368f9 govern as they stand.
**Evidence tags:** [V] verified on the box this session · [I] inferred · [A] assumption / choice made by this note · [U] unknown / provenance not on the box.

## 0. Lineage

| Artifact | Path (under `packets/`) | sha256 | Role |
|---|---|---|---|
| Amendment C (freeze governed) | `CARD01_HOUSE_ONLY_PROSPECTIVE_FREEZE_2026-09-24_AMENDMENT_C.md` | `cc75f09614ad285756fd7cb7f7a5c2ce4e711b5adb98102c2dd043ccfc1af0f0` | [V] re-hashed |
| Conductor ACCEPT of C | `CONDUCTOR_ACCEPT_CARD01_AMENDMENT_C_2026-10-03.json` | `2225c3fa0bea7c58cad59f52476f9fbe69e1d6fa813114a7557c748126dd2b1a` | [V] (ruling 5: AF-4/5/8/11 owner = Variants) |
| Amendment B | `CARD01_HOUSE_ONLY_PROSPECTIVE_FREEZE_2026-09-24_AMENDMENT_B.md` | `ee6af37cef95f1e468d28e5b06750caaca8b1706ec11ed5cf5cdce460524c2c6` | [V] |
| Conductor ACCEPT of B | `CONDUCTOR_ACCEPT_CARD01_NH002H_AMENDMENT_B_2026-09-24.json` | `74c5d49c0452ce97def7b36129ba362ebc4387627b93d5611bb67c5f8dfcbd23` | [V] |
| Base freeze | `CARD01_HOUSE_ONLY_PROSPECTIVE_FREEZE_2026-09-24.md` | `c31724463d81747702910a2d5296c2fc21d2a1dbc594727b26ac3d894b55ec59` | [V] |
| Pinned script (**unchanged**) | `card01_hybrid_forecast/amendment_b/NH002H_AMENDMENT_B_national_miss.py` | `049368f942741ff4a63acad328a49ff256252587d6c65f1e7e6d65d6101781f2` | [V] |
| Self-test input / output | `card01_hybrid_forecast/amendment_b/SELFTEST_SYNTHETIC_{input,output}.json` | `b16ba92b…cf65e` / `0e93e153…82f23` | [V] |
| Universe | `card01_hybrid_forecast/UNIVERSE_2026_HOUSE_FROZEN.json` | `d8af74515e449b151016105f956c5e54a4fb4eac3ec570364da58f8fe47d8ca6` | [V] |
| Adversary review of B | `ADVERSARY_CARD01_AMENDMENT_B_REVIEW_2026-10-03.md` | `271ec099481ca35a57e4605b28abeff78d2660b6fd2657044666d45bcb728f01` | [V] (AF-5, AF-8, AF-11) |
| **Rule source** | `CONDUCTOR_SCORE_ACCEPT_EXT_K2_PARTA_2026-10-03.md` | `6824793a44f5a10ee1d6e869e694d6681cfaba1681ff9b4bfb7cd0ed98242502` | [V] line 9: "STANDING RULE from today: every new freeze must pin the bootstrap draw method and order (RNG, seed, resampling unit, draw sequence)." |

The remedy for already-ACCEPTED freezes (an implementation note, ACCEPTed by the Conductor, not a re-freeze) comes from the Conductor via the delegation text; no on-box file states it [U]. The Archivist should file it.

## 1. What is already pinned (verbatim, with line numbers) [V]

Base freeze `c3172446`:
- L202: "State-cluster bootstrap, 10,000 resamples of states with replacement, seed 20261102. Report the 95% percentile CI."
- L206: "Leave-one-state-out range is reported."
- L225: "**Uncertainty is reported by state cluster, and the report must state that it is conditional on one election.**"

Amendment B `ee6af37c`:
- L20: "the bootstrap (state-cluster, 10,000 resamples, seed 20261102);"
- L52: "CI: the frozen state-cluster bootstrap (10,000 resamples, seed 20261102, random.Random)."
- L53: "**δ_f is re-estimated inside every resample, for every arm.**"
- L54: "Percentile interval: lo = sorted[250], hi = sorted[9749]."
- L61: pinned implementation = script `049368f9`; L64: "If the script and this text ever disagree, this text governs and the Examiner flags the discrepancy."
- L119: "Report n, states, D_raw, D_rc and both CIs (same bootstrap, with δ re-estimated within group)…"

Amendment C `cc75f096`:
- L26/L31: unchanged: "the bootstrap (state-cluster, 10,000 resamples, `random.Random(20261102)`, lo = sorted[250], hi = sorted[9749]);"
- L62: "…hi = sorted[9749] of the 10,000 bootstrap values of D_rc(0.5) satisfies hi ≥ 0."
- L99–L103 (§C3, AF-5): per block and per arm w ∈ {0, 0.25, 0.5, 1.0}, "`n_boundary_resamples`: the number of the 10,000 bootstrap resamples in which the δ re-estimated for that arm in that resample returned `boundary = true`"; "This count is descriptive. It changes no CI, no statistic and no verdict."; "A block with n = 0 reports no count."
- L105: `UNSTABLE_SPLIT` not adopted.
- L211: "For every key that script 049368f9 already emits, the new code must reproduce 049368f9's values exactly on `amendment_b/SELFTEST_SYNTHETIC_input.json`."

Script `049368f9`:
- L26–L28 (docstring): "CI: state-cluster bootstrap, 10000 resamples of states with replacement, random.Random(20261102); delta re-estimated inside every resample for every arm; 95% percentile interval lo = sorted[int(0.025*B)], hi = sorted[int(0.975*B) - 1]."
- L43–L44: `B_RESAMPLES = 10000`, `SEED = 20261102`.
- L81: `states = sorted({r["state"] for r in rows})`
- L82: `by = {s: [r for r in rows if r["state"] == s] for s in states}` (each state's rows in input order)
- L83: `rng = random.Random(SEED)` (inside `boot()`, so a fresh instance per block)
- L85–L86: `for _ in range(B_RESAMPLES): rs = [r for s in rng.choices(states, k=len(states)) for r in by[s]]`
- L87–L89: `st = stats(rs)`, then D_raw and D_rc are appended for every arm, all from the same `rs`
- L94: `xs.sort(); ci[w][k] = [xs[int(0.025 * B_RESAMPLES)], xs[int(0.975 * B_RESAMPLES) - 1]]` (= indices 250 and 9749 [V])
- L98: `if not rows: return {"n": 0}`; L124–L125 scored-row filter (input order kept); L131–L133 block order `all_admitted`, `split_KXHOUSERACE`, `split_LEGACY`.

## 2. Item-by-item status

| Item | Status | Where |
|---|---|---|
| RNG / library | **Pinned**: stdlib `random.Random` (Mersenne Twister), no numpy | B L52; C L31; script L37, L83 [V] |
| Seed | **Pinned**: 20261102 | base L202; B L20/L52; C L31; script L44 [V] |
| Number of resamples | **Pinned**: 10,000 | base L202; B L52; C L31; script L43 [V] |
| Resampling unit | **Pinned**: state cluster, with replacement | base L202; script L81–L86 [V] |
| Stratification | **Pinned (none)**: splits are separate bootstraps within group, not strata | B L119; script L29–L30, L131–L133 [V] |
| Draw primitive and sequence | **Pinned in code only**: `rng.choices(states, k=len(states))`, a fresh `random.Random(20261102)` per block | script L83, L86 [V]. The freeze texts do not name the primitive; script binds via B L61 and C L211 |
| Order of units before drawing | **AMBIGUOUS**: code sorts the `state` strings (L81), but **no text or pinned file fixes how `state` is spelled**. The input builder is unpinned (AF-8). A different spelling with the same partition reorders the list and changes every resample (§4) | script L81; Adversary AF-8 [V]; search of card01 texts for a `state` encoding found none [V] |
| Row order within a resample | **Partly pinned**: drawn-state order, then input order within state (L82, L86). Input row order is set by the unpinned builder | script L82/L86 [V] |
| One draw vector shared across arms / statistics | **Pinned**: one `rs` per resample feeds all four arms, D_raw and D_rc | script L87–L89; Adversary §1.2, L93 [V] |
| Per-draw statistic | **Pinned**: `stats(rs)`: δ re-estimated per arm by 60-step bisection on [−10, 10], D_raw and D_rc as means | B L41–L54; C §C2; script L50–L78 [V] |
| Percentile method | **Pinned**: order statistics of the ascending sort, `sorted[250]`, `sorted[9749]`, no interpolation | B L54; C L31/L62; script L94 [V] |
| Dropped / undefined draws | **Effectively pinned, but never stated in text**: no resample is dropped. Every drawn state has ≥ 1 row, so `stats()` is always defined; boundary resamples are kept with δ = ±10 | script L50–L60, L80–L95 [V by reading] |
| AF-5 `n_boundary_resamples` | **Pinned in meaning**, silent on mechanics (it must come from the same `rs` loop) | C L99–L103 [V] |
| Leave-one-state-out range | **SILENT on its mechanics**: statistic, arms, blocks, δ handling, and whether any CI is attached. It is also **not implemented** in 049368f9 and not in C's code list (C L212) | base L206 [V] |
| Interpreter / stream stability | Recorded, not pinned (C §C7). `choices` without weights is `population[floor(random() * n)]` on CPython 3.13.5 [V]. It is stable across recent CPython [I] | C L192–L196; Adversary AF-11 |

## 3. Pins (govern implementation; all [A] unless tagged otherwise)

**P1. Canonical `state` value (resolves the unit-order ambiguity).** In every scoring input row, `state` is the two-letter USPS postal code, uppercase ASCII, equal to the first two characters of the race's frozen universe code (`UNIVERSE_2026_HOUSE_FROZEN.json`, format `XX-NN`; all 92 entries match `^[A-Z]{2}-\d{2}$`, giving 28 distinct codes [V]). Examples: `AL-02 → "AL"`, `PA-07 → "PA"`. No full names, FIPS codes, lowercase, padding or whitespace. Precedent: the Amendment B exploration input `EXPLORATION_2024_house_primary_crosscheck_input.json` already uses this form (`2024-HOUSE-AZ-1 → "AZ"`) [V]. The unit list is then `sorted({r["state"] for r in rows})` exactly as script L81 does: Python default `str` ordering (code point), which for these codes is alphabetical.

**P2. Input row order.** The input builder emits `rows` in the order of `UNIVERSE_2026_HOUSE_FROZEN.json` `universe_2026_house` (ascending race code; that list is already sorted [V]). Rows that are unresolved or unscorable stay in place, and the script's filter (L124–L125) keeps the order of the rest. Within a resample, rows are concatenated in drawn-state order and, within a state, in that input order (L82, L86).

**P3. Draw procedure (restated from code so the text pins it; [V]).** For each block (`all_admitted`, then `split_KXHOUSERACE`, then `split_LEGACY`; any order gives identical output because each block re-seeds), with block rows `R`, where `n_R ≥ 1`:
1. `states = sorted({r["state"] for r in R})`; `S = len(states)`.
2. `rng = random.Random(20261102)`, a new instance for this block only. No other code draws from it, and no other consumer shares it.
3. For `b` in `0..9999`, in order: `drawn = rng.choices(states, k=S)`; `rs = [r for s in drawn for r in by_state[s]]`.
4. `st = stats(rs)` computes all arms w ∈ {0, 0.25, 0.5, 1.0} from the **same** `rs`. For each arm, δ_w is re-estimated (`delta_mle`) on `rs`, and D_raw(w), D_rc(w) and the `boundary` flag are taken from `st`.
5. No numpy and no vectorised substitute in this path. Any re-implementation must consume the identical stream: `random()` is called exactly `S` times per resample, in draw order, and in no other place.

**P4. Percentile (restated; [V]).** For each block, arm and statistic, sort the 10,000 values ascending with `list.sort()`. Then `lo = xs[250]` and `hi = xs[9749]`, i.e. `xs[int(0.025*10000)]` and `xs[int(0.975*10000) - 1]`. No interpolation and no `numpy.percentile`.

**P5. Dropped / undefined draws (restated; [V] by code reading).** No resample is ever dropped or skipped. A resample whose δ hits the bound (`boundary = true`, per C §C2) is **kept** with δ = ±10 and enters the CI unchanged. There is no `UNSTABLE_SPLIT` (C L105). A block with `n = 0` emits `{"n": 0}` and no CI (script L98). This note sets **no** verdict consequence for that case (see open question Q2).

**P6. AF-5 count (mechanics only).** `n_boundary_resamples[block][w]` = the number of `b` in P3 step 4 for which `st[str(w)]["boundary"] is True`. It is counted inside the **same** loop over the **same** `rs`, with no second RNG and no second pass. It is an integer in [0, 10000]. It is reported for all four arms, including the w = 0 market control, for every block with `n ≥ 1`. It is omitted for `n = 0` (C L103). Adding the counter must leave every 049368f9 key byte-identical on the self-test input (C L211).

**P7. Leave-one-state-out range (base L206; reporting-only).** Computed on the `all_admitted` block only. For each state `s` in `sorted(states)`, drop all rows of `s` (keeping the P2 order of the rest) and run `stats()` on the remainder, which **re-estimates δ per arm** as B L53 does for every subsample. Report, per arm, D_raw(w) and D_rc(w) for each `s`, plus their min and max ("range"), with the `boundary` flag per `s`. **No bootstrap and no CI** is computed for leave-one-out rows, and no RNG is used. This is **descriptive only and cannot fire PASS (i)/(ii) or REJECT (a)/(b)**. If a leave-one-out remainder is empty (impossible with ≥ 2 states), that row is reported as `UNDEFINED`, not imputed. The Examiner may strike P7 if the Conductor reads base L206 differently (Q3); doing so changes no verdict.

**P8. Provenance.** The scoring JSON records `bootstrap_sampler: "random.Random(20261102).choices(sorted_states, k=len(sorted_states)), fresh per block"`, `percentile_method: "order statistics xs[250], xs[9749] of 10000 ascending"`, `state_encoding: "USPS2 from universe code"`, and `rows_order: "UNIVERSE_2026_HOUSE_FROZEN order"`, next to the §C7 `python_version` and `platform`.

## 4. Why P1 matters (scratch evidence on synthetic data only; no number here is a result) [V]

On a byte copy of 049368f9 (sha re-verified) in `/workspace/scratch_bootpin/`, on the synthetic self-test input:
- The unmodified input reproduces `SELFTEST_SYNTHETIC_output.json` byte for byte (`0e93e153…`).
- **Relabelling the synthetic states `S<k>` → `S<kk>` (zero-padded; identical partition, only the sort order changes)** moves the headline w = 0.5 D_rc CI from [−0.0037968, 0.0127790] to [−0.0038706, 0.0129672], about 1.9e-4 at hi, and the LEGACY-split D_rc CI by about 4e-4 to 5e-4 at each end. That is larger than the K2 draw-order anomaly (5th decimal).
- Reversing input row order (same labels) gave byte-identical output on this input, so P2 is a determinism pin with low expected effect.

So the spelling of `state` alone can move `hi = sorted[9749]` across 0 in a marginal case. That decides REJECT (b) (C L62) and REJECT (a). Without P1, the verdict depends on an unpinned upstream choice.

## 5. Open questions for the Conductor (not resolved by this note)

- **Q1 (verdict-relevant, resolved here only if ACCEPTed):** P1 fixes the `state` encoding. If the Conductor prefers another encoding, it must be fixed **before** the snapshot, because the choice can move a CI endpoint across 0 (§4).
- **Q2 (internal gap, verdict rule):** if `all_admitted` has n = 0 or a single state, the freezes define no verdict. With n = 0 there is no CI. With one state, every resample is identical and the CI collapses to a point. Card01's vocabulary has no INCONCLUSIVE. An N6-style "undefined CI → INCONCLUSIVE" rule would be a **verdict-rule addition**, so this note does not make it. It needs a Conductor ruling or amendment. [I] Practically remote (58 KXHOUSERACE races at freeze).
- **Q3 (reporting):** base L206 (leave-one-state-out range) is not implemented in 049368f9 and is not in Amendment C's code list (C L212). P7 pins one reading. The Conductor may prefer another (e.g. headline arm only).
- **Q4 (owner):** P1/P2 bind the AF-8 input builder, which is still unpinned. Variants must pin and anchor the builder by sha before 2026-11-02T22:00Z (ACCEPT C ruling 1).

## 6. No change

No gate, threshold, verdict rule or estimand changes. Script 049368f9 is not edited. No new variant (attempted-variant count unchanged, 0 new). The p16 checklist statuses stay null for the Examiner.
