# REFINER PASS-2 FREEZE KERNEL — Q7-B-PORTFOLIO-RANK-SIZING — 2026-09-23 (ET)

**Status:** FROZEN_PRE_OUTCOME — Conductor `PASS2_SALVAGE_GO` · implement authorized under kick (results/pnl null)  
**Packet ID:** `Q7-B-REHAB-P2-PORTFOLIO-RANK-SIZING`  
**Parent corpse:** `CEM-ASTRA-20260922-001` · after Pass-1 KILL (`admission_cadence`)  
**Pass:** 2 of 3 · Policy `packets/refiner/REHAB_POLICY_3PASS_2026-09-23.md`  
**Owner chain:** Refiner (freeze) → Simulator → Examiner (Kalshi) → Adversary  
**Hard rules:** No invented fills/depth/fee_cost/queue/PnL. No live orders. No Q6-`000` silent retune. No post-outcome soften of 95%-of-D or B2>B0. Do not reopen Pass-1 cadence freeze. Do not multi-knob. Do not waive Clock/Examiner/Treasurer/Adversary.

---

## Question (new; not Pass-1 reopen)

Holding original-router route selection, pair-check ON, **continuous** new-exposure admission (Pass-1 cadence gate closed), and the same selection bars, does switching **only** baseline full-`wanted` sizing to **portfolio_rank capital-budget sizing** (Q6-`000` rank semantics, F/P/R off) close enough of the residual D−B gap for the challenger to clear **B2 > B0** and **B2 ≥ 95% of D** on every stress?

---

## One knob

| Field | Value |
|---|---|
| Knob | `portfolio_rank_sizing` |
| Baseline (B0 / Q7 Arm B) | `OriginalPairCheck` · `AdaptiveReplay(..., 'baseline')` · continuous refresh · full chosen-leg `wanted` |
| Rehab arm (B2) | Same as B0 **except** refresh uses allocation capital-budget sizing: rebalance via `portfolio_rank` → event budgets → fraction quantities by `allocations[event]/total` (AdaptiveReplay allocation branch); rank semantics = Q6-`000` (`Factors(False,False,False)` · neutral adjusted); offset legs independently protected |
| Not moved | `choose()` · combined-cost margin · order_size · cushion · fees · cohort · stresses · selection bars · **no** Pass-1 `admission_cadence` admission gate · no Q6-`000` source edit · F/P/R off |

**Orthogonality note:** Pass-1 changed *when* new paired exposure may be admitted on the baseline router. Pass-2 changes *how much* capital/size is allocated across events under continuous admission. Do not reintroduce RehabCadenceReplay / `admission_cadence=600` as part of B2.

---

## Arms (minimal)

| Arm | Role |
|---|---|
| **B0** | Pin: Q7 Arm B / Pass-1 B0 (original + check, baseline continuous) — positive control vs parent B ledgers where comparable |
| **B2** | Rehab: original + check + **portfolio_rank_sizing only** |
| **D** | Pin: Q7 Arm D / Q6-`000` + check — retention reference (do not edit `000` freeze) |

Stresses: same four (`q3300_d0.25`, `q3300_d5`, `q10000_d0.25`, `q10000_d5`). Account $5,000 · 31-game development cohort.

---

## Selection (frozen before outcomes — same engineering bars)

Apply only if all scenarios flat with non-null `completed_strategy_pnl`:

- Require **B2 > B0** on every stress
- Require D > 0 every stress and **B2 ≥ 95% of D** every stress
- Primary weeks: B2 week contributions > B0 on `q3300_d0.25`
- Inventory: B2 unhedged_contract_hours ≤ 1.25 × B0 every stress
- Else: `NO_NEW_SELECTION` · fallback shadow `000` · `live_promotion=false`

Softening the 95% bar or dropping B2>B0 is **out of scope** for this packet.

---

## Dead-card overlap

- Overlaps `CEM-ASTRA-20260922-001` (continued salvage under a **new** hypothesis).
- Does **not** reopen Pass-1 cadence freeze.
- Does not retune Q6-`000`.

---

## Lab deliverables (Simulator)

New lab dir (e.g. `nfl_q7_rehab_p2_rank_sizing_20260923/`):

- `EXPERIMENT_SPEC.md` + `FROZEN_EXPERIMENT.json` with `results`/`pnl` **null** at freeze
- Implement B2 sizing only; import Q6/Q7 modules read-only; hash-pin parent labs + Pass-1 dead-knob cite
- Positive controls: B0 matches Q7 Arm B / Pass-1 B0 ledger hashes where comparable; D matches Q7 Arm D / `000` pins vs `PARENT_Q7_BD_LEDGER_SOURCE_PINS`
- Unit tests for budget fractioning + refuse invent-PnL path; assert B2 has **no** Pass-1 admission_cadence gate
- First PR = freeze + units; no score until Examiner; no tape walk until Conductor/Refiner positive-control PASS if required

---

## Refuse

Invent PnL · live orders · multi-knob · reopen Pass-1 cadence as Pass-2 · Q6-`000` edit · post-peek bar soften · scoring own output · NOT_SCORED harness rehab
