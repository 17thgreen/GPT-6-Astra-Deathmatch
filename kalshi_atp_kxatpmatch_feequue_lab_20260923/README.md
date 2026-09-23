# ATP KXATPMATCH fee+queue honesty harness

Status: hypothesis committed, then source frozen. The unit page is
`results/UNIT_RESULTS.md`. `python3 -m unittest -v tests.test_orchestrator`
ran 13 tests in 0.069s at 2026-09-23T18:23:56Z. Result: OK. Failures: 0.
Errors: 0. That page is not profit and not an Examiner pass.
`EXPERIMENT_SPEC.md` is the hypothesis. `FROZEN_EXPERIMENT.json` keeps
`results` and `pnl` null. `results/EMPTY_RESULTS.json` keeps
`maker_vs_taker_roi_delta`, `fresh_vs_stale_gap`, `settled_join_n`, and
`n_books` null.

This lab is measurement-only. Feature family ATP-FQ. The series is
`KXATPMATCH`. The only knob is `analysis_slice`: ATPA0
`maker_vs_taker_native` and ATPA1 `content_fresh_vs_stale_bin`. Lee-Ready
is refused on every input. Fill density and `occurrence_datetime` are not
invented. On the attached hunt the missing `occurrence_datetime` count is
0, and that zero is the census, not a filled timestamp. The NFL `000` file
is a pointer only. S1 is not claimed green. S1, S2, and R2-P4 stay gated.

`lab/governance/astra/packets/` is not in this checkout. The attached
freeze, scout hunt, and panel stub on this branch match the conductor
sha256 claims. `SOURCE_PINS.json` lists those digests.

- Freeze `ATP_KXATPMATCH_FEEQUEUE_HARNESS_FREEZE_2026-09-23.md` sha256 `4d4ce944946e72dd40567d14388fe11c6145fbbb32505a880bcf80a4c8b4dffe`
- Scout hunt `packets/scout_cashcow_hunt_2026-09-22/scout_hunt_KXATPMATCH.json` sha256 `14c99ec8ea00bae507a21d0e6a1879fb94d32ef69ad4b5e3b40a9952821e5da7` (48 markets / 24 events)
- Panel stub `lab/astra-capture/atp-kxatpmatch/panel_stub.json` sha256 `ed041c502d1f775d33c44bf900ac91b1339d99045bddd2052edd09a139ae2d3f` (`2026-09-23.atp-kxatpmatch-v0`, `admitted_at` null, 6 events / 12 markets, authentic scout subset)
- Accept stamp sha256 `b038994585e19d28d014882594239eafc2657b6de7da105f238c90d49954bd8b`

Fee pin `22371178cb2663250b4762f328069571c48cb551`.
Rails pin `6a28e0d6254327ea4e6451c781bec56215ac6cac`.
Those trees are not edited.

From this directory, Python 3.12 standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

No Logan keys. No live orders. A passing unit run is not an Examiner score.
