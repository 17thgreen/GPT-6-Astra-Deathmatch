# Queue fragility of Q6-000 under R1-P5

September 22, 2026. This file is the hypothesis. It is committed before source is
frozen and before any unit-test outcome is recorded. No figure in this document
is a trading result. Q6 outcomes that already exist are not re-labeled as
evidence from this lab.

## Pin lock

The canonical freeze is
`QUEUE_FRAGILITY_000_R1P5_FREEZE_2026-09-22.md` in this directory. Its sha256
is `e01d684abefd2d919ac6546f85619a246ce73098c04f7b24c84451ff49b00308`.
The conductor packet name is
`packets/QUEUE_FRAGILITY_000_R1P5_FREEZE_2026-09-22.md`. Those bytes are the
file stored here. `queue_fragility_000_r1p5_freeze.json` is the conductor
kernel that cites that digest. `EXPERIMENT_SPEC.md` is the lab hypothesis.

The only knob is queue/fill stress. The fee treatment stays on the R1-P1
examiner channel. Strategy Q6-`000` stays frozen. Capital stays the shared
A1-equivalent pool. R2-P1 hygiene, merged at `25ec05381207252abb8abec8f6f99e30765f9704`,
is the prior and is orthogonal: that lab held queue fixed and relabeled fees.
This lab holds the fee channel fixed and varies the rails queue.

## Placement

`kalshi_feebook_lab_20260922` and `kalshi_rails_lab_20260922` are frozen
evidence snapshots. This lab imports those modules and does not edit them.
`kalshi_r2p1_hygiene_000_lab_20260922`, `kalshi_capital_structure_lab_20260922`,
and the Q1–Q7 directories stay untouched. The new directory is
`kalshi_queue_fragility_000_lab_20260922`.

Fee path, fixed: `astra.r1p1.feebook.claude_order_level_ceil.v1`, commit
`22371178cb2663250b4762f328069571c48cb551`.

Queue path, the knob: `kalshi_rails_lab_20260922` `QueueInstrument`, commit
`6a28e0d6254327ea4e6451c781bec56215ac6cac`.

## Question

Holding strategy Q6-`000`, the shared 5000 USD account, the 31-game tape
pointer, and the R1-P1 examiner fee channel, do the three rails queue arms
below differ only in queue parameters on unit fixtures, while every arm binds
the same feebook formula, the same series table, and the same maker-on
examiner path?

This is a code-verification question. It is not a Q6 tape walk and not live
trading. The three pre-settlement outputs stay null until a real fixture join.
`FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null. Unit tests may assert
queue arithmetic on a synthetic print. They may not invent walk P&L, and they
may not write those outputs into the freeze file.

## Constants

| Pin | Frozen value |
|---|---|
| Strategy pointer | Q6 label `000` |
| Shadow file | `nfl_factorial_lab_20260921/SHADOW_CANDIDATE_FREEZE.json` sha256 `b55ff36cb161c824a3d1b490795c8ac6891f01489456f61da311ac863366af48` |
| Tape manifest | `nfl_factorial_lab_20260921/inputs/manifest.json` sha256 `375ea6e2c9125a411d5444a88115213542d5b19c874d73a2bed0b9355fd6277d` |
| Cohort | 31 development events, read from `inputs/week_membership.json` |
| Capital | Shared 5000 USD, mode `A1_shared_pool` only |
| Examiner formula | `feebook.EXAMINER_FORMULA_ID` |
| Empty outputs | `results/EMPTY_RESULTS.json` |
| Prior merge | R2-P1 `25ec05381207252abb8abec8f6f99e30765f9704` |

The shadow freeze file contains fee coefficients under its common config.
This lab does not read that object and does not copy those coefficients into
source. Examiner rates come only from `feebook.load_series_table` through the
rails instrument, which calls `feebook.order_fee`.

## Arms

Each arm constructs `rails.QueueInstrument` with one participation value,
`rails.FILL_PARTICIPATION_DEFAULT`, and no series override and no fee-table
override. Magnitudes come from `rails.scenario_queue`.

| Arm | `queue_ahead_contracts` | `fill_participation` | `queue_model` |
|---|---|---|---|
| `QF0_q3300_measured` | `rails.scenario_queue('q3300')` | `rails.FILL_PARTICIPATION_DEFAULT` | `measured` |
| `QF1_q10000_stress` | `rails.scenario_queue('q10000')` | `rails.FILL_PARTICIPATION_DEFAULT` | `measured` |
| `QF2_front_optimistic` | `0` | `rails.FILL_PARTICIPATION_DEFAULT` | `front` |

`QF0` versus `QF1` changes `queue_ahead_contracts` only. `QF2` sets
`queue_model` to `front` and sets the configured ahead value to 0, which is
the rails optimistic bound. Participation is the same on every arm. No arm
passes a maker-off flag, an unrounded comparator id, or a shadow coefficient.

The rails fill rule is consumed unchanged:

```
consumed = min(Q, V)
Q := Q - consumed
post = V - consumed
fill = min(R, post * p)
```

`front` forces `Q = 0` on a new order. A partial fill charges
`order_fee('maker', got, our_price, round_up=False)` inside rails. That
`round_up=False` flag is the frozen rails partial path. It is the same call
for every arm. It is not a fee-treatment arm. Order admission still goes
through `rails.admit_maker_quote`, which uses the examiner cent ceiling.
A quote the credit floor refuses is refused on every arm.

Optional instrument labels, checked in units, are rails behavior and are not
extra knobs:

- Taker YES fills resting NO, and taker NO fills resting YES
  (`feebook.TAKER_FILLS_RESTING`).
- A later maker intent at the same ticker, outcome, and price keeps
  `queue_ahead`.
- A new price starts at the back of the queue for that arm's model.

## Pre-settlement outputs

These three keys are nullable until a real join of historical fills:

- `fill_rate_delta_vs_q3300`
- `adverse_queue_exposure`
- `participation_stress_gap`

`pre_settlement_outputs` returns all three as null, with `results` and `pnl`
null and status `NOT_RUN`, unless the caller passes `joined=True` together
with intents and trades. That joined return is a synthetic fixture
calculation. Its status is `SYNTHETIC_FIXTURE_ONLY`. It still sets `results`
and `pnl` to null. Nothing in this lab writes it into `FROZEN_EXPERIMENT.json`
or `results/EMPTY_RESULTS.json`.

On a joined slice the instrument defines:

- `fill_rate` = filled contracts / resting maker size.
- `fill_rate_delta_vs_q3300` maps `QF1_q10000_stress` and
  `QF2_front_optimistic` to `fill_rate(arm) - fill_rate(QF0)`.
- `adverse_queue_exposure` maps each arm to the sum of queue contracts
  consumed ahead of our order (`min(Q, V)` on each print the rails price
  check accepts). The unit is contracts. It is not cash and not profit.
- `participation_stress_gap` is
  `rails.FILL_PARTICIPATION_DEFAULT - (QF1 filled / QF1 eligible volume)`.
  Eligible volume is the size of prints that match polarity and trade at or
  through our bid. The gap is null when that volume is zero. The gap is the
  stress arm only.

`historical_completed_net` raises. There is no tape walker and no settlement
cash figure.

## Capital

`shared_capital` accepts mode `A1_shared_pool` and returns one pool of
5000 USD. Modes `A2_shared_soft_reserve` and `A3_hard_equal_slices` raise
`CapitalArmForbidden`. This lab does not import
`kalshi_capital_structure_lab_20260922` and does not reimplement borrows,
slices, or wallet sums.

## Live orders

No live order client and no `KalshiExecutionAdapter`. `execution_adapter`
raises `LiveOrdersForbidden`.

## Left untouched

`kalshi_feebook_lab_20260922`, `kalshi_rails_lab_20260922`,
`kalshi_r2p1_hygiene_000_lab_20260922`, `kalshi_capital_structure_lab_20260922`,
`nfl_factorial_lab_20260921` (Q6 `000` included), `nfl_paircheck_lab_20260922`,
the prospective recorder, and the earlier Q labs. No signal retune. No capital
redesign. No fee-treatment arm. No inherited `common_config` fee literals in
this lab's source.

The frozen R2-P1 unit file asserts that no `*queue_fragility*` directory
exists, because that twin had not been started. This lab starts that twin in
a new directory and does not rewrite the R2-P1 snapshot. A later rerun of the
R2-P1 suite will fail that one assertion. That failure is the snapshot pin
meeting this directory. It is not a reason to edit the R2-P1 lab.

## What a later result file may say

After the source freeze, a result file may record whether the unit tests
passed and may repeat these limitations. It may not report profit, may not
relabel development games, and may not fill the three pre-settlement outputs.
`results`, `pnl`, `fill_rate_delta_vs_q3300`, `adverse_queue_exposure`, and
`participation_stress_gap` in `FROZEN_EXPERIMENT.json` stay null until an
Examiner fixture join. A full Q6-`000` tape walk is out of this unit page.
