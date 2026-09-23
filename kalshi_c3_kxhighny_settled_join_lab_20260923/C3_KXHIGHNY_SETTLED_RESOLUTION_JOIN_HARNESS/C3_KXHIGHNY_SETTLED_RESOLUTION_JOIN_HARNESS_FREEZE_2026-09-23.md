# C3 KXHIGHNY SETTLED-RESOLUTION JOIN HARNESS — FREEZE KERNEL 2026-09-23 (ET)

**Owner:** R&D Variants (harness freeze) → Collector/Clock admit path → Examiner  
**Status:** FROZEN — Conductor MAXIMIZE NEXT after ETH-FQ PR36 merge @`82bf7bb99bcc618b912255cc24022b23f9f15047`  
**Cite:** Orthogonal pin `MAXIMIZE_PIN_2026-09-23_1457ET.md`; prior Clock join CONDITIONAL ADMIT REFUSED (settled N=0) `CLOCK_JOIN_C3_KXHIGHNY_2026-09-22.md`; parent panel stub `2026-09-22.c3-kxhighny-v0`; settled reget scout `scout_c3_settled_rejoin_2026-09-23/`  
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`  
**Packet ID:** C3-KXHIGHNY-SETTLED-RESOLUTION-JOIN-HARNESS  
**Feature family:** **C3-RJ** (settled-resolution join + Clock-admit readiness) — orthogonal to C3 bordering-strike algebra (PR22 Feature done; this is NEW Feature, not C3 reopen)  
**Nearest dead card:** Inventing settled `result` / inventing depth/fills OR empty-books invent (C1 PR19 refuse).  
**Hard rules:** Measurement-only join gate. GET-only. No invent settled result. No Lee-Ready. No Cap-SR/FQ reopen. No Arm B touch. No `admit.py` (Variants does NOT run admit). Does **not** ungate S1/S2/R2-P4. `results`/`pnl` null until Examiner after Clock admit. Examiner **HOLD pre-PR**.

## Why C3-RJ (this slot)

Per `MAXIMIZE_PIN_2026-09-23_1455ET` / `1457ET`: prefer Examiner-scorable (Clock admit + settled/authentic join). ETH-FQ done. Do **not** freeze KXFED / another FQ sibling. Refiner owns Arm B — do not touch.

Primary candidate C3 KXHIGHNY: prior Clock join refused on settled N=0. **2026-09-23 reget:** settled nonempty `result` **N=4** (3× NY SEP22 finalized + 1× CHI SEP22 finalized; 1× CHI still 429 honest; 1× NY SEP23 still active). Candidate **won** — no C5-RJ / R3P3-RJ fallback needed.

## Intent (one knob)

Measurement join only — fee arms already covered elsewhere; feebook/rails FIXED import-only if honesty path needs labels, else measurement join without fee arms.

**One knob only:** `join_gate` ∈ {`nonempty_result_required`, `occurrence_datetime_match`}

**Not arms:** inventing settled `result`; inventing depth/fills; Cap-SR/FQ reopen; C3 bordering reopen; Lee-Ready; empty-books invent; Arm B; running `admit.py`.

## Pins

| Pin | Value |
|---|---|
| Orthogonal slot | `MAXIMIZE_PIN_2026-09-23_1457ET.md` — active Feature **C3-RJ** |
| Prior Clock join | `CLOCK_JOIN_C3_KXHIGHNY_2026-09-22.md` — ADMIT REFUSED / settled N=0 (historical) |
| Settled reget scout | `lab/governance/astra/packets/scout_c3_settled_rejoin_2026-09-23/` · settled nonempty result **N=4** · scout sha256 `e8950352745007d3cb565050161430807fa5de70d15321bb00bede6ca9ac18ee` · summary sha256 `b32bbf3200649bcea4fb61a98a4869d5123060a57702a9327262cccbc8e1ca93` |
| Capture bundle | `lab/astra-capture/c3-kxhighny/settled_reget_2026-09-23.json` · sha256 `0055faae508ba034eb49a12d52713566cbfe20bfbfbd2a16203ef350152ac24a` |
| Panel stub (parent; admitted_at null) | `lab/governance/astra/packets/C3_KXHIGHNY_PANEL_STUB_2026-09-22.json` ≡ `lab/astra-capture/c3-kxhighny/panel_stub.json` · sha256 `2a5da7fe85ca1adc6b7c4dcf9e09ed5c6bb62be6b5c9b42731e36e31d1e8dfea` · `2026-09-22.c3-kxhighny-v0` · **Variants does NOT run admit.py**; keep `admitted_at` null until Collector/Clock |
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

`kalshi_c3_kxhighny_settled_join_lab_20260923/` (do not mutate C3 bordering lab / Cap-SR / FQ siblings / feebook / rails / Arm B / S1/S2/R2-P4).

## Integrity (Clock gate)

Commit attached freeze / scout reget / panel stub bytes **verbatim**. Pin digests to `sha256sum`. **Refuse inventing settled result / depth / fills / PnL.** CHI 429 remains honest gap — do not backfill.

## Merge gates

Units green when implemented; `results`/`pnl` null; Examiner HOLD pre-PR → READY NOT_SCORED only after PR branch sha verify + merge + Clock admit path.

## Refuse binds

invent settled `result`/depth/fills/PnL · Lee-Ready · Cap-SR/QF/L2/EMPTY-OB/SOT-ID/L2-SF/NHL-FQ/CPI-FQ/ATP-FQ/ETH-FQ reopen · C3 bordering reopen as this Feature · ungate S1/S2/R2-P4 · Arm B touch · `admit.py` by Variants · KXFED/another FQ freeze · empty-books invent (C1 PR19)
