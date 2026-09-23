# Q7 Arm B rehab, pass 1: 600s admission cadence

September 23, 2026. This specification is the hypothesis. It is committed before
the rehab source is frozen and before any rehab scenario is executed. No P&L
in this document is a rehab result. Q7 Arm B remains the killed parent
(CEM-ASTRA-20260922-001). This pass does not relabel that kill as a profit.

The Conductor GO named these packet paths as accepted:

- `packets/refiner/REFINER_PASS1_FREEZE_Q7_B_CADENCE_600_2026-09-23.md`
- `packets/refiner/CONDUCTOR_ACCEPT_Q7_B_REHAB_P1_CADENCE_600_2026-09-23.json`
- `packets/refiner/REFINER_PASS1_DIAGNOSIS_Q7_ARM_B_2026-09-23.md`

Those paths are absent from `origin/main` at `438f4ab`. This file is the
hypothesis committed from that GO. It is not a reconstructed conductor stamp,
and it does not invent an accept JSON.

Do not modify `nfl_paircheck_lab_20260922`, `nfl_factorial_lab_20260921`, or
`SHADOW_CANDIDATE_FREEZE.json`. This directory imports those modules read-only.
A hash mismatch against the pins in `FROZEN_EXPERIMENT.json` is a failed
control, not permission to edit the older tree.

## Question

Does withholding new paired exposure on the original router until a 600-second
entry-budget cadence, leaving route choice and the chosen-pair cost check
unchanged, retain Q6 label `000` on the development cohort?

The parent failure is Q7 Arm B: original router, pair check on, continuous
`AdaptiveReplay` refresh. The allocator's ten-minute entry budget is the
scheduling difference this pass isolates. Nothing else moves.

## One knob

`admission_cadence`.

| Arm | What it is | Knob |
|---|---|---|
| B0 | Q7 Arm B, imported. Original router, pair check on, continuous refresh. | None. Positive control. |
| B1 | Same as B0, except new paired exposure is admitted only when `now >= next_allocation`. On that admit attempt, `next_allocation = now + 600`. | `admission_cadence` = 600 seconds. |
| D | Q7 Arm D, imported. Q6 label `000` with the combined-cost check on. | None. Retention reference. Do not edit the `000` freeze. |

B0 and D are parent instances. B1 subclasses the parent original-router check
and adds only the cadence gate. `choose()`, the per-direction route screen,
the combined-cost margin, order size, cushion, fees, the 31-game development
cohort, the four stresses, and the selection bar do not move.

The margin stays the parent expression, evaluated on the two routes `choose()`
returned:

```
margin = 1 - (cost of chosen leg 1 + cost of chosen leg 2)
         - 0.0002 - 2 * balance_precision / order_size
```

`cost` remains `price + maker_coefficient * price * (1 - price)`. The cushion
quantity remains the configured order size. A non-positive margin still blocks
new paired exposure and still leaves an offset leg admissible. The cadence
does not replace that check and does not re-rank.

## Cadence rule

`next_allocation` starts at the inherited negative infinity, so the first
finite decision time is inside the window.

When a refresh has at least one chosen leg that is new paired exposure
(`direction * holdings >= 0`):

- If `now >= next_allocation`, this refresh is an admit attempt. Set
  `next_allocation = now + 600` before the parent admission path runs. The
  slot is consumed even when the combined-cost check then rejects the pair.
  That matches the inherited allocator entry budget, which advances the clock
  at the start of the attempt.
- If `now < next_allocation`, do not submit a new-exposure order that is not
  already working. Record the block with `counted_as_pnl: false`. Do not
  advance `next_allocation`.

Offset legs stay on the continuous parent path. A working order is not pulled
because the cadence window is closed. The gate does not add a cancel loop, does
not read a later quote, and does not require both legs to be fillable together.
A refresh with no new paired exposure does not consume the slot.

B0 never writes `next_allocation`. Its refresh is the parent continuous path.
D keeps the parent allocator, including that class's own rebalance clock. This
pass does not retune D.

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

1. `q3300_d0.25_{B0,B1,D}`
2. `q3300_d5_{B0,B1,D}`
3. `q10000_d0.25_{B0,B1,D}`
4. `q10000_d5_{B0,B1,D}`

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
stay negative. Rejection margins and cadence blocks stay out of the cash
ledger. Completed profit requires the imported feebook fee channel. A missing
channel is a refusal, not a completed profit.

Apply the candidate rule only when all twelve scenarios are flat and each has
a non-null `completed_strategy_pnl`. Otherwise the status is
`NO_NEW_SELECTION`, the fallback shadow is Q6 label `000`, and
`live_promotion` is false.

B1 becomes a development shadow candidate only when all of the following hold:

- B1's completed P&L is strictly above B0's in every stress.
- D's completed P&L is strictly positive in every stress, and B1's completed
  P&L is at least 95 percent of D's in every stress.
- On `q3300_d0.25`, both week contributions of B1 are strictly above B0's.
- B1's unhedged contract-hours are at most 1.25 times B0's in every stress.

There is no live promotion either way. A passing B1 is still only a candidate
for a later prospective shadow. Failing the bar leaves `000` in place. This
study does not soften the bar after seeing output, and this freeze contains
no output.

## Positive controls

When a real run exists, compare it before interpreting the cadence effect.

- B0 must reproduce Q7 Arm B where those ledgers exist: summaries
  `q{queue}_d{delay}_B`, on completed net, flatness, unresolved size, week
  contributions, unhedged contract-hours, and uncompressed fill, order, and
  decision hashes. The rehab cadence side ledger is not part of B0.
- D must reproduce Q7 Arm D where those ledgers exist:
  `q{queue}_d{delay}_D`, on the same fields and uncompressed fill, order, and
  decision hashes. D is Q6 `000` plus the parent check. Do not edit the `000`
  freeze to make D match.
- Parent Q7 result bytes are not in this checkout (`results/NOT_RUN.json`
  only). Absence is not a match and is not a pass. Do not invent ledger hashes.
- A control mismatch on a real run is a failed reproduction. It is not a
  rehab finding.

Unit tests may check the cadence gate on synthetic books, the imported fee
refusal, null freeze fields, and the one-knob invariant. They are not the
twelve-scenario result.

## Forward boundary

No always-on collector is running. This experiment does not admit games,
deploy a recorder, or place orders. Fresh-game validation remains a separate
gate.
