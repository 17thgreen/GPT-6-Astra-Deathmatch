# R3-P4 L2 SF1/SF2 ALGEBRA-OBJECT HARNESS — FREEZE KERNEL 2026-09-23 (ET)

**Owner:** R&D Variants (harness freeze / implement) → Simulator → Examiner  
**Status:** FROZEN — Conductor MAXIMIZE NEXT after EMPTY-OB PR30 merge @`d7b93595`  
**Cite:** Parent DR freeze `R3-P4_L2_SHAPE_LONGSHOT_DEPTH_FREEZE_KERNEL_2026-09-22.md` (sha256 `4a4e7cc61efcb436955c566edc7a2681603a014725bc79047f9d825392064528`); panel stub `2026-09-22.r3-p4-l2-shape-v0` (sha256 `7477e023ab70c59a6739650155ddb9d77077766e3afd80443e540d60b5a86cbb`; admitted_at null; 4 events / 6 markets; sports_n=4 NCAAF + nonsports_n=2 KXBTC; OB seed 6/6 with non-empty yes_dollars/no_dollars); L2-CAT PR28 sibling (category slice — **do not reopen**); EMPTY-OB invent-depth refuse just gated  
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`  
**Packet ID:** R3-P4-L2-SF-HARNESS  
**Feature family:** **L2-SF** (L2 shape SF1 vs SF2 algebra object) — ≠ EMPTY-OB / Cap-SR / Cap-SR-FX / MVE-FL / NCAAF-FQ / PROP-LQ / L2-CAT / SOT-ID / F1–F3  
**Nearest dead card:** Inventing depth or fills (EMPTY-OB invent-depth refuse just gated). Also refuse: Lee-Ready; dual-edit PR13 base L2 lab into PnL; L2-CAT reopen; Cap-SR/QF/PROP-LQ/SOT-ID/EMPTY-OB reopen; Q6-`000` retune; ATL@GB; live orders.  
**Hard rules:** Measurement-only. GET-only public L2. No Logan keys. No invent depth/fills/PnL. No Lee-Ready. No `admit.py`. No poll steal from ADMIT-1. Does **not** ungate S2/R2-P4. `results`/`pnl` null until Examiner after Clock admit.

## Why L2-SF (oldest leftover this slot)

Excluded (Conductor hard WAIT / closed): S2+R2-P4 until C1 T−7d smoke PASS; R3-P2 until Logan keys; S1 empty-events; R3-P1 FIXTURE_GAP (auth `fee_cost`); Cap-SR / Cap-SR-FX / QF / L2-CAT / PROP-LQ / SOT-ID / EMPTY-OB reopen; Q6-`000` retune; ATL@GB; live orders.

Capital-structure probe already landed as Cap-SR / Cap-SR-FX (PR5→PR20→PR24) — **not still open**.

R3-P4 parent is FREEZE-ACCEPTED with a **non-empty** stratified panel + authentic OB fixtures. L2-CAT (PR28) already owns the **category_slice** knob. Parent measurement objects still name **SF1** (half-spread bps by mid decile) and **SF2** (L1/top-10 depth share + KL vs uniform 1/10) as distinct algebra — not replaced by L2-CAT. Feature family is new (**L2-SF ≠ L2-CAT**). GET-only / no new Logan credentials.

## Intent (one knob)

Holding **R1-P1 feebook** (reciprocal book) and **R1-P5 rails** (`content_fresh_flag`) fixed, and holding category mix as the panel's natural sports+nonsports seed (not the knob), wire an L2 shape harness that runs Dubach algebra on the R3-P4 panel stub (prefer `panel_admitted.json` when present), selecting **which SF algebra object** is the scorecard primary.

**One knob only:** shape_object ∈ {`sf1_half_spread`, `sf2_depth_kl`} with feebook+rails fixed. Category slice is **not** an arm here (owned by L2-CAT; do not reopen).

**Not arms:** inventing depth; Lee-Ready; `000` allocator port; Cap-SR; L2-CAT category arms; dual-editing PR13 base lab in place (new lab dir).

## Pins

| Pin | Value |
|---|---|
| Parent freeze | sha256 `4a4e7cc61efcb436955c566edc7a2681603a014725bc79047f9d825392064528` |
| Panel stub | `lab/astra-capture/r3-p4-l2-shape/panel_stub.json` · `2026-09-22.r3-p4-l2-shape-v0` · sha256 `7477e023ab70c59a6739650155ddb9d77077766e3afd80443e540d60b5a86cbb` · `admitted_at` **null** · 4 events / 6 markets |
| Live OB seed (supporting) | `packets/r3_p4_l2_shape/live_get_2026-09-22/ob_*.json` (do not invent; use as fixture only; primary books have non-empty yes_dollars/no_dollars) |
| Fee / book (FIXED) | `kalshi_feebook_lab_20260922/` @`22371178cb2663250b4762f328069571c48cb551` |
| Rails (FIXED) | `kalshi_rails_lab_20260922/` @`6a28e0d6254327ea4e6451c781bec56215ac6cac` |
| Capture | GET-only public orderbook — no trading host; no Logan keys |
| Strategy | **None** — quote-side microstructure only |

## Arms

| Arm | Name | Shape object |
|---|---|---|
| **R3P4S0** | SF1 half-spread | Median half-spread bps by mid-price decile; Lee-Ready **REFUSED** |
| **R3P4S1** | SF2 depth KL | L1/top-10 depth share + KL vs uniform 1/10; no invent depth; no invent fills |

## Dead-card / live-pin overlap (named)

| Pin / card | Overlap | Handling |
|---|---|---|
| EMPTY-OB invent-depth refuse | Complementary gate just landed | Name as nearest dead card; do not invent depth here either |
| L2-CAT PR28 | Sibling category knob | New lab dir; do **not** reopen L2-CAT |
| Base R3-P4 SF1/SF2 lab (PR13) | Complementary substrate | New lab dir; do not dual-edit PR13 into PnL |
| Cap-SR / Cap-SR-FX / QF / PROP-LQ / SOT-ID | Closed | Do not reopen |
| R3-P3 FL bands | Complementary (price-outcome vs quote-side) | Share feebook/rails only |
| S2 / R2-P4 | Hard WAIT | Stay queued |
| R3-P1 / R3-P2 / S1 | WAIT / deferred | Stay deferred |
| Capital-structure A1/A2/A3 | Already landed | Not this packet |

## Scorecard fields (null now)

`sf1_median_half_spread_bps_by_mid_decile`, `sf2_l1_top10_depth_share`, `sf2_kl_vs_uniform_1_10`, `n_books`, `n_snapshots`, `results`, `pnl` — null until Clock admit + Examiner.

## Lab dir

`kalshi_r3p4_l2_sf_lab_20260923/` (do not mutate Q / Cap-SR / Cap-SR-FX / C3 / C5 / R3-P3 / R3-P4 base / L2-CAT / EMPTY-OB / SOT-ID / S4 / S5 / R2-P3 / feebook / rails labs).

## Integrity (Clock gate)

Commit the **attached** Conductor-box freeze / parent / panel / OB fixture bytes **verbatim**. Pin digests to `sha256sum` of those files. **Refuse labeled recreations / invented non-empty books.** Prefer `panel_admitted.json` when present; do not invent markets/depth/cohort beyond the authentic stub + recorded live_get fixtures.

## Merge gates

Units green; `results`/`pnl` null; Examiner stub_ready NOT_SCORED after merge.
