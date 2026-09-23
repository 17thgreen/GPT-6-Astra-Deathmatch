# S4 KXNCAAFGAME SETTLED-RESOLUTION JOIN HARNESS — FREEZE KERNEL 2026-09-23 (ET)

**Owner:** R&D Variants (harness freeze) → Collector/Clock admit path → Examiner  
**Status:** FROZEN — Conductor MAXIMIZE NEXT after NHL-RJ PR44 squash-merge main@`b450e780fd9752887579ee8d217b6dee76d918f8`  
**Cite:** Orthogonal pin `MAXIMIZE_PIN_2026-09-23_1643ET.md`; parent panel stub `2026-09-22.s4-kxncaafgame-v0`; settled reget scout `scout_s4_settled_rejoin_2026-09-23/`; prior FQ freeze `S4_KXNCAAFGAME_FEEQUEUE_HARNESS_FREEZE_2026-09-23.md`  
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`  
**Packet ID:** S4-KXNCAAFGAME-SETTLED-RESOLUTION-JOIN-HARNESS  
**Feature family:** **S4-RJ** (KXNCAAFGAME settled-resolution join + Clock-admit readiness) — mirror NHL-RJ / C5-RJ / R3P3-RJ / C3-RJ; **orthogonal to S4-FQ / NCAAF-FQ** (fee+queue Feature sibling; this is NEW Feature, not FQ reopen)  
**Nearest dead card:** Inventing settled `result` / inventing depth/fills OR empty-books invent (C1 PR19 refuse) OR FQ sibling (S4-FQ / NCAAF-FQ closed).  
**Hard rules:** Measurement-only join gate. GET-only. No invent settled result. No Lee-Ready. No Cap-SR/FQ reopen. No Arm B touch. No `admit.py` (Variants does NOT run admit). Does **not** ungate S1/S2/R2-P4. `results`/`pnl` null until Examiner after Clock admit. Examiner **HOLD pre-PR**.

## Why S4-RJ (this slot)

Per Conductor pin rules after NHL-RJ PR44 @`b450e780…` (ACCEPT digests MATCH `ce82d934…`; Examiner READY NOT_SCORED): prefer Examiner-scorable (Clock admit + settled/authentic join). Do **not** freeze KXFED / another FQ sibling. Refiner owns Arm B — do not touch. Prefer not to reopen Cap-SR / C3-RJ / C5-RJ / R3P3-RJ / NHL-RJ (closed).

Primary candidate **S4-RJ** (order #1): capture `astra-capture/s4-kxncaafgame/`; prior FQ freeze for parent SEP26 seeds. **2026-09-23 reget:** GET-only `/events` embeds + single-market on prior-weekend SEP05/SEP12/SEP19 cohort → finalized nonempty `result` **N=18**; series list `status=settled|finalized|open` **429 honest** (do not invent). Parent FQ panel SEP26 seeds remain **active/empty result** (future occ — honest). Candidate **won**. Not R2P3-RJ / S5-RJ / C1-RJ fallback.

## Intent (one knob)

Measurement join only — fee arms already covered on S4-FQ / NCAAF-FQ stub; feebook/rails FIXED import-only if needed, else measurement join without fee arms.

**One knob only:** `join_gate` ∈ {`nonempty_result_required`, `occurrence_datetime_match`}

**Not arms:** inventing settled `result`; inventing depth/fills; Cap-SR/FQ reopen; C3-RJ / C5-RJ / R3P3-RJ / NHL-RJ reopen; Lee-Ready; empty-books invent; Arm B; running `admit.py`.

## Pins

| Pin | Value |
|---|---|
| Orthogonal slot | `MAXIMIZE_PIN_2026-09-23_1643ET.md` — active Feature **S4-RJ** |
| Settled reget scout | `lab/governance/astra/packets/scout_s4_settled_rejoin_2026-09-23/` · settled nonempty result **N=18** · scout sha256 `57fa0b28325ac13015f49521a87661b3cc064d22a13cf960f4fcdfd9badaa3dc` · summary sha256 `9e67cd16f3ec6536d5dae3fe07de6e6b073c1c8d1adc9bb7e9297090ef567ce1` |
| Capture bundle | `lab/astra-capture/s4-kxncaafgame/settled_reget_2026-09-23.json` · sha256 `5bb0acfaa429e2ec1ad22e2e35e296540ac5b8e66eba4df6a0b2419d43257528` |
| Panel stub (parent; admitted_at null) | `lab/governance/astra/packets/S4_KXNCAAFGAME_PANEL_STUB_2026-09-22.json` ≡ `lab/astra-capture/s4-kxncaafgame/panel_stub.json` · sha256 `38167d11da5842bc4d39e6e7dcaab20a67294c735ba14d8bbeafde3154c6342a` · `2026-09-22.s4-kxncaafgame-v0` · **Variants does NOT run admit.py**; keep `admitted_at` null until Collector/Clock |
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

`kalshi_kxncaafgame_settled_join_lab_20260923/` (do not mutate S4-FQ / NHL-RJ / C3-RJ / C5-RJ / R3P3-RJ / Cap-SR / FQ siblings / feebook / rails / Arm B / S1/S2/R2-P4).

## Integrity (Clock gate)

Commit attached freeze / scout reget / panel stub bytes **verbatim**. Pin digests to `sha256sum`. **Refuse inventing settled result / depth / fills / PnL.** Series settled/finalized/open list 429 remain honest gaps — do not backfill. Parent SEP26 FQ seeds not yet settled — do not invent. Scout N=18 is a pin — do **not** copy into `settled_join_n`.

## Merge gates

Units green when implemented; `results`/`pnl` null; Examiner HOLD pre-PR → READY NOT_SCORED only after PR branch sha verify + merge + Clock admit path.

## Refuse binds

invent settled `result`/depth/fills/PnL · Lee-Ready · Cap-SR/QF/L2/EMPTY-OB/SOT-ID/L2-SF/NHL-FQ/CPI-FQ/ATP-FQ/ETH-FQ/S4-FQ/C3-RJ/C5-RJ/R3P3-RJ/NHL-RJ reopen · ungate S1/S2/R2-P4 · Arm B touch · `admit.py` by Variants · KXFED/another FQ freeze · empty-books invent (C1 PR19) · live orders
