# R3-P3 FL MAKER/TAKER BANDS HARNESS — FREEZE KERNEL 2026-09-23 (ET)

**Owner:** R&D Variants (harness freeze / implement) → Simulator → Examiner  
**Status:** FROZEN — Conductor MAXIMIZE NEXT after C3 PR22 merge @`63764496`  
**Cite:** Conductor 2026-09-23 scoring-path unblock; parent freeze `R3-P3_FL_MAKER_TAKER_BANDS_FREEZE_KERNEL_2026-09-22.md` (sha256 `0ed697149136acb3aa840aeeb79d11c8f6ef80f37ce4dd692a3cb690212206a7`); Collector panel stub `2026-09-22.r3-p3-fl-maker-taker-v0` (15 trades; settled N=0; bands pre-registered); C3 weather first preference  
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`  
**Packet ID:** R3-P3-FL-MAKER-TAKER-HARNESS  
**Hard rules:** Settled **public** tape only when admitted. GET-only. No Logan keys. **Refuse Lee-Ready.** Paper maker≥50¢ claim = hypothesis only. No live orders. No invented PnL. No Q6-`000` retune. No QF reopen. No Cap-SR reopen. Do not steal C3/C5 admit (Clock owns). `results`/`pnl` null until Examiner after Clock admit.

---

## Why R3-P3 (not C3/C5 panel-admit join this slot)

C3/C5 Clock joins still **ADMIT REFUSED** (settled join N=0 at last Clock stamp). Harnesses for C3/C5 already prefer `panel_admitted.json` when present — admit itself is Collector/Clock, not Variants.

R3-P3 stub already has **panel material**: 15 public trades with native `taker_*` fields, 10¢ bands pre-registered before outcome join, C3 weather-first inventory. This harness advances the settled-weather scoring path without Logan keys.

---

## Intent (one knob)

Holding **R1-P1 feebook** fixed and **Lee-Ready refused**, wire a maker/taker + favorite–longshot bands harness that consumes the R3-P3 panel stub (and later admitted panel): join public trades → pre-registered 10¢ bands → fee-honest schema objects — **without** computing Examiner ROI / MZ until admit + Examiner open.

**One knob only:** analysis slice ∈ {`maker_vs_taker`, `fl_bands_10c`} with feebook fixed, native taker fields required, bands registry frozen.

**Not arms:** Lee-Ready aggressor inference; capital Cap-SR; Q6 signal; QF reopen; paper EV import; inventing settled outcomes.

---

## Pins

| Pin | Value |
|---|---|
| Parent freeze | `R3-P3_FL_MAKER_TAKER_BANDS_FREEZE_KERNEL_2026-09-22.md` sha256 `0ed697149136acb3aa840aeeb79d11c8f6ef80f37ce4dd692a3cb690212206a7` |
| Panel stub | `lab/astra-capture/r3-p3-fl-maker-taker/panel_stub.json` · panel_version `2026-09-22.r3-p3-fl-maker-taker-v0` · `admitted_at` **null** |
| Bands registry | `lab/astra-capture/r3-p3-fl-maker-taker/bands_registry_10c.json` (pre-registered before outcome join) |
| Fee (FIXED) | `kalshi_feebook_lab_20260922/` @`22371178cb2663250b4762f328069571c48cb551` — ROI schema only; **null** until Examiner |
| Rails (optional freshness) | `kalshi_rails_lab_20260922/` @`6a28e0d6254327ea4e6451c781bec56215ac6cac` |
| C3 weather prefer | parent cite — kernels distinct from C3 bordering harness |
| Capture | GET-only public — no Logan keys |
| Lee-Ready | **REFUSED** — native `taker_outcome_side` / `taker_book_side` only |
| Adversary | `R3-P3_ADVERSARY_REFUSE_BIND_2026-09-22.md` — paper EV / invented ROI |

---

## Arms (slice knob only)

| Arm | Name | Slice |
|---|---|---|
| **R3P3A0** | Maker vs Taker | Partition stub trades by native taker fields; fee-schema objects per side — metrics null |
| **R3P3A1** | FL bands 10¢ | Assign trades to pre-registered 10¢ bands; fee-schema objects per band — metrics null |

Both arms share identical feebook pin + bands registry. Settled resolution join stays empty until Clock/Collector admit (honest N=0 on stub).

---

## Scorecard fields (null now)

| Field | Meaning |
|---|---|
| `mz_alpha` / `mz_psi` | Mincer–Zarnowitz event-clustered coeffs |
| `post_fee_roi_by_band` | R1-P1 post-fee ROI by 10¢ band |
| `maker_vs_taker_roi_delta` | Native-field maker vs taker ROI delta |
| `settled_join_n` | Count of settled resolved markets joined |

All stay **null** in this freeze / EMPTY_RESULTS until Examiner after Clock admit. Units assert schema, band registry lock, Lee-Ready refuse, pin locks only.

---

## Lab deliverables (implement now)

New dir: `kalshi_r3p3_fl_maker_taker_lab_20260923/` in Astra repo:

- `EXPERIMENT_SPEC.md` + `FROZEN_EXPERIMENT.json` (results/pnl null)  
- Harness loads panel stub + bands registry; prefers `panel_admitted.json` when present  
- Bind feebook import; refuse fee literals + Lee-Ready  
- Unit tests: pin lock; stub trade load (15); band assignment; R3P3A0/A1 schema; refuse paper-EV / invented-settlement labels  
- First PR = **unit/instrument + stub join**; scorecard null  
- Do **not** mutate feebook / rails / C3 / C5 / Cap-SR / Q labs

---

## Do-not-modify

1. No live orders / no Logan keys.  
2. No Lee-Ready / no inventing aggressor side.  
3. No inventing settled outcomes or ROI.  
4. No paper +2.6% / author PnL as Astra evidence.  
5. No Q6-`000` retune; no QF reopen; no Cap-SR reopen.  
6. No running `admit.py` from this lab (Collector/Clock).  
7. `results`/`pnl` null until Examiner opens.

---

## Dead-card / orthogonality

- C3/C5 admit still Clock-blocked (settled N=0) — this harness does not ungate their admit.  
- C3 bordering harness merged — distinct kernel; weather panel preference only.  
- ≠ Cap-SR / F1–F3 / Q7 Arm B.

---

## Frozen-at

Desk 2026-09-23 ET. Conductor MAXIMIZE NEXT after C3 PR22 merge. Variants owner: R&D Variants.
