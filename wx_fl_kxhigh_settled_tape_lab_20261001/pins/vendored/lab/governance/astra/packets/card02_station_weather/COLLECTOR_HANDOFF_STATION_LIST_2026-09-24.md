# COLLECTOR HANDOFF: Card 02 station list + 60-day GET-only archive spec (2026-09-24 ET)

**From:** Deep Research. **To:** Collector. **Governs:** `packets/CARD02_STATION_WEATHER_NOWCAST_FREEZE_KERNEL_2026-09-24.md`.
**Rules:**
- GET-only and public. No orders, no auth.
- Kalshi throttle 2–3 s. On a 429, back off 60–90 s, log it, and never fill the gap.
- Stamp `received_at_utc` locally on every file. Save raw bytes.
- The box egress IP is shared with other agents. Today's discovery run logged 429s on Climate series listing, HIGHAUS ×2, HIGHNY ×2, KXDENHIGH, KXHIGHTSEA and KXLOWTAUS. Budget for this.
**Pins:**
- R1-P1 feebook @ `22371178cb2663250b4762f328069571c48cb551`
- R1-P5 rails @ `6a28e0d6254327ea4e6451c781bec56215ac6cac`

## 1. Stations

| Series | Station (Kalshi rules) | ICAO | WFO | CLI `issuedby` | tz | LST climate day (DST) | CLI HTML | CLI API list |
|---|---|---|---|---|---|---|---|---|
| KXHIGHLAX | Los Angeles Intl | KLAX | LOX | LAX | America/Los_Angeles | 01:00–00:59 PDT | https://forecast.weather.gov/product.php?site=LOX&product=CLI&issuedby=LAX | https://api.weather.gov/products/types/CLI/locations/LAX |
| KXHIGHMIA | Miami Intl | KMIA | MFL | MIA | America/New_York | 01:00–00:59 EDT | https://forecast.weather.gov/product.php?site=MFL&product=CLI&issuedby=MIA | https://api.weather.gov/products/types/CLI/locations/MIA |
| KXHIGHNY | Central Park | KNYC | OKX | NYC | America/New_York | 01:00–00:59 EDT | https://forecast.weather.gov/product.php?site=OKX&product=CLI&issuedby=NYC | https://api.weather.gov/products/types/CLI/locations/NYC |
| KXHIGHCHI | Chicago Midway | KMDW | LOT | MDW | America/Chicago | 01:00–00:59 CDT | https://forecast.weather.gov/product.php?site=LOT&product=CLI&issuedby=MDW | https://api.weather.gov/products/types/CLI/locations/MDW |

The four `api.weather.gov` CLI list endpoints returned HTTP 200 on 2026-09-24. Raw files: `live_get_2026-09-24/nws/`.

Outside DST, the LST day is 00:00–23:59 local.

## 2. Streams, cadence and landing

Suggested landing: `/workspace/lab/astra-capture/card02-station-weather/<YYYY-MM-DD>/`

| Stream | Endpoint | Cadence | Notes |
|---|---|---|---|
| Kalshi open markets | `GET /trade-api/v2/markets?series_ticker=<S>&status=open&limit=200` | every 60 min | Record `rules_primary`, `early_close_condition`, `close_time`, strikes, `volume_24h_fp`, `open_interest_fp` |
| Kalshi orderbook | `GET /trade-api/v2/markets/<ticker>/orderbook` | every 15 min for all open buckets of the current climate day, **plus** one snapshot within ±2 min of 10:00, 14:00 and 18:00 LST (the knob levels) | 4 series × 6 buckets for the current day is about 24 books per 15 min, or about 1 request every 37 s. For NY/CHI, reuse the C3 capture where cadence matches. |
| Kalshi trades | `GET /trade-api/v2/markets/trades?ticker=<ticker>&limit=1000` (cursor) | hourly, and at close | Needed for adverse selection after fills |
| Kalshi settlement | `GET /trade-api/v2/markets/<ticker>` after settlement | once per market, after the result posts | `result` plus settlement timestamps. This is the settled join (C3-RJ compatible). |
| METAR/ASOS obs | `GET https://api.weather.gov/stations/<ICAO>/observations` (User-Agent header with contact per NWS API policy) | every 10 min | Keep the raw JSON. Keep the hourly T-group (tenths °C) separate from 5-min whole-°C obs. **Never convert a 5-min °C value into a °F running max.** |
| NWS CLI | the CLI API list above, then each `products/<id>` | every 30 min between 00:30 and 09:00 local, and 15:00–18:00 local | Save **every** issuance (the LAX Sep 23 CLI was issued twice, at 08:26Z and 08:40Z). Mark which one Kalshi treats as "first non-preliminary." Keep corrections (CCA) separate. |
| NWS point forecast (simple baseline input) | `GET https://api.weather.gov/points/<lat>,<lon>`, then the `forecast` URL | hourly | Archive with receipt time. It is the input to the simple forecast-error baseline. |

## 3. 60-day spec

- **Pilot:** 60 consecutive climate days starting from the Collector's first full day. This is a collection target, not proof of power.
- **Evaluation:** the next 60 climate days, held untouched for the Examiner. Do not analyze them during the pilot.
- **Data-failure flag:** more than 30% of station-days excluded (missing book at a knob time, no METAR in the prior 90 min, CLI MM/missing, Kalshi result unavailable) over any 14 consecutive days. Report it to the Conductor. Do not patch.
- **Log both:** `early_close_condition` text ("11:59 PM local") and raw `close_time` (00:00 LST). The interpretation is UNVERIFIED.

## 4. Coordination

- `/workspace/lab/astra-capture/weather-nowcast/` (another box agent's collector) has `stations.json` = `{"placeholder": true}`. Adopt the 4 stations above rather than running a second stream.
- `/workspace/lab/astra-capture/c3-kxhighny/` (C3): reuse its NY/CHI books and its settled join.
