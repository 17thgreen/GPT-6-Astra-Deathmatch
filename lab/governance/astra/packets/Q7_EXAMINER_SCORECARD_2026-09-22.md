# Examiner scorecard — Q7 Chosen-pair cost check

**Seat:** Examiner (Kalshi)  
**Packet:** Q7 / `nfl_paircheck_lab_20260922`  
**Experiment:** `Q7_CHOSEN_PAIR_COST_CHECK`  
**Scored:** 2026-09-22 (America/New_York)  
**Reviewer:** Examiner (Kalshi) — not dual-hat with Simulator/build  
**Authority:** Working Plan v0.1 · charter `lab/governance/astra/seats/EXAMINER_KALSHI.md`

---

## Verdict

| Subject | Stamp |
|---|---|
| Arm B as new shadow candidate | **KILL** |
| Q6 shadow incumbent label `000` (Arm D) | **KEEP** |
| Live promotion / orders | **DENIED** (not in scope; `live_promotion=false`) |
| Packet Q7 measurement | **CLOSED** (question answered under frozen rule) |

**Desk headline:** **KILL** Arm B candidacy · **KEEP** shadow `000` · no ITERATE on this 2×2 without a new freeze.

---

## Gates (must-pass before interpreting effects)

| Gate | Result | Source |
|---|---|---|
| Freeze before outcomes | PASS | `FROZEN_EXPERIMENT.json` (hypothesis + implementation pins; results null at freeze) |
| Grid complete | PASS | 16/16 scenarios · `experiment_summary.json` status `COMPLETE` · `failures={}` |
| All flat · non-null completed PnL | PASS | `all_flat=true` every arm · unresolved 0 |
| Positive controls A / D | PASS | `verification.json` status `VERIFIED` · `all_checks_passed=true` · `mismatches=[]` (A≡Q6 baseline fields+ledger hashes; D≡Q6-`000` fields+ledger hashes) |
| Fee-honest accounting | PASS | Inherited maker 0.0175 / taker 0.07 · rejection margins `counted_as_pnl=false` |
| Selection rule applied only if eligible | PASS | All 16 flat → rule applied |

`analysis_status.json` still reads `NOT_RUN_INPUTS_MISSING` — **stale relative to** `paircheck_effects.json` (`COMPLETE`) and `verification.json` (`VERIFIED`). Examiner scores from the verified complete artifacts, not the stale stub.

---

## Fee-honest completed_strategy_pnl (not a promotion claim)

Account $5,000 · 31 development games (W1+W2 pooled) · evidence tag `Q7_CHOSEN_PAIR_CHECK_REUSED_31_GAME_DEVELOPMENT_HYPOTHETICAL_EXECUTION`.

### Primary `q3300_d0.25`

| Arm | Role | Net PnL | %gain on $5k |
|---|---|---:|---:|
| A | original router · check off | +$201.52 | 4.03% |
| B | original router · check on | +$290.99 | 5.82% |
| C | Q6 `000` · check off (ablation) | +$205.94 | 4.12% |
| D | Q6 `000` · check on (reference) | +$345.24 | 6.90% |

Declared contrasts (primary): original_guard B−A = **+$89.47** · allocator_guard D−C = **+$139.30** · interaction = **+$49.83** · architecture_check_off C−A = **+$4.42** · architecture_check_on D−B = **+$54.25**.

### All stresses (B vs D retention)

| Stress | A | B | C | D | B/D | ≥95% of D? |
|---|---:|---:|---:|---:|---:|:---:|
| q3300_d0.25 | 201.52 | 290.99 | 205.94 | 345.24 | 0.843 | NO |
| q3300_d5 | 198.41 | 291.20 | 203.26 | 345.42 | 0.843 | NO |
| q10000_d0.25 | 10.35 | 45.53 | 14.29 | 75.90 | 0.600 | NO |
| q10000_d5 | 0.32 | 37.83 | 6.69 | 69.06 | 0.548 | NO |

Primary weeks (`q3300_d0.25`): B week1/week2 both strictly above A (PASS). Inventory: B unhedged_contract_hours ≤ 1.25×A every stress (PASS; ratios ≈ 0.99).

---

## Frozen selection rule (pre-declared)

Candidate Arm B requires all of: B>A every stress · D>0 every stress and B ≥ 95% of D every stress · primary weeks B>A · inventory hours gate.

| Condition | Result |
|---|---|
| `beats_original_all` | true |
| `retains_95pct_of_D` | **false** (hard fail) |
| `improves_both_primary_weeks` | true |
| `inventory_within_limit` | true |
| Selection status | **`NO_NEW_SELECTION`** |
| `live_promotion` | false |
| Fallback shadow | **`000`** |

Arm C is ablation only — not a candidate.

---

## Interpretation (deterministic contrasts only)

1. Chosen-pair check **helps** the original router (B−A > 0 all stresses) and **helps** the allocator (D−C > B−A; positive interaction).
2. Check alone does **not** explain the Q6 improvement: architecture_check_on (D−B ≈ +$30–$54) dwarfs architecture_check_off (C−A ≈ +$4–$6). Allocator scheduling/sizing rules matter beyond the filter.
3. Arm B fails the declared 95%-of-D engineering bar on every stress → **KILL** as new shadow candidate.
4. Positive-control match of Arm D to Q6 `000` supports **KEEP** of the existing shadow freeze. No displacement bakeoff triggered (no new challenger selected).

Extrapolation: projection on a fixed reused development window only — **not** annualized, **not** holdout, **not** live causal.

---

## Banned / refused

- No invented rates or annualized returns  
- No promote without freeze + artifacts (artifacts present; selection still denies B)  
- No live orders  
- No dual-hat with build seats  

---

## Next (Conductor)

1. Archivist: file this scorecard; update registry Q7 → **SCORED_KILL_B_KEEP_000**.  
2. Reporter: publish fee-honest card from this verdict (cite artifacts; no promotion language).  
3. Adversary: optional spot-check on fee blindness / capacity fantasy for `000` line.  
4. No Q7 ITERATE until a **new** frozen hypothesis (different question or cohort).  

---

## Artifact pins (sha256 of scored bytes)

```
{
  "paircheck_effects.json": "5d87ea610f22482c980868d8a31a228ca1931368d9eeab73add4256d2e117fdf",
  "verification.json": "eb1586bf13b1631951a4f177293350cb89fc7948a50fbb7044f4f05313ebc06f",
  "FROZEN_EXPERIMENT.json": "b0dd91699d2170e42c3a0ae9e27769a80f64f8121b116da030f253ac0d8a7f2b",
  "EXPERIMENT_SPEC.md": "cdfba7817a4a13c51b3aec3dc2256e7de1cd61386d9e1b359d85b2b65a78344f"
}
```

Lab: `lab/astra-science/nfl_paircheck_lab_20260922`  
Effects: `results/paircheck_effects.json`  
Verification: `results/verification.json`  
Summary: `results/experiment_summary.json` (status COMPLETE)

---

## Addendum — 95%-of-D bar (Conductor probe question)

**Stamp: STAND for this packet.** Do not amend Q7’s pre-declared selection rule after outcomes.

| Option | Ruling |
|---|---|
| Soften / drop 95%-of-D on Q7 after seeing B/D | **REFUSED** — freeze-before-outcome; moving the bar here would convert a fail into a pass |
| Maximize probe that revisits the tolerance | **Allowed only as a new freeze** (new packet ID, hypothesis before any new outcomes) — not an Examiner rewrite of Q7 |
| Pair-check as a mechanism | Not killed as worthless; Arm B candidacy failed the declared engineering bar. Check remains inside KEEP’d `000` (Arm D) |

Examiner does not dual-hat a maximize redesign. If Conductor commissions a new tolerance / capital-structure probe, score that packet after its own freeze + artifacts.

