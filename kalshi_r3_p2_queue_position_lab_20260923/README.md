# R3-P2 queue_position calibration lab

Sanitized Mechanic demo `queue_position_fp` samples. Calibration is not run.
Status: `SAMPLE_INGESTED_CALIBRATION_NOT_RUN`.

`results`, `abs_err_contracts`, `signed_bias`, `brier`, `pnl`, `mz`, and
`roi` stay null.

```bash
cd kalshi_r3_p2_queue_position_lab_20260923
python3 -m unittest -v tests.test_ingest
```

The first poll is the sample_id 0 cross-check: ticker
`KXNFLGAME-26OCT01PITCLE-PIT`, `queue_position_fp` `4207.00`, verdict
`POLL_OK`, a clean cancel. The series source is
`lab/governance/astra/packets/r3_p2_queue_position/results/demo_queue_sample_series.json`
with schema `{meta, samples[]}`. Authentic sha256
`74ef9a9bb54054691e26b7b752568c8e833f51d21292034b1f40b9f3ca4ba8b4`.
`samples_n` is 38. `leftover_resting` is `no`. The fixture copy is the same
bytes. Calibration is not run. Queue labels cite R1-P5.
Q6-`000` is not retuned. No live orders.
