# REFINER PASS-1 DIAGNOSIS — Q7 Arm B — 2026-09-23 (ET)

**Corpse:** Q7 Arm B · `CEM-ASTRA-20260922-001` · Examiner **KILL** as new shadow candidate  
**Budget:** pass **1 of 3**  
**Sources (no invented metrics):** `packets/Q7_EXAMINER_SCORECARD_2026-09-22.md` · `reports/RPT-Q7.md` · `nfl_paircheck_lab_20260922/results/paircheck_effects.json` (sha256 `5d87ea610f22482c980868d8a31a228ca1931368d9eeab73add4256d2e117fdf`) · cemetery addendum STAND on 95%-of-D

## What the KILL proved

1. Under the **pre-declared** selection rule, Arm B (original router · pair check ON) is **not** eligible to displace shadow `000`: `retains_95pct_of_D=false` on **every** stress (primary B/D = **0.843**; harsh queues 0.600 / 0.548).
2. Other candidate gates **passed**: `beats_original_all`, `improves_both_primary_weeks`, `inventory_within_limit`.
3. Architecture beyond the check dominates the gap to the KEEP'd reference: primary **D−B ≈ +$54.25** vs check-alone **C−A ≈ +$4.42** (from scored effects; not re-derived).
4. Softening / dropping the 95%-of-D bar **after** Q7 outcomes is **REFUSED** for this packet (Examiner + Conductor STAND). A tolerance change is a **new freeze**, not Pass-1 bar surgery.

## What the KILL did **not** prove

1. That the chosen-pair check is worthless — original_guard B−A and allocator_guard D−C are both positive on every stress.
2. That shadow `000` is optimal or should be retuned — KEEP is retention of the frozen incumbent, not a license to edit Q6-`000` timing/sizing/offset without a new experiment ID.
3. Annualized / holdout / live causal edge — HISTORICAL_DEV on the reused 31-game window only; `live_promotion=false`.
4. That every allocator rule must move at once — D−B is a **bundle** (cadence + ranking/sizing + offset path). Q7 did not attribute within that bundle.

## Dead-card overlap

| Card | Overlap |
|---|---|
| `CEM-ASTRA-20260922-001` Q7 Arm B | **This corpse** — salvage, not reopen of closed Q7 2×2 as-is |
| Q6-`000` / Arm D | KEEP'd reference — **do not** silent-retune; challenger must clear same 95%-of-D bar under a **new** freeze |
| Arm C ablation | Not a candidate; not rehabbed |
| Cap-SR / fee-queue harness stubs | Orthogonal maximize-forward measurement — **out of Refiner scope** (NOT_SCORED nulls) |

## Pass-1 knob (exactly one) — proposed, not yet frozen

**Knob name:** `admission_cadence`  
**From → to:** original AdaptiveReplay continuous refresh admission → **Q6 allocator 600-second entry-budget cadence** (`next_allocation = now + 600`)  
**Held fixed:** original_router `choose()` route selection · combined-cost filter ON (same margin expression) · order_size 250 · cushion `0.0002` · balance_precision · F/P/R off · fee model · 31-game cohort · 95%-of-D selection bar · no Q6-`000` edit  

**Why this knob (evidence-aligned):** Q7 closed the question “does the check alone explain Q6?” with **no**. The residual D−B gap is allocator architecture. Cadence is the **first isolable** architecture slice (factorial `next_allocation+=600`) that does not yet import `portfolio_rank` sizing — saving rank/sizing for Pass 2 if cadence alone fails attribution.

**Explicitly not Pass-1:** soften 95%-of-D · retune cushion/order_size · enable F/P/R · invent PnL · live orders · rehab of READY NOT_SCORED harnesses.

## Gate before outcomes

Freeze packet must land **before** any re-sim. Simulator → Examiner → Adversary only after freeze file exists with `results`/`pnl` null.
