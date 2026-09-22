# R2-P1 fixture join on Q6-000

September 22, 2026. This file is the hypothesis. It is committed before the
join harness runs and before any unit-test outcome is recorded. No figure in
this document is a trading result. Q6 outcomes that already exist are not
re-labeled as evidence from this lab.

## Pick

Pick **A**: wire a join harness that reads Q6-`000` fill and order fixtures
into the R2-P1 hygiene helpers under the R1-P1 examiner feebook and the R1-P5
rails labels.

The canonical freeze is `packets/R2-P1_FIXTURE_JOIN_000_FREEZE_2026-09-22.md`,
sha256 `e9bac91ca908b2ba704d966f0cf48cb181070ac11de1d117b93512bd2719ae1c`.
Pick B, a queue-fragility fixture join, stays deferred. This lab does not
start it.

## Placement

`kalshi_r2p1_hygiene_000_lab_20260922` is a frozen evidence snapshot. The
lab merge is `25ec05381207252abb8abec8f6f99e30765f9704`. The imported tree
is that directory as it stands on main at
`c33af159d00c07f2d66b2f93174cfcdb4cde8d37`, including the queue-fragility
sibling pin. This lab imports `hygiene.py` and does not edit it. `kalshi_feebook_lab_20260922`
at `22371178cb2663250b4762f328069571c48cb551` and
`kalshi_rails_lab_20260922` at `6a28e0d6254327ea4e6451c781bec56215ac6cac`
stay frozen. Capital structure, queue fragility, and the Q1–Q7 trees stay
untouched.

The new directory is `kalshi_r2p1_fixture_join_000_lab_20260922`.

## Question

Holding strategy Q6-`000`, can a read-only harness:

1. Load a fill ledger and the matching order ledger.
2. Join maker fills to orders on `order_id`.
3. Call `hygiene.fee_delta` with the feebook rate for that role.
4. Call `hygiene.maker_credit_floor_zero_refuse` on maker slices.
5. Call `hygiene.content_fresh_flag` through `FreshnessCursor` when a row
   carries a book annotation or a keepalive bit.
6. Call `hygiene.queue_bin_mismatch` with the joined order's `initial_queue`
   against the ledger's assumed scenario (`q3300` or `q10000`).

This is a code-verification question. It is not a Q6 tape walk and not live
trading.

## Scorecard

These fields stay null in `FROZEN_EXPERIMENT.json`, in
`results/EMPTY_RESULTS.json`, and in `packets/R2-P1_FIXTURE_JOIN_000/results.json`:

- `fee_delta_vs_inherited_model`
- `freshness_gap_sec`
- `queue_bin_mismatch_rate`
- `results`
- `pnl`

Unit tests may assert that the helpers return values on synthetic rows. Those
values stay in memory. The harness has no writer that stores them in the
freeze packet. `published` on a join report is the null scorecard, status
`NOT_RUN`, pick `A`.

## Fixture pin

| Role | Path | SHA-256 |
|---|---|---|
| Primary fills | `nfl_factorial_lab_20260921/results/q3300_d0.25_000_fills.jsonl.gz` | `9d56f5d3c599e092606be9f4a1ad41ae8baabff4921d3d722adf0b57ac944a3f` |
| Primary orders | `nfl_factorial_lab_20260921/results/q3300_d0.25_000_orders.jsonl.gz` | `c390801b9a7cf6d182d2d097123ed944792980524a7975e6e59a904a530f4b1c` |
| Harsh twin fills | `nfl_factorial_lab_20260921/results/q10000_d0.25_000_fills.jsonl.gz` | `678d6cb602fb832f8a77ac7a0cfefd9a4d8390002b0962ddc956ba1f19f4b59d` |
| Harsh twin orders | `nfl_factorial_lab_20260921/results/q10000_d0.25_000_orders.jsonl.gz` | `e16632b630058854bfc6ac410cb960d5439fb8a151e180d0793c37e8f92068d9` |

The harsh twin is a queue-label stress pin. It is not a second fee knob and
the default join does not open it. Pair-check arm D is not a strategy. The
ledger label must be `000`.

`*.jsonl.gz` is gitignored. When the primary pair is absent, the harness
reads the synthetic stand-in under `fixtures/`. That stand-in uses the
factorial fill and order keys. It is not a replay and not a restoration of
the indexed gzip bytes. `fixtures/PIN.md` records the production path.

## Ledger mapping

Required fill keys, from the Q6 factorial writers: `at`, `ticker`, `event`,
`outcome`, `direction`, `price`, `size`, `fee`, `kind`, `paired`, `reason`,
`inventory_after`, `cash_after`, `order_id`, `improved`, `resting_seconds`,
`queue_remaining`, `completion_instruction`, `entry_window_open`.

Required order keys: `order_id`, `ticker`, `event`, `outcome`, `direction`,
`submitted_at`, `active_at`, `submitted_quantity`, `price`,
`entry_window_open`, `inventory_at_submission`, `filled_quantity`,
`cancel_requested_at`, `initial_queue`.

`cash_after`, `inventory_after`, `paired`, and the recorded `fee` are carried
so the schema can be checked. They are not summed. They are not profit.

JSON numbers become `Decimal` through `Decimal(str(value))` before any
feebook call. Floats are not passed into `feebook.as_decimal`. The fee
coefficient is the rate `feebook.order_fee` resolves for that role. A shadow
literal is not read from the factorial summary.

`round_up` follows the hygiene pin: true when the fill size equals the joined
order's submitted quantity, and true for a taker slice that has no resting
order. A smaller maker fill uses `round_up=False`.

`queue_remaining` is the queue after consumption. Attribution uses
`initial_queue` on the joined maker order. A maker order without
`initial_queue` stays unattributed. Taker rows use order id `-1` in the
engine and are not required to join an order record. Their queue label stays
unattributed.

Book freshness is unlabeled unless the row includes a `book` object plus
`transaction_time`, or `keepalive` true. Those annotations are absent from
the factorial gzip schema. The synthetic stand-in adds them so
`content_fresh_flag` is exercised. A keepalive does not move the freshness
anchor.

## Left closed

No Q6-`000` retune. No capital A2 or A3. No live orders. No second fee
treatment. No queue-fragility fixture join. No completed-profit claim.

## What a later result file may say

After the source freeze, a result file may record whether the unit tests
passed and may repeat these limitations. It may not report profit and may not
fill the five scorecard fields.
