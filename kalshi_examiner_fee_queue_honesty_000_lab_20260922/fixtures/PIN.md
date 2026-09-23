# Q6-000 fixture pin for the Examiner fee and queue channel

The production ledgers are the factorial results named below. `*.jsonl.gz` is
gitignored, so a checkout can lack the bytes. The freeze kernel records that
the fills gzip was present on the freeze desk. This pin is the path and the
sha256. It does not contain the file bytes.

When both production files exist and match these hashes, the orchestrator
sends that pair to the hygiene join and the queue-fragility join. When they
are absent, both joins read one synthetic schema stand-in:

`kalshi_queue_fragility_000_lab_20260922/fixtures/synthetic_q3300_d0.25_000_fills.jsonl`

and its orders file. The hygiene lab's own synthetic pair is not that stream.
Its one-cent maker quote is refused by the queue-fragility instrument, so it
cannot be the shared fills stream. Neither synthetic is a replay.

| Role | Path | SHA-256 |
|---|---|---|
| Primary fills | `nfl_factorial_lab_20260921/results/q3300_d0.25_000_fills.jsonl.gz` | `9d56f5d3c599e092606be9f4a1ad41ae8baabff4921d3d722adf0b57ac944a3f` |
| Primary orders | `nfl_factorial_lab_20260921/results/q3300_d0.25_000_orders.jsonl.gz` | `c390801b9a7cf6d182d2d097123ed944792980524a7975e6e59a904a530f4b1c` |

Hashes match `nfl_factorial_lab_20260921/DELIVERY_MANIFEST.json` and both
join modules. The harsh twin `q10000_d0.25_000_*` stays unloaded. Restoring
the kit does not authorize writing scorecard metrics into
`FROZEN_EXPERIMENT.json`.
