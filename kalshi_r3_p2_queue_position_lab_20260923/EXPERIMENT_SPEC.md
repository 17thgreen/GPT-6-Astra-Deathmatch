# R3-P2 queue_position calibration lab

Status: `SAMPLE_INGESTED_CALIBRATION_NOT_RUN`. Feature family R3-P2.
Calibration fields stay null.

## Question

Does the Mechanic series load as `{meta, samples[]}`, with each
`queue_position_fp` matched to batch `queue_positions` by `order_id`, and
with `sample_id` 0 equal to the first poll, while estimate-error fields stay
null?

## Samples

| Source | Role |
|---|---|
| `fixtures/first_demo_queue_poll.json` | sample_id 0 cross-check. Verdict `POLL_OK`, ticker `KXNFLGAME-26OCT01PITCLE-PIT`, `queue_position_fp` `"4207.00"`, clean cancel, fill absent, L2 top `0.01`, size narrative `~4208` |
| `lab/governance/astra/packets/r3_p2_queue_position/results/demo_queue_sample_series.json` | Series body. Schema `{meta, samples[]}`. sha256 `74ef9a9bb54054691e26b7b752568c8e833f51d21292034b1f40b9f3ca4ba8b4`. Narrative `MECHANIC_DEMO_QUEUE_SAMPLE_SERIES_2026-09-23.md` |
| `fixtures/demo_queue_sample_series.json` | Same bytes as the desk file. No secret keys were present, so the copy was not reformatted |

The desk file is on this checkout. `samples_n` is 38. `samples[]` was not
invented. The file has no `queue_positions` array, and the loader does not
add one. Eighteen `queue_position_fp` values are null and stay null. When a
document does contain `queue_positions`, each sample matches that batch by
`order_id`. `meta.n_success_including_prior` is 17 and
`meta.n_success_new_total` is 16, the file stamps.
`leftover_resting` is `no`. `final_resting_ids` is empty. Twenty-eight
samples have `final_status` `resting`; those rows are not relabeled and are
not scored. Host `demo-api.kalshi.co` only. Series rows record
`https://demo-api.kalshi.co`.

## Rails cite

A queue label join calls `queue_attribution_bin` from
`kalshi_r2p1_hygiene_000_lab_20260922`, which reads R1-P5
`kalshi_rails_lab_20260922` @ `6a28e0d6254327ea4e6451c781bec56215ac6cac`.
Pinned magnitudes stay `q3300` = 3300 and `q10000` = 10000.
`4207.00` lands in `outside_pinned_bins`. That label is not a scorecard
write. Q6-`000` is not retuned.

## Hard nulls

`results`, `abs_err_contracts`, `signed_bias`, `brier`, `pnl`, `mz`, and
`roi` stay null. The same three estimate fields stay null on each source
sample. Estimate-error writes raise `CalibrationNotRun`. Profit labels raise
`ProfitLabelRefused`. Live orders are refused.

Feebook `22371178cb2663250b4762f328069571c48cb551` is cited as the sibling
pin and is not used to price this sample. No Logan keys.
