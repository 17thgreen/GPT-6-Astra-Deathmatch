# NFL timing and event-cap research Q4

Read NFL_Timing_Cap_Results.md and EXPERIMENT_SPEC.md. The 52-case experiment
uses the same previously examined 31 games, one shared $5,000 bankroll, and
explicit hypothetical queue/exit assumptions. No live trading is included.

The results distinguish desired order size from event exposure cap. They also
distinguish an entry window from an exit deadline. The prior Q1/Q2 engine and
router are unchanged and pinned by BASELINE_HASHES.json.

Reproduce with Python 3.12 standard library on Linux:

```bash
python3 -m unittest -v test_replay_v2 test_queue_policies test_completion test_timing test_collector
python3 run_experiment.py
python3 verify_results.py
python3 collector/inspect_capture.py collector/development_capture.sqlite --output results/collector_verification.json
python3 build_report.py
```

The runner uses three forked worker processes and atomic per-case files. It
requires enough RAM for roughly one million normalized event rows plus workers.
`inputs/manifest.json` includes hashes of those standalone normalized inputs
and all original Q2 raw files used to prepare them. The previously delivered Q2
kit contains the complete original raw venue captures. `prepare_data.py` is only
needed to re-extract from that original sibling project; it is not required for
offline reproduction of this package.

`results/` contains all 52 case summaries and compressed fill/order ledgers.
An unresolved case has null completed P&L and explicit residual quantities and
payout bounds. Do not convert its cashflow or payout bound into completed profit.
`FROZEN_EXPERIMENT.json` pins rules, strategy code and input manifests before the
run. The two old Q2 financial regressions are retained and verified.

`collector/OPERATIONS.md` gives local and Docker commands for persistent
development-data collection. A successful restart test is included, along with
the initial timeout and recovery record. The Docker configuration is prepared
but not deployed; no continuous service or future holdout collection is active.
The recorder's entrypoint contains only public market-data routes and cannot
place an order. Existing panel changes require a new retained collection
database, so old and new cohorts are not silently mixed.
