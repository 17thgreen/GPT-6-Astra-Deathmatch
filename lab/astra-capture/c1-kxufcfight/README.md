# C1 KXUFCFIGHT capture slot (stub only)

**panel_version:** `2026-09-22.c1-kxufcfight-v0`
**packet_id:** `C1-KXUFCFIGHT-MEAS`
**freeze:** `packets/C1_KXUFCFIGHT_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md`
**freeze_sha256:** `a191c9b3f71030445d1d32684feb6dc1bf09abb7e09403d5dbdf1927eafc63c9`
**panel_stub_sha256:** `2cc661d86202d3daf9ffa45320e39d249852a97490f458f72ab7ea8ec5c81a00`
**status:** Clock admit consumed by the honesty harness. `panel_admitted.json` is the subject (`admitted_at` `2026-09-23T00:49:43Z`, sha256 prefix `24426d80`). The stub stays the pre-admit seed. No recorder is running.
**isolation:** separate from ADMIT-1 (`nfl_prospective_recorder_20260922/`), and from S1/S4/S5/R2-P3 poll budget

## Series

`KXUFCFIGHT` only. The shared 5000 USD figure is a measurement bakeoff label.

## Artifacts in this checkout

- Admitted panel: `lab/astra-capture/c1-kxufcfight/panel_admitted.json`
- Pre-admit stub: `lab/astra-capture/c1-kxufcfight/panel_stub.json`
- Kernel: `packets/C1_KXUFCFIGHT_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md`
- Scout packet: `packets/scout_c1_kxufcfight/FROZEN_EXPERIMENT.json`
- Harness: `kalshi_c1_kxufcfight_honesty_lab_20260922/`

## Production capture path

Public GET orderbooks belong at:

`lab/astra-capture/c1-kxufcfight/orderbooks/`

The collector is `kalshi_c1_kxufcfight_honesty_lab_20260922/collect_orderbooks.py`.
Its hypothesis is `ORDERBOOK_CAPTURE_SPEC.md`. One pass may GET only
`/markets/{ticker}/orderbook` for the four admitted tickers on
`https://api.elections.kalshi.com/trade-api/v2`. `POST /portfolio/orders` is
out of scope. This directory does not start a recorder and does not run
`admit.py`.

JSON in `orderbooks/` is refused unless `FROZEN_EXPERIMENT.json` pins each
file's sha256. No pinned file is `FIXTURE_GAP`. The 2026-09-23 public GET
wrote four files here. Each body is
`{"orderbook_fp":{"no_dollars":[],"yes_dollars":[]}}`, sha256
`e07d09f130e604a9e1acfc736fb57cbdfc33d8a5a253466a0cbd5c98cf6c9f74`. Empty bid
lists were not filled in. A pin does not fill the Examiner scorecard. C1
stays `NOT_SCORED` until pinned books and an Examiner-ready scorecard both
exist. These empty books are not that scorecard. The honesty harness uses
`kalshi_c1_kxufcfight_honesty_lab_20260922/fixtures/synthetic_orderbooks.json`
for in-memory label checks. Those fixtures are not live depth and are refused
for scorecard fill. `volume_fp` and `open_interest_fp` on the stub stay null.

## Pins

- R1-P1 `kalshi_feebook_lab_20260922` @ `22371178cb2663250b4762f328069571c48cb551`
- R1-P5 `kalshi_rails_lab_20260922` @ `6a28e0d6254327ea4e6451c781bec56215ac6cac`

## Seed

Markets N=4. Events N=2. ORTDAS dropped after HTTP 429. Volume, open interest,
results, and pnl are null.
