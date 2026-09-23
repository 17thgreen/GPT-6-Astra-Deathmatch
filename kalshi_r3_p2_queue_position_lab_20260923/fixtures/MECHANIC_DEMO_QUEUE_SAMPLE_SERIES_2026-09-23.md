# Mechanic demo queue sample series

The series document is `{meta, samples[]}`, not NDJSON. The desk path is:

`lab/governance/astra/packets/r3_p2_queue_position/results/demo_queue_sample_series.json`

Checked on this checkout: that file is absent. `samples[]` was not invented.
`fixtures/demo_queue_sample_series.json` is not a stand-in row list.

When the desk file is present, the lab copies a sanitized body into
`fixtures/demo_queue_sample_series.json` and pins its sha256. Each sample
`queue_position_fp` must match `queue_positions` on `order_id`. `sample_id`
0 cross-checks the first poll: `4207.00` on `KXNFLGAME-26OCT01PITCLE-PIT`,
cancel confirmed, fill absent.

`abs_err_contracts`, `signed_bias`, and `brier` stay null. `leftover_resting`
must be false or `no`. Host `demo-api.kalshi.co` only.
