# EXAMINER-CHANNEL FEE+QUEUE HONESTY ON Q6-000 — FREEZE KERNEL 2026-09-22 (ET)

**Owner:** R&D Variants (freeze) → Simulator join → Examiner  
**Status:** FROZEN — before any filled metrics  
**Cite:** Conductor post-PR10 (`7026be51`); R2-P1 hygiene join in `kalshi_r2p1_hygiene_000_lab_20260922/`; QF join in `kalshi_queue_fragility_000_lab_20260922/`  
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`  
**Hard rules:** ONE scorecard path. Consumes both hygiene join + QF join. No 000 retune. No A2/A3. No live orders. No invented PnL. All scorecard fields stay **null** until Examiner-ready.

---

## Intent

Run a **single Examiner-channel** honesty pass on Q6-`000` that combines:

1. **Fee hygiene** (R2-P1 / feebook @ `22371178cb2663250b4762f328069571c48cb551`) — `fee_delta_vs_inherited_model`, `freshness_gap_sec`, `queue_bin_mismatch_rate`  
2. **Queue fragility** (QF arms / rails @ `6a28e0d6254327ea4e6451c781bec56215ac6cac`) — `fill_rate_delta_vs_q3300`, `adverse_queue_exposure`, `participation_stress_gap`

Same fills stream; same shared $5k; strategy pointer `000` frozen. Not two separate Examiner claims.

---

## Inputs

| Source | Role |
|---|---|
| Production (preferred) | `nfl_factorial_lab_20260921/results/q3300_d0.25_000_fills.jsonl.gz` (+ matching orders) |
| Present at freeze (box) | **True** · sha256 `9d56f5d3c599e092606be9f4a1ad41ae8baabff4921d3d722adf0b57ac944a3f` |
| Synthetic stand-in | Hygiene `fixtures/synthetic_q3300_d0.25_000_*.jsonl` and/or QF synthetic — OK for units; if production gzip absent in checkout, document synthetic-only and **keep metrics null** |
| Hygiene join | `kalshi_r2p1_hygiene_000_lab_20260922/` (`fixture_join` + `hygiene`) |
| QF join | `kalshi_queue_fragility_000_lab_20260922/` (QF0/QF1/QF2) |

Shadow: `b55ff36cb161c824a3d1b490795c8ac6891f01489456f61da311ac863366af48` selected `000`.

---

## Scorecard (all null in this freeze)

| Field | Channel |
|---|---|
| `fee_delta_vs_inherited_model` | Fee / R2-P1 |
| `freshness_gap_sec` | Rails content-fresh |
| `queue_bin_mismatch_rate` | Rails queue bin |
| `fill_rate_delta_vs_q3300` | QF |
| `adverse_queue_exposure` | QF |
| `participation_stress_gap` | QF |
| `results` / `pnl` | Always null here |

`write_scorecard` / freeze writers must refuse non-null until Examiner GO.

---

## Do-not-modify

1. No live orders.  
2. No 000 retune; no A2/A3; no Q7 reopen.  
3. Do not invent filled metrics from synthetic rows into freeze files.  
4. Do not split into two Examiner packets.  
5. Prefer one new thin orchestration lab **or** a single module that imports both joins — do not mutate feebook/rails cores.  
6. Do not reopen capital-structure.

---

## Empty results

`packets/EXAMINER_FEE_QUEUE_HONESTY_000/results.json` + `results/EMPTY_RESULTS.json`

---

## Frozen-at

`2026-09-22T23:56:29.261094+00:00` UTC. Desk 2026-09-22 ET.
