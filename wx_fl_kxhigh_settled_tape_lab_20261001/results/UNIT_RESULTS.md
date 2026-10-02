# WX-FL unit results

Not an Examiner score. Code verification only. `results` and `pnl` stay null. Zero GETs. Zero orders.

Command: `python3 -m unittest discover -s tests -v`

Run at: 2026-10-02T00:06:52Z

```
test_gm_cov_requires_a_spanning_complete_later_poll (test_gap_mapping.GapMappingTests.test_gm_cov_requires_a_spanning_complete_later_poll) ... ok
test_gm_lit_boundaries_and_open_and_storm (test_gap_mapping.GapMappingTests.test_gm_lit_boundaries_and_open_and_storm) ... ok
test_gm_lit_pad_widens_budget_only (test_gap_mapping.GapMappingTests.test_gm_lit_pad_widens_budget_only) ... ok
test_open_window_is_never_proven_and_cursor_minus_one_is_not_assumed (test_gap_mapping.GapMappingTests.test_open_window_is_never_proven_and_cursor_minus_one_is_not_assumed) ... ok
test_storm_proof_is_per_ticker (test_gap_mapping.GapMappingTests.test_storm_proof_is_per_ticker) ... ok
test_no_module_imports_a_network_client (test_imports.ImportBoundaryTests.test_no_module_imports_a_network_client) ... ok
test_sqlite3_is_imported_only_by_the_snapshot_loader (test_imports.ImportBoundaryTests.test_sqlite3_is_imported_only_by_the_snapshot_loader) ... ok
test_live_db_and_capture_are_refused_before_open (test_orchestrator.AuthorityTests.test_live_db_and_capture_are_refused_before_open) ... ok
test_pins_manifest_accept_ruling_and_bundle (test_orchestrator.AuthorityTests.test_pins_manifest_accept_ruling_and_bundle) ... ok
test_sha_mismatch_does_not_open_sqlite (test_orchestrator.AuthorityTests.test_sha_mismatch_does_not_open_sqlite) ... ok
test_vendored_text_matches_the_bundle_manifest (test_orchestrator.AuthorityTests.test_vendored_text_matches_the_bundle_manifest) ... ok
test_count_files_keep_results_null_and_omit_prices (test_orchestrator.RealTapeCountTests.test_count_files_keep_results_null_and_omit_prices) ... ok
test_gm_cov_reports_unproven_windows_without_loosening (test_orchestrator.RealTapeCountTests.test_gm_cov_reports_unproven_windows_without_loosening) ... ok
test_published_card_stays_null (test_orchestrator.RealTapeCountTests.test_published_card_stays_null) ... ok
test_snapshot_open_is_readonly (test_orchestrator.RealTapeCountTests.test_snapshot_open_is_readonly) ... ok
test_timestamp_universe_and_gap_sensitivities (test_orchestrator.RealTapeCountTests.test_timestamp_universe_and_gap_sensitivities) ... ok
test_admit1_no_result_post_close_block_and_conflict (test_orchestrator.RefusalTests.test_admit1_no_result_post_close_block_and_conflict) ... ok
test_live_order_http_get_lee_ready_and_rebin_raise (test_orchestrator.RefusalTests.test_live_order_http_get_lee_ready_and_rebin_raise) ... ok
test_registry_boundaries (test_orchestrator.RefusalTests.test_registry_boundaries) ... ok
test_result_disagreement_is_a_hard_fail (test_orchestrator.RefusalTests.test_result_disagreement_is_a_hard_fail) ... ok
test_measure_synthetic_is_the_only_roi_entry_and_conduct_does_not_call_it_on_tape (test_orchestrator.SourceShapeTests.test_measure_synthetic_is_the_only_roi_entry_and_conduct_does_not_call_it_on_tape) ... ok
test_equal_weighted_differs_from_trade_weighted_and_sep25_split (test_orchestrator.SyntheticMetricTests.test_equal_weighted_differs_from_trade_weighted_and_sep25_split) ... ok
test_locdo_reading_ignores_lodo_and_loco (test_orchestrator.SyntheticMetricTests.test_locdo_reading_ignores_lodo_and_loco) ... ok
test_threshold_is_six_of_eight_and_h2_is_less_or_equal (test_orchestrator.SyntheticMetricTests.test_threshold_is_six_of_eight_and_h2_is_less_or_equal) ... ok

----------------------------------------------------------------------
Ran 24 tests in 12.977s

OK
```
