# C2 KXNHLGAME fee+queue honesty harness

Status: hypothesis committed, then source frozen. The unit page is
`results/UNIT_RESULTS.md`. `python3 -m unittest -v tests.test_orchestrator`
ran 12 tests in 0.057s at 2026-09-23T17:49:26Z. Result: OK. Failures: 0.
Errors: 0. That page is not profit and not an Examiner pass.
`EXPERIMENT_SPEC.md` is the hypothesis. `FROZEN_EXPERIMENT.json` keeps
`results` and `pnl` null. `results/EMPTY_RESULTS.json` keeps
`maker_vs_taker_roi_delta`, `fresh_vs_stale_gap`, `settled_join_n`, and
`n_books` null.

This lab is measurement-only. Feature family NHL-FQ. The series is
`KXNHLGAME`. The only knob is `analysis_slice`: C2A0
`maker_vs_taker_native` and C2A1 `content_fresh_vs_stale_bin`. Lee-Ready
is refused on every input. The NFL `000` file is a pointer only. S1 is not
claimed green. S1, S2, and R2-P4 stay gated.

`lab/governance/astra/packets/` is not in this checkout. The attached
freeze, scout hunt, and panel stub on this branch match the conductor
sha256 claims. `SOURCE_PINS.json` lists those digests.

- Freeze `C2_KXNHLGAME_FEEQUEUE_HARNESS_FREEZE_2026-09-23.md` sha256 `a36ec35143a32c7cd24e9fdf2a33f645d356b93e34c131bb1b8a94e3f92e38f5`
- Scout hunt `packets/scout_cashcow_hunt_2026-09-22/scout_hunt_KXNHLGAME.json` sha256 `1ab794ad688ba31e0178e78294dcdbe50cf2799a71f40245e5a04a80e9dd5762` (66 markets / 33 events)
- Panel stub `lab/astra-capture/c2-kxnhlgame/panel_stub.json` sha256 `60d183e7bdcf25adbc94eeeb3bb361b5232c19c0fe3e6a115f45ab3fcb100c79` (`2026-09-23.c2-kxnhlgame-v0`, `admitted_at` null, 6 events / 12 markets)

Fee pin `22371178cb2663250b4762f328069571c48cb551`.
Rails pin `6a28e0d6254327ea4e6451c781bec56215ac6cac`.
Those trees are not edited.

From this directory, Python 3.12 standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

No Logan keys. No live orders. A passing unit run is not an Examiner score.
