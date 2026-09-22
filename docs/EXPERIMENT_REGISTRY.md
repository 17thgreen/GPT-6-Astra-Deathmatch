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
| Q7 | Completed: guarded original router passes frozen simplification screen; 16 ledger audits and eight exact Q6 controls | `nfl_pair_price_lab_20260921/Q7_RESULTS.md` |

Prior Q6 candidate: `nfl_factorial_lab_20260921/SHADOW_CANDIDATE_FREEZE.json`.
Same 31 development games, 16 Week 1 and 15 Week 2, pooled $5,000. Q6 baseline
and selected candidate use the same hard 250-event cap and assumed total exit
depth 250 per game. The old $1,027.47 result used the original engine, 16 games
and early queue near 291; it is a different scenario, not a contradicted figure.

No always-on collector is running. The prior 32-game reservation is schedule-only;
most venue IDs and full-window coverage remain unverified. Never backdate a
missed admission/capture deadline or silently replace games after outcomes.

Current research candidate: `nfl_pair_price_lab_20260921/SHADOW_CANDIDATE_FREEZE.json`.
Q7 source was committed before outcomes at f0a2692; the specification at d15f57c.
115 unit tests pass. The selected router earns simulated $354.33/$353.89 at
queue 3,300 (.25s/5s), and $90.45/$79.08 at queue 10,000. No fresh evaluation
or live strategy promotion follows from this reused-cohort mechanism result.

Q8 complete: `nfl_joint_route_lab_20260921/EXPERIMENT_SPEC.md`. Joint routing
and rejected-pair recovery, with unchanged Q7 controls; market portability is a
separate algebra/adapter build. Both variants fail the frozen screen; Q7 remains selected. Primary completed
P&L: Q7 $354.33, recovery $360.03, joint $371.45; queue-10000/.25s:
$90.45/$73.27/$70.85. All 12 ledgers and four exact Q7 controls pass.
See `nfl_joint_route_lab_20260921/Q8_RESULTS.md`.

M1 complete: `market_access_lab_20260922/MARKET_UPDATE.md`. Descriptive six-sport
book census and execution-neutral adapters; 16 tests, 50 arithmetic checks,
6 retained timeouts. No fills simulated; no non-NFL P&L. Spec cfe48ab, source
freeze 079d7c7. NCAAF/WNBA historical adapter integration remains next.

M2 complete: `cross_sport_replay_20260922/M2_RESULTS.md`. Four NCAAF plus four
WNBA events, all 16 captures complete, twelve hypothetical transport scenarios.
Source/input freeze 3f12171 preceded outcomes. Ten new tests plus 152 inherited
tests pass; twelve independent ledger audits pass. At queues 3300/10000:
NCAAF +$2.47/-$2.80, WNBA -$45.18/-$35.29, combined -$42.72/-$38.09.
No sport promotion and no tuning. All raw inputs are in Git; compressed outcome
ledgers are indexed in DATA_ARCHIVE.json. Equal-total-capital fixed-versus-shared
bot allocation remains a separate unrun experiment direction.

M3 complete: `market_adaptation_20260922/M3_RESULTS.md`. Spec 58ae378, source/input
freeze f20bd36. 32 individual-sport cutoff x queue-environment x depth x delay
cases; all flat and independently audited, eight exact M2 controls, 174 tests.
CFB late/constant-depth net $79.02/$30.51 at queues 3300/10000, but no late-cutoff
gain under the inherited NFL late-depth profile. WNBA negative throughout.
No promotion; NFL Q7 unchanged. Separate six-series metadata availability audit
specified at f80f984; reservations are not replay admission or profitability.
Next stages: independent market adaptation, matched-calendar comparison, then
capital capacity and feasible reinvestment. All tried variants remain visible.
