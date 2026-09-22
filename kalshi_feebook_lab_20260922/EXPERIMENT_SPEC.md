# R1-P1 feebook: reciprocal YES/NO book and fee algebra

September 22, 2026. This file is the hypothesis. It is committed before source is
frozen and before any unit-test outcome is recorded. No profit figure in this
document is a result of this lab. Q1–Q6 outcomes that already exist are not
re-labeled as R1-P1 evidence.

Do not modify `nfl_factorial_lab_20260921`, `nfl_paircheck_lab_20260922`, the
prospective recorder, or any earlier frozen lab. This directory does not import
those modules.

## Placement

AGENTS.md says older experiment directories are evidence snapshots and new work
belongs in a new experiment version. Existing questions already live in
top-level directories (`nfl_queue_lab_20260921` through
`nfl_paircheck_lab_20260922`). Putting this pin under a new top-level lab
matches that pattern. The directory is `kalshi_feebook_lab_20260922` because
the question is venue book and fee algebra, not another NFL strategy arm.
That placement check is not a profitability claim.

## Question

Do the bids-only reciprocal identities and the order-level cent-ceiling fee
formula reproduce the pinned hand vectors and the transcribed general taker
table, and does a scorecard helper withhold the label `completed_profit` unless
the examiner fee channel is present?

This is a code-verification question. It is not a backtest, not a queue study,
and not live trading. R1-P5 rails are out of scope.

## Pin A — reciprocal bids-only book

Kalshi orderbooks return bids only. With prices in dollars:

```
ask_YES = 1 − best_NO_bid
ask_NO  = 1 − best_YES_bid
bid_YES = best_YES_bid
bid_NO  = best_NO_bid
spread_YES = ask_YES − bid_YES = 1 − best_NO_bid − best_YES_bid
spread_NO  = ask_NO − bid_NO   = 1 − best_YES_bid − best_NO_bid
```

Best bid is the highest dollar price on that side. Array order is not trusted.
Size at the touch is the summed fixed-point count at that price. A missing side
leaves the implied ask and the spread unset. No price is invented. A locked or
crossed book keeps a negative spread; it is not clamped.

The unit fixture is the public documentation example retrieved 2026-09-22 from
`https://docs.kalshi.com/getting_started/orderbook_responses`, stored in
`bids_only_fixture.json`. It is not a live capture. The documented top of book
is bid YES `0.4200`, bid NO `0.5600`, ask YES `0.4400`, ask NO `0.5800`, and
both spreads `0.0200`.

Taker polarity, from the hand-vector packet:

```
taker YES fills resting NO bids
taker NO  fills resting YES bids
```

The taker price is the implied ask on the taker's side. The resting maker price
is the best bid on the opposite side. Those two prices sum to 1. Fee algebra at
the touch does not mean the requested size is available, and it does not walk
deeper levels.

## Pin B — fee formula

Examiner channel, Claude-shaped, order-level:

```
raw = M × rate × C × P × (1 − P)
fee = round_up_to_cent(raw)          when round_up is true
fee = raw                            when round_up is false
fee = min(fee, 0.035 × C)            only if the series cap flag is on
                                     and round_up is true
```

| Role | rate |
|---|---|
| taker | 0.07 |
| maker | 0.0175 |

`round_up_to_cent` is `Decimal` quantize to `0.01` with `ROUND_CEILING`.
The packet's float description is `ceil(raw × 100 − eps) / 100` with
`eps = 1e-9`. That description is a comparator for the hand vectors. The
examiner implementation is the Decimal ceiling, because binary floating point
is not the pinned arithmetic.

`C` is the order contract count (fixed-point, positive). `P` is the contract
price in dollars on `[0, 1]`. `M` comes from the series stub. Partial fills
use `round_up=false` so a cent ceiling is not applied once per partial. The
uncapped order-level ceiling is then at most one cent above the unrounded
order raw. Summing per-partial ceilings can exceed that by more than one cent.
That excess is the reason partials stay unrounded.

The per-contract cap `0.035 × C` is the Claude optional flag. It is off in the
stub. It is not a row in the general taker table. When it is on, it is applied
after the cent ceiling on the order-level path only.

`series_fee_table.stub.json` default is `M = 1`, maker fees enabled, cap off,
overrides `{}`. Unknown series names resolve to that default and are marked
`default_unknown_series`. That mark is not evidence the live schedule uses
`M = 1`. Split maker and taker multipliers exist on the PDF; this stub has one
`M`. A caller may pass `taker_M` or `maker_M` on an override. Those keys are
absent from the committed stub.

Hand vectors in `fee_fixture_vectors.json` are the predeclared ceil checks.
`kalshi_general_fee_table.json` is a transcription of the PDF's general taker
table, not the PDF bytes.

Two PDF readings are predeclared disagreements, not silent merges:

1. The PDF prose says rounding makes `fee + positionCost` land on a centicent.
   The numeric table matches ceiling the fee itself to one cent. A centicent
   ceiling of the one-contract `$0.05` taker raw (`0.003325` → `0.0034`)
   disagrees with the table cell `$0.01`. The examiner follows the table and
   this pin. The centicent-of-sum reading is not implemented; `positionCost`
   is not defined here.
2. The PDF prose says the maker multiplier defaults to 0. The stub default is
   `M = 1` with maker fees enabled, matching the packet and the `KXNFLGAME`
   row (multipliers 1 and 1). Maker-off series are not copied into overrides.

Sibling repositories named in `SOURCE_PINS.json` were not retrieved (public
raw URLs returned 404). Their commits and paths are attribution. This lab does
not vendor their source and does not claim byte-identical ports.

## Claude versus Grok

| Aspect | Claude examiner | Grok comparator |
|---|---|---|
| Formula id | `astra.r1p1.feebook.claude_order_level_ceil.v1` | `grok.fees_ts.unrounded_per_unit.v1` |
| Contract count | Order-level `C` | Per unit, `C` implicit |
| Maker rounding | Cent ceiling when `round_up` | Unrounded |
| Cap | Optional `0.035 × C` after ceiling | None |

The Astra examiner completed-profit channel is the Claude-shaped id only.
The Grok unrounded maker quote is a paper comparator for later microstructure
comparison. It is not an examiner fee. At `P = 0.50` and `C = 1`, the
predeclared maker pair is examiner `0.01` versus Grok `0.004375`.

## Pin C — refuse gate

`classify_scorecard` returns `completed_profit` only when all of the following
hold:

- `kind` is not `extrapolation` (extrapolations return `projection`)
- `inventory_flat` is not `false` (unresolved inventory is not profit; a
  missing flag is not proof the inventory is flat)
- `fee_channel.taker_fee` and `fee_channel.maker_fee` are non-null
- `fee_channel.formula_id` equals the examiner id

Otherwise an execution row raises `CompletedProfitRefused`. A computed zero
fee is non-null. Float fees are rejected. The Grok formula id is rejected.

## Out of scope

Live orders, credentials, queue participation, R1-P5, book walking, the full
non-standard series table, and any change to frozen Q1–Q7 code or results.
`SOURCE_PINS.json` records queue and MICRO fields as context. This lab does
not implement them.

## What a later result file may say

After the source freeze, a result file may record whether the unit tests
passed and may repeat the limitations above. It may not report profit, may
not relabel Q6 development games, and may not treat this freeze as live
validation. `FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.
