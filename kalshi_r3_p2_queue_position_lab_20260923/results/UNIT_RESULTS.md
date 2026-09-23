# R3-P2 queue_position unit results

September 23, 2026. This file records a code check of the series ingest.
It is a unit verification. It is not a calibration run, not a simulated
trading run, and not live validation. `FROZEN_EXPERIMENT.json` still has
status `SAMPLE_INGESTED_CALIBRATION_NOT_RUN` with `results`,
`abs_err_contracts`, `signed_bias`, `brier`, `pnl`, `mz`, and `roi` null.
`series_embedded` is false. `series_sha256` is null. `samples_n` is null.
Those fields stay null on purpose. This page is not profit.

## Command

From `kalshi_r3_p2_queue_position_lab_20260923`, Python 3, standard library:

```bash
python3 -m unittest -v tests.test_ingest
```

Ran 5 tests in 0.001s at 2026-09-23T19:07:28Z. Result: OK. Failures: 0.
Errors: 0.

The checks that passed: the first poll loads with `queue_position_fp`
`"4207.00"`, ticker `KXNFLGAME-26OCT01PITCLE-PIT`, verdict `POLL_OK`, a
clean cancel, and fill absent. The desk series path
`lab/governance/astra/packets/r3_p2_queue_position/results/demo_queue_sample_series.json`
is absent, and `embed_desk_series` raises `SeriesSourceAbsent` without
writing `fixtures/demo_queue_sample_series.json`. An in-memory
`{meta, samples[]}` document matches `queue_position_fp` to
`queue_positions` by `order_id`, keeps estimate fields null, and refuses a
fill. That in-memory document is not written as the Mechanic series.
R1-P5 `q3300` stays 3300 and `q10000` stays 10000.

## Limitation

The operator desk series JSON was not on this checkout at 2026-09-23T19:07:28Z.
`samples[]` was not invented. `n_success_including_prior` and
`n_success_new_total` are null in the freeze until that file is read.
The earlier partial summary (4 successes, 26 rows, 25 unembedded bodies)
is withdrawn.
