# C1 KXUFCFIGHT EMPTY-ORDERBOOK REFUSE HARNESS — FREEZE KERNEL 2026-09-23 (ET)

**Owner:** R&D Variants (harness freeze / implement) → Simulator → Examiner  
**Status:** FROZEN — Conductor MAXIMIZE NEXT after SOT-ID PR29 merge @`6f1e22e1`  
**Cite:** Parent DR freeze `C1_KXUFCFIGHT_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md` (sha256 `a191c9b3f71030445d1d32684feb6dc1bf09abb7e09403d5dbdf1927eafc63c9`); panel admitted `2026-09-22.c1-kxufcfight-v0` (sha256 `24426d804c51bde23cf2557a11a8481a12026da10024094c4ae546d1f7d3956e`; admitted_at `2026-09-23T00:49:43Z`; 2 events / 4 markets); empty orderbook pin sha256 `e07d09f130e604a9e1acfc736fb57cbdfc33d8a5a253466a0cbd5c98cf6c9f74` (4 identical empty OB JSONs under `lab/astra-capture/c1-kxufcfight/orderbooks/`; PIN_SHA256 meta `241d745e6ddfb6cccdc8f123e4d57d627635065c3406df8f66d0d0d2e168f4ca`); Examiner ACK empty-books NOT_SCORED `8a71c67b2cfa59887f80e386defad4ba39f3807b54ce991f17e10f22be3b4388`; Adversary refuse-bind `0287c9d7a9012c3fea9ae99fb4801c3fd843866c580d31bd8a273aad67e92fe7`  
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`  
**Packet ID:** C1-EMPTY-OB-HARNESS  
**Feature family:** **EMPTY-OB** (empty L2 refuse / wait-fresh gate) — ≠ Cap-SR / Cap-SR-FX / MVE-FL / NCAAF-FQ / PROP-LQ / L2-CAT / SOT-ID / F1–F3  
**Nearest dead card:** Inventing depth or fills when books are empty (primary refuse). Also refuse: promoting C1 scorecard from empty pin alone; Lee-Ready invent; Q6-`000` retune; Cap-SR/QF/L2-CAT/PROP-LQ/SOT-ID reopen; ATL@GB; live orders.  
**Hard rules:** Measurement-only. GET-only / offline pinned empty books. No Logan keys. No invent depth/fills/PnL. No `admit.py`. No poll steal from ADMIT-1/PIT@CLE. Does **not** ungate S2/R2-P4. `results`/`pnl` null until Examiner after non-empty depth or explicit refuse stamp.

## Why EMPTY-OB (oldest leftover this slot)

Excluded (Conductor hard WAIT / closed): S2+R2-P4 until C1 T−7d smoke PASS; R3-P2 until Logan keys; S1 empty-events; R3-P1 FIXTURE_GAP (auth `fee_cost`); QF/Cap-SR/FX reopen; Q6-`000` retune; ATL@GB; L2-CAT/PROP-LQ/SOT-ID reopen.

C1 UFC panel is **admitted** but Examiner remains NOT_SCORED because PR19 pinned **empty** orderbooks (no depth). Parent C1 honesty bakeoff (PR18) does not replace a one-knob **empty-book refuse gate**. Feature family is new (EMPTY-OB ≠ F1/F2/F3). No new Logan credentials.

## Intent (one knob)

Holding **R1-P1 feebook** and **R1-P5 rails** fixed (import-only), wire a harness that loads the admitted C1 panel + authentic empty OB pin and applies a single empty-book policy before any fee/queue honesty score path.

**One knob only:** empty_book_gate ∈ {`refuse_scorecard`, `wait_fresh_depth`} with panel+empty pin fixed.

**Not arms:** inventing depth; inventing fills; scoring C1 from units alone; Cap-SR; ungating S2; retuning `000`.

## Pins

| Pin | Value |
|---|---|
| Parent freeze | sha256 `a191c9b3f71030445d1d32684feb6dc1bf09abb7e09403d5dbdf1927eafc63c9` |
| Panel admitted | sha256 `24426d804c51bde23cf2557a11a8481a12026da10024094c4ae546d1f7d3956e` · `2026-09-22.c1-kxufcfight-v0` · 2 events / 4 markets |
| Empty OB pin | sha256 `e07d09f130e604a9e1acfc736fb57cbdfc33d8a5a253466a0cbd5c98cf6c9f74` · four market files identical empty books |
| Pin meta | sha256 `241d745e6ddfb6cccdc8f123e4d57d627635065c3406df8f66d0d0d2e168f4ca` (`PIN_SHA256.json`) |
| Fee (FIXED import) | `kalshi_feebook_lab_20260922/` @`22371178cb2663250b4762f328069571c48cb551` |
| Rails (FIXED import) | `kalshi_rails_lab_20260922/` @`6a28e0d6254327ea4e6451c781bec56215ac6cac` |
| Strategy | **None** — refuse / wait gate only |

## Arms

| Arm | Name | Slice |
|---|---|---|
| **C1E0** | Refuse scorecard | Empty OB ⇒ `ScorecardPromotionRefused`; Lee-Ready **REFUSED**; no invent depth |
| **C1E1** | Wait fresh depth | Empty OB ⇒ wait/freshness bin only (rails `content_fresh_flag`); still null results/pnl; no invent fills |

## Dead-card / live-pin overlap (named)

| Pin / card | Overlap | Handling |
|---|---|---|
| C1 honesty bakeoff PR18 | Complementary substrate | New lab dir; do not reopen into PnL via empty pin |
| Q6-`000` / Q7 | Low / none on signal | Measurement refuse gate only |
| Cap-SR / QF / L2-CAT / PROP-LQ / SOT-ID | Closed / just merged | Do not reopen |
| S2 / R2-P4 | Hard WAIT | This packet does not ungate |
| R3-P1 / R3-P2 / S1 | WAIT / deferred | Stay deferred |

## Scorecard fields (null now)

`empty_book_n`, `scorecard_refuse_n`, `wait_fresh_depth_n`, `depth_present_n`, `results`, `pnl` — null until Examiner (and non-empty depth if scoring).

## Lab dir

`kalshi_c1_empty_ob_lab_20260923/` (do not mutate Q / Cap-SR / Cap-SR-FX / C3 / C5 / R3-P3 / R3-P4 / L2-CAT / SOT-ID / S4 / S5 / R2-P3 / C1 honesty lab / feebook / rails / ADMIT-1 recorder).

## Integrity (Clock gate)

Commit the **attached** Conductor-box freeze / parent / panel / empty OB / pin-meta bytes **verbatim**. Pin digests to `sha256sum` of those files. **Refuse labeled recreations / inventing non-empty books.**

## Merge gates

Units green; `results`/`pnl` null; Examiner stub_ready NOT_SCORED after merge.
