# C4 KXCPI FEE+QUEUE HONESTY HARNESS — FREEZE KERNEL 2026-09-23 (ET)

**Owner:** R&D Variants (harness freeze / implement) → Simulator → Examiner  
**Status:** FROZEN — Conductor MAXIMIZE NEXT after NHL-FQ PR32 merge @`677d5d4f`  
**Cite:** Scout cashcow TRY **C4** `KXCPI` (hunt sha256 `6033907bb739bc00c41c796a3c1ed24553e0b7a44116ec3ea4bbaf39066bdcc8`; triage HOLD for sparse 24h / SoT gaps — this harness treats sparse tape as the **honesty stress**, not a reason to invent fills); triage sha256 `a4b4cb588c042342b8f5d936e98e0830c788f83f89d3a3517f83be77f4dea679`; panel stub `2026-09-23.c4-kxcpi-v0` (sha256 `b20b0cbee50c127d2e9bb2548b574b7d643cc708f54019d53bd91775f9762c13`; admitted_at null; 4 events / 44 markets — authentic full scout set; 21 markets missing `occurrence_datetime` kept honest); NHL-FQ just gated invent-depth/fills  
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`  
**Packet ID:** C4-KXCPI-FEEQUEUE-HARNESS  
**Feature family:** **CPI-FQ** (macro CPI threshold-ladder fee+queue honesty) — ≠ NHL-FQ / L2-SF / EMPTY-OB / Cap-SR / Cap-SR-FX / MVE-FL / NCAAF-FQ / PROP-LQ / L2-CAT / SOT-ID / F1–F3  
**Nearest dead card:** Inventing fill density on sparse 24h tape OR inventing `occurrence_datetime` / SoT for strikes that lack it. Also refuse: Lee-Ready; Q6-`000` retune; Cap-SR/QF/L2-*/EMPTY-OB/SOT-ID/L2-SF/NHL-FQ reopen; ATL@GB; live orders; ungating S1/S2/R2-P4.  
**Hard rules:** Measurement-only. GET-only. No Logan keys. No invent depth/fills/PnL/fill-density. No Lee-Ready. No `admit.py`. Does **not** ungate S1/S2/R2-P4. `results`/`pnl` null until Examiner after Clock admit.

## Why CPI-FQ (oldest leftover this slot)

Excluded (Conductor hard WAIT / closed): S2+R2-P4 until C1 T−7d smoke; R3-P2 keys; S1 empty-events; Cap-SR/QF/L2-*/EMPTY-OB/SOT-ID/L2-SF/NHL-FQ reopen; Q6-`000` retune; ATL@GB; live orders.

C1/C2/C3/C5 cash-cow harnesses landed. **C4 CPI** is the oldest remaining Scout TRY (triage HOLD for sparse 24h — we convert that into a measurement honesty stress, not a pad). Authentic hunt: 44 active markets / 4 events; fee `quadratic_with_maker_fees`. ATP remains optional watch behind C4.

## Intent (one knob)

Holding **R1-P1 feebook** and **R1-P5 rails** fixed, wire a fee+queue honesty harness on `KXCPI` panel stub (prefer `panel_admitted.json` when present): compare fee-honest reciprocal-book + rails freshness/queue labels on macro threshold ladders, with sparse-24h / missing-SoT treated as refuse bins — not fill invention.

**One knob only:** analysis_slice ∈ {`maker_vs_taker_native`, `sparse_24h_vs_fresh_bin`} with feebook+rails fixed.

**Not arms:** inventing fills; inventing SoT; `000` retune; Cap-SR; S2 start.

## Pins

| Pin | Value |
|---|---|
| Scout hunt (parent seed) | sha256 `6033907bb739bc00c41c796a3c1ed24553e0b7a44116ec3ea4bbaf39066bdcc8` · 44 markets / 4 events active |
| Panel stub | `lab/astra-capture/c4-kxcpi/panel_stub.json` · `2026-09-23.c4-kxcpi-v0` · sha256 `b20b0cbee50c127d2e9bb2548b574b7d643cc708f54019d53bd91775f9762c13` · `admitted_at` **null** · 4 events / 44 markets (authentic full scout) |
| Fee (FIXED) | `kalshi_feebook_lab_20260922/` @`22371178cb2663250b4762f328069571c48cb551` |
| Rails (FIXED) | `kalshi_rails_lab_20260922/` @`6a28e0d6254327ea4e6451c781bec56215ac6cac` |
| Capture | GET-only public — no trading host; no Logan keys |
| Strategy | **None** — measurement contrast only |

## Arms

| Arm | Name | Slice |
|---|---|---|
| **C4A0** | Native taker | Partition on native `taker_*` fields only; Lee-Ready **REFUSED** |
| **C4A1** | Sparse/fresh bin | Rails `content_fresh_flag` + sparse-24h / missing-`occurrence_datetime` refuse bins; **no invent fills** |

## Dead-card / live-pin overlap (named)

| Pin / card | Overlap | Handling |
|---|---|---|
| Triage C4 HOLD sparse 24h | Same series | Honesty stress, not invent density |
| NHL-FQ / NCAAF-FQ / C5 | Sibling FQ | New lab dir; share feebook/rails only |
| Q6-`000` / Q7 | None on signal | No retune |
| Cap-SR / QF / L2-* / EMPTY-OB / SOT-ID / NHL-FQ | Closed | Do not reopen |
| S1 / S2 / R2-P4 | Hard WAIT | Stay queued |

## Scorecard fields (null now)

`maker_vs_taker_roi_delta`, `sparse_vs_fresh_gap`, `missing_sot_n`, `settled_join_n`, `n_books`, `results`, `pnl` — null until Clock admit + Examiner.

## Lab dir

`kalshi_c4_kxcpi_feequue_lab_20260923/` (do not mutate Q / Cap-SR / Cap-SR-FX / C1–C3 / C5 / S4 / S5 / NHL-FQ / L2-* / EMPTY-OB / SOT-ID / feebook / rails labs).

## Integrity (Clock gate)

Commit the **attached** Conductor-box freeze / scout hunt / panel stub bytes **verbatim**. Pin digests to `sha256sum`. **Refuse labeled recreations / inventing markets/depth/fills/SoT.** Missing `occurrence_datetime` stays missing.

## Merge gates

Units green; `results`/`pnl` null; Examiner stub_ready NOT_SCORED after merge.
