# R3-P1 fee-cost unit results

September 23, 2026. This file records a code check of the frozen helpers. It is
not a simulated trading run and not live validation. `FROZEN_EXPERIMENT.json`
still has `results: null`, `pnl: null`, and `fee_model_minus_venue_delta: null`.
Those fields stay null on purpose: this page is not profit, and it is not
folded back into the freeze hashes.

## Command

From `kalshi_r3_p1_fee_cost_lab_20260922`, Python 3.12.3, standard library:

```bash
python3 -m unittest -v tests.test_fee_cost
```

Ran 18 tests in 0.009s. Result: OK. Failures: 0. Errors: 0.

The checks that passed are the predeclared ones: `fee_model` equals imported
`order_fee` on the examiner channel, `fee_model_minus_venue_delta` equals
`fee_model − fee_cost` in `Decimal` when the venue fee is present, a null
`fee_cost` leaves that delta null, taker and maker rows use different roles,
and a model-only completed net is refused when `fee_cost` was available.
`classify_scorecard` can still return `completed_profit` for the examiner
channel. This lab does not promote that label to a completed net. A venue
basis binds the accounting fee to `fee_cost` and returns null `pnl`.

## Limitations

- The fills are synthetic. They are not a portfolio read and not a live
  capture. No account endpoint was called.
- `kalshi_feebook_lab_20260922` is imported at
  `22371178cb2663250b4762f328069571c48cb551`. It is not copied. The taker and
  maker coefficients are not restated in this lab.
- The closed-form comparison uses the order-level cent ceiling
  (`round_up=True`). The feebook's unrounded partial path is out of scope.
- The Grok unrounded maker quote is not an accounting fee. Passing it as the
  counterpart quote fails inside `examiner_fee_channel`.
- The counterpart quote exists so the examiner channel has both roles. It is
  not a second venue fee.
- A null `fee_cost` may be used as a projection. It is not a completed net
  and it is not a zero delta.
- A reported zero is a present venue fee. Model-only completed net is refused
  in that case as well.
- Summing non-null synthetic deltas inside the harness is a unit check. That
  sum is not written to `FROZEN_EXPERIMENT.json` or `results/EMPTY_RESULTS.json`.
- Unresolved inventory still raises the feebook refusal. No profit is
  substituted for it.
- No Q1–Q7 directory was modified. Q6 label `000` was not retuned. Historical
  replays were not rerun.

No profit is reported.
