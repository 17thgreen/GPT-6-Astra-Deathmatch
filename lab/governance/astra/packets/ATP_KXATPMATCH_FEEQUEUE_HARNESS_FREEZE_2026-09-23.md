# ATP KXATPMATCH FEE+QUEUE HONESTY HARNESS — FREEZE KERNEL 2026-09-23 (ET)

**Owner:** R&D Variants (harness freeze / implement) → Simulator → Examiner  
**Status:** FROZEN — Conductor MAXIMIZE NEXT after CPI-FQ PR33 merge @`6e55a997`  
**Cite:** Scout cashcow optional watch `KXATPMATCH` (hunt sha256 `14c99ec8ea00bae507a21d0e6a1879fb94d32ef69ad4b5e3b40a9952821e5da7`; 48 markets / 24 events; fee `quadratic_with_maker_fees`); panel stub `2026-09-23.atp-kxatpmatch-v0` (sha256 `ed041c502d1f775d33c44bf900ac91b1339d99045bddd2052edd09a139ae2d3f`; admitted_at null; 6 events / 12 markets — authentic scout-subset); CPI-FQ invent fill-density / SoT just gated  
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`  
**Packet ID:** ATP-KXATPMATCH-FEEQUEUE-HARNESS  
**Feature family:** **ATP-FQ** (tennis match ML fee+queue honesty OOS) — ≠ CPI-FQ / NHL-FQ / L2-SF / EMPTY-OB / Cap-SR / Cap-SR-FX / MVE-FL / NCAAF-FQ / PROP-LQ / L2-CAT / SOT-ID / F1–F3  
**Nearest dead card:** Inventing depth/fills/fill-density OR inventing `occurrence_datetime`/SoT (CPI-FQ sparse/SoT refuse just gated). Also refuse: Lee-Ready; Q6-`000` retune; Cap-SR/QF/L2/EMPTY-OB/SOT-ID/L2-SF/NHL-FQ/CPI-FQ reopen; ATL@GB; live orders; ungating S1/S2/R2-P4.  
**Hard rules:** Measurement-only. GET-only. No Logan keys. No invent depth/fills/PnL/fill-density/SoT. No Lee-Ready. No `admit.py`. Does **not** ungate S1/S2/R2-P4. `results`/`pnl` null until Examiner after Clock admit.

## Why ATP-FQ (oldest leftover this slot)

Excluded (Conductor hard WAIT / closed reopen): S2/R2-P4 until C1 T−7d smoke; R3-P2/R3-P1 fee_cost truth (keys); S1 empty-events; Cap-SR/QF/L2/EMPTY-OB/SOT-ID/L2-SF/NHL-FQ/CPI-FQ reopen; Q6-`000` retune; ATL@GB; invent depth/fills/fill-density/occurrence/PnL; Lee-Ready; live orders.

C1–C5 numbered Scout TRY harnesses are closed (C4 CPI-FQ just merged). **ATP** is the oldest remaining Scout optional watch with a **non-empty** authentic hunt (48 active / 24 events) and GET-only maker-fee channel matching NFL/NCAAF/NHL game books — clean fee-honest tennis OOS without new credentials. KXFED still 429-blocked; KXETH15M sibling of C5 (prefer ATP first).

## Intent (one knob)

Holding **R1-P1 feebook** and **R1-P5 rails** fixed, wire a fee+queue honesty harness on `KXATPMATCH` panel stub (prefer `panel_admitted.json` when present): compare fee-honest reciprocal-book + rails freshness/queue labels on tennis YES/NO books vs the NFL `000` instrument **pointer only** (no signal port).

**One knob only:** analysis_slice ∈ {`maker_vs_taker_native`, `content_fresh_vs_stale_bin`} with feebook+rails fixed.

**Not arms:** inventing fills; `000` retune; Cap-SR; S2 start; CPI sparse invent.

## Pins

| Pin | Value |
|---|---|
| Scout hunt (parent seed) | sha256 `14c99ec8ea00bae507a21d0e6a1879fb94d32ef69ad4b5e3b40a9952821e5da7` · 48 markets / 24 events active |
| Panel stub | `lab/astra-capture/atp-kxatpmatch/panel_stub.json` · `2026-09-23.atp-kxatpmatch-v0` · sha256 `ed041c502d1f775d33c44bf900ac91b1339d99045bddd2052edd09a139ae2d3f` · `admitted_at` **null** · 6 events / 12 markets (authentic subset) |
| Fee (FIXED) | `kalshi_feebook_lab_20260922/` @`22371178cb2663250b4762f328069571c48cb551` |
| Rails (FIXED) | `kalshi_rails_lab_20260922/` @`6a28e0d6254327ea4e6451c781bec56215ac6cac` |
| Capture | GET-only public — no trading host; no Logan keys |
| Strategy | **None** — measurement contrast only |

## Arms

| Arm | Name | Slice |
|---|---|---|
| **ATPA0** | Native taker | Partition on native `taker_*` fields only; Lee-Ready **REFUSED** |
| **ATPA1** | Freshness bin | Rails `content_fresh_flag` / queue-attribution bins; no fee invent; no invent fills |

## Dead-card / live-pin overlap (named)

| Pin / card | Overlap | Handling |
|---|---|---|
| CPI-FQ sparse/SoT invent | Complementary refuse just gated | Name as nearest dead card; tennis OOS does not reopen CPI |
| NHL-FQ / NCAAF-FQ / C5 | Sibling FQ | New lab dir; share feebook/rails only |
| Q6-`000` / Q7 | Pointer only | No retune |
| Cap-SR / QF / L2-* / EMPTY-OB / SOT-ID / NHL-FQ / CPI-FQ | Closed | Do not reopen |
| S1 / S2 / R2-P4 | Hard WAIT | Stay queued |
| R3-P1 / R3-P2 | Keys WAIT | Stay deferred |

## Scorecard fields (null now)

`maker_vs_taker_roi_delta`, `fresh_vs_stale_gap`, `settled_join_n`, `n_books`, `results`, `pnl` — null until Clock admit + Examiner.

## Lab dir

`kalshi_atp_kxatpmatch_feequue_lab_20260923/` (do not mutate Q / Cap-SR / Cap-SR-FX / C1–C5 / S4 / S5 / NHL-FQ / CPI-FQ / L2-* / EMPTY-OB / SOT-ID / feebook / rails labs).

## Integrity (Clock gate)

Commit the **attached** Conductor-box freeze / scout hunt / panel stub bytes **verbatim**. Pin digests to `sha256sum`. **Refuse labeled recreations / inventing markets/depth/fills/SoT.**

## Merge gates

Units green; `results`/`pnl` null; Examiner stub_ready NOT_SCORED after merge.
