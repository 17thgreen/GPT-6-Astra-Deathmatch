# R1-P5 rails: queue, fee-credit, and book freshness

September 22, 2026. This file is the hypothesis. It is committed before source is
frozen and before any unit-test outcome is recorded. No figure in this document
is a trading result. Q1–Q6 outcomes that already exist are not re-labeled as
R1-P5 evidence.

This lab measures queue attribution, maker-fee admission, and book freshness.
It does not choose markets, size a book, or report strategy ROI.

## Placement

`kalshi_feebook_lab_20260922` is a frozen evidence snapshot. Its
`FROZEN_EXPERIMENT.json` hashes `feebook.py` and its tests. R1-P5 imports that
module and does not edit it. Q1–Q7 directories stay untouched. The new
directory is `kalshi_rails_lab_20260922`.

The fee path is the merged examiner:
`astra.r1p1.feebook.claude_order_level_ceil.v1`, commit
`22371178cb2663250b4762f328069571c48cb551`.

## Question

Do a Claude-shaped queue instrument, a venue-rounded maker-credit floor, and a
content-fresh book predicate reproduce the pins below on unit inputs, and does
a MICRO_V1 scorecard helper keep the declared verdict order and evidence stage?

This is a code-verification question. It is not a backtest and not live
trading. `FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.

## Pin A — queue and fill

Source read at the pinned tip, not vendored:
`src/flatstake/paper/execution.py` blob
`8d9827657001aac6a3dfc2ffdc84f0bf121f0310` on
`11e00f182e0fa1f97ed80eb69fec1269d43d8f5a`.

| Setting | Value | Role |
|---|---|---|
| `queue_ahead_contracts` | 3300 | Default measured queue ahead |
| `fill_participation` | 0.5 | Share of post-queue volume awarded |
| `queue_model` | `measured` or `front` | `front` is the optimistic bound, 0 ahead |
| Stress ahead | 10000 | Same `measured` model with a larger ahead value |
| Scenario labels | `q3300`, `q10000` | Magnitudes used on the Q1–Q6 grid |

`front` ignores a supplied book size and uses 0. `measured` uses a supplied
non-negative book size when the caller passes one, and otherwise uses the
configured ahead value. A supplied 0 is an observed empty level. It is not the
`front` model.

Contracts, prices, sizes, and participation are `Decimal`, `int`, or `str`.
Floats are rejected, matching the feebook. Participation must lie in `(0, 1]`.
Ahead must be `>= 0`.

Polarity, the same map as `feebook.TAKER_FILLS_RESTING`:

```
taker_side "yes" fills our resting NO
taker_side "no"  fills our resting YES
```

A trade is compared with the price of our outcome. The NO price is the trade's
`no_price` when present, otherwise `1 - yes_price`. If both are present they
must sum to 1. A trade whose outcome price is strictly above our bid does not
consume queue and does not fill. A trade at or through our bid can fill, and
the fill price is our bid.

Given remaining size `R`, queue ahead `Q`, trade volume `V`, participation `p`:

```
consumed = min(Q, V)
Q := Q - consumed
post = V - consumed
fill = min(R, post * p)
```

A zero fill leaves the order resting and charges no fee. A positive fill of
`got` contracts charges the feebook partial maker path:

```
order_fee('maker', got, our_price, round_up=False)
```

That fee is the unrounded raw. The order-level cent ceiling is not applied on
the fill. One trade updates at most the polarity-matched order.

Same-price keep, from the pinned `replace_quotes`:

- The unfilled remainder is `size - filled`.
- A later maker intent with the same ticker, outcome, and price, while that
  remainder is positive, keeps `queue_ahead`. Resting size becomes the
  remainder. Filled resets to 0. The new intent's size is not adopted.
- A new price, a missing prior order, or a fully filled prior order is a new
  order at the back: `queue_ahead` is the model queue, and the size is the new
  intent's size.
- An omitted key is cancelled.
- A `taker` intent is not rested.

Fee-credit admission (Pin B) runs against the whole replacement set before the
resting map changes. A refusal leaves the previous map in place.

This instrument has no live order type and no flatten/cross helper. Those
paths stay out of this directory.

## Pin B — fee-credit floor

A maker quote of `C` contracts at price `P` is admitted only after the venue
fee is subtracted and the net is floored to one cent.

```
fee     = order_fee('maker', C, P, round_up=True).fee
net     = P * C - fee
credit  = net.quantize(0.01, ROUND_FLOOR)
```

`round_up=True` is the examiner cent ceiling. The rule id is
`astra.r1p5.rails.maker_credit_floor_cent.v1`. It is not an examiner
completed-profit channel.

Refuse when `credit <= 0`. A positive net that is still below one cent floors
to `0.00` and is refused. The cash identity `P * C` with the fee omitted is
the fee-blind quote; this pin refuses the case where that blind cash floors
above zero and the venue-rounded credit does not.

Predeclared rows, default series stub (`M = 1`, maker fees on):

| C | P | Venue maker fee | Net | Floored credit | Decision |
|---|---|---|---|---|---|
| 1 | 0.50 | 0.01 | 0.49 | 0.49 | admit |
| 1 | 0.02 | 0.01 | 0.01 | 0.01 | admit |
| 1 | 0.015 | 0.01 | 0.005 | 0.00 | refuse |
| 1 | 0.01 | 0.01 | 0.00 | 0.00 | refuse |

At `C = 1`, `P = 0.01`, the fee-blind cash is `0.01`. The rail refuses.

A series override that disables maker fees evaluates a zero fee and can admit
a positive price. The zero is the evaluated fee, recorded on the quote. The
partial-fill path in Pin A stays on `round_up=False` and is separate from
admission.

## Pin C — content-fresh book predicate

Freshness is a change in canonical book content or in the venue transaction
time. A websocket keepalive is not a book update. This pass is the predicate
only. There is no collector, socket client, or clock loop.

```
keepalive true                         -> not fresh (keepalive_ignored)
previous absent and keepalive false    -> fresh (initial)
content differs                        -> fresh (content_changed)
transaction time differs               -> fresh (transaction_time_changed)
otherwise                              -> not fresh (unchanged)
```

Canonical content is the SHA-256 of JSON with sorted keys. Key order alone
does not change the token. `received_at` is not an argument. Two observations
with the same content and the same transaction time stay unchanged however far
apart a local clock sits.

## Pin D — MICRO_V1 scorecard shape

Config pin: `grok_config_MICRO_V1.json`.

| Field | Value |
|---|---|
| taker rate | 0.07, one-lot examiner cent ceiling |
| maker rate | 0.0175, Grok unrounded per unit |
| `thinN` | 500 |
| `surviveRoi` | 0 |
| `skipBlockTrades` | true |
| `nflInplayHours` | 3.25, stored, not a kickoff model |
| Verdicts | `SURVIVES`, `FAILS`, `THIN`, `CONTROL` |
| Evidence stage | `HISTORICAL_OUT_OF_SAMPLE` only |

Verdict order, for one role on one print set:

1. `kind == control` returns `CONTROL`, including when `n < thinN` and when
   ROI is positive.
2. `n < thinN` returns `THIN`.
3. A null ROI returns `FAILS`.
4. `SURVIVES` when ROI is strictly greater than `surviveRoi` and either the
   counterpart ROI is null or ROI is strictly greater than the counterpart ROI.
5. Otherwise `FAILS`.

Each print is scored as one role, maker or taker. The score object carries
both the one-lot ROI (`net / n`, one contract per print) and the size-weighted
ROI (`sum(profit * size) / sum(size)`). The one-lot figure treats the print as
a unique counterparty and overstates executable size; the size-weighted figure
is reported beside it. Block prints are dropped when `skipBlockTrades` is
true.

Role cash on one contract, price `P` equal to the taker's outcome price:

```
taker wins when the taker side matches the settlement result
taker: fee = order_fee('taker', 1, P).fee
       gross = (1 - P) if the taker wins else -P
maker: fee = grok_unrounded_maker_per_unit(P).fee
       gross = (P - 1) if the taker wins else P
profit = gross - fee
```

Any evidence stage other than `HISTORICAL_OUT_OF_SAMPLE` is rejected. Picker
fields on the config (`longshotMax`, `favoriteMin`, `favoriteMax`,
`weatherCheapMax`) are stored and are not applied. This helper does not run a
tape and does not call `classify_scorecard`.

## Left untouched

`nfl_factorial_lab_20260921` (Q6 `000` included), `nfl_paircheck_lab_20260922`
arms A–D, the prospective recorder, the earlier Q labs, `kalshi_feebook_lab_20260922`
source, HX spread selection, weather cheap-YES selection, directional pickers,
and event YES/YES netting. No live order client is added.

## What a later result file may say

After the source freeze, a result file may record whether the unit tests
passed and may repeat these limitations. It may not report profit, may not
relabel development games, and may not mark an Examiner pass complete.
`results` and `pnl` in `FROZEN_EXPERIMENT.json` stay null.
