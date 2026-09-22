# R2-P1 FIXTURE-JOIN ON Q6-000 — FREEZE KERNEL 2026-09-22 (ET)

**Pick:** **(A)** fixture-join R2-P1 fee/rails hygiene scorecard (preferred — Q6-`000` fill ledgers already on disk under factorial results)  
**Not picked:** (B) queue-fragility QF fixture-join — queued after this join lands  
**Owner:** R&D Variants (freeze) → Simulator fixture join → Examiner  
**Status:** FROZEN — before any filled metrics  
**Cite:** Conductor post-PR7 (`c33af159…`); R2-P1 hygiene lab merge `25ec05381207252abb8abec8f6f99e30765f9704`; Deep Research §R2-P1  
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`  
**Hard rules:** No Q6-000 signal retune. No capital A2/A3. No live orders. No invented PnL. Scorecard fields stay **null** until Examiner-ready; this freeze does not authorize writing filled metrics yet.

---

## Why (A) over (B)

| Signal | (A) R2-P1 join | (B) QF join |
|---|---|---|
| Lab on main | `kalshi_r2p1_hygiene_000_lab_20260922/` @ `25ec05381207252abb8abec8f6f99e30765f9704` | `kalshi_queue_fragility_000_lab_20260922/` @ PR7 merge |
| Join inputs closer | Yes — `nfl_factorial_lab_20260921/results/q*_000_fills.jsonl.gz` (+ orders) exist for label `000` | Needs QF arm attribution join; fee path already covered by A |
| Board leverage | Highest — Board risk #1 fee-pin ≠ R1-P1 | Second — queue stress after fee truth |

---

## Measurement (still instrument-only)

Join existing Q6-`000` fill/order fixtures into R2-P1 helpers under **Examiner feebook channel** + R1-P5 labels:

- `maker_credit_floor_zero_refuse`
- `content_fresh_flag`
- `queue_attribution_bin` vs assumed q3300/q10000

**Outputs (remain null in this freeze / EMPTY_RESULTS):**

| Field | Status |
|---|---|
| `fee_delta_vs_inherited_model` | null until Examiner-ready |
| `freshness_gap_sec` | null until Examiner-ready |
| `queue_bin_mismatch_rate` | null until Examiner-ready |
| `results` / `pnl` | null |

Implement may land **join harness + unit fixtures** that prove wiring without writing non-null scorecard values into `FROZEN_EXPERIMENT.json`.

---

## Fixture pins (read-only)

| Fixture | Role |
|---|---|
| `nfl_factorial_lab_20260921/results/q3300_d0.25_000_fills.jsonl.gz` | Primary fill stream for label `000` |
| Matching `*_000_orders.jsonl.gz` | Order context |
| Optional harsh twin `q10000_d0.25_000_*` | Stress label only — not a second fee knob |
| Do **not** treat paircheck arm D fills as a new strategy | Allocator is still `000`; pair-check stays closed (KILL B) |

Fee bind: `kalshi_feebook_lab_20260922/` @22371178cb2663250b4762f328069571c48cb551  
Rails labels: `kalshi_rails_lab_20260922/` @6a28e0d6254327ea4e6451c781bec56215ac6cac  
Shadow: `b55ff36cb161c824a3d1b490795c8ac6891f01489456f61da311ac863366af48` selected `000`

---

## Do-not-modify

1. No live orders.  
2. No 000 retune; no A2/A3; no Q7 reopen.  
3. Do not fill scorecard metrics in this freeze packet.  
4. Do not invent PnL / completed-profit.  
5. Do not start (B) QF fixture-join until this (A) join freeze is accepted and harness lands (or Conductor reorders).  
6. New join code only under R2-P1 lab or `kalshi_r2p1_fixture_join_000_lab_*` — do not mutate feebook/rails/Q.

---

## Empty results

`packets/R2-P1_FIXTURE_JOIN_000/results.json` + `results/EMPTY_RESULTS.json`

---

## Frozen-at

`2026-09-22T23:27:12.377517+00:00` UTC. Desk 2026-09-22 ET.
