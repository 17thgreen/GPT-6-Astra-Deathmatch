# NFL adaptive-control research Q5

Start with NFL_Adaptive_Results.md. This is an offline development experiment,
not an order-enabled bot. No live orders, fresh completed holdout or continuous
recorder are included. Source/input hashes and every saved ledger are supplied.

Main frozen comparison: 3 candidates plus the existing router, 2 queue assumptions,
2 order/cancel latencies =16runs; one shared5k account over31reused games.
The capital-only controls and neutral-ranking diagnostics are separate additions.
Read CAPITAL_RECOVERY.md for the retained failed $1k run and uniform two-cent
buffer. Do not multiply the1k result into hypothetical multi-bot profit.

Python3.12 standard library, Linux, sufficient RAM for ~1million event rows plus
three forked replay workers. Reproduce from this directory:

```bash
python3 -m unittest -v test_replay_v2 test_queue_policies test_completion test_timing test_adaptive
python3 run_experiment.py
python3 run_capital_controls.py
python3 run_allocation_diagnostic.py
python3 verify_results.py
python3 build_report.py
```

These programs replace their own result files on rerun. Preserve the delivered
package before rerunning if you need an immutable record. The old capital-v1
runner is retained for failure provenance; its old freeze refers to the original
file names and is superseded. Do not use it as the current reproduction command.

inputs/events.jsonl.gz contains normalized trade/quote events; markets.json and
week_membership.json preserve identities and grouping. inputs/manifest.json
pins these files plus the original raw Q2 inputs; the prior Q2 delivery contains
those raw captures. The Q5 kit is standalone for normalized offline reproduction.

FROZEN_EXPERIMENT.json pins the primary rules/code. Supplemental freezes document
when the capital and neutral controls were added. BASELINE_HASHES.json pins all
unchanged inherited replay files. DELIVERY_MANIFEST.json covers the final kit.
All order/fill/decision ledgers are compressed JSON lines; no interpolation or
fabricated fills are used for missing forward data. Historical matches themselves
are explicitly hypothetical queue/participation counterfactuals.

FORWARD_PROTOCOL.md lists fresh-data gates; RESERVED_HOLDOUT.json is only a
schedule reservation. MULTIBOT_EXPERIMENT_DESIGN.md describes required shared
liquidity and wallet accounting; a multi-wallet simulator is not included.
