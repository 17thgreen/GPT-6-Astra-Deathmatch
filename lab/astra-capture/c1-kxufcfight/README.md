# C1 KXUFCFIGHT capture slot (stub only)

**panel_version:** `2026-09-22.c1-kxufcfight-v0`
**packet_id:** `C1-KXUFCFIGHT-MEAS`
**freeze:** `packets/C1_KXUFCFIGHT_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md`
**freeze_sha256:** `a191c9b3f71030445d1d32684feb6dc1bf09abb7e09403d5dbdf1927eafc63c9`
**panel_stub_sha256:** `2cc661d86202d3daf9ffa45320e39d249852a97490f458f72ab7ea8ec5c81a00`
**status:** no recorder running — `PANEL_SCHEMA_STUB_SEED` (`admitted_at` null)
**isolation:** separate from ADMIT-1 (`nfl_prospective_recorder_20260922/`), and from S1/S4/S5/R2-P3 poll budget

## Series

`KXUFCFIGHT` only. The shared 5000 USD figure is a measurement bakeoff label.

## Artifacts in this checkout

- Panel stub: `lab/astra-capture/c1-kxufcfight/panel_stub.json`
- Kernel: `packets/C1_KXUFCFIGHT_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md`
- Scout packet: `packets/scout_c1_kxufcfight/FROZEN_EXPERIMENT.json`
- Harness: `kalshi_c1_kxufcfight_honesty_lab_20260922/`

## Production capture path

Public GET orderbooks, when a later collector writes them, belong at:

`lab/astra-capture/c1-kxufcfight/orderbooks/`

Routes stay inside the stub allowlist: series, market, small open list,
orderbook, and small trades, on `https://api.elections.kalshi.com/trade-api/v2`.
`POST /portfolio/orders` is out of scope. This directory does not start a
recorder and does not run `admit.py`.

This freeze has no production orderbook manifest. The honesty harness refuses
an unpinned file in `orderbooks/` and uses
`kalshi_c1_kxufcfight_honesty_lab_20260922/fixtures/synthetic_orderbooks.json`
for unit checks. Those fixtures are not live depth. `volume_fp` and
`open_interest_fp` on the stub stay null.

## Pins

- R1-P1 `kalshi_feebook_lab_20260922` @ `22371178cb2663250b4762f328069571c48cb551`
- R1-P5 `kalshi_rails_lab_20260922` @ `6a28e0d6254327ea4e6451c781bec56215ac6cac`

## Seed

Markets N=4. Events N=2. ORTDAS dropped after HTTP 429. Volume, open interest,
results, and pnl are null.
