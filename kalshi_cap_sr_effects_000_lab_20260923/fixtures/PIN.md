# Q6-000 fixture pin for the Cap-SR effects path

The production ledgers are the factorial results named below. `*.jsonl.gz` is
gitignored, so a checkout can lack the bytes. The index entry is the pin.
`synthetic_q3300_d0.25_000_*.jsonl` is a schema stand-in for FX0. It is not
the production gzip and it is not a replay.

`synthetic_borrow_stress_*.jsonl` is the FX1 unit fixture. It forces a
cross-event borrow and a blend-pool draw through the imported Cap-SR engine.
It is not a market panel.

| Role | Path | SHA-256 | Bytes |
|---|---|---|---|
| FX0 fills | `nfl_factorial_lab_20260921/results/q3300_d0.25_000_fills.jsonl.gz` | `9d56f5d3c599e092606be9f4a1ad41ae8baabff4921d3d722adf0b57ac944a3f` | 534945 |
| FX0 orders | `nfl_factorial_lab_20260921/results/q3300_d0.25_000_orders.jsonl.gz` | `c390801b9a7cf6d182d2d097123ed944792980524a7975e6e59a904a530f4b1c` | 569767 |

Hashes match `nfl_factorial_lab_20260921/DELIVERY_MANIFEST.json`. The strategy
label on the pinned stem is `000`. Queue 10000 is not an FX arm.

When the primary gzip pair is absent, FX0 reads the synthetic jsonl pair in
this directory. Restoring the kit does not authorize writing
`borrow_count_delta_vs_fifo`, `blend_utilization_gap`,
`soft_breach_or_blend_rate`, `effects_path_fixture_id`, `results`, or `pnl`
into `FROZEN_EXPERIMENT.json`.
