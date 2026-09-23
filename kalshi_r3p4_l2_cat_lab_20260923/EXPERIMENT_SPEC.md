# R3-P4 L2-CAT sports-versus-nonsports harness

September 23, 2026. This file is the hypothesis. It is committed before a
unit-test outcome is recorded. No figure in this document is a trading
result. Q6 outcomes that already exist are not re-labeled as evidence from
this probe. This is measurement-only L2 shape partitioned by category
slice. Feature family **L2-CAT**.

## Placement

The harness freeze on this branch is
`R3_P4_L2_CAT_HARNESS_FREEZE_2026-09-23_2259.md`, sha256
`3fc370d93f0ea42864f7bf482d7f6515254999c76e2fc4477df1273bfcdc051f`.
That digest is the sha256 of the attached Conductor-box file. The same
bytes sit at the lab root, the lab bundle, `packets/`, and
`packets/R3_P4_L2_CAT_HARNESS/`.

The parent kernel on this branch is
`R3-P4_L2_SHAPE_LONGSHOT_DEPTH_FREEZE_KERNEL_2026-09-22.md`, sha256
`4a4e7cc61efcb436955c566edc7a2681603a014725bc79047f9d825392064528`.
That digest matches the attached parent file on the same four paths.

The panel stub is `lab/astra-capture/r3-p4-l2-shape/panel_stub.json`,
`panel_version` `2026-09-22.r3-p4-l2-shape-v0`, sha256
`7477e023ab70c59a6739650155ddb9d77077766e3afd80443e540d60b5a86cbb`.
`admitted_at` is null. The file is the attached conductor stub: 4 events
and 6 markets, sports 4 (NCAAF) and nonsports 2 (KXBTC), orderbook seed
6/6. The same bytes are copied into the lab bundle and
`packets/R3_P4_L2_CAT_HARNESS/`. `panel_admitted.json` is absent and is
preferred when it appears. A labeled recreation or an empty seed is refused.
The superseded digest prefix `e7c6b6d5` is not a pin.

`EXPERIMENT_SPEC.md` is the lab hypothesis. It is not a second freeze.
`lab/governance/astra/packets/` is not in this checkout.

`FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.
`results/EMPTY_RESULTS.json` keeps
`sf1_median_half_spread_bps_by_mid_decile`, `sf2_l1_top10_depth_share`,
`sf2_kl_vs_uniform_1_10`, `sports_vs_nonsports_sf_gap`, `n_books`, and
`n_snapshots` null.

The conductor stamp `CONDUCTOR_FROZEN_EXPERIMENT.json` is sha256
`6108488d33a4be6ece3235fa5b5a39cf563e97a543e3d8ec9828c4f5bea8ba9e`.
The import-only seed summary is sha256
`e0d5281133d89d5f0215a8f02ae438b688bf53e4a48f2eb4c3727db4a29bb6f2`.
`packets/r3_p4_l2_shape/live_get_2026-09-22/` is not in this checkout.
This hypothesis does not invent that directory. Recorded order books stay
inside the panel stub.

## One knob

Category slice, with feebook and rails fixed:

| Arm | Slice |
|---|---|
| R3P4C0 | `sports_only` — SF1/SF2 schema on sports books. Lee-Ready refused |
| R3P4C1 | `nonsports_only` — SF1/SF2 schema on non-sports (KXBTC) books. No invented depth |

Fee pin `22371178cb2663250b4762f328069571c48cb551` (import only).
Rails pin `6a28e0d6254327ea4e6451c781bec56215ac6cac` (import only).

The base R3-P4 SF1/SF2 lab (`kalshi_r3_p4_l2_shape_lab_20260922`, PR13)
stays a closed sibling. This harness does not edit it and does not turn
it into PnL.

`fixtures/synthetic_mid_depth_ladder.json`, added with the source freeze,
is a code-path stand-in. Book ids start with `synthetic:`. It is not a
panel fill, not production depth, and not an Examiner score.

## What this run does not claim

No live orders. No Logan keys. No invented depth, markets, fills, or PnL.
No Lee-Ready. No Q6-`000` retune. No queue-fragility reopen. No Cap-SR
reopen. No Cap-SR-FX reopen. No ATL@GB. No `admit.py`. Q, Cap-SR,
Cap-SR-FX, C3, C5, R3-P3, S4, S5, R2-P3, feebook, rails, and the PR13
base L2 shape lab are not edited. A later unit page is code verification
only, not an Examiner score.
