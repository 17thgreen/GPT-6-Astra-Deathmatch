# Q6S1 KXATPMATCH INVENTORY RE-PROOF — FREEZE KERNEL 2026-09-25 (ET)

**Owner:** R&D Variants (harness freeze / implement) → Simulator → Examiner  
**Status:** FROZEN — awaiting Conductor ACCEPT+IMPLEMENT GO (no cloud until ACCEPT)  
**Cite:** Conductor KICK `packets/CONDUCTOR_KICK_VARIANTS_Q6S1_KXATPMATCH_INVENTORY_REPROOF_FREEZE_2026-09-25.json` (sha256 `63eab2f727c9636196e08092339d5efc10439396bc9a7d3f696b7344ac746cb6`); MAXIMIZE pin `packets/MAXIMIZE_PIN_2026-09-25_0031ET.md` (sha256 `7629b19f9a9e2d2aabf83bf46918963d118f6333ffc35f4af5bd227f72b9c09e`); fresh MAXIMIZE pin `packets/MAXIMIZE_PIN_2026-09-25_0033ET.md` (sha256 `d36b57761fa1ca3d84af1b8c58e03618e94e283857fbade5ff3f82666f0d463d` — Q7-B Pass-2 KEEP accepted; B2 shadow only; 000 incumbent; do not touch Pass-3/Refiner/B2 promote); Sports screen ACCEPT `packets/CONDUCTOR_ACCEPT_SPORTS_Q6_SCREEN_2026-09-24.json` (sha256 `2aefbc1712a0389d65f565439d5599a7275688e872e8bc67d5c6dde3b1cd81f8`; rank-among-TRY=2); Sports screen freeze `packets/scout_sports_q6_screen/FREEZE_SPORTS_Q6_SCREEN_2026-09-24.md` (sha256 `552314d2822f86bf4127be5de03b8d64aa8c16d6c0c81887bdc0cfbd411571df`); after Q6S5 PR58 squash-merge main@`f349ffa819960b8f641725fbf259f5430dffcff7`  
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`  
**Packet ID:** Q6S1-KXATPMATCH-INVENTORY-REPROOF  
**Feature family:** **Q6S1-ATP-INVENTORY** (KXATPMATCH inventory re-proof / unresolved-inventory bakeoff slice on existing ATP FQ+RJ stack vs Q6-000 under shared $5k bakeoff) — ≠ F1 / F2 / F3 (Strategy League structural/attachment/microstructure families) · ≠ ATP-FQ · ≠ ATP-RJ · ≠ Cap-SR · ≠ Cap-SR-FX · ≠ Q6S5-MLBSPREAD-FEEQUEUE · ≠ PR57 measure-transport INFRA · ≠ ETH-FQ · ≠ NHL-FQ · ≠ CPI-FQ  
**Nearest dead card:** **Cap-SR / ATP-FQ reopen (FORBIDDEN)** / **Card 06 CLOSED** / **S1 KXMLBGAME ML retune FORBIDDEN**. Also refuse: invent fills/PnL/depth/settlement_ts/inventory deltas; Q6S5 reopen; Q6-000 retune; live orders; Lee-Ready; `admit.py`; dual-cloud; PR57 INFRA duplicate.  
**Hard rules:** Measurement-only inventory re-proof. GET-only. No Logan keys. No invent fills/PnL/depth/settled counts/inventory deltas. No Lee-Ready. No `admit.py`. Does **not** ungate S1/S2/R2-P4. `results`/`pnl`/inventory deltas null until Examiner after Clock admit. Examiner **HOLD_PRE_PR** until merge. Freeze before implement. No dual-cloud. No cloud until ACCEPT.

## Why Q6S1-ATP-INVENTORY (maximize-next after Q6S5 PR58 + sports screen rank-2 TRY)

Screen ACCEPT ranked TRY #2 = KXATPMATCH inventory re-proof for **existing** ATP fee/queue + settled-join lane vs Q6-000 KEEP under shared $5k bakeoff — **not** a new cash-cow C* re-nominate; **not** PR57 measure-hardening INFRA duplicate; **not** Cap-SR / ATP-FQ / ETH-FQ / Q6S5 reopen.

Parent ATP stack already on disk:
- ATP-FQ freeze sha256 `4d4ce944946e72dd40567d14388fe11c6145fbbb32505a880bcf80a4c8b4dffe` (PR34; analysis_slice ATPA0/ATPA1) — **closed; do not reopen as FQ**
- ATP-RJ freeze sha256 `dc9fcb326a97ce24267ed96438bf403687bc9aef6b79dccef3483d0e4cdeeb69` (join_gate J0/J1) — **closed; do not reopen as RJ**
- Panel stub `2026-09-23.atp-kxatpmatch-v0` sha256 `ed041c502d1f775d33c44bf900ac91b1339d99045bddd2052edd09a139ae2d3f` · 6 events / 12 markets · `admitted_at` **null** — **reuse verbatim; do not invent markets**

**Explicit NOT:** Cap-SR reopen; ATP-FQ fee-formula change; ATP-RJ join_gate retune; PR57 INFRA duplicate; Q6S5 reopen; invent fills; Q6-000 retune; S1 ML retune; live orders; Pass-3 / Refiner / B2 promote.

## Intent (one knob)

Holding **feebook** + **rails** FIXED and holding ATP-FQ / ATP-RJ measurement objects as **import-only closed parents**, wire an **inventory-centric** measurement harness that re-proofs the existing ATP FQ+RJ stack vs the NFL Q6-000 instrument **pointer only** under shared $5k bakeoff rules — by partitioning (or not) on unresolved-inventory / position-bucket exposure.

**One knob only:** `inventory_slice` ∈ {`flat_control`, `inventory_bin_exposure`} with feebook+rails FIXED; ATP-FQ analysis_slice and ATP-RJ join_gate **not** reopened.

**Not arms:** inventing fills; fee formula change; Cap-SR soft-reserve reopen; PR57 measure-transport INFRA; Q6S5 reopen; Q6-000 retune; S1 ML retune; live orders.

## Pins

| Pin | Value |
|---|---|
| Conductor KICK | `packets/CONDUCTOR_KICK_VARIANTS_Q6S1_KXATPMATCH_INVENTORY_REPROOF_FREEZE_2026-09-25.json` · sha256 `63eab2f727c9636196e08092339d5efc10439396bc9a7d3f696b7344ac746cb6` |
| Maximize pin (kick-cited) | `packets/MAXIMIZE_PIN_2026-09-25_0031ET.md` · sha256 `7629b19f9a9e2d2aabf83bf46918963d118f6333ffc35f4af5bd227f72b9c09e` |
| Maximize pin (fresh; cite both) | `packets/MAXIMIZE_PIN_2026-09-25_0033ET.md` · sha256 `d36b57761fa1ca3d84af1b8c58e03618e94e283857fbade5ff3f82666f0d463d` · Q7-B Pass-2 KEEP; B2 shadow; 000 incumbent |
| Sports screen freeze | `packets/scout_sports_q6_screen/FREEZE_SPORTS_Q6_SCREEN_2026-09-24.md` · sha256 `552314d2822f86bf4127be5de03b8d64aa8c16d6c0c81887bdc0cfbd411571df` |
| Sports screen ACCEPT | `packets/CONDUCTOR_ACCEPT_SPORTS_Q6_SCREEN_2026-09-24.json` · sha256 `2aefbc1712a0389d65f565439d5599a7275688e872e8bc67d5c6dde3b1cd81f8` · Q6S1 rank-among-TRY=2 |
| Scout hunt (parent seed) | `packets/scout_cashcow_hunt_2026-09-22/scout_hunt_KXATPMATCH.json` · sha256 `14c99ec8ea00bae507a21d0e6a1879fb94d32ef69ad4b5e3b40a9952821e5da7` · 48 markets / 24 events |
| Sports-screen raw markets | `packets/scout_sports_q6_screen/raw/markets_open_KXATPMATCH.json` · sha256 `b603474b3ca336b0a3678ff0deb8a937dfdcc4205e8e24db4d657d40d2323c60` · screen inventory 28/14 (pin only; panel not reinvented) |
| Sports-screen raw summary | `packets/scout_sports_q6_screen/raw/markets_open_KXATPMATCH_SUMMARY.json` · sha256 `d5aee9c9254a0c9178b3ecc4fbd84f6db7bc29f6bc11af4df8690e4242ebe647` · fee_cache quadratic_with_maker_fees×1 |
| Panel stub (reused; NOT_ADMITTED) | `lab/astra-capture/atp-kxatpmatch/panel_stub.json` ≡ `packets/ATP_KXATPMATCH_PANEL_STUB_2026-09-23.json` · `2026-09-23.atp-kxatpmatch-v0` · sha256 `ed041c502d1f775d33c44bf900ac91b1339d99045bddd2052edd09a139ae2d3f` · `admitted_at` **null** · 6 events / 12 markets — **Variants does NOT run admit.py** |
| ATP-FQ parent (CLOSED; import-only) | `packets/ATP_KXATPMATCH_FEEQUEUE_HARNESS_FREEZE_2026-09-23.md` · sha256 `4d4ce944946e72dd40567d14388fe11c6145fbbb32505a880bcf80a4c8b4dffe` |
| ATP-RJ parent (CLOSED; import-only) | `packets/ATP_KXATPMATCH_SETTLED_RESOLUTION_JOIN_HARNESS_FREEZE_2026-09-24.md` · sha256 `dc9fcb326a97ce24267ed96438bf403687bc9aef6b79dccef3483d0e4cdeeb69` |
| Settled reget (parent pin) | `lab/astra-capture/atp-kxatpmatch/settled_reget_2026-09-24.json` · sha256 `068ff00fe420d3365cc798549ef2e89aac96fa7e841846f73e67d5103c49760a` |
| Fee (FIXED lab pin; CACHE-LABELED) | `kalshi_feebook_lab_20260922/` @22371178cb2663250b4762f328069571c48cb551 — series fee **CACHE-LABELED** `quadratic_with_maker_fees`×1 (ATP FQ / sports-screen pin; **not** R1-P1 live until Examiner `/series` test; **not** quadratic×0.5) |
| Rails (FIXED) | `kalshi_rails_lab_20260922/` @6a28e0d6254327ea4e6451c781bec56215ac6cac |
| Examiner scorecard template | `lab/governance/astra/templates/EXAMINER_KALSHI_SCORECARD_TEMPLATE_v1.2.json` · sha256 `56bcf6269a42031d9d90496e9a65c2292321aed2165033f6fb44ff8cc4d6b1cc` (RATIFIED; box-only) |
| p16 source | `lab/governance/astra/research/KALSHI_EDGE_RESEARCH_2026-09-24.pdf` p16 · sha256 `7e55bc260526aa5088ee31f74475851219ab2cd7f19fdd2f0dd5e9f998c8b45e` |
| Transport | in-memory GET stub; `live_gets=0`; refuse `/orders` `/portfolio`; prefer `/events` when `/markets` hot |
| Capture | GET-only public — no trading host; no Logan keys |
| Strategy | **None** — inventory measurement contrast only |
| Base | main@f349ffa819960b8f641725fbf259f5430dffcff7 (Q6S5 PR58 merge) |

## Arms

| Arm | Name | Slice |
|---|---|---|
| **Q6S1A0** | Flat control | `inventory_slice=flat_control` — ATP FQ+RJ stack measured under shared $5k bakeoff vs Q6-000 pointer with **no** inventory partition (flat / null position bucket) |
| **Q6S1A1** | Inventory-bin exposure | `inventory_slice=inventory_bin_exposure` — same stack partitioned by unresolved-inventory / `position_bucket` exposure bins; inventory deltas remain **null** until Clock+Examiner |

Both arms share identical panel stub + GET-only transport + CACHE-LABELED fee. No fee-arm dual; no invent fills/PnL.

## Dead-card / live-pin overlap (named)

| Pin / card | Overlap | Handling |
|---|---|---|
| Cap-SR / Cap-SR-FX / Soft-blended reserves | CLOSED | Named nearest dead; do not reopen |
| ATP-FQ | CLOSED (PR34) | Import-only parent; do not reopen analysis_slice |
| ATP-RJ | CLOSED | Import-only parent; do not reopen join_gate |
| Card 06 open-window | CLOSED (CEM-006) | Named nearest dead; do not reopen |
| S1 KXMLBGAME ML | Occupied / retune FORBIDDEN | Do not retune |
| Q6S5-MLBSPREAD-FEEQUEUE | PR58 merged READY NOT_SCORED | Do not reopen |
| ETH-FQ / NHL-FQ / CPI-FQ | Sibling FQ | Do not reopen |
| PR57 ATP measure INFRA | Merged | Do not duplicate |
| Q6-000 / Q7-B Pass-2 | Pointer only ($5k bakeoff); Pass-2 KEEP / B2 shadow | No retune; no Pass-3; no B2 promote |
| F1 / F2 / F3 | Strategy League families | Orthogonal — this packet is inventory-slice, not blend/microstructure |

## Scorecard fields (null now)

`inventory_delta_flat_vs_binned`, `unresolved_inventory`, `position_bucket_gap`, `settled_join_n`, `n_books`, `results`, `pnl` — **null** until Clock admit + Examiner. Sports-screen inventory 28/14 and scout hunt 48/24 are pins — do **not** copy into scorecard counts.

**Examiner scorecard v1.2 fields (Conductor new-lab requirement):** schema from `EXAMINER_KALSHI_SCORECARD_TEMPLATE_v1.2.json` (sha256 `56bcf6269a42031d9d90496e9a65c2292321aed2165033f6fb44ff8cc4d6b1cc`) embedded in Examiner HOLD + EMPTY_RESULTS — scorecard/verdict/common_scorecard (11 metrics)/simulated_fills/stress_sensitivity/executable_dollars_per_day/study_label/preregistration_checklist.gate_status all **null** (`measured=false`). Declared pre-outcome: no default overrides; no rewards thesis; controls market_only/simple_model/no_trade not applicable (no strategy); calibration `emits_probabilities=false`. Examiner **HOLD_PRE_PR**.

## p16 preregistration checklist (Conductor new-lab requirement)

Source: v1.2 template block `preregistration_checklist` (PDF p16 "Minimum preregistration"). Template marks REQUIRED for cards 01-04; Q6S1 is not a card 01-04 study — completed here per Conductor all-new-freeze rule. Declared pre-outcome at 2026-09-25T00:39:00-04:00. Examiner `gate_status` null.

| # | Item | Status | Evidence |
|---|---|---|---|
| 1 | Freeze the market universe (`market_universe`) | **satisfied** | KXATPMATCH panel stub `2026-09-23.atp-kxatpmatch-v0` 6/12 sha256 `ed041c502d1f775d33c44bf900ac91b1339d99045bddd2052edd09a139ae2d3f` + scout hunt 48/24 sha256 `14c99ec8ea00bae507a21d0e6a1879fb94d32ef69ad4b5e3b40a9952821e5da7` + sports-screen raw 28/14 sha256 `b603474b3ca336b0a3678ff0deb8a937dfdcc4205e8e24db4d657d40d2323c60` (pin; panel not reinvented) |
| 2 | Freeze the exclusions (`exclusions`) | **satisfied** | KXATPMATCH ONLY; exclude Cap-SR/ATP-FQ/ETH-FQ/Q6S5 reopen; exclude PR57 INFRA duplicate; exclude invent fills/PnL/depth/settlement_ts; exclude S1 ML retune; exclude Pass-3/B2 promote |
| 3 | Freeze the receipt-time information set (`receipt_time_information_set`) | **satisfied** | Parent ATP panel + scout/sports raw GET bodies as received; in-memory GET stub at implement (`live_gets=0`) |
| 4 | Freeze the fee regime (`fee_regime`) | **satisfied** | quadratic_with_maker_fees×1 CACHE-LABELED; feebook @22371178cb2663250b4762f328069571c48cb551 FIXED; cache ≠ R1-P1 live until Examiner `/series` test |
| 5 | Freeze the order timing (`order_timing`) | **n/a** | no orders; GET-only; refuse `/orders` |
| 6 | Freeze the sizing (`sizing`) | **n/a** | no orders / no sizing; $5k bakeoff is shared rule pointer only |
| 7 | Freeze the fill model (`fill_model`) | **n/a** | no fills; invent fills REFUSED |
| 8 | Freeze the stopping rules (`stopping_rules`) | **satisfied** | freeze-before-implement; HOLD_PRE_PR; no dual-cloud; no cloud until ACCEPT |
| 9 | Freeze the evaluation metrics (`evaluation_metrics`) | **satisfied** | inventory_delta_flat_vs_binned / unresolved_inventory / position_bucket_gap / settled_join_n / n_books / results / pnl + v1.2 common_scorecard — all null |
| 10 | Limit candidate variants (`limit_candidate_variants`) | **satisfied** | one knob inventory_slice; arms Q6S1A0 / Q6S1A1 |
| 11 | Log every attempted variant (`log_every_attempted_variant`) | **satisfied** | only Q6S1A0/Q6S1A1 declared; further variants need new freeze |
| 12 | Separate discovery, tuning and untouched evaluation periods (`separate_discovery_tuning_evaluation_periods`) | **n/a** | measurement-only; panel/scout cohorts are pins |

Counts: satisfied 8, n/a 4; missing 0.

## Lab dir

`kalshi_q6s1_kxatpmatch_inventory_reproof_lab_20260925/` (do not mutate ATP-FQ / ATP-RJ / Cap-SR / Cap-SR-FX / Q6S5 / ETH-FQ / NHL-FQ / CPI-FQ / PR57 INFRA / feebook / rails / S1 KXMLBGAME / Arm B / Q7-B Pass-2 labs).

## Integrity (Clock gate)

- Transport: **in-memory GET stub**; `live_gets=0` at freeze; refuse `/orders` `/portfolio`; prefer `/events` while `/markets` hot.
- Commit attached freeze / maximize pins (0031ET + 0033ET) / kick / panel stub / Examiner HOLD bytes **verbatim**. Pin digests to `sha256sum`.
- **Refuse** labeled recreations / inventing markets/depth/fills/PnL/settlement_ts/inventory deltas.
- Fee remains CACHE-LABELED until live `/series` pin.
- `digest_all_match_claimed=false` for absent pins: panel_admitted, live /series fee, fresh 28/14 panel subset, invent fields, prior Archivist Q6S1 index.

## Merge gates

Units green when implemented; `results`/`pnl`/inventory deltas null; Examiner HOLD_PRE_PR → READY NOT_SCORED only after PR branch sha verify + merge + Clock admit path. **HOLD for Conductor ACCEPT — no CloudAgent / no PR / no admit.py / no live orders.**

## Refuse binds

invent fills/PnL/depth/settlement_ts/inventory deltas · Cap-SR/ATP-FQ/ETH-FQ/Q6S5/PR57-INFRA reopen · fee formula change · Q6-000 retune · S1 ML retune · Pass-3 / Refiner / B2 promote · Lee-Ready · `admit.py` by Variants · live orders · dual-cloud · claim CACHE fee = R1-P1 live without Examiner `/series` test · ungating S1/S2/R2-P4
