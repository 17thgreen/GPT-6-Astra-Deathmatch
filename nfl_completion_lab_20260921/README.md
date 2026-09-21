# NFL Completion Lab Q2

Research only. No account access, API key or live order placement. Python 3.12 standard library.

The frozen experiment compares the previous Q1 router, a joint two-leg entry gate, and that gate plus an event-level inventory-completion controller. Read `EXPERIMENT_SPEC.md` for all rules and limitations. No threshold tuning is performed after results.

Inputs include the 16 original week-one games and 15 additional completed week-two games. Week two was chosen by schedule and completed window, excluding Monday NYG–LAR before its cutoff. It appeared in older repository aggregates and is not claimed to be a pristine holdout. Original week-one captures and all additional public captures are included and hashed.

The pooled 31-game runs use ONE $5,000 account across overlapping pregame windows. Isolated week-one and week-two runs each reset to $5,000; their profits must not be added and labeled the actual pooled result.

Run offline from this directory:

```bash
python3 -m unittest -v test_replay_v2 test_queue_policies test_completion
python3 run_experiment.py
python3 verify_results.py
python3 build_report.py
```

`collect_week2.py` is an optional online public REST collector. It resumes verified completed market captures and has bounded retries. The delivered data make redownloading unnecessary. Both published trade timestamps and assumed candle-publication delays retain the preceding replay's limitations; raw input hashes do not prove our hypothetical orders would fill.

`replay_v2.py` and `queue_policies.py` are unchanged copies of Q1's accounting engine and router, pinned by BASELINE_HASHES.json. The policy, loader, runner and new tests are pinned by FROZEN_CODE.json before new outcomes. Q1_REGRESSION_REFERENCE.json retains the three week-one route results used as regression gates. No private repository source is included.

`completion_policy.py` subtracts queue volume before projecting available fills, evaluates two directions jointly, and optionally concentrates on offsetting existing inventory. It uses a deterministic steady-flow projection, not a calibrated probability. Pair admission cannot make fills atomic or guarantee the offset price will persist. Cancellation and quantity-change acknowledgment races remain possible and are measured. This is not an exchange-native cross-ticker reduce-only order type.

`results/` contains all 30 ledgers, cohort summaries, per-game results, tests and verification. Completed P&L is reported only if positions are flat at completed windows; otherwise use residual quantities and payout bounds. Historical queues, account-specific fee history, complete collateral mechanics, actual receipt latency and executable exit depth remain assumptions.
