# R3-P2 queue_position unit results

September 23, 2026. This file records a code check of the frozen sample
ingest. It is a unit verification. It is not a calibration run, not a
simulated trading run, and not live validation. `FROZEN_EXPERIMENT.json`
still has status `SAMPLE_INGESTED_CALIBRATION_NOT_RUN` with `results`,
`abs_err_contracts`, `signed_bias`, `brier`, `pnl`, `mz`, and `roi` null.
`results/EMPTY_RESULTS.json` keeps the same nulls. Those fields stay null
on purpose. This page is not profit, and it is not folded back into the
freeze. No tape walk was run. No P&L figure is reported.

## Command

From `kalshi_r3_p2_queue_position_lab_20260923`, Python 3, standard library:

```bash
python3 -m unittest -v tests.test_ingest
```

Ran 4 tests in 0.002s at 2026-09-23T19:00:15Z. Result: OK. Failures: 0.
Errors: 0.

The checks that passed are the predeclared ones: the first poll loads with
`queue_position_fp` `"4207.00"`, ticker `KXNFLGAME-26OCT01PITCLE-PIT`,
verdict `POLL_OK`, a clean cancel, and fill absent. The series loads with
`n_success_this_run` 4, prior first included, `rows_total` 26,
`leftover_resting` `no`, and host `demo-api.kalshi.co` only. One sample
body is embedded. Twenty-five row bodies stay unembedded. Estimate-error
writes raise `CalibrationNotRun`. Profit labels raise `ProfitLabelRefused`.
The queue label cites R1-P5 and is `outside_pinned_bins`. `q3300` stays
3300 and `q10000` stays 10000. Live orders and a Q6-`000` retune raise.

## Limitation

Desk files `MECHANIC_FIRST_DEMO_QUEUE_POLL_2026-09-23.md`,
`MECHANIC_DEMO_QUEUE_SAMPLE_SERIES_2026-09-23.md`, and
`results/demo_queue_sample_series.json` were absent from this checkout.
The fixtures contain the stated keys. They do not contain the other 25
row bodies or the four this-run success payloads. L2 size stays the
narrative `~4208`.
