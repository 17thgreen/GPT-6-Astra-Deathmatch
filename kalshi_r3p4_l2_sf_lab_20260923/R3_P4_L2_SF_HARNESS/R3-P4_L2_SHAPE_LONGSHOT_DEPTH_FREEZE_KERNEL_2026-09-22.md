# R3-P4 — L2 longshot half-spread + depth shape — FREEZE 2026-09-22 (ET)

**Packet ID:** R3-P4-L2-SHAPE-SF1-SF2  
**Owner (freeze):** Deep Research  
**Implementer (later):** Collector (GET L2 panel) → Simulator (shape stats) → Examiner  
**Reviewer:** Conductor triage; Adversary on top-heavy book assumptions  
**Status:** **FROZEN** — results/pnl **null** (not run)  
**Cite:** Conductor R3 triage ADMIT NOW; R3 brief §R3-P4; Dubach arXiv:2604.24366 SF1/SF2 → Kalshi bids-only; R1-P1 reciprocal book; R1-P5 freshness  
**Hard rules:** No live orders. No invented PnL. No Lee-Ready. No Q6-`000` allocator port. GET-only public L2.

---

## Intent

Port Dubach SF1/SF2 shape algebra to Kalshi bids-only books: (SF1) median quoted half-spread (bps of mid) by mid-price decile; (SF2) L1/top-10 depth share + KL vs uniform \(1/10\) null. Sports vs non-sports slices. Falsifies top-heavy assumptions that sneak into queue/fill models.

**Not a strategy.** Quote-side microstructure panel only.

---

## Dead-card / live-pin overlap (named)

| Pin | Overlap | Handling |
|---|---|---|
| Q6-`000` / Q7 / capital / F1–F3 | **Low / none** | Shape panel; no allocator port |
| R1-P1 / R1-P5 | **Uses as instruments** | Reciprocal book + content_fresh |
| R3-P3 FL bands | **Complementary** | P3 = price-outcome; P4 = quote-side shape |
| S1/S4/S5/R2-P3 | **May share L2 later** | Separate panel_version; do not steal C1 budget |
| Poly direction-inference 59% | **Explicitly out** | Kalshi has native taker fields |

---

## Mandatory pins

| Dep | Pin | Rule |
|---|---|---|
| Book | R1-P1 @ `22371178…` | `ask_YES=1−best_NO_bid` etc. |
| Freshness | R1-P5 @ `6a28e0d6…` | `content_fresh_flag` required |
| Capture | GET-only public orderbook | Stratified panel; raw depth only |

---

## Measurement objects

1. SF1: half-spread bps by mid decile (median)  
2. SF2: per-level share of top-10 depth; KL vs uniform  
3. Category slice: sports vs non-sports (no `000` knobs)  

**Null until Examiner:** `results`, `pnl`.

---

## Do-not-modify

No live orders; no invented depth; no Lee-Ready; no `000` retune; no S2/R2-P4 start before C1.

## Empty results

`packets/r3_p4_l2_shape/` — `results`/`pnl` null

## Frozen-at
`2026-09-22T23:59:59+00:00` UTC. Deep Research under Conductor R3 ADMIT NOW (parallel with P1).
