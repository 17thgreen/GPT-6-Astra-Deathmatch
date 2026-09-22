# R2-P1 hygiene unit results

September 22, 2026. This file records a code check of the frozen hygiene
helpers. It is not a simulated trading run and not live validation.
`FROZEN_EXPERIMENT.json` still has `results: null`, `pnl: null`,
`fee_delta_vs_inherited_model: null`, `freshness_gap_sec: null`, and
`queue_bin_mismatch_rate: null`. Those fields stay null on purpose: this page
is not profit, and it is not a fixture join. No Q6-`000` tape walk was run.
No completed-net figure is reported.

## Command

From `kalshi_r2p1_hygiene_000_lab_20260922`, Python 3.12.3, standard library:

```bash
python3 -m unittest -v tests.test_hygiene
```

Ran 20 tests in 0.007s. Result: OK. Failures: 0. Errors: 0.

The checks that passed are the predeclared ones: examiner `order_fee` round-up
differs from the inherited fixed-point balance fee on the same feebook rate;
partials keep `round_up=False` and still differ; inherited partials on one
accumulator sum to one whole-order charge; a coefficient other than the
feebook rate is refused; shadow fee literals are absent from `hygiene.py`;
maker credit that floors to zero is refused; a keepalive is not content-fresh
and does not move the freshness anchor; queue bins match only
`rails.scenario_queue('q3300')` and `rails.scenario_queue('q10000')`; an
unjoined pre-settlement report is null; a synthetic joined report does not
rewrite the freeze file; `historical_completed_net` raises; `completed_profit`
still requires the examiner fee channel.

The frozen feebook suite was rerun from its own directory: 37 tests, OK.
The frozen rails suite was rerun from its own directory: 44 tests, OK.
Those reruns check unchanged modules. They are not R2-P1 results.

## Limitations

- Examiner rates are whatever `feebook.load_series_table()` returns. This lab
  does not copy fee coefficients from `SHADOW_CANDIDATE_FREEZE.json`. The
  inherited charge uses the same resolved feebook rate so the delta is
  rounding only. A different coefficient is refused.
- The inherited model is a local reimplementation of the Q6 fixed-point
  balance charge. This lab does not import the factorial replay and does not
  walk the 31-game tape. A one-contract fixture difference is not a rescore
  of historical completed net.
- `fee_delta_vs_inherited_model`, `freshness_gap_sec`, and
  `queue_bin_mismatch_rate` stay null in the freeze and in
  `EMPTY_RESULTS.json`. A synthetic `joined=True` call can sum row deltas,
  take the max freshness gap, and divide mismatches by row count. That return
  still has `results` and `pnl` null, and this run did not write it to disk.
- Queue labels `q3300` and `q10000` are instrument settings from
  `rails.scenario_queue`. They are not a queue-fragility knob. Capital arms
  were not reopened. The `000` signal was not retuned.
- The canonical freeze is `R2-P1_FEEBOOK_RAILS_HYGIENE_000_FREEZE_2026-09-22.md`,
  sha256 prefix `ddcd4427`. Those bytes were not in this checkout. This lab
  does not substitute a file under that name. `fee_sensitivity_000_r1p1` is
  superseded by R2-P1. No second lab directory exists. FS0, FS1, and FS2 are
  not scorecard columns. Queue-fragility is a separate sibling lab, not a knob
  of this one.

## Sibling pin amendment

After `kalshi_queue_fragility_000_lab_20260922` landed, the pin-lock allows
that directory name and no other `*queue_fragility*` or `*queue-fragility*`
path. A second fee-sensitivity lab and a second R2-P1 directory stay
forbidden. `queue_fragility_twin` stays false: this lab is not that twin.
Pre-settlement outputs and pnl stay null.
- No live order client was added. No Q1–Q7 directory, and neither the feebook
  lab, the rails lab, nor the capital-structure lab, was modified.

No profit is reported.
