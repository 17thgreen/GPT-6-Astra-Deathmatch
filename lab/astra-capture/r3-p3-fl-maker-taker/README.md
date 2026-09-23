# R3-P3 FL maker/taker capture slot (stub only)

**panel_version:** `2026-09-22.r3-p3-fl-maker-taker-v0`
**packet_id:** `R3-P3-FL-MAKER-TAKER`
**freeze:** `packets/R3-P3_FL_MAKER_TAKER_BANDS_FREEZE_KERNEL_2026-09-22.md`
**freeze_sha256:** `0ed697149136acb3aa840aeeb79d11c8f6ef80f37ce4dd692a3cb690212206a7`
**panel_stub_sha256:** `6f640dd3a6091ba6b896ded38fdded4676583aa3c885223da21ddf03780250c0`
**bands_registry_sha256:** `0860cbe28d28ecc6142ddf6f1ebb67792084264ed82e0b4d868c3b3138ea5312`
**status:** Stub only. `admitted_at` is null. `panel_admitted.json` is not in this checkout. No recorder is running. `admit.py` is not run.
**isolation:** separate from ADMIT-1 (`nfl_prospective_recorder_20260922/`). Idle slot `lab/astra-capture/r3-p3-fl-maker-taker/`.

## Series

`KXHIGHNY` and `KXHIGHCHI` are the C3 weather-first seed. This slot is a
maker/taker and 10¢-band measurement subject. It is not a strategy merge
with the C3 bordering harness. Native taker fields are on the stub trades.
Lee-Ready is refused. Settled resolved markets on the stub: 0. Volume,
`results`, and `pnl` stay null.

## Artifacts in this checkout

- Stub: `lab/astra-capture/r3-p3-fl-maker-taker/panel_stub.json`
- Bands: `lab/astra-capture/r3-p3-fl-maker-taker/bands_registry_10c.json`
- Parent kernel: `packets/R3-P3_FL_MAKER_TAKER_BANDS_FREEZE_KERNEL_2026-09-22.md`
- Harness: `kalshi_r3p3_fl_maker_taker_lab_20260923/`

Public capture, if a later collector runs, is GET-only on
`https://api.elections.kalshi.com/trade-api/v2`. `POST /portfolio/orders`
is out of scope. This directory does not start a recorder and does not
hold Logan keys.
