# C3 KXHIGHNY capture slot (stub only)

**panel_version:** `2026-09-22.c3-kxhighny-v0`
**packet_id:** `C3-KXHIGHNY-MEAS`
**freeze:** `packets/C3_KXHIGHNY_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md`
**freeze_sha256:** `0e79a0194e2371efae8d8cac0f4f2ec9ce4cf53f60dd870bae1a1ed7acff3604`
**panel_stub_sha256:** `2a5da7fe85ca1adc6b7c4dcf9e09ed5c6bb62be6b5c9b42731e36e31d1e8dfea`
**status:** Stub only. `admitted_at` is null. `panel_admitted.json` is not in this checkout. No recorder is running. `admit.py` is not run.
**isolation:** separate from ADMIT-1 (`nfl_prospective_recorder_20260922/`). Idle slot `lab/astra-capture/c3-kxhighny/`.

## Series

`KXHIGHNY` is primary. `KXHIGHCHI` is the multi-city presence proof. This slot is a bordering-strike measurement subject. It is not a GitHub weather-spread strategy. Volume, open interest, `results`, and `pnl` stay null in the stub.

## Artifacts in this checkout

- Stub: `lab/astra-capture/c3-kxhighny/panel_stub.json`
- Parent kernel: `packets/C3_KXHIGHNY_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md`
- Bordering-strike harness: `kalshi_c3_kxhighny_bordering_lab_20260923/`

Public capture, if a later collector runs, is GET-only on
`https://api.elections.kalshi.com/trade-api/v2`. `POST /portfolio/orders`
is out of scope. This directory does not start a recorder and does not
hold Logan keys.
