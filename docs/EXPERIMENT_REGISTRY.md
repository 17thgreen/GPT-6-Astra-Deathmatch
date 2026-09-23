# Experiment registry

This initial checkpoint imports work already completed before this repository
existed. Original timestamps and file hashes are retained; the import commit is
not presented as a pre-outcome Git preregistration of that historical work.

| Stage | Evidence/status | Primary record |
|---|---|---|
| Stern adaptation | Historical model and settlement research; consult each retained round's status | `stern_lab/MODEL_STATUS.json` |
| Maker audit/replay | Original model defects and repaired execution accounting | `maker_replay_round2/NFL_Maker_REST_Replay_Results.md` |
| Q1 | Queue sensitivity and routing; early queue remains an assumption | `nfl_queue_lab_20260921/NFL_Queue_Experiment_Results.md` |
| Q2 | Completion policies reduced inventory but did not maximize net profit | `nfl_completion_lab_20260921/NFL_Completion_Experiment_Results.md` |
| Q3 | Public measurement and prospective cohort requirements; no completed forward validation | `nfl_measurement_lab_20260921/NFL_Measurement_Results.md` |
| Q4 | Early-week small orders failed; cap sensitivity matters | `nfl_timing_lab_20260921/NFL_Timing_Cap_Results.md` |
| Q5 | Allocation bundle improved development P&L; ranking attribution unresolved | `nfl_adaptive_lab_20260921/NFL_Adaptive_Results.md` |
| Q6 | Simplest allocator selected; optional F/P/R features unnecessary under declared retention rule | `nfl_factorial_lab_20260921/NFL_Allocation_Factorial_Results.md` |
| Q7 | Implemented and frozen; 16 scenarios NOT RUN (historical tape absent) | `nfl_paircheck_lab_20260922/EXPERIMENT_SPEC.md` |
| Prospective recorder | GET-only schedule-only admission path. Rules frozen before the 2026-09-22 listing snapshot. 16 week-4 games have venue ids; PHI@CHI is not backfilled; week 5 is unresolved. Not deployed. Not a P&L experiment. Separate from Q7. | `nfl_prospective_recorder_20260922/PROTOCOL.md` |
| R1-P1 | Reciprocal book and fee algebra pinned to unit tests. Code verification only; no simulated or live P&L. Does not replace the Q6 candidate. | `kalshi_feebook_lab_20260922/results/FEEBOOK_UNIT_RESULTS.md` |
| R1-P5 | Queue, fee-credit, freshness, and MICRO scorecard rails pinned to unit tests. Code verification only; no simulated or live P&L. Does not replace the Q6 candidate. | `kalshi_rails_lab_20260922/results/RAILS_UNIT_RESULTS.md` |
| Capital structure | Shared $5,000 partition rails for A1/A2/A3. Imports the R1-P1 feebook and R1-P5 rails. Code verification only; no tape-walk P&L. Does not replace the Q6 candidate. | `kalshi_capital_structure_lab_20260922/results/CAPITAL_STRUCTURE_UNIT_RESULTS.md` |
| R2-P1 | Feebook and rails hygiene labels on Q6-000. Fee delta versus the inherited fixed-point model, content-fresh versus keepalive, and queue-bin mismatch against fixed q3300/q10000. Canonical freeze `R2-P1_FEEBOOK_RAILS_HYGIENE_000_FREEZE_2026-09-22.md` (sha256 prefix `ddcd4427`); bytes not in this checkout. `fee_sensitivity_000_r1p1` superseded; no second lab. Code verification only; pre-settlement outputs null. Does not replace the Q6 candidate. | `kalshi_r2p1_hygiene_000_lab_20260922/results/R2P1_UNIT_RESULTS.md` |
| Queue fragility | Q6-000 queue/fill stress under R1-P5. Arms QF0, QF1, and QF2 differ in rails queue parameters only. Feebook examiner channel fixed at R1-P1 (`22371178cb2663250b4762f328069571c48cb551`). Rails knob `6a28e0d6254327ea4e6451c781bec56215ac6cac`. Capital is the shared A1-equivalent pool. Freeze sha256 `e01d684abefd2d919ac6546f85619a246ce73098c04f7b24c84451ff49b00308`. Code verification only; pre-settlement outputs null. Does not replace the Q6 candidate. | `kalshi_queue_fragility_000_lab_20260922/results/QUEUE_FRAGILITY_UNIT_RESULTS.md` |
| R2-P1 fixture join | Pick A, accepted. Read-only join of Q6-000 fill and order fixtures into the R2-P1 hygiene helpers, inside `kalshi_r2p1_hygiene_000_lab_20260922` (one lab). Feebook `22371178cb2663250b4762f328069571c48cb551`. Rails `6a28e0d6254327ea4e6451c781bec56215ac6cac`. Freeze sha256 `e9bac91ca908b2ba704d966f0cf48cb181070ac11de1d117b93512bd2719ae1c`. Production gzip ledgers are gitignored; the lab ships a synthetic schema stand-in and pins the factorial path. Code verification only. `fee_delta_vs_inherited_model`, `freshness_gap_sec`, `queue_bin_mismatch_rate`, `results`, and `pnl` stay null. Does not replace the Q6 candidate. | `kalshi_r2p1_hygiene_000_lab_20260922/results/FIXTURE_JOIN_UNIT_RESULTS.md` |
| QF fixture join | Pick B. Read-only join of Q6-000 fill and order fixtures through QF0, QF1, and QF2 inside `kalshi_queue_fragility_000_lab_20260922`. Fee fixed at the R1-P1 examiner (`22371178cb2663250b4762f328069571c48cb551`). Rails `6a28e0d6254327ea4e6451c781bec56215ac6cac`. Freeze sha256 `d95adb9b7e8aba852134c96b8f0f7d35a76bbf68254b8808f82f99ec82bb6ca4`. Production gzip pin documented; synthetic stand-in when the gzip is absent. Code verification only. `fill_rate_delta_vs_q3300`, `adverse_queue_exposure`, `participation_stress_gap`, `results`, and `pnl` stay null. Does not replace the Q6 candidate. | `kalshi_queue_fragility_000_lab_20260922/results/FIXTURE_JOIN_UNIT_RESULTS.md` |
| Examiner fee+queue honesty | One Examiner channel on Q6-000. Imports the hygiene join (`79800a82b8ad2c1e10f614f69fd7105d11e0d041`) and the QF join (`7026be5104cd00cabcf9b34154506a76b2768b8a`). Feebook `22371178cb2663250b4762f328069571c48cb551`. Rails `6a28e0d6254327ea4e6451c781bec56215ac6cac`. Freeze sha256 `4799642e54cf233a925697e00c5a9e29f5cb39070962a2e011f0fbe090c169f2`. Code verification only. Production gzip pin documented; this checkout used one synthetic stand-in. Queue fields and fee fields share one refuse path. `fee_delta_vs_inherited_model`, `freshness_gap_sec`, `queue_bin_mismatch_rate`, `fill_rate_delta_vs_q3300`, `adverse_queue_exposure`, `participation_stress_gap`, `results`, and `pnl` stay null. No target edge ratio. Does not replace the Q6 candidate. | `kalshi_examiner_fee_queue_honesty_000_lab_20260922/results/EXAMINER_UNIT_RESULTS.md` |

Current Q6 candidate: `nfl_factorial_lab_20260921/SHADOW_CANDIDATE_FREEZE.json`.
Same 31 development games, 16 Week 1 and 15 Week 2, pooled $5,000. Q6 baseline
and selected candidate use the same hard 250-event cap and assumed total exit
depth 250 per game. The old $1,027.47 result used the original engine, 16 games
and early queue near 291; it is a different scenario, not a contradicted figure.

No always-on collector is running. Preparing a Docker file or a prospective
panel is not deployment. The prior 32-game reservation cannot support a
complete-cohort comparison: PHI@CHI's full T−7d window opened
2026-09-22T00:15:00Z with no durable recorder. Admission rules for a new
schedule-only version are in `nfl_prospective_recorder_20260922/PROTOCOL.md`.
Never backdate a missed admission/capture deadline or silently replace games
after outcomes.
