# S5 KXMVECROSSCATEGORY capture slot (stub only)

**panel_version:** `2026-09-22.s5-kxmvecrosscategory-v0`
**packet_id:** `S5-KXMVECROSSCATEGORY-MEAS`
**freeze:** `packets/S5_KXMVECROSSCATEGORY_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md`
**freeze_sha256:** `a28932ba13b4913b69c48b73dde8ba066cebd212670d0b1cbb5ea8e93734b8ba`
**panel_stub_sha256:** `4918b820d454c5f997ea100917859f7e9467d92933bed1bc8a55c81ab8ce5b8e`
**status:** Stub only. `admitted_at` is null. `panel_admitted.json` is not in this checkout. No recorder is running. `admit.py` is not run.
**isolation:** separate from ADMIT-1 (`nfl_prospective_recorder_20260922/`), and from S1/S4/R2-P3/C1/C3/C5 poll budget

## Series

`KXMVECROSSCATEGORY*` with the combo fee pin on `KXMVECROSSCATEGORY`,
`KXMVECROSSCATEGORY-SHARD1`, and `KXMVESPORTSMULTIGAMEEXTENDED`. The seed
holds 5 markets and 21 events. Every seed market has `mve_selected_legs`.
The trade probe on the stub is empty. Volume, open interest, `results`,
and `pnl` stay null in the stub.

## Artifacts in this checkout

- Stub: `lab/astra-capture/s5-kxmvecrosscategory/panel_stub.json`
- Parent kernel: `packets/S5_KXMVECROSSCATEGORY_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md`
- Fill-vs-legs harness: `kalshi_s5_mve_filllegs_lab_20260923/`

Public capture, if a later collector runs, is GET-only on
`https://api.elections.kalshi.com/trade-api/v2`. RFQ `/communications`
is out of scope. This directory does not start a recorder and does not
hold Logan keys.
