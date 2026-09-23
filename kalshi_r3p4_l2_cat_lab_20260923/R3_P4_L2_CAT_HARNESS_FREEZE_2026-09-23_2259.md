# R3-P4 L2 CATEGORY-SLICE HARNESS — FREEZE KERNEL 2026-09-23 (ET)

**Owner:** R&D Variants (harness freeze / implement) → Simulator → Examiner  
**Status:** FROZEN — Conductor MAXIMIZE NEXT after R2-P3 PR27 merge @`3b0d1429`  
**Cite:** Parent DR freeze `R3-P4_L2_SHAPE_LONGSHOT_DEPTH_FREEZE_KERNEL_2026-09-22.md` (sha256 `4a4e7cc61efcb436955c566edc7a2681603a014725bc79047f9d825392064528`); panel stub `2026-09-22.r3-p4-l2-shape-v0` (sha256 `7477e023ab70c59a6739650155ddb9d77077766e3afd80443e540d60b5a86cbb`; admitted_at null; 4 events / 6 markets; sports_n=4 NCAAF + nonsports_n=2 KXBTC; OB seed 6/6)  
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`  
**Packet ID:** R3-P4-L2-CAT-HARNESS  
**Feature family:** **L2-CAT** (L2 shape sports-vs-nonsports category slice) — ≠ Cap-SR / Cap-SR-FX / MVE-FL / NCAAF-FQ / PROP-LQ / F1–F3  
**Nearest dead card:** Invented depth (primary refuse). Also refuse: Lee-Ready, Q6-`000` retune, Cap-SR/QF reopen, ATL@GB. Parent intent = top-heavy book assumptions in queue/fill models; Q6-`000`/Q7 overlap **low/none**. Base L2 SF1/SF2 lab PR13 stays closed sibling (panel-join harness ≠ reopen PR13 units into PnL).  
**Hard rules:** Measurement-only. GET-only public L2. No Logan keys. No live orders. No invented depth/PnL. No Lee-Ready. No Q6-`000` retune. No QF/Cap-SR reopen. No `admit.py`. `results`/`pnl` null until Examiner after Clock admit.

## Why L2-CAT (oldest leftover this slot)

Excluded (Conductor hard WAIT / closed): S2+R2-P4 until C1 T−7d smoke PASS; R3-P2 until Logan demo/paper keys; S1 empty-events deferred; QF/Cap-SR/Cap-SR-FX reopen denied; Q6-`000` retune denied; ATL@GB denied; R3-P1 FIXTURE_GAP (auth `fee_cost` fills absent — needs credentials).

R3-P4 parent is FREEZE-ACCEPTED (Conductor R3 ADMIT NOW) with a **non-empty** stratified panel seed (6 markets, raw OB GETs on disk) and is GET-only without new Logan credentials. Parent already names sports vs non-sports slices; base SF1/SF2 lab (PR13) does not replace a one-knob **category** harness. Feature family is new (L2-CAT ≠ F1/F2/F3).

## Intent (one knob)

Holding **R1-P1 feebook** (reciprocal book) and **R1-P5 rails** (`content_fresh_flag`) fixed, wire an L2 shape harness that computes Dubach SF1/SF2 algebra on the R3-P4 panel stub (prefer `panel_admitted.json` when present), partitioned by **category slice**.

**One knob only:** category slice ∈ {`sports_only`, `nonsports_only`} with feebook+rails fixed. SF1 = median half-spread bps by mid decile; SF2 = L1/top-10 depth share + KL vs uniform 1/10.

**Not arms:** inventing depth; Lee-Ready; `000` allocator port; Cap-SR; expanding weather/Fed/GDP seeds past honest 429; mutating PR13 base lab in place (new lab dir).

## Pins

| Pin | Value |
|---|---|
| Parent freeze | sha256 `4a4e7cc61efcb436955c566edc7a2681603a014725bc79047f9d825392064528` |
| Panel stub | `lab/astra-capture/r3-p4-l2-shape/panel_stub.json` · `2026-09-22.r3-p4-l2-shape-v0` · sha256 `7477e023ab70c59a6739650155ddb9d77077766e3afd80443e540d60b5a86cbb` · `admitted_at` **null** · 4 events / 6 markets |
| Live OB seed (supporting) | `packets/r3_p4_l2_shape/live_get_2026-09-22/` (do not invent; use as fixture only) |
| Fee / book (FIXED) | `kalshi_feebook_lab_20260922/` @`22371178cb2663250b4762f328069571c48cb551` |
| Rails (FIXED) | `kalshi_rails_lab_20260922/` @`6a28e0d6254327ea4e6451c781bec56215ac6cac` |
| Capture | GET-only public orderbook — no trading host; no Logan keys |
| Strategy | **None** — quote-side microstructure only |

## Arms

| Arm | Name | Slice |
|---|---|---|
| **R3P4C0** | Sports only | SF1/SF2 on sports books (NCAAF seed); Lee-Ready **REFUSED** |
| **R3P4C1** | Non-sports only | SF1/SF2 on non-sports books (KXBTC seed); no fee invent; no invented depth |

## Dead-card / live-pin overlap (named)

| Pin / card | Overlap | Handling |
|---|---|---|
| Q6-`000` KEEP / Q7 Arm B | Low / none | Shape panel; no allocator port; do not reopen CEM-001 |
| Cap-SR / Cap-SR-FX / QF | Closed | Do not reopen |
| PROP-LQ / NCAAF-FQ / MVE-FL | Just-merged siblings; distinct Feature | Do not mutate those labs |
| R3-P3 FL bands | Complementary (price-outcome vs quote-side) | Share feebook/rails only |
| Base R3-P4 SF1/SF2 lab (PR13) | Complementary substrate | New lab dir; do not dual-edit PR13 lab |
| S2 / R2-P4 | Hard WAIT | Stay queued |
| R3-P1 / R3-P2 | Fixture gap / keys WAIT | Stay deferred |
| S1 empty-events | Deferred | Do not mutate |

## Scorecard fields (null now)

`sf1_median_half_spread_bps_by_mid_decile`, `sf2_l1_top10_depth_share`, `sf2_kl_vs_uniform_1_10`, `sports_vs_nonsports_sf_gap`, `n_books`, `n_snapshots`, `results`, `pnl` — null until Clock admit + Examiner.

## Lab dir

`kalshi_r3p4_l2_cat_lab_20260923/` (do not mutate Q / Cap-SR / Cap-SR-FX / C3 / C5 / R3-P3 / R3-P4 base / S4 / S5 / R2-P3 / feebook / rails labs).

## Integrity (Clock gate)

Commit the **attached** Conductor-box freeze / parent / panel bytes **verbatim**. Pin digests to `sha256sum` of those files. **Refuse labeled recreations / empty seeds.** Prefer `panel_admitted.json` when present; do not invent markets/depth/cohort beyond the authentic stub + recorded live_get fixtures.

## Merge gates

Units green; `results`/`pnl` null; Examiner stub_ready NOT_SCORED after merge.
