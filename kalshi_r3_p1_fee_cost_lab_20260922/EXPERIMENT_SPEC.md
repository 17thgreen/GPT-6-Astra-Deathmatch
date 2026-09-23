# R3-P1 fee_cost versus the R1-P1 fee model

September 23, 2026. This file is the hypothesis. It is committed before source
is frozen and before any unit-test outcome is recorded. No figure in this
document is a trading result. Q1–Q6 outcomes that already exist are not
re-labeled as R3-P1 evidence.

Packet id: `R3-P1-FEE-COST-VS-MODEL`.

This is an accounting instrument. It compares the closed-form R1-P1 fee model
with the exchange-reported fee on synthetic fill rows. It does not choose
markets, size orders, retune Q6 label `000`, or report strategy profit.

## Placement

`kalshi_feebook_lab_20260922` is a frozen evidence snapshot. R3-P1 imports
that module and does not edit it, copy it, or vendor a second fee formula.
`kalshi_rails_lab_20260922`, `kalshi_capital_structure_lab_20260922`,
`kalshi_r2p1_hygiene_000_lab_20260922`, `kalshi_queue_fragility_000_lab_20260922`,
and the Q1–Q7 directories stay untouched. The new directory is
`kalshi_r3_p1_fee_cost_lab_20260922`.

The fee model is the examiner channel
`astra.r1p1.feebook.claude_order_level_ceil.v1` at commit
`22371178cb2663250b4762f328069571c48cb551`.

## Question

On synthetic Kalshi Fill-shaped rows, does the harness compute
`fee_model` from the imported examiner `order_fee`, keep the row's
`fee_cost` and `is_taker`, and score `fee_model_minus_venue_delta`, and does
it refuse a completed-net claim that used the model alone when `fee_cost`
was available?

This is a code-verification question. It is not a backtest and not live
trading. `FROZEN_EXPERIMENT.json` keeps `results`, `pnl`, and
`fee_model_minus_venue_delta` null.

## Pin A — imported fee model

Call `feebook.order_fee` with `round_up=True`. Do not reimplement the ceiling.
Do not read the Grok comparator as an accounting fee. Do not write the taker
or maker coefficients into this lab. `M`, the role rate, and the cent ceiling
come from the imported feebook and its series stub.

```
fee_model = round_up(M × rate × C × P × (1 − P))
```

`round_up` is the examiner `Decimal` quantize to one cent with `ROUND_CEILING`.
`C` is the fill contract count. `P` is the dollar price of the filled side on
`[0, 1]`. Role is `taker` when `is_taker` is true and `maker` when it is false.
The rate is the feebook rate for that role. Partials left unrounded are the
feebook's own order path; this instrument scores the closed-form order-level
ceiling only.

`examiner_fee_channel` and `classify_scorecard` are the examiner gate. A
scorecard the feebook would label `completed_profit` is still not a
completed net in this lab. See Pin D.

## Pin B — venue fee on a Fill-shaped row

Units read fixture rows. They do not call a portfolio endpoint, do not
authenticate, and do not place orders.

Required fields:

| Field | Rule |
|---|---|
| `is_taker` | JSON boolean. Missing or non-boolean is an error. |
| `side` | `yes` or `no`. |
| `count_fp` and/or `count` | Positive contract count. `Decimal`, `int`, or `str`. Floats are rejected. If both are present they must be equal. |
| price of `side` | `yes_price_dollars` or `no_price_dollars` for that side. The missing side is not invented. If both prices are present they must sum to 1. |
| `fee_cost` | The key is required. JSON `null` means the venue fee was not reported. A string, int, or `Decimal` is a reported venue fee, including zero. Floats and negatives are rejected. |

`fee_cost` is dollars, the synthetic stand-in for the Kalshi Fill fixed-point
field. A reported zero is present. It is not treated as null.

These rows are synthetic. They are not live captures.

## Pin C — delta and preference

When `fee_cost` is non-null:

```
fee_model_minus_venue_delta = fee_model − fee_cost
preferred fee = fee_cost
preferred source = venue
```

When `fee_cost` is null:

```
fee_model_minus_venue_delta = null
preferred source = model_only
```

A null venue fee is not scored as a zero delta. The model fee may be shown as
a projection fee. It is not an accounting completion. Arithmetic is `Decimal`.

The predeclared fixture cases, in `fixtures/synthetic_fills.json` once source
is frozen, are:

| `case_id` | Role | Venue fee |
|---|---|---|
| `venue_match_taker` | taker | present and equal to `fee_model` |
| `venue_mismatch_taker` | taker | present and different from `fee_model` |
| `venue_mismatch_subcent_taker` | taker | present and not equal to `fee_model` |
| `venue_match_maker` | maker | present and equal to `fee_model` |
| `venue_mismatch_maker` | maker | present, including a reported zero |
| `venue_null_taker` | taker | null |
| `venue_null_maker` | maker | null |
| `venue_match_taker_c100` | taker | present and equal to `fee_model` |
| `venue_mismatch_maker_c1000` | maker | present and different from `fee_model` |

Match and mismatch are properties of `fee_model − fee_cost` after the import,
not a second formula. Taker and maker rows share contract counts and prices
only where the case table says so; the role still selects the feebook rate.

An aggregate of non-null row deltas may be returned by the harness for a unit
check. That aggregate is not profit. The freeze file does not store it.
`results` and `pnl` on every harness return stay null.

## Pin D — refuse model-only completed net

`classify_scorecard` is necessary and not sufficient.

Build the examiner channel with `examiner_fee_channel` from the fill's
`order_fee` quote and a counterpart quote for the other role. The counterpart
exists so the examiner channel has both a taker fee and a maker fee. It is not
a second venue fee and it is not a profit.

Then:

- `kind = extrapolation` stays `projection`. Model-only projection is allowed
  whether or not `fee_cost` was reported. The projection fee is `fee_model`.
  It does not replace a reported `fee_cost` as the preferred accounting fee.
- `kind = execution` asks for a completed net. If `fee_cost` is null, refuse.
  Model-only is not a completed net.
- `kind = execution` with `fee_cost` present and fee basis `model`, refuse,
  even when `classify_scorecard` returns `completed_profit`.
- `kind = execution` with `fee_cost` present and fee basis `venue` binds the
  accounting fee to `fee_cost`. The label is `venue_fee_bound`. `results` and
  `pnl` stay null. No completed-net dollars are emitted.
- Unresolved inventory still raises the feebook `CompletedProfitRefused`.
  A non-examiner counterpart quote still fails inside `examiner_fee_channel`.

The refusal is the honesty rule: do not claim a completed net from the
closed-form model when the fill already carried `fee_cost`.

## Out of scope

Live orders, credentials, portfolio reads, queue participation, R1-P5 rails,
capital arms, Q6 label `000` retune, Q7 fee literals written into this lab,
book walking, and any change to frozen sibling labs. Naked copies of the
feebook rates are forbidden. Profit is not invented to fill a null.

## What a later result file may say

After the source freeze, a result file may record whether the unit tests
passed and may repeat the limitations above. It may not report profit, may
not relabel Q6 development games, and may not treat this freeze as live
validation. `FROZEN_EXPERIMENT.json` keeps `results`, `pnl`, and
`fee_model_minus_venue_delta` null.
