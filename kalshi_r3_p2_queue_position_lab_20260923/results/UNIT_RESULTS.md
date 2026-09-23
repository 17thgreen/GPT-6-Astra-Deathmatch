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

## Command

From `kalshi_r3_p2_queue_position_lab_20260923`, Python 3, standard library:

```bash
python3 -m unittest -v tests.test_ingest
```

Ran 6 tests in 0.007s at 2026-09-23T19:16:17Z. Result: OK. Failures: 0.
Errors: 0.

The checks that passed: the first poll loads with `queue_position_fp`
`"4207.00"`, ticker `KXNFLGAME-26OCT01PITCLE-PIT`, verdict `POLL_OK`, a
clean cancel, and fill absent. A missing path raises `SeriesSourceAbsent`
and writes no file. The desk series sha256 is
`74ef9a9bb54054691e26b7b752568c8e833f51d21292034b1f40b9f3ca4ba8b4`,
`samples_n` is 38, and `leftover_resting` is `no`. The fixture bytes match
the desk bytes. An in-memory `{meta, samples[]}` document with a
`queue_positions` batch matches `queue_position_fp` by `order_id`, keeps
estimate fields null, and refuses a fill. A document without that batch
does not receive invented positions. R1-P5 `q3300` stays 3300 and
`q10000` stays 10000.

## Limitation

The desk file has no `queue_positions` array. Eighteen `queue_position_fp`
values are null. They were not filled in. Twenty-eight samples have
`final_status` `resting` while `meta.leftover_resting` is `no` and
`final_resting_ids` is empty. Those rows were not relabeled and were not
scored. The first-poll fixture still has L2 `size_exact` null and size
narrative `~4208`. The series L2 snapshot was not copied onto that fixture.
This page is not profit. Calibration is not run.
