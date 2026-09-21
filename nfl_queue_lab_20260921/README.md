# NFL Queue Lab Q1

Offline, credential-free research package. No live order placement. Python 3.12 standard library is sufficient for this package's documented commands.

Run from this directory:

```bash
python3 -m unittest -v test_replay_v2 test_queue_policies test_forward
python3 run_queue_suite.py
python3 run_mechanism_check.py
python3 run_queue_stress.py
python3 analyze_forward.py
python3 verify_results.py
python3 build_report.py
```

`run_queue_suite.py` runs the fourteen frozen cases, verifies raw input hashes and the exact earlier five-minute-wind-down baseline P&L, and saves summaries plus every hypothetical fill. `run_mechanism_check.py` is explicitly a later, two-case flow-score ablation. `analyze_forward.py` analyzes the saved public REST observation session; it does not fetch new data or place orders. Forward service measurements are overlapping hypothetical joins, not actual orders or independent trading trials.

`run_queue_stress.py` adds four post-result hypothetical large-queue cases specified in `QUEUE_STRESS_SPEC.md`. These are sensitivity assumptions, not historical estimates inferred from today's books.

Read `EXPERIMENT_SPEC.md` before interpreting results. `FROZEN_INPUTS.json` locks its bytes and the unchanged previous accounting engine. The primary simulations use the original static queue assumptions; current books never replace historical queues. Historical candles are delayed by an assumed sixty seconds, and inside-spread quotes are counterfactual insertions into a fixed tape. Fees, collateral release and liquidation depth retain the prior research assumptions.

The preserved 16-game cohort is 2026 NFL week one, 32 team markets. It contains 387,258 pre-cutoff trades plus 3,860 five-minute postlude prints, and 173,074 minute quote records. Games are already examined development data, not a sealed holdout. All cases use a single shared $5,000 account, 250-contract event cap and five-minute wind-down ahead of T−3 hours.

## Files

- `replay_v2.py`: unchanged prior accounting/clock/reservation engine.
- `queue_policies.py`: preservation/churn, equivalent-payoff routing, FIFO pair-margin gate for one-cent exit improvement, and causal trailing trade flow.
- `run_queue_suite.py`: controlled suite and ex-post markouts.
- `run_mechanism_check.py`: margin-only routing diagnostic.
- `capture_queue.py`: bounded public GET-only recorder with pagination, timestamps and resumable append.
- `analyze_forward.py`: observed depth/flow/latency, shadow route rankings and hypothetical join service.
- `data/`: original public captures and manifests; `forward/`: new raw public observations.
- `results/`: machine-readable summaries, complete hypothetical fill logs, tests and integrity checks.

`run_suite.py` and `run_candle_suite.py` are retained as input loaders. Do not use their older standalone experiment entrypoints for Q1. The legacy repository comparison option in `run_suite.py` is not part of this package; it requires the separate prior audit kit and private repository sources. No private repository source code is included here.

For a new bounded public recording, use a fresh copy/directory for `capture_queue.py`; the bundled observations are intentionally protected against silent overwrite. `--resume` appends after the last recorded round and is for an interrupted session only. The observed workspace HTTP latency made the original five-second target cadence unattainable at first; an explicitly recorded interruption switched to four independent concurrent GETs. Do not describe the saved feed as uninterrupted or exchange-native latency.

No process is intended to remain running after the session finishes. Exact position for an owned resting order requires authenticated account access; public depth only approximates the initial queue a newly submitted order might join.
