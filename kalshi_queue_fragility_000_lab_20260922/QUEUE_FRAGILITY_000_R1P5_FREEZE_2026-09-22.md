# QUEUE-FRAGILITY OF Q6-000 UNDER R1-P5 — FREEZE KERNEL 2026-09-22 (ET)

**Owner:** R&D Variants (freeze) → Simulator → Examiner  
**Status:** FROZEN — maximize twin after R2-P1 merge `25ec0538`  
**Cite:** Conductor 2026-09-22 post-PR6; R1-P5 rails extract; R2-P1 complete (fee hygiene)  
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`  
**Hard rules:** One knob = **queue/fill stress only**. Fee treatment **FIXED** at R1-P1 examiner channel. No Q6-000 signal retune. No capital A2/A3 reopen. No live orders. No invented PnL. `results`/`pnl` null until Examiner-ready fixture join.

---

## Intent

Holding strategy **Q6-`000`**, shared **$5,000**, 31-game tape, and **R1-P1 feebook examiner channel fixed**, measure how **R1-P5 queue/fill assumptions** change fill attribution and adversity labels (instrument only — not a promotion claim).

Orthogonal to R2-P1 (fee hygiene with queue fixed). Do not merge knobs.

---

## Pins

| Pin | Value |
|---|---|
| Strategy | Q6-`000` KEEP · shadow sha `b55ff36cb161c824a3d1b490795c8ac6891f01489456f61da311ac863366af48` |
| Tape | factorial inputs manifest sha `375ea6e2c9125a411d5444a88115213542d5b19c874d73a2bed0b9355fd6277d` · N_events=31 |
| Fee (FIXED) | `kalshi_feebook_lab_20260922/` @22371178cb2663250b4762f328069571c48cb551 examiner channel only — **not** the knob; forbid shadow fee literals |
| Queue (KNOB) | `kalshi_rails_lab_20260922/` @6a28e0d6254327ea4e6451c781bec56215ac6cac |
| Capital | shared pool A1-equivalent — **do not reopen** A2/A3 |
| Prior | R2-P1 hygiene merged @25ec0538 |

---

## Arms (queue/fill only; same fee channel, same 000, same C_total)

| Arm | Name | Queue / fill treatment (via rails) |
|---|---|---|
| **QF0** | Primary assumed | `queue_ahead=3300`, `fill_participation=0.5`, `queue_model=measured` — baseline label |
| **QF1** | Stress ahead | `queue_ahead=10000` (rails stress), same participation 0.5, measured model |
| **QF2** | Front / optimistic bound | `queue_model=front` (0 ahead), participation 0.5 — optimistic bound vs measured |

Optional instrument labels (not extra knobs): taker_side polarity asserts; same-price keep place; new price → back of queue — consume R1-P5 pins unchanged.

---

## Pre-settlement outputs (nullable until fixture join)

| Output | Meaning |
|---|---|
| `fill_rate_delta_vs_q3300` | Fill/participation outcome delta of QF1/QF2 vs QF0 on same tape slice |
| `adverse_queue_exposure` | Exposure attributed to being behind assumed queue (instrument) |
| `participation_stress_gap` | Gap between assumed 0.5 participation and realized under stress ahead |

`results` / `pnl` stay null. No completed-profit claim without fee channel (always present via fixed R1-P1).

---

## Do-not-modify

1. No live orders / no live adapter.  
2. No Q6-000 retune; no Q7/pair-check reopen.  
3. No capital A2/A3 redesign.  
4. No fee-treatment arms (R2-P1 already covered); do not vary maker off / unrounded here.  
5. No invented walk PnL; empty results stay null until instrument-verified join.  
6. New lab dir only when implementing — do not mutate rails/feebook/Q/R2-P1/capital labs.

---

## Implement (after Conductor GO on this freeze, or immediate if standing maximize says freeze then land)

New dir e.g. `kalshi_queue_fragility_000_lab_20260922/`:

- `EXPERIMENT_SPEC.md` + `FROZEN_EXPERIMENT.json` (pnl + three outputs null)  
- Units: arms differ only in rails queue params; feebook binding identical; ban fee literals; empty results unchanged by units  
- PR cites this freeze + rails @6a28e0d6254327ea4e6451c781bec56215ac6cac + feebook fixed @22371178cb2663250b4762f328069571c48cb551

---

## Empty results

`packets/QUEUE_FRAGILITY_000_R1P5/results.json` + `results/EMPTY_RESULTS.json`

---

## Frozen-at

`2026-09-22T23:11:03.331014+00:00` UTC. Desk 2026-09-22 ET.
