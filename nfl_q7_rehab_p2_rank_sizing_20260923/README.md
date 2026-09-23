# Q7 Arm B rehab, pass 2: portfolio-rank sizing

Status: **hypothesis committed, not scored**. This directory does not contain
rehab profit. `EXPERIMENT_SPEC.md` is the hypothesis. `FROZEN_EXPERIMENT.json`
keeps `results` and `pnl` null. Q7 Arm B stays the killed parent,
CEM-ASTRA-20260922-001. Pass 1 `admission_cadence` stays closed.

The Refiner freeze, diagnosis, and Simulator hand are in this checkout under
`packets/refiner/`. `FROZEN_EXPERIMENT.json` records each verified sha256.
Those packet bytes were copied. They were not invented. The Examiner P1 KILL
ack, the Conductor Pass-2 kick, and the 3-pass rehab policy are cited by the
hand and are absent here.

## Knob

`portfolio_rank_sizing` only.

| Arm | What it is |
|---|---|
| B0 | Imported Q7 Arm B. Original router, pair check on, continuous refresh, full `wanted`. |
| B2 | Same as B0, except chosen-leg size is the allocation capital-budget fraction. Q6 label `000` rank semantics. No Pass-1 cadence gate. |
| D | Imported Q7 Arm D. Q6 label `000` with the combined-cost check on. |

Route choice, the combined-cost margin, order size, cushion, fees, the 31-game
development cohort, and the four Q7 stresses stay put. `nfl_paircheck_lab_20260922`,
`nfl_factorial_lab_20260921`, and `nfl_q7_rehab_p1_cadence_20260923` are
read-only pins.

Fixed account: $5,000. Stresses: `q3300_d0.25`, `q3300_d5`, `q10000_d0.25`,
`q10000_d5`. Twelve scenarios. The selection bar requires B2 above B0 on every
stress, B2 at least 95 percent of D on every stress, and B2 unhedged
contract-hours at most 1.25 times B0. Anything short of it is
`NO_NEW_SELECTION`, fallback shadow `000`, `live_promotion` false. This freeze
does not apply that bar to outcomes. There are none.

## Tests that run without the historical kit

From this directory, Python 3.12 standard library:

```bash
python3 -m unittest -v test_rank_sizing
```

Those tests cover budget fractioning, the imported feebook refusal, null freeze
fields, parent hash pins, and the closed Pass-1 cadence gate. They do not
replay the 31 games. The recorded run is in `results/UNIT_RESULTS.md`. That
file is code verification. It is not a score.

## Score run

This freeze refuses the tape walk:

```bash
python3 run_experiment.py
```

That writes `results/NOT_RUN.json` with `pnl` and `results` null and exits 3.
`execute_score_run()` raises `ScoreRunRefused`. The Examiner runs the twelve
scenarios in a later pass. Parent Q7 Arm B and Arm D ledger blobs are not on
main and were not committed. `waive_parent_ledger_hash_check` is false. The
conductor source-pin manifest records their sha256 values. That absence is not
a positive-control pass, and this lab does not invent their hashes.

No live orders, credentials, or holdout outcomes are used.
