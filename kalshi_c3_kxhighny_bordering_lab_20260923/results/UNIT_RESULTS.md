# C3 KXHIGHNY bordering-strike harness unit results

September 23, 2026. This file records a code check of the frozen strike-band
harness. It is a unit verification. It is not a simulated trading run and
not live validation. `FROZEN_EXPERIMENT.json` still has `results: null` and
`pnl: null`. `results/EMPTY_RESULTS.json` still has `adjacent_spread_gap`,
`bordering_depth_imbalance`, `fee_delta_vs_inherited_model`,
`freshness_gap_sec`, and `multi_city_inventory_join` null. Those fields stay
null on purpose. This page is not profit, and it is not folded back into the
freeze hashes. No tape walk was run. No P&L figure is reported. This is not
an Examiner pass and not a live-order certification. Ladder objects stay a
structure hypothesis.

## Command

From `kalshi_c3_kxhighny_bordering_lab_20260923`, Python 3.12.3, standard
library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

Ran 8 tests in 0.038s at 2026-09-23T14:13:58Z. Result: OK. Failures: 0.
Errors: 0.

The checks that passed are the predeclared ones: fee pin
`22371178cb2663250b4762f328069571c48cb551` and rails pin
`6a28e0d6254327ea4e6451c781bec56215ac6cac` with those trees unchanged since
those commits; packet sha256
`27530d6427794a5559e40c7f56d6cd938d8c57cc8f51406fc26a5b0e36a5fdff`; parent
kernel sha256
`0e79a0194e2371efae8d8cac0f4f2ec9ce4cf53f60dd870bae1a1ed7acff3604`; panel
stub `2026-09-22.c3-kxhighny-v0` sha256
`2a5da7fe85ca1adc6b7c4dcf9e09ed5c6bb62be6b5c9b42731e36e31d1e8dfea` with
`admitted_at` null; preference for a temporary `panel_admitted.json` when
that file exists; C3B0 `near_extreme` and C3B1 `mid_ladder` schema with the
five instrument fields null; a synthetic ladder that does not change freeze
bytes; refusal of GitHub weather-spread EV, live-order, and invented-arb
labels; refusal of a non-GET verb and of `execution_adapter`.

`fee_source` is feebook. `rails_source` is rails. The hygiene module
supplies `fee_delta` and `freshness_gap_seconds`. None of those in-memory
values are copied into the freeze files.

C5 and the other paths in `DOES_NOT_MODIFY` match
`ee69245a5dba058ee1198c88bb4685893508f273`. C5 `results` and `pnl` remain
null.

## Limitations

- On the stub, C3B0 has three neighboring pairs. C3B1 has zero pairs: the
  only mid-ladder price is `KXHIGHNY-26SEP23-B67.5` at `0.5200`, alone in
  its event. The report records `stub_mid_ladder_pair_absent_expand_only_after_admit`.
  The mid-ladder pair in `fixtures/synthetic_ladder.json` has source
  `synthetic_schema_standin`. It is not a Kalshi GET and not an admitted
  cohort.
- The band cut is price `<= 0.10` or `>= 0.90` for `near_extreme`, and
  strictly between those cuts for `mid_ladder`. Scout role
  `mid_ladder_anchor` on `KXHIGHNY-26SEP22-B67.5` does not select C3B1;
  that row's price `0.9900` is `near_extreme`. The cut is a schema rule.
  It was not fit to a PnL.
- Neighboring means next in `floor_strike` order inside one event after the
  band filter. Strikes missing from the six-ticker seed are not invented.
- `panel_admitted.json` is absent. `admitted_at` on the stub is null.
  Clock admit is still closed, so Examiner scoring stays closed.
- NY and CHI are both present on occurrence date `2026-09-23`. NY alone is
  present on `2026-09-24`. `multi_city_inventory_join` stays null.
  `arb_pnl` on that presence table stays null. This run does not score a
  cross-city arb.
- In-memory `fee_delta` and `freshness_gap_seconds` values are helper
  checks. They are not the freeze fields of the same names.
- The hygiene module is loaded directly. The Examiner orchestrator and
  `queue_fragility` are not imported. No QF arm is called.
- No public GET was issued. No Logan key was read. No order route exists
  in this lab.
- `lab/governance/astra/packets/` is absent. The packet bytes used here are
  the copies under the lab and under `packets/C3_KXHIGHNY_BORDERING_STRIKE_HARNESS/`.
- R3-P3 remains a cite on the stub. This run does not merge kernels.
