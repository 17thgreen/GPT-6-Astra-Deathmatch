# Unit results

Code verification from this directory:

`python3 -m unittest discover -s tests -v`

Ran 41 tests in 5.009s. Result: OK. Failures: 0. Errors: 0. This run is not an Examiner score and not a Simulator score.

## Structural counts

These counts are placement, print, and fill-set sizes. `results`, `pnl`, `roi`, `Q6S5A0`, and `Q6S5A1` stay null.

| Count | Value |
|---|---|
| n_books | 15 |
| eligible_placements | 15 |
| crossed_or_locked_n | 0 |
| empty_side_n | 0 |
| fresh_n | 15 |
| stale_n | 0 |
| requested_maker_contracts | 30 |
| requested_taker_contracts | 30 |
| prints_in | 21 |
| excluded_block_n | 0 |
| excluded_native_conflict_n | 0 |
| excluded_price_inconsistent_n | 0 |
| excluded_admit1_window_n | 0 |
| maker_filled_n | 0 |
| maker_unfilled_n | 30 |
| taker_filled_n | 30 |
| taker_unfilled_n | 0 |
| settled tickers joined | 6 |

Freshness reasons on the 15 placements: 6 `initial`, 9 `content_changed`. The stale bin is empty, so `A1_null_reason` is `STALE_BIN_EMPTY`.

## T1b

All 720 permutations of the 6-value settlement vector left the quote sha256 and the fill sha256 unchanged.

- quotes sha256 `3780742e41fa49d7d72ff11d4378eb0adeae9264d4a8913d9cc887c81b961946`
- fills sha256 `6fa0f543d8e8cc4c572f5385d83098639927d78e4f2be8364d833a92389d40f4`

The test prints no settlement label and no PnL. A T1b failure would void the run. This run did not fail.

## Labels

`evidence_class` `IN_SAMPLE_DEV / HISTORICAL_REPLAY`. `family_size` 1. `verdict_domain` `ITERATE|INCONCLUSIVE`. `counts_toward_keep` false. `promote` false. `fills_are_MODEL` true. Fee `CACHE_NOT_R1P1`. `accept_sha256` `9c6e19ca11a855015fb4e3e63cd65ae5e5c334875240e817e164e988426df9f5`. `freeze_sha256` `213ee6dd33f292c8041977b0b8d7566da9412fd3debe0597643c500dc1e42db4`. `A1_null_reason` `STALE_BIN_EMPTY`.

## Limitations

No quote file, fill file, or PnL figure is committed. `results/EMPTY_RESULTS.json` keeps every metric null. The Examiner file stays `HOLD_PRE_PR`. Zero maker fills is the fill-set size under the frozen queue rule on this tape; it is not a profit figure and it is not an Examiner verdict.
