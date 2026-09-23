# Examiner fee and queue honesty unit results

September 23, 2026. This file records a code check of the Q6-`000` Examiner
orchestrator. It is not a simulated trading run and not live validation.
`FROZEN_EXPERIMENT.json`, `results/EMPTY_RESULTS.json`, and
`packets/EXAMINER_FEE_QUEUE_HONESTY_000/FROZEN_EXPERIMENT.json` still have
`fee_delta_vs_inherited_model: null`, `freshness_gap_sec: null`,
`queue_bin_mismatch_rate: null`, `fill_rate_delta_vs_q3300: null`,
`adverse_queue_exposure: null`, `participation_stress_gap: null`,
`results: null`, and `pnl: null`.
No completed-net figure is reported. No target edge ratio is stated.

One packet. Freeze sha256
`4799642e54cf233a925697e00c5a9e29f5cb39070962a2e011f0fbe090c169f2`.

## Command

From `kalshi_examiner_fee_queue_honesty_000_lab_20260922`, Python 3.12.3,
standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

Ran 11 tests in 0.017s. Result: OK. Failures: 0. Errors: 0.

The checks that passed are the predeclared ones: the orchestrator imports
`kalshi_r2p1_hygiene_000_lab_20260922/fixture_join.py` and
`kalshi_queue_fragility_000_lab_20260922/fixture_join.py`; feebook, rails,
`hygiene.py`, `queue_fragility.py`, and both join modules match their pin
commits; the freeze packet hash matches `4799642e…`; the six scorecard fields
stay null in the lab freeze, the empty results, and the packet freeze; the
fee trio and the queue trio are both present, both typed, and both refused
by the same `write_scorecard` exception; both joins read one fills path and
one orders path; maker rows from the queue join carry QF0, QF1, and QF2 arm
slices in memory and those slices are not written to the scorecard; a
non-`000` stem is refused; live orders are refused; capital modes A2 and A3
are refused; the harsh twin stays unloaded.

The frozen hygiene suite was 20 tests in 0.009s, OK. The pick A join suite
was 14 tests in 0.017s, OK. The frozen queue-fragility suite was 12 tests in
0.011s, OK. The pick B join suite was 15 tests in 0.017s, OK. Feebook was 37
tests in 0.004s, OK. Rails was 44 tests in 0.004s, OK. Those reruns check
unchanged modules. They are not orchestrator profit results.

## Limitations

- The production ledgers
  `nfl_factorial_lab_20260921/results/q3300_d0.25_000_fills.jsonl.gz` and
  `q3300_d0.25_000_orders.jsonl.gz` are gitignored and were absent in this
  checkout. The freeze kernel still records the fills gzip as present on the
  freeze desk. The unit run used
  `kalshi_queue_fragility_000_lab_20260922/fixtures/synthetic_q3300_d0.25_000_{fills,orders}.jsonl`
  as one shared stand-in. That stand-in is not the indexed gzip and not a
  replay. `fixtures/PIN.md` records the production path and sha256. The
  hygiene lab's own synthetic pair was not the shared stream.
- In-memory labels from either join were not copied into freeze files.
- Rows are not a 31-game walk. The harsh twin `q10000_d0.25_000_*` was not
  opened.
- `fee_delta_vs_inherited_model`, `freshness_gap_sec`,
  `queue_bin_mismatch_rate`, `fill_rate_delta_vs_q3300`,
  `adverse_queue_exposure`, and `participation_stress_gap` stay null. So do
  `results` and `pnl`. No edge ratio is recorded.
- No live order client was added. `hygiene.py` and `queue_fragility.py` were
  not edited. The feebook lab, the rails lab, both fixture-join modules, the
  capital-structure lab, and the Q1–Q7 trees were not modified. Q6-`000` was
  not retuned. Capital A2 and A3 stay closed.

No profit is reported.
