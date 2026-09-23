# S5 KXMVECROSSCATEGORY fill-vs-legs harness

Status: hypothesis committed, then source frozen. The unit page is
`results/UNIT_RESULTS.md` (8 tests, OK, 2026-09-23T15:05:04Z). That page is
not profit and not an Examiner pass. `EXPERIMENT_SPEC.md` is the hypothesis.
`FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.
`results/EMPTY_RESULTS.json` keeps `fill_vs_legs_mid_gap`,
`combo_fee_delta_vs_feebook`, `legs_join_rate`, and `freshness_gap_sec` null.

This lab is measurement-only. Feature family MVE-FL. The series is
`KXMVECROSSCATEGORY`. The only knob is leg mid source: S5L0 `tob_1m` and
S5L1 `synthetic_leg_product`. RFQ is out of scope. S4 NCAAF and R2-P3 stay
queued. Cap-SR and Cap-SR-FX are not edited.

`lab/governance/astra/packets/` is not in this checkout. Freeze copies:

- `S5_KXMVECROSSCATEGORY_FILLLEGS_HARNESS_FREEZE_2026-09-23.md` (sha256 `8a118e6f1fdc8c22c6e559f395667aedffa5d270d067e39b6ae3ee24b2046d16`)
- `S5_KXMVECROSSCATEGORY_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md` (sha256 `a28932ba13b4913b69c48b73dde8ba066cebd212670d0b1cbb5ea8e93734b8ba`)
- `S5_KXMVECROSSCATEGORY_FILLLEGS_HARNESS/`
- `packets/S5_KXMVECROSSCATEGORY_FILLLEGS_HARNESS_FREEZE_2026-09-23.md`
- `packets/S5_KXMVECROSSCATEGORY_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md`
- `packets/S5_KXMVECROSSCATEGORY_FILLLEGS_HARNESS/`

Panel stub: `lab/astra-capture/s5-kxmvecrosscategory/panel_stub.json`,
`panel_version` `2026-09-22.s5-kxmvecrosscategory-v0`, `admitted_at` null,
5 markets and 21 events.

Fee pin `22371178cb2663250b4762f328069571c48cb551` with series override
`quadratic_with_combo_maker_fees`.
Rails pin `6a28e0d6254327ea4e6451c781bec56215ac6cac`.
Those trees are not edited.

From this directory, Python 3.12 standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

No Logan keys. No live orders. No RFQ. A passing unit run, once recorded,
is not an Examiner score.
