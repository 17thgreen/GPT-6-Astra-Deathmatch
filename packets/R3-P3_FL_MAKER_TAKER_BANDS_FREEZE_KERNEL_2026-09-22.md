# R3-P3 — Maker/Taker + favorite–longshot bands — FREEZE 2026-09-22 (ET)

**Packet ID:** R3-P3-FL-MAKER-TAKER  
**Owner (freeze):** Deep Research → Variants maximize kick  
**Implementer (later):** Collector (settled public trades+resolution) → Simulator/Polars panel → Examiner replication checklist  
**Reviewer:** Conductor triage; Adversary on citing paper EV as Astra evidence  
**Status:** **FROZEN / MAXIMIZE-NEXT** — Conductor post-PR11; results/pnl **null** (not run)
**Variants kick:** Collector stub filed 2026-09-22; Variants owns freeze path report  
**Cite:** Conductor R3 triage ADMIT-NEXT (freeze after P1/P4); R3 brief §R3-P3; Bürgi–Deng–Whelan Kalshi.pdf; public `taker_*` trade fields  
**Hard rules:** Settled **public** tape only. **Refuse Lee-Ready.** Paper +2.6% maker≥50¢ = **hypothesis to replicate**, not Astra EV. No live orders. No invented PnL. No `000` retune. Prefer weather/politics/economics first; sports only on non-frozen series if Scout unblocks.

---

## Intent

On a bounded settled panel: join public trades (`taker_outcome_side` / `taker_book_side`) + resolution. Compute (1) Mincer–Zarnowitz \(Y-P=\alpha+\psi P\) event-clustered; (2) post-fee ROI by 10¢ bands via R1-P1 (pin post-Apr-2025 maker fees); (3) Maker vs Taker via native taker fields.

**Not a strategy.** Pricing / adverse-band measurement only.

---

## Dead-card / live-pin overlap (named)

| Pin | Overlap | Handling |
|---|---|---|
| R1-P3 adverse objects | **Distinct** | External-odds de-vig/hedge/odds_age ≠ FL band expectancy |
| S1/S4/S5/R2-P3 | **Avoid frozen series as first panel** | Prefer non-sports or Scout-cleared non-frozen |
| Q6-`000` | **None on signal** | Stress whether sports maker sits in toxic bands — no retune |
| Paper author PnL claims | **Hypothesis only** | Replicate under R1-P1; never import as evidence |

---

## Mandatory pins

| Dep | Pin | Rule |
|---|---|---|
| Fee | R1-P1 @ `22371178…` | Post-Apr-2025 maker-fee regime |
| Trades | Public Get Trades taker fields | Refuse Lee-Ready |
| Bands | Pre-register 10¢ bands before looking | Examiner checklist |

---

## Measurement objects

MZ regression; post-fee ROI by band; Maker vs Taker slice — **null** until Examiner.

## Empty results

`packets/r3_p3_fl_maker_taker/` — `results`/`pnl` null

## Frozen-at
`2026-09-22T23:59:59+00:00` UTC. Deep Research under Conductor R3 ADMIT-NEXT (after P1/P4).
