# Q7 Arm B rehab pass 2 unit results

Code verification only. Not an Examiner score. Not a tape walk. Not a P&L.

Command, from `nfl_q7_rehab_p2_rank_sizing_20260923/`:

```bash
python3 -m unittest -v test_rank_sizing
```

Ran 11 tests in 0.009s at 2026-09-23T21:44:39Z. Result: OK. Failures: 0. Errors: 0.

Covered:

- Entry-budget fraction is `min(1, allocations[event] / total)` and `floor_qty(wanted * fraction)`. A short two-event budget cuts H below full `wanted` while B0 on the same book stays at full `wanted`. Neutral `adjusted` is 1. Protection holdback is 0.
- When one event's capital fits in cash, B2 order size matches B0.
- A rejected pair does not become cash. An offset leg is still quoted when the entry budget is zero.
- A future `next_allocation` does not block a new submit. The next refresh still rebalances. B2 has no `RehabCadenceReplay` and no admission-cadence seconds.
- `choose()`, combined-cost margin, and order size are unchanged. Rank matches imported `FactorialReplay` with `Factors(False, False, False)`. Requesting B1 raises.
- B0 is the imported Q7 `OriginalPairCheck`. D is the imported Q7 `AllocatorPairCheck` at label `000`.
- Freeze `results` and `pnl` are null. A non-null stamp is refused. The one knob is `portfolio_rank_sizing`.
- `execute_score_run()` raises. `execute()` writes `NOT_RUN.json` with zero scenarios. A document carrying `pnl`, `results`, or `completed_strategy_pnl` is refused.
- Imported `feebook.classify_scorecard` refuses a completed-profit label when the fee channel is missing.
- Parent Q7 Arm B and Arm D ledger blobs are absent from this checkout. `all_checks_passed` is null. Absence is not a pass. `waive_parent_ledger_hash_check` is false. `PARENT_Q7_BD_LEDGER_SOURCE_PINS_2026-09-23.json` is present; its hashes were not invented, and the blobs were not committed.
- The selection helper returns `NO_NEW_SELECTION` when a supplied stress misses B2 > B0, 95 percent of D, or the 1.25 inventory cap. It does not write `pnl`. It was not run on rehab outcomes.

`FROZEN_EXPERIMENT.json` `results` and `pnl` stayed null after this run. Parent `nfl_paircheck_lab_20260922`, `nfl_factorial_lab_20260921`, and `nfl_q7_rehab_p1_cadence_20260923` were not edited. No live orders were sent.
