# Cap-SR soft-blended reserves unit results

September 23, 2026. This file records a code check of the frozen soft-policy
helpers. It is not a simulated trading run and not live validation.
`FROZEN_EXPERIMENT.json` still has `results: null` and `pnl: null`.
`results/EMPTY_RESULTS.json` still has `borrow_count_delta_vs_fifo`,
`blend_utilization_gap`, and `soft_breach_or_blend_rate` null. Those fields
stay null on purpose. This page is not profit, and it is not folded back
into the freeze hashes. No Q6-`000` tape walk was run. No P&L figure is
reported. This is not an Examiner pass and not a live-order certification.

## Command

From `kalshi_soft_blended_reserves_000_lab_20260923`, Python 3.12, standard
library:

```bash
python3 -m unittest -v tests.test_soft_policy
```

Ran 32 tests in 0.021s at 2026-09-23T13:48:04Z. Result: OK. Failures: 0.
Errors: 0.

The checks that passed are the predeclared ones: equal `C_total` of 5000 USD
on SR0, SR1, and SR2; residual 9 unable to fund an order on every arm; SR0
borrow rows matching capital-structure A2 on schedules that do not draw A2's
unreserved slack; SR1 pro-rata takes against unused reserve; SR2 local-then-
blend-pool draws with other events' local reserves left in place; refusal of
a sum-of-N independent wallets versus one shared 5000 USD; and quote locks
that take examiner fees from `kalshi_feebook_lab_20260922` and maker
admission plus queue magnitudes from `kalshi_rails_lab_20260922`.

`fee_source` is feebook. `queue_source` is rails. A1 and A3 did not open.
Queue-fragility was not imported.

## Limitations

- SR0 reuses `CapitalAccount` for `A2_shared_soft_reserve` and then seats the
  9 USD residual as `non_trading_residual_bucket`. Borrow logs match A2 when
  the draw fits in the 4991 USD of soft reserve. A2 can still fund that 9 USD
  from `unreserved_pool`. SR0 refuses that draw. The match is the FIFO
  unused-borrow path, not a second copy of A2's tradable slack.
- SR1 weights donors by unused reserve. Takes are multiples of `10^-8` USD
  under Hamilton's method, with ascending `event_id` breaking remainder ties.
  A finer amount is refused. The log is not empty once a borrow is required.
- SR2 seats `floor(161 / 2) = 80` USD per event in one blend pool (2480 USD)
  and leaves 81 USD event-local. Draw order is local unused, then the blend
  pool, then refuse. Cross-event local reserve is not borrowed. Blend draws
  are logged. The log is not empty once the local seat is exceeded.
- Fee rates are whatever `feebook.load_series_table()` returns at import
  time. This lab does not copy shadow fee literals. Queue labels
  `q3300_d0.25` and `q10000_d0.25` come from `rails.scenario_queue`. Neither
  label is a soft-policy knob. This run did not replay the Q6 tape.
- `measurement_scorecard` calls `feebook.classify_scorecard`. Without the
  examiner fee channel, `completed_profit` is refused. A classifier label is
  not a tape result and is not written into the freeze. Promotion from
  isolated wallet sums is refused. The three scorecard fields stay null.
- No live order client was added. The capital lab, the feebook lab, the
  rails lab, the queue-fragility lab, and the Q labs were not modified.
  Q6-`000` was not retuned.

No profit is reported.
