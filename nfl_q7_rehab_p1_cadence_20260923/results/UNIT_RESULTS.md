# Q7 Arm B rehab pass 1 unit results

Code verification only. Not an Examiner score. Not a tape walk. Not a P&L.

Command, from `nfl_q7_rehab_p1_cadence_20260923/`:

```bash
python3 -m unittest -v test_cadence
```

Ran 10 tests in 0.010s at 2026-09-23T19:11:11Z. Result: OK. Failures: 0. Errors: 0.

Covered:

- 600s cadence blocks a new paired-exposure submit, then admits when `now >= next_allocation` and sets the next slot 600s later.
- A rejected combined-cost attempt still consumes the slot. The rejection margin is not cash.
- A closed window does not cancel a working order and still allows an offset quote.
- `choose()`, combined-cost margin, order size, and baseline routing are unchanged. B1 does not enable ranking.
- B0 is the imported Q7 `OriginalPairCheck`. D is the imported Q7 `AllocatorPairCheck` at label `000`.
- Freeze `results` and `pnl` are null. A non-null stamp is refused.
- `execute_score_run()` raises. `execute()` writes `NOT_RUN.json` with zero scenarios.
- Imported `feebook.classify_scorecard` refuses a completed-profit label when the fee channel is missing.
- Parent Q7 Arm B and Arm D ledger blobs are absent from this checkout. `all_checks_passed` is null. Absence is not a pass. `waive_parent_ledger_hash_check` is false. The conductor source-pin manifest is present; its hashes were not invented, and the blobs were not committed.
- The selection helper returns `NO_NEW_SELECTION` when a stress misses the frozen bar. It does not write `pnl`.

`FROZEN_EXPERIMENT.json` `results` and `pnl` stayed null after this run. Parent `nfl_paircheck_lab_20260922` and `SHADOW_CANDIDATE_FREEZE.json` were not edited. No live orders were sent.
