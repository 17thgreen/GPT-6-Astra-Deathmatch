# R3-P4 L2-CAT sports-versus-nonsports harness

Status: hypothesis committed. The unit page is not yet recorded. This
README is not profit and not an Examiner pass. `EXPERIMENT_SPEC.md` is
the hypothesis. `FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.
`results/EMPTY_RESULTS.json` keeps
`sf1_median_half_spread_bps_by_mid_decile`, `sf2_l1_top10_depth_share`,
`sf2_kl_vs_uniform_1_10`, `sports_vs_nonsports_sf_gap`, `n_books`, and
`n_snapshots` null.

This lab is measurement-only. Feature family L2-CAT. The only knob is
category slice: R3P4C0 `sports_only` and R3P4C1 `nonsports_only`.
Lee-Ready is refused. Invented depth is refused. ATL@GB is refused.
Q6-`000`, QF, Cap-SR, and Cap-SR-FX stay closed. The PR13 base L2 shape
lab is not edited.

`lab/governance/astra/packets/` is not in this checkout. The attached
conductor-box freeze, parent kernel, and panel stub on this branch match
the conductor sha256 claims. Copies:

- `R3_P4_L2_CAT_HARNESS_FREEZE_2026-09-23_2259.md` sha256 `3fc370d93f0ea42864f7bf482d7f6515254999c76e2fc4477df1273bfcdc051f` (lab root, lab bundle, `packets/`, and `packets/R3_P4_L2_CAT_HARNESS/`)
- `R3-P4_L2_SHAPE_LONGSHOT_DEPTH_FREEZE_KERNEL_2026-09-22.md` sha256 `4a4e7cc61efcb436955c566edc7a2681603a014725bc79047f9d825392064528` (same four paths)
- `lab/astra-capture/r3-p4-l2-shape/panel_stub.json` sha256 `7477e023ab70c59a6739650155ddb9d77077766e3afd80443e540d60b5a86cbb` (also the lab bundle and `packets/R3_P4_L2_CAT_HARNESS/`)
- `R3_P4_L2_CAT_HARNESS/`
- `packets/R3_P4_L2_CAT_HARNESS/`

Panel stub: `panel_version` `2026-09-22.r3-p4-l2-shape-v0`, `admitted_at`
null, 4 events, 6 markets, sports 4, nonsports 2.

Fee pin `22371178cb2663250b4762f328069571c48cb551`.
Rails pin `6a28e0d6254327ea4e6451c781bec56215ac6cac`.
Those trees are not edited.

From this directory, Python 3 standard library, once the source freeze is
present:

```bash
python3 -m unittest -v tests.test_orchestrator
```

No Logan keys. No live orders. A passing unit run is not an Examiner score.
