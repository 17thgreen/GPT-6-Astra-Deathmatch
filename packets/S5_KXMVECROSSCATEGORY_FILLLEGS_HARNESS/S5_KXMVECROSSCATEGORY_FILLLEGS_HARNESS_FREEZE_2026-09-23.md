# S5 KXMVECROSSCATEGORY FILL-VS-LEGS HARNESS — FREEZE KERNEL 2026-09-23 (ET)

**Owner:** R&D Variants (harness freeze / implement) → Simulator → Examiner  
**Status:** FROZEN — Conductor MAXIMIZE NEXT after Cap-SR effects PR24 merge @`79347f0e`  
**Cite:** Conductor 2026-09-23 leftover orthogonal; parent DR freeze `S5_KXMVECROSSCATEGORY_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md` (sha256 `a28932ba13b4913b69c48b73dde8ba066cebd212670d0b1cbb5ea8e93734b8ba`); panel stub `2026-09-22.s5-kxmvecrosscategory-v0` (5 markets / 21 events; legs join 5/5)  
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`  
**Packet ID:** S5-KXMVECROSSCATEGORY-FILLLEGS-HARNESS  
**Feature family:** **MVE-FL** (combo fill-vs-independent-legs) — ≠ Cap-SR / Cap-SR-FX / F1–F3  
**Hard rules:** Measurement-only fill-vs-legs. GET-only. No Logan keys (RFQ `/communications` **out**). **Not** R1-P4 strategy open. No live orders. No invented PnL. No Q6-`000` retune. No QF reopen. No Cap-SR reopen. No `admit.py`. `results`/`pnl` null until Examiner after Clock admit.

---

## Why S5 (oldest leftover this slot)

Excluded by Conductor: Cap-SR soft_policy / FX0–FX1 (just merged); S1 empty-events stub; S2+R2-P4 WAIT until C1 T−7d smoke; R3-P2 keys HOLD; QF no reopen.

S5 is the oldest remaining FREEZE-ACCEPTED cash-cow / Scout TRY kernel with **non-empty** panel seed (5 markets, legs join 5/5, combo fee pin) that is GET-only without Logan keys. S4 NCAAF and R2-P3 prop slate stay queued behind this implement.

---

## Intent (one knob)

Holding **R1-P1 feebook** with series override `quadratic_with_combo_maker_fees` and **R1-P5 rails** labels fixed, wire a fill-vs-legs harness that consumes the S5 panel stub (and later admitted panel): for each combo market with `mve_selected_legs`, compare fee-honest combo touch / print objects to the **product of independent-leg 1-minute TOB mids** (flip \(1-\mathrm{mid}\) for NO legs) — **without** claiming EV vs `000` or opening RFQ.

**One knob only:** leg mid source ∈ {`tob_1m`, `synthetic_leg_product`} with combo fee channel fixed.

**Not arms:** RFQ maker; R1-P4 strategy; Cap-SR; Q6 signal; QF; inventing fills when tape empty.

---

## Pins

| Pin | Value |
|---|---|
| Parent freeze | `S5_KXMVECROSSCATEGORY_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md` sha256 `a28932ba13b4913b69c48b73dde8ba066cebd212670d0b1cbb5ea8e93734b8ba` |
| Panel stub | `lab/astra-capture/s5-kxmvecrosscategory/panel_stub.json` · panel_version `2026-09-22.s5-kxmvecrosscategory-v0` · `admitted_at` **null** |
| Fee (FIXED) | `kalshi_feebook_lab_20260922/` @`22371178cb2663250b4762f328069571c48cb551` · series `quadratic_with_combo_maker_fees` / multiplier 1 |
| Rails (FIXED) | `kalshi_rails_lab_20260922/` @`6a28e0d6254327ea4e6451c781bec56215ac6cac` |
| Capture | GET-only public — **no** `/communications` RFQ; no Logan keys |
| Strategy | **None** — measurement vs `000` fee/queue honesty contrast only; no retune |

---

## Arms (leg-mid-source knob only)

| Arm | Name | Leg mid source |
|---|---|---|
| **S5L0** | TOB 1m | Independent-leg product from 1-minute TOB mids at fill minute (NO legs flip \(1-\mathrm{mid}\)) |
| **S5L1** | Synthetic leg product | Unit-only synthetic leg mid vector that forces a known product — schema/fixture only; not a panel invent |

Both arms share identical combo feebook pin. Empty historical trade tape on zero-vol samples is allowed (do not invent fills); units may use synthetic prints for schema only.

---

## Scorecard fields (null now)

| Field | Meaning |
|---|---|
| `fill_vs_legs_mid_gap` | Combo mid/print vs independent-leg product gap |
| `combo_fee_delta_vs_feebook` | Observed/applied combo fee vs R1-P1 series override |
| `legs_join_rate` | Fraction of markets with complete `mve_selected_legs` |
| `freshness_gap_sec` | Rails freshness gap on joined samples |

All stay **null** in this freeze / EMPTY_RESULTS until Examiner after Clock admit.

---

## Lab deliverables (implement now)

New dir: `kalshi_s5_mve_filllegs_lab_20260923/` in Astra repo:

- `EXPERIMENT_SPEC.md` + `FROZEN_EXPERIMENT.json` (results/pnl null)  
- Harness loads panel stub; prefers `panel_admitted.json` when present  
- Bind feebook (combo series override) + rails; refuse fee literals  
- Unit tests: pin lock; stub load (5 markets / legs join); S5L0/S5L1 schema; refuse RFQ / R1-P4-strategy / invented-fill labels  
- First PR = **unit/instrument + stub join**; scorecard null  
- Do **not** mutate feebook / rails / Cap-SR / Cap-SR-FX / C3 / C5 / R3-P3 / Q labs

---

## Do-not-modify

1. No live orders / no Logan keys / no RFQ path.  
2. No R1-P4 strategy open.  
3. No inventing fills or combo EV.  
4. No Q6-`000` retune; no QF reopen; no Cap-SR reopen.  
5. No `admit.py`.  
6. `results`/`pnl` null until Examiner opens.

---

## Dead-card / orthogonality (named)

| Card | Handling |
|---|---|
| Cap-SR / Cap-SR-FX (PR20/PR24) | **Orthogonal** — capital soft_policy ≠ combo fill-vs-legs |
| S1 empty-events | **Deferred** — not this slot |
| S2 + R2-P4 | **WAIT** until C1 T−7d smoke |
| R3-P2 queue_position_fp | **HOLD** (keys / demo) |
| QF reopen | **DENIED** |
| RFQ 401 / KXMVENFL empty | **Out of scope** |
| C1 empty-book / Q7 Arm B | Nearest blocked siblings — do not ungate |

---

## Frozen-at

Desk 2026-09-23 ET. Conductor MAXIMIZE NEXT after Cap-SR effects PR24. Variants owner: R&D Variants.
