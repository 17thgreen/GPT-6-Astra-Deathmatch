# WX-FL-KXHIGH-SETTLED-TAPE

Out-of-domain replication of FL-band freeze `fb6540f52ed5f819ccf6e80bf0cf7eb6d951e065416b9d550fead0c6d06043fa` on 48 finalized KXHIGH markets (CHI, LAX, MIA, NY on 26SEP24 and 26SEP25). The 18 26SEP26 markets are out. Trades and settlements at or after `2026-09-27T00:00:00Z` are the ADMIT-1 exclusion.

## Knob

`price_band` of the native taker-purchased side, registry `0860cbe28d28ecc6142ddf6f1ebb67792084264ed82e0b4d868c3b3138ea5312` unchanged.

| Arm | p_taker | Bands |
|---|---|---|
| WXFL0 longshot_taker | [0.00, 0.20) | b00, b01 |
| WXFL1 mid | [0.20, 0.80) | b02–b07 |
| WXFL2 favorite_taker | [0.80, 1.00] | b08, b09 |

Row rules match fb6540f5: native `taker_outcome_side` only, Lee-Ready refused, block and post-close and price-inconsistent prints excluded and counted, weight `count_fp`.

## Hypotheses

- H1: `maker_gross_roi_delta_FL0_minus_FL1 > 0`
- H2: `maker_gross_roi_delta_FL2_minus_FL1 <= 0`

The contradicts / supports rule is the fb6540f5 text with city-day substituted for event. The verdict vote is the freeze formula: `n = n_eff = |D|`, `need = ceil(2n/3)`, and the reading is inconclusive if `n_eff < 3`. H1 votes only over D01 (city-days where both WXFL0 and WXFL1 have capital > 0). H2 votes only over D21. Empty-arm city-days are not votes. Conductor addendum `68e1ff7a3f170a90b74a72448809558c3ce7364e32a8b5296a1d10c3b2590153` supersedes the ACCEPT's ">= 6 of 8", which assumed all 8 city-days were in D. Leave-one-date-out and leave-one-city-out are robustness reports and are not verdict inputs. Under the primary, the three non-empty D units are CHI, MIA, and NY on 2026-09-25, so `n_eff = 3` and the threshold is at least 2 of 3, but those units share one date (`date_level_n = 1`). The verdict is capped at ITERATE for any reading, and `contradicts_H1` does not map to KILL in this run. The without-Sep-25 subset has `n_eff = 0` and is inconclusive. KILL scope is the four KXHIGH series only.

Primary aggregation is the city-day-equal-weighted mean of Examiner `maker_gross_roi` (`2e74f17b`: return `Σ q·(p_taker − Y_s)` over capital `Σ q·(1 − p_taker)`). Trade-weighted pooled ROI is secondary. Both are reported with and without Sep-25. Those functions run on synthetic rows only.

## Gap mappings

Primary GM-COV is union coverage (addendum ruling 3, option b). A window `[start, end)` is proven when the union of later complete polls' closed cursor intervals `[min_ts, requested_at]` covers it with no hole. Later means the poll's first-page `requested_at` is strictly after the window start. A contributing poll is complete only when every page is ok and HTTP 200, with no 429, last-page `n_items < 1000`, at most 10 pages, and an intact cursor chain. Incomplete polls are excluded. Open windows are never proven. An all-ticker storm is proven for a ticker only when that ticker's union covers it; the window headline is proven only when all 48 in-scope tickers are. Trades in an unproven window for their ticker are dropped from all arms. Cursor-minus-1s is not assumed.

GM-COV-SINGLE keeps the previous literal rule as a full sensitivity: one later complete poll's half-open range `[min_ts, requested_at)` spans the whole window.

GM-LIT drops any trade whose `created_time` is in a ticker gap or a storm window `[start, end)`, with open windows running forever. It is a full sensitivity. Expected timestamp-only counts: 27,199 dropped, 6,558 kept.

GM-LIT-PAD widens budget windows by 1,920 seconds and is counts only (expected 33,622 dropped, 135 kept; CHI24 and NY24 empty).

## Labels

Every measurement output carries `evidence_class=IN_SAMPLE_DEV / HISTORICAL_REPLAY`, `pre_admitted_at_flag_possible=false`, `family_size=1`, `verdict_ceiling=ITERATE`, `counts_toward_keep=false`, `promote=false`, fee label `CACHE_NOT_R1P1` with net null, `out_of_domain_replication_of` the fb6540f5 sha256, `accept_sha256` above, and `addendum_sha256` `68e1ff7a3f170a90b74a72448809558c3ce7364e32a8b5296a1d10c3b2590153`. Count outputs and the scorecard shell also carry `reading_scope`, `date_level_n`, `verdict_cap=ITERATE`, and `kill_mapping_disabled=true`. Caveats: Sep-24 covers only its last ~5-8 h, Sep-25 lacks its first ~10 h, and Sep-25 carries 33,119 of 33,757 trades. `results/EMPTY_RESULTS.json` stays the sha-pinned freeze-time copy.

## Pins

`pins/MANIFEST.sha256` covers the authentic tarball, the ACCEPT, the ruling, and the pre-ROI addendum. Runtime checks the addendum sha256 alongside the ACCEPT. Extraction checks the tarball sha256 `febc74af09b06db83fb686e904d6f3e305fe30414e4c4f67c05705f0de597807`, `MANIFEST.sha256` inside the tarball, and snapshot `d20d5e7d0cedc79ed77c92e905b2824f0ca1d79f8e524635bfd3a8f0e3c6eae2` before `sqlite3` opens it. The extract directory is removed when the loader created it. The gap export is regenerated from the snapshot and must match `0211f5ca…`. The trades-poll export must match `a287572c…`.
