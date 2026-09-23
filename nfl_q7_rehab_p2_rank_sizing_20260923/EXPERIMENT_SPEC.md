# Q7 Arm B rehab, pass 2: portfolio-rank capital-budget sizing

September 23, 2026. This specification is the hypothesis. It is committed before
the rehab source is frozen and before any rehab scenario is executed. No P&L
in this document is a rehab result. Q7 Arm B remains the killed parent
(CEM-ASTRA-20260922-001). Pass 1 (`admission_cadence` = 600) is a dead knob.
This pass does not relabel either kill as a profit.

Packet `Q7-B-REHAB-P2-PORTFOLIO-RANK-SIZING`. The Refiner freeze, diagnosis,
and Simulator hand are copied under `packets/refiner/`:

- `packets/refiner/REFINER_PASS2_FREEZE_Q7_B_PORTFOLIO_RANK_SIZING_2026-09-23.md`
- `packets/refiner/REFINER_PASS2_DIAGNOSIS_Q7_ARM_B_2026-09-23.md`
- `packets/refiner/REFINER_HAND_SIMULATOR_Q7_B_PASS2_RANK_SIZING_2026-09-23.json`

The hand cites `packets/EXAMINER_ACK_Q7_B_REHAB_P1_TAPE_WALK_KILL_2026-09-23.json`,
`packets/CONDUCTOR_KICK_REFINER_Q7_B_PASS2_2026-09-23.json`, and
`packets/refiner/REHAB_POLICY_3PASS_2026-09-23.md`. Those three paths are absent
from this checkout. This file does not invent their bytes.

Do not modify `nfl_paircheck_lab_20260922`, `nfl_factorial_lab_20260921`,
`nfl_q7_rehab_p1_cadence_20260923`, or `SHADOW_CANDIDATE_FREEZE.json`. This
directory imports those modules read-only. A hash mismatch against the pins in
`FROZEN_EXPERIMENT.json` is a failed control, not permission to edit the older
tree.

## Question

Holding original-router route selection, pair-check on, and continuous
new-exposure admission (the Pass-1 cadence gate stays closed), does switching
only baseline full-`wanted` sizing to portfolio-rank capital-budget sizing
retain Q6 label `000` on the development cohort?

The parent failure is Q7 Arm B. Pass 1 already asked whether a 600-second
admission cadence, alone, closes the gap to Arm D. It does not. This pass
isolates sizing. Nothing else moves.

## One knob

`portfolio_rank_sizing`.

| Arm | What it is | Knob |
|---|---|---|
| B0 | Q7 Arm B / Pass-1 B0, imported. Original router, pair check on, continuous refresh, full chosen-leg `wanted`. | None. Positive control. |
| B2 | Same as B0, except each refresh sizes chosen legs on the allocation capital-budget path. | `portfolio_rank_sizing` only. |
| D | Q7 Arm D, imported. Q6 label `000` with the combined-cost check on. | None. Retention reference. Do not edit the `000` freeze. |

B1 is not an arm. `RehabCadenceReplay`, `admission_cadence`, and a cadence of
600 seconds are the closed Pass-1 gate. Requesting B1 is an error.

B0 and D are parent instances. B2 subclasses the parent original-router check.
`choose()`, the per-direction route screen, the combined-cost margin, order
size, cushion, fees, the 31-game development cohort, the four stresses, and
the selection bar do not move. F, P, and R stay off.

The margin stays the parent expression, evaluated on the two routes `choose()`
returned:

```
margin = 1 - (cost of chosen leg 1 + cost of chosen leg 2)
         - 0.0002 - 2 * balance_precision / order_size
```

`cost` remains `price + maker_coefficient * price * (1 - price)`. The cushion
quantity remains the configured order size. A non-positive margin still blocks
new paired exposure and still leaves an offset leg admissible.

## Sizing rule

B2 keeps `OriginalPairCheck` admission. The check still decides which new
paired-exposure keys may be submitted. It does not wait for
`now >= next_allocation`. A refresh with a passing pair submits on that
refresh. A working order is not pulled because a budget clock is closed. Offset
legs stay admissible. The gate does not add a cancel loop and does not read a
later quote.

Size, and only size, comes from the imported allocation branch:

1. Rank with Q6 label `000` semantics. B2 calls `FactorialReplay.portfolio_rank`
   with `Factors(False, False, False)`. Flow off does not invent a rate.
   Protection off does not hold entry cash back for offsets. Ranking off sets
   `adjusted` to the neutral value 1. Event id is the tie break. A non-positive
   combined margin still returns no rank. This call does not copy the `000`
   function and does not edit it.
2. Budget with the imported `FactorialReplay.rebalance` body: event cash
   budgets are `min(remaining, rank capital)` in neutral order. The imported
   function also returns early while `next_allocation` is in the future and
   then sets `next_allocation = now + 600`. That clock is the Pass-1 admission
   cadence. B2 clears `next_allocation` before the call, so the body runs on
   this refresh, and clears it again after the call, so the clock is not left
   armed. The clear is the closed gate. It is not a second sizing rule.
3. Fraction with the imported `AdaptiveReplay.refresh` path for
   `experiment == 'allocation'`. On the chosen legs,

```
total = sum(wanted * (cost + 0.0001) + balance_precision)
fraction = 0 if total == 0 else min(1, allocations[event] / total)
quantity = floor_qty(wanted * fraction)
```

`floor_qty` is the imported helper. An offset leg (`direction * holdings < 0`)
then keeps the imported offset floor: `quantity = max(quantity, offset room)`
from `bounded_quantity(candidate, 0)`. Offset inventory is protected inside
that branch even when protection is off and even when the entry budget is zero.

B0 never takes this branch. Its refresh is the parent continuous full-`wanted`
path. D keeps the parent allocator, including that class's own rebalance
clock. This pass does not retune D and does not make B2 into D.

## Fixed design

Twelve scenarios. Arms do not share fills.

- Starting cash $5,000. One pooled account per replay.
- The Q6 31-game development cohort (16 Week 1, 15 Week 2). Not a holdout.
  Do not read `RESERVED_HOLDOUT.json` outcomes. Do not admit or drop games
  after looking at results.
- Desired order size 250, hard event exposure 250, assumed total exit depth
  250 per game.
- Inherited fee model, balance precision, candle quotes, five-minute
  liquidation lead, participation 0.5, and the Q6 last-12-hour queue.
- Stresses, same four as Q7: `q3300_d0.25`, `q3300_d5`, `q10000_d0.25`,
  `q10000_d5`. Submit and cancel delays move together.

Scenario names are `{stress}_{arm}`:

1. `q3300_d0.25_{B0,B2,D}`
2. `q3300_d5_{B0,B2,D}`
3. `q10000_d0.25_{B0,B2,D}`
4. `q10000_d5_{B0,B2,D}`

No paid data, live orders, credentialed trading, external predictors, or
multi-wallet simulation. No parameter search after any output exists.

Historical inputs remain the Q6 normalized kit under
`nfl_factorial_lab_20260921/inputs/`. Those bytes are not copied here. This
freeze PR does not walk that tape. The score entry point raises
`ScoreRunRefused`. The Examiner runs the twelve scenarios in a later pass.
A missing tape, when that pass exists, writes a not-run status and invents
no fills, cash, or P&L.

## Metrics and selection

Report these only from an actual replay. Unresolved inventory makes
`completed_strategy_pnl` null. Null is not zero and is not a profit. Losses
stay negative. Rejection margins stay out of the cash ledger. Completed profit
requires the imported feebook fee channel. A missing channel is a refusal,
not a completed profit. A document that carries `results`, `pnl`, or
`completed_strategy_pnl` through the freeze path is refused.

Apply the candidate rule only when all twelve scenarios are flat and each has
a non-null `completed_strategy_pnl`. Otherwise the status is
`NO_NEW_SELECTION`, the fallback shadow is Q6 label `000`, and
`live_promotion` is false. This freeze has no outcomes, so the rule is not
applied to a score.

B2 becomes a development shadow candidate only when all of the following hold:

- B2's completed P&L is strictly above B0's in every stress.
- D's completed P&L is strictly positive in every stress, and B2's completed
  P&L is at least 95 percent of D's in every stress.
- On `q3300_d0.25`, both week contributions of B2 are strictly above B0's.
- B2's unhedged contract-hours are at most 1.25 times B0's in every stress.

There is no live promotion either way. A passing B2 is still only a candidate
for a later prospective shadow. Failing the bar leaves `000` in place. This
study does not soften the 95 percent bar and does not drop B2 > B0 after
seeing output. This freeze contains no output.

## Positive controls

When a real run exists, compare it before interpreting the sizing effect.

- B0 must reproduce Q7 Arm B / Pass-1 B0 where those ledgers exist: summaries
  `q{queue}_d{delay}_B`, on completed net, flatness, unresolved size, week
  contributions, unhedged contract-hours, and uncompressed fill, order, and
  decision hashes. The rehab sizing side is not part of B0.
- D must reproduce Q7 Arm D where those ledgers exist:
  `q{queue}_d{delay}_D`, on the same fields and uncompressed fill, order, and
  decision hashes. D is Q6 `000` plus the parent check. Do not edit the `000`
  freeze to make D match.
- Parent hashes are the conductor manifest
  `packets/refiner/PARENT_Q7_BD_LEDGER_SOURCE_PINS_2026-09-23.json`.
  `waive_parent_ledger_hash_check` is false. The ledger blobs are not in this
  checkout and are not committed. Absence is not a match and is not a pass.
  Do not invent ledger hashes.
- A control mismatch on a real run is a failed reproduction. It is not a
  rehab finding.

Unit tests may check budget fractioning on synthetic books, the closed
Pass-1 gate, the imported fee refusal, null freeze fields, and the one-knob
invariant. They are not the twelve-scenario result.

## Forward boundary

No always-on collector is running. This experiment does not admit games,
deploy a recorder, or place orders. Fresh-game validation remains a separate
gate.
