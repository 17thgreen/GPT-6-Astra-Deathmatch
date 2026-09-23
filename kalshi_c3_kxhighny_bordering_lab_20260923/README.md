# C3 KXHIGHNY bordering-strike harness

Status: hypothesis committed, then source frozen. The unit page is
`results/UNIT_RESULTS.md` (8 tests, OK, 2026-09-23T14:13:58Z). That page is
not profit and not an Examiner pass. `EXPERIMENT_SPEC.md` is the hypothesis.
`FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.
`results/EMPTY_RESULTS.json` keeps `adjacent_spread_gap`,
`bordering_depth_imbalance`, `fee_delta_vs_inherited_model`,
`freshness_gap_sec`, and `multi_city_inventory_join` null.

This lab is measurement-only. The series is `KXHIGHNY`, with `KXHIGHCHI`
as a same-calendar presence proof. The only knob is strike band: C3B0
`near_extreme` and C3B1 `mid_ladder`. Ladder objects are a structure
hypothesis. They are not GitHub weather-spread EV. The city join is not
arbitrage PnL. C5 stays as merged and is not edited.

`lab/governance/astra/packets/` is not in this checkout. Freeze copies:

- `C3_KXHIGHNY_BORDERING_STRIKE_HARNESS_FREEZE_2026-09-23.md` (sha256 `27530d6427794a5559e40c7f56d6cd938d8c57cc8f51406fc26a5b0e36a5fdff`)
- `C3_KXHIGHNY_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md` (sha256 `0e79a0194e2371efae8d8cac0f4f2ec9ce4cf53f60dd870bae1a1ed7acff3604`)
- `C3_KXHIGHNY_BORDERING_STRIKE_HARNESS/`
- `packets/C3_KXHIGHNY_BORDERING_STRIKE_HARNESS_FREEZE_2026-09-23.md`
- `packets/C3_KXHIGHNY_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md`
- `packets/C3_KXHIGHNY_BORDERING_STRIKE_HARNESS/`

Panel stub: `lab/astra-capture/c3-kxhighny/panel_stub.json`,
`panel_version` `2026-09-22.c3-kxhighny-v0`, `admitted_at` null.

Fee pin `22371178cb2663250b4762f328069571c48cb551`.
Rails pin `6a28e0d6254327ea4e6451c781bec56215ac6cac`.

From this directory, Python 3.12 standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

No Logan keys. No live orders. A passing unit run is not an Examiner score.
