# Cap-SR-FX: effects path of Q6-000

September 23, 2026. This file is the hypothesis. It is committed before source
is frozen and before any unit-test outcome is recorded. No figure in this
document is a trading result. Q6 outcomes that already exist are not re-labeled
as evidence from this probe.

Feature family **Cap-SR-FX** (effects path). This probe is orthogonal to
R3-P3, C3, C5, and C1 empty-books. It builds on the Cap-SR soft_policy rails.
It is not a second soft_policy lab. S1 `KXMLBGAME` stays deferred: the panel
stub is `PANEL_SCHEMA_STUB_EMPTY_EVENTS` (`admitted_at` null) and is not
unit-GO ready. Nearest dead cards remain **C1 empty-book** and **Q7 Arm B
kill**. This path does not ungate C1 books and does not revive Arm B.

## Placement

`kalshi_soft_blended_reserves_000_lab_20260923`,
`kalshi_capital_structure_lab_20260922`, `kalshi_feebook_lab_20260922`, and
`kalshi_rails_lab_20260922` are frozen evidence snapshots. This lab imports
the Cap-SR engine and does not edit it. Q labs, C3, C5, and R3-P3 stay
untouched. The new directory is `kalshi_cap_sr_effects_000_lab_20260923`.

`lab/governance/astra/packets/` is not in this checkout. Packet copies sit
beside the harness and in the existing governance packet tree:

| Copy | Path |
|---|---|
| Freeze markdown | `kalshi_cap_sr_effects_000_lab_20260923/CAP_SR_EFFECTS_PATH_000_FREEZE_2026-09-23.md` |
| Lab bundle | `kalshi_cap_sr_effects_000_lab_20260923/CAP_SR_EFFECTS_PATH_000/` |
| Governance bundle | `packets/CAP_SR_EFFECTS_PATH_000/` |
| Governance markdown | `packets/CAP_SR_EFFECTS_PATH_000_FREEZE_2026-09-23.md` |

The markdown sha256 is
`cd08a93af2659c36f83cd1b9ffc3174364cc767efc374a4e0669e128f6a29074`.
`FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.
`results/EMPTY_RESULTS.json` keeps `borrow_count_delta_vs_fifo`,
`blend_utilization_gap`, `soft_breach_or_blend_rate`, and
`effects_path_fixture_id` null.

Parent Cap-SR lab: `kalshi_soft_blended_reserves_000_lab_20260923` @
`45863037` (`45863037a30af6caf9c00361e46fe8bd5444c426`), freeze sha256
`1f263dec7d7810515c3e32c13f3c5eca4344c4951db762a88ea01a8dfde7b1b3`.
SR0, SR1, and SR2 are imported from that lab's `soft_policy` module.
This lab does not re-implement the soft_policy math and does not add a
second `kalshi_soft_blended_*` tree.

Fee path: `kalshi_feebook_lab_20260922` @
`22371178cb2663250b4762f328069571c48cb551`. Queue labels:
`kalshi_rails_lab_20260922` @
`6a28e0d6254327ea4e6451c781bec56215ac6cac`. Both stay fixed. The parent
capital lab pin remains `ce4671b8`, reached only through the Cap-SR import.

## Question

Holding strategy Q6-`000`, one shared account of 5000 USD, soft reserve
`R_m` = 161, residual 9 in `non_trading_residual_bucket`, the R1-P1
feebook, the R1-P5 rails labels, and the Cap-SR soft_policy set fixed, can
an effects-path harness join SR0, SR1, and SR2 to a Q6-`000` fill/order
fixture and emit the Cap-SR instrument schema without writing Examiner PnL?

The only knob is the fixture stress:

| Arm | Fixture stress |
|---|---|
| FX0 | `q3300_d0.25` |
| FX1 | `synthetic_borrow_stress` |

Both arms run the same three imported policies. The soft_policy set is not
reopened as a knob.

This is a code-verification question. It is not a Q6 tape walk and not live
trading. Unit tests may assert the join schema, the Cap-SR import pin, the
feebook and rails pins, the non-trading residual, and the wallet-sum refusal.
They may not invent walk P&L. The four scorecard fields stay null until an
Examiner opens them.

## Constants

| Pin | Frozen value |
|---|---|
| `C_total` | 5000 USD, shared scoreboard only |
| `R_m` | 161 USD, from the imported Cap-SR engine |
| Residual | 9 USD, `non_trading_residual_bucket`, may not fund orders |
| Strategy pointer | Q6 label `000` |
| Shadow file | `nfl_factorial_lab_20260921/SHADOW_CANDIDATE_FREEZE.json` sha256 `b55ff36cb161c824a3d1b490795c8ac6891f01489456f61da311ac863366af48` |
| FX0 fills | `nfl_factorial_lab_20260921/results/q3300_d0.25_000_fills.jsonl.gz` when that file and the matching orders file are present and match the factorial pin |
| FX0 orders pin | `nfl_factorial_lab_20260921/results/q3300_d0.25_000_orders.jsonl.gz` |
| FX0 stand-in | `fixtures/synthetic_q3300_d0.25_000_fills.jsonl` and the matching orders file, used only when the production gzip pair is absent |
| FX1 | `fixtures/synthetic_borrow_stress_fills.jsonl`, unit-only, not a panel |
| Promotion scoreboard | `shared_account_only` |
| Knob | `fixture_stress` only |
| Soft policies | `borrow_unused_event_id_FIFO`, `borrow_unused_proportional`, `soft_blend_pool_fraction_0_5` |

`161 * 31 + 9 = 5000`. The account is the imported 31-event development
cohort. Cash amounts are `Decimal`. A fund request stays all-or-nothing
inside the imported engine. Identity after every applied fund:

```
available + committed + non_trading_residual_bucket = C_total
```

The residual bucket stays 9. `draw_residual` raises. Ledger `cash_after`
and ledger `fee` are carried unread. Quote locks come from the imported
`fund_quote` path, which reads the feebook and the rails.

## Arms

### FX0 — `q3300_d0.25`

Join SR0, SR1, and SR2 under the Q6-`000` fill and order fixtures for
assumed queue 3300 and delay 0.25. Prefer the production gzip pair when
both files are on disk and their sha256 values match the factorial pin. A
different hash is refused. When the pair is absent, the harness reads the
synthetic schema stand-in in this lab. That stand-in is not the production
gzip and it is not a replay. The harsh twin `q10000` is not an arm.

### FX1 — `synthetic_borrow_stress`

The same three policies under a unit-only synthetic fixture that seats at
least one fill whose quote lock exceeds one event's unused soft reserve and
exceeds the SR2 local seat. The imported engine must log a cross-event
borrow on SR0 and SR1 and a blend-pool draw on SR2. This fixture is not a
market panel and not an invented cohort.

## Not arms

New soft_policy variants. A1 or A3. Queue 3300 versus 10000. Fee treatment
variants. Any Q6 signal change. Queue-fragility arms. A sum of N independent
wallets versus one shared 5000 USD account. A second Cap-SR lab.

## Instrument schema

Each joined fill carries SR0, SR1, and SR2. Each policy row records whether
the imported account seated the quote, whether that seat appended a
cross-event borrow, and whether it appended a blend-pool draw. `results` and
`pnl` on every row are null. The harness does not compute:

| Field | Later meaning |
|---|---|
| `borrow_count_delta_vs_fifo` | SR1 or SR2 borrow or blend-draw count minus SR0, under that fixture |
| `blend_utilization_gap` | Max minus min soft utilization across events |
| `soft_breach_or_blend_rate` | Fraction of fills that needed a cross-event borrow or a blend-pool draw |
| `effects_path_fixture_id` | Which fixture stress produced those metrics |

Those four fields stay null in `FROZEN_EXPERIMENT.json`, in
`results/EMPTY_RESULTS.json`, and on the join report. A per-fill borrow flag
is the instrument schema. It is not the Examiner scorecard. Raw log lengths
are not written into the freeze files.

## Promotion scoreboard

The scoreboard is the one shared account of 5000 USD. `pnl` is null.
`compare_independent_wallets_to_shared_account` raises
`IndependentWalletSumForbidden` and does not add wallets. Passing a wallet
list into `promotion_scoreboard` raises the same way. The three policy
accounts are three views of that shared total. They are not three wallets
to be summed.

## Live orders

No live order client, no Logan keys, and no `admit.py`.
`execution_adapter` raises `LiveOrdersForbidden`.

## Left untouched

`kalshi_soft_blended_reserves_000_lab_20260923`,
`kalshi_capital_structure_lab_20260922`, `kalshi_feebook_lab_20260922`,
`kalshi_rails_lab_20260922`, `nfl_factorial_lab_20260921` (Q6 `000`
included), `nfl_paircheck_lab_20260922`,
`kalshi_queue_fragility_000_lab_20260922`, the C1, C3, and C5 labs, and
`kalshi_r3p3_fl_maker_taker_lab_20260923`. No `000` retune. No
queue-fragility reopen. No A1 or A3 re-arm. No `000` or QF reopen.

## What a later result file may say

After the source freeze, a result file may record whether the unit tests
passed and may repeat these limitations. It may not report profit, may not
relabel development games, and may not mark an Examiner tape pass complete.
`results` and `pnl` stay null until that Examiner pass. S1 stays deferred.
