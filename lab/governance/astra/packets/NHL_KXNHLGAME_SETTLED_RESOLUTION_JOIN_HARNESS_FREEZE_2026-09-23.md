# NHL KXNHLGAME SETTLED-RESOLUTION JOIN HARNESS — FREEZE KERNEL 2026-09-23 (ET)

**Owner:** R&D Variants (harness freeze) → Collector/Clock admit path → Examiner  
**Status:** FROZEN — Conductor MAXIMIZE NEXT after R3P3-RJ PR42 squash-merge main@`2fce8642d1b1961cbe0ef60fae1411cd8906f31a`  
**Cite:** Orthogonal pin `MAXIMIZE_PIN_2026-09-23_1556ET.md`; parent panel stub `2026-09-23.c2-kxnhlgame-v0`; settled reget scout `scout_nhl_settled_rejoin_2026-09-23/`; prior FQ freeze seed tickers from `scout_cashcow_hunt_2026-09-22/scout_hunt_KXNHLGAME.json`  
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`  
**Packet ID:** NHL-KXNHLGAME-SETTLED-RESOLUTION-JOIN-HARNESS  
**Feature family:** **NHL-RJ** (KXNHLGAME settled-resolution join + Clock-admit readiness) — mirror C3-RJ / C5-RJ / R3P3-RJ; **orthogonal to NHL-FQ** (C2 fee+queue Feature done; this is NEW Feature, not FQ reopen)  
**Nearest dead card:** Inventing settled `result` / inventing depth/fills OR empty-books invent (C1 PR19 refuse) OR FQ sibling (NHL-FQ closed).  
**Hard rules:** Measurement-only join gate. GET-only. No invent settled result. No Lee-Ready. No Cap-SR/FQ reopen. No Arm B touch. No `admit.py` (Variants does NOT run admit). Does **not** ungate S1/S2/R2-P4. `results`/`pnl` null until Examiner after Clock admit. Examiner **HOLD pre-PR**.

## Why NHL-RJ (this slot)

Per Conductor pin rules after R3P3-RJ PR42 @`2fce8642…`: prefer Examiner-scorable (Clock admit + settled/authentic join). Do **not** freeze KXFED / another FQ sibling. Refiner owns Arm B — do not touch. Prefer not to reopen Cap-SR / C3-RJ / C5-RJ / R3P3-RJ (closed).

Primary candidate **NHL-RJ** (order #1): capture `astra-capture/c2-kxnhlgame/`; prior FQ freeze for seed tickers. **2026-09-23 reget:** GET-only single-market on overnight SEP22 hunt cohort → finalized nonempty `result` **N=17**; series list `status=settled|finalized|open` **429 honest** (do not invent). Parent FQ panel SEP26 seeds remain **active/empty result** (future occ — honest). Candidate **won**. Not S4-RJ / R2P3-RJ / S5-RJ / C1-RJ fallback.

## Intent (one knob)

Measurement join only — fee arms already covered on NHL-FQ / C2 stub; feebook/rails FIXED import-only if needed, else measurement join without fee arms.

**One knob only:** `join_gate` ∈ {`nonempty_result_required`, `occurrence_datetime_match`}

**Not arms:** inventing settled `result`; inventing depth/fills; Cap-SR/FQ reopen; C3-RJ / C5-RJ / R3P3-RJ reopen; Lee-Ready; empty-books invent; Arm B; running `admit.py`.

## Pins

| Pin | Value |
|---|---|
| Orthogonal slot | `MAXIMIZE_PIN_2026-09-23_1556ET.md` — active Feature **NHL-RJ** |
| Settled reget scout | `lab/governance/astra/packets/scout_nhl_settled_rejoin_2026-09-23/` · settled nonempty result **N=17** · scout sha256 `99a7f90564ee2150f5edef4efafb7ccb954b87036e0b43f29ff7dc6ed104706f` · summary sha256 `794e148df5927c64d08b4578b47a7453589f02872af65880922bcb9273194a1a` |
| Capture bundle | `lab/astra-capture/c2-kxnhlgame/settled_reget_2026-09-23.json` · sha256 `8d597578bc65ea14ab1cbf5aa3c6d121d61431078a755b8419c815aa1d354df0` |
| Panel stub (parent; admitted_at null) | `lab/governance/astra/packets/C2_KXNHLGAME_PANEL_STUB_2026-09-23.json` ≡ `lab/astra-capture/c2-kxnhlgame/panel_stub.json` · sha256 `60d183e7bdcf25adbc94eeeb3bb361b5232c19c0fe3e6a115f45ab3fcb100c79` · `2026-09-23.c2-kxnhlgame-v0` · **Variants does NOT run admit.py**; keep `admitted_at` null until Collector/Clock |
| Fee (FIXED import-only if needed) | `kalshi_feebook_lab_20260922/` @22371178cb2663250b4762f328069571c48cb551 |
| Rails (FIXED import-only if needed) | `kalshi_rails_lab_20260922/` @6a28e0d6254327ea4e6451c781bec56215ac6cac |
| Capture | GET-only public — no trading host; no Logan keys |
| Strategy | **None** — join measurement only |

## Arms (join_gate knob only)

| Arm | Name | Gate |
|---|---|---|
| **J0** | Nonempty result required | `join_gate=nonempty_result_required` — Clock-admit readiness when settled markets have non-empty official `result` |
| **J1** | Occurrence datetime match | `join_gate=occurrence_datetime_match` — SoT `occurrence_datetime` matches live_get / seed for join integrity |

Both arms share identical panel parent + GET-only reget pins. No fee-arm dual; no invent.

## Scorecard fields (null now)

`settled_join_n`, `occurrence_match_n`, `admit_ready_flag`, `results`, `pnl` — **null** until Clock admit + Examiner.

## Lab dir

`kalshi_kxnhlgame_settled_join_lab_20260923/` (do not mutate NHL-FQ / C3-RJ / C5-RJ / R3P3-RJ / Cap-SR / FQ siblings / feebook / rails / Arm B / S1/S2/R2-P4).

## Integrity (Clock gate)

Commit attached freeze / scout reget / panel stub bytes **verbatim**. Pin digests to `sha256sum`. **Refuse inventing settled result / depth / fills / PnL.** Series settled/finalized/open list 429 remain honest gaps — do not backfill. Parent SEP26 FQ seeds not yet settled — do not invent.

## Merge gates

Units green when implemented; `results`/`pnl` null; Examiner HOLD pre-PR → READY NOT_SCORED only after PR branch sha verify + merge + Clock admit path.

## Refuse binds

invent settled `result`/depth/fills/PnL · Lee-Ready · Cap-SR/QF/L2/EMPTY-OB/SOT-ID/L2-SF/NHL-FQ/CPI-FQ/ATP-FQ/ETH-FQ/C3-RJ/C5-RJ/R3P3-RJ reopen · ungate S1/S2/R2-P4 · Arm B touch · `admit.py` by Variants · KXFED/another FQ freeze · empty-books invent (C1 PR19) · live orders
