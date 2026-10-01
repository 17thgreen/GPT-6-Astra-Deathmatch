# ETH KXETH15M FEE+QUEUE HONESTY HARNESS — FREEZE KERNEL 2026-09-23 (ET)

**Owner:** R&D Variants (harness freeze / implement) → Simulator → Examiner  
**Status:** FROZEN — Conductor MAXIMIZE NEXT after ATP-FQ PR34 merge @`438f4abf…`  
**Cite:** Scout cashcow optional watch `KXETH15M` (C5 sibling leftover; ATP done; KXFED 429; KXEPL empty); hunt sha256 `18f70001c8d68418d435e2016b756f90753e374a92d323f8e999f76215d9cf9c` (1 market / 1 event; series fee `quadratic`×1); panel stub `2026-09-23.eth-kxeth15m-v0` (sha256 `b3379783c84eaa910f6a57f5318b8536f21220cfeaf0f73e9ff73ee0f20dd90d`; admitted_at null; full tiny hunt — 1 event / 1 market); orthogonal pin `MAXIMIZE_PIN_2026-09-23_1427ET.md`  
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`  
**Packet ID:** ETH-KXETH15M-FEEQUEUE-HARNESS  
**Feature family:** **ETH-FQ** (KXETH15M fee+queue honesty OOS) — ≠ C5 KXBTC15M honesty / ATP-FQ / CPI-FQ / NHL-FQ / L2-SF / EMPTY-OB / Cap-SR / Cap-SR-FX / MVE-FL / NCAAF-FQ / PROP-LQ / L2-CAT / SOT-ID / F1–F3  
**Nearest dead card:** Inventing depth/fills/fill-density OR inventing SoT/`occurrence_datetime`. Also refuse: C5/ATP reopen; Lee-Ready; Q6-`000` retune; Cap-SR/QF/L2/EMPTY-OB/SOT-ID/L2-SF/NHL-FQ/CPI-FQ/ATP-FQ reopen; ATL@GB; live orders; ungating S1/S2/R2-P4; bacchus/kxeth15m strategy port.  
**Hard rules:** Measurement-only. GET-only. No Logan keys. No invent depth/fills/PnL/fill-density/SoT. No Lee-Ready. No `admit.py`. Does **not** ungate S1/S2/R2-P4. `results`/`pnl` null until Examiner after Clock admit. **NOT live crypto trading.**

## Why ETH-FQ (this slot)

Excluded (Conductor hard WAIT / closed reopen): S2/R2-P4 until C1 T−7d smoke; R3-P2/R3-P1 fee_cost truth (keys); S1 empty-events; Cap-SR/QF/L2/EMPTY-OB/SOT-ID/L2-SF/NHL-FQ/CPI-FQ/**ATP-FQ** reopen; Q6-`000` retune; ATL@GB; invent depth/fills/fill-density/occurrence/PnL; Lee-Ready; live orders.

C1–C5 numbered Scout TRY harnesses closed; ATP-FQ just merged PR34. **KXETH15M** is the remaining Scout optional-watch C5 sibling with a **non-empty** authentic hunt (1 active market / 1 event) and GET-only quadratic fee channel matching C5 BTC15M — clean fee-honest ETH 15m OOS without new credentials. KXFED still 429-blocked; KXEPL empty — do not invent.

## Intent (one knob)

Holding **R1-P1 feebook** and **R1-P5 rails** fixed, wire a fee+queue honesty harness on `KXETH15M` panel stub (prefer `panel_admitted.json` when present): compare fee-honest reciprocal-book + rails freshness/queue labels on ETH 15m YES/NO books vs the NFL `000` instrument **pointer only** (no signal port) and vs C5 BTC15m **sibling pattern only** (no C5 reopen / no bacchus port).

**One knob only:** analysis_slice ∈ {`maker_vs_taker_native`, `content_fresh_vs_stale_bin`} with feebook+rails fixed.

**Not arms:** inventing fills; `000` retune; Cap-SR; S2 start; C5 reopen; live crypto maker; bacchus/kxeth15m strategy port.

## Pins

| Pin | Value |
|---|---|
| Orthogonal slot | `MAXIMIZE_PIN_2026-09-23_1427ET.md` — active Feature ETH-FQ |
| Scout hunt (parent seed) | sha256 `18f70001c8d68418d435e2016b756f90753e374a92d323f8e999f76215d9cf9c` · 1 market / 1 event active · also `scout_cashcow_hunt_2026-09-22/scout_hunt_KXETH15M.json` |
| Panel stub | `lab/astra-capture/eth-kxeth15m/panel_stub.json` · `2026-09-23.eth-kxeth15m-v0` · sha256 `b3379783c84eaa910f6a57f5318b8536f21220cfeaf0f73e9ff73ee0f20dd90d` · `admitted_at` **null** · 1 event / 1 market (full tiny hunt) |
| Fee channel (live GET) | series `fee_type=quadratic` · `fee_multiplier=1` (GET `/series/KXETH15M`) |
| Fee (FIXED) | `kalshi_feebook_lab_20260922/` @`22371178cb2663250b4762f328069571c48cb551` |
| Rails (FIXED) | `kalshi_rails_lab_20260922/` @`6a28e0d6254327ea4e6451c781bec56215ac6cac` |
| Capture | GET-only public — no trading host; no Logan keys |
| Strategy | **None** — measurement contrast only; ≠ live crypto trading |

## Arms

| Arm | Name | Slice |
|---|---|---|
| **ETHA0** | Native taker | Partition on native `taker_*` fields only; Lee-Ready **REFUSED** |
| **ETHA1** | Freshness bin | Rails `content_fresh_flag` / queue-attribution bins; no fee invent; no invent fills |

## Dead-card / live-pin overlap (named)

| Pin / card | Overlap | Handling |
|---|---|---|
| Invent depth/fills/SoT | Nearest dead card | Name + refuse |
| C5 KXBTC15M honesty | Sibling 15m crypto | New lab dir; share feebook/rails only; no C5 reopen; no bacchus port |
| ATP-FQ | Sibling FQ just merged | Closed reopen; do not mutate ATP lab |
| Q6-`000` / Q7 | Pointer only | No retune |
| Cap-SR / QF / L2-* / EMPTY-OB / SOT-ID / NHL-FQ / CPI-FQ / ATP-FQ | Closed | Do not reopen |
| S1 / S2 / R2-P4 | Hard WAIT | Stay queued |
| R3-P1 / R3-P2 | Keys WAIT | Stay deferred |

## Scorecard fields (null now)

`maker_vs_taker_roi_delta`, `fresh_vs_stale_gap`, `settled_join_n`, `n_books`, `results`, `pnl` — null until Clock admit + Examiner.

## Lab dir

`kalshi_eth_kxeth15m_feequue_lab_20260923/` (do not mutate Q / Cap-SR / Cap-SR-FX / C1–C5 / S4 / S5 / NHL-FQ / CPI-FQ / ATP-FQ / L2-* / EMPTY-OB / SOT-ID / feebook / rails labs).

## Integrity (Clock gate)

Commit the **attached** Conductor-box freeze / scout hunt / panel stub bytes **verbatim**. Pin digests to `sha256sum`. **Refuse labeled recreations / inventing markets/depth/fills/SoT.**

## Merge gates

Units green; `results`/`pnl` null; Examiner stub_ready NOT_SCORED after merge.
