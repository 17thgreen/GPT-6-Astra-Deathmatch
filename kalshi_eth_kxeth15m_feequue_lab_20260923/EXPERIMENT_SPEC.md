# ETH KXETH15M fee and queue honesty

September 23, 2026. This file is the hypothesis. It is committed before a
unit-test outcome is recorded. No figure in this document is a trading
result. Q6 outcomes that already exist are not re-labeled as evidence from
this probe. This is measurement-only ETH 15-minute fee and queue honesty.
Feature family ETH-FQ. It is not live crypto trading.

## Placement

The harness freeze to be committed verbatim is
`ETH_KXETH15M_FEEQUEUE_HARNESS_FREEZE_2026-09-23.md`, sha256
`9cae3bad089e6e18bee22694a36a1a2c18db33935a315766cd6bd8f8476aa83a`.
Those bytes are the attached conductor freeze. The same bytes will sit at
the lab root, the lab bundle, `packets/`, and
`packets/ETH_KXETH15M_FEEQUEUE_HARNESS/`.

The scout hunt is the attached file sha256
`18f70001c8d68418d435e2016b756f90753e374a92d323f8e999f76215d9cf9c`.
1 market and 1 event. The panel cites
`packets/scout_eth_kxeth15m_2026-09-23/scout_hunt_KXETH15M.json`.
The freeze also names
`packets/scout_cashcow_hunt_2026-09-22/scout_hunt_KXETH15M.json`.
Both paths will hold the same attached bytes.

Panel stub: `lab/astra-capture/eth-kxeth15m/panel_stub.json`,
`panel_version` `2026-09-23.eth-kxeth15m-v0`, sha256
`b3379783c84eaa910f6a57f5318b8536f21220cfeaf0f73e9ff73ee0f20dd90d`.
`admitted_at` is null. 1 event and 1 market. The panel is the full tiny
hunt. The market object equals the scout-hunt object with the same ticker.
The same bytes are also at
`packets/ETH_KXETH15M_PANEL_STUB_2026-09-23.json`.
`panel_admitted.json` is preferred when it appears.

The attached market and the panel event both carry
`occurrence_datetime` `2026-09-23T18:35:00Z`. The missing count on this
hunt is 0. A missing key or a null value stays missing. This hypothesis
does not fill one in. `fill_density` is absent from the hunt and is not
invented. Public size fields on the market quote are not a depth ladder
and are not `n_books`.

The attached accept stamp sha256
`3e553395a47d5ced1a4b48d81b8d0d760d984becdbcb6c1dd574dafc39621a5e`
is Conductor `ACCEPT` with `implement` true. It is committed verbatim.
It is not rewritten into a larger accept record.

`EXPERIMENT_SPEC.md` is the lab hypothesis. It is not a second freeze.
`SOURCE_PINS.json` will list the authentic digests. It does not contain
the file bytes.

`lab/governance/astra/packets/` is not in this checkout. Packet copies sit
beside the engine and under `packets/ETH_KXETH15M_FEEQUEUE_HARNESS/`.

`FROZEN_EXPERIMENT.json` will keep `results` and `pnl` null.
`results/EMPTY_RESULTS.json` will keep `maker_vs_taker_roi_delta`,
`fresh_vs_stale_gap`, `settled_join_n`, and `n_books` null.
The attached pre-ACCEPT empty payload is stored as
`PRE_ACCEPT_EMPTY_RESULTS.json` and is refused as a scorecard.
The attached conductor stamp is stored as
`CONDUCTOR_FROZEN_EXPERIMENT.json`.

## One knob

`analysis_slice`:

| Arm | Slice |
|---|---|
| ETHA0 | `maker_vs_taker_native` — native `taker_*` fields only. Lee-Ready refused on every input |
| ETHA1 | `content_fresh_vs_stale_bin` — rails `content_fresh_flag` and queue-attribution bins only. No invented fills, fill density, or `occurrence_datetime` |

Fee pin `22371178cb2663250b4762f328069571c48cb551` (import only).
Rails pin `6a28e0d6254327ea4e6451c781bec56215ac6cac` (import only).

The attached panel records series `fee_type` `quadratic` and
`fee_multiplier` 1 from `GET /series/KXETH15M`. Market objects on the hunt
do not carry `fee_*` fields. This hypothesis does not install a feebook
series override. A probe of the imported table is expected to resolve
`KXETH15M` as `default_unknown_series` until an override exists in that
pinned table. The numeric fee is not a scorecard field.

The NFL `000` instrument is a path pointer only
(`nfl_factorial_lab_20260921/SHADOW_CANDIDATE_FREEZE.json`). No signal is
ported from that file. No bacchus or kxeth15m strategy is ported. C5 is
not reopened. ATP-FQ is not reopened.

## What this run does not claim

No live orders. No Logan keys. No invented markets, depth, fills, fill
density, `occurrence_datetime`, or PnL. No Lee-Ready. No `admit.py`. No
Q6-`000` retune or signal port. No Cap-SR, QF, L2, EMPTY-OB, SOT-ID,
L2-SF, NHL-FQ, CPI-FQ, ATP-FQ, or C5 reopen. No bacchus or kxeth15m
strategy port. R3-P1 and R3-P2 stay out of this harness. This packet does
not claim S1 green and does not ungate S1, S2, or R2-P4. A later unit page
is code verification only, not an Examiner score. Examiner hold stays
`NOT_SCORED` and `stub_ready` stays false.
