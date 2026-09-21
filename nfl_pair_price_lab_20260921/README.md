# Q7 paired-price mechanism study

Read EXPERIMENT_SPEC.md before running. Requires Python 3.12 and the unchanged
Q6 modules in `../nfl_factorial_lab_20260921`; all dependencies are hashed.
No network or order-placement capability is included in the replay.

The normalized `inputs/events.jsonl.gz` is identical to the Q6 kit's copy,
SHA-256 cd300e664c2c5f2ff344c4b1eb17dd3f8e5f3326168b9dd8e3ade94a3a7382b4.
It is excluded from routine Git commits. Restore that file from the delivered
Q6 kit before running; the manifest checks its bytes. Market mappings and week
membership are tracked. The standalone Q7 delivery kit includes these inputs
and the required unchanged Q6 source modules.

From this directory:

```bash
python -m unittest -q test_pair_policy test_q7_analysis test_replay_v2 test_queue_policies test_completion test_timing test_adaptive test_factorial test_analysis
python run_experiment.py
python verify_results.py
python q7_analysis.py
```

Preserve delivered results before any rerun. The runner writes sixteen separate
scenario records and fill/order/decision/pair ledgers. Pair diagnostics stream
to disk; they do not influence fills. allocator_on delegates policy ranking to
the unchanged Q6 method and only observes its choice afterward. Both unchanged
control arms must reproduce exact Q6 fill/order ledger hashes in all settings.

Q7 is a mechanism test on the reused development sample. No live-profitability
claim, fresh holdout completion, continuous recorder or multi-wallet simulator
is supplied by this experiment.
