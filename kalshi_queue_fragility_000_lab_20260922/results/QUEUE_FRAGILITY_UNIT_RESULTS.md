# Queue-fragility unit results

September 22, 2026. This file records a code check of the frozen queue arms.
It is not a simulated trading run and not live validation.
`FROZEN_EXPERIMENT.json` still has `results: null`, `pnl: null`,
`fill_rate_delta_vs_q3300: null`, `adverse_queue_exposure: null`, and
`participation_stress_gap: null`. Those fields stay null on purpose: this page
is not profit, and it is not a fixture join. No Q6-`000` tape walk was run.
No completed-net figure is reported.

## Command

From `kalshi_queue_fragility_000_lab_20260922`, Python 3.12.3, standard library:

```bash
python3 -m unittest -v tests.test_queue_fragility
```

Ran 12 tests in 0.010s. Result: OK. Failures: 0. Errors: 0.

The checks that passed are the predeclared ones: `QF0`, `QF1`, and `QF2`
differ only in rails queue parameters; participation is
`rails.FILL_PARTICIPATION_DEFAULT` on every arm; `QF0` uses
`rails.scenario_queue('q3300')` and `measured`; `QF1` uses
`rails.scenario_queue('q10000')` and `measured`; `QF2` uses `front` with
ahead 0. The feebook binding is the examiner formula
`astra.r1p1.feebook.claude_order_level_ceil.v1` and is identical across arms.
Maker-credit refusal at one cent is the same on every arm. A one-print slice
follows the rails fill rule, and the fills that occur carry the examiner
formula and the same maker rate. Taker polarity, same-price queue keep, and
a new price at the back of that arm's queue match the rails pins. Shadow fee
literals are absent from `queue_fragility.py`. A2 and A3 are refused. An
unjoined pre-settlement report is null. A synthetic joined report does not
rewrite the freeze file. `historical_completed_net` raises. Live orders are
refused. The feebook and rails directories still match commits
`22371178cb2663250b4762f328069571c48cb551` and
`6a28e0d6254327ea4e6451c781bec56215ac6cac`.

The frozen feebook suite was rerun from its own directory: 37 tests, OK.
The frozen rails suite was rerun from its own directory: 44 tests, OK.
Those reruns check unchanged modules. They are not queue-fragility results.
The R2-P1 hygiene suite was rerun after the sibling-pin amendment: 20 tests, OK.

## Limitations

- Examiner rates are whatever `feebook.load_series_table()` returns. This lab
  does not copy fee coefficients from `SHADOW_CANDIDATE_FREEZE.json`.
- The one-print slice is a synthetic instrument check of the rails rule
  `consumed = min(Q, V)`, `fill = min(R, post * p)`. It is not a walk of the
  31-game tape and it is not cash profit. `results` and `pnl` stay null in
  the freeze and in `EMPTY_RESULTS.json`.
- `fill_rate_delta_vs_q3300`, `adverse_queue_exposure`, and
  `participation_stress_gap` stay null in the freeze. A synthetic
  `joined=True` call can compute them in memory. That return still has
  `results` and `pnl` null, and this run did not write it to disk.
- Capital is the shared A1-equivalent pool of 5000 USD. A2 and A3 were not
  reopened. The `000` signal was not retuned. Maker-off and the unrounded
  comparator are not arms.
- The R2-P1 pin-lock allows `kalshi_queue_fragility_000_lab_20260922` and no
  other `*queue_fragility*` or `*queue-fragility*` path. A second
  fee-sensitivity lab and a second R2-P1 directory stay forbidden.
  `queue_fragility_twin` stays false on the R2-P1 lab. The hygiene behavior
  of that lab was not retuned.
- No live order client was added. No Q1–Q7 directory, and neither the feebook
  lab, the rails lab, the R2-P1 lab, nor the capital-structure lab, was
  modified.

No profit is reported.
