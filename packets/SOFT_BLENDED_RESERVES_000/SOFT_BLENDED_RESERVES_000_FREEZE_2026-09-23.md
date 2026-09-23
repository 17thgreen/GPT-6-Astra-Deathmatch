# SOFT-BLENDED RESERVES OF Q6-000 — FREEZE KERNEL 2026-09-23 (ET)

**Owner:** R&D Variants (freeze) → Simulator → Examiner  
**Status:** FROZEN — Conductor MAXIMIZE GO 2026-09-23 (C1 books path exhausted)  
**Cite:** Conductor soft-blended capital reserves GO; `MAXIMIZE_PIN_2026-09-23_0915ET.md`; capital-structure PR5 merged @`ce4671b8` (A1/A2/A3 rails); deferred fourth arm from capital draft do-not-modify #10  
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`  
**Feature family:** **Cap-SR** (capital soft-reserve policy) — **≠ F1 / F2 / F3**  
**Nearest dead cards:** **C1 empty-book** (orderbook pin = real empty books; scoring blocked / PR19) · **Q7 Arm B kill** (Examiner KEEP `000` / KILL B)  
**Hard rules:** One knob = **soft_policy / blend rule only**. Shared $5k remains the **only** promotion scoreboard. Fee-honest via R1-P1. No live orders. No Q6-`000` retune. Do **not** reopen queue-fragility. Do **not** reopen A1 vs A3 as arms. `results`/`pnl` null until Examiner opens.

---

## Intent

Holding strategy **Q6-`000`**, shared **$5,000**, soft per-event reserve **R_m = 161**, residual **9** non-trading, 31-game tape, **R1-P1 feebook**, and **R1-P5 rails labels fixed**, measure how **soft-reserve blend / borrow policy** changes utilization and borrow instrumentation (measurement only — not a promotion claim).

Capital-structure A1/A2/A3 rails already live (`kalshi_capital_structure_lab_20260922/`). This probe is the queued **soft-reserve what-if** twin: soft_policy variants under the **A2 substrate** only. Promotion metric stays shared-account; never sum-of-N wallets.

---

## Pins

| Pin | Value |
|---|---|
| Strategy | Q6-`000` KEEP · shadow sha `b55ff36cb161c824a3d1b490795c8ac6891f01489456f61da311ac863366af48` |
| Tape | factorial inputs manifest sha `375ea6e2c9125a411d5444a88115213542d5b19c874d73a2bed0b9355fd6277d` · N_events=31 |
| C_total | **5000** USD (shared scoreboard) |
| Soft slice R_m | **161** USD / event |
| Residual | **9** USD → `non_trading_residual_bucket` (may **not** fund orders) |
| Fee (FIXED) | `kalshi_feebook_lab_20260922/` @`22371178cb2663250b4762f328069571c48cb551` examiner channel — forbid shadow fee literals `0.0175`/`0.07` |
| Queue labels (FIXED) | `kalshi_rails_lab_20260922/` @`6a28e0d6254327ea4e6451c781bec56215ac6cac` — instrument only; **not** the knob |
| Parent capital lab | `kalshi_capital_structure_lab_20260922/` @`ce4671b8…` — A2 soft_policy control pin = `borrow_unused_event_id_FIFO` |
| Capital substrate | **A2-family only** (shared pool + soft reserves). Do **not** arm A1 (no soft) or A3 (hard fence) here. |
| Primary stress label | `q3300_d0.25` (not a second capital knob) |

---

## Arms (soft_policy / blend only; same C_total, same R_m, same 000)

| Arm | Name | Soft policy (one knob) |
|---|---|---|
| **SR0** | FIFO unused (A2 control) | `borrow_unused_event_id_FIFO` — borrow only unused soft reserve of other events; borrowers ordered by ascending event_id; every borrow logged; never exceed remaining pool cash. Matches capital-structure A2 pin. |
| **SR1** | Proportional unused blend | `borrow_unused_proportional` — same unused-only constraint; donors contribute **pro-rata to their unused soft reserve** (blended unused pool), not FIFO event_id order. Borrow log required. |
| **SR2** | Soft blend pool fraction | `soft_blend_pool_fraction_0_5` — **half** of each R_m (`floor(R_m/2)=80`) seats a shared soft blend pool; remainder stays event-local soft; draw order = local unused → blend pool → refuse. Residual 9 stays non-trading. Borrow/blend draws logged. |

**Not arms:** A1 shared-no-soft; A3 hard equal slices; queue 3300 vs 10000; fee treatment variants; any Q6 signal change; multi-wallet promotion scoreboard.

### Soft blend rationale
SR0 is the conservative A2 control already unit-tested. SR1 changes only donor **selection weights** among unused soft. SR2 is the deferred “blended” fourth-arm brief: an explicit shared soft blend pool without hard ring-fence and without changing the shared $5k promotion scoreboard.

If SR1/SR2 never produce borrow/blend-log entries by construction, Adversary may refuse the arm as collapsed into SR0/A3.

---

## Do-not-modify list

1. No live orders / no live launcher.  
2. No Q6-`000` signal retune; no Q7 reopen; no pair-check knob.  
3. No queue-fragility reopen / no QF arm changes.  
4. No A1 vs A3 re-arming in this lab (parent capital lab already owns that).  
5. No silent fee or queue retune — consume merged R1-P1 / R1-P5.  
6. No multi-wallet promotion scoreboard; no sum-of-N vs one-5k tables.  
7. Do not mutate `kalshi_capital_structure_lab_20260922/` / feebook / rails / Q labs — **new lab dir only**.  
8. `results` / `pnl` stay null in `FROZEN_EXPERIMENT.json` until Examiner opens (units may assert invariants without inventing walk P&L).  
9. No invented 110% / no strategy claim from Cap-SR instruments alone.

---

## Lab deliverables (implement now)

New dir: `kalshi_soft_blended_reserves_000_lab_20260922/` (or `…20260923/` if clock requires) in Astra repo:

- `EXPERIMENT_SPEC.md` + `FROZEN_EXPERIMENT.json` (hypothesis → freeze → unit page) before result claims  
- Soft-policy engine: SR0 / SR1 / SR2 with equal C_total + R_m invariants  
- Prefer **import / reuse** capital-structure A2 engine for SR0; extend only soft_policy hook — do not fork fee/queue  
- Unit tests: SR0 matches A2 FIFO behavior; SR1 pro-rata unused; SR2 blend-pool fraction + local-first; residual non-trading; forbid wallet-sum helper; fee_source=feebook + queue_source=rails pins stated  
- First PR may be **unit/instrument only** with pnl null (preferred)

---

## Scorecard fields (Examiner later — null now)

| Field | Meaning |
|---|---|
| `borrow_count_delta_vs_fifo` | SR1/SR2 borrow or blend-draw count minus SR0 |
| `blend_utilization_gap` | Max−min soft utilization across events under the arm |
| `soft_breach_or_blend_rate` | Fraction of fills that required cross-event borrow or blend-pool draw |

All three stay **null** in this freeze / EMPTY_RESULTS. Fee-honest shared-account net stays Examiner-owned.

---

## Dead-card / orthogonality note

- **≠ F1/F2/F3** feature families.  
- Nearest cemetery / blocked cards named: **C1 empty-book** (cannot score UFC honesty until live depth); **Q7 Arm B kill**.  
- Cap-SR does not ungate C1 books and does not revive Arm B.

---

## Frozen-at

Desk 2026-09-23 ET. Conductor MAXIMIZE GO soft blended reserves acknowledged. Variants owner: R&D Variants.
