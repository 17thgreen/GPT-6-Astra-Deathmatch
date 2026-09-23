# CAP-SR EFFECTS PATH ON Q6-000 — FREEZE KERNEL 2026-09-23 (ET)

**Owner:** R&D Variants (freeze / implement) → Simulator → Examiner  
**Status:** FROZEN — Conductor MAXIMIZE NEXT after R3-P3 PR23 merge @`cfd5f95a`  
**Cite:** Conductor 2026-09-23 leftover orthogonal; `MAXIMIZE_PIN_2026-09-23_1025ET.md` Cap-SR Simulator effects path; parent Cap-SR PR20 @`45863037` · freeze sha `1f263dec…`; capital-structure PR5 @`ce4671b8`  
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`  
**Packet ID:** CAP-SR-EFFECTS-PATH-000  
**Feature family:** **Cap-SR-FX** (effects path) — orthogonal to R3-P3 / C3 / C5 / C1-empty-books; builds on Cap-SR soft_policy rails (not a dual soft_policy lab)  
**Hard rules:** Instrument metrics only. Shared **$5k** promotion scoreboard only. GET-only / no Logan keys. No live orders. No invented PnL. No Q6-`000` retune. No QF reopen. No dual Cap-SR labs. No `admit.py`. `results`/`pnl` null until Examiner.

---

## Why Cap-SR effects (not S1 this slot)

S1 `KXMLBGAME` panel stub is `PANEL_SCHEMA_STUB_EMPTY_EVENTS` (`admitted_at` null) — not unit-GO ready. Cap-SR soft-policy rails already merged (PR20, 32 unit OK) but **effects path** (join soft_policy arms to Q6-`000` tape/fixtures for instrument metrics) is the oldest leftover scoring-path unblock Conductor named.

Archivist PACKET_INDEX bump PR19–23 remains Archivist-owned (not this freeze).

---

## Intent (one knob)

Holding strategy **Q6-`000`**, shared **$5,000**, R_m=161, residual 9 non-trading, **R1-P1 feebook**, **R1-P5 rails**, and Cap-SR soft_policy engine fixed, wire an **effects-path** harness that joins Cap-SR arms to Q6-`000` fill/order fixtures (prefer production gzip when present) and emits Cap-SR instrument schema — **without** Examiner PnL.

**One knob only:** fixture stress label ∈ {`q3300_d0.25` (primary), `synthetic_borrow_stress`} with soft_policy arms SR0/SR1/SR2 all run under the chosen stress (soft_policy itself already frozen in Cap-SR — not reopened as a new knob family).

**Not arms:** new soft_policy variants; A1↔A3 reopen; QF queue arms; C3/C5/R3-P3 kernels; `000` retune.

---

## Pins

| Pin | Value |
|---|---|
| Parent Cap-SR lab | `kalshi_soft_blended_reserves_000_lab_20260923/` @`45863037` (PR20) · freeze sha `1f263dec7d7810515c3e32c13f3c5eca4344c4951db762a88ea01a8dfde7b1b3` |
| Parent capital lab | `kalshi_capital_structure_lab_20260922/` @`ce4671b8` — A2 substrate only |
| Strategy | Q6-`000` KEEP · shadow sha `b55ff36cb161c824a3d1b490795c8ac6891f01489456f61da311ac863366af48` |
| Tape / fixtures | Prefer `nfl_factorial_lab_20260921/results/q3300_d0.25_000_fills.jsonl.gz` when present; else synthetic borrow-stress fixtures for units only |
| Fee (FIXED) | `kalshi_feebook_lab_20260922/` @`22371178cb2663250b4762f328069571c48cb551` |
| Rails (FIXED) | `kalshi_rails_lab_20260922/` @`6a28e0d6254327ea4e6451c781bec56215ac6cac` |
| Soft policies (FIXED set) | SR0 `borrow_unused_event_id_FIFO` · SR1 `borrow_unused_proportional` · SR2 `soft_blend_pool_fraction_0_5` — import from Cap-SR lab; do not re-implement |

---

## Arms (fixture-stress knob only)

| Arm | Name | Fixture stress |
|---|---|---|
| **FX0** | Primary q3300 | Join Cap-SR SR0/SR1/SR2 under `q3300_d0.25` fill/order fixtures (or documented synthetic stand-in) |
| **FX1** | Borrow-stress synthetic | Same Cap-SR policies under a unit-only synthetic borrow-stress fixture that forces cross-event borrows/blend draws — **not** a panel invent |

Both arms keep C_total=5000, R_m=161, residual non-trading, shared-account scoreboard. Soft_policy set is **not** the knob (already Cap-SR).

---

## Scorecard fields (null now)

| Field | Meaning |
|---|---|
| `borrow_count_delta_vs_fifo` | SR1/SR2 borrow/blend-draw count minus SR0 under the arm’s fixture |
| `blend_utilization_gap` | Max−min soft utilization across events |
| `soft_breach_or_blend_rate` | Fraction of fills needing cross-event borrow or blend-pool draw |
| `effects_path_fixture_id` | Which fixture stress produced the (still-null) metrics |

All stay **null** in this freeze / EMPTY_RESULTS until Examiner. Units assert join schema + Cap-SR import + wallet-sum forbid only.

---

## Lab deliverables (implement now)

New dir: `kalshi_cap_sr_effects_000_lab_20260923/` in Astra repo:

- `EXPERIMENT_SPEC.md` + `FROZEN_EXPERIMENT.json` (results/pnl null)  
- Effects harness importing Cap-SR soft_policy engine (no fork of soft_policy math)  
- Prefer production q3300 gzip fills when present; synthetic OK for units  
- Unit tests: FX0/FX1 schema; Cap-SR pin lock; feebook/rails pins; residual non-trading; forbid wallet-sum; no dual `kalshi_soft_blended_*` edits  
- First PR = **unit/instrument + fixture join**; scorecard null  
- Do **not** mutate Cap-SR / capital / feebook / rails / Q / C3 / C5 / R3-P3 labs

---

## Do-not-modify

1. No live orders / no Logan keys.  
2. No Q6-`000` retune; no QF reopen.  
3. No second Cap-SR soft_policy lab — effects path only.  
4. No A1↔A3 re-arm; no inventing PnL.  
5. No `admit.py`.  
6. `results`/`pnl` null until Examiner opens.

---

## Dead-card / orthogonality

- ≠ R3-P3 / C3 / C5 / C1-empty-books.  
- S1 deferred (empty-events stub).  
- Nearest dead: C1 empty-book · Q7 Arm B kill.

---

## Frozen-at

Desk 2026-09-23 ET. Conductor MAXIMIZE NEXT after R3-P3 PR23. Variants owner: R&D Variants.
