# R3-P3 FL MAKER/TAKER SETTLED-RESOLUTION JOIN HARNESS — FREEZE KERNEL 2026-09-23 (ET)

**Owner:** R&D Variants (harness freeze) → Collector/Clock admit path → Examiner  
**Status:** FROZEN — Conductor MAXIMIZE NEXT after C5-RJ PR41 squash-merge main@`8cfcd17a62d3793dee554a4da422e8075bde9cf6`  
**Cite:** Orthogonal pin `MAXIMIZE_PIN_2026-09-23_1533ET.md`; prior Clock join CONDITIONAL ADMIT REFUSED (settled N=0) `CLOCK_JOIN_R3_P3_FL_MAKER_TAKER_2026-09-22.md`; parent panel stub `2026-09-22.r3-p3-fl-maker-taker-v0`; settled reget scout `scout_r3p3_settled_rejoin_2026-09-23/`  
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`  
**Packet ID:** R3P3-FL-MAKER-TAKER-SETTLED-RESOLUTION-JOIN-HARNESS  
**Feature family:** **R3P3-RJ** (R3-P3 FL maker/taker settled-resolution join + Clock-admit readiness) — mirror C3-RJ / C5-RJ; orthogonal to R3-P3 fee/bands measurement stub (not an FQ sibling; not C3-RJ reopen)  
**Nearest dead card:** Inventing settled `result` / inventing depth/fills OR empty-books invent (C1 PR19 refuse) OR FQ sibling.  
**Hard rules:** Measurement-only join gate. GET-only. No invent settled result. No Lee-Ready. No Cap-SR/FQ reopen. No Arm B touch. No `admit.py` (Variants does NOT run admit). Does **not** ungate S1/S2/R2-P4. `results`/`pnl` null until Examiner after Clock admit. Examiner **HOLD pre-PR**.

## Why R3P3-RJ (this slot)

Per Conductor pin rules after C5-RJ PR41 @`8cfcd17a…`: prefer Examiner-scorable (Clock admit + settled/authentic join). Do **not** freeze KXFED / another FQ sibling. Refiner owns Arm B — do not touch. Prefer not to reopen C3-RJ (closed).

Primary candidate R3-P3 FL maker/taker: prior Clock join refused on settled N=0 (`packets/CLOCK_JOIN_R3_P3_FL_MAKER_TAKER_2026-09-22.md` / capture `astra-capture/r3-p3-fl-maker-taker/`). **2026-09-23 reget:** `GET /markets?series_ticker=KXHIGHNY&status=settled&limit=20` → settled/finalized nonempty `result` **N=20**; all 3 parent seed tickers (`KXHIGHNY-26SEP22-B67.5`, `KXHIGHNY-26SEP22-T70`, `KXHIGHCHI-26SEP22-B64.5`) **finalized** with nonempty `result`; `occurrence_datetime` SoT **2026-09-23T14:00:00Z** matches panel live_get for all seeds. Candidate **won**. Honest gaps: `KXHIGHCHI` settled list **429**; `KXHIGHNY` open list **429** (do not invent).

## Intent (one knob)

Measurement join only — fee arms / bands already covered on R3-P3 stub; feebook/rails FIXED import-only if needed, else measurement join without fee arms.

**One knob only:** `join_gate` ∈ {`nonempty_result_required`, `occurrence_datetime_match`}

**Not arms:** inventing settled `result`; inventing depth/fills; Cap-SR/FQ reopen; C3-RJ / C5-RJ reopen; Lee-Ready; empty-books invent; Arm B; running `admit.py`.

## Pins

| Pin | Value |
|---|---|
| Orthogonal slot | `MAXIMIZE_PIN_2026-09-23_1533ET.md` — active Feature **R3P3-RJ** |
| Prior Clock join | `CLOCK_JOIN_R3_P3_FL_MAKER_TAKER_2026-09-22.md` — ADMIT REFUSED / settled N=0 (historical) |
| Settled reget scout | `lab/governance/astra/packets/scout_r3p3_settled_rejoin_2026-09-23/` · settled nonempty result **N=20** · scout sha256 `f675d7c40ccad37173b2cb54837349cd3053b7b76606c43efba5759a1bde551f` · summary sha256 `b43d4ab065b712f5bf1b87eb164bccb00e8e9993f97db9d86a8d1619ce9ec13d` |
| Capture bundle | `lab/astra-capture/r3-p3-fl-maker-taker/settled_reget_2026-09-23.json` · sha256 `c5f680e4ff66af67691672c4b8c43eb57906f25b4d79fdeb65f61e031c13efda` |
| Panel stub (parent; admitted_at null) | `lab/governance/astra/packets/R3_P3_FL_MAKER_TAKER_PANEL_STUB_2026-09-22.json` ≡ `lab/astra-capture/r3-p3-fl-maker-taker/panel_stub.json` · sha256 `6f640dd3a6091ba6b896ded38fdded4676583aa3c885223da21ddf03780250c0` · `2026-09-22.r3-p3-fl-maker-taker-v0` · **Variants does NOT run admit.py**; keep `admitted_at` null until Collector/Clock |
| Fee (FIXED import-only if needed) | `kalshi_feebook_lab_20260922/` @`22371178cb2663250b4762f328069571c48cb551` |
| Rails (FIXED import-only if needed) | `kalshi_rails_lab_20260922/` @`6a28e0d6254327ea4e6451c781bec56215ac6cac` |
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

`kalshi_r3p3_fl_settled_join_lab_20260923/` (do not mutate C3-RJ / C5-RJ / Cap-SR / FQ siblings / feebook / rails / Arm B / S1/S2/R2-P4 / R3-P3 bands stub).

## Integrity (Clock gate)

Commit attached freeze / scout reget / panel stub bytes **verbatim**. Pin digests to `sha256sum`. **Refuse inventing settled result / depth / fills / PnL.** KXHIGHCHI settled list 429 + KXHIGHNY open 429 remain honest gaps — do not backfill. Do not invent prior-day tickers.

## Merge gates

Units green when implemented; `results`/`pnl` null; Examiner HOLD pre-PR → READY NOT_SCORED only after PR branch sha verify + merge + Clock admit path.

## Refuse binds

invent settled `result`/depth/fills/PnL · Lee-Ready · Cap-SR/QF/L2/EMPTY-OB/SOT-ID/L2-SF/NHL-FQ/CPI-FQ/ATP-FQ/ETH-FQ/C3-RJ/C5-RJ reopen · ungate S1/S2/R2-P4 · Arm B touch · `admit.py` by Variants · KXFED/another FQ freeze · empty-books invent (C1 PR19) · live orders
