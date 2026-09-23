# S4 KXNCAAFGAME FEE+QUEUE HONESTY HARNESS — FREEZE KERNEL 2026-09-23 (ET)

**Owner:** R&D Variants (harness freeze / implement) → Simulator → Examiner  
**Status:** FROZEN — Conductor MAXIMIZE NEXT after S5 PR25 merge @`6626c689`  
**Cite:** Parent DR freeze `S4_KXNCAAFGAME_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md` (sha256 `9e6556c150c726b679ac8393f1f5338cf983489259b0f34cdedf221c030be795`); panel stub `2026-09-22.s4-kxncaafgame-v0` (sha256 `38167d11da5842bc4d39e6e7dcaab20a67294c735ba14d8bbeafde3154c6342a`; admitted_at null; 113 events)  
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`  
**Packet ID:** S4-KXNCAAFGAME-FEEQUEUE-HARNESS  
**Feature family:** **NCAAF-FQ** (college football fee+queue honesty OOS) — ≠ Cap-SR / Cap-SR-FX / MVE-FL / F1–F3  
**Nearest dead card:** Q7 Arm B KILL (CEM-001) — this packet does not reopen pair-check; C1 empty-book NOT_SCORED stays closed sibling.  
**Hard rules:** Measurement-only. GET-only. No Logan keys. No live orders. No invented PnL. No Q6-`000` retune. No QF reopen. No Cap-SR reopen. No `admit.py`. `results`/`pnl` null until Examiner after Clock admit.

## Why S4 (oldest leftover this slot)

Excluded: S5 MVE-FL just merged; Cap-SR/FX just merged; S1 empty-events deferred; S2+R2-P4 WAIT until C1 T−7d; R3-P2 keys HOLD; QF no reopen.

S4 is the oldest remaining FREEZE-ACCEPTED Scout TRY kernel with **non-empty** panel seed (113 events) that is GET-only football **OOS** vs NFL `000`. R2-P3 prop slate stays queued behind this implement.

## Intent (one knob)

Holding **R1-P1 feebook** and **R1-P5 rails** fixed, wire a fee+queue honesty harness on `KXNCAAFGAME` panel stub (prefer `panel_admitted.json` when present): compare fee-honest reciprocal-book + rails freshness/queue labels on college football YES/NO books vs the NFL `000` instrument **pointer only** (no signal port).

**One knob only:** analysis slice ∈ {`maker_vs_taker_native`, `content_fresh_vs_stale_bin`} with feebook+rails fixed.

**Not arms:** `000` retune; R1-P2 challenger bakeoff; Cap-SR; inventing fills when tape empty.

## Pins

| Pin | Value |
|---|---|
| Parent freeze | sha256 `9e6556c150c726b679ac8393f1f5338cf983489259b0f34cdedf221c030be795` |
| Panel stub | `lab/astra-capture/s4-kxncaafgame/panel_stub.json` · `2026-09-22.s4-kxncaafgame-v0` · sha256 `38167d11da5842bc4d39e6e7dcaab20a67294c735ba14d8bbeafde3154c6342a` · `admitted_at` **null** |
| Fee (FIXED) | `kalshi_feebook_lab_20260922/` @`22371178cb2663250b4762f328069571c48cb551` |
| Rails (FIXED) | `kalshi_rails_lab_20260922/` @`6a28e0d6254327ea4e6451c781bec56215ac6cac` |
| Capture | GET-only public — no trading host; no Logan keys |
| Strategy | **None** — measurement contrast only |

## Arms

| Arm | Name | Slice |
|---|---|---|
| **S4A0** | Native taker | Partition on native `taker_*` fields only; Lee-Ready **REFUSED** |
| **S4A1** | Freshness bin | Rails `content_fresh_flag` / queue-attribution bins; no fee invent |

## Scorecard fields (null now)

`maker_vs_taker_roi_delta`, `fresh_vs_stale_gap`, `settled_join_n`, `results`, `pnl` — null until Clock admit + Examiner.

## Lab dir

`kalshi_s4_ncaaf_feequue_lab_20260923/` (do not mutate Q / Cap-SR / Cap-SR-FX / C3 / C5 / R3-P3 / S5 / feebook / rails labs).

## Merge gates

Units green; `results`/`pnl` null; Examiner stub_ready NOT_SCORED after merge.
