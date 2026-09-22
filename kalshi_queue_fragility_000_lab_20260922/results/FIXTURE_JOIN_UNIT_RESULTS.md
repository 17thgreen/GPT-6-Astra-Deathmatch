# Queue-fragility fixture-join unit results

September 22, 2026. This file records a code check of the Q6-`000` join
harness. It is not a simulated trading run and not live validation.
`FROZEN_EXPERIMENT.json`, `results/EMPTY_RESULTS.json`, and
`packets/QF_FIXTURE_JOIN_000/results.json` still have
`fill_rate_delta_vs_q3300: null`, `adverse_queue_exposure: null`,
`participation_stress_gap: null`, `results: null`, and `pnl: null`.
No completed-net figure is reported.

Pick **B**. Freeze sha256
`d95adb9b7e8aba852134c96b8f0f7d35a76bbf68254b8808f82f99ec82bb6ca4`.

## Command

From `kalshi_queue_fragility_000_lab_20260922`, Python 3.12.3, standard
library:

```bash
python3 -m unittest -v tests.test_fixture_join
```

Ran 15 tests in 0.017s. Result: OK. Failures: 0. Errors: 0.

The checks that passed are the predeclared ones: the harness imports
`queue_fragility.py` in this lab and pins
`kalshi_r2p1_hygiene_000_lab_20260922/fixture_join.py`; the removed
`kalshi_r2p1_fixture_join_000_lab_*` directory is absent; the freeze packet
hash matches `d95adb9b…`; the five scorecard fields stay null in the lab
freeze, the empty results, the acceptance block, and the packet copies; the
production sha256 pins match `DELIVERY_MANIFEST.json`; the synthetic jsonl
pair carries the factorial fill and order keys; maker fills join on
`order_id`; taker order id `-1` is not sent through the maker instrument;
each maker row is one slice through QF0, QF1, and QF2; arm ahead comes from
`arm_queue_params` and not from the order's `initial_queue`; examiner formula
and maker rate match on produced fills; a gzip copy of the same bytes labels
the same rows; a non-`000` stem and a maker fill with no order are refused;
a one-contract quote at price 0.01 raises `MakerCreditRefused`;
`write_scorecard` raises. An in-memory `pre_settlement_outputs` preview on
the wide slice was computed inside the test and was not written to disk.

The frozen queue-fragility suite was rerun from this directory: 12 tests in
0.011s, OK. The hygiene suite was 20 tests in 0.007s, OK. The pick A join
suite was 14 tests in 0.017s, OK. Feebook was 37 tests in 0.004s, OK. Rails
was 44 tests in 0.004s, OK. Those reruns check unchanged modules. They are
not fixture-join profit results.

## Limitations

- The production ledgers
  `nfl_factorial_lab_20260921/results/q3300_d0.25_000_fills.jsonl.gz` and
  `q3300_d0.25_000_orders.jsonl.gz` are gitignored and were absent in this
  checkout. The unit run used
  `fixtures/synthetic_q3300_d0.25_000_{fills,orders}.jsonl`. That stand-in is
  not the indexed gzip and not a replay. `fixtures/PIN.md` records the
  production path and sha256. The same hashes are pinned by the hygiene-lab
  join module.
- Each maker row is measured alone: one quote and one print through QF0,
  QF1, and QF2. Rows are not chained into one book. This is not a 31-game
  walk.
- The order field `initial_queue` is parsed and is not the arm's
  `queue_ahead_contracts`. Recorded `fee`, `cash_after`, `inventory_after`,
  `paired`, and `queue_remaining` are required schema fields and are not
  summed.
- The harsh twin `q10000_d0.25_000_*` was not opened. It is a queue label,
  not a second fee rate. The fee channel is the R1-P1 examiner on every arm.
  There is no maker-off arm and no unrounded arm.
- `fill_rate_delta_vs_q3300`, `adverse_queue_exposure`, and
  `participation_stress_gap` stay null in the freeze. So do `results` and
  `pnl`.
- No live order client was added. `queue_fragility.py` was not edited. The
  feebook lab, the rails lab, the hygiene lab, the capital-structure lab, and
  the Q1–Q7 trees were not modified. Q6-`000` was not retuned. Capital A2 and
  A3 stay closed.

No profit is reported.
