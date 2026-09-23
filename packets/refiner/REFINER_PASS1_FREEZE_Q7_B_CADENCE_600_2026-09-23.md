# REFINER PASS-1 FREEZE KERNEL — Q7-B-CADENCE-600 — 2026-09-23 (ET)

**Status:** ACCEPTED — Conductor GO 2026-09-23 ~14:51 ET · implement:true  
**Packet ID:** `Q7-B-REHAB-P1-CADENCE-600`  
**Parent corpse:** `CEM-ASTRA-20260922-001` · Q7 Arm B KILL  
**Pass:** 1 of 3 · Policy `packets/refiner/REHAB_POLICY_3PASS_2026-09-23.md`  
**Owner chain after GO:** Refiner (freeze) → Simulator → Examiner (Kalshi) → Adversary  
**Hard rules:** No invented fills/depth/fee_cost/queue/PnL. No live orders. No Q6-`000` silent retune. No post-outcome soften of 95%-of-D. Do not waive Clock/Examiner/Treasurer/Adversary.

---

## Question (new; not a silent Q7 reopen)

Holding original-router route selection and the chosen-pair combined-cost filter **ON**, does switching **only** new-paired-exposure admission from continuous AdaptiveReplay refresh to the Q6 allocator **600-second entry-budget cadence** close enough of the Q7 D−B gap for the challenger to clear the **same** pre-declared 95%-of-D retention bar vs KEEP'd `000` (Arm D reference behavior)?

---

## One knob

| Field | Value |
|---|---|
| Knob | `admission_cadence` |
| Baseline (corpse Arm B) | Continuous AdaptiveReplay refresh; pair check gates new exposure |
| Rehab arm | Same as Arm B **except** new paired exposure may be admitted only when `now >= next_allocation`; on admit attempt set `next_allocation = now + 600` |
| Not moved | `choose()` · combined-cost margin formula · order_size · cushion · fees · cohort · stresses · selection rule |

---

## Arms (minimal)

| Arm | Role |
|---|---|
| **B0** | Pin: Q7 Arm B behavior (original + check, continuous) — positive control vs Q7 artifacts |
| **B1** | Rehab: original + check + **600s cadence only** |
| **D** | Pin: Q7 Arm D / Q6-`000` + check — retention reference (do not edit `000` freeze) |

Stresses: same four as Q7 (`q3300_d0.25`, `q3300_d5`, `q10000_d0.25`, `q10000_d5`). Account $5,000 · 31-game development cohort.

---

## Selection (frozen before outcomes — same engineering bar)

Apply only if all scenarios flat with non-null `completed_strategy_pnl`:

- Require B1 > B0 on every stress (cadence must not destroy the check's prior lift vs continuous B)
- Require D > 0 every stress and **B1 ≥ 95% of D** every stress
- Primary weeks: B1 week contributions > B0 on `q3300_d0.25`
- Inventory: B1 unhedged_contract_hours ≤ 1.25 × B0 every stress
- Else: `NO_NEW_SELECTION` · fallback shadow `000` · `live_promotion=false`

Softening the 95% bar is **out of scope** for this packet.

---

## Dead-card overlap

- Overlaps `CEM-ASTRA-20260922-001` (salvage of Arm B candidacy under a **new** hypothesis).
- Does not reopen closed Q7 2×2 without the cadence knob.
- Does not retune Q6-`000`.

---

## Lab deliverables (Simulator after GO)

New lab dir under Astra science (name TBD by Simulator, e.g. `nfl_q7_rehab_p1_cadence_20260923/`):

- `EXPERIMENT_SPEC.md` + `FROZEN_EXPERIMENT.json` with `results`/`pnl` **null** at freeze
- Implement B1 cadence gate only; import Q6/Q7 modules read-only; hash-pin parent labs
- Positive controls: B0 matches Q7 Arm B ledger hashes where comparable; D matches Q7 Arm D / `000` pins
- Unit tests for cadence gate + refuse invent-PnL path
- First PR = freeze + units; no score until Examiner

---

## Refuse

Invent PnL · live orders · multi-knob (cadence+rank together) · Q6-`000` edit · post-peek bar soften · scoring own output · NOT_SCORED harness rehab
