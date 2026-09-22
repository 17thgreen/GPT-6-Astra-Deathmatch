# Capital structure unit results

September 22, 2026. This file records a code check of the frozen partition
helpers. It is not a simulated trading run and not live validation.
`FROZEN_EXPERIMENT.json` still has `results: null` and `pnl: null`. Those
fields stay null on purpose: this page is not profit, and it is not folded
back into the freeze hashes. No Q6-`000` tape walk was run. No P&L figure is
reported.

## Command

From `kalshi_capital_structure_lab_20260922`, Python 3.12.3, standard library:

```bash
python3 -m unittest -v tests.test_capital_structure
```

Ran 23 tests in 0.011s. Result: OK. Failures: 0. Errors: 0.

The checks that passed are the predeclared ones: equal `C_total` of 5000 USD
on A1, A2, and A3; A3 refusal of cross-event borrow; A2 unused-only borrows
logged in ascending `event_id` order for both donors and batched borrowers;
the A3 `non_trading_residual_bucket` of 9 USD unable to fund orders; refusal
of a sum-of-N independent wallets versus one shared 5000 USD; and quote locks
that take examiner fees from `kalshi_feebook_lab_20260922` and maker admission
plus queue magnitudes from `kalshi_rails_lab_20260922`.

The frozen feebook suite was rerun from its own directory: 37 tests, OK.
The frozen rails suite was rerun from its own directory: 44 tests, OK.
Those reruns check unchanged modules. They are not capital-structure results.

## Limitations

- Fee rates are whatever `feebook.load_series_table()` returns at import time.
  This lab does not copy `maker_coefficient` or `taker_coefficient` from
  `SHADOW_CANDIDATE_FREEZE.json`. A numerical match with the historical
  shadow coefficients is a property of the feebook pin, not a second source.
- Maker cash lock is the quote gross after `rails.admit_maker_quote`. Taker
  cash lock is gross plus `feebook.order_fee` with `round_up=True`. Neither
  lock is booked as profit. A refused maker credit moves no cash.
- A2's leftover 9 USD is `unreserved_pool`. It can fund an order only after
  the borrower's own unused reserve and other events' unused reserves are
  exhausted, and that draw is not a cross-event borrow row. A3's 9 USD is
  `non_trading_residual_bucket` and cannot fund an order. Within-reserve A2
  spends append no borrow row. An over-reserve spend does. The borrow log is
  not empty by construction.
- Queue labels `q3300_d0.25` and `q10000_d0.25` are instrument settings from
  `rails.scenario_queue`. The harsh twin is not a capital knob. This run did
  not replay the Q6 tape. The checkout has the development manifest and week
  membership, not the external candle kits.
- The freeze packet cites Q7 verification sha256
  `eb1586bf13b1631951a4f177293350cb89fc7948a50fbb7044f4f05313ebc06f` and
  `paircheck_effects.json` sha256
  `5d87ea610f22482c980868d8a31a228ca1931368d9eeab73add4256d2e117fdf`. Those
  blobs are not in this checkout. In-tree `verification.json` is
  `NOT_RUN_INPUTS_MISSING`. This lab does not rewrite it and does not vary
  pair-check. The strategy pointer is the on-tree Q6 label `000` shadow
  freeze, whose file hash matches the packet.
- `measurement_scorecard` calls `feebook.classify_scorecard`. Without the
  examiner fee channel, `completed_profit` is refused. A classifier label is
  not a tape result. Promotion from isolated wallet sums is refused.
- No live order client was added. No Q1–Q7 directory, and neither the feebook
  lab nor the rails lab, was modified.

No profit is reported.
