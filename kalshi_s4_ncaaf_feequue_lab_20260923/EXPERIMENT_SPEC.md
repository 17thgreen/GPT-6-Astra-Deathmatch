# S4 KXNCAAFGAME fee and queue honesty

September 23, 2026. This file is the hypothesis. It is committed before a
unit-test outcome is recorded. No figure in this document is a trading
result. Q6 outcomes that already exist are not re-labeled as evidence from
this probe. This is measurement-only college-football fee and queue honesty.
Feature family NCAAF-FQ.

## Placement

The harness freeze on this branch is
`S4_KXNCAAFGAME_FEEQUEUE_HARNESS_FREEZE_2026-09-23.md`, sha256
`3318204bf6e962f4f3372dad8c0f302e62d85c26b855de7369718654d0114728`.
That digest matches the conductor claim. The same bytes sit at the lab
root, the lab bundle, `packets/`, and
`packets/S4_KXNCAAFGAME_FEEQUEUE_HARNESS/`.

The parent kernel on this branch is
`S4_KXNCAAFGAME_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md`, sha256
`9e6556c150c726b679ac8393f1f5338cf983489259b0f34cdedf221c030be795`.
That digest matches the conductor parent claim on the same four paths.

`EXPERIMENT_SPEC.md` is the lab hypothesis. It is not a second freeze.

`lab/governance/astra/packets/` is not in this checkout. Packet copies sit
beside the engine and under `packets/S4_KXNCAAFGAME_FEEQUEUE_HARNESS/`.

`FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.
`results/EMPTY_RESULTS.json` keeps `maker_vs_taker_roi_delta`,
`fresh_vs_stale_gap`, and `settled_join_n` null.

Panel stub: `lab/astra-capture/s4-kxncaafgame/panel_stub.json`,
`panel_version` `2026-09-22.s4-kxncaafgame-v0`, sha256
`38167d11da5842bc4d39e6e7dcaab20a67294c735ba14d8bbeafde3154c6342a`.
`admitted_at` is null. The file is the conductor stub: 113 events, with
`volume_fp`, `open_interest_fp`, `results`, and `pnl` null. Capture README
sha256 `b0df0e86423ea11a049fb674602ab20f45acae5a549acf9eca604a6aa2d251b1`.
`panel_admitted.json` is preferred when it appears.

## One knob

Honesty partition:

| Arm | Partition |
|---|---|
| S4A0 | `maker_vs_taker_native` — native `taker_*` fields only. Lee-Ready refused on every input |
| S4A1 | `content_fresh_vs_stale_bin` — rails `content_fresh_flag` and queue-attribution bins only |

Fee pin `22371178cb2663250b4762f328069571c48cb551` (import only).
Rails pin `6a28e0d6254327ea4e6451c781bec56215ac6cac` (import only).

## What this run does not claim

No live orders. No Logan keys. No invented fills or PnL. No Q6-`000` retune.
No queue-fragility reopen. No Cap-SR reopen. No `admit.py`. No R1-P2
challenger bakeoff. Q7 Arm B stays killed. C1 empty-book stays `NOT_SCORED`.
Cap-SR, Cap-SR-FX, C3, C5, R3-P3, S5, feebook, and rails labs are not edited.
A later unit page is code verification only, not an Examiner score.
