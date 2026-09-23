# S4 KXNCAAFGAME capture slot (schema seed)

**panel_version:** `2026-09-22.s4-kxncaafgame-v0`
**packet_id:** `S4-KXNCAAFGAME-MEAS`
**status:** Schema seed. `admitted_at` is null. `panel_admitted.json` is not in this checkout. No recorder is running. `admit.py` is not run.

The conductor panel stub sha256 claim is
`38167d11da5842bc4d39e6e7dcaab20a67294c735ba14d8bbeafde3154c6342a`
(~113 events). Those bytes were not in this checkout. `panel_stub.json`
here is an empty schema seed. It does not invent that cohort. The harness
prefers `panel_admitted.json` when that file appears later.

**isolation:** separate from ADMIT-1 (`nfl_prospective_recorder_20260922/`),
and from S1/S5/R2-P3/C1/C3/C5 poll budget.

Public capture, if a later collector runs, is GET-only on
`https://api.elections.kalshi.com/trade-api/v2`. This directory does not
start a recorder and does not hold Logan keys.

Harness: `kalshi_s4_ncaaf_feequue_lab_20260923/`.
