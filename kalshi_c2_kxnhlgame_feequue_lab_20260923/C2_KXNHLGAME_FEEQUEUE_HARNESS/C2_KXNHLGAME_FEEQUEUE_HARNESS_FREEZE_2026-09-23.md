# C2 KXNHLGAME FEE+QUEUE HONESTY HARNESS — FREEZE KERNEL 2026-09-23 (ET)

**Owner:** R&D Variants (harness freeze / implement) → Simulator → Examiner  
**Status:** FROZEN — Conductor MAXIMIZE NEXT after L2-SF PR31 merge @`ead2cb41`  
**Cite:** Scout cashcow TRY **C2** `KXNHLGAME` (hunt sha256 `1ab794ad688ba31e0178e78294dcdbe50cf2799a71f40245e5a04a80e9dd5762`; triage ADMIT-NEXT after S1 — S1 still empty-events WAIT but C2 is oldest remaining Scout TRY without new keys); Scout hunt doc sha256 `711a75d4a1cb3266de5fdb44bb27e08255b9df86527243edeedc927cc8df96f0`; triage sha256 `a4b4cb588c042342b8f5d936e98e0830c788f83f89d3a3517f83be77f4dea679`; panel stub `2026-09-23.c2-kxnhlgame-v0` (sha256 `60d183e7bdcf25adbc94eeeb3bb361b5232c19c0fe3e6a115f45ab3fcb100c79`; admitted_at null; 6 events / 12 markets — authentic market objects subset of scout hunt); L2-SF invent-depth / in-memory-SF-to-scorecard dead card just gated  
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`  
**Packet ID:** C2-KXNHLGAME-FEEQUEUE-HARNESS  
**Feature family:** **NHL-FQ** (hockey game ML fee+queue honesty OOS) — ≠ L2-SF / EMPTY-OB / Cap-SR / Cap-SR-FX / MVE-FL / NCAAF-FQ / PROP-LQ / L2-CAT / SOT-ID / F1–F3  
**Nearest dead card:** Inventing depth/fills OR writing in-memory SF algebra into scorecard without Clock admit (L2-SF just gated). Also refuse: Lee-Ready; Q6-`000` retune; Cap-SR/QF/L2-CAT/PROP-LQ/SOT-ID/EMPTY-OB/L2-SF reopen; claiming S1 units green; ungating S2/R2-P4; ATL@GB; live orders.  
**Hard rules:** Measurement-only. GET-only. No Logan keys. No invent depth/fills/PnL. No Lee-Ready. No `admit.py`. Does **not** ungate S1/S2/R2-P4. `results`/`pnl` null until Examiner after Clock admit.

## Why NHL-FQ (oldest leftover this slot)

Excluded (Conductor hard WAIT / closed): S2+R2-P4 until C1 T−7d smoke PASS; R3-P2 until Logan keys; S1 empty-events; R3-P1 FIXTURE_GAP; Cap-SR / Cap-SR-FX / QF / L2-CAT / PROP-LQ / SOT-ID / EMPTY-OB / L2-SF reopen; Q6-`000` retune; ATL@GB; live orders.

Capital-structure already Cap-SR/FX. R3-P4 category + SF algebra both landed. C1/C3/C5 cash-cow harnesses landed. **C2 NHL** is the oldest remaining Scout TRY (triage ADMIT-NEXT) with **non-empty** authentic hunt (66 active markets / 33 events) and GET-only fee channel `quadratic_with_maker_fees` matching NFL/NCAAF game books — clean fee-honest OOS vs `000` pointer without new credentials. C4 CPI remains HOLD (sparse 24h). ATP stays optional watch behind C2.

## Intent (one knob)

Holding **R1-P1 feebook** and **R1-P5 rails** fixed, wire a fee+queue honesty harness on `KXNHLGAME` panel stub (prefer `panel_admitted.json` when present): compare fee-honest reciprocal-book + rails freshness/queue labels on hockey YES/NO books vs the NFL `000` instrument **pointer only** (no signal port).

**One knob only:** analysis_slice ∈ {`maker_vs_taker_native`, `content_fresh_vs_stale_bin`} with feebook+rails fixed.

**Not arms:** `000` retune; Cap-SR; inventing fills; claiming S1 green; S2 start.

## Pins

| Pin | Value |
|---|---|
| Scout hunt (parent seed) | sha256 `1ab794ad688ba31e0178e78294dcdbe50cf2799a71f40245e5a04a80e9dd5762` · 66 markets / 33 events active |
| Panel stub | `lab/astra-capture/c2-kxnhlgame/panel_stub.json` · `2026-09-23.c2-kxnhlgame-v0` · sha256 `60d183e7bdcf25adbc94eeeb3bb361b5232c19c0fe3e6a115f45ab3fcb100c79` · `admitted_at` **null** · 6 events / 12 markets (authentic subset) |
| Fee (FIXED) | `kalshi_feebook_lab_20260922/` @`22371178cb2663250b4762f328069571c48cb551` |
| Rails (FIXED) | `kalshi_rails_lab_20260922/` @`6a28e0d6254327ea4e6451c781bec56215ac6cac` |
| Capture | GET-only public — no trading host; no Logan keys |
| Strategy | **None** — measurement contrast only |

## Arms

| Arm | Name | Slice |
|---|---|---|
| **C2A0** | Native taker | Partition on native `taker_*` fields only; Lee-Ready **REFUSED** |
| **C2A1** | Freshness bin | Rails `content_fresh_flag` / queue-attribution bins; no fee invent; no invent fills |

## Dead-card / live-pin overlap (named)

| Pin / card | Overlap | Handling |
|---|---|---|
| S1 KXMLBGAME | Triage said ADMIT-NEXT after S1 green | S1 still empty-events WAIT; this packet does **not** claim S1 green or steal S1 admit |
| S4 NCAAF-FQ | Sibling football OOS | New lab dir; share feebook/rails only |
| Q6-`000` / Q7 | Pointer only | No retune; no pair-check reopen |
| Cap-SR / QF / L2-* / EMPTY-OB / SOT-ID | Closed | Do not reopen |
| S2 / R2-P4 | Hard WAIT | Stay queued |

## Scorecard fields (null now)

`maker_vs_taker_roi_delta`, `fresh_vs_stale_gap`, `settled_join_n`, `n_books`, `results`, `pnl` — null until Clock admit + Examiner.

## Lab dir

`kalshi_c2_kxnhlgame_feequue_lab_20260923/` (do not mutate Q / Cap-SR / Cap-SR-FX / C1 / C3 / C5 / S4 / S5 / R2-P3 / L2-* / EMPTY-OB / SOT-ID / feebook / rails labs).

## Integrity (Clock gate)

Commit the **attached** Conductor-box freeze / scout hunt / panel stub bytes **verbatim**. Pin digests to `sha256sum`. **Refuse labeled recreations / inventing markets/depth/fills.** Panel markets must remain authentic Kalshi objects from the scout hunt subset.

## Merge gates

Units green; `results`/`pnl` null; Examiner stub_ready NOT_SCORED after merge.
