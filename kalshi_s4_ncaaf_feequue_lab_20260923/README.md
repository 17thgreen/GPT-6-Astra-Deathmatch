# S4 KXNCAAFGAME fee+queue honesty harness

Status: hypothesis committed, then source frozen. The unit page is
`results/UNIT_RESULTS.md`. `python3 -m unittest -v tests.test_orchestrator`
ran 9 tests in 0.033s at 2026-09-23T15:59:28Z. Result: OK. Failures: 0.
Errors: 0. That page is not profit and not an Examiner pass. `EXPERIMENT_SPEC.md` is the hypothesis.
`FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.
`results/EMPTY_RESULTS.json` keeps `maker_vs_taker_roi_delta`,
`fresh_vs_stale_gap`, and `settled_join_n` null.

This lab is measurement-only. Feature family NCAAF-FQ. The series is
`KXNCAAFGAME`. The only knob is the honesty partition: S4A0
`maker_vs_taker_native` and S4A1 `content_fresh_vs_stale_bin`. Lee-Ready is
refused on every input. Q7 Arm B stays killed. C1 empty-book stays
`NOT_SCORED`. Cap-SR, Cap-SR-FX, C3, C5, R3-P3, and S5 are not edited.

`lab/governance/astra/packets/` is not in this checkout. The conductor-box
freeze, parent kernel, and panel stub on this branch match the conductor
sha256 claims. Copies:

- `S4_KXNCAAFGAME_FEEQUEUE_HARNESS_FREEZE_2026-09-23.md` sha256 `3318204bf6e962f4f3372dad8c0f302e62d85c26b855de7369718654d0114728` (lab root, lab bundle, `packets/`, and `packets/S4_KXNCAAFGAME_FEEQUEUE_HARNESS/`)
- `S4_KXNCAAFGAME_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md` sha256 `9e6556c150c726b679ac8393f1f5338cf983489259b0f34cdedf221c030be795` (same four paths)
- `S4_KXNCAAFGAME_FEEQUEUE_HARNESS/`
- `packets/S4_KXNCAAFGAME_FEEQUEUE_HARNESS/`

Panel stub: `lab/astra-capture/s4-kxncaafgame/panel_stub.json`,
`panel_version` `2026-09-22.s4-kxncaafgame-v0`, `admitted_at` null,
sha256 `38167d11da5842bc4d39e6e7dcaab20a67294c735ba14d8bbeafde3154c6342a`.
The file is the conductor stub: 113 events, with `volume_fp`,
`open_interest_fp`, `results`, and `pnl` null. Capture README sha256
`b0df0e86423ea11a049fb674602ab20f45acae5a549acf9eca604a6aa2d251b1`.

Fee pin `22371178cb2663250b4762f328069571c48cb551`.
Rails pin `6a28e0d6254327ea4e6451c781bec56215ac6cac`.
Those trees are not edited.

From this directory, Python 3.12 standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

No Logan keys. No live orders. A passing unit run is not an Examiner score.
