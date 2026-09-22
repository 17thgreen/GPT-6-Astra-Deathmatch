# CAPITAL STRUCTURE PROBE — FREEZE KERNEL 2026-09-22 (ET)

**Owner:** R&D Variants (freeze / pin ownership)  
**Implementer:** Cloud agent → Simulator review  
**Reviewer:** Examiner (Kalshi) scorecard; Adversary spot-check on wallet-sum fallacy  
**Status:** FROZEN — Conductor GO 2026-09-22 (post Q7 verify+analyze)  
**Cite:** Conductor GO; Q7 verification VERIFIED; paircheck_effects NO_NEW_SELECTION; SHADOW_CANDIDATE_FREEZE selected 000  
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`  
**Hard rules:** No live orders. No Q6/Q7 signal retune. Same tape + same fee channel across arms. Shared $5k = only promotion scoreboard.

---

## Signed Q7 / shadow inputs (freeze-before-results)

| Artifact | Pin |
|---|---|
| Q7 verification | `nfl_paircheck_lab_20260922/results/verification.json` status=`VERIFIED` all_checks_passed=`true` sha256=`eb1586bf13b1631951a4f177293350cb89fc7948a50fbb7044f4f05313ebc06f` |
| Q7 analyze / selection | `nfl_paircheck_lab_20260922/results/paircheck_effects.json` status=`COMPLETE` selection=`NO_NEW_SELECTION` fallback_shadow=`000` sha256=`5d87ea610f22482c980868d8a31a228ca1931368d9eeab73add4256d2e117fdf` |
| Note on `analysis_status.json` | May still read `NOT_RUN_INPUTS_MISSING`; **authoritative analyze artifact for this freeze is `paircheck_effects.json`** (`q7_analyze.log`=`COMPLETE`) |
| Shadow incumbent | `nfl_factorial_lab_20260921/SHADOW_CANDIDATE_FREEZE.json` selected=`000` sha256=`b55ff36cb161c824a3d1b490795c8ac6891f01489456f61da311ac863366af48` |
| Tape / panel | Q6/Q7 **31-game development cohort** under `nfl_factorial_lab_20260921/inputs/` · `manifest.json` sha256=`375ea6e2c9125a411d5444a88115213542d5b19c874d73a2bed0b9355fd6277d` · **N_events=31** |
| Primary stress | `q3300_d0.25` (optional harsh twin `q10000_d0.25` — not a second capital knob) |
| Strategy pointer | **Q6 label `000` shadow incumbent** (NO_NEW_SELECTION → do not bind Q7 arm B). Pair-check on/off is **not** varied here. |
| Fee channel | R1-P1 FEEBOOK (merged) |
| Queue / fill rails | R1-P5 rails (merged) — instrument labels only |

A/D PASS (Conductor): Q7 verify controls green; this probe does not reopen pair-check selection.

---

## 0. Promotion scoreboard (locked)

**Only the SHARED account is the promotion scoreboard.**

Forbidden: comparing the sum of N independent per-market wallets to one shared C_total.

---

## 1. Constants

| Pin | Frozen value |
|---|---|
| C_total | **5000** USD |
| N_events | **31** (development cohort) |
| Soft / hard per-event default slice | floor(C_total / N_events) = **161** USD |
| A3 residual | **9** USD → `non_trading_residual_bucket` (may **not** fund orders) |
| Strategy | Q6-`000` shadow incumbent |
| Shadow starting_cash | 5000 |

---

## 2. Arms (one capital-rule difference; same C_total)

| Arm | Name | Rule |
|---|---|---|
| **A1** | Shared pool (status quo) | Single pool C_total; markets compete; no per-market reserve |
| **A2** | Shared + soft per-market reserves | Soft reserve R_m = 161 per event; **soft_policy = `borrow_unused_event_id_FIFO`** (conservative): borrow only unused soft reserve of other events; borrowers ordered by ascending event_id; every borrow logged; never exceed remaining pool cash |
| **A3** | Hard equal slices | Hard slice 161 per event; **no cross-event borrow**; residual 9 USD locked in `non_trading_residual_bucket` |

### Soft policy rationale (A2)
Unused-only + deterministic FIFO by event_id + mandatory borrow log. If the borrow log is empty by construction, Adversary may refuse A2 as collapsed into A3.

### A3 residual rationale
Leftover after equal floor division does not trade — keeps slices + residual = C_total with no silent extra slice.

---

## 3. Do-not-modify list

1. No live orders / no live launcher.  
2. No Q6 `000` signal retune; no Q7 arms A–D retune; no pair-check knob in this lab.  
3. No HX / weather / directional picker reopen.  
4. No silent fee or queue retune (consume merged R1-P1 / R1-P5).  
5. No Collector freshness implementation; no Examiner historical walk from this packet alone.  
6. No multi-wallet promotion scoreboard; no sum-of-N vs one-5k tables.  
7. No fourth blended arm without a new one-knob brief.  
8. Do not mutate Q / feebook / rails lab directories — new lab only.  
9. `results` / `pnl` stay null in `FROZEN_EXPERIMENT.json` until an Examiner pass (units may assert invariants without inventing walk P&L).

---

## 4. Lab deliverables (implement now)

New dir e.g. `kalshi_capital_structure_lab_20260922/` in Astra repo:

- `EXPERIMENT_SPEC.md` + `FROZEN_EXPERIMENT.json` (hypothesis → freeze → unit page) before result claims  
- Capital engine: A1 / A2 / A3 with equal C_total invariant tests  
- Unit tests: A3 no-borrow; A2 borrow log + unused-only; residual non-trading; forbid wallet-sum helper  
- Import feebook + rails as frozen deps (no edits)  
- First PR may be **unit/instrument only** with pnl null (preferred if full Q6-000 replay is heavy); runner bind to Q6-000 may follow

---

## 5. Scorecard fields (Examiner later)

Per arm on same tape slice: fee-honest shared-account net; drawdown; A2 borrow count/time; per-event utilization vs reserve/slice; refuse completed-profit without fee channel; refuse promotion from isolated wallet sum.

---

## Frozen-at

`2026-09-22T22:45:31.730109+00:00` (UTC). Desk date 2026-09-22 ET.  
Variants owner: R&D Variants. Conductor GO acknowledged.
