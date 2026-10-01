# Q6S5 KXMLBSPREAD game-phase settled-tape

Hypothesis and row rules are the frozen packet
`Q6S5-KXMLBSPREAD-GAME-PHASE-SETTLED-TAPE`, vendored verbatim.
This specification is the implementation record of that freeze.
No phase ROI is filled here.

- Feature family: `settled_tape_game_phase`
- Parent packet: `Q6S5-KXMLBSPREAD-FEEQUEUE-HARNESS`
- One knob: `game_phase` on the print's own `created_time`
- Arms: `Q6S5GP0` pregame (`created_time < scheduled first pitch`), `Q6S5GP1` in-play (`scheduled first pitch <= created_time < close_time`)
- Prints at or after `close_time` are excluded. The freeze feasibility pin is 6 such prints.
- Scheduled first pitch is parsed from pinned `rules_primary` with `originally scheduled for (Mon) (D), (YYYY) at (H):(MM) (AM|PM) EDT`, converted from EDT (UTC−4), and required to equal the event-ticker code `YYMONDDHHMM` read as ET. A mismatch or a missing pattern is a hard fail.
- `first_pitch_source` is `SCHEDULED_START_PROXY` on every output. This is a proxy for actual first pitch. `occurrence_datetime` and `expected_expiration_time` are not used.
- Declared UTC starts: HOUATH `2026-09-25T01:40:00Z`, LAASEA `2026-09-25T01:40:00Z`, SDLAD `2026-09-25T02:10:00Z`.
- A print at exactly the scheduled start is `Q6S5GP1`. A print one microsecond earlier is `Q6S5GP0`. A print at exactly `close_time` is excluded.
- `start_shift_plus_30m` recomputes the primary at `scheduled_start + 30 min`. It is a stress, not an arm.
- Registry: R3-P3 10¢ bands, sha256 `0860cbe28d28ecc6142ddf6f1ebb67792084264ed82e0b4d868c3b3138ea5312`. The secondary uses FL1 only, bands b02–b07, `[0.20, 0.80)`. No rebin. No FL0/FL1/FL2 delta is computed.
- Universe: 6 finalized panel_admitted markets, 3 events (HOUATH, LAASEA, SDLAD), 11,723 pinned prints. Six Sep-25 markets stay out of scope.
- Timestamp-only arm counts from the freeze, before native-side, block, and price exclusions: pregame 1,865, in-play 9,852, post-close 6.
- Primary metric: `maker_gross_roi_delta_GP1_minus_GP0` (gross, fee-free). Hypothesis H1: the delta is negative.
- Secondary: the same delta inside the FL1 stratum. Robustness: leave-one-game-out (`logo`, the freeze name `loeo`), leave-one-market-out (`lomo`), `one_tick_worse`, `start_shift_plus_30m`, and `fees_2x` on the `CACHE_NOT_R1P1` secondary.
- Fee label: `CACHE_NOT_R1P1`. Not R1-P1. The maker role is resolved through `feebook.resolve_terms` and the resolved value is not asserted.
- Orthogonal to `analysis_slice` (PR58), `fill_model` (PR60), and `price_band` (PR61).
- `family_size` is 4 on this universe. `hypothesis_generating_only` is true. `universe_cap_last_knob` is true. This is the last knob on these 3 games.
- Evidence class: `IN_SAMPLE_DEV`. `pre_admitted_at` is true iff `created_time` is strictly before `2026-09-25T04:37:47Z`.
- Verdict ceiling: ITERATE. `promote` false. `counts_toward_keep` false.
- `results` and `pnl` stay null until Examiner scores. This lab does not score.

Conductor ACCEPT sha256 `08d23b363d72b8c8599772ee6fc6736cb90f13e8ed814b12c59b58fd5c7dc91e`.
Freeze sha256 `5beba803f3f6d33410409acc23ad3b782be62dc8829a0f54584e1da8ac18575a`.
Authentic bundle sha256 `6576ee6cf9f023137e4357270f228dd9a5d29e3dc1d5e7ced85384681f2a7ecc`.
Packet-dir MANIFEST sha256 `88af3bd79ad37c6fa09cfbe1bcd516c72b8a35d2928ce04eeaec994b5c1233a1`.
Inherited ruling sha256 `09763030c67df066f2b59346200813e181777670cd46fcee6b8877a6dd74d754`.

Examiner status at implement: `HOLD_PRE_PR`. The post-PR examiner path is `READY_NOT_SCORED`. This lab does not mark SCORED.

ADMIT-1 window `[2026-09-27T00:00:00Z, 2026-09-30T04:00:00Z)` is refused for trade time and settlement time. `capture.sqlite` is not opened. No gap backfill. No live Kalshi HTTP. `live_gets` stays 0. No live orders. `admit.py` is not run. Lee-Ready is refused. No invented fills, PnL, depth, markets, or settlement times. The arm does not use a later print or the settlement outcome.
