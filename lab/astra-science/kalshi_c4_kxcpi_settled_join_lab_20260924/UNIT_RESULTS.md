# C4 KXCPI settled-resolution join unit results

September 24, 2026. This file records a code check of the join-gate
harness. It is a unit verification. It is not a simulated trading run and
not live validation. `FROZEN_EXPERIMENT.json` still has `results` null
and `pnl` null. `results/EMPTY_RESULTS.json` still has `settled_join_n`,
`occurrence_match_n`, `admit_ready_flag`, `results`, and `pnl` null.
`admitted_at` stays null. Those fields stay null on purpose. This page is
not profit. No tape walk was run. No P&L figure is reported. This is not
an Examiner score.

## Command

From `kalshi_c4_kxcpi_settled_join_lab_20260924`, Python 3, standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

```text
test_j0_and_j1_leave_the_scorecard_null (tests.test_orchestrator.ArmTests.test_j0_and_j1_leave_the_scorecard_null) ... ok
test_j1_fallback_is_labeled_and_does_not_write_occurrence (tests.test_orchestrator.ArmTests.test_j1_fallback_is_labeled_and_does_not_write_occurrence) ... ok
test_scout_n_is_not_settled_join_n (tests.test_orchestrator.ArmTests.test_scout_n_is_not_settled_join_n) ... ok
test_unknown_gate_and_scorecard_write_are_refused (tests.test_orchestrator.ArmTests.test_unknown_gate_and_scorecard_write_are_refused) ... ok
test_empty_results_and_frozen_stay_null (tests.test_orchestrator.PinTests.test_empty_results_and_frozen_stay_null) ... ok
test_panel_parent_bytes_match_and_admitted_at_stays (tests.test_orchestrator.PinTests.test_panel_parent_bytes_match_and_admitted_at_stays) ... ok
test_pins_present_and_digests_match (tests.test_orchestrator.PinTests.test_pins_present_and_digests_match) ... ok
test_capture_and_sibling_bytes_unchanged (tests.test_orchestrator.RefuseTests.test_capture_and_sibling_bytes_unchanged) ... ok
test_lee_ready_live_orders_admit_ungate_reopens_refused (tests.test_orchestrator.RefuseTests.test_lee_ready_live_orders_admit_ungate_reopens_refused) ... ok
test_list_gaps_and_fee_queue_book_fill_tape_are_not_filled (tests.test_orchestrator.RefuseTests.test_list_gaps_and_fee_queue_book_fill_tape_are_not_filled) ... ok

----------------------------------------------------------------------
Ran 10 tests in 0.026s

OK
```

Ran 10 tests in 0.026s. Recorded at 2026-09-24T23:38:32Z. Result: OK.
Failures: 0. Errors: 0.

## What the checks cover

The panel parent copy matches `lab/astra-capture/c4-kxcpi/panel_stub.json`,
sha256 `b20b0cbee50c127d2e9bb2548b574b7d643cc708f54019d53bd91775f9762c13`.
`panel_version` is `2026-09-23.c4-kxcpi-v0`. Top-level `admitted_at` stays
null. Stub status stays `NOT_ADMITTED`. 4 events and 44 markets. The
admit tool is refused.

J0 `nonempty_result_required` labels the 25 finalized scout markets whose
official `result` is `yes` or `no`. That label count is not
`settled_join_n`. J1 `occurrence_datetime_match` keeps
`occurrence_datetime` on those 25 rows. It differs from
`expected_expiration_time` on all 25, and both raw values stay as returned.
`join_source` on those rows is `occurrence_datetime`.

21 parent-panel markets omit `occurrence_datetime`. Each of those J1 rows
is labeled `join_source=expected_expiration_time_fallback`. The raw
`expected_expiration_time` is not written into `occurrence_datetime`.
Seven of those rows are KXCPI-26SEP. Assigning an `occurrence_datetime`
is refused.

Declared scout N=25 is not `settled_join_n`. `results` and `pnl` stay
null. `digest_all_match_claimed` is true because every hash listed in
`SOURCE_PINS.json` matches the in-repo bytes. The four mirror copies are
byte-identical.

KXCPI-26JUN, KXCPI-26MAY, and KXCPI-26APR stay missing. The settled
markets list `429` is not backfilled. Fee, queue, book, fill, and tape
metrics stay HELD. Lee-Ready, live orders, Logan keys, Cap-SR, CPI-FQ,
other FQ features, sibling RJ harnesses, and Arm B are refused. S1, S2,
and R2-P4 stay gated. Examiner status stays `HOLD_PRE_PR`. `stub_ready`
stays false. The authentic examiner hold bytes are not rewritten.

## Limitation

This run reads pinned scout and panel bytes already in the checkout. It
does not fetch new market data and does not place orders. It does not
admit the panel. It does not turn the 25 settled labels or the 21
fallback labels into `settled_join_n` or `occurrence_match_n`. A later
READY state is NOT_SCORED only, and only after a branch sha check and
merge. This page is not that score.
