# Fixture pin

- `first_demo_queue_poll.json`: verdict `POLL_OK`, `queue_position_fp`
  `"4207.00"`, ticker `KXNFLGAME-26OCT01PITCLE-PIT`, clean cancel, fill absent,
  L2 top price `0.01` with size narrative `~4208`. This is the sample_id 0
  cross-check.
- Desk series `lab/governance/astra/packets/r3_p2_queue_position/results/demo_queue_sample_series.json`
  was absent here. Schema required when it appears: `{meta, samples[]}`.
  No sanitized series copy is stored until those bytes are read.

No API keys, tokens, or account secrets. Calibration metrics stay null.
