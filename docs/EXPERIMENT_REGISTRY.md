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
| Q7 | Proposed: isolate the actual chosen-pair price check; NOT YET RUN | `docs/NEXT_EXPERIMENT.md` |

Current Q6 candidate: `nfl_factorial_lab_20260921/SHADOW_CANDIDATE_FREEZE.json`.
Same 31 development games, 16 Week 1 and 15 Week 2, pooled $5,000. Q6 baseline
and selected candidate use the same hard 250-event cap and assumed total exit
depth 250 per game. The old $1,027.47 result used the original engine, 16 games
and early queue near 291; it is a different scenario, not a contradicted figure.

No always-on collector is running. The prior 32-game reservation is schedule-only;
most venue IDs and full-window coverage remain unverified. Never backdate a
missed admission/capture deadline or silently replace games after outcomes.
