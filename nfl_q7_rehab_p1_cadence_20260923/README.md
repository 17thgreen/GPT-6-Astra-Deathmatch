# Q7 Arm B rehab, pass 1: 600s admission cadence

Status: **hypothesis committed, source frozen, not scored**. This directory does
not contain rehab profit. `EXPERIMENT_SPEC.md` is the hypothesis.
`FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null. Q7 Arm B stays the
killed parent, CEM-ASTRA-20260922-001.

The Conductor paths named in the GO (`packets/refiner/REFINER_PASS1_*` and
`CONDUCTOR_ACCEPT_Q7_B_REHAB_P1_CADENCE_600_2026-09-23.json`) are not in this
checkout. This lab does not invent those bytes.

## Knob

`admission_cadence` only.

| Arm | What it is |
|---|---|
| B0 | Imported Q7 Arm B. Original router, pair check on, continuous refresh. |
| B1 | Same as B0, except new paired exposure waits for `now >= next_allocation`, and an admit attempt sets `next_allocation = now + 600`. |
| D | Imported Q7 Arm D. Q6 label `000` with the combined-cost check on. |

Route choice, the combined-cost margin, order size, cushion, fees, the 31-game
development cohort, and the four Q7 stresses stay put. `nfl_paircheck_lab_20260922`
and `SHADOW_CANDIDATE_FREEZE.json` are read-only pins.

Fixed account: $5,000. Stresses: `q3300_d0.25`, `q3300_d5`, `q10000_d0.25`,
`q10000_d5`. Twelve scenarios, not sixteen. The selection bar is the GO bar.
Anything short of it is `NO_NEW_SELECTION`, fallback shadow `000`,
`live_promotion` false.

## Tests that run without the historical kit

From this directory, Python 3.12 standard library:

```bash
python3 -m unittest -v test_cadence
```

Those tests cover the 600s block-then-admit gate, the imported feebook refusal
when a scorecard has no fee channel, null freeze fields, parent hash pins, and
the one-knob invariant. They do not replay the 31 games.

## Score run

This freeze refuses the tape walk:

```bash
python3 run_experiment.py
```

That writes `results/NOT_RUN.json` with `pnl` and `results` null and exits 3.
`execute_score_run()` raises `ScoreRunRefused`. The Examiner runs the twelve
scenarios in a later pass. Parent Q7 Arm B and Arm D ledgers are not in this
checkout. That absence is not a positive-control pass, and this lab does not
invent their hashes.

No live orders, credentials, or holdout outcomes are used.
