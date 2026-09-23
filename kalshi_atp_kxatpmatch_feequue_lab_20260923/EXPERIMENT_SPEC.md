# ATP KXATPMATCH fee and queue honesty

September 23, 2026. This file is the hypothesis. It is committed before a
unit-test outcome is recorded. No figure in this document is a trading
result. Q6 outcomes that already exist are not re-labeled as evidence from
this probe. This is measurement-only tennis fee and queue honesty.
Feature family ATP-FQ.

## Placement

The harness freeze on this branch is
`ATP_KXATPMATCH_FEEQUEUE_HARNESS_FREEZE_2026-09-23.md`, sha256
`4d4ce944946e72dd40567d14388fe11c6145fbbb32505a880bcf80a4c8b4dffe`.
Those bytes are the attached conductor freeze. The same bytes sit at the
lab root, the lab bundle, `packets/`, and
`packets/ATP_KXATPMATCH_FEEQUEUE_HARNESS/`.

The scout hunt is
`packets/scout_cashcow_hunt_2026-09-22/scout_hunt_KXATPMATCH.json`, sha256
`14c99ec8ea00bae507a21d0e6a1879fb94d32ef69ad4b5e3b40a9952821e5da7`.
48 markets and 24 events. Copies sit beside the freeze.

Panel stub: `lab/astra-capture/atp-kxatpmatch/panel_stub.json`,
`panel_version` `2026-09-23.atp-kxatpmatch-v0`, sha256
`ed041c502d1f775d33c44bf900ac91b1339d99045bddd2052edd09a139ae2d3f`.
`admitted_at` is null. 6 events and 12 markets. Each market object equals
the scout-hunt object with the same ticker. The same bytes are also at
`packets/ATP_KXATPMATCH_PANEL_STUB_2026-09-23.json`.
`panel_admitted.json` is preferred when it appears.

On this hunt every scout market and every panel market carries an
`occurrence_datetime` that ends in `Z`. The missing count is 0. A missing
key or a null value stays missing. This hypothesis does not fill one in.
`fill_density` is absent from the hunt and is not invented.

`EXPERIMENT_SPEC.md` is the lab hypothesis. It is not a second freeze.
`SOURCE_PINS.json` lists the authentic digests. It does not contain the
file bytes.

`lab/governance/astra/packets/` is not in this checkout. Packet copies sit
beside the engine and under `packets/ATP_KXATPMATCH_FEEQUEUE_HARNESS/`.

`FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.
`results/EMPTY_RESULTS.json` keeps `maker_vs_taker_roi_delta`,
`fresh_vs_stale_gap`, `settled_join_n`, and `n_books` null.
The attached pre-ACCEPT empty payload is stored as
`PRE_ACCEPT_EMPTY_RESULTS.json` and is refused as a scorecard.

## One knob

`analysis_slice`:

| Arm | Slice |
|---|---|
| ATPA0 | `maker_vs_taker_native` — native `taker_*` fields only. Lee-Ready refused on every input |
| ATPA1 | `content_fresh_vs_stale_bin` — rails `content_fresh_flag` and queue-attribution bins only. No invented fills, fill density, or `occurrence_datetime` |

Fee pin `22371178cb2663250b4762f328069571c48cb551` (import only).
Rails pin `6a28e0d6254327ea4e6451c781bec56215ac6cac` (import only).

The NFL `000` instrument is a path pointer only
(`nfl_factorial_lab_20260921/SHADOW_CANDIDATE_FREEZE.json`). No signal is
ported from that file.

## What this run does not claim

No live orders. No Logan keys. No invented markets, depth, fills, fill
density, `occurrence_datetime`, or PnL. No Lee-Ready. No `admit.py`. No
Q6-`000` retune. No Cap-SR, QF, L2, EMPTY-OB, SOT-ID, L2-SF, NHL-FQ, or
CPI-FQ reopen. This packet does not claim S1 green and does not ungate S1,
S2, or R2-P4. ATL@GB stays refused. A later unit page is code verification
only, not an Examiner score.
