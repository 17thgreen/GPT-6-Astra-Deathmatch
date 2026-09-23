# R3-P2 queue_position unit results

September 23, 2026. This file records a code check of the series ingest.
It is a unit verification. It is not a calibration run, not a simulated
trading run, and not live validation. `FROZEN_EXPERIMENT.json` has status
`SAMPLE_INGESTED_CALIBRATION_NOT_RUN` with `results`, `abs_err_contracts`,
`signed_bias`, `brier`, `pnl`, `mz`, and `roi` null. `calibration_run` is
false.

## Pin

Desk path
`lab/governance/astra/packets/r3_p2_queue_position/results/demo_queue_sample_series.json`.

- `series_sha256`: `74ef9a9bb54054691e26b7b752568c8e833f51d21292034b1f40b9f3ca4ba8b4`
- fixture sha256: the same digest
- `samples_n`: 38
- `leftover_resting`: `no`
- `n_success_including_prior`: 17
- `n_success_new_total`: 16
- `null_queue_position_n`: 18
- `queue_positions_batch_present`: false
- bytes rewritten: false

The counted unit run for this pin is recorded after the source revision
that added these bytes.

## Command

From `kalshi_r3_p2_queue_position_lab_20260923`, Python 3, standard library:

```bash
python3 -m unittest -v tests.test_ingest
```

## Limitation

The desk file has no `queue_positions` array. Eighteen `queue_position_fp`
values are null. They were not filled in. Twenty-eight samples have
`final_status` `resting` while `meta.leftover_resting` is `no` and
`final_resting_ids` is empty. Those rows were not relabeled and were not
scored. The first-poll fixture still has L2 `size_exact` null and size
narrative `~4208`. The series L2 snapshot was not copied onto that fixture.
This page is not profit. Calibration is not run.
