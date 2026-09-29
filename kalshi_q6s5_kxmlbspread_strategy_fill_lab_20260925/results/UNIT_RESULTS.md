# Q6S5 KXMLBSPREAD strategy-fill path unit results

Code verification only. This run is not an Examiner score and not a tape walk.

Command: `python3 -m unittest -v tests.test_orchestrator`

Ran 11 tests in 0.007s at 2026-09-29T21:04:24Z. Result: OK. Failures: 0. Errors: 0.

`digest_all_match_claimed` is false. Conductor ACCEPT `c6f95b32a9224a6beede1a8c0e3d7f0a5a4530cc8b3d0b9d997995f65d64f8f3`, freeze markdown `9f50ba19694083c774bbe2a6cff491d1a2f81ed3a6f9cc21a3641a938c84955d`, kick prefix `dc19794b`, ADMIT-1 ruling prefix `ac7cfe63`, and `lab/governance/astra/packets/Q6S5_KXMLBSPREAD_STRATEGY_FILL/` were absent at `origin/main` `cb8957d` and were not recreated.

The checks that passed are the predeclared ones: ADMIT-1 window `[2026-09-27T00:00:00Z, 2026-09-30T04:00:00Z)` rejects interior timestamps and accepts `2026-09-30T04:00:00Z`; backfill is refused; `capture.sqlite` is refused without a read; lookahead is refused; Lee-Ready is refused; a strict public through observation leaves contracts, simulated fill, `results`, `pnl`, and ROI null; a touch is not a through; `mechanic_demo_observed` stays `UNAVAILABLE`; queue bytes prefixed `08aa54de` are not recreated; fee label is `CACHE_NOT_R1P1` with `formula_id` null; `counts_toward_keep` is false; arms stay Q6S5A0 `maker_vs_taker_native` and Q6S5A1 `content_fresh_vs_stale_bin`; Examiner status stays `HOLD_PRE_PR` with `stub_ready` false.

No live orders. `live_gets` stays 0. `admit.py` was not run.
