# R2P3 KXNFLPASSYDS SETTLED-RESOLUTION JOIN HARNESS — FREEZE KERNEL 2026-09-23 (ET)

**Owner:** R&D Variants (harness freeze) → Collector/Clock admit path → Examiner  
**Status:** FROZEN — Conductor MAXIMIZE NEXT after S4-RJ PR45 squash-merge main@`aeff380b29dbe89b16da58f9e15e58415b42b147`  
**Cite:** Orthogonal pin `MAXIMIZE_PIN_2026-09-23_1712ET.md`; parent panel stub `2026-09-22.r2-p3-prop-slate-v0`; settled reget scout `scout_r2p3_settled_rejoin_2026-09-23/`; prior prop-ladder freeze `R2_P3_KXNFLPASSYDS_PROP_LADDER_HARNESS_FREEZE_2026-09-23.md`  
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`  
**Packet ID:** R2P3-KXNFLPASSYDS-SETTLED-RESOLUTION-JOIN-HARNESS  
**Feature family:** **R2P3-RJ** (KXNFLPASSYDS prop-slate settled-resolution join + Clock-admit readiness) — mirror S4-RJ / NHL-RJ / C5-RJ / R3P3-RJ / C3-RJ; **orthogonal to R2-P3 prop-ladder / PASSYDS-PROP** (fee+ladder Feature sibling; this is NEW Feature, not FQ/prop-ladder reopen)  
**Nearest dead card:** Inventing settled `result` / inventing depth/fills OR empty-books invent (C1 PR19 refuse) OR FQ/prop-ladder sibling (R2-P3 prop-ladder / PASSYDS-PROP closed).  
**Hard rules:** Measurement-only join gate. GET-only. No invent settled result. No Lee-Ready. No Cap-SR/FQ reopen. No Arm B touch. No `admit.py` (Variants does NOT run admit). Does **not** ungate S1/S2/R2-P4. `results`/`pnl` null until Examiner after Clock admit. Examiner **HOLD pre-PR**.

## Why R2P3-RJ (this slot)

Per Conductor pin rules after S4-RJ PR45 @`aeff380b…` (ACCEPT digests MATCH `87bb8d44…`; Examiner READY NOT_SCORED): prefer Examiner-scorable (Clock admit + settled/authentic join). Do **not** freeze KXFED / another FQ sibling. Refiner owns Arm B — do not touch. Prefer not to reopen Cap-SR / C3-RJ / C5-RJ / R3P3-RJ / NHL-RJ / S4-RJ (closed).

Primary candidate **R2P3-RJ** (order #1): capture `astra-capture/r2-p3-prop-slate/`; prior prop-ladder harness + panel stub for parent SEP27 seeds. **2026-09-23 reget:** GET-only `/markets?series_ticker=KXNFLPASSYDS&status=settled&limit=20` → finalized nonempty `result` **N=20** (SEP20/SEP21 cohort); finalized/events_closed/events_settled lists **429 honest**; close-window params **400 honest**. Parent SEP27 prop-ladder seeds remain **active/empty result** (future occ — honest). ATL@GB SEP24 active/empty excluded (NOT ATL@GB). Candidate **won**. Not S5-RJ / C1-RJ fallback.

## Intent (one knob)

Measurement join only — prop-ladder fee arms already covered on R2-P3 prop-ladder stub; feebook/rails FIXED import-only if needed, else measurement join without fee arms.

**One knob only:** `join_gate` ∈ {`nonempty_result_required`, `occurrence_datetime_match`}

**Not arms:** inventing settled `result`; inventing depth/fills; Cap-SR/FQ reopen; C3-RJ / C5-RJ / R3P3-RJ / NHL-RJ / S4-RJ reopen; Lee-Ready; empty-books invent; Arm B; running `admit.py`.

## Pins

| Pin | Value |
|---|---|
| Orthogonal slot | `MAXIMIZE_PIN_2026-09-23_1712ET.md` — active Feature **R2P3-RJ** |
| Settled reget scout | `lab/governance/astra/packets/scout_r2p3_settled_rejoin_2026-09-23/` · settled nonempty result **N=20** · (digests in DIGESTS.txt) |
| Capture bundle | `lab/astra-capture/r2-p3-prop-slate/settled_reget_2026-09-23.json` |
| Panel stub (parent; admitted_at null) | `lab/governance/astra/packets/R2_P3_PROP_SLATE_PANEL_STUB_2026-09-22.json` ≡ `lab/astra-capture/r2-p3-prop-slate/panel_stub.json` · sha256 `70e879e8738d033f392d821849dee3537af3e7b8a916670779d238f78ce098be` · `2026-09-22.r2-p3-prop-slate-v0` · **Variants does NOT run admit.py**; keep `admitted_at` null until Collector/Clock |
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

`kalshi_r2p3_kxnflpassyds_settled_join_lab_20260923/` (do not mutate R2-P3 prop-ladder / S4-RJ / NHL-RJ / C3-RJ / C5-RJ / R3P3-RJ / Cap-SR / FQ siblings / feebook / rails / Arm B / S1/S2/R2-P4).

## Integrity (Clock gate)

Commit attached freeze / scout reget / panel stub bytes **verbatim**. Pin digests to `sha256sum`. **Refuse inventing settled result / depth / fills / PnL.** Finalized/events list 429 and close-window 400 remain honest gaps — do not backfill. Parent SEP27 prop-ladder seeds not yet settled — do not invent. Scout N=20 is a pin — do **not** copy into `settled_join_n`.

## Merge gates

Units green when implemented; `results`/`pnl` null; Examiner HOLD pre-PR → READY NOT_SCORED only after PR branch sha verify + merge + Clock admit path.

## Refuse binds

invent settled `result`/depth/fills/PnL · Lee-Ready · Cap-SR/QF/L2/EMPTY-OB/SOT-ID/L2-SF/NHL-FQ/CPI-FQ/ATP-FQ/ETH-FQ/S4-FQ/R2-P3-prop-ladder/C3-RJ/C5-RJ/R3P3-RJ/NHL-RJ/S4-RJ reopen · ungate S1/S2/R2-P4 · Arm B touch · `admit.py` by Variants · KXFED/another FQ freeze · empty-books invent (C1 PR19) · live orders
