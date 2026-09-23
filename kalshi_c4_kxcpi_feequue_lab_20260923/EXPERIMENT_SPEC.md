# C4 KXCPI fee and queue honesty

September 23, 2026. This file is the hypothesis. It is committed before a
unit-test outcome is recorded. No figure in this document is a trading
result. Q6 outcomes that already exist are not re-labeled as evidence from
this probe. This is measurement-only CPI threshold-ladder fee and queue
honesty. Feature family CPI-FQ.

## Placement

The harness freeze on this branch is
`C4_KXCPI_FEEQUEUE_HARNESS_FREEZE_2026-09-23.md`, sha256
`949b255859196f02d73303a1019e51276c583f8d1e3ffb4f0a64d330467c6f93`.
Those bytes are the attached conductor freeze. The same bytes sit at the
lab root, the lab bundle, `packets/`, and
`packets/C4_KXCPI_FEEQUEUE_HARNESS/`.

The scout hunt is
`packets/scout_cashcow_hunt_2026-09-22/scout_hunt_KXCPI.json`, sha256
`6033907bb739bc00c41c796a3c1ed24553e0b7a44116ec3ea4bbaf39066bdcc8`.
44 markets and 4 events. Copies sit beside the freeze.

Panel stub: `lab/astra-capture/c4-kxcpi/panel_stub.json`,
`panel_version` `2026-09-23.c4-kxcpi-v0`, sha256
`b20b0cbee50c127d2e9bb2548b574b7d643cc708f54019d53bd91775f9762c13`.
`admitted_at` is null. 4 events and 44 markets. Each market object equals
the scout-hunt object with the same ticker. The panel is the full scout.
Twenty-one markets keep a null `occurrence_datetime`. The `KXCPI-26NOV`
event `occurrence_datetime` stays null. Event occurrence is taken only from
market occurrence values that are already present. The same bytes are also
at `packets/C4_KXCPI_PANEL_STUB_2026-09-23.json`.
`panel_admitted.json` is preferred when it appears.

`EXPERIMENT_SPEC.md` is the lab hypothesis. It is not a second freeze.
`SOURCE_PINS.json` lists the authentic digests. It does not contain the
file bytes.

`lab/governance/astra/packets/` is not in this checkout. Packet copies sit
beside the engine and under `packets/C4_KXCPI_FEEQUEUE_HARNESS/`.

`FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.
`results/EMPTY_RESULTS.json` keeps `maker_vs_taker_roi_delta`,
`sparse_vs_fresh_gap`, `missing_sot_n`, `settled_join_n`, and `n_books`
null. The attached pre-ACCEPT empty payload is stored as
`PRE_ACCEPT_EMPTY_RESULTS.json` and is refused as a scorecard.

## One knob

`analysis_slice`:

| Arm | Slice |
|---|---|
| C4A0 | `maker_vs_taker_native` — native `taker_*` fields only. Lee-Ready refused on every input |
| C4A1 | `sparse_24h_vs_fresh_bin` — rails `content_fresh_flag` plus sparse-24h and missing-`occurrence_datetime` refuse bins. No invented fills, fill density, or source of time |

Fee pin `22371178cb2663250b4762f328069571c48cb551` (import only).
Rails pin `6a28e0d6254327ea4e6451c781bec56215ac6cac` (import only).

The NFL `000` instrument is a path pointer only
(`nfl_factorial_lab_20260921/SHADOW_CANDIDATE_FREEZE.json`). No signal is
ported from that file.

## What this run does not claim

No live orders. No Logan keys. No invented markets, depth, fills, fill
density, `occurrence_datetime`, or PnL. No Lee-Ready. No `admit.py`. No
Q6-`000` retune. No Cap-SR, QF, L2, EMPTY-OB, SOT-ID, L2-SF, or NHL-FQ
reopen. This packet does not ungate S1, S2, or R2-P4. ATL@GB stays refused.
A later unit page is code verification only, not an Examiner score.
