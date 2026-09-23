# R3-P4 L2-SF half-spread versus depth-KL harness

September 23, 2026. This file is the hypothesis. It is committed before a
unit-test outcome is recorded. No figure in this document is a trading
result. This is measurement-only quote-side shape. Feature family **L2-SF**.

## Placement

The harness freeze on this branch is
`R3_P4_L2_SF_HARNESS_FREEZE_2026-09-23.md`, sha256
`f00425261f085aef90e93b186810a0248165273f8bb923ef3597940a9e8345de`.
That digest is the sha256 of the attached Conductor-box file.

The parent kernel is
`R3-P4_L2_SHAPE_LONGSHOT_DEPTH_FREEZE_KERNEL_2026-09-22.md`, sha256
`4a4e7cc61efcb436955c566edc7a2681603a014725bc79047f9d825392064528`.

The panel stub is `lab/astra-capture/r3-p4-l2-shape/panel_stub.json`,
`panel_version` `2026-09-22.r3-p4-l2-shape-v0`, sha256
`7477e023ab70c59a6739650155ddb9d77077766e3afd80443e540d60b5a86cbb`.
`admitted_at` is null. The file is the attached conductor stub: 4 events
and 6 markets. Sports and nonsports stay the natural seed. They are not
an arm. `panel_admitted.json` is absent and is preferred when it appears.

`lab/governance/astra/` is not in this checkout. Authentic copies live at
the lab root, `R3_P4_L2_SF_HARNESS/`, `packets/R3_P4_L2_SF_HARNESS/`, and,
for the uniquely named freeze, accept, and examiner-hold files, `packets/`.
`packets/PRE_ACCEPT_EMPTY_RESULTS.json` and
`packets/CONDUCTOR_FROZEN_EXPERIMENT.json` already belong to other packets
and are not overwritten.

`packets/r3_p4_l2_shape/live_get_2026-09-22/` stays absent. The closed
L2-CAT harness pins that absence. The attached order-book bytes are stored
under `live_get_2026-09-22/` in this lab and in
`packets/R3_P4_L2_SF_HARNESS/`. Digests are listed in `SOURCE_PINS.json`.

Each of the six files has at least one non-empty bid side. The bytes also
show one empty side on PITT, BUCK, T76250, and T95749.99. Those empty
sides are not filled in. TENN and MRST have both sides. This hypothesis
does not publish half-spread, depth share, or KL for any of them.

## One knob

`shape_object`, with feebook and rails fixed. Category slice is not an arm.

| Arm | Shape object |
|---|---|
| R3P4S0 | `sf1_half_spread` — median half-spread bps by mid-price decile. Lee-Ready refused |
| R3P4S1 | `sf2_depth_kl` — L1/top-10 depth share and KL versus uniform 1/10. No invented depth or fills |

Fee pin `22371178cb2663250b4762f328069571c48cb551` (import only).
Rails pin `6a28e0d6254327ea4e6451c781bec56215ac6cac` (import only).

The base R3-P4 lab (`kalshi_r3_p4_l2_shape_lab_20260922`, PR13) stays a
closed sibling. This harness does not edit it and does not turn it into
PnL. L2-CAT stays closed. EMPTY-OB stays closed.

`FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.
`results/EMPTY_RESULTS.json` keeps
`sf1_median_half_spread_bps_by_mid_decile`, `sf2_l1_top10_depth_share`,
`sf2_kl_vs_uniform_1_10`, `n_books`, and `n_snapshots` null.
The attached pre-ACCEPT empty payload is stored as
`PRE_ACCEPT_EMPTY_RESULTS.json` and is refused as a scorecard.

`fixtures/synthetic_two_sided_ladder.json`, added with the source freeze,
is a code-path stand-in. Book ids start with `synthetic:`. It is not a
panel fill, not production depth, and not an Examiner score.

## What this run does not claim

No live orders. No Logan keys. No invented depth, markets, fills, or PnL.
No Lee-Ready. No `admit.py`. No Q6-`000` retune. No Cap-SR, Cap-SR-FX, QF,
PROP-LQ, SOT-ID, EMPTY-OB, or L2-CAT reopen. No S2 or R2-P4 ungate. No
ATL@GB. Q, Cap-SR, Cap-SR-FX, C3, C5, R3-P3, the PR13 base L2 lab, L2-CAT,
EMPTY-OB, SOT-ID, S4, S5, R2-P3, feebook, and rails are not edited. A later
unit page is code verification only, not an Examiner score.
