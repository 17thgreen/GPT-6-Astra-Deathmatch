# R3-P2 queue_position calibration lab

Status: hypothesis committed before a calibration outcome. Feature family
R3-P2. This lab ingests sanitized Mechanic demo `queue_position_fp` samples
and leaves the scorecard null.

Status string: `SAMPLE_INGESTED_CALIBRATION_NOT_RUN`.

## Question

Do the Mechanic demo samples load with `queue_position_fp` present, with the
first poll recorded as a clean cancel, and with the calibration fields left
null?

## Samples

Desk narratives were absent from this checkout. The fixtures embed the stated
keys.

| Source | Embedded fact |
|---|---|
| `MECHANIC_FIRST_DEMO_QUEUE_POLL_2026-09-23.md` | verdict `POLL_OK`, ticker `KXNFLGAME-26OCT01PITCLE-PIT`, `queue_position_fp` `"4207.00"`, order canceled clean, fill absent, L2 top price `0.01`, size narrative `~4208` |
| `MECHANIC_DEMO_QUEUE_SAMPLE_SERIES_2026-09-23.md` and `results/demo_queue_sample_series.json` | `n_success_this_run` 4, prior first included, `rows_total` 26, `leftover_resting` `no`, host `demo-api.kalshi.co` only |

The prior first poll is the one embedded sample body. The other 25 row bodies
and the four this-run success payloads were not in the checkout and were not
invented. Exact L2 size was stated as `~4208`, so `size_exact` stays null.

## Rails cite

A queue label join calls `queue_attribution_bin` from
`kalshi_r2p1_hygiene_000_lab_20260922`, which reads R1-P5
`kalshi_rails_lab_20260922` @ `6a28e0d6254327ea4e6451c781bec56215ac6cac`.
Pinned magnitudes stay `q3300` = 3300 and `q10000` = 10000.
`4207.00` lands in `outside_pinned_bins`. That label is not a scorecard
write. Q6-`000` is not retuned.

## Hard nulls

`results`, `abs_err_contracts`, `signed_bias`, `brier`, `pnl`, `mz`, and
`roi` stay null. Estimate-error writes raise `CalibrationNotRun`. Profit
labels raise `ProfitLabelRefused`. Live orders are refused. Hosts other than
`demo-api.kalshi.co` are refused. `leftover_resting` other than `no` is
refused.

Feebook `22371178cb2663250b4762f328069571c48cb551` is cited as the sibling
pin and is not used to price this sample. No Logan keys. No secrets in the
fixtures.
