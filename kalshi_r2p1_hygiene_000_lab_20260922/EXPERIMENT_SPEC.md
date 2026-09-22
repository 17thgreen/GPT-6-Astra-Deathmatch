# R2-P1 hygiene stress on Q6-000

September 22, 2026. This file is the hypothesis. It is committed before source is
frozen and before any unit-test outcome is recorded. No figure in this document
is a trading result. Q6 outcomes that already exist are not re-labeled as
evidence from this lab.

Conductor ADMIT R2-P1 is the measurement kernel. No separate Deep Research
packet was in this checkout. The pins below are that admission plus the frozen
feebook and rails labs already on main.

This lab relabels Q6-`000` measurement hygiene. It does not retune the `000`
signal, does not reopen capital arms A1/A2/A3, and does not start the
queue-fragility twin. Fee-treatment arms FS0/FS1/FS2 are not this experiment.
The fee question that remains is the examiner-versus-inherited delta below.

## Placement

`kalshi_feebook_lab_20260922` and `kalshi_rails_lab_20260922` are frozen
evidence snapshots. This lab imports those modules and does not edit them.
`kalshi_capital_structure_lab_20260922` and the Q1–Q7 directories stay
untouched. The new directory is `kalshi_r2p1_hygiene_000_lab_20260922`.

Fee path: `astra.r1p1.feebook.claude_order_level_ceil.v1`, commit
`22371178cb2663250b4762f328069571c48cb551`.

Queue, maker-credit, and content-fresh path:
`astra.r1p5.rails.maker_credit_floor_cent.v1` and `rails.judge_freshness`,
commit `6a28e0d6254327ea4e6451c781bec56215ac6cac`. Queue magnitudes are read
from `rails.scenario_queue`. They are fixed labels, not a knob.

## Question

Holding strategy Q6-`000`, the shared 5000 USD account, and the 31-game
development tape pointer, do the hygiene helpers do all of the following on
unit fixtures:

1. Re-score a fill's fee with R1-P1 `order_fee` round-up algebra and subtract
   the inherited Q6 fixed-point fee, without reading shadow fee literals.
2. Label maker admission with `maker_credit_floor_zero_refuse` from the R1-P5
   credit floor.
3. Label a book observation with `content_fresh_flag`, treating a keepalive as
   not fresh, and measure `freshness_gap_sec` from the last fresh observation.
4. Attribute `queue_ahead` to the pinned bins `q3300` and `q10000`, and flag a
   mismatch against the row's assumed scenario.

This is a code-verification question. It is not a Q6 tape walk and not live
trading. The three pre-settlement outputs stay null until a real fixture join.
`FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null. Unit tests may assert
helper arithmetic on synthetic rows. They may not invent walk P&L, and they
may not write those outputs into the freeze file.

## Constants

| Pin | Frozen value |
|---|---|
| Strategy pointer | Q6 label `000` |
| Shadow file | `nfl_factorial_lab_20260921/SHADOW_CANDIDATE_FREEZE.json` sha256 `b55ff36cb161c824a3d1b490795c8ac6891f01489456f61da311ac863366af48` |
| Tape manifest | `nfl_factorial_lab_20260921/inputs/manifest.json` sha256 `375ea6e2c9125a411d5444a88115213542d5b19c874d73a2bed0b9355fd6277d` |
| Cohort | 31 development events, read from `inputs/week_membership.json` |
| Account | Shared 5000 USD, status quo. Not a capital knob |
| Primary assumed queue label | `q3300` via `rails.scenario_queue` |
| Other assumed queue label | `q10000` via `rails.scenario_queue` |
| Examiner formula | `feebook.EXAMINER_FORMULA_ID` |
| Inherited model id | `q6.order_fees.fixed_point_balance.v1` |
| Empty outputs | `results/EMPTY_RESULTS.json` |

The shadow freeze file contains fee coefficients under its common config.
This lab does not read that object and does not copy those coefficients into
source. Examiner rates come only from `feebook.load_series_table` through
`feebook.order_fee`.

## Fee delta versus the inherited model

The inherited model is the Q6 fixed-point charge, reimplemented here so this
lab does not import or run `replay_v2`:

```
nominal = coefficient * C * P * (1 - P), ceiled to 0.000001
cash    = -C * P - nominal, floored to balance precision 0.0001
fee     = nominal + alignment remainder - accumulator rebate
```

The accumulator is per order identity and starts at zero. A later partial can
receive a rebate. The sum of partial charges on one fresh accumulator equals
one charge of the summed contracts. That identity is the inherited model. It
is not the examiner channel.

The examiner fee is `feebook.order_fee`:

- `round_up=True`: order-level cent ceiling (`ROUND_CEILING` to one cent).
  This is the rescore of a whole order.
- `round_up=False`: the unrounded raw order product. Partials use this path
  so a cent ceiling is not applied once per partial. That flag is the feebook
  pin. It is not a promotion arm and it is not the Grok comparator.

`fee_delta` is examiner fee minus inherited fee for the same role, price,
contracts, and rate. The inherited coefficient argument must equal the rate
`order_fee` resolved. A different coefficient is refused, so a shadow literal
cannot become a second rate source. The Grok unrounded per-unit id is not an
input to `fee_delta`. `classify_scorecard` still refuses that id for
`completed_profit`.

A positive delta means the examiner ceiling is larger than the inherited
fixed-point fee. The cohort key `fee_delta_vs_inherited_model` is the sum of
row deltas. That sum is a fee-hygiene statistic. It is not completed net, and
it is not subtracted from the shared 5000 USD account inside this lab.

## R1-P5 fill labels

`maker_credit_floor_zero_refuse` calls `rails.admit_maker_quote`. A
`MakerCreditRefused` is the label true. An admission is false. The rule id
stays `rails.FEE_CREDIT_RULE_ID`. Taker rows do not carry this label.

`content_fresh_flag` calls `rails.judge_freshness`:

```
keepalive true                         -> not fresh (keepalive_ignored)
previous absent and keepalive false    -> fresh (initial)
content differs                        -> fresh (content_changed)
transaction time differs               -> fresh (transaction_time_changed)
otherwise                              -> not fresh (unchanged)
```

A keepalive does not replace the previous book and does not move
`prior_fresh_at`. `freshness_gap_sec` on a row is `observed_at - prior_fresh_at`
in seconds. The first fresh observation has no prior anchor, so its gap is
null. The cohort output, when a fixture is joined, is the maximum non-null row
gap. Until that join the frozen output is null.

`queue_attribution_bin` is exact equality with `rails.scenario_queue`:

| Measured `queue_ahead` | Bin |
|---|---|
| `scenario_queue('q3300')` | `q3300` |
| `scenario_queue('q10000')` | `q10000` |
| anything else | `outside_pinned_bins` |

`queue_bin_mismatch` is true when that bin is not the row's assumed scenario.
The assumed scenario is only `q3300` or `q10000`. Both labels are read from
rails. This lab does not construct a third queue and does not vary fill
participation. The cohort key `queue_bin_mismatch_rate` is mismatches divided
by row count. Until a fixture join the frozen output is null.

## Pre-settlement outputs

These three keys are nullable until a real join of historical fills:

- `fee_delta_vs_inherited_model`
- `freshness_gap_sec`
- `queue_bin_mismatch_rate`

`pre_settlement_outputs` returns all three as null, with `results` and `pnl`
null, unless the caller passes `joined=True` and a non-empty labeled list.
That joined return is a synthetic fixture calculation. Its status is
`SYNTHETIC_FIXTURE_ONLY`. It still sets `results` and `pnl` to null. Nothing
in this lab writes it into `FROZEN_EXPERIMENT.json` or `EMPTY_RESULTS.json`.

`historical_completed_net` raises. A classifier label from
`feebook.classify_scorecard` is not stored as profit. There is no tape walker.

## Live orders

No live order client and no `KalshiExecutionAdapter`. `execution_adapter`
raises `LiveOrdersForbidden`.

## Left untouched

`kalshi_feebook_lab_20260922`, `kalshi_rails_lab_20260922`,
`kalshi_capital_structure_lab_20260922`, `nfl_factorial_lab_20260921`
(Q6 `000` included), `nfl_paircheck_lab_20260922`, the prospective recorder,
and the earlier Q labs. No signal retune. No capital redesign. No
queue-fragility twin. No inherited `common_config` fee literals in this lab's
source.

## What a later result file may say

After the source freeze, a result file may record whether the unit tests
passed and may repeat these limitations. It may not report profit, may not
relabel development games, and may not fill the three pre-settlement outputs.
`results`, `pnl`, `fee_delta_vs_inherited_model`, `freshness_gap_sec`, and
`queue_bin_mismatch_rate` in `FROZEN_EXPERIMENT.json` stay null until an
Examiner fixture join. A full Q6-`000` tape walk is out of this unit page.
