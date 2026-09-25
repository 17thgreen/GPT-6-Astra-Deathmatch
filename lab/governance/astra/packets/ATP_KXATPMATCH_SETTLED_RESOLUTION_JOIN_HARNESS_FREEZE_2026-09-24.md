# ATP KXATPMATCH SETTLED-RESOLUTION JOIN HARNESS — FREEZE KERNEL 2026-09-24 (ET)

**Owner:** R&D Variants (harness freeze) → Collector/Clock admit path → Examiner  
**Status:** FROZEN — Conductor MAXIMIZE NEXT after C4-RJ PR50 squash-merge main@`959c3f2beaec5f999b4852c428a3c4cdae1e9603`  
**Cite:** Orthogonal pin `MAXIMIZE_PIN_2026-09-24_1948ET.md`; merge cite `packets/CONDUCTOR_MERGE_C4_KXCPI_SETTLED_JOIN_HARNESS_PR50_2026-09-24.json` (ACCEPT `8a86ae6b…`; 26/26 pins OK at head `ac9ee37d…`; results/pnl/settled_join_n null; "next: Variants next freeze ATP-RJ"); Scout cash-cow triage `SCOUT_TRIAGE_CASHCOW_2026-09-22.md` (optional watch ATP/ETH/KXFED); Scout hunt `packets/scout_cashcow_hunt_2026-09-22/scout_hunt_KXATPMATCH.json` (sha256 `14c99ec8ea00bae507a21d0e6a1879fb94d32ef69ad4b5e3b40a9952821e5da7`); parent panel stub `2026-09-23.atp-kxatpmatch-v0` (reused unchanged); prior ATP-FQ freeze `ATP_KXATPMATCH_FEEQUEUE_HARNESS_FREEZE_2026-09-23.md` (sha256 `4d4ce944…`, **PR34** squash @`438f4abf…` — nearest dead card)  
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`  
**Packet ID:** ATP-KXATPMATCH-SETTLED-RESOLUTION-JOIN-HARNESS  
**Feature family:** **ATP-RJ** (KXATPMATCH ATP tennis match-winner settled-resolution join + Clock-admit readiness) — mirror C4-RJ / C1-RJ / S5-RJ / R2P3-RJ / S4-RJ / NHL-RJ / R3P3-RJ / C5-RJ / C3-RJ; **NOT FQ sibling**; orthogonal to ATP-FQ (closed; this is NEW Feature)  
**Nearest dead card:** **ATP-FQ** (PR34; merge `438f4abf28a3c0156daf6c96ece5efda9557f1dc`; PR35 was a duplicate draft closed unmerged "[superseded by #34]") — inventing depth/fills/fill density OR inventing `occurrence_datetime`/SoT. Also: inventing settled `result`, inventing books.  
**Orthogonality (one line):** ATP-FQ varied `analysis_slice` (ATPA0 maker_vs_taker_native / ATPA1 content_fresh_vs_stale_bin) on the *active* KXATPMATCH ladder with feebook+rails; ATP-RJ varies only `join_gate` on *already-settled* (finalized) KXATPMATCH markets and reads/produces no fee, queue, book, fill or tape metric — no shared knob, cohort state, or metric.  
**Hard rules:** Measurement-only join gate. GET-only. No invent settled result. No Lee-Ready. No Cap-SR/FQ reopen. No Arm B touch. No `admit.py` (Variants does NOT run admit). Does **not** ungate S1/S2/R2-P4 (held until C1 PIT@CLE T−7d smoke PASS — no PASS artifact on disk at stamp; holdout T−7d 2026-09-24 20:15 ET). `results`/`pnl` null until Examiner after Clock admit. Examiner **HOLD pre-PR**.

## Why ATP-RJ (next queued scorable leftover)

Scorable-first rule (`MAXIMIZE_PIN_2026-09-23_1750ET.md` §1; `MAXIMIZE_PIN_2026-09-24_1926ET.md` §1): prefer Examiner-scorable (Clock admit + settled/authentic join) over FQ / pure pin probes.

Leftover queue = Scout cash-cow triage order: C1 → C3 → C5 → C2 → C4 → optional watch **ATP** / ETH / KXFED. RJ status: C1-RJ PR49, C3-RJ PR40, C5-RJ PR41, NHL-RJ (C2) PR44, **C4-RJ PR50** all merged/closed; Q6-stress/R kernels S4-RJ PR45, S5-RJ PR48, R2P3-RJ PR46, R3P3-RJ PR42 merged/closed; S1/S2/R2-P4 held. `MAXIMIZE_PIN_2026-09-24_1926ET.md` §8 queued ATP-RJ then ETH-RJ behind C4-RJ; PR50 merge stamp names ATP-RJ next. **KXATPMATCH** has only ATP-FQ (closed) and no settled join; tennis matches settle within hours, so an authentic finalized cohort exists now. ETH-RJ stays queued behind. KXFED barred.

**2026-09-24 reget (GET-only, host `https://api.elections.kalshi.com/trade-api/v2`, UTC window 2026-09-24T23:45:02.182623Z → 2026-09-24T23:46:50.094385Z):** series `KXATPMATCH` **200** (Sports · custom · ATP source · `quadratic_with_maker_fees`×1); `/markets?status=settled&limit=30` **429 ×4 honest** (initial + 3 retries @10/20/40s; do not invent list books); `/events?status=settled&limit=15&with_nested_markets=true` **200** first attempt — 15 events × 2 markets, all `finalized`, nonempty `result` **N=30** (yes 15 / no 15; ATP Chengdu 7 events, ATP Hangzhou 8 events; match dates 2026-09-22..24); cursor present, page 2 **not** fetched. Parent panel 6 single-event GETs **200**: 12/12 `finalized`, nonempty result 12/12; 4 events (8 markets) overlap list page 1 with field-for-field match; KXATPMATCH-26SEP22HARGAL, KXATPMATCH-26SEP22MOCKOT outside page 1 (recorded, not added to N). HTTP totals: 200×8, 429×4; 0 × 404. Candidate **won**. Not FQ sibling.

## Intent (one knob)

Measurement join only — ATP-FQ fee/queue arms already covered and closed; feebook/rails FIXED import-only if needed, else measurement join without fee arms.

**One knob only:** `join_gate` ∈ {`nonempty_result_required`, `occurrence_datetime_match`}

**Not arms:** inventing settled `result`; inventing depth/fills/fill density; inventing `occurrence_datetime`; ATP-FQ `analysis_slice` reuse; Cap-SR/FQ reopen; C1-RJ / C3-RJ / C4-RJ / C5-RJ / R3P3-RJ / NHL-RJ / S4-RJ / R2P3-RJ / S5-RJ reopen; Lee-Ready; Arm B; running `admit.py`; ungating S1/S2/R2-P4.

## Pins

| Pin | Value |
|---|---|
| Orthogonal slot | `MAXIMIZE_PIN_2026-09-24_1948ET.md` — active Feature **ATP-RJ** |
| Settled reget scout | `lab/governance/astra/packets/scout_atp_settled_rejoin_2026-09-24/scout_settled_rejoin_ATP_KXATPMATCH.json` · sha256 `2982a245ebd4ff8430ef4b2fe13692c15211c2077e2460d6c0246480f59736df` · settled nonempty result **N=30** (pin-only) |
| Seed summary | `scout_atp_settled_rejoin_2026-09-24/SEED_SETTLED_SUMMARY.json` · sha256 `913fc5d646c51192e40869a68a64b4fe2b66f8231dd75b90f5467bd50559700e` |
| Capture bundle | `lab/astra-capture/atp-kxatpmatch/settled_reget_2026-09-24.json` · sha256 `068ff00fe420d3365cc798549ef2e89aac96fa7e841846f73e67d5103c49760a` (≡ scout-dir copy) |
| Panel stub (parent; NOT_ADMITTED; reused unchanged) | `lab/governance/astra/packets/ATP_KXATPMATCH_PANEL_STUB_2026-09-23.json` ≡ `lab/astra-capture/atp-kxatpmatch/panel_stub.json` · sha256 `ed041c502d1f775d33c44bf900ac91b1339d99045bddd2052edd09a139ae2d3f` · `2026-09-23.atp-kxatpmatch-v0` · `admitted_at` **null** · 6 events / 12 markets · 0 missing `occurrence_datetime` — **Variants does NOT run admit.py**; FROZEN_EXPERIMENT.admitted_at stays null |
| Fee (FIXED import-only if needed) | `kalshi_feebook_lab_20260922/` @22371178cb2663250b4762f328069571c48cb551 · series `quadratic_with_maker_fees` / multiplier 1 |
| Rails (FIXED import-only if needed) | `kalshi_rails_lab_20260922/` @6a28e0d6254327ea4e6451c781bec56215ac6cac |
| Examiner scorecard template | `lab/governance/astra/templates/EXAMINER_KALSHI_SCORECARD_TEMPLATE_v1.2.json` · sha256 `56bcf6269a42031d9d90496e9a65c2292321aed2165033f6fb44ff8cc4d6b1cc` (RATIFIED 2026-09-24 ~19:37 ET; box-only, not on main) |
| p16 source | `lab/governance/astra/research/KALSHI_EDGE_RESEARCH_2026-09-24.pdf` p16 "Minimum preregistration" · sha256 `7e55bc260526aa5088ee31f74475851219ab2cd7f19fdd2f0dd5e9f998c8b45e` |
| Capture | GET-only public — no trading host; no Logan keys; no `/communications` RFQ |
| Strategy | **None** — join measurement only |
| Base | main@`959c3f2beaec5f999b4852c428a3c4cdae1e9603` |

## Arms (join_gate knob only)

| Arm | Name | Gate |
|---|---|---|
| **J0** | Nonempty result required | `join_gate=nonempty_result_required` — Clock-admit readiness when settled markets have non-empty official `result` (status finalized) |
| **J1** | Occurrence datetime match | `join_gate=occurrence_datetime_match` — market `occurrence_datetime` matches event-level SoT across list-embed + single-event GET; **fallback `expected_expiration_time` when `occurrence_datetime` is null**, each fallback row labeled per row `join_source='expected_expiration_time_fallback'` (non-fallback rows `join_source='occurrence_datetime'`); **never write `expected_expiration_time` into `occurrence_datetime`**. Scout: `occurrence_datetime` present 30/30 settled + 12/12 parent; equals `expected_expiration_time` 30/30 (scheduled start) → fallback path not exercised by this cohort (0 expected fallback rows); `settlement_ts` < `occurrence_datetime` on 8/30 — both kept verbatim, not reconciled |

Both arms share identical panel parent + GET-only reget pins. No fee-arm dual; no invent.

## Scorecard fields (null now)

Packet metrics `settled_join_n`, `occurrence_match_n`, `fallback_join_n`, `admit_ready_flag`, `results`, `pnl` — **null** until Clock admit + Examiner. Scout N=30 is a pin — do **not** copy into `settled_join_n`.

**Examiner scorecard v1.2 fields (Conductor new-lab requirement):** schema from `EXAMINER_KALSHI_SCORECARD_TEMPLATE_v1.2.json` (sha256 `56bcf626…`) embedded in `EXAMINER_HOLD_ATP_KXATPMATCH_SETTLED_JOIN_HARNESS_PRE_PR_2026-09-24.json` (`examiner_scorecard_v1_2`) and `EMPTY_RESULTS.json` — scorecard/verdict/common_scorecard (11 metrics)/simulated_fills/stress_sensitivity/executable_dollars_per_day/study_label/preregistration_checklist.gate_status all **null** (`measured=false`). Declared pre-outcome: no default overrides; no rewards thesis; controls market_only/simple_model/no_trade not applicable (no strategy); calibration `emits_probabilities=false` (Examiner may record "N/A" at scoring; left null now).

## p16 preregistration checklist (Conductor new-lab requirement)

Source: v1.2 template block `preregistration_checklist` (items extracted from PDF p16 "Minimum preregistration": *"Freeze the market universe, exclusions, receipt-time information set, fee regime, order timing, sizing, fill model, stopping rules and evaluation metrics before the test. Limit candidate variants; log every attempted variant. Separate discovery, tuning and untouched evaluation periods. Sampling more prints from the same event does not solve small-sample uncertainty."*). Template marks it REQUIRED for cards 01-04; ATP-RJ is not a card 01-04 study — completed here per Conductor all-new-freeze rule. Declared pre-outcome at 2026-09-24T19:48:42-04:00. Examiner `gate_status` null.

| # | Item | Status | Evidence |
|---|---|---|---|
| 1 | Freeze the market universe (`market_universe`) | **satisfied** | KXATPMATCH (series GET 200) already-settled markets: 30 finalized nonempty-result markets from /events?status=settled page 1 (15 events, tickers frozen in scout_settled_rejoin_ATP_KXATPMATCH.json) + parent panel 2026-09-23.atp-kxatpmatch-v0 (6 events/12 markets, sha256 ed041c50…) reused unchanged |
| 2 | Freeze the exclusions (`exclusions`) | **satisfied** | exclude empty result; exclude status not in {finalized, settled}; exclude events beyond list page 1 (cursor not followed); exclude outside-list parent rows from N; /markets settled list 429 not backfilled; no fair-price/void rows observed (all results yes/no) — any future such row excluded from J0/J1 and logged |
| 3 | Freeze the receipt-time information set (`receipt_time_information_set`) | **satisfied** | raw GET bodies exactly as received at the UTC timestamps in http_log.jsonl (raw/ saved per attempt); no post-receipt enrichment. Data is post-outcome by construction (historical replay of settled markets) |
| 4 | Freeze the fee regime (`fee_regime`) | **n/a** | no fee quantity read or produced; series fee_type quadratic_with_maker_fees x1 recorded as metadata only; feebook @22371178 import-only if ever needed |
| 5 | Freeze the order timing (`order_timing`) | **n/a** | no orders; GET-only measurement join |
| 6 | Freeze the sizing (`sizing`) | **n/a** | no orders / no sizing |
| 7 | Freeze the fill model (`fill_model`) | **n/a** | no fills; fill/fill-density/queue metrics refused |
| 8 | Freeze the stopping rules (`stopping_rules`) | **satisfied** | single GET pass; ≤3 retries per request with 10/20/40s backoff, every attempt logged; list page 1 only; no backfill of gaps; N fixed as pin at freeze stamp |
| 9 | Freeze the evaluation metrics (`evaluation_metrics`) | **satisfied** | settled_join_n, occurrence_match_n, fallback_join_n (rows with join_source='expected_expiration_time_fallback'), admit_ready_flag — all null until Clock admit + Examiner |
| 10 | Limit candidate variants (`limit_candidate_variants`) | **satisfied** | one knob join_gate; two arms J0 nonempty_result_required / J1 occurrence_datetime_match (+ fallback) |
| 11 | Log every attempted variant (`log_every_attempted_variant`) | **satisfied** | J0 and J1 are the only variants and are both declared here; any further variant requires a new freeze/addendum logged before outcome; all HTTP attempts logged |
| 12 | Separate discovery, tuning and untouched evaluation periods (`separate_discovery_tuning_evaluation_periods`) | **n/a** | no tunable parameter and no outcome-dependent selection in a measurement join; scout cohort is a pin, not a tuning set. Examiner note: if ever scored beyond harness readiness, use KXATPMATCH markets settled AFTER this freeze stamp as the untouched evaluation set |

Counts: satisfied 7, n/a 5; missing 0.

## Lab dir

`kalshi_atp_kxatpmatch_settled_join_lab_20260924/` (do not mutate ATP-FQ lab `kalshi_atp_kxatpmatch_feequue_lab_20260923/` / C4-RJ / C1-RJ / S5-RJ / R2P3-RJ / NHL-RJ / S4-RJ / C3-RJ / C5-RJ / R3P3-RJ / Cap-SR / FQ siblings / feebook / rails / Arm B / S1/S2/R2-P4).

## Integrity (Clock gate)

Commit attached freeze / maximize pin / examiner hold / full scout dir (raw/ + http_log.jsonl) / lab dir bytes **verbatim** from the implement bundle `ATP_RJ_authentic_pins_2026-09-24.tgz` (repo-relative `lab/governance/astra/packets/…` + `lab/astra-science/…` paths) — in-repo from the first commit (PR49/PR50 lesson). Pin digests to `sha256sum`. **Refuse inventing settled result / depth / fills / PnL / books / occurrence_datetime.** Settled `/markets` list 429s, un-fetched events-list page 2, and outside-page-1 parent rows remain honest gaps — do not backfill. Scout N=30 is a pin — do **not** copy into `settled_join_n`.

## Merge gates

Units green when implemented; `results`/`pnl` null; Examiner HOLD pre-PR → READY NOT_SCORED only after PR branch sha verify + merge + Clock admit path. **HOLD for Conductor ACCEPT — no CloudAgent / no PR / no admit.py / no live orders.**

## Refuse binds

invent settled `result`/depth/fills/fill-density/PnL · invent `occurrence_datetime` · write `expected_expiration_time` into `occurrence_datetime` · invent books · Lee-Ready · Cap-SR/QF/L2/EMPTY-OB/SOT-ID/L2-SF/NHL-FQ/CPI-FQ/ATP-FQ/ETH-FQ/S4-FQ/R2-P3-prop-ladder/S5-FILLLEGS/C1-RJ/C3-RJ/C4-RJ/C5-RJ/R3P3-RJ/NHL-RJ/S4-RJ/R2P3-RJ/S5-RJ reopen · ungate S1/S2/R2-P4 · Arm B touch · `admit.py` by Variants · KXFED/another FQ freeze · live orders · Conductor pulse cloud on RJ
