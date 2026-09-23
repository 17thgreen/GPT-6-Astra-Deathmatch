# C4 KXCPI fee+queue honesty harness

Status: hypothesis committed, then source frozen. The unit page is
`results/UNIT_RESULTS.md` after the code check. `EXPERIMENT_SPEC.md` is the
hypothesis. `FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.
`results/EMPTY_RESULTS.json` keeps `maker_vs_taker_roi_delta`,
`sparse_vs_fresh_gap`, `missing_sot_n`, `settled_join_n`, and `n_books`
null.

This lab is measurement-only. Feature family CPI-FQ. The series is
`KXCPI`. The only knob is `analysis_slice`: C4A0 `maker_vs_taker_native`
and C4A1 `sparse_24h_vs_fresh_bin`. Lee-Ready is refused on every input.
Sparse 24h tape and a missing `occurrence_datetime` are refuse bins. The
NFL `000` file is a pointer only. S1, S2, and R2-P4 stay gated.

`lab/governance/astra/packets/` is not in this checkout. The attached
freeze, scout hunt, and panel stub on this branch match the conductor
sha256 claims. `SOURCE_PINS.json` lists those digests.

- Freeze `C4_KXCPI_FEEQUEUE_HARNESS_FREEZE_2026-09-23.md` sha256 `949b255859196f02d73303a1019e51276c583f8d1e3ffb4f0a64d330467c6f93`
- Scout hunt `packets/scout_cashcow_hunt_2026-09-22/scout_hunt_KXCPI.json` sha256 `6033907bb739bc00c41c796a3c1ed24553e0b7a44116ec3ea4bbaf39066bdcc8` (44 markets / 4 events)
- Panel stub `lab/astra-capture/c4-kxcpi/panel_stub.json` sha256 `b20b0cbee50c127d2e9bb2548b574b7d643cc708f54019d53bd91775f9762c13` (`2026-09-23.c4-kxcpi-v0`, `admitted_at` null, 4 events / 44 markets, full scout, 21 missing `occurrence_datetime`, `KXCPI-26NOV` event occurrence null)
- Accept stamp sha256 `19ae0ae1fca66fa5c45bf8c13e013e3d710423c3e04194cc617d8bac1db546d7`

Fee pin `22371178cb2663250b4762f328069571c48cb551`.
Rails pin `6a28e0d6254327ea4e6451c781bec56215ac6cac`.
Those trees are not edited.

From this directory, Python 3.12 standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

No Logan keys. No live orders. A passing unit run is not an Examiner score.
