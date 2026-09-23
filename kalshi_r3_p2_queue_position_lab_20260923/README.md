# R3-P2 queue_position calibration lab

Sanitized Mechanic demo `queue_position_fp` samples. Calibration is not run.
Status: `SAMPLE_INGESTED_CALIBRATION_NOT_RUN`.

`results`, `abs_err_contracts`, `signed_bias`, `brier`, `pnl`, `mz`, and
`roi` stay null.

```bash
cd kalshi_r3_p2_queue_position_lab_20260923
python3 -m unittest -v tests.test_ingest
```

The first poll is ticker `KXNFLGAME-26OCT01PITCLE-PIT`,
`queue_position_fp` `4207.00`, verdict `POLL_OK`, a clean cancel. The series
states 4 successes this run, the prior first included, 26 rows total,
`leftover_resting` `no`, host `demo-api.kalshi.co` only. Queue labels cite
R1-P5. Q6-`000` is not retuned. No live orders.

Code verification on 2026-09-23T19:00:15Z: 4 tests, 0 failures. That run is
recorded in `results/UNIT_RESULTS.md`. It does not fill the scorecard.
