# S5 KXMVECROSSCATEGORY fill-vs-legs unit results

September 23, 2026. This file records a code check of the frozen leg-mid
harness. It is a unit verification. It is not a simulated trading run and
not live validation. `FROZEN_EXPERIMENT.json` still has `results: null` and
`pnl: null`. `results/EMPTY_RESULTS.json` still has `fill_vs_legs_mid_gap`,
`combo_fee_delta_vs_feebook`, `legs_join_rate`, and `freshness_gap_sec`
null. Those fields stay null on purpose. This page is not profit, and it
is not folded back into the freeze hashes. No tape walk was run. No P&L
figure is reported. This is not an Examiner pass and not a live-order
certification. RFQ stays out of scope.

## Command

From `kalshi_s5_mve_filllegs_lab_20260923`, Python 3.12, standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

Ran 8 tests in 0.046s at 2026-09-23T15:05:04Z. Result: OK. Failures: 0.
Errors: 0.

The checks that passed are the predeclared ones: fee pin
`22371178cb2663250b4762f328069571c48cb551` and rails pin
`6a28e0d6254327ea4e6451c781bec56215ac6cac` with those trees unchanged since
those commits; in-memory series override `quadratic_with_combo_maker_fees`
with multiplier 1 on the three bound series, resolving as `override`;
packet sha256
`8a118e6f1fdc8c22c6e559f395667aedffa5d270d067e39b6ae3ee24b2046d16`; parent
kernel sha256
`a28932ba13b4913b69c48b73dde8ba066cebd212670d0b1cbb5ea8e93734b8ba`; panel
stub `2026-09-22.s5-kxmvecrosscategory-v0` sha256
`4918b820d454c5f997ea100917859f7e9467d92933bed1bc8a55c81ab8ce5b8e` with
`admitted_at` null, 5 markets, 21 events, and `mve_selected_legs` on 5/5
(leg counts 3, 27, 4, 4, 4); preference for a temporary
`panel_admitted.json` when that file exists; S5L0 `tob_1m` and S5L1
`synthetic_leg_product` schema with the four instrument fields null; a
synthetic known product `0.10` from YES `0.50`, NO flip of `0.20`, and YES
`0.25` that does not change freeze bytes; refusal of RFQ, R1-P4 strategy,
Logan keys, `admit.py`, and invented fills.

`fee_source` is feebook. `rails_source` is rails. A plain feebook quote on
`KXMVECROSSCATEGORY` without the override stays `default_unknown_series`
and is refused as a combo channel. The hygiene module supplies
`freshness_gap_seconds` and `maker_credit_floor_zero_refuse` for in-memory
checks. None of those values are copied into the freeze files.

Cap-SR, Cap-SR-FX, C3, C5, R3-P3, and the Q labs in `DOES_NOT_MODIFY` match
`79347f0ed8562f7df8d539e79a1cb15985d8abfe`. S4 NCAAF and R2-P3 stay queued.

## Limitations

- The checkout stub has an empty trade probe (`trades_n` 0 on three
  tickers, HTTP 200). S5L0 on that stub keeps `leg_product` and
  `fill_price` null and records `empty_tape_no_tob_mids`. No fill was
  invented.
- S5L1 on the stub records `synthetic_product_fixture_only` and leaves
  `schema_product` null. The known product is
  `fixtures/synthetic_leg_product.json` with source
  `synthetic_schema_standin`. The synthetic print is not scored into
  `fill_vs_legs_mid_gap`. It is not a Kalshi GET and not an admitted
  cohort.
- `panel_admitted.json` is absent. `admitted_at` on the stub is null.
  Clock admit is still closed, so Examiner scoring stays closed.
- The stub document stores `legs_join_rate` as the string `5/5`. The
  harness scorecard field of the same name stays null. Structural counts
  on the report are `markets_n` 5 and `legs_complete_n` 5.
- In-memory `freshness_gap_seconds` and maker-credit checks are helper
  checks. They are not the freeze fields `freshness_gap_sec` or
  `combo_fee_delta_vs_feebook`.
- A missing leg mid and a stale rails observation raise. Those refusals
  are schema gates. They are not a scored gap.
- No public GET was issued. No Logan key was read. No order route exists
  in this lab. `admit.py` was not run.
- `lab/governance/astra/packets/` is absent. The packet bytes used here are
  the copies under the lab and under `packets/S5_KXMVECROSSCATEGORY_FILLLEGS_HARNESS/`.
