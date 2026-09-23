# Cap-SR: soft-blended reserves of Q6-000

September 23, 2026. This file is the hypothesis. It is committed before source
is frozen and before any unit-test outcome is recorded. No figure in this
document is a trading result. Q6 outcomes that already exist are not re-labeled
as evidence from this probe.

Feature family **Cap-SR** (capital soft-reserve policy). This probe is not
F1, not F2, and not F3. Nearest dead cards are **C1 empty-book** (orderbook
pin is real empty books; scoring blocked) and **Q7 Arm B kill** (Examiner
KEEP `000` / KILL B). Cap-SR does not ungate C1 books and does not revive
Arm B.

This lab measures one knob: `soft_policy` / blend rule, under the A2
substrate only. It does not choose markets, retune Q6 label `000`, reopen
queue-fragility, re-arm A1 or A3, or report strategy ROI.

## Placement

`kalshi_capital_structure_lab_20260922`, `kalshi_feebook_lab_20260922`, and
`kalshi_rails_lab_20260922` are frozen evidence snapshots. This lab imports
them and does not edit them. Q labs stay untouched. The new directory is
`kalshi_soft_blended_reserves_000_lab_20260923`.

`lab/governance/astra/packets/` is not in this checkout. Packet copies sit
beside the engine and in the existing governance packet tree:

| Copy | Path |
|---|---|
| Freeze markdown | `kalshi_soft_blended_reserves_000_lab_20260923/SOFT_BLENDED_RESERVES_000_FREEZE_2026-09-23.md` |
| Lab bundle | `kalshi_soft_blended_reserves_000_lab_20260923/SOFT_BLENDED_RESERVES_000/` |
| Governance bundle | `packets/SOFT_BLENDED_RESERVES_000/` |
| Governance markdown | `packets/SOFT_BLENDED_RESERVES_000_FREEZE_2026-09-23.md` |

The markdown sha256 is
`1f263dec7d7810515c3e32c13f3c5eca4344c4951db762a88ea01a8dfde7b1b3`.
`FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.
`results/EMPTY_RESULTS.json` keeps `borrow_count_delta_vs_fifo`,
`blend_utilization_gap`, and `soft_breach_or_blend_rate` null.

Fee path: `kalshi_feebook_lab_20260922` @
`22371178cb2663250b4762f328069571c48cb551`. `fee_source` is that feebook.
Shadow fee literals `0.0175` and `0.07` are forbidden in this lab.

Queue labels: `kalshi_rails_lab_20260922` @
`6a28e0d6254327ea4e6451c781bec56215ac6cac`. `queue_source` is those rails.
Labels only. Queue is not the knob.

Parent capital lab: `kalshi_capital_structure_lab_20260922` @ `ce4671b8`
(`ce4671b8201b3fe49ecab91d684815fe6bd51447`). SR0 reuses that lab's A2
engine for the FIFO unused-borrow path. This lab does not mutate it.

## Question

Holding strategy Q6-`000`, one shared account of 5000 USD, soft reserve
`R_m` = 161, residual 9 in `non_trading_residual_bucket`, the 31-event
development tape, the R1-P1 feebook, and the R1-P5 rails labels fixed, do
soft-policy arms SR0, SR1, and SR2 keep the partition identity and the
borrow / blend logs described below?

This is a code-verification question. It is not a Q6 tape walk and not live
trading. Unit tests may assert invariants. They may not invent walk P&L.
The three scorecard fields stay null until an Examiner opens them.

## Constants

| Pin | Frozen value |
|---|---|
| `C_total` | 5000 USD, shared scoreboard |
| `N_events` | 31 |
| `R_m` | floor(5000 / 31) = 161 USD |
| Residual | 9 USD, `non_trading_residual_bucket`, may not fund orders |
| Strategy pointer | Q6 label `000` |
| Shadow file | `nfl_factorial_lab_20260921/SHADOW_CANDIDATE_FREEZE.json` sha256 `b55ff36cb161c824a3d1b490795c8ac6891f01489456f61da311ac863366af48` |
| Tape manifest | `nfl_factorial_lab_20260921/inputs/manifest.json` sha256 `375ea6e2c9125a411d5444a88115213542d5b19c874d73a2bed0b9355fd6277d` |
| Primary stress label | `q3300_d0.25`, not a second capital knob |
| Promotion scoreboard | `shared_account_only` |
| Knob | `soft_policy` only |
| Capital substrate | A2 shared soft reserve. A1 and A3 stay closed |

`161 * 31 + 9 = 5000`. Event ids are the sorted keys of
`nfl_factorial_lab_20260921/inputs/week_membership.json`. That file is read.
The cohort length must be 31.

Cash amounts are `Decimal`. Floats are rejected. A fund request is
all-or-nothing. Identity after every applied fund and release:

```
available + committed + non_trading_residual_bucket = C_total
```

The residual bucket stays 9 on every arm. `draw_residual` raises. Releasing
an order returns the same cash to the buckets that funded it. Borrow and
blend logs are append-only.

## Arms

Each arm is one shared account. `C_total` is 5000 USD. Competitive admission
of several requests uses ascending `event_id`, with original input order as
the tie break. That admission order is shared. It is not a second knob.

### SR0 — `borrow_unused_event_id_FIFO`

Control. Reuses `CapitalAccount` for arm `A2_shared_soft_reserve` from the
parent capital lab. Donors are other events, visited in ascending `event_id`.
Only unused soft reserve is borrowed. Every cross-event take appends one
borrow-log row. A spend inside the borrower's own unused reserve appends no
borrow row.

The parent A2 engine also keeps a 9 USD `unreserved_pool` that can fund an
order after unused reserves are exhausted. This freeze seats that 9 USD in
`non_trading_residual_bucket` instead. SR0 therefore matches A2 FIFO borrow
behavior on every schedule that A2 funds without an unreserved draw, and
refuses a schedule that would spend the residual. That refusal is the
residual pin, not a second soft-policy.

### SR1 — `borrow_unused_proportional`

Same unused-only constraint as SR0. After the borrower's own unused reserve,
donors contribute pro-rata to their unused soft reserve. The weight is unused
reserve, not event_id order. Donors with no unused reserve are skipped. The
borrower is not a donor. Takes are whole multiples of `10^-8` USD (Hamilton
largest remainder, event_id ascending on a tie) and sum to the borrowed
amount. Each take is at most that donor's unused reserve. Every positive
take is logged. The residual is not a donor.

### SR2 — `soft_blend_pool_fraction_0_5`

Half of each `R_m` seats a shared soft blend pool: `floor(R_m / 2) = 80`
USD per event, `31 * 80 = 2480` USD in the pool. The other 81 USD stays
event-local soft. Draw order is local unused, then the blend pool, then
refuse. Another event's local reserve is not a donor. A blend-pool draw is
logged. A local-only spend is not. The residual stays non-trading.
`2480 + 31 * 81 + 9 = 5000`.

## Not arms

A1 shared-no-soft. A3 hard equal slices. Queue 3300 versus 10000. Fee
treatment variants. Any Q6 signal change. A sum of N independent wallets
versus one shared 5000 USD account.

## Quote cash

Capital partitions take a `Decimal` cash amount. Quote admission reuses the
parent capital lab, which reads the feebook and the rails:

- Maker: `rails.admit_maker_quote`. Lock is quote gross after the rail
  admits the quote. A refused credit moves no cash.
- Taker: `feebook.order_fee` with the examiner ceiling. Lock is gross plus
  that fee.
- Both locks record the examiner formula id. Maker locks also record the
  rails fee-credit rule id.

`instrument_binding()` states `fee_source=feebook` and `queue_source=rails`.
Queue magnitudes come from `rails.scenario_queue`. Pair-check on/off is not
a parameter. `SHADOW_CANDIDATE_FREEZE.json` `common_config` is not a fee
source.

## Promotion scoreboard

The scoreboard is the one shared account. `pnl` is null.
`compare_independent_wallets_to_shared_account` raises
`IndependentWalletSumForbidden` and does not add wallets. Passing a wallet
list into `promotion_scoreboard` raises the same way.

## Scorecard

These fields stay null in `FROZEN_EXPERIMENT.json` and
`results/EMPTY_RESULTS.json`:

| Field | Later meaning |
|---|---|
| `borrow_count_delta_vs_fifo` | SR1 or SR2 borrow or blend-draw count minus SR0 |
| `blend_utilization_gap` | Max minus min soft utilization across events |
| `soft_breach_or_blend_rate` | Fraction of fills that needed a cross-event borrow or a blend-pool draw |

Fee-honest shared-account net stays Examiner-owned. A unit invariant is not
that scorecard.

## Live orders

No live order client and no `KalshiExecutionAdapter`. `execution_adapter`
raises `LiveOrdersForbidden`.

## Left untouched

`kalshi_capital_structure_lab_20260922`, `kalshi_feebook_lab_20260922`,
`kalshi_rails_lab_20260922`, `nfl_factorial_lab_20260921` (Q6 `000`
included), `nfl_paircheck_lab_20260922`, `kalshi_queue_fragility_000_lab_20260922`,
the C1 honesty lab, and the earlier Q labs. No `000` retune. No
queue-fragility reopen. No A1 or A3 re-arm.

## What a later result file may say

After the source freeze, a result file may record whether the unit tests
passed and may repeat these limitations. It may not report profit, may not
relabel development games, and may not mark an Examiner tape pass complete.
`results` and `pnl` stay null until that Examiner pass.
