# L2 shape unit results

September 23, 2026. This file records a code check of the frozen SF1 and SF2
helpers. It is not a simulated trading run, not a Kalshi stylized-fact panel,
and not live validation. `FROZEN_EXPERIMENT.json` still has `results: null`
and `pnl: null`. `results/EMPTY_RESULTS.json` still has `sf1: null` and
`sf2: null`. Those fields stay null on purpose: this page is not profit, and
the synthetic fixture medians are not folded back into the freeze. No live
orderbook poll was run. No P&L figure is reported.

## Command

From `kalshi_r3_p4_l2_shape_lab_20260922`, Python 3.12.3, standard library:

```bash
python3 -m unittest -v tests.test_shape
```

Ran 26 tests in 0.010s. Result: OK. Failures: 0. Errors: 0.

The checks that passed are the predeclared ones: half-spread bps equals
`(spread / 2) / mid * 10000` using `feebook.reciprocal_book`; a negative
spread stays negative; a missing side and a zero mid are refused; absolute
mid deciles follow the Dubach Table 1 edges, and an empty bin is null; flat
top-10 shares sum to 1 and have KL 0 against uniform `1/10`; a one-level book
has KL `ln(10)`; L1 share of `1/2` is not top-heavy; a three-level book keeps
ranks 4–10 at depth 0; same-price rows are one level; the rails content-fresh
gate refuses an unchanged snapshot and a keepalive; the synthetic fixture
panel keeps ten fresh snapshots and nine markets, with the stale duplicate
and the keepalive excluded; sports and non-sports slices use those category
tags; `completed_profit` and trade-sign inference raise; running the panel
does not rewrite the empty results file or the freeze. Feebook and rails file
hashes match `SOURCE_PINS.json`.

The frozen feebook suite was rerun from its own directory: 37 tests, OK.
The frozen rails suite was rerun from its own directory: 44 tests, OK.
Those reruns check unchanged modules. They are not shape results.

## Limitations

- Mids and spreads are whatever `feebook.reciprocal_book` returns at the pin
  `22371178cb2663250b4762f328069571c48cb551`. This lab does not copy that
  function and does not read fee coefficients.
- Inclusion is `rails.judge_freshness` at
  `6a28e0d6254327ea4e6451c781bec56215ac6cac`. A keepalive is not a book. An
  unchanged content token and transaction time is not a second observation.
- Depth at rank `k` sums the observed YES bid size and the observed NO bid
  size at that rank. Missing deeper ranks are zero. A side with no positive
  size is incomplete. No ask size is fabricated.
- Deciles are absolute probability bins of width `0.1`. They are not sample
  quantiles. The fixture medians check that arithmetic. They are not a
  statement about Kalshi markets.
- Dubach's Polymarket panel numbers are not recomputed. The paper table's
  central-decile figure of about 400 bps is not the pinned half-spread.
- No fee channel is computed. No Lee-Ready sign is computed. No live order
  client was added. Q6 `000` was not retuned. No Q1–Q7 directory, and neither
  the feebook lab nor the rails lab, was modified.

No profit is reported.
