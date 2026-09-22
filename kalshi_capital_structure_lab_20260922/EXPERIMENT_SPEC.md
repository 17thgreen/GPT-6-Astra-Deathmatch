# Capital structure probe: one shared $5,000 under A1, A2, and A3

September 22, 2026. This file is the hypothesis. It is committed before source is
frozen and before any unit-test outcome is recorded. No figure in this document
is a trading result. Q6 outcomes that already exist are not re-labeled as
evidence from this probe.

This lab measures capital partition rules. It does not choose markets, retune
Q6 label `000`, vary the Q7 pair-check, or report strategy ROI.

## Placement

`kalshi_feebook_lab_20260922` and `kalshi_rails_lab_20260922` are frozen
evidence snapshots on main. This lab imports those modules and does not edit
them. Q1–Q7 directories stay untouched. The new directory is
`kalshi_capital_structure_lab_20260922`, beside those two labs.

Fee path: `astra.r1p1.feebook.claude_order_level_ceil.v1`, commit
`22371178cb2663250b4762f328069571c48cb551`.

Queue and maker-credit path: `astra.r1p5.rails.maker_credit_floor_cent.v1`,
commit `6a28e0d6254327ea4e6451c781bec56215ac6cac`. Queue magnitudes are read
from `rails.scenario_queue`. They are instrument labels.

The freeze packet copied into this directory is
`CAPITAL_STRUCTURE_PROBE_FREEZE_KERNEL_2026-09-22.md`, sha256
`729c493e7a059615e6c734a19967b98a61c0c0cc2bc6949d203dd5096414060c`.
`capital_structure_freeze.json` is the packet's machine pin.

## Question

On one shared account with the same `C_total` of 5000 USD and the same 31-event
development cohort, do arms A1, A2, and A3 keep the partition identity, and do
the A2 unused-only borrow log, the A3 no-borrow rule, the non-trading residual,
and the shared-account scoreboard match the freeze?

This is a code-verification question. It is not a Q6 tape walk and not live
trading. `FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null until an
Examiner pass. Unit tests may assert invariants. They may not invent walk P&L.

## Constants

| Pin | Frozen value |
|---|---|
| `C_total` | 5000 USD |
| `N_events` | 31 |
| Per-event slice | `floor(C_total / N_events)` = 161 USD |
| A3 residual | 9 USD in `non_trading_residual_bucket` |
| A2 soft policy | `borrow_unused_event_id_FIFO` |
| Strategy pointer | Q6 label `000` |
| Shadow file | `nfl_factorial_lab_20260921/SHADOW_CANDIDATE_FREEZE.json` sha256 `b55ff36cb161c824a3d1b490795c8ac6891f01489456f61da311ac863366af48` |
| Tape manifest | `nfl_factorial_lab_20260921/inputs/manifest.json` sha256 `375ea6e2c9125a411d5444a88115213542d5b19c874d73a2bed0b9355fd6277d` |
| Primary stress | `q3300_d0.25` |
| Harsh twin | `q10000_d0.25`, instrument label only, not a second capital knob |
| Promotion scoreboard | `shared_account_only` |

`161` and `9` are the floor division of the frozen `C_total` and `N_events`.
Event ids are the sorted keys of
`nfl_factorial_lab_20260921/inputs/week_membership.json`. That file is read.
It is not rewritten. The cohort length must be 31.

## Arms

Each arm is one shared account. `C_total` is the same 5000 USD on every arm.
Cash amounts are `Decimal`. Floats are rejected. A fund request is
all-or-nothing. Identity after every applied fund and release:

```
available + committed + non_trading_residual_bucket = C_total
```

No fill on this path writes a profit number. Releasing an order returns the
same cash to the buckets that funded it. The borrow log is append-only.

### A1 — `A1_shared_pool`

One pool of `C_total`. Markets compete for that pool. There is no per-event
reserve and no cross-event borrow log. One event may consume the whole pool.
The residual bucket is 0.

### A2 — `A2_shared_soft_reserve`

Soft reserve `R_m` = 161 USD on each event. `31 * 161 = 4991`. The remaining
9 USD stays in `unreserved_pool`. That slack is still pool cash. It is not
`non_trading_residual_bucket` (that bucket is 0 on A2).

Policy `borrow_unused_event_id_FIFO`:

1. Spend the borrower's own unused soft reserve.
2. If still short, borrow unused soft reserve of other events. Donors are
   visited in ascending `event_id`. The borrower is skipped. A donor with no
   unused reserve is skipped. Used reserve and reserve already borrowed away
   are not unused.
3. If still short, draw `unreserved_pool`. That draw is logged on
   `unreserved_draws`. It is not a cross-event borrow row.
4. Otherwise refuse the request. The pool never goes negative.

Competitive admission of several requests uses `fund_many`. Borrowers are
processed in ascending `event_id`, and original input order breaks ties for
the same event. Each cross-event take appends one borrow-log row: policy,
borrower, donor, amount, order id, sequence. A request inside the borrower's
own unused reserve appends no borrow row.

A release restores own reserve, donor unused reserve, and unreserved slack.
The historical borrow rows stay.

### A3 — `A3_hard_equal_slices`

Hard slice 161 USD per event. No cross-event borrow. An event cannot spend
another event's slice. A request above the event's own unused slice is
refused and leaves every slice unchanged.

The 9 USD residual is `non_trading_residual_bucket`. It cannot fund an order.
`draw_residual` raises. The bucket stays 9. Slices plus the residual equal
`C_total`.

## Quote cash and the fee channel

Capital partitions take a `Decimal` cash amount. A quote admission is a
separate step, and its rates come from the imported labs:

- Maker: `rails.admit_maker_quote`. The cash lock is the quote gross
  (`price * contracts`) after the rail admits the quote. The examiner fee is
  the fee on that rail result. A refused credit (`rails.MakerCreditRefused`)
  moves no cash.
- Taker: `feebook.order_fee('taker', ..., round_up=True)`. The cash lock is
  gross plus that examiner fee.
- Both locks record `feebook.EXAMINER_FORMULA_ID`. Maker locks also record
  `rails.FEE_CREDIT_RULE_ID`.

`instrument_binding()` reads taker and maker rates from
`feebook.load_series_table()` and queue magnitudes from
`rails.scenario_queue('q3300')` and `rails.scenario_queue('q10000')`.
`SHADOW_CANDIDATE_FREEZE.json` `common_config` is not a fee source and not a
queue source. Pair-check on/off is not a parameter.

`measurement_scorecard` calls `feebook.classify_scorecard`. Without the
examiner fee channel the classifier refuses `completed_profit`. This lab still
stores no walk P&L on the account. A classifier label is not a tape result.

## Promotion scoreboard

The scoreboard is the one shared account on the arm under test.
`promotion_scoreboard` returns that account's arm, `C_total`, and partition
identity, with `pnl` null.

`compare_independent_wallets_to_shared_account` raises
`IndependentWalletSumForbidden` with code
`sum_of_N_independent_wallets_vs_one_5k`. Passing a wallet list into
`promotion_scoreboard` raises the same way. The partition identity
(slices + residual = `C_total`, or pool available + committed = `C_total`)
is one account's books. It is not a sum of N independent wallets.

## Strategy pointer and the Q7 citation

The packet's strategy pointer is Q6 label `000`. Pair-check is not varied.
Q7 arm B is not bound. HX, weather, and directional pickers stay closed.

The packet cites:

| Artifact | Packet pin |
|---|---|
| Q7 `results/verification.json` | status `VERIFIED`, sha256 `eb1586bf13b1631951a4f177293350cb89fc7948a50fbb7044f4f05313ebc06f` |
| Q7 `results/paircheck_effects.json` | status `COMPLETE`, selection `NO_NEW_SELECTION`, fallback shadow `000`, sha256 `5d87ea610f22482c980868d8a31a228ca1931368d9eeab73add4256d2e117fdf` |

Those blobs are not in this checkout at base
`6a28e0d6254327ea4e6451c781bec56215ac6cac`. The in-tree
`nfl_paircheck_lab_20260922/results/verification.json` hashes to
`9cde03dc3d52eb3ab9d18024155c341451de9e1e8836356cdcf3cf1d0ac006e4` and reads
`NOT_RUN_INPUTS_MISSING`. `paircheck_effects.json` is absent.
`analysis_status.json` hashes to
`8acec3c77b86abce43b6eb01a941de317f1603a5a30c7ee4bc4582800c119ebb` and reads
`NOT_RUN_INPUTS_MISSING`. This lab does not rewrite those files and does not
treat the in-tree status as the packet's `VERIFIED` hash. The shadow freeze
file and the tape manifest on this base do match the packet hashes above.
The pointer used here is that on-tree Q6 `000` file.

## Live orders

No live order client and no `KalshiExecutionAdapter`. `execution_adapter`
raises `LiveOrdersForbidden`.

## Left untouched

`kalshi_feebook_lab_20260922`, `kalshi_rails_lab_20260922`,
`nfl_factorial_lab_20260921` (Q6 `000` included), `nfl_paircheck_lab_20260922`
arms A–D, the prospective recorder, the earlier Q labs, HX spread selection,
weather cheap-YES selection, and directional pickers. No fourth blended
capital arm. No signal retune. No fee or queue retune inside those labs.

## What a later result file may say

After the source freeze, a result file may record whether the unit tests
passed and may repeat these limitations. It may not report profit, may not
relabel development games, and may not mark an Examiner tape pass complete.
`results` and `pnl` in `FROZEN_EXPERIMENT.json` stay null until that Examiner
pass. A full Q6-`000` tape walk is out of this unit page when the external
kits are not in the checkout.
