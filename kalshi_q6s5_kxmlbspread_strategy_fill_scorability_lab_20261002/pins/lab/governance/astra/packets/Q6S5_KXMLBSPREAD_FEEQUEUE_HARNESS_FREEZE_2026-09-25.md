# Q6S5 KXMLBSPREAD FEE+QUEUE HONESTY HARNESS — FREEZE KERNEL 2026-09-25 (ET)

**Owner:** R&D Variants (harness freeze / implement) → Simulator → Examiner  
**Status:** FROZEN — awaiting Conductor ACCEPT+IMPLEMENT GO (no cloud until ACCEPT)  
**Cite:** Conductor ACCEPT sports Q6 screen `packets/CONDUCTOR_ACCEPT_SPORTS_Q6_SCREEN_2026-09-24.json` (sha256 `2aefbc1712a0389d65f565439d5599a7275688e872e8bc67d5c6dde3b1cd81f8`); Conductor KICK `packets/CONDUCTOR_KICK_VARIANTS_Q6S5_KXMLBSPREAD_FEEQUEUE_FREEZE_2026-09-25.json` (sha256 `9c68ab12f6f5561ee176c5669b17ef40c4f5be20299687823ad7f0e9b67701c8`); Scout freeze `packets/scout_sports_q6_screen/FREEZE_SPORTS_Q6_SCREEN_2026-09-24.md` (sha256 `552314d2822f86bf4127be5de03b8d64aa8c16d6c0c81887bdc0cfbd411571df`); scout raw KXMLBSPREAD summary sha256 `c9e871b3c4edbc648972f9313b3bbcd6784efc46ca847e1f0de4c2847ce85ebe` · full markets sha256 `80b52f47c836248d5869806d7f59617535e6b78258367ebe6045af4275fff7e7` (93 markets / 15 events; vol24≈1.6179M; oi≈1.1246M; fee_cache quadratic×0.5); panel stub `2026-09-25.q6s5-kxmlbspread-v0` (sha256 `c7f1f1f4ca263838c4600ed46db8f525b68efc5399a567bd60929d18d76803cc`; admitted_at null; 6 events / 12 markets — authentic scout-subset)  
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`  
**Packet ID:** Q6S5-KXMLBSPREAD-FEEQUEUE-HARNESS  
**Feature family:** **Q6S5-MLBSPREAD-FEEQUEUE** (MLB spread fee+queue honesty OOS) — ≠ ATP-FQ / NHL-FQ / CPI-FQ / S1 KXMLBGAME ML / Cap-SR / Q6-000 retune  
**Nearest dead card:** **Card 06 open-window CLOSED** / **S1 KXMLBGAME ML retune FORBIDDEN** (name both). Also refuse: invent fills/PnL/depth/settled counts; Q6-000 retune; Cap-SR reopen; live orders; Lee-Ready; `admit.py`; dual-cloud.  
**Hard rules:** Measurement-only. GET-only. No Logan keys. No invent fills/PnL/depth/settled counts. No Lee-Ready. No `admit.py`. Does **not** ungate S1/S2/R2-P4. `results`/`pnl` null until Examiner after Clock admit. Examiner **HOLD_PRE_PR** until merge. Freeze before implement. No dual-cloud.

## Why Q6S5-MLBSPREAD-FEEQUEUE (maximize-next after sports screen ACCEPT)

Screen ACCEPT ranked TRY #1 = KXMLBSPREAD (distinct vs occupied S1 KXMLBGAME ML; strongest fee-channel stress this screen — quadratic×0.5 cache). Pattern: ATP / C2 feequeue freezes. Inventory authentic from scout raw (93/15). Fee pin starts **cache-labeled**; live `/series` pin when rate budget allows — Adversary note: cache ≠ R1-P1 until Examiner tests.

**Explicit NOT:** KXMLBGAME ML retune; invent fills; Q6-000 retune; Cap-SR reopen; live orders.

## Intent (one knob)

Holding **feebook** and **rails** FIXED (commits below), wire a fee+queue honesty harness on `KXMLBSPREAD` panel stub (prefer `panel_admitted.json` when present): compare fee-honest maker/taker + rails freshness/queue labels on MLB spread YES books under fee_type=quadratic multiplier=0.5 **CACHE-LABELED** vs the NFL Q6-000 instrument **pointer only** (shared $5k bakeoff rules; no signal port).

**One knob only:** analysis_slice ∈ {`maker_vs_taker_native`, `content_fresh_vs_stale_bin`} with feebook+rails FIXED.

**Not arms:** inventing fills; KXMLBGAME ML retune; Q6-000 retune; Cap-SR; claiming S1 green; live orders.

## Pins

| Pin | Value |
|---|---|
| Sports screen freeze | `packets/scout_sports_q6_screen/FREEZE_SPORTS_Q6_SCREEN_2026-09-24.md` · sha256 `552314d2822f86bf4127be5de03b8d64aa8c16d6c0c81887bdc0cfbd411571df` |
| Sports screen ACCEPT | `packets/CONDUCTOR_ACCEPT_SPORTS_Q6_SCREEN_2026-09-24.json` · sha256 `2aefbc1712a0389d65f565439d5599a7275688e872e8bc67d5c6dde3b1cd81f8` |
| Conductor KICK | `packets/CONDUCTOR_KICK_VARIANTS_Q6S5_KXMLBSPREAD_FEEQUEUE_FREEZE_2026-09-25.json` · sha256 `9c68ab12f6f5561ee176c5669b17ef40c4f5be20299687823ad7f0e9b67701c8` |
| Scout raw KXMLBSPREAD summary | `packets/scout_sports_q6_screen/raw/markets_open_KXMLBSPREAD_SUMMARY.json` · sha256 `c9e871b3c4edbc648972f9313b3bbcd6784efc46ca847e1f0de4c2847ce85ebe` · 93 markets / 15 events · fee_cache quadratic×0.5 |
| Scout raw KXMLBSPREAD markets | `packets/scout_sports_q6_screen/raw/markets_open_KXMLBSPREAD.json` · sha256 `80b52f47c836248d5869806d7f59617535e6b78258367ebe6045af4275fff7e7` |
| Panel stub | `lab/astra-capture/q6s5-kxmlbspread/panel_stub.json` · `2026-09-25.q6s5-kxmlbspread-v0` · sha256 `c7f1f1f4ca263838c4600ed46db8f525b68efc5399a567bd60929d18d76803cc` · `admitted_at` **null** · 6 events / 12 markets (authentic subset; see capture plan) |
| Fee (FIXED lab pin) | `kalshi_feebook_lab_20260922/` @22371178cb2663250b4762f328069571c48cb551 — series fee **CACHE-LABELED** quadratic×0.5 (not R1-P1 live until Examiner tests `/series` pin) |
| Rails (FIXED) | `kalshi_rails_lab_20260922/` @6a28e0d6254327ea4e6451c781bec56215ac6cac |
| Examiner scorecard template | `lab/governance/astra/templates/EXAMINER_KALSHI_SCORECARD_TEMPLATE_v1.2.json` · sha256 `56bcf6269a42031d9d90496e9a65c2292321aed2165033f6fb44ff8cc4d6b1cc` (RATIFIED; box-only) |
| p16 source | `lab/governance/astra/research/KALSHI_EDGE_RESEARCH_2026-09-24.pdf` p16 · sha256 `7e55bc260526aa5088ee31f74475851219ab2cd7f19fdd2f0dd5e9f998c8b45e` |
| Capture | GET-only public — no trading host; no Logan keys |
| Strategy | **None** — measurement contrast only |

## Arms

| Arm | Name | Slice |
|---|---|---|
| **Q6S5A0** | Native taker | Partition on native `taker_*` fields only; Lee-Ready **REFUSED** |
| **Q6S5A1** | Freshness bin | Rails `content_fresh_flag` / queue-attribution bins; no fee invent; no invent fills |

## Dead-card / live-pin overlap (named)

| Pin / card | Overlap | Handling |
|---|---|---|
| Card 06 open-window | CLOSED | Named nearest dead; do not reopen |
| S1 KXMLBGAME ML | Occupied / retune FORBIDDEN | This packet is spread-only; does **not** retune S1 ML |
| ATP-FQ / NHL-FQ / CPI-FQ | Sibling FQ | New lab dir; share feebook/rails only |
| Q6-000 / Q7 | Pointer only ($5k bakeoff) | No retune |
| Cap-SR / QF / L2-* / EMPTY-OB / SOT-ID | Closed | Do not reopen |
| S2 / R2-P4 | Hard WAIT | Stay queued |
| ATP measure INFRA | Standing down | Until post-ACCEPT settles |

## Scorecard fields (null now)

`maker_vs_taker_roi_delta`, `fresh_vs_stale_gap`, `settled_join_n`, `n_books`, `results`, `pnl` — null until Clock admit + Examiner.

**Examiner scorecard v1.2 fields (Conductor new-lab requirement):** schema from `EXAMINER_KALSHI_SCORECARD_TEMPLATE_v1.2.json` (sha256 `56bcf6269a42031d9d90496e9a65c2292321aed2165033f6fb44ff8cc4d6b1cc`) embedded in Examiner HOLD + EMPTY_RESULTS — scorecard/verdict/common_scorecard (11 metrics)/simulated_fills/stress_sensitivity/executable_dollars_per_day/study_label/preregistration_checklist.gate_status all **null** (`measured=false`). Declared pre-outcome: no default overrides; no rewards thesis; controls market_only/simple_model/no_trade not applicable (no strategy); calibration `emits_probabilities=false`.

## p16 preregistration checklist (Conductor new-lab requirement)

Source: v1.2 template block `preregistration_checklist` (PDF p16 "Minimum preregistration"). Template marks REQUIRED for cards 01-04; Q6S5 is not a card 01-04 study — completed here per Conductor all-new-freeze rule. Declared pre-outcome at 2026-09-25T00:22:00-04:00. Examiner `gate_status` null.

| # | Item | Status | Evidence |
|---|---|---|---|
| 1 | Freeze the market universe (`market_universe`) | **satisfied** | KXMLBSPREAD scout raw 93/15 sha256 `80b52f47…` + panel stub `2026-09-25.q6s5-kxmlbspread-v0` 6/12 sha256 `c7f1f1f4…` |
| 2 | Freeze the exclusions (`exclusions`) | **satisfied** | KXMLBSPREAD ONLY; exclude KXMLBGAME ML/S1 retune; exclude invent fills/PnL/depth; exclude Cap-SR/Q6-000 retune; panel = first-6 events × lowest-floor per side |
| 3 | Freeze the receipt-time information set (`receipt_time_information_set`) | **satisfied** | Scout raw GET bodies as received; panel markets verbatim from raw |
| 4 | Freeze the fee regime (`fee_regime`) | **satisfied** | quadratic×0.5 CACHE-LABELED; feebook @22371178… FIXED; cache ≠ R1-P1 live until Examiner `/series` test |
| 5 | Freeze the order timing (`order_timing`) | **n/a** | no orders; GET-only |
| 6 | Freeze the sizing (`sizing`) | **n/a** | no orders / no sizing |
| 7 | Freeze the fill model (`fill_model`) | **n/a** | no fills; invent fills REFUSED |
| 8 | Freeze the stopping rules (`stopping_rules`) | **satisfied** | freeze-before-implement; HOLD_PRE_PR; no dual-cloud; S5-RJ queue only if needed |
| 9 | Freeze the evaluation metrics (`evaluation_metrics`) | **satisfied** | maker_vs_taker_roi_delta / fresh_vs_stale_gap / settled_join_n / n_books / results / pnl + v1.2 common_scorecard — all null |
| 10 | Limit candidate variants (`limit_candidate_variants`) | **satisfied** | one knob analysis_slice; arms Q6S5A0 / Q6S5A1 |
| 11 | Log every attempted variant (`log_every_attempted_variant`) | **satisfied** | only Q6S5A0/Q6S5A1 declared; further variants need new freeze |
| 12 | Separate discovery, tuning and untouched evaluation periods (`separate_discovery_tuning_evaluation_periods`) | **n/a** | measurement-only; scout cohort is a pin |

Counts: satisfied 8, n/a 4; missing 0.

## Lab dir

`kalshi_q6s5_kxmlbspread_feequue_lab_20260925/` (do not mutate Q / Cap-SR / Cap-SR-FX / C1–C5 / S4 / S5 / ATP-FQ / NHL-FQ / CPI-FQ / L2-* / EMPTY-OB / SOT-ID / feebook / rails / S1 KXMLBGAME labs).

## Integrity (Clock gate)

Commit the **attached** Conductor-box freeze / scout raw / panel stub bytes **verbatim**. Pin digests to `sha256sum`. **Refuse labeled recreations / inventing markets/depth/fills/PnL/settled counts.** Fee remains cache-labeled until live `/series` pin.

## Merge gates

Units green; `results`/`pnl` null; Examiner HOLD_PRE_PR → READY NOT_SCORED only after PR branch sha verify + merge + Clock admit path. **HOLD for Conductor ACCEPT — no CloudAgent / no PR / no admit.py / no live orders.**

## Refuse binds

invent fills/PnL/depth/settled counts · KXMLBGAME ML retune · Q6-000 retune · Cap-SR/QF/L2/EMPTY-OB/SOT-ID reopen · Lee-Ready · `admit.py` by Variants · live orders · dual-cloud · claim cache fee = R1-P1 live without Examiner `/series` test · ungating S1/S2/R2-P4
