# C5 KXBTC15M SETTLED-RESOLUTION JOIN HARNESS — FREEZE KERNEL 2026-09-23 (ET)

**Owner:** R&D Variants (harness freeze) → Collector/Clock admit path → Examiner  
**Status:** FROZEN — Conductor MAXIMIZE NEXT after C3-RJ PR40 squash-merge main@`9fd5d7cb89693a0ed29d9e97d2b723c0810989bc`  
**Cite:** Orthogonal pin `MAXIMIZE_PIN_2026-09-23_1518ET.md`; prior Clock join CONDITIONAL ADMIT REFUSED (settled N=0) `CLOCK_JOIN_C5_KXBTC15M_2026-09-22.md`; parent panel stub `2026-09-22.c5-kxbtc15m-v0`; settled reget scout `scout_c5_settled_rejoin_2026-09-23/`  
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`  
**Packet ID:** C5-KXBTC15M-SETTLED-RESOLUTION-JOIN-HARNESS  
**Feature family:** **C5-RJ** (settled-resolution join + Clock-admit readiness) — orthogonal to C5 honesty/fee-queue measurement (PR21 Feature done; this is NEW Feature, not C5 reopen)  
**Nearest dead card:** Inventing settled `result` / inventing depth/fills OR empty-books invent (C1 PR19 refuse) OR FQ sibling.  
**Hard rules:** Measurement-only join gate. GET-only. No invent settled result. No Lee-Ready. No Cap-SR/FQ reopen. No Arm B touch. No `admit.py` (Variants does NOT run admit). Does **not** ungate S1/S2/R2-P4. `results`/`pnl` null until Examiner after Clock admit. Examiner **HOLD pre-PR**.

## Why C5-RJ (this slot)

Per Conductor pin rules after C3-RJ PR40 @`9fd5d7cb…`: prefer Examiner-scorable (Clock admit + settled/authentic join). Do **not** freeze KXFED / another FQ sibling. Refiner owns Arm B — do not touch.

Primary candidate C5 KXBTC15M: prior Clock join refused on settled N=0 (`packets/CLOCK_JOIN_C5_KXBTC15M_2026-09-22.md` / capture `astra-capture/c5-kxbtc15m/`). **2026-09-23 reget:** `GET /markets?series_ticker=KXBTC15M&status=settled&limit=20` → settled/finalized nonempty `result` **N=20**; parent seed `KXBTC15M-26SEP222045-45` also **finalized** with nonempty `result=no`. Open list still has rolling active window (parent stub kept; `admitted_at` null). Candidate **won** — no R3P3-RJ fallback needed. Honest gaps: `status=finalized` and `status=closed` list filters **429** (do not invent).

## Intent (one knob)

Measurement join only — fee arms already covered elsewhere; feebook/rails FIXED import-only if honesty path needs labels, else measurement join without fee arms.

**One knob only:** `join_gate` ∈ {`nonempty_result_required`, `occurrence_datetime_match`}

**Not arms:** inventing settled `result`; inventing depth/fills; Cap-SR/FQ reopen; C5 honesty reopen; Lee-Ready; empty-books invent; Arm B; running `admit.py`.

## Pins

| Pin | Value |
|---|---|
| Orthogonal slot | `MAXIMIZE_PIN_2026-09-23_1518ET.md` — active Feature **C5-RJ** |
| Prior Clock join | `CLOCK_JOIN_C5_KXBTC15M_2026-09-22.md` — ADMIT REFUSED / settled N=0 (historical) |
| Settled reget scout | `lab/governance/astra/packets/scout_c5_settled_rejoin_2026-09-23/` · settled nonempty result **N=20** · scout sha256 `7be17c44aef31abf7a0ab94938d0289f8766670ddacefdec566735818e044796` · summary sha256 `b39c919809f709bcb81ff10a3d983b266bc7a1303c0de502c7c20be726415198` |
| Capture bundle | `lab/astra-capture/c5-kxbtc15m/settled_reget_2026-09-23.json` · sha256 `319d6d3e394089fd21fefbfaa52c58166e78c2d781077a3f876331d2c54de617` |
| Panel stub (parent; admitted_at null) | `lab/governance/astra/packets/C5_KXBTC15M_PANEL_STUB_2026-09-22.json` ≡ `lab/astra-capture/c5-kxbtc15m/panel_stub.json` · sha256 `60f613e8d775b66b9044ad31d2faf77bba84176f214a7bce599aa7a65b6905f8` · `2026-09-22.c5-kxbtc15m-v0` · **Variants does NOT run admit.py**; keep `admitted_at` null until Collector/Clock |
| Fee (FIXED import-only if needed) | `kalshi_feebook_lab_20260922/` @`22371178cb2663250b4762f328069571c48cb551` |
| Rails (FIXED import-only if needed) | `kalshi_rails_lab_20260922/` @`6a28e0d6254327ea4e6451c781bec56215ac6cac` |
| Capture | GET-only public — no trading host; no Logan keys; **not live crypto trading** |
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

`kalshi_c5_kxbtc15m_settled_join_lab_20260923/` (do not mutate C5 honesty lab / Cap-SR / FQ siblings / feebook / rails / Arm B / S1/S2/R2-P4 / C3-RJ).

## Integrity (Clock gate)

Commit attached freeze / scout reget / panel stub bytes **verbatim**. Pin digests to `sha256sum`. **Refuse inventing settled result / depth / fills / PnL.** Finalized/closed list 429 remains honest gap — do not backfill. Series rotates 15m — do not invent expired windows.

## Merge gates

Units green when implemented; `results`/`pnl` null; Examiner HOLD pre-PR → READY NOT_SCORED only after PR branch sha verify + merge + Clock admit path.

## Refuse binds

invent settled `result`/depth/fills/PnL · Lee-Ready · Cap-SR/QF/L2/EMPTY-OB/SOT-ID/L2-SF/NHL-FQ/CPI-FQ/ATP-FQ/ETH-FQ/C3-RJ reopen · C5 honesty reopen as this Feature · ungate S1/S2/R2-P4 · Arm B touch · `admit.py` by Variants · KXFED/another FQ freeze · empty-books invent (C1 PR19) · live crypto trading
