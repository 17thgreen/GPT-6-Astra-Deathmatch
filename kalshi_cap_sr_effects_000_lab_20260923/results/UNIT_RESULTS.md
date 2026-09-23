# Cap-SR-FX effects path unit results

September 23, 2026. This file records a code check of the frozen effects-path
harness. It is not a simulated trading run and not live validation.
`FROZEN_EXPERIMENT.json` still has `results: null` and `pnl: null`.
`results/EMPTY_RESULTS.json` still has `borrow_count_delta_vs_fifo`,
`blend_utilization_gap`, `soft_breach_or_blend_rate`, and
`effects_path_fixture_id` null. Those fields stay null on purpose. This page
is not profit, and it is not folded back into the freeze hashes. No Q6-`000`
tape walk was run. No P&L figure is reported. This is not an Examiner pass
and not a live-order certification.

## Command

From `kalshi_cap_sr_effects_000_lab_20260923`, Python 3.12, standard library:

```bash
python3 -m unittest -v tests.test_effects_path
```

Ran 11 tests in 0.021s at 2026-09-23T14:49:04Z. Result: OK. Failures: 0.
Errors: 0.

The checks that passed are the predeclared ones: FX0 and FX1 join schema;
Cap-SR import of SR0, SR1, and SR2 from
`kalshi_soft_blended_reserves_000_lab_20260923` at `45863037`; feebook pin
`22371178cb2663250b4762f328069571c48cb551`; rails pin
`6a28e0d6254327ea4e6451c781bec56215ac6cac`; residual 9 unable to fund an
order after the FX1 seats; refusal of a sum of independent wallets versus
one shared 5000 USD account; and refusal to write the scorecard.

`fee_source` is feebook. `queue_source` is rails. The only knob is fixture
stress. A second `kalshi_soft_blended_*` tree was not created. Queue-fragility
was not imported. Q6-`000` was not retuned.

## Limitations

- FX0 in this checkout used
  `fixtures/synthetic_q3300_d0.25_000_fills.jsonl` because
  `nfl_factorial_lab_20260921/results/q3300_d0.25_000_fills.jsonl.gz` and the
  matching orders file were absent. The harness refuses a present gzip whose
  sha256 is not the factorial pin
  `9d56f5d3c599e092606be9f4a1ad41ae8baabff4921d3d722adf0b57ac944a3f`. The
  stand-in is not that gzip and not a replay. This run did not walk the
  production tape. Restoring the kit does not fill the scorecard.
- The FX0 stand-in seats two small quotes inside one event's unused reserve.
  SR0, SR1, and SR2 borrow logs stayed empty on that stand-in. That is the
  schema fixture, not an Examiner finding that production fills never borrow.
- FX1 `synthetic_borrow_stress` is a unit fixture on two development event
  ids already in the 31-event cohort. The second maker quote locks 200 USD
  through the imported `fund_quote` path. SR0 and SR1 appended cross-event
  borrow rows. SR2 appended a blend-pool draw and did not append a donor
  borrow. Those booleans are instrument schema. They were not reduced to
  `borrow_count_delta_vs_fifo`, `blend_utilization_gap`, or
  `soft_breach_or_blend_rate`. `effects_path_fixture_id` stayed null.
- Ledger `cash_after`, ledger `fee`, and `initial_queue` were not read as
  cash or as a queue knob. Quote locks use the imported feebook and rails
  path. Soft-policy math was not copied into this lab.
- `C_total` stays 5000 USD on each imported account. The three policies are
  not three wallets. `draw_residual` still raises. Identity stayed
  `available + committed + non_trading_residual_bucket = 5000`.
- S1 `PANEL_SCHEMA_STUB_EMPTY_EVENTS` was not implemented. No `admit.py` was
  added. No live order client was added. The Cap-SR lab, the capital lab,
  the feebook lab, the rails lab, the Q labs, C3, C5, and R3-P3 were not
  modified.

No profit is reported.
