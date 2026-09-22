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
