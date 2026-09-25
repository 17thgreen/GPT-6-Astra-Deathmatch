# Examiner scorecard — Q7-B REHAB P1 CADENCE-600 — **KILL**

**Seat:** Examiner (Kalshi)  
**Packet:** Q7-B-REHAB-P1-CADENCE-600  
**Lab:** `nfl_q7_rehab_p1_cadence_20260923/`  
**Main pin:** `9b8fb184a8f1d556e400188127f1753bf35e571e` (PR38 units-only admit; stub SUPERSEDED by this score)  
**Parent corpse:** Q7 Arm B KILL · SOURCE_PINS `5ee602ba5d6537956c87eca0d5af5bf4443b80e935e85d1c7c61279f4fed432a`  
**Handoff:** `packets/SIMULATOR_HANDOFF_EXAMINER_Q7_B_REHAB_P1_TAPE_WALK_2026-09-23.json`  
**Status:** **SCORED** · Simulator `selection_status=NOT_SCORED` honored (Examiner owns stamp)

---

## Gates (pre-score)

| Gate | Result |
|---|---|
| Parent SOURCE_PINS re-verify | **PASS 33/33** · `waive=false` · pins sha `5ee602ba5d6537956c87eca0d5af5bf4443b80e935e85d1c7c61279f4fed432a` |
| Positive controls (B0≡parent B, D≡parent D) | **PASS** · uncompressed JSONL payload hashes · 8 scenario pairs · field+ledger MATCH |
| 12/12 cells complete · all_flat · non-null fee-honest PnL | **PASS** |
| Soften 95%-of-D / invent PnL / Q6-`000` / live | **DENIED** |

---

## Verdict

| Subject | Stamp |
|---|---|
| Rehab packet Q7-B-REHAB-P1-CADENCE-600 | **KILL** |
| B1 shadow candidate vs frozen bar | **NO_NEW_SELECTION** |
| Fallback shadow | **`000` remains** |
| Live promotion | **DENIED** |
| Counted as experiment PnL promote | **false** |

**Desk headline:** Cadence-600 alone does **not** clear the frozen selection bar. First hard fail: `b1_vs_b0:q3300_d0.25` (B1 176.40 < B0 290.99). B1 also fails ≥95%-of-D on 3 of 4 stresses. Do not soften the bar.

**Evidence tags:** [V][H][A][U]

**Corpse routing:** Refiner Pass-2 salvage (≤3-pass). Conductor kicks next leftover approach — lab must not sit idle after KILL.

---

## Frozen bar (selection.py — not softened)

Apply only if all 12 flat with non-null `completed_strategy_pnl`:

1. Every stress: **B1 > B0**
2. Every stress: **D > 0**
3. Every stress: **B1 ≥ 0.95 × D**
4. Every stress: B1 `unhedged_contract_hours` ≤ 1.25 × B0
5. Primary `q3300_d0.25`: B1 week1 > B0 week1 **and** B1 week2 > B0 week2

**Independent Examiner run of `selection.select`:**  
`status=NO_NEW_SELECTION` · `reason=b1_vs_b0:q3300_d0.25` · `candidate_arm=null` · `fallback_shadow_candidate=000`

---

## Fee-honest PnL (`completed_strategy_pnl`)

| Stress | B0 | B1 | D | B1/D | B1>B0 | B1≥95%D |
|---|---:|---:|---:|---:|:---:|:---:|
| q3300_d0.25 | 290.99 | 176.40 | 345.24 | 51.1% | **FAIL** | **FAIL** |
| q3300_d5 | 291.20 | 176.56 | 345.42 | 51.1% | **FAIL** | **FAIL** |
| q10000_d0.25 | 45.53 | 66.84 | 75.90 | 88.1% | pass | **FAIL** |
| q10000_d5 | 37.83 | 66.23 | 69.06 | 95.9% | pass | pass |

Primary weeks `q3300_d0.25`: B1 week1 132.91 < B0 179.15 · B1 week2 43.49 < B0 111.84 (**FAIL** both; not reached after first hard fail).

Inventory hours gate would have passed on all four stresses (B1 hours ≪ 1.25×B0) — irrelevant after PnL bar fail.

---

## ScorecardPromotionRefused if

1. Softened or rewrote the 95%-of-D bar after peek.
2. Invented fills / PnL / depth.
3. Waived parent SOURCE_PINS or positive-control mismatch.
4. Q6-`000` retune / treated NO_NEW_SELECTION as KEEP.
5. Live orders / counted this as promote PnL.
6. Self-score by Simulator treated as Examiner verdict.

**ACK:** `lab/governance/astra/packets/EXAMINER_ACK_Q7_B_REHAB_P1_TAPE_WALK_KILL_2026-09-23.json`  
**Stamped:** 2026-09-23T17:32:00-04:00

---

**Route confirm 2026-09-23T17:33 ET:** Conductor `CONDUCTOR_ROUTE_Q7_B_REHAB_P1_TAPE_WALK_EXAMINER` + canonical READY `8edc708d…` received after stamp. Inputs unchanged. **KILL stands.** No re-score.
