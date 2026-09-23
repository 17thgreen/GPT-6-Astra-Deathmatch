# R3-P3 favorite–longshot maker and taker

September 23, 2026. This file is the hypothesis. It is committed before source
is frozen and before any unit-test outcome is recorded. No figure in this
document is a Kalshi trading result. Q1–Q6 outcomes that already exist are
not re-labeled as evidence from this lab. Published maker and taker returns
are not evidence here.

Packet id: `R3-P3-FL-MAKER-TAKER`.

FL names the favorite–longshot question: public trades assigned to pinned
10¢ price bands, with the taker read from native public `taker_*` fields.
This directory is a unit scaffold. It is not a strategy, not a backtest, and
not an Examiner pass.

## Conductor gate

Collector stub: `READY`.

`panel_version`: `2026-09-22.r3-p3-fl-maker-taker-v0`.

Clock: `REFUSED`. Settled N is 0. The collector being ready does not admit a
settled panel. `clock_admit` raises. An Examiner pass is not this scaffold.

`FROZEN_EXPERIMENT.json` keeps `results`, `pnl`, `MZ`, and `band_roi` null.
`results/EMPTY_RESULTS.json` keeps the same four fields null. Schema checks
do not fill either file.

## Placement

`kalshi_feebook_lab_20260922` is a frozen evidence snapshot. This lab imports
that module and does not edit it, copy it, or vendor a second fee formula.
The rails lab, the capital-structure lab, the hygiene lab, the queue-fragility
lab, the examiner lab, `kalshi_r3_p1_fee_cost_lab_20260922`,
`kalshi_r3_p4_l2_shape_lab_20260922`, and the Q1–Q7 directories stay
untouched. The new directory is
`kalshi_r3_p3_fl_maker_taker_lab_20260922`.

Fee path: `feebook.order_fee` with `round_up=True`, and
`feebook.examiner_fee_channel` to pair the two role quotes. Commit
`22371178cb2663250b4762f328069571c48cb551`. Formula
`astra.r1p1.feebook.claude_order_level_ceil.v1`.

The maker and taker rates stay in the feebook series stub. This lab does not
restate them. Q6 and Q7 fee coefficients are not written here.

## Literature

The question is the maker/taker favorite–longshot panel in Constantin Burgi,
Wanying Deng, and Karl Whelan, "Makers and Takers: The Economics of the Kalshi
Prediction Market" (University College Dublin, January 2026). The paper's
bytes are not vendored. Its reported returns, including the maker return on
contracts priced at or above 50 cents (2.6 percent), are not recomputed, are
not a target, and are not a scorecard entry.

The paper's pre-2025 taker-only fee story is not the fee model. Fees in this
lab are the imported examiner feebook.

Lee and Ready (1991) is the refused trade-sign heuristic. The quote test and
the tick test have no successful path in this lab.

## Question

On schema-only public-trade rows, does the harness assign prices to the pinned
10¢ bands, classify the taker only from native public `taker_*` fields, join
taker and maker fees through the imported feebook, and refuse Lee-Ready,
rebinned edges, admission, and any scorecard that would fill `results`,
`pnl`, `MZ`, or `band_roi`?

This is a code-verification question. It is not a backtest and not live
trading. `MZ` is the Mincer–Zarnowitz slot. `band_roi` is the per-band return
slot. Both stay null while settled N is 0.

## Pin A — 10¢ bands

Registry id: `astra.r3p3.fl_maker_taker.price_bands_10c.v0`.

The file `price_bands_10c.v0.json` is the only edge table. Edges are absolute
dollar cuts of width `0.10`. They are not sample quantiles. They are not
refit after outcomes. `assign_band` reads this file. An `outcome` argument
raises `RebinRefused`.

| Band | Lo (inclusive) | Hi |
|---|---|---|
| b00 | 0.00 | 0.10 exclusive |
| b01 | 0.10 | 0.20 exclusive |
| b02 | 0.20 | 0.30 exclusive |
| b03 | 0.30 | 0.40 exclusive |
| b04 | 0.40 | 0.50 exclusive |
| b05 | 0.50 | 0.60 exclusive |
| b06 | 0.60 | 0.70 exclusive |
| b07 | 0.70 | 0.80 exclusive |
| b08 | 0.80 | 0.90 exclusive |
| b09 | 0.90 | 1.00 inclusive |

A price outside `[0, 1]` is an error. Floats are rejected. The band of a
printed price does not depend on a resolution.

## Pin B — native public taker fields

Classification reads only these public trade fields:

| Field | Values |
|---|---|
| `taker_outcome_side` | `yes` or `no` |
| `taker_book_side` | `bid` (yes) or `ask` (no) |
| `taker_side` | legacy public `yes` or `no` |

`bid` and `yes` are the same directional bit on the public trade schema.
`ask` and `no` are the same bit. That equivalence is the venue's field
dictionary. It is not a quote-mid comparison.

Every present field must agree. A missing value is absent. If no native
`taker_*` field is present, classification raises `TakerFieldRefused`.
An unknown `taker_*` key raises as well. `is_taker`, `side`, and `action`
are not public `taker_*` fields and do not classify a trade.

The maker outcome side is the other side of the taker outcome, the resting
side in `feebook.TAKER_FILLS_RESTING`. That polarity is the public trade
identity. It is not Lee-Ready.

`lee_ready(...)` raises `LeeReadyRefused` on every input, including a row
that already has `taker_*` fields and including a price that sits above or
below a midpoint. A row that sets `lee_ready` true, or `classifier` to
`lee_ready`, raises `LeeReadyRefused` inside `classify_taker`. Quote fields
such as `mid`, `bid`, `ask`, and `prev_price` are ignored when native
`taker_*` fields already classify the row, and they do not fill in a side
when those fields are absent.

## Pin C — fee join

`join_fees` classifies the row, then reads `yes_price_dollars` and
`no_price_dollars`. Both are required. They are `Decimal`, `int`, or `str`.
Floats are rejected. The two prices must sum to 1. A missing side is not
invented as `1 − p`.

The taker price is the dollar price of `taker_outcome_side`. The maker price
is the other printed price. Contract count is `count_fp` (or `count` when
`count_fp` is absent). If both counts are present they must be equal. The
count must be positive.

```
taker_quote = feebook.order_fee('taker', contracts, taker_price, round_up=True)
maker_quote = feebook.order_fee('maker', contracts, maker_price, round_up=True)
channel     = feebook.examiner_fee_channel(taker_quote, maker_quote)
```

`series` is passed through when the row has one. The returned row carries the
two quotes, the channel formula id, the two band ids, and null `results`,
`pnl`, `MZ`, and `band_roi`. No sum of fees is a profit. `classify_scorecard`
is not called on the success path. A later unit check may show that the
feebook would label the examiner channel `completed_profit`. This lab does
not copy that label onto the scorecard. `scorecard_refuse` raises
`ScorecardRefused`.

A row that carries a non-null `resolution`, `result`, `outcome`, `pnl`,
`roi`, `MZ`, or `band_roi` is refused before any fee is quoted.

## Pin D — schema-only fixture

`fixtures/schema_only_public_trades.json` is a field-shape sheet. Its header
says `SCHEMA_ONLY`, `admitted_settled_panel` false, collector `READY`, clock
`REFUSED`, settled N 0, and the panel version above. The rows are not an
admitted panel, not captures, and not fills. They have no resolution keys.

| `schema_id` | What the harness does |
|---|---|
| `schema_yes_bid` | `taker_outcome_side=yes`, `taker_book_side=bid`, prices 0.40 and 0.60. Taker band b04. Maker band b06. |
| `schema_no_ask` | `taker_outcome_side=no`, `taker_book_side=ask`, prices 0.25 and 0.75. Taker band b07. Maker band b02. |
| `schema_legacy_taker_side` | Only legacy `taker_side=yes`, prices 0.10 and 0.90. Taker band b01. Maker band b09. |
| `schema_missing_taker` | Prices present. No `taker_*` field. `TakerFieldRefused`. No side. |
| `schema_taker_fields_disagree` | `taker_outcome_side=yes` with `taker_book_side=ask`. Refused. No side. |

`walk_schema` joins the three classified rows and records the two refusals.
The walk's `results`, `pnl`, `MZ`, and `band_roi` are null. It does not
write `FROZEN_EXPERIMENT.json` or `results/EMPTY_RESULTS.json`.

## Out of scope

Live orders, credentials, and account endpoints. Lee-Ready and any other
trade-sign heuristic, including a path that would succeed. Mincer–Zarnowitz
coefficients. Per-band ROI. Invented resolutions and invented fills. Rebinning
after outcomes. Copying the feebook or writing Q6/Q7 fee literals. Retuning
Q6 label `000`. Using the published 2.6 percent maker return as evidence.
An Examiner pass. Any change to frozen sibling labs.

## What a later result file may say

After the source freeze, a result file may record whether the unit tests
passed and may repeat these limitations. It may not report profit, may not
fill `MZ` or `band_roi`, may not relabel development games, and may not treat
a schema row as a settled contract. Those four scorecard fields stay null
until an Examiner pass. This scaffold does not run that pass.
