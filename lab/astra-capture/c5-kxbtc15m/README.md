# C5 KXBTC15M capture slot (stub only)

**panel_version:** `2026-09-22.c5-kxbtc15m-v0`
**packet_id:** `C5-KXBTC15M-MEAS`
**freeze:** `packets/C5_KXBTC15M_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md`
**freeze_sha256:** `4d1b72a38603de181e71f80b3cc6515b170a2bffe11f8770dac1296373e50263`
**panel_stub_sha256:** `60f613e8d775b66b9044ad31d2faf77bba84176f214a7bce599aa7a65b6905f8`
**status:** Stub only. `admitted_at` is null. `panel_admitted.json` is not in this checkout. No recorder is running. `admit.py` is not run.
**isolation:** separate from ADMIT-1 (`nfl_prospective_recorder_20260922/`), and from S1/S4/S5/R2-P3/C1/C3 poll budget

## Series

`KXBTC15M` only. This slot is a fee and queue honesty stress subject. It is not live crypto trading. No bacchus or kxeth15m strategy is imported. Volume, open interest, `results`, and `pnl` stay null in the stub.

## Artifacts in this checkout

- Stub: `lab/astra-capture/c5-kxbtc15m/panel_stub.json`
- Parent kernel: `packets/C5_KXBTC15M_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md`
- Honesty harness: `kalshi_c5_kxbtc15m_honesty_lab_20260923/`

Public capture, if a later collector runs, is GET-only on
`https://api.elections.kalshi.com/trade-api/v2`. `POST /portfolio/orders`
is out of scope. This directory does not start a recorder and does not
hold Logan keys.
