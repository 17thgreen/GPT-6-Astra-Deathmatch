# R3-P4 L2-SF half-spread versus depth-KL harness

Status: hypothesis committed, then source frozen. The unit page is
`results/UNIT_RESULTS.md`. `python3 -m unittest -v tests.test_orchestrator`
ran 7 tests in 0.069s at 2026-09-23T17:31:39Z. Result: OK. Failures: 0.
Errors: 0. That page is not profit and not an Examiner pass. `EXPERIMENT_SPEC.md`
is the hypothesis. `FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.
`results/EMPTY_RESULTS.json` keeps
`sf1_median_half_spread_bps_by_mid_decile`, `sf2_l1_top10_depth_share`,
`sf2_kl_vs_uniform_1_10`, `n_books`, and `n_snapshots` null.

This lab is measurement-only. Feature family L2-SF. The only knob is
`shape_object`: R3P4S0 `sf1_half_spread` and R3P4S1 `sf2_depth_kl`.
Category slice is not an arm. Lee-Ready is refused. Invented depth is refused.
L2-CAT, EMPTY-OB, Cap-SR, QF, PROP-LQ, and SOT-ID stay closed. The PR13 base
L2 shape lab is not edited. S2 and R2-P4 stay queued.

`lab/governance/astra/` is not in this checkout. Authentic copies:

| File | sha256 |
|---|---|
| `R3_P4_L2_SF_HARNESS_FREEZE_2026-09-23.md` | `f00425261f085aef90e93b186810a0248165273f8bb923ef3597940a9e8345de` |
| `R3-P4_L2_SHAPE_LONGSHOT_DEPTH_FREEZE_KERNEL_2026-09-22.md` | `4a4e7cc61efcb436955c566edc7a2681603a014725bc79047f9d825392064528` |
| `lab/astra-capture/r3-p4-l2-shape/panel_stub.json` | `7477e023ab70c59a6739650155ddb9d77077766e3afd80443e540d60b5a86cbb` |

The same freeze, parent, and panel bytes sit in this lab, `R3_P4_L2_SF_HARNESS/`,
and `packets/R3_P4_L2_SF_HARNESS/`. The six `ob_*.json` files sit in
`live_get_2026-09-22/` on those three trees. Digests are in `SOURCE_PINS.json`.
`packets/r3_p4_l2_shape/live_get_2026-09-22/` stays absent.

Panel stub: `panel_version` `2026-09-22.r3-p4-l2-shape-v0`, `admitted_at`
null, 4 events, 6 markets, sports 4, nonsports 2.

Fee pin `22371178cb2663250b4762f328069571c48cb551` (import only).
Rails pin `6a28e0d6254327ea4e6451c781bec56215ac6cac` (import only).
Those trees are not edited.

From this directory, Python 3 standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

No Logan keys. No live orders. A passing unit run is not an Examiner score.
