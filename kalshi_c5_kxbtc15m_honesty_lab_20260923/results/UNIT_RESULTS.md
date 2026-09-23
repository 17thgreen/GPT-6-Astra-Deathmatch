# C5 KXBTC15M honesty harness unit results

September 23, 2026. This file records a code check of the frozen cadence
harness. It is a unit verification. It is not a simulated trading run and
not live validation. `FROZEN_EXPERIMENT.json` still has `results: null` and
`pnl: null`. `results/EMPTY_RESULTS.json` still has `freshness_gap_sec`,
`queue_bin_mismatch_rate`, `fee_delta_vs_inherited_model`, and
`turnover_stress_flag` null. Those fields stay null on purpose. This page
is not profit, and it is not folded back into the freeze hashes. No tape
walk was run. No P&L figure is reported. This is not an Examiner pass and
not a live-order certification. It is not live crypto trading.

## Command

From `kalshi_c5_kxbtc15m_honesty_lab_20260923`, Python 3.12, standard
library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

Ran 8 tests in 0.033s at 2026-09-23T14:01:54Z. Result: OK. Failures: 0.
Errors: 0.

The checks that passed are the predeclared ones: fee pin
`22371178cb2663250b4762f328069571c48cb551` and rails pin
`6a28e0d6254327ea4e6451c781bec56215ac6cac` with those trees unchanged since
those commits; packet sha256
`23b908af6e9a7799c9bbdac04b27e683dfccd0c0c25d691df84ff715202d3cab`; parent
kernel sha256
`4d1b72a38603de181e71f80b3cc6515b170a2bffe11f8770dac1296373e50263`; panel
stub `2026-09-22.c5-kxbtc15m-v0` sha256
`60f613e8d775b66b9044ad31d2faf77bba84176f214a7bce599aa7a65b6905f8` with
`admitted_at` null; preference for a temporary `panel_admitted.json` when
that file exists; C5H0 `per_window` and C5H1 `multi_window_stack` schema
with the four instrument fields null; a two-window synthetic stack that
does not change freeze bytes; refusal of live-crypto, bacchus, and
kxeth15m labels; refusal of a non-GET verb and of `execution_adapter`.

`fee_source` is feebook. `queue_source` is rails. Examiner fee-channel
names match `fee_delta_vs_inherited_model`, `freshness_gap_sec`, and
`queue_bin_mismatch_rate`. The hygiene module those joins already import
supplies `fee_delta`, `freshness_gap_seconds`, and `queue_bin_mismatch`.
The C1 queue-bin helper agrees on `q3300`, `q10000`, and an outside size.
None of those in-memory values are copied into the freeze files.

Cap-SR and the other paths in `DOES_NOT_MODIFY` match
`45863037a30af6caf9c00361e46fe8bd5444c426`. C3 is not implemented.

## Limitations

- The checkout stub has one window. C5H1 on that stub keeps
  `window_count` 1 and records `stub_n_expand_only_after_admit`. The
  two-window stack is `fixtures/synthetic_multi_window.json` with source
  `synthetic_schema_standin`. It is not a Kalshi GET and not an admitted
  cohort.
- `panel_admitted.json` is absent. `admitted_at` on the stub is null.
  Clock admit is still closed, so Examiner scoring stays closed.
- `turnover_stress_flag` is null because panel volume is null. Passing a
  volume into `turnover_stress_flag` is refused. This run does not compare
  turnover with a sports T-window.
- In-memory `fee_delta` and `freshness_gap_seconds` values are helper
  checks. They are not the freeze fields of the same names.
- Loading the Examiner orchestrator also loads the queue-fragility module,
  because that orchestrator imports it. This lab does not call a QF arm,
  does not change QF parameters, and does not edit that tree. The harness
  source has no `import queue_fragility` statement.
- No public GET was issued. No Logan key was read. No order route exists
  in this lab.
- `lab/governance/astra/packets/` is absent. The packet bytes used here are
  the copies under the lab and under `packets/C5_KXBTC15M_HONESTY_HARNESS/`.
