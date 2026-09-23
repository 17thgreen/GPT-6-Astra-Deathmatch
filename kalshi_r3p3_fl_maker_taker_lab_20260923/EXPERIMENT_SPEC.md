# R3-P3 FL maker/taker + favorite–longshot bands harness

September 23, 2026. This file is the hypothesis. It is committed before source
is frozen and before any unit-test outcome is recorded. No figure in this
document is a trading result. Q6 outcomes that already exist are not re-labeled
as evidence from this probe. This is a measurement-only maker/taker and
favorite–longshot bands harness. It is not a strategy, not paper EV, and not
a Lee-Ready aggressor sign.

## Placement

The canonical harness freeze is
`R3_P3_FL_MAKER_TAKER_HARNESS_FREEZE_2026-09-23.md`, sha256
`fbc58539b7a469d005b7f75b786efddecc1028a3bb0da601bc0082c9d4aab179`.
The parent kernel is
`R3-P3_FL_MAKER_TAKER_BANDS_FREEZE_KERNEL_2026-09-22.md`, sha256
`0ed697149136acb3aa840aeeb79d11c8f6ef80f37ce4dd692a3cb690212206a7`.
`EXPERIMENT_SPEC.md` is the lab hypothesis. It is not a second freeze.

`lab/governance/astra/packets/` is not in this checkout. Packet copies sit
beside the engine and under `packets/`:

| Copy | Path |
|---|---|
| Harness freeze | `kalshi_r3p3_fl_maker_taker_lab_20260923/R3_P3_FL_MAKER_TAKER_HARNESS_FREEZE_2026-09-23.md` |
| Parent kernel | `kalshi_r3p3_fl_maker_taker_lab_20260923/R3-P3_FL_MAKER_TAKER_BANDS_FREEZE_KERNEL_2026-09-22.md` |
| Lab bundle | `kalshi_r3p3_fl_maker_taker_lab_20260923/R3_P3_FL_MAKER_TAKER_HARNESS/` |
| Governance freeze | `packets/R3_P3_FL_MAKER_TAKER_HARNESS_FREEZE_2026-09-23.md` |
| Governance kernel | `packets/R3-P3_FL_MAKER_TAKER_BANDS_FREEZE_KERNEL_2026-09-22.md` |
| Governance bundle | `packets/R3_P3_FL_MAKER_TAKER_HARNESS/` |

`FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.
`results/EMPTY_RESULTS.json` keeps `mz_alpha`, `mz_psi`,
`post_fee_roi_by_band`, `maker_vs_taker_roi_delta`, and `settled_join_n`
null.

Panel stub: `lab/astra-capture/r3-p3-fl-maker-taker/panel_stub.json`,
`panel_version` `2026-09-22.r3-p3-fl-maker-taker-v0`, sha256
`6f640dd3a6091ba6b896ded38fdded4676583aa3c885223da21ddf03780250c0`.
`admitted_at` is null. The stub records 15 public trades, native taker
fields on every row, and `settled_markets_resolved_n` 0. That cohort count
is a property of the stub. It is not a fill of the scorecard field
`settled_join_n`, which stays null.
`panel_admitted.json` is not in this freeze. When that file appears later,
the harness prefers it and still refuses a non-null scorecard.

Bands registry, pre-registered before outcome join:
`lab/astra-capture/r3-p3-fl-maker-taker/bands_registry_10c.json`, sha256
`0860cbe28d28ecc6142ddf6f1ebb67792084264ed82e0b4d868c3b3138ea5312`,
registry id `astra.r3p3.fl_maker_taker.price_bands_10c.v0`.
`measurement_roi_by_band` on that file is null.

Fee path, fixed: `kalshi_feebook_lab_20260922` at
`22371178cb2663250b4762f328069571c48cb551`. The harness imports that
module for the examiner formula id. Fee objects are schema only. Numeric
fees are not stored. ROI stays null.

Rails path, optional freshness pin, fixed:
`kalshi_rails_lab_20260922` at
`6a28e0d6254327ea4e6451c781bec56215ac6cac`. Freshness is not a scorecard
field of this harness. The rails tree is not edited.

Shadow fee literals `0.0175` and `0.07` are forbidden in the harness source.
Rates come from the imported feebook table when a probe quote is built, and
that quote is not copied onto the scorecard.

C3 and C5 stay as merged at `637644966bae3737b52ab35826d3a63bf4b9b936`.
This pulse does not edit them. Weather preference on the stub is a cite.
Kernels stay distinct. Queue-fragility is not loaded. `admit.py` is not run.

## One knob

Analysis slice only.

| Arm | Slice |
|---|---|
| R3P3A0 | `maker_vs_taker` |
| R3P3A1 | `fl_bands_10c` |

Both arms share the feebook pin and the bands registry. Fee is not a knob.
Lee-Ready is not an arm.

### R3P3A0 maker versus taker

Partition loaded trades by the native pair
(`taker_outcome_side`, `taker_book_side`). Allowed outcome values are
`yes` and `no`. Allowed book values are `bid` and `ask`. When the
deprecated alias `taker_side` is present it must equal
`taker_outcome_side`. `taker_action` is not a side field and must stay
null. `aggressor_inference` must stay null. `lee_ready` on each trade must
be the string `REFUSED`.

The partition records those native fields, the trade ids, and a fee-schema
object. It does not invent a maker aggressor label, a quote-midpoint sign,
or a tick test. Calling the harness aggressor helper raises a refusal.
The maker role of a later Examiner comparison is not computed here.

On the frozen stub prices and sides, the native pairs are `no`/`ask` (13
trades) and `yes`/`bid` (2 trades). That count is a property of the stub
fields. It is not ROI.

### R3P3A1 favorite–longshot bands

Assign `yes_price_dollars` to exactly one pre-registered band. Bounds and
inclusivity come from the registry file:

| Band | Interval |
|---|---|
| b00 | `[0, 0.10)` |
| b01 | `[0.10, 0.20)` |
| b02 | `[0.20, 0.30)` |
| b03 | `[0.30, 0.40)` |
| b04 | `[0.40, 0.50)` |
| b05 | `[0.50, 0.60)` |
| b06 | `[0.60, 0.70)` |
| b07 | `[0.70, 0.80)` |
| b08 | `[0.80, 0.90)` |
| b09 | `[0.90, 1.00]` |

`0.10` belongs to b01. `0.90` and `1` belong to b09. A price outside
`[0, 1]`, or a price that matches two bands, is refused. The harness does
not rebin after looking at outcomes. There are no settled outcomes on the
stub.

The stub `yes_price_dollars` values are `0.0100` (5 trades, b00),
`0.9800` (2 trades, b09), and `0.9900` (8 trades, b09). Bands b01 through
b08 are empty on the stub. Empty membership is not a ROI of zero. Each
band still carries a fee-schema object and a null `post_fee_roi`.

`fixtures/synthetic_trades.json` may exercise other bands in memory. That
file is labeled `synthetic_schema_standin`. It is not a panel fill, not a
settlement, and it does not write the freeze scorecard.

## Question

Holding the R1-P1 feebook fixed and Lee-Ready refused, does one harness do
all of the following on a code check:

1. Load `panel_stub.json` at `panel_version`
   `2026-09-22.r3-p3-fl-maker-taker-v0` with `admitted_at` null, 15 trades,
   and stub `settled_markets_resolved_n` 0. Prefer `panel_admitted.json`
   when that file is present. Refuse a different panel version, a live-order
   route, a paper-EV flag, a non-null settlement, and a non-null ROI field.
2. Load the pre-registered 10¢ bands registry and refuse a registry whose
   bounds, ids, or null ROI field do not match the pin. Bind fees through
   `kalshi_feebook_lab_20260922` at the commit above. Do not edit that
   module. Do not store a numeric fee on the scorecard. Pin the rails
   commit without making freshness a knob.
3. Emit R3P3A0 schema: native taker partitions only, Lee-Ready refused,
   fee-schema objects per partition, ROI null. Emit R3P3A1 schema: one
   object per registry band, membership from `yes_price_dollars`,
   fee-schema objects per band, ROI null. Both arms share the fee pin.
4. Leave `mz_alpha`, `mz_psi`, `post_fee_roi_by_band`,
   `maker_vs_taker_roi_delta`, `settled_join_n`, `results`, and `pnl` null
   in `FROZEN_EXPERIMENT.json` and `results/EMPTY_RESULTS.json`. The
   scorecard `settled_join_n` stays null even though the stub cohort count
   of resolved markets is 0. The harness does not invent settlements.

This is a code-verification question. It is not a tape walk, not a
Q6-`000` retune, and not live trading. The strategy pointer is null.
Capture, when a later collector runs, is GET-only on the public elections
host. This harness does not place orders and does not open a network client.
No Logan key is required.

## Scorecard

Until Examiner opens the packet after Clock admit, each of these keys is
present and null:

| Field | Meaning while null |
|---|---|
| `mz_alpha` / `mz_psi` | Mincer–Zarnowitz event-clustered coefficients |
| `post_fee_roi_by_band` | R1-P1 post-fee ROI by 10¢ band |
| `maker_vs_taker_roi_delta` | Native-field maker versus taker ROI delta |
| `settled_join_n` | Count of settled resolved markets joined |
| `results` / `pnl` | Null in this freeze |

`write_scorecard` does not write these fields. A non-null value is refused.
A null payload is also refused, so the freeze files stay as committed.
An in-memory feebook probe checks the formula id. It is not a copy into
`post_fee_roi_by_band` or `maker_vs_taker_roi_delta`.

## Do-not

1. No live orders, no signed trading host, and no Logan keys.
2. No Lee-Ready and no invented aggressor side.
3. No invented settled outcomes and no invented ROI.
4. No paper +2.6% and no author PnL as Astra evidence. The paper
   maker-at-or-above-50¢ claim stays a hypothesis.
5. No Q6-`000` retune, no queue-fragility reopen, and no Cap-SR reopen.
6. No C3 or C5 admit steal. Do not run `admit.py`. Do not edit the C3 or
   C5 labs.
7. No inherited fee literals in the harness source.
8. No rebin of the 10¢ registry after outcomes.
9. Do not edit the feebook, rails, capital, Cap-SR, C3, C5, or Q trees.

## Empty results

`results/EMPTY_RESULTS.json`, the lab bundle `results.json`, and
`packets/R3_P3_FL_MAKER_TAKER_HARNESS/results.json` stay
`EMPTY_RESULTS_PRE_EXAMINER` with the five instrument fields, `results`,
and `pnl` null.
