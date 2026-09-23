# C2 KXNHLGAME fee and queue honesty

September 23, 2026. This file is the hypothesis. It is committed before a
unit-test outcome is recorded. No figure in this document is a trading
result. Q6 outcomes that already exist are not re-labeled as evidence from
this probe. This is measurement-only hockey fee and queue honesty.
Feature family NHL-FQ.

## Placement

The harness freeze on this branch is
`C2_KXNHLGAME_FEEQUEUE_HARNESS_FREEZE_2026-09-23.md`, sha256
`a36ec35143a32c7cd24e9fdf2a33f645d356b93e34c131bb1b8a94e3f92e38f5`.
Those bytes are the attached conductor freeze. The same bytes sit at the
lab root, the lab bundle, `packets/`, and
`packets/C2_KXNHLGAME_FEEQUEUE_HARNESS/`.

The scout hunt is
`packets/scout_cashcow_hunt_2026-09-22/scout_hunt_KXNHLGAME.json`, sha256
`1ab794ad688ba31e0178e78294dcdbe50cf2799a71f40245e5a04a80e9dd5762`.
66 markets and 33 events. Copies sit beside the freeze.

Panel stub: `lab/astra-capture/c2-kxnhlgame/panel_stub.json`,
`panel_version` `2026-09-23.c2-kxnhlgame-v0`, sha256
`60d183e7bdcf25adbc94eeeb3bb361b5232c19c0fe3e6a115f45ab3fcb100c79`.
`admitted_at` is null. 6 events and 12 markets. Each market object equals
the scout-hunt object with the same ticker. The same bytes are also at
`packets/C2_KXNHLGAME_PANEL_STUB_2026-09-23.json`.
`panel_admitted.json` is preferred when it appears.

`EXPERIMENT_SPEC.md` is the lab hypothesis. It is not a second freeze.
`SOURCE_PINS.json` lists the authentic digests. It does not contain the
file bytes.

`lab/governance/astra/packets/` is not in this checkout. Packet copies sit
beside the engine and under `packets/C2_KXNHLGAME_FEEQUEUE_HARNESS/`.

`FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.
`results/EMPTY_RESULTS.json` keeps `maker_vs_taker_roi_delta`,
`fresh_vs_stale_gap`, `settled_join_n`, and `n_books` null.
The attached pre-ACCEPT empty payload is stored as
`PRE_ACCEPT_EMPTY_RESULTS.json` and is refused as a scorecard.

## One knob

`analysis_slice`:

| Arm | Slice |
|---|---|
| C2A0 | `maker_vs_taker_native` — native `taker_*` fields only. Lee-Ready refused on every input |
| C2A1 | `content_fresh_vs_stale_bin` — rails `content_fresh_flag` and queue-attribution bins only. No fee invent. No invented fills |

Fee pin `22371178cb2663250b4762f328069571c48cb551` (import only).
Rails pin `6a28e0d6254327ea4e6451c781bec56215ac6cac` (import only).

The NFL `000` instrument is a path pointer only
(`nfl_factorial_lab_20260921/SHADOW_CANDIDATE_FREEZE.json`). No signal is
ported from that file.

## What this run does not claim

No live orders. No Logan keys. No invented markets, depth, fills, or PnL.
No Lee-Ready. No `admit.py`. No Q6-`000` retune. No Cap-SR, QF, L2, EMPTY-OB,
SOT-ID, or L2-SF reopen. This packet does not claim S1 green and does not
ungate S1, S2, or R2-P4. ATL@GB stays refused. A later unit page is code
verification only, not an Examiner score.
