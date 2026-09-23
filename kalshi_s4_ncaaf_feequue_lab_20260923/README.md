# S4 KXNCAAFGAME fee+queue honesty harness

Status: hypothesis committed, then source frozen. The unit page is
`results/UNIT_RESULTS.md` (9 tests, OK, 2026-09-23T15:46:14Z). That page is
not profit and not an Examiner pass. `EXPERIMENT_SPEC.md` is the hypothesis.
`FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.
`results/EMPTY_RESULTS.json` keeps `maker_vs_taker_roi_delta`,
`fresh_vs_stale_gap`, and `settled_join_n` null.

This lab is measurement-only. Feature family NCAAF-FQ. The series is
`KXNCAAFGAME`. The only knob is the honesty partition: S4A0
`maker_vs_taker_native` and S4A1 `content_fresh_vs_stale_bin`. Lee-Ready is
refused on every input. Q7 Arm B stays killed. C1 empty-book stays
`NOT_SCORED`. Cap-SR, Cap-SR-FX, C3, C5, R3-P3, and S5 are not edited.

`lab/governance/astra/packets/` is not in this checkout. The conductor-box
freeze bytes were not attached. Freeze copies are the checkout recreation:

- `S4_KXNCAAFGAME_FEEQUEUE_HARNESS_FREEZE_2026-09-23.md` (sha256 `00117c348573076bc35af422e6618d750c1e6b89c3387f2b7c0b0f259d3fe2a2`; conductor claim `3318204bf6e962f4f3372dad8c0f302e62d85c26b855de7369718654d0114728`)
- `S4_KXNCAAFGAME_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md` (sha256 `f0e502264ce79d8e958c54cace387aa0521f616dd59290356aaafc33e9096847`; conductor claim `9e6556c150c726b679ac8393f1f5338cf983489259b0f34cdedf221c030be795`)
- `S4_KXNCAAFGAME_FEEQUEUE_HARNESS/`
- `packets/S4_KXNCAAFGAME_FEEQUEUE_HARNESS_FREEZE_2026-09-23.md`
- `packets/S4_KXNCAAFGAME_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md`
- `packets/S4_KXNCAAFGAME_FEEQUEUE_HARNESS/`

Panel seed: `lab/astra-capture/s4-kxncaafgame/panel_stub.json`,
`panel_version` `2026-09-22.s4-kxncaafgame-v0`, `admitted_at` null,
sha256 `eb0a9ea7e4cf24d6f805f63688dbb48c71dc91a81bcea4afb2c88f73588b8112`.
The conductor stub claim is
`38167d11da5842bc4d39e6e7dcaab20a67294c735ba14d8bbeafde3154c6342a`
(~113 events). This seed has zero events so that cohort is not invented.

Fee pin `22371178cb2663250b4762f328069571c48cb551`.
Rails pin `6a28e0d6254327ea4e6451c781bec56215ac6cac`.
Those trees are not edited.

From this directory, Python 3.12 standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

No Logan keys. No live orders. A passing unit run is not an Examiner score.
