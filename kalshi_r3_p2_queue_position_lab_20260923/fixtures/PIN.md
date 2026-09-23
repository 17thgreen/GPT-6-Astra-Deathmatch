# Fixture pin

- `first_demo_queue_poll.json`: verdict `POLL_OK`, `queue_position_fp`
  `"4207.00"`, ticker `KXNFLGAME-26OCT01PITCLE-PIT`, clean cancel, fill absent,
  L2 top price `0.01` with size narrative `~4208`. This is the sample_id 0
  cross-check. `size_exact` stays null on this fixture.
- Desk series `lab/governance/astra/packets/r3_p2_queue_position/results/demo_queue_sample_series.json`
  sha256 `74ef9a9bb54054691e26b7b752568c8e833f51d21292034b1f40b9f3ca4ba8b4`,
  70373 bytes, schema `{meta, samples[]}`, `samples_n` 38,
  `leftover_resting` `no`.
- `demo_queue_sample_series.json` in this directory is those same bytes.
  No secret key was removed, and the JSON was not reformatted, so the
  fixture digest equals the desk digest.

No API keys, tokens, or account secrets. Calibration metrics stay null.
