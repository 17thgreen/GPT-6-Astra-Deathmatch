# C3 KXHIGHNY BORDERING-STRIKE HARNESS — FREEZE KERNEL 2026-09-23 (ET)

**Owner:** R&D Variants (harness freeze / implement) → Simulator → Examiner  
**Status:** FROZEN — Conductor MAXIMIZE NEXT after C5 PR21 merge @`ee69245a`  
**Cite:** Conductor 2026-09-23 post-C5 merge; parent DR freeze `C3_KXHIGHNY_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md` (sha256 `0e79a0194e2371efae8d8cac0f4f2ec9ce4cf53f60dd870bae1a1ed7acff3604`); panel stub `2026-09-22.c3-kxhighny-v0`; C5 honesty harness pattern (PR21)  
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`  
**Packet ID:** C3-KXHIGHNY-BORDERING-STRIKE-HARNESS  
**Series:** `KXHIGHNY` primary · `KXHIGHCHI` multi-city proof  
**Hard rules:** Measurement-only **bordering-strike weather ladder** objects. GET-only public. No Logan keys. No live orders. No invented PnL. No GitHub weather-spread EV as Astra evidence (hypothesis only). No Q6-`000` retune. No QF reopen. No Cap-SR reopen. No C5 dual-steal. `results`/`pnl` null until Examiner opens after Clock admit.

---

## Intent (one knob)

Holding **R1-P1 feebook** + **R1-P5 rails** fixed, wire a bordering-strike harness that consumes the C3 panel stub (and later admitted panel) for daily max-temp threshold ladders — adjacent-strike mid/spread/depth raw API fields + fee/rails labels — **without** importing the GitHub weather-spread algo or claiming settlement-penalty EV.

**One knob only:** strike band ∈ {`near_extreme` (near 0/1), `mid_ladder`} with feebook+rails fixed.

**Not arms:** capital Cap-SR; Q6 signal; queue-fragility reopen; wholesale weather-spread MM port; R3-P3 strategy merge (panel material preference only).

---

## Pins

| Pin | Value |
|---|---|
| Parent freeze | `C3_KXHIGHNY_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md` sha256 `0e79a0194e2371efae8d8cac0f4f2ec9ce4cf53f60dd870bae1a1ed7acff3604` |
| Panel stub | `lab/astra-capture/c3-kxhighny/panel_stub.json` · panel_version `2026-09-22.c3-kxhighny-v0` · `admitted_at` **null** until Clock |
| Fee (FIXED) | `kalshi_feebook_lab_20260922/` @`22371178cb2663250b4762f328069571c48cb551` — forbid shadow `0.0175`/`0.07` |
| Rails (FIXED) | `kalshi_rails_lab_20260922/` @`6a28e0d6254327ea4e6451c781bec56215ac6cac` |
| Capture | GET-only public elections host — **no signed trading**; no Logan keys |
| Structure hyp | Bordering-strike ladder objects — **hypothesis only** |
| R3-P3 | Weather panel material preference only — kernels stay distinct |
| Adversary refuse | `C1_C3_C5_ADVERSARY_REFUSE_BIND_2026-09-22.md` — GitHub EV / invented arb / fee-blind completed-profit |

---

## Arms (strike-band knob only)

| Arm | Name | Strike band |
|---|---|---|
| **C3B0** | Near extreme | Threshold strikes near 0/1 (favorite/longshot ladder ends) |
| **C3B1** | Mid ladder | Mid-ladder bordering strikes (adjacent threshold pairs away from extremes) |

Both arms share identical fee+rails pins. Stub markets may skew to one band — units may use synthetic fixtures for the other band **without** writing non-null freeze scorecard fields.

---

## Scorecard fields (null now)

| Field | Meaning |
|---|---|
| `adjacent_spread_gap` | Spread gap between adjacent threshold strikes |
| `bordering_depth_imbalance` | Depth imbalance across bordering YES/NO books |
| `fee_delta_vs_inherited_model` | Feebook vs inherited fee assumption delta |
| `freshness_gap_sec` | Rails freshness gap on weather ladder samples |
| `multi_city_inventory_join` | NY vs CHI same-calendar presence flag (instrument; not arb PnL) |

All stay **null** in this freeze / EMPTY_RESULTS until Examiner after Clock admit.

---

## Lab deliverables (implement now)

New dir: `kalshi_c3_kxhighny_bordering_lab_20260923/` in Astra repo:

- `EXPERIMENT_SPEC.md` + `FROZEN_EXPERIMENT.json` (results/pnl null)  
- Harness loads panel stub; prefers `panel_admitted.json` when present  
- Bind feebook + rails imports; refuse fee literals  
- Unit tests: pin lock; stub load; C3B0/C3B1 schema; refuse GitHub-EV / live-order / invented-arb labels  
- First PR = **unit/instrument + stub join**; scorecard null  
- Do **not** mutate feebook / rails / capital / Cap-SR / C5 / Q / C1 labs

---

## Do-not-modify

1. No live orders / no Logan keys required.  
2. No GitHub weather-spread author PnL as Astra evidence.  
3. No invented cross-city arb / settlement-penalty EV.  
4. No Q6-`000` retune; no QF reopen; no Cap-SR reopen.  
5. No merge of C3 into R3-P3 as a strategy.  
6. No inventing OI/volume beyond Scout cite / live GET / stub bytes.  
7. `results`/`pnl` null until Examiner opens.

---

## Dead-card / orthogonality

- Sibling cash-cows: C1 empty-book (blocked); C5 honesty harness merged (do not reopen).  
- ≠ Cap-SR / F1–F3 / Q7 Arm B revival.

---

## Frozen-at

Desk 2026-09-23 ET. Conductor MAXIMIZE NEXT after C5 PR21 merge. Variants owner: R&D Variants.
