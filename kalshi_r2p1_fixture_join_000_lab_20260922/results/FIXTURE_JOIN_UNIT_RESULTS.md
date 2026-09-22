# R2-P1 fixture-join unit results

September 22, 2026. This file records a code check of the Q6-`000` join
harness. It is not a simulated trading run and not live validation.
`FROZEN_EXPERIMENT.json`, `results/EMPTY_RESULTS.json`, and
`packets/R2-P1_FIXTURE_JOIN_000/results.json` still have
`fee_delta_vs_inherited_model: null`, `freshness_gap_sec: null`,
`queue_bin_mismatch_rate: null`, `results: null`, and `pnl: null`.
No completed-net figure is reported.

Pick **A**. Freeze sha256
`e9bac91ca908b2ba704d966f0cf48cb181070ac11de1d117b93512bd2719ae1c`.

## Command

From `kalshi_r2p1_fixture_join_000_lab_20260922`, Python 3.12.3, standard
library:

```bash
python3 -m unittest -v tests.test_fixture_join
```

Ran 14 tests in 0.016s. Result: OK. Failures: 0. Errors: 0.

The checks that passed are the predeclared ones: the harness imports the
feebook, rails, and hygiene modules at the pinned commits; the freeze packet
hash matches `e9bac91c…`; the five scorecard fields stay null in the lab
freeze, the empty results, and the packet copies; the production sha256 pins
match `DELIVERY_MANIFEST.json`; the synthetic jsonl pair carries the factorial
fill and order keys; maker fills join on `order_id`; taker order id `-1` stays
unattributed for queue; `initial_queue` is the queue bin input and
`queue_remaining` is not; maker-credit refusal, keepalive freshness, and
`fee_delta` match direct helper calls; a gzip copy of the same bytes labels
the same rows; a non-`000` stem and a maker fill with no order are refused;
`write_scorecard` raises. An in-memory `pre_settlement_outputs` preview on the
maker rows was computed inside the test and was not written to disk.

The frozen hygiene suite was rerun from its own directory: 20 tests, OK.
The frozen queue-fragility suite was rerun from its own directory: 12 tests,
OK. Those reruns check unchanged modules. They are not fixture-join results.

## Limitations

- The production ledgers
  `nfl_factorial_lab_20260921/results/q3300_d0.25_000_fills.jsonl.gz` and
  `q3300_d0.25_000_orders.jsonl.gz` are gitignored and were absent in this
  checkout. The unit run used
  `fixtures/synthetic_q3300_d0.25_000_{fills,orders}.jsonl`. That stand-in is
  not the indexed gzip and not a replay. `fixtures/PIN.md` records the
  production path and sha256.
- `book`, `transaction_time`, and `keepalive` are harness annotations on the
  stand-in. Factorial fill rows do not carry them. A production row without
  those keys leaves `content_fresh_flag` unlabeled.
- Queue attribution reads the joined order's `initial_queue` and compares it
  with `rails.scenario_queue` for the filename scenario. The harsh twin
  `q10000_d0.25_000_*` was not opened. It is a queue label, not a second fee
  rate.
- The fee coefficient is the rate resolved by `feebook.order_fee`. The
  recorded fill `fee`, `cash_after`, `inventory_after`, and `paired` are
  required schema fields and are not summed.
- `fee_delta_vs_inherited_model`, `freshness_gap_sec`, and
  `queue_bin_mismatch_rate` stay null in the freeze. So do `results` and
  `pnl`. Pick B, the queue-fragility fixture join, was not started.
- No live order client was added. The feebook lab, the rails lab, the hygiene
  lab, the queue-fragility lab, the capital-structure lab, and the Q1–Q7
  trees were not modified. Q6-`000` was not retuned. Capital A2 and A3 stay
  closed.

No profit is reported.
