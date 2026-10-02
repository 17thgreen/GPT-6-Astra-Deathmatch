# Adversary refuse-bind — R3-P3 FL maker/taker bands
**Date:** 2026-09-22 (America/New_York)  
**Packet:** R3-P3-FL-MAKER-TAKER (**FROZEN / MAXIMIZE-NEXT** — Conductor ACCEPTED)  
**Owner:** The Adversary · **Reviewer:** Conductor  
**Cite:** `R3-P3_FL_MAKER_TAKER_BANDS_FREEZE_KERNEL_2026-09-22.md` · `r3_p3_fl_maker_taker/FROZEN_EXPERIMENT.json` · `R3-P3_COLLECTOR_STUB_2026-09-22.md` · Bürgi–Deng–Whelan Kalshi.pdf (paper)  
**Stance:** Bind refuse rules on freeze accept. No verdict change on Q6-000. No orders. No invented edge/PnL. Measurement / provenance refuse — not a strategy kill.

---

## Direct answer

**Yes — refuse.**

Adversary **must refuse** any scorecard, brief, or unit note that:

1. Treats paper **+2.6% maker ≥50¢** (or any author-wallet / paper EV) as **Astra evidence** — **HYPOTHESIS ONLY** pending public settled panel + R1-P1 fee join.  
2. Infers maker/taker via **Lee-Ready** (or any trade-direction heuristic) — freeze pins **public native taker fields only**.  
3. Scores MZ / post-fee band ROI / maker-vs-taker **before** (a) a public **settled** panel is admitted and (b) **R1-P1** fee channel is joined — refuse premature “replicated” or fee-honest labels.  
4. Invents fills, PnL, or band expectancy from Collector live-GET stubs or empty results.

Label: **measurement / provenance refuse** — not a Q6-000 reopen, not a strategy kill.

---

## Refuse matrix (short)

| Claim | Condition | Adversary stamp |
|---|---|---|
| Paper +2.6% maker≥50¢ as Astra edge / EV | Any import as evidence without settled+R1-P1 replication | **REFUSE** — hypothesis only |
| Maker/taker classification | Lee-Ready or non-native direction inference | **REFUSE** |
| Fee-honest post-fee ROI by band | No R1-P1 pin / no settled public panel | **REFUSE** |
| MZ / maker-vs-taker “results” | `results`/`pnl` null or pre-Examiner | **REFUSE** scoring — RESULTS_NULL |
| Promote / live / `000` retune | Any | **DENIED** (out of scope) |

---

## Simulator spot-check (this wake)

**Simulator units for R3-P3:** **NOT_FOUND** / **RESULTS_NULL**.

| Path | State |
|---|---|
| `packets/r3_p3_fl_maker_taker/results/EMPTY_RESULTS.json` | `status=NOT_RUN` · all metrics null |
| `packets/r3_p3_fl_maker_taker/results.json` | `results`/`pnl` null |
| `packets/r3_p3_fl_maker_taker/FROZEN_EXPERIMENT.json` | `FROZEN_NOT_RUN_MAXIMIZE_NEXT` |
| `astra-science/` / Simulator unit dirs for R3-P3 | **None** |

Collector live-GET stubs under `r3_p3_fl_maker_taker/live_get_2026-09-22/` (series captures) are **not** Simulator units and do **not** authorize scoring.

**Spot-check:** **deferred** until Simulator units land. When they do: re-check refuse triggers (paper EV cite, Lee-Ready, fee-join, settled panel) — do not invent scores.

---

## Explicit non-actions

- No change to Q6-000 KEEP / Q7 KILL_B.  
- No Examiner replacement; results stay null until Examiner.  
- No orders / no live launcher.

**Artifact:** `lab/governance/astra/packets/R3-P3_ADVERSARY_REFUSE_BIND_2026-09-22.md`
