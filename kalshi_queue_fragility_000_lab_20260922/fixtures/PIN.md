# Q6-000 fixture pin for the queue-fragility join

The production ledgers are the factorial results named below. `*.jsonl.gz` is
gitignored, so a checkout can lack the bytes. The index entry is the pin.
This directory's `synthetic_q3300_d0.25_000_*.jsonl` files are a schema
stand-in for the harness. They are not the production gzip and they are not a
replay.

Pick A reads the same production paths from
`kalshi_r2p1_hygiene_000_lab_20260922/fixture_join.py` and
`kalshi_r2p1_hygiene_000_lab_20260922/fixtures/`. This lab does not import a
`kalshi_r2p1_fixture_join_000_lab_*` tree. That second directory is gone.

| Role | Path | SHA-256 | Bytes |
|---|---|---|---|
| Primary fills | `nfl_factorial_lab_20260921/results/q3300_d0.25_000_fills.jsonl.gz` | `9d56f5d3c599e092606be9f4a1ad41ae8baabff4921d3d722adf0b57ac944a3f` | 534945 |
| Primary orders | `nfl_factorial_lab_20260921/results/q3300_d0.25_000_orders.jsonl.gz` | `c390801b9a7cf6d182d2d097123ed944792980524a7975e6e59a904a530f4b1c` | 569767 |
| Harsh twin fills | `nfl_factorial_lab_20260921/results/q10000_d0.25_000_fills.jsonl.gz` | `678d6cb602fb832f8a77ac7a0cfefd9a4d8390002b0962ddc956ba1f19f4b59d` | 174316 |
| Harsh twin orders | `nfl_factorial_lab_20260921/results/q10000_d0.25_000_orders.jsonl.gz` | `e16632b630058854bfc6ac410cb960d5439fb8a151e180d0793c37e8f92068d9` | 553661 |

Hashes match `nfl_factorial_lab_20260921/DELIVERY_MANIFEST.json`. The harsh
twin is a queue label only. It is not a second fee knob. The default join
does not open it. The strategy label on every pinned stem is `000`.

When the primary gzip pair is absent, the join harness reads the synthetic
jsonl pair in this directory. Restoring the kit does not authorize writing
`fill_rate_delta_vs_q3300`, `adverse_queue_exposure`,
`participation_stress_gap`, `results`, or `pnl` into `FROZEN_EXPERIMENT.json`.
