# C1 KXUFCFIGHT SETTLED-RESOLUTION JOIN HARNESS — FREEZE KERNEL 2026-09-23 (ET)

**Owner:** R&D Variants (harness freeze) → Collector/Clock admit path → Examiner  
**Status:** FROZEN — Conductor MAXIMIZE NEXT after S5-RJ PR48 squash-merge main@`fec05e8cf7c11f1c975ab791fda64f896d40d1cd`  
**Cite:** Orthogonal pin `MAXIMIZE_PIN_2026-09-23_1750ET.md`; merge cite `packets/CONDUCTOR_MERGE_S5_KXMVECROSSCATEGORY_SETTLED_JOIN_HARNESS_PR48_2026-09-23.json` (ACCEPT digests MATCH `49567517…`; results/pnl/settled_join_n null; scout N=20 pin-only); prior Clock rejoin `CLOCK_JOIN_C1_KXUFCFIGHT_REJOIN_2026-09-22.md`; parent panel stub `2026-09-22.c1-kxufcfight-v0`; prior MEAS freeze `C1_KXUFCFIGHT_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md`; EMPTY-OB PR19 refuse (nearest dead); admit-wire PR39 merge (Collector admit stamp already on panel — Variants does NOT re-run admit.py)  
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`  
**Packet ID:** C1-KXUFCFIGHT-SETTLED-RESOLUTION-JOIN-HARNESS  
**Feature family:** **C1-RJ** (KXUFCFIGHT UFC settled-resolution join + Clock-admit readiness) — mirror S5-RJ / R2P3-RJ / NHL-RJ / S4-RJ / C5-RJ / R3P3-RJ / C3-RJ; **NOT FQ sibling**; orthogonal to C1 EMPTY-OB / MEAS / admit-wire Features (those closed; this is NEW Feature)  
**Nearest dead card:** Inventing settled `result` / inventing depth/fills OR **empty-books invent** (C1 PR19 refuse) OR invent books.  
**Hard rules:** Measurement-only join gate. GET-only. No invent settled result. No Lee-Ready. No Cap-SR/FQ reopen. No Arm B touch. No `admit.py` (Variants does NOT run admit). Does **not** ungate S1/S2/R2-P4 (held until C1 T−7d smoke — this freeze does not claim that smoke). `results`/`pnl` null until Examiner after Clock admit. Examiner **HOLD pre-PR**.

## Why C1-RJ (this slot)

Per Conductor pin rules after S5-RJ PR48 @`fec05e8c…` (ACCEPT digests MATCH `49567517…`; results/pnl/settled_join_n null; next_maximize C1-RJ): prefer Examiner-scorable (Clock admit + settled/authentic join). Do **not** freeze KXFED / another FQ sibling. Refiner owns Arm B — do not touch. Prefer not to reopen Cap-SR / C3-RJ / C5-RJ / R3P3-RJ / NHL-RJ / S4-RJ / R2P3-RJ / S5-RJ / FQ siblings (closed).

Primary candidate **C1-RJ** (order #1): capture `astra-capture/c1-kxufcfight/`; prior MEAS + EMPTY-OB + admit-wire + Clock rejoin + panel stub for parent seeds. **2026-09-23 reget:** GET-only parent-seed `/markets/{ticker}` → finalized nonempty `result` **N=4**; series **200**; settled/finalized/events list attempts **429 honest** (retries x3 still 429 — do not invent list books). `occurrence_datetime` present on all 4 parent seeds and matches panel SoT. Candidate **won**. Not FQ sibling.

## Intent (one knob)

Measurement join only — EMPTY-OB empty-book arms already covered on C1 EMPTY-OB / PR19 refuse; feebook/rails FIXED import-only if needed, else measurement join without fee arms.

**One knob only:** `join_gate` ∈ {`nonempty_result_required`, `occurrence_datetime_match`}

**Not arms:** inventing settled `result`; inventing depth/fills; empty-books invent (C1 PR19); Cap-SR/FQ reopen; C3-RJ / C5-RJ / R3P3-RJ / NHL-RJ / S4-RJ / R2P3-RJ / S5-RJ reopen; Lee-Ready; Arm B; running `admit.py`; ungating S1/S2/R2-P4.

## Pins

| Pin | Value |
|---|---|
| Orthogonal slot | `MAXIMIZE_PIN_2026-09-23_1750ET.md` — active Feature **C1-RJ** |
| Settled reget scout | `lab/governance/astra/packets/scout_c1_settled_rejoin_2026-09-23/` · settled nonempty result **N=4** (parent seed GETs; list 429 honest) |
| Capture bundle | `lab/astra-capture/c1-kxufcfight/settled_reget_2026-09-23.json` |
| Panel stub (parent; prior Collector admitted_at present) | `lab/governance/astra/packets/C1_KXUFCFIGHT_PANEL_STUB_2026-09-22.json` ≡ `lab/astra-capture/c1-kxufcfight/panel_stub.json` · sha256 `24426d804c51bde23cf2557a11a8481a12026da10024094c4ae546d1f7d3956e` · `2026-09-22.c1-kxufcfight-v0` · prior Collector `admitted_at=2026-09-23T00:49:43Z` — **Variants does NOT run admit.py**; FROZEN_EXPERIMENT.admitted_at stays null |
| Fee (FIXED import-only if needed) | `kalshi_feebook_lab_20260922/` @22371178cb2663250b4762f328069571c48cb551 · series `quadratic` / multiplier 1 |
| Rails (FIXED import-only if needed) | `kalshi_rails_lab_20260922/` @6a28e0d6254327ea4e6451c781bec56215ac6cac |
| Capture | GET-only public — no trading host; no Logan keys; no `/communications` RFQ |
| Strategy | **None** — join measurement only |

## Arms (join_gate knob only)

| Arm | Name | Gate |
|---|---|---|
| **J0** | Nonempty result required | `join_gate=nonempty_result_required` — Clock-admit readiness when settled markets have non-empty official `result` |
| **J1** | Occurrence datetime match | `join_gate=occurrence_datetime_match` — SoT `occurrence_datetime` matches live_get / seed when present (present on all 4 parent seeds here) — do not invent `occurrence_datetime` |

Both arms share identical panel parent + GET-only reget pins. No fee-arm dual; no invent.

## Scorecard fields (null now)

`settled_join_n`, `occurrence_match_n`, `admit_ready_flag`, `results`, `pnl` — **null** until Clock admit + Examiner. Scout N=4 is a pin — do **not** copy into `settled_join_n`.

## Lab dir

`kalshi_c1_kxufcfight_settled_join_lab_20260923/` (do not mutate C1 EMPTY-OB / MEAS / admit-wire / S5-RJ / R2P3-RJ / NHL-RJ / S4-RJ / C3-RJ / C5-RJ / R3P3-RJ / Cap-SR / FQ siblings / feebook / rails / Arm B / S1/S2/R2-P4).

## Integrity (Clock gate)

Commit attached freeze / scout reget / panel stub bytes **verbatim**. Pin digests to `sha256sum`. **Refuse inventing settled result / depth / fills / PnL / empty books.** Settled/finalized/events list 429s remain honest gaps — do not backfill list books. Scout N=4 is a pin — do **not** copy into `settled_join_n`.

## Merge gates

Units green when implemented; `results`/`pnl` null; Examiner HOLD pre-PR → READY NOT_SCORED only after PR branch sha verify + merge + Clock admit path. **HOLD for Conductor ACCEPT — no CloudAgent / no PR / no admit.py / no live orders.**

## Refuse binds

invent settled `result`/depth/fills/PnL · empty-books invent (C1 PR19) · invent books · Lee-Ready · Cap-SR/QF/L2/EMPTY-OB/SOT-ID/L2-SF/NHL-FQ/CPI-FQ/ATP-FQ/ETH-FQ/S4-FQ/R2-P3-prop-ladder/S5-FILLLEGS/C3-RJ/C5-RJ/R3P3-RJ/NHL-RJ/S4-RJ/R2P3-RJ/S5-RJ reopen · ungate S1/S2/R2-P4 · Arm B touch · `admit.py` by Variants · KXFED/another FQ freeze · live orders · Conductor pulse cloud on RJ
