# Q6S5 KXMLBSPREAD game-phase settled-tape unit results

Code verification only. This run is not an Examiner score and not a settlement-joined phase ROI.

Command: `python3 -m unittest discover -s tests -v`

Ran 20 tests in 0.505s at 2026-10-01T23:36:30Z. Result: OK. Failures: 0. Errors: 0.

`digest_all_match_claimed` is true. Conductor ACCEPT `08d23b363d72b8c8599772ee6fc6736cb90f13e8ed814b12c59b58fd5c7dc91e`. Freeze `5beba803f3f6d33410409acc23ad3b782be62dc8829a0f54584e1da8ac18575a`. Authentic bundle `6576ee6cf9f023137e4357270f228dd9a5d29e3dc1d5e7ced85384681f2a7ecc`. Packet-dir MANIFEST `88af3bd79ad37c6fa09cfbe1bcd516c72b8a35d2928ce04eeaec994b5c1233a1`. Band registry `0860cbe28d28ecc6142ddf6f1ebb67792084264ed82e0b4d868c3b3138ea5312`. IN_SAMPLE_DEV ruling `09763030c67df066f2b59346200813e181777670cd46fcee6b8877a6dd74d754`. `sha256sum -c MANIFEST.sha256` matched the vendored bundle (119 payload files) and `pins/MANIFEST.sha256` matched the tarball, the ACCEPT, and the ruling.

The checks that passed are the predeclared ones: rules_primary parse and event-ticker cross-check, including a mismatch and a missing pattern hard-fail; a print at exactly scheduled first pitch is Q6S5GP1 and a print one microsecond earlier is Q6S5GP0; a print at close is excluded; `pre_admitted_at` is strict `<`; `evidence_class` is `IN_SAMPLE_DEV`; `family_size` is 4; `hypothesis_generating_only` is true; `universe_cap_last_knob` is true; `first_pitch_source` is `SCHEDULED_START_PROXY`; FL1 uses registry inclusivity with no rebin; a market without `result` produces no row; ADMIT-1 window rejects an interior trade and an interior settlement; post-close, block, native-field conflict, and price-inconsistent rows are excluded; Lee-Ready, gap backfill, lookahead, invented pnl, depth, settlement, and markets are refused; `capture.sqlite` is refused without a read; live HTTP and live orders are refused; non-test code has no network import; Sep-25 markets stay out of scope; closed-manifest and pins-manifest sha mismatches fail before parse; synthetic gross deltas, leave-one-game-out, leave-one-market-out, `one_tick_worse`, `start_shift_plus_30m`, and `fees_2x` stay off the published card; fee label is `CACHE_NOT_R1P1` with `formula_id` null; pinned print count is 11,723; Examiner status stays `HOLD_PRE_PR` with `scored` false.

Timestamp-only arm counts. These use `created_time`, the pinned schedule, and `close_time`. No price, side, or result.

| arm | rows |
| --- | ---: |
| Q6S5GP0 pregame | 1865 |
| Q6S5GP1 in-play | 9852 |
| post-close | 6 |

`pre_admitted_at` is strict `< 2026-09-25T04:37:47Z`. `post_admitted_at` is the complement. Counts only. No outcome, return, PnL, or win rate. Included output rows match the timestamp-only arm totals: block, taker-conflict, and price-inconsistent exclusions are 0. The 6 post-close prints are not output rows.

| arm | pre_admitted_at | post_admitted_at |
| --- | ---: | ---: |
| Q6S5GP0 | 1865 | 0 |
| Q6S5GP1 | 8815 | 1037 |

The same counts are in `results/PHASE_ARM_COUNTS.json` and `results/ADMITTED_AT_ARM_COUNTS.json`.

`results` and `pnl` stay null. No live orders. `live_gets` stays 0. `orders` stays 0. `admit.py` was not run.
