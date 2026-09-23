# C3-KXHIGHNY bordering-strike weather ladder

September 23, 2026. This file is the hypothesis. It is committed before source
is frozen and before any unit-test outcome is recorded. No figure in this
document is a Kalshi trading result. Q1–Q6 outcomes that already exist are
not re-labeled as evidence from this lab. Published weather returns are not
evidence here.

Packet id: `C3-KXHIGHNY-MEAS`.

This directory is a null-scorecard simulator scaffold for adjacent strikes on
the daily-high ladders `KXHIGHNY` and `KXHIGHCHI`. It is not a strategy, not
a backtest, and not an Examiner pass.

## Conductor gate

Collector stub: `READY`.

`panel_version`: `2026-09-23.c3-kxhighny-meas-v0`.

Clock: `REFUSED`. Settled N is 0. The collector being ready does not admit a
settled panel. `clock_admit` raises. An Examiner pass is not this scaffold.

`FROZEN_EXPERIMENT.json` keeps `results`, `pnl`, `MZ`, and `ROI` null.
`results/EMPTY_RESULTS.json` keeps the same four fields null. Schema checks
do not fill either file.

The ladder schema is weather panel material a later R3-P3 pass can prefer.
This scaffold does not join that lab. `later_r3_p3_panel.joined_now` stays
false. Native public `taker_*` prints are not synthesized. R3-P3, including
an open pull request that adds it, stays unmodified.

## Placement

`kalshi_feebook_lab_20260922` and `kalshi_rails_lab_20260922` are frozen
evidence snapshots. This lab imports those modules and does not edit them,
copy them, or vendor a second fee formula. The capital-structure lab, the
hygiene lab, the queue-fragility lab, the examiner lab,
`kalshi_r3_p1_fee_cost_lab_20260922`, `kalshi_r3_p4_l2_shape_lab_20260922`,
and the Q1–Q7 directories stay untouched. The new directory is
`kalshi_c3_kxhighny_lab_20260922`.

Fee path: `feebook.reciprocal_book` and `feebook.order_fee` with
`round_up=True`. Commit `22371178cb2663250b4762f328069571c48cb551`. Formula
`astra.r1p1.feebook.claude_order_level_ceil.v1`.

Rail path: `rails.maker_quote_credit` and `rails.judge_freshness` with
`rails.canonical_book_content`. Commit
`6a28e0d6254327ea4e6451c781bec56215ac6cac`. Rule
`astra.r1p5.rails.maker_credit_floor_cent.v1`. Queue labels
`rails.scenario_queue('q3300')` and `rails.scenario_queue('q10000')` are
read as instrument names. They are not a knob, and this scaffold does not
construct `QueueInstrument` or award queue volume.

`KXHIGHNY` and `KXHIGHCHI` are absent from the feebook series stub. The
imported resolver marks them `default_unknown_series`. That mark is the stub
rule. It is not evidence the live schedule uses `M = 1`.

## Hypothesis source

GitHub weather-spread is hypothesis only. The text was read from
`17thgreen/Claude-SportsBetting-Competition-to-the-Death`,
`src/flatstake/providers/kalshi_weather.py`, blob
`323463cd7538464dfe90ec8b6acea9c76e10ee29`, at ref
`ce34417c1a2f3353225ed6e585e48217d41de96d`. Those bytes are not vendored.
`port_weather_algorithm` raises. No forecast client is added.

The hypothesis, in that file's own terms: a daily high-temperature ladder is
a set of mutually exclusive buckets (below 76, 76–77, 78–79, and an open top).
Honest mids on an exhaustive ladder should sum to about $1, and the overround
is a tightness reading. This lab does not sum mids, does not normalize them
into probabilities, and does not store that sum.

Station identity from the same file, coordinates left there:

| Series | City | NWS station | Identity note |
|---|---|---|---|
| `KXHIGHNY` | New York City | `KNYC` | Contract station named in that table |
| `KXHIGHCHI` | Chicago | `KMDW` | Midway. The file's Chicago station is Midway |

`KXHIGHMIA` appears in that table and in the Grok series list. It is outside
this packet. A rung with that series raises `SeriesRefused`.

Published weather ROI, the cheap-YES lottery, HX spread selection, directional
pickers, and the Grok nowcast lock stay outside this directory. Q6 label
`000` is not retuned.

## Question

On schema-only ladder fixtures, do the helpers mark adjacent whole-degree
strikes on `KXHIGHNY` and `KXHIGHCHI`, quote each rung through the imported
bids-only book and the maker-credit rail, treat a keepalive as stale, and
refuse forecast ports, queue fills, settled fills, and any scorecard that
would fill `results`, `pnl`, `MZ`, or `ROI`?

This is a code-verification question. It is not a backtest and not live
trading. `MZ` is the Mincer–Zarnowitz slot. `ROI` is the return slot. Both
stay null while settled N is 0.

## Pin A — bordering strikes

Registry id: `astra.c3.kxhighny.bordering_strike.v0`.

A rung carries `series`, `event_ticker`, `ticker`, `floor_strike`, and
`cap_strike`. Strikes are whole degrees Fahrenheit as `Decimal`, `int`, or
`str`. Floats are rejected. A fractional degree is a ladder defect.

| Shape | `floor_strike` | `cap_strike` |
|---|---|---|
| Bottom tail | null | present |
| Interior | present | present, and `cap >= floor` |
| Top tail | present | null |

An event has at most one bottom tail and one top tail. Floors are unique.
Sort order is bottom tail first, then ascending floor. The top tail is the
warmest rung. A top tail with a warmer neighbor is a ladder defect.

Consecutive rungs after that sort:

```
degree_gap = warmer.floor_strike - colder.cap_strike
border when degree_gap == 1
gap    when degree_gap > 1
overlap when degree_gap <= 0
```

A border is the GitHub bucket shape: 75 then 76, and 77 then 78. Uncovered
degrees are `degree_gap - 1`. A gap stays a gap. The helper does not insert
a strike between the rungs. Overlap raises `LadderDefect`.

Event tickers match `KXHIGHNY-26SEP23` or `KXHIGHCHI-26SEP23`: series, two
digits, an English month abbreviation, two digits. The date is a schema
label. It is not a forecast day and not evidence the venue listed that event.
Each rung ticker starts with its event ticker.

## Pin B — imported book, credit, and freshness

When a rung carries `orderbook_fp`, `feebook.reciprocal_book` supplies the
bids-only touch. A missing side leaves the implied ask and the spread unset.
The missing price is not invented.

Maker admission is a one-contract probe at the best YES bid:

```
rails.maker_quote_credit(bid_yes, 1, series=series)
```

The probe uses the examiner cent ceiling inside the rail. `admitted` follows
that credit. A one-cent YES bid whose venue-rounded credit is zero is
recorded as refused. Touch size is reported beside the quote. It is not an
awarded fill. `award_queue_fill` raises `InventedFillRefused`.

Freshness wraps `rails.judge_freshness`. Canonical content is
`rails.canonical_book_content` of the event's series, ticker, strikes, and
bids. A first observation is `initial`. Identical content and the same
schema transaction label are `unchanged`. `keepalive=True` is
`keepalive_ignored`. The label is caller-supplied. This scaffold has no
clock loop and no websocket client.

## Pin C — schema-only fixture

`fixtures/schema_only_ladder.json` is a field-shape sheet. Its header says
`SCHEMA_ONLY`, `admitted_settled_panel` false, collector `READY`, clock
`REFUSED`, settled N 0, and the panel version above. The rungs are not a
capture and not fills. The committed file has no resolution, result, fill,
or profit keys.

| `schema_id` | What the harness does |
|---|---|
| `ny_documented_shape` | `KXHIGHNY-26SEP23`. Tails and interiors: cap 75, 76–77, 78–79, floor 83. Two borders (75\|76 and 77\|78). One gap before 83. No inserted rung. |
| `chi_interior_border` | `KXHIGHCHI-26SEP23`. 64–65 borders 66–67. |
| `chi_fee_blind_cent` | One rung, YES bid `0.01`, NO bid `0.50`. No border. Maker credit refused. |
| `ny_missing_yes` | NO bids only. YES bid stays unset. No maker probe. |
| `chi_overlap` | 76–78 against 77–79. `LadderDefect`. No border emitted. |
| `mia_out_of_scope` | `KXHIGHMIA`. `SeriesRefused`. |

`simulate_ladder` walks those events. Its `results`, `pnl`, `MZ`, and `ROI`
are null. It does not write `FROZEN_EXPERIMENT.json` or
`results/EMPTY_RESULTS.json`.

A unit may add `result`, `fill`, or `pnl` to an in-memory copy. The walker
raises `SettledFillRefused` on that copy and does not write the copy back.
The committed fixture stays free of those keys.

## Out of scope

Live orders, credentials, and account endpoints. Forecast, Open-Meteo, and
NWS clients. Porting `implied_distribution` or any sibling weather script.
Queue fills and `QueueInstrument`. Invented resolutions and invented fills.
Mincer–Zarnowitz coefficients. ROI. Summing mids into a probability.
Retuning Q6 label `000`. Copying the feebook or the rails. Editing R3-P3.
An Examiner pass.

## What a later result file may say

After the source freeze, a result file may record whether the unit tests
passed and may repeat these limitations. It may not report profit, may not
fill `MZ` or `ROI`, may not relabel development games, and may not treat a
schema rung as a settled contract. Those four scorecard fields stay null
until an Examiner pass. This scaffold does not run that pass.
