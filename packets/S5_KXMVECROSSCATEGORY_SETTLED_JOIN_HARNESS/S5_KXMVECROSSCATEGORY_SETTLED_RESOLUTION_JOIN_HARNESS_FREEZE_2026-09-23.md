# S5 KXMVECROSSCATEGORY SETTLED-RESOLUTION JOIN HARNESS — FREEZE KERNEL 2026-09-23 (ET)

**Owner:** R&D Variants (harness freeze) → Collector/Clock admit path → Examiner  
**Status:** FROZEN — Conductor MAXIMIZE NEXT after R2P3-RJ PR46 squash-merge main@`b2c1639a77f62114572fd41182f8a3c5ef70cad1`  
**Cite:** Orthogonal pin `MAXIMIZE_PIN_2026-09-23_1733ET.md`; parent panel stub `2026-09-22.s5-kxmvecrosscategory-v0`; settled reget scout `scout_s5_settled_rejoin_2026-09-23/`; prior S5 MEAS freeze `S5_KXMVECROSSCATEGORY_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md`; merge cite `packets/CONDUCTOR_MERGE_R2P3_KXNFLPASSYDS_SETTLED_JOIN_HARNESS_PR46_2026-09-23.json`  
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`  
**Packet ID:** S5-KXMVECROSSCATEGORY-SETTLED-RESOLUTION-JOIN-HARNESS  
**Feature family:** **S5-RJ** (KXMVECROSSCATEGORY MVE settled-resolution join + Clock-admit readiness) — mirror R2P3-RJ / S4-RJ / NHL-RJ / C5-RJ / R3P3-RJ / C3-RJ; **orthogonal to S5 FILLLEGS / MVE-FL** (fill-vs-legs Feature sibling; this is NEW Feature, not FILLLEGS/FQ reopen)  
**Nearest dead card:** Inventing settled `result` / inventing depth/fills OR empty-books invent (C1 PR19 refuse) OR S5 FILLLEGS / MVE-FL sibling reopen.  
**Hard rules:** Measurement-only join gate. GET-only. No invent settled result. No Lee-Ready. No Cap-SR/FQ reopen. No Arm B touch. No `admit.py` (Variants does NOT run admit). Does **not** ungate S1/S2/R2-P4. `results`/`pnl` null until Examiner after Clock admit. Examiner **HOLD pre-PR**.

## Why S5-RJ (this slot)

Per Conductor pin rules after R2P3-RJ PR46 @`b2c1639a…` (ACCEPT digests MATCH `e5218cf2…`; results/pnl/settled_join_n null; next_maximize S5-RJ then C1-RJ): prefer Examiner-scorable (Clock admit + settled/authentic join). Do **not** freeze KXFED / another FQ sibling. Refiner owns Arm B — do not touch. Prefer not to reopen Cap-SR / C3-RJ / C5-RJ / R3P3-RJ / NHL-RJ / S4-RJ / R2P3-RJ (closed).

Primary candidate **S5-RJ** (order #1): capture `astra-capture/s5-kxmvecrosscategory/`; prior MEAS + FILLLEGS harness + panel stub for parent seeds. **2026-09-23 reget:** GET-only `/markets?series_ticker=KXMVECROSSCATEGORY&status=settled&limit=20` → finalized nonempty `result` **N=20** (cursor present); earlier settled/finalized/events list attempts **429 honest**; SHARD1 series **429 honest**; related fee-pin `KXMVESPORTSMULTIGAMEEXTENDED` settled lim20 also **200 N=20**. Parent panel seeds (N=5) ticker GETs all **finalized/nonempty** (honest). `occurrence_datetime` null on settled cohort (honest API gap) — J1 uses `expected_expiration_time` when present. Candidate **won**. Not C1-RJ fallback.

## Intent (one knob)

Measurement join only — FILLLEGS fill-vs-legs arms already covered on S5 FILLLEGS / MVE-FL stub; feebook/rails FIXED import-only if needed, else measurement join without fee arms.

**One knob only:** `join_gate` ∈ {`nonempty_result_required`, `occurrence_datetime_match`}

**Not arms:** inventing settled `result`; inventing depth/fills; Cap-SR/FQ reopen; C3-RJ / C5-RJ / R3P3-RJ / NHL-RJ / S4-RJ / R2P3-RJ reopen; Lee-Ready; empty-books invent; Arm B; running `admit.py`; S5 FILLLEGS / MVE-FL reopen.

## Pins

| Pin | Value |
|---|---|
| Orthogonal slot | `MAXIMIZE_PIN_2026-09-23_1733ET.md` — active Feature **S5-RJ** |
| Settled reget scout | `lab/governance/astra/packets/scout_s5_settled_rejoin_2026-09-23/` · settled nonempty result **N=20** · (digests in DIGESTS.txt) |
| Capture bundle | `lab/astra-capture/s5-kxmvecrosscategory/settled_reget_2026-09-23.json` |
| Panel stub (parent; admitted_at null) | `lab/governance/astra/packets/S5_KXMVECROSSCATEGORY_PANEL_STUB_2026-09-22.json` ≡ `lab/astra-capture/s5-kxmvecrosscategory/panel_stub.json` · sha256 `4918b820d454c5f997ea100917859f7e9467d92933bed1bc8a55c81ab8ce5b8e` · `2026-09-22.s5-kxmvecrosscategory-v0` · **Variants does NOT run admit.py**; keep `admitted_at` null until Collector/Clock |
| Fee (FIXED import-only if needed) | `kalshi_feebook_lab_20260922/` @22371178cb2663250b4762f328069571c48cb551 · series override `quadratic_with_combo_maker_fees` / multiplier 1 |
| Rails (FIXED import-only if needed) | `kalshi_rails_lab_20260922/` @6a28e0d6254327ea4e6451c781bec56215ac6cac |
| Capture | GET-only public — no trading host; no Logan keys; no `/communications` RFQ |
| Strategy | **None** — join measurement only |

## Arms (join_gate knob only)

| Arm | Name | Gate |
|---|---|---|
| **J0** | Nonempty result required | `join_gate=nonempty_result_required` — Clock-admit readiness when settled markets have non-empty official `result` |
| **J1** | Occurrence datetime match | `join_gate=occurrence_datetime_match` — SoT `occurrence_datetime` matches live_get / seed when present; if API null (honest on this MVE cohort), match on `expected_expiration_time` — do not invent `occurrence_datetime` |

Both arms share identical panel parent + GET-only reget pins. No fee-arm dual; no invent.

## Scorecard fields (null now)

`settled_join_n`, `occurrence_match_n`, `admit_ready_flag`, `results`, `pnl` — **null** until Clock admit + Examiner.

## Lab dir

`kalshi_s5_kxmvecrosscategory_settled_join_lab_20260923/` (do not mutate S5 FILLLEGS / MVE-FL / R2P3-RJ / S4-RJ / NHL-RJ / C3-RJ / C5-RJ / R3P3-RJ / Cap-SR / FQ siblings / feebook / rails / Arm B / S1/S2/R2-P4).

## Integrity (Clock gate)

Commit attached freeze / scout reget / panel stub bytes **verbatim**. Pin digests to `sha256sum`. **Refuse inventing settled result / depth / fills / PnL.** Earlier settled/finalized/events list 429s remain honest gaps — do not backfill. `occurrence_datetime` null on settled lim20 — do not invent. Scout N=20 is a pin — do **not** copy into `settled_join_n`.

## Merge gates

Units green when implemented; `results`/`pnl` null; Examiner HOLD pre-PR → READY NOT_SCORED only after PR branch sha verify + merge + Clock admit path.

## Refuse binds

invent settled `result`/depth/fills/PnL · Lee-Ready · Cap-SR/QF/L2/EMPTY-OB/SOT-ID/L2-SF/NHL-FQ/CPI-FQ/ATP-FQ/ETH-FQ/S4-FQ/R2-P3-prop-ladder/S5-FILLLEGS/MVE-FL/C3-RJ/C5-RJ/R3P3-RJ/NHL-RJ/S4-RJ/R2P3-RJ reopen · ungate S1/S2/R2-P4 · Arm B touch · `admit.py` by Variants · KXFED/another FQ freeze · empty-books invent (C1 PR19) · live orders
