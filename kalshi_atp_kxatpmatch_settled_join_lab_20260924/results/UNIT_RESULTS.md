# ATP KXATPMATCH settled-resolution join unit results

September 24, 2026. This file records a code check of the join-gate
harness. It is a unit verification. It is not a simulated trading run and
not live validation. `FROZEN_EXPERIMENT.json` still has `results` null
and `pnl` null. `results/EMPTY_RESULTS.json` still has `settled_join_n`,
`occurrence_match_n`, `fallback_join_n`, `admit_ready_flag`, `results`,
and `pnl` null. `admitted_at` stays null. Those fields stay null on
purpose. This page is not profit. No tape walk was run. No P&L figure is
reported. This is not an Examiner score. No live measured count is
committed.

## Command

From `kalshi_atp_kxatpmatch_settled_join_lab_20260924`, Python 3, standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

```text
test_j0_and_j1_leave_the_scorecard_null (tests.test_orchestrator.ArmTests.test_j0_and_j1_leave_the_scorecard_null) ... ok
test_j1_fallback_is_labeled_and_does_not_write_occurrence (tests.test_orchestrator.ArmTests.test_j1_fallback_is_labeled_and_does_not_write_occurrence) ... ok
test_scout_n_is_not_settled_join_n (tests.test_orchestrator.ArmTests.test_scout_n_is_not_settled_join_n) ... ok
test_unknown_gate_and_scorecard_write_are_refused (tests.test_orchestrator.ArmTests.test_unknown_gate_and_scorecard_write_are_refused) ... ok
test_429_gap_is_recorded_and_not_filled (tests.test_orchestrator.MeasurementTests.test_429_gap_is_recorded_and_not_filled) ... ok
test_get_only_enforcement (tests.test_orchestrator.MeasurementTests.test_get_only_enforcement) ... ok
test_since_filter_and_j0_j1_counts_and_fallback_label (tests.test_orchestrator.MeasurementTests.test_since_filter_and_j0_j1_counts_and_fallback_label) ... ok
test_empty_results_and_frozen_stay_null (tests.test_orchestrator.PinTests.test_empty_results_and_frozen_stay_null) ... ok
test_panel_parent_bytes_match_and_admitted_at_stays (tests.test_orchestrator.PinTests.test_panel_parent_bytes_match_and_admitted_at_stays) ... ok
test_pins_present_and_digests_match (tests.test_orchestrator.PinTests.test_pins_present_and_digests_match) ... ok
test_capture_and_sibling_bytes_unchanged (tests.test_orchestrator.RefuseTests.test_capture_and_sibling_bytes_unchanged) ... ok
test_lee_ready_live_orders_admit_ungate_reopens_refused (tests.test_orchestrator.RefuseTests.test_lee_ready_live_orders_admit_ungate_reopens_refused) ... ok
test_list_gaps_and_fee_queue_book_fill_tape_are_not_filled (tests.test_orchestrator.RefuseTests.test_list_gaps_and_fee_queue_book_fill_tape_are_not_filled) ... ok

----------------------------------------------------------------------
Ran 13 tests in 0.031s

OK
```

Ran 13 tests in 0.031s. Recorded at 2026-09-25T00:01:05Z. Result: OK.
Failures: 0. Errors: 0.

## What the checks cover

The panel parent copy matches `lab/astra-capture/atp-kxatpmatch/panel_stub.json`,
sha256 `ed041c502d1f775d33c44bf900ac91b1339d99045bddd2052edd09a139ae2d3f`.
`panel_version` is `2026-09-23.atp-kxatpmatch-v0`. Top-level `admitted_at` stays
null. Stub status stays `NOT_ADMITTED`. 6 events and 12 markets. The
admit tool is refused.

J0 `nonempty_result_required` labels the 30 finalized scout markets whose
official `result` is `yes` or `no`. That label count is not
`settled_join_n`. J1 `occurrence_datetime_match` keeps
`occurrence_datetime` on those 30 rows. It equals
`expected_expiration_time` on all 30, and both raw values stay as returned.
`join_source` on those rows is `occurrence_datetime`.

The parent panel has 0 null `occurrence_datetime` rows, so the pinned
cohort does not exercise the fallback. A copied row with
`occurrence_datetime` set to null is labeled
`join_source=expected_expiration_time_fallback`. The raw
`expected_expiration_time` is not written into `occurrence_datetime`.
Assigning an `occurrence_datetime`, or writing the fallback clock into
that field, is refused.

Declared scout N=30 is not `settled_join_n`. `results` and `pnl` stay
null. `digest_all_match_claimed` is true because every hash listed in
`SOURCE_PINS.json` matches the in-repo bytes. The four mirror copies are
byte-identical. Calibration on the empty scorecard stays null with
`emits_probabilities` false.

The settled markets list `429` is not backfilled. Events page 2 is not
fetched. KXATPMATCH-26SEP22HARGAL and KXATPMATCH-26SEP22MOCKOT stay
outside N. Fee, queue, book, fill, and tape metrics stay HELD. Lee-Ready,
live orders, Logan keys, Cap-SR, ATP-FQ, other FQ features, sibling RJ
harnesses, and Arm B are refused. S1, S2, and R2-P4 stay gated. Examiner
status stays `HOLD_PRE_PR`. `stub_ready` stays false. The authentic
examiner hold bytes are not rewritten.

Measurement mode is covered with mocked HTTP only. A market settled at or
before `2026-09-24T23:52:00Z` is excluded. A scout pin ticker is excluded
even when its `settlement_ts` is after that instant. J0, occurrence
matches, and fallback labels are counted on the remaining rows. A 429 is
logged with backoff 10s, 20s, and 40s and the missing page is not
invented. POST and non-Kalshi hosts are refused before a transport call.
The committed empty scorecard bytes are unchanged. No live GET was issued
by this unit run.

## Limitation

The join-gate page reads pinned scout and panel bytes already in the
checkout. It does not fetch new market data and does not place orders.
It does not admit the panel. It does not turn the 30 settled labels into
`settled_join_n`. Measurement mode can compute post-ACCEPT counts, and
this run did not execute it against the public host. Those counts stay
out of the committed scorecard until a later run after Clock admit, which
Examiner scores. `admitted_at` stays null and admit_ready stays pending
Clock. A later READY state is NOT_SCORED only, and only after a branch
sha check and merge. This page is not that score.
