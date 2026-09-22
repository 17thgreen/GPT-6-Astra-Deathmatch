# QUEUE-FRAGILITY QF FIXTURE-JOIN ON Q6-000 — FREEZE KERNEL 2026-09-22 (ET)

**Pick:** **(B)** fixture-join queue-fragility QF0/QF1/QF2 arms  
**Prior:** (A) R2-P1 fixture-join harness live @ `80050e9b`  
**Owner:** R&D Variants (freeze) → Simulator → Examiner  
**Status:** FROZEN — before any filled metrics  
**Cite:** Conductor post-PR8; `QUEUE_FRAGILITY_000_R1P5_FREEZE_2026-09-22.md` (e01d684a…); QF lab merge `c33af159`  
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`  
**Hard rules:** One knob = queue/fill arm attribution join. Fee channel **FIXED** at R1-P1 examiner. No 000 retune. No A2/A3. No live orders. No invented PnL. Outputs stay **null** until Examiner-ready.

---

## Measurement

Join Q6-`000` fill/order fixtures through `kalshi_queue_fragility_000_lab_20260922/` arms:

| Arm | Queue treatment |
|---|---|
| QF0 | ahead 3300, participation 0.5, measured |
| QF1 | ahead 10000, participation 0.5, measured |
| QF2 | front (0 ahead), participation 0.5 |

Fee: R1-P1 examiner @ `22371178cb2663250b4762f328069571c48cb551` — identical on every arm (not the knob).  
Rails instrument: @6a28e0d6254327ea4e6451c781bec56215ac6cac.

**Outputs (remain null in this freeze / EMPTY_RESULTS):**

| Field | Status |
|---|---|
| `fill_rate_delta_vs_q3300` | null until Examiner-ready |
| `adverse_queue_exposure` | null until Examiner-ready |
| `participation_stress_gap` | null until Examiner-ready |
| `results` / `pnl` | null |

Harness+units may prove wiring on synthetic rows without writing non-null freeze scorecard values.

---

## Fixture pins (read-only)

| Fixture | Role |
|---|---|
| `nfl_factorial_lab_20260921/results/q3300_d0.25_000_fills.jsonl.gz` | Primary |
| Matching `*_000_orders.jsonl.gz` | Orders |
| Optional `q10000_d0.25_000_*` | Harsh twin label — not a fee knob |
| Synthetic stand-in | OK for units if gzip absent in checkout; document production pin |

Shadow: `b55ff36cb161c824a3d1b490795c8ac6891f01489456f61da311ac863366af48` selected `000`.

---

## Do-not-modify

1. No live orders.  
2. No 000 retune; no A2/A3; no Q7 reopen.  
3. Do not vary fee treatment (R2-P1 already covered).  
4. Do not fill scorecard metrics in freeze files.  
5. Prefer join under/against `kalshi_queue_fragility_000_lab_20260922/` — one lab/PR.  
6. Do not mutate feebook/rails/Q/R2-P1 cores beyond necessary sibling pins.

---

## Empty results

`packets/QF_FIXTURE_JOIN_000/results.json` + `results/EMPTY_RESULTS.json`

---

## Frozen-at

`2026-09-22T23:43:00.722525+00:00` UTC. Desk 2026-09-22 ET.
