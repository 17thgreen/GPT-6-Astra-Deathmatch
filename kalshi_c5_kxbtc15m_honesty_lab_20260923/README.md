# C5 KXBTC15M fee and queue honesty stress

Status: hypothesis committed, then source frozen. The unit page is
`results/UNIT_RESULTS.md` (8 tests, OK, 2026-09-23T14:01:54Z). That page is
not profit and not an Examiner pass. `EXPERIMENT_SPEC.md` is the hypothesis.
`FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.
`results/EMPTY_RESULTS.json` keeps `freshness_gap_sec`,
`queue_bin_mismatch_rate`, `fee_delta_vs_inherited_model`, and
`turnover_stress_flag` null.

This lab is measurement-only. It is not live crypto trading. The series is
`KXBTC15M`. The only knob is honesty stress cadence: C5H0 `per_window` and
C5H1 `multi_window_stack`. C3 stays queued. Cap-SR is not edited.

`lab/governance/astra/packets/` is not in this checkout. Freeze copies:

- `C5_KXBTC15M_HONESTY_HARNESS_FREEZE_2026-09-23.md` (sha256 `23b908af6e9a7799c9bbdac04b27e683dfccd0c0c25d691df84ff715202d3cab`)
- `C5_KXBTC15M_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md` (sha256 `4d1b72a38603de181e71f80b3cc6515b170a2bffe11f8770dac1296373e50263`)
- `C5_KXBTC15M_HONESTY_HARNESS/`
- `packets/C5_KXBTC15M_HONESTY_HARNESS_FREEZE_2026-09-23.md`
- `packets/C5_KXBTC15M_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md`
- `packets/C5_KXBTC15M_HONESTY_HARNESS/`

Panel stub: `lab/astra-capture/c5-kxbtc15m/panel_stub.json`,
`panel_version` `2026-09-22.c5-kxbtc15m-v0`, `admitted_at` null.

Fee pin `22371178cb2663250b4762f328069571c48cb551`.
Rails pin `6a28e0d6254327ea4e6451c781bec56215ac6cac`.
Helpers are imported from the Examiner hygiene join and checked against the
C1 queue-bin helper. Those trees are not edited.

From this directory, Python 3.12 standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

No Logan keys. No live orders. A passing unit run, once recorded, is not an
Examiner score.

