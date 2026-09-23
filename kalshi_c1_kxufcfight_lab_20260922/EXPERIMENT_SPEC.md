# C1 KXUFCFIGHT measurement: fee and queue honesty on ML binaries versus 000

September 23, 2026. This file is the hypothesis. It is committed before source
is frozen and before any unit-test outcome is recorded. No figure in this
document is a Kalshi trading result. Q1–Q6 outcomes that already exist are
not re-labeled as evidence from this lab.

Packet id: `C1-KXUFCFIGHT-MEAS`.

This directory is a unit scaffold for a fee-and-queue honesty bakeoff. The
two arms are schema-only KXUFCFIGHT moneyline binaries and the Q6 instrument
pointer `000`. The shared $5,000 figure is a measurement-contrast label on
both arms. It is not a strategy claim and it is not a retune of `000`.

## Conductor gate

Collector stub: `READY`.

`panel_version`: `2026-09-22.c1-kxufcfight-meas-v0`.

Clock admit: `NOT_ADMITTED`, awaiting `CLOCK_ADMIT_PASS`. The collector
being ready does not admit a settled panel. `clock_admit` raises on every
input, including a caller that passes the string `ADMIT_PASS`. An Examiner
pass is not this scaffold. `MZ` and `roi` have no successful path while that
admit is outstanding.

The original scaffold recorded Clock `REFUSED` at admitted settled N 0.
A later conductor update, recorded below, does not replace that admit rule.

`FROZEN_EXPERIMENT.json` keeps `results`, `pnl`, `MZ`, and `roi` null.
`results/EMPTY_RESULTS.json` keeps the same four fields null. A schema walk
does not fill either file. `winner` stays null. No fill is awarded.

## Conductor update — rejoin kicked, admit still closed

September 23, 2026, after the source freeze. The conductor reports that both
KXUFCFIGHT events are finalized and that settled N is 4. The clock re-join
is `KICKED`.

That report is a status pin. It is not a resolution file, not a fill, and
not a scorecard. This scaffold does not know which contracts settled, and it
does not store a yes or no result. Admitted settled N stays 0. `results`,
`pnl`, `MZ`, and `roi` stay null until a Clock `ADMIT_PASS` that this
checkout does not contain.

`fixtures/resolution_hook_not_admitted.json` is the placeholder path for a
later wiring of resolution fixtures. Its label is `NOT_ADMITTED`. It has
four slots, two events, and a null resolution on every slot.
`wire_resolution_hook` returns those slot ids with `resolutions_applied` 0.
`apply_resolutions` raises. A slot that already carries a resolution,
result, pnl, roi, or MZ is refused before any of those values is copied
into the return.

## Placement

`kalshi_feebook_lab_20260922` and `kalshi_rails_lab_20260922` are frozen
evidence snapshots. This lab imports those modules and does not edit them,
copy them, or vendor a second fee formula or a second queue rule. The
capital-structure lab, the hygiene lab, the queue-fragility lab, the examiner
lab, `kalshi_r3_p1_fee_cost_lab_20260922`, `kalshi_r3_p4_l2_shape_lab_20260922`,
and the Q1–Q7 directories stay untouched. The new directory is
`kalshi_c1_kxufcfight_lab_20260922`.

Fee path: `feebook.order_fee` with `round_up=True`, `feebook.polarity_fill`,
and `feebook.examiner_fee_channel`. Commit
`22371178cb2663250b4762f328069571c48cb551`. Formula
`astra.r1p1.feebook.claude_order_level_ceil.v1`.

Freshness path: `rails.judge_freshness`, `rails.canonical_book_content`, and
`rails.BookObservation`. Queue path: `rails.scenario_queue` for the labels
`q3300` and `q10000`. Maker-credit path: `rails.admit_maker_quote`. Commit
`6a28e0d6254327ea4e6451c781bec56215ac6cac`. Rule
`astra.r1p5.rails.maker_credit_floor_cent.v1`.

The maker and taker rates stay in the feebook series stub. This lab does not
restate them. Q6 and Q7 fee coefficients are not written here. The stub's
override map is empty. Series `KXUFCFIGHT` therefore resolves as
`default_unknown_series`. That mark is the honest reading of the stub. This
lab does not add a UFC fee-schedule override.

## Question

On schema-only synthetic books, does one harness do all of the following for
both the `KXUFCFIGHT` moneyline-binary arm and the `000` instrument arm:

1. Quote taker and maker fees through the imported feebook when native public
   `taker_*` fields are present, and leave the taker unset when they are absent.
2. Label book freshness and pinned queue bins through the imported rails.
3. Stamp both arms with the same shared $5,000 measurement-contrast label.
4. Refuse Lee-Ready, invented fills, a strategy port of `000`, and any
   scorecard that would fill `results`, `pnl`, `MZ`, or `roi`.

This is a code-verification question. It is not a backtest and not live
trading. `MZ` is the Mincer–Zarnowitz slot. `roi` is the return slot. Both
stay null while settled N is 0.

## Pin A — two arms, one measurement label

| Arm | Identity | Fee series argument |
|---|---|---|
| `KXUFCFIGHT` | Schema-only UFC fight moneyline binary | `KXUFCFIGHT` |
| `000` | Q6 instrument pointer, file `nfl_factorial_lab_20260921/SHADOW_CANDIDATE_FREEZE.json` sha256 `b55ff36cb161c824a3d1b490795c8ac6891f01489456f61da311ac863366af48` | none (`null`) |

The `000` pointer is the file hash. This lab does not parse that JSON, does
not read `common_config`, and does not read `starting_cash`. The shared
budget below is not copied out of that file.

```
measurement_budget_usd  = 5000
measurement_budget_role = measurement_contrast_label
strategy_claim          = false
```

Both arms carry that same label. A different budget on either arm is refused.
`spend_measurement_budget` raises. The label does not lock cash, does not
select a capital arm, and does not retune `000`. `port_strategy` and
`retune_000` raise. `winner` is null on the bakeoff return.

## Pin B — native public taker fields

Classification reads only these public trade fields, and only when one of
them is present:

| Field | Values |
|---|---|
| `taker_outcome_side` | `yes` or `no` |
| `taker_book_side` | `bid` (yes) or `ask` (no) |
| `taker_side` | legacy public `yes` or `no` |

`bid` and `yes` are the same directional bit on the public trade schema.
`ask` and `no` are the same bit. That equivalence is the venue's field
dictionary. It is not a quote-mid comparison.

Every present field must agree. If no native `taker_*` field is present,
`classify_taker` raises `TakerFieldRefused` and the book label leaves the
taker, the fee quotes, and the maker-credit label unset. An unknown
`taker_*` key raises. `is_taker`, `side`, and `action` do not classify a
trade.

The maker outcome side is the other side of the taker outcome, the resting
side in `feebook.TAKER_FILLS_RESTING`.

`lee_ready(...)` raises `LeeReadyRefused` on every input, including a row
that already has `taker_*` fields and including a price that sits above or
below a midpoint. A row that sets `lee_ready` true, or `classifier` to
`lee_ready`, raises inside `label_schema_row` before a fee is quoted. Quote
fields such as `mid`, `bid`, `ask`, and `prev_price` do not fill in a side.

## Pin C — fee-honest touch probe

When native taker fields agree, the probe is `feebook.polarity_fill` on the
row's bids-only `orderbook_fp`, with `round_up=True` and the arm's series
argument. Contract count is `schema_probe_contracts` (or `count_fp` when the
probe key is absent). The count is a schema probe. It is not an awarded fill.
`awarded_fill` on the label is null. `size_exceeds_touch` is the feebook
flag. It does not create a fill.

A missing bid leaves the implied ask unset. `feebook.BookIncomplete` is the
result. This lab does not invent the missing side as `1 − p` outside the
feebook, and it does not replace an incomplete book with a zero spread.

The two quotes pass through `feebook.examiner_fee_channel`. The Grok
unrounded comparator is not an input. `classify_scorecard` is not called on
the success path. A later unit check may show that the feebook would label
the examiner channel `completed_profit`. This lab does not copy that label
onto the scorecard.

The maker-credit label calls `rails.admit_maker_quote` at the resting maker
price and the same probe count. A `MakerCreditRefused` is recorded as
`maker_credit_floor_zero_refuse: true`. An admission is false on that flag.
The call does not place an order.

Rows that carry a non-null settlement or fill claim are refused before any
fee is quoted. The claim keys are `resolution`, `result`, `settled_result`,
`pnl`, `roi`, `MZ`, `mz`, `winner`, `band_roi`, `fill`, `filled`, `fills`,
`fill_count`, `awarded_contracts`, and `awarded_fill`.

## Pin D — rails freshness and queue labels

Freshness is `rails.judge_freshness` on `rails.canonical_book_content`:

```
keepalive true                         -> not fresh (keepalive_ignored)
previous absent and keepalive false    -> fresh (initial)
content differs                        -> fresh (content_changed)
transaction time differs               -> fresh (transaction_time_changed)
otherwise                              -> not fresh (unchanged)
```

A keepalive does not replace the previous book and does not receive a fee
probe. A refused Lee-Ready row or an invented-fill row does not move the
cursor.

Queue labels are exact equality with `rails.scenario_queue`:

| Measured `queue_ahead` | Bin |
|---|---|
| `scenario_queue('q3300')` | `q3300` |
| `scenario_queue('q10000')` | `q10000` |
| any other non-negative size | `outside_pinned_bins` |
| absent | null bin |

This lab does not construct a third queue and does not run a queue-fill
simulator. A schema row may carry `queue_ahead` with
`queue_ahead_role: schema_vector` and `queue_ahead_is_observation: false`.
That row checks the label function. It is not an observed UFC queue and it
is not an observed `000` queue. The shipped fixture rejects
`queue_ahead_is_observation: true`. Arm-level `observed_queue_ahead` and
`queue_bin_mismatch_rate` stay null.

## Pin E — schema-only fixture

`fixtures/schema_only_kxufcfight.json` is a field-shape sheet. Its header
says `SCHEMA_ONLY`, `admitted_settled_panel` false, collector `READY`,
clock `NOT_ADMITTED`, clock re-join `KICKED`, awaiting `CLOCK_ADMIT_PASS`,
reported settled N 4, admitted settled N 0, series `KXUFCFIGHT`, and the
panel version above. The rows are not an admitted panel, not captures, and
not fills. They have no resolution keys. `fixtures/PIN.md` says the same
thing. The reported count on the header is not a scorecard.

`walk_schema` labels both arms in memory. Its `results`, `pnl`, `MZ`, `roi`,
and `winner` are null. It does not write `FROZEN_EXPERIMENT.json` or
`results/EMPTY_RESULTS.json`.

## Out of scope

Live orders, credentials, and account endpoints. Lee-Ready and any other
trade-sign heuristic. Mincer–Zarnowitz coefficients. ROI. Invented fills and
invented resolutions. A UFC fee-schedule override. Copying the feebook or
the rails. Reading Q6 `common_config`. Retuning Q6 label `000`. Porting the
`000` strategy onto `KXUFCFIGHT`. Spending the $5,000 label. An Examiner
pass. Any change to frozen sibling labs.

## What a later result file may say

After the source freeze, a result file may record whether the unit tests
passed and may repeat these limitations. It may not report profit, may not
fill `MZ` or `roi`, may not name a winner, may not relabel development
games, and may not treat a schema row as a settled contract or a fill.
`results`, `pnl`, `MZ`, and `roi` stay null until a Clock `ADMIT_PASS`. This
scaffold does not obtain that pass. A unit file may say that the rejoin
hook loaded four empty slots. It may not fill those fields from the
reported settled N of 4.
