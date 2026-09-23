# REFINER PASS-2 DIAGNOSIS — Q7 Arm B — 2026-09-23 (ET)

**Corpse:** Q7 Arm B · `CEM-ASTRA-20260922-001`  
**Budget:** pass **2 of 3** (Pass 1 KILL stamped)  
**Sources (no invented metrics):** `packets/EXAMINER_ACK_Q7_B_REHAB_P1_TAPE_WALK_KILL_2026-09-23.json` · `packets/EXAMINER_SCORECARD_Q7_B_REHAB_P1_TAPE_WALK_KILL_2026-09-23.md` · `nfl_q7_rehab_p1_cadence_20260923/results/experiment_summary.json` · `packets/refiner/REFINER_PASS1_DIAGNOSIS_Q7_ARM_B_2026-09-23.md` · parent `paircheck_policy.py` / Q6 `adaptive_policy.py` / `factorial_policy.py`

## What Pass-1 KILL proved

1. Under the **same** pre-declared selection rule, **cadence-600 alone** on original+check does **not** salvage Arm B: first hard fail `b1_vs_b0:q3300_d0.25` (Examiner KILL · `NO_NEW_SELECTION`).
2. On primary stresses, B1 **destroyed** prior check lift vs continuous B0 (q3300_d0.25: B0≈291 · B1≈176 · D≈345; B1≈51% of D). Cadence-600 is not a free add-on on this line.
3. On harsh queues, B1 beat B0 but still failed 95%-of-D on `q10000_d0.25` (≈88%); only `q10000_d5` cleared both B1>B0 and ≥95%-of-D.
4. Softening 95%-of-D / B1>B0 after outcomes remains **REFUSED**. Pass-1 `admission_cadence` freeze is **dead** — do not reopen it as Pass-2.

## What Pass-1 KILL did **not** prove

1. That the chosen-pair check is worthless — Q7 original_guard / allocator_guard lifts still stand; Pass-1 did not re-open that question.
2. That Q6-`000` should be retuned — fallback shadow stays `000`; KEEP is retention, not edit license.
3. Attribution of the residual **D−B architecture bundle** beyond cadence — Pass-1 diagnosis reserved **`portfolio_rank` / capital-budget sizing** as the next isolable slice. Cadence alone failed; that reservation is now due.
4. Live / holdout / causal claims — HISTORICAL_DEV only; `live_promotion=false`.

## Dead-card / dead-knob

| Item | Status |
|---|---|
| Pass-1 `admission_cadence` (continuous→600 on baseline) | **KILL** — closed; not Pass-2 |
| Q6-`000` / Arm D | KEEP'd reference — no silent retune |
| Soften 95%-of-D or drop B1>B0 | Out of scope |
| Cap-SR / fee-queue NOT_SCORED harnesses | Out of Refiner scope |

## Pass-2 knob (exactly one) — proposed for freeze

**Knob name:** `portfolio_rank_sizing`  
**From → to:** original-router **baseline** refresh (full `wanted` on chosen legs · continuous admission · pair check ON) → same original router + pair check ON + **continuous admission** (Pass-1 cadence gate **not** reintroduced), but size chosen legs via the AdaptiveReplay **`allocation`** capital-budget path: `portfolio_rank` → event cash budgets → fraction `wanted` by `allocations[event]/total`, with offset inventory independently protected (same branch as `adaptive_policy.AdaptiveReplay.refresh` when `experiment=='allocation'`). Rank function for budgeting must match Q6 label **`000`** semantics (F/P/R **off**; neutral `adjusted=1` as in `FactorialReplay` with `Factors(False,False,False)`), without editing the frozen `000` tree.  
**Held fixed:** `choose()` · combined-cost filter ON · order_size 250 · cushion · fees · cohort · stresses · **same** 95%-of-D and B2>B0 bars · **no** Pass-1 `admission_cadence` gate · **no** Q6-`000` edit · F/P/R stay off  

**Why this knob:** Pass-1 closed “does 600s admission cadence alone close D−B?” with **no**. Residual gap is still allocator architecture. Next isolable slice reserved in Pass-1 diagnosis is portfolio capital budgeting / sizing — orthogonal to the dead cadence gate.

**Explicitly not Pass-2:** reopen cadence freeze · soften bars · multi-knob (cadence+rank together as two intentional changes) · retune cushion/order_size · enable F/P/R · invent PnL · live orders.

## Gate before outcomes

Freeze packet must land with `results`/`pnl` **null** before any re-sim. Simulator → Examiner → Adversary only after freeze exists.
