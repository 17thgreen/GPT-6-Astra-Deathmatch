# Q6S5 KXMLBSPREAD strategy-fill path unit results

Code verification only. This run is not an Examiner score and not a tape walk.

Command: `python3 -m unittest discover -s tests -v`

Ran 14 tests in 0.023s at 2026-09-29T21:14:42Z. Result: OK. Failures: 0. Errors: 0.

The prior pre-pin run was `python3 -m unittest -v tests.test_orchestrator`: Ran 11 tests in 0.007s at 2026-09-29T21:04:24Z. Result: OK.

`digest_all_match_claimed` is true for the 14 vendored pins under `Q6S5_KXMLBSPREAD_STRATEGY_FILL/`. Implementation ACCEPT `c6f95b32a9224a6beede1a8c0e3d7f0a5a4530cc8b3d0b9d997995f65d64f8f3`. Companion rulings ACCEPT `a5398129aa45c5dee5fdd15656a252bb6c460d00e4f5b06360ce522de0f968b4`. Reconcile `0f33a94c970eec6a9863041396071c78ce64b58abc8a7ab91f48062fbfc052b0`. Primary authentic bundle v2 `739d81d6ab29d1b3964d3c4d1d72c02e0db202e8646777f8c484152d4816e02a`. v1 subset `6602e07ef9b444b8b242086d0cb338025507d117aa0874f24e99390cd9d01993`. Those governance paths were absent at `origin/main` `cb8957d` and were not recreated there. Queue bytes `08aa54de` were not recreated. `7472b8ac` supersedes them and is routing-only.

Measurement gaps stay absent and were not invented: Mechanic demo KXMLBSPREAD artifact, Examiner `formula_id`, Sep-25 settlements for 6/12 markets, an untouched evaluation period, and ADMIT-1 window data.

The checks that passed are the predeclared ones: ADMIT-1 window `[2026-09-27T00:00:00Z, 2026-09-30T04:00:00Z)` rejects interior timestamps and accepts `2026-09-30T04:00:00Z`; backfill is refused; `capture.sqlite` is refused without a read; lookahead is refused; Lee-Ready is refused; a strict public through observation leaves contracts, simulated fill, `results`, `pnl`, and ROI null; a touch is not a through; `mechanic_demo_observed` stays `UNAVAILABLE`; queue bytes prefixed `08aa54de` are not recreated; fee label is `CACHE_NOT_R1P1` with `formula_id` null; `counts_toward_keep` is false; arms stay Q6S5A0 `maker_vs_taker_native` and Q6S5A1 `content_fresh_vs_stale_bin`; Examiner status stays `HOLD_PRE_PR` with `stub_ready` false. Vendored pin sha256 values match the hard-coded table, `MANIFEST.sha256` checks clean, and a one-byte tamper is reported as a mismatch.

No live orders. `live_gets` stays 0. `orders` stays 0. `admit.py` was not run.
