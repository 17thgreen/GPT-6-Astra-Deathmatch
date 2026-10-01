# Q6S5 KXMLBSPREAD FL-band settled-tape unit results

Code verification only. This run is not an Examiner score and not a settlement-joined band ROI.

Command: `python3 -m unittest discover -s tests -v`

Ran 13 tests in 0.041s at 2026-10-01T23:00:25Z. Result: OK. Failures: 0. Errors: 0.

`digest_all_match_claimed` is true. Conductor ACCEPT `8e4fbac7d0426bc67c1f53fb8057a382fe46da738bd701cb970a9812a6dc2a3b`. Freeze `fb6540f52ed5f819ccf6e80bf0cf7eb6d951e065416b9d550fead0c6d06043fa`. Authentic bundle `63b5d981bc06f684eebb69a8ac29394534f8ae52c101f3018557544f14e29857`. Band registry `0860cbe28d28ecc6142ddf6f1ebb67792084264ed82e0b4d868c3b3138ea5312`. `sha256sum -c MANIFEST.sha256` matched the vendored bundle.

The checks that passed are the predeclared ones: registry boundaries at 0.00, 0.20, 0.80, and 1.00; rebin refused; a market without `result` produces no row; ADMIT-1 window rejects an interior trade and an interior settlement; post-close, block, native-field conflict, and price-inconsistent rows are excluded; Lee-Ready, gap backfill, lookahead, and invented pnl are refused; `capture.sqlite` is refused without a read; Sep-25 markets stay out of scope; closed-manifest sha mismatch fails before parse; synthetic gross deltas, LOEO, LOMO, `one_tick_worse`, and `fees_2x` stay off the published card; fee label is `CACHE_NOT_R1P1` with `formula_id` null; pinned print count is 11,723; Examiner status stays `HOLD_PRE_PR` with `scored` false.

`results` and `pnl` stay null. No live orders. `live_gets` stays 0. `orders` stays 0. `admit.py` was not run.
