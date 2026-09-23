# R3-P3 FL maker/taker + favorite–longshot bands harness

Status: hypothesis committed, then source frozen. The unit page is
`results/UNIT_RESULTS.md` (8 tests, OK, 2026-09-23T14:27:43Z). That page is
not profit and not an Examiner pass. `EXPERIMENT_SPEC.md` is the hypothesis.
`FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.
`results/EMPTY_RESULTS.json` keeps `mz_alpha`, `mz_psi`,
`post_fee_roi_by_band`, `maker_vs_taker_roi_delta`, and `settled_join_n`
null.

This lab is measurement-only. The only knob is the analysis slice: R3P3A0
`maker_vs_taker` and R3P3A1 `fl_bands_10c`. Native taker fields are
`taker_outcome_side` and `taker_book_side`. Lee-Ready is refused. The
feebook import is schema only. ROI stays null. C3 weather preference on
the stub is a cite. C3 and C5 are not edited.

`lab/governance/astra/packets/` is not in this checkout. Freeze copies:

- `R3_P3_FL_MAKER_TAKER_HARNESS_FREEZE_2026-09-23.md` (sha256 `fbc58539b7a469d005b7f75b786efddecc1028a3bb0da601bc0082c9d4aab179`)
- `R3-P3_FL_MAKER_TAKER_BANDS_FREEZE_KERNEL_2026-09-22.md` (sha256 `0ed697149136acb3aa840aeeb79d11c8f6ef80f37ce4dd692a3cb690212206a7`)
- `R3_P3_FL_MAKER_TAKER_HARNESS/`
- `packets/R3_P3_FL_MAKER_TAKER_HARNESS_FREEZE_2026-09-23.md`
- `packets/R3-P3_FL_MAKER_TAKER_BANDS_FREEZE_KERNEL_2026-09-22.md`
- `packets/R3_P3_FL_MAKER_TAKER_HARNESS/`

Panel stub: `lab/astra-capture/r3-p3-fl-maker-taker/panel_stub.json`,
`panel_version` `2026-09-22.r3-p3-fl-maker-taker-v0`, `admitted_at` null.
Bands registry: `lab/astra-capture/r3-p3-fl-maker-taker/bands_registry_10c.json`.

Fee pin `22371178cb2663250b4762f328069571c48cb551`.
Rails pin `6a28e0d6254327ea4e6451c781bec56215ac6cac`.

From this directory, Python 3.12 standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

No Logan keys. No live orders. A passing unit run is not an Examiner score.
