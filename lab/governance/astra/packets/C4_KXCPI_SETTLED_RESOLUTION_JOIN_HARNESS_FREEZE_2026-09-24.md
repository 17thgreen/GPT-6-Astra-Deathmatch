# C4 KXCPI SETTLED-RESOLUTION JOIN HARNESS — FREEZE KERNEL 2026-09-24 (ET)

**Owner:** R&D Variants (harness freeze) → Collector/Clock admit path → Examiner  
**Status:** FROZEN — Conductor MAXIMIZE NEXT after C1-RJ PR49 squash-merge main@`34a2720218b4f4f2d6dd0cbde6334ee672a3684b`  
**Cite:** Orthogonal pin `MAXIMIZE_PIN_2026-09-24_1926ET.md`; merge cite `packets/CONDUCTOR_MERGE_C1_KXUFCFIGHT_SETTLED_JOIN_HARNESS_PR49_2026-09-24.json` (ACCEPT digests MATCH `5c3d559a…`; results/pnl/settled_join_n null); Scout cash-cow triage `SCOUT_TRIAGE_CASHCOW_2026-09-22.md` (C4 `KXCPI` HOLD sparse-24h/SoT gaps — ranked after C1/C3/C5/C2, before optional watch ATP/ETH/KXFED); Scout hunt `packets/scout_cashcow_hunt_2026-09-22/scout_hunt_KXCPI.json` (sha256 `6033907bb739bc00c41c796a3c1ed24553e0b7a44116ec3ea4bbaf39066bdcc8`); parent panel stub `2026-09-23.c4-kxcpi-v0`; prior CPI-FQ freeze `C4_KXCPI_FEEQUEUE_HARNESS_FREEZE_2026-09-23.md` (sha256 `949b2558…`, PR33 @`6e55a997…` — nearest dead card)  
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`  
**Packet ID:** C4-KXCPI-SETTLED-RESOLUTION-JOIN-HARNESS  
**Feature family:** **C4-RJ** (KXCPI macro-CPI threshold-ladder settled-resolution join + Clock-admit readiness) — mirror C1-RJ / S5-RJ / R2P3-RJ / S4-RJ / NHL-RJ / R3P3-RJ / C5-RJ / C3-RJ; **NOT FQ sibling**; orthogonal to CPI-FQ (closed; this is NEW Feature)  
**Nearest dead card:** **CPI-FQ** (PR33) — inventing fill density on sparse 24h tape OR inventing `occurrence_datetime` / SoT for strikes that lack it. Also: inventing settled `result`, inventing depth/fills/books.  
**Orthogonality (one line):** CPI-FQ varied `analysis_slice` (maker_vs_taker_native / sparse_24h_vs_fresh_bin) on the *active* pre-release KXCPI ladder with feebook+rails; C4-RJ varies only `join_gate` on the *finalized* KXCPI-26JUL/26AUG cohort and reads/produces no fee, queue, book or fill quantity — no shared knob, cohort, or metric.  
**Hard rules:** Measurement-only join gate. GET-only. No invent settled result. No Lee-Ready. No Cap-SR/FQ reopen. No Arm B touch. No `admit.py` (Variants does NOT run admit). Does **not** ungate S1/S2/R2-P4 (held until C1 PIT@CLE T−7d smoke PASS — no PASS artifact on disk at stamp; holdout T−7d 2026-09-24 20:15 ET). `results`/`pnl` null until Examiner after Clock admit. Examiner **HOLD pre-PR**.

## Why C4-RJ (oldest scorable eligible leftover)

Scorable-first rule (`MAXIMIZE_PIN_2026-09-23_1750ET.md` §1; ETH-FQ PR36 merge note "Maximize next: scorable join / Clock-admit leftover — no new FQ sibling"): prefer Examiner-scorable (Clock admit + settled/authentic join) over FQ / pure pin probes.

Leftover queue = Scout cash-cow triage order (`SCOUT_TRIAGE_CASHCOW_2026-09-22.md`): C1 → C3 → C5 (ADMIT FREEZE NOW) → C2 (ADMIT-NEXT) → **C4 (HOLD)** → optional watch ATP / ETH / KXFED. RJ status: C1-RJ PR49, C3-RJ PR40, C5-RJ PR41, NHL-RJ (C2) PR44 all merged/closed; Q6-stress/R kernels S4-RJ PR45, S5-RJ PR48, R2P3-RJ PR46, R3P3-RJ PR42 merged/closed; S1/S2/R2-P4 held; R3-P4 L2 shape is quote-side only (no settled outcome to join; L2-CAT/L2-SF closed). **C4 `KXCPI`** is therefore the oldest remaining triage item whose join can produce scorable settled rows; it has only CPI-FQ (closed) and no settled join. ATP-RJ / ETH-RJ stay queued behind (optional watch, later rank). KXFED barred.

**2026-09-24 reget (GET-only):** series `KXCPI` **200** (Economics · monthly · BLS source · `quadratic_with_maker_fees`×1); `/markets?status=settled` **429 ×4 honest** (do not invent list books); `/events?status=settled&with_nested_markets=true` 429 then **200** on retry — nested markets on KXCPI-26AUG (15) and KXCPI-26JUL (10); KXCPI-26JUN/MAY/APR listed **without** nested markets (honest; not backfilled); single-event GETs KXCPI-26AUG / KXCPI-26JUL **200** → finalized nonempty `result` **N=25** (yes 13 / no 12), byte-consistent with list embeds. Parent panel seed event KXCPI-26SEP reget **200**: 14/14 active, result empty, `occurrence_datetime` null on 7/14 (not settled; not counted). Candidate **won**. Not FQ sibling.

## Intent (one knob)

Measurement join only — CPI-FQ fee/queue arms already covered and closed; feebook/rails FIXED import-only if needed, else measurement join without fee arms.

**One knob only:** `join_gate` ∈ {`nonempty_result_required`, `occurrence_datetime_match`}

**Not arms:** inventing settled `result`; inventing depth/fills/fill density; inventing `occurrence_datetime`; CPI-FQ `analysis_slice` reuse; Cap-SR/FQ reopen; C1-RJ / C3-RJ / C5-RJ / R3P3-RJ / NHL-RJ / S4-RJ / R2P3-RJ / S5-RJ reopen; Lee-Ready; Arm B; running `admit.py`; ungating S1/S2/R2-P4.

## Pins

| Pin | Value |
|---|---|
| Orthogonal slot | `MAXIMIZE_PIN_2026-09-24_1926ET.md` — active Feature **C4-RJ** |
| Settled reget scout | `lab/governance/astra/packets/scout_c4_settled_rejoin_2026-09-24/scout_settled_rejoin_C4_KXCPI.json` · sha256 `bb72a2ebfa942026913687e4c040a9def598b5080294a346d71f8f7283ab5f7f` · settled nonempty result **N=25** (pin-only) |
| Seed summary | `scout_c4_settled_rejoin_2026-09-24/SEED_SETTLED_SUMMARY.json` · sha256 `8b749373c6949a1aa40b6852e313b0c626da0d0623fcafe167a8196ec228e0bf` |
| Capture bundle | `lab/astra-capture/c4-kxcpi/settled_reget_2026-09-24.json` · sha256 `235c9dad7d244db4c91152c8ae3f6d043f6732d31f99b05bc836abaf2f5d3f56` (≡ scout-dir copy) |
| Panel stub (parent; NOT_ADMITTED) | `lab/governance/astra/packets/C4_KXCPI_PANEL_STUB_2026-09-23.json` ≡ `lab/astra-capture/c4-kxcpi/panel_stub.json` · sha256 `b20b0cbee50c127d2e9bb2548b574b7d643cc708f54019d53bd91775f9762c13` · `2026-09-23.c4-kxcpi-v0` · `admitted_at` **null** · 4 events / 44 markets · 21 missing `occurrence_datetime` — **Variants does NOT run admit.py**; FROZEN_EXPERIMENT.admitted_at stays null |
| Fee (FIXED import-only if needed) | `kalshi_feebook_lab_20260922/` @22371178cb2663250b4762f328069571c48cb551 · series `quadratic_with_maker_fees` / multiplier 1 |
| Rails (FIXED import-only if needed) | `kalshi_rails_lab_20260922/` @6a28e0d6254327ea4e6451c781bec56215ac6cac |
| Capture | GET-only public — no trading host; no Logan keys; no `/communications` RFQ |
| Strategy | **None** — join measurement only |
| Base | main@`34a2720218b4f4f2d6dd0cbde6334ee672a3684b` |

## Arms (join_gate knob only)

| Arm | Name | Gate |
|---|---|---|
| **J0** | Nonempty result required | `join_gate=nonempty_result_required` — Clock-admit readiness when settled markets have non-empty official `result` (status finalized) |
| **J1** | Occurrence datetime match | `join_gate=occurrence_datetime_match` — market `occurrence_datetime` matches event-level SoT across list-embed + single-event GET; **fallback `expected_expiration_time` when `occurrence_datetime` null** (null on 7/14 parent KXCPI-26SEP and 21/44 parent-panel markets; present on 25/25 settled scout markets, where it differs from `expected_expiration_time` — both kept verbatim) — do not invent `occurrence_datetime` |

Both arms share identical panel parent + GET-only reget pins. No fee-arm dual; no invent.

## Scorecard fields (null now)

`settled_join_n`, `occurrence_match_n`, `admit_ready_flag`, `results`, `pnl` — **null** until Clock admit + Examiner. Scout N=25 is a pin — do **not** copy into `settled_join_n`.

## Lab dir

`kalshi_c4_kxcpi_settled_join_lab_20260924/` (do not mutate CPI-FQ lab `kalshi_c4_kxcpi_feequue_lab_20260923/` / C1-RJ / S5-RJ / R2P3-RJ / NHL-RJ / S4-RJ / C3-RJ / C5-RJ / R3P3-RJ / Cap-SR / FQ siblings / feebook / rails / Arm B / S1/S2/R2-P4).

## Integrity (Clock gate)

Commit attached freeze / maximize pin / examiner hold / full scout dir (raw/ + http_log.jsonl) bytes **verbatim** from the implement bundle `C4_RJ_authentic_pins_2026-09-24.tgz` (packets/-relative paths) — in-repo from the first commit (PR49 lesson). Pin digests to `sha256sum`. **Refuse inventing settled result / depth / fills / PnL / books / occurrence_datetime.** Settled list 429s and the three events listed without nested markets remain honest gaps — do not backfill. Scout N=25 is a pin — do **not** copy into `settled_join_n`.

## Merge gates

Units green when implemented; `results`/`pnl` null; Examiner HOLD pre-PR → READY NOT_SCORED only after PR branch sha verify + merge + Clock admit path. **HOLD for Conductor ACCEPT — no CloudAgent / no PR / no admit.py / no live orders.**

## Refuse binds

invent settled `result`/depth/fills/fill-density/PnL · invent `occurrence_datetime` · invent books · Lee-Ready · Cap-SR/QF/L2/EMPTY-OB/SOT-ID/L2-SF/NHL-FQ/CPI-FQ/ATP-FQ/ETH-FQ/S4-FQ/R2-P3-prop-ladder/S5-FILLLEGS/C1-RJ/C3-RJ/C5-RJ/R3P3-RJ/NHL-RJ/S4-RJ/R2P3-RJ/S5-RJ reopen · ungate S1/S2/R2-P4 · Arm B touch · `admit.py` by Variants · KXFED/another FQ freeze · live orders · Conductor pulse cloud on RJ
