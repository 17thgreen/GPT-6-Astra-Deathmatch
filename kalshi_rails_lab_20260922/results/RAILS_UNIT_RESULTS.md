# R1-P5 rails unit results

September 22, 2026. This file records a code check of the frozen helpers. It is
not a simulated trading run and not live validation. `FROZEN_EXPERIMENT.json`
still has `results: null` and `pnl: null`. Those fields stay null on purpose:
this page is not profit, and it is not folded back into the freeze hashes.

## Command

From `kalshi_rails_lab_20260922`, Python 3.12.3, standard library:

```bash
python3 -m unittest -v tests.test_rails
```

Ran 44 tests in 0.004s. Result: OK. Failures: 0. Errors: 0.

The checks that passed are the predeclared ones: taker-side polarity, queue
consumption before the 0.5 participation share, same-price retention of
consumed queue, new-price and fully-filled orders returning to the back,
partial maker fees on the `round_up=False` path, the maker-credit floor
refusals, the content-fresh predicate, and the MICRO verdict order.

The frozen feebook suite was rerun from its own directory: 37 tests, OK. That
rerun is a regression check of an unchanged module. It is not an R1-P5 result.

## Limitations

- `execution.py` at blob `8d9827657001aac6a3dfc2ffdc84f0bf121f0310` was read
  and not vendored. This lab uses `Decimal` and the feebook fee functions.
  The sibling simulator uses binary floats and applies the per-contract cap
  on the unrounded path as well. The feebook cap stays off unless
  `round_up` is true. Partial fills here follow that feebook rule.
- Queue labels `q3300` and `q10000` are instrument settings. This run did not
  replay the Q1–Q6 tapes, and it does not apply that engine's cent-contract
  fill floor, cancel delay, or cash ledger.
- A same-price replacement keeps the unfilled remainder. It does not adopt a
  new size. A fully filled order, including one replaced at the same price,
  is a new order at the back.
- The maker-credit floor is `floor_cent(price * contracts - ceiled maker fee)`.
  At one contract and `$0.01` the fee-blind cash is `$0.01` and the floored
  credit is `$0.00`, so the quote is refused. A series override with maker
  fees disabled can still admit, because the zero fee was evaluated.
- Book freshness is a predicate. No collector, socket, or clock loop is
  attached. A local receive time is not an input.
- MICRO scores on the unit rows are synthetic. Two kept prints are `THIN`
  because `n < 500`. No tape was walked. One-lot ROI and size-weighted ROI
  are both reported; the one-lot figure assumes a unique counterparty.
  Picker fields on `grok_config_MICRO_V1.json` are not applied. The only
  evidence stage accepted is `HISTORICAL_OUT_OF_SAMPLE`. Control stays
  `CONTROL`.
- No Q1–Q7 directory was modified. `kalshi_feebook_lab_20260922` source was
  not modified. No live order type was added.

No profit is reported.
