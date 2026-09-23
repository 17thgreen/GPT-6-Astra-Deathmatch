# Mechanic demo queue sample series

The series document is `{meta, samples[]}`, not NDJSON. The desk path is:

`lab/governance/astra/packets/r3_p2_queue_position/results/demo_queue_sample_series.json`

Checked on this checkout: that file is present. sha256
`74ef9a9bb54054691e26b7b752568c8e833f51d21292034b1f40b9f3ca4ba8b4`.
`samples_n` is 38. `samples[]` was not invented.

`fixtures/demo_queue_sample_series.json` is the same byte string. The desk
file has no secret keys, so the lab does not re-serialize it.

The desk file has no `queue_positions` array. Each sample
`queue_endpoint_used` records
`GET /trade-api/v2/portfolio/orders/queue_positions?market_tickers=<ticker>`.
The loader does not build a batch from those URLs. Eighteen
`queue_position_fp` values are null and stay null. `0.00` is a recorded
position, not a missing one. When a document does include `queue_positions`,
`queue_position_fp` must match on `order_id`.

`sample_id` 0 cross-checks the first poll: `4207.00` on
`KXNFLGAME-26OCT01PITCLE-PIT`, cancel confirmed, fill absent.
`meta.n_success_including_prior` is 17. `meta.n_success_new_total` is 16.

`abs_err_contracts`, `signed_bias`, and `brier` stay null. `leftover_resting`
is `no`. `final_resting_ids` is empty. Twenty-eight samples have
`final_status` `resting`. Those rows are not relabeled into cancels and are
not scored. Host `demo-api.kalshi.co` only. Series rows use
`https://demo-api.kalshi.co`.
