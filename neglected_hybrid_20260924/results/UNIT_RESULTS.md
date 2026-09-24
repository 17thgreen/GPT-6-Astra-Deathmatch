# Verification

Run 2026-09-24T05:29:50.158918+00:00

```text
test_boundary_quotes_refuse_absent_side_midpoint (test_core.CausalAndLedgerTests.test_boundary_quotes_refuse_absent_side_midpoint) ... ok
test_closed_contract_refused (test_core.CausalAndLedgerTests.test_closed_contract_refused) ... ok
test_conflicting_forecasts_refused (test_core.CausalAndLedgerTests.test_conflicting_forecasts_refused) ... ok
test_duplicate_race_refused (test_core.CausalAndLedgerTests.test_duplicate_race_refused) ... ok
test_forecast_lag_rejects_latest (test_core.CausalAndLedgerTests.test_forecast_lag_rejects_latest) ... ok
test_future_stale_crossed_and_missing_quote (test_core.CausalAndLedgerTests.test_future_stale_crossed_and_missing_quote) ... ok
test_hybrid_score_and_frozen_cost_stress (test_core.CausalAndLedgerTests.test_hybrid_score_and_frozen_cost_stress) ... ok
test_logloss_only_clipped (test_core.CausalAndLedgerTests.test_logloss_only_clipped) ... ok
test_loss_debits_principal_and_costs (test_core.CausalAndLedgerTests.test_loss_debits_principal_and_costs) ... ok
test_market_mid_abstains (test_core.CausalAndLedgerTests.test_market_mid_abstains) ... ok
test_no_reciprocity_and_cash (test_core.CausalAndLedgerTests.test_no_reciprocity_and_cash) ... ok
test_postdecision_and_unproven_forecasts_rejected (test_core.CausalAndLedgerTests.test_postdecision_and_unproven_forecasts_rejected) ... ok
test_probability_nan_rejected (test_core.CausalAndLedgerTests.test_probability_nan_rejected) ... ok
test_stale_forecast_rejected (test_core.CausalAndLedgerTests.test_stale_forecast_rejected) ... ok
test_strict_margin_threshold (test_core.CausalAndLedgerTests.test_strict_margin_threshold) ... ok
test_timezone_required (test_core.CausalAndLedgerTests.test_timezone_required) ... ok
test_unresolved_is_not_zero_loss (test_core.CausalAndLedgerTests.test_unresolved_is_not_zero_loss) ... ok
test_at_large_and_leading_zero_mapping (test_normalize.SourceMappingTests.test_at_large_and_leading_zero_mapping) ... ok
test_integrity_mismatch_refused (test_normalize.SourceMappingTests.test_integrity_mismatch_refused) ... ok
test_invalid_probability_sum_refused (test_normalize.SourceMappingTests.test_invalid_probability_sum_refused) ... ok
test_party_probability_sums_same_party_candidates (test_normalize.SourceMappingTests.test_party_probability_sums_same_party_candidates) ... ok
test_rule_alias_is_exact_and_ticker_scoped (test_normalize.SourceMappingTests.test_rule_alias_is_exact_and_ticker_scoped) ... ok
test_special_or_wrong_year_not_silently_joined (test_normalize.SourceMappingTests.test_special_or_wrong_year_not_silently_joined) ... ok
test_missing_crossed_negative_nan_and_duplicate_refused (test_books.DepthTests.test_missing_crossed_negative_nan_and_duplicate_refused) ... ok
test_old_cent_schema_not_misinterpreted (test_books.DepthTests.test_old_cent_schema_not_misinterpreted) ... ok
test_reciprocal_ask_keeps_opposite_quantity (test_books.DepthTests.test_reciprocal_ask_keeps_opposite_quantity) ... ok
test_unsorted_levels_zero_quantity_and_decimal_prices (test_books.DepthTests.test_unsorted_levels_zero_quantity_and_decimal_prices) ... ok

----------------------------------------------------------------------
Ran 27 tests in 0.004s

OK
```

Full score reproduction and independent decimal accounting: see verification.json.
These checks verify code and calculations, not live execution.
