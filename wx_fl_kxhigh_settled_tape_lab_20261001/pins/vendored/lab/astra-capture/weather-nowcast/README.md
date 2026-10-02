# weather-nowcast: prospective GET-only archive (Kalshi daily HIGH temp + NWS)

panel_version `2026-09-24.cw-weather-nowcast-v0`. `admitted_at` is null. Start and stop times are in `MANIFEST.json`: archive_started_at 2026-09-25T00:07:29Z, stop_at +60 days. After the pilot comes a 60-day untouched evaluation holdout. This collector does NOT capture the holdout.
Series and stations are FINAL per Deep Research: KXHIGHLAX/KLAX/CLI LAX, KXHIGHMIA/KMIA/CLI MIA, KXHIGHNY/KNYC/CLI NYC, KXHIGHCHI/KMDW/CLI MDW.
This archive is fully separate from ADMIT-1 (`../prospective/`). It uses its own DB and its own processes, and it never touches record.py or admit1_supervisor.sh.

## Files
- `archive.sqlite`: the SQLite archive (WAL mode). Raw bodies are stored zlib-compressed and byte-verbatim (`raw` columns). Every row has `received_at` (UTC box clock at receipt). Source timestamp fields are kept untouched.
- `collector.py`: a single process. `supervisor.sh` is a bash loop that relaunches the collector if it dies, logs each relaunch and writes a gap row. It exits at stop_at.
- `collector.pid`, `supervisor.pid`, `status.json` (heartbeat, rewritten every 60 s), `logs/` (`collector_*.log`, `supervisor.log`, `kalshi_429.jsonl`, `kalshi_hourly.jsonl`).
- `stations.json`: the editable station config. `station_pick_provisional.json` holds the ranking evidence, with raw data in `evidence/`.

## Tables
`kalshi_orderbook` (a snapshot every 60 s from the public batch orderbook endpoint; `same_as_prev=1` rows record the poll without repeating the blob), `kalshi_trades` (PK trade_id), `kalshi_markets` / `kalshi_events` (a row is stored only when content changes; result is captured after close), `kalshi_series_meta`, `nws_obs` (unique on station+obs_timestamp+properties hash; `pre_archive_start` flag), `nws_product_index` + `nws_products` (every CLI/CF6 issuance, including corrections, with full text), `nws_listing_snapshots`, `nws_forecast` (points + forecast + forecastHourly), `polls` (one row per request), `gaps`, `runs`, `config_versions`.

## Rules
The collector is GET-only and unauthenticated, and it never places orders. URLs are enforced by a regex allowlist. It never fills, interpolates or backfills. Every failed, 429'd, skipped (cooldown or pause), stale or late poll becomes a `gaps` row. Gap streams include `*_fresh`/stale, `kalshi_orderbook_late` and `kalshi_trades_budget` (budget_shortfall_sweep_late). Collector downtime is recorded as a `collector_not_running` gap.

## Kalshi budget (governing: /workspace/lab/governance/astra/COLLECTOR_KALSHI_GET_BUDGET_2026-09-24.md)
- Phase A: at least 6 s between Kalshi GETs (10 rpm or less). List endpoints (events list, trades, series) are spaced at least 15 s apart (4 rpm or less).
- Phase B: from 2026-09-27T16:30Z to 2026-10-02T06:15Z the collector switches automatically to 12 s spacing and list calls at least 30 s apart.
- Tonight, until 2026-09-25T03:10Z: 9 s spacing and list calls at least 60 s apart, to make room for the Conductor audit.
- Emergency drop to Phase B: `touch FORCE_PHASE_B` (takes effect on the next request). Delete the file to revert.
- On a 429, the collector honors Retry-After. Otherwise it applies a per-class cooldown of 30/60/120/240 s, capped at 600. Each 429 in the last 30 min adds 2 s of spacing (capped at +10). Three or more 429s in 10 min pause all Kalshi GETs for 10 min (`PAUSE_429_STORM`). Failed polls are not retried immediately.

## Swap stations
1. Edit `stations.json`. It must stay valid JSON, and each entry needs `series_ticker`, `nws_station` and `cli_location`. Optional keys: `cf6_location`, `timezone`, `lat`, `lon`, `wfo` and `climate_day`.
2. Either wait up to 60 s (the collector reloads when the file's mtime changes) or run `kill -HUP $(cat collector.pid)`.
3. Check with `grep CONFIG logs/collector_*.log | tail` and `sqlite3 archive.sqlite 'select id,loaded_at,sha256 from config_versions'`. If the JSON is invalid, the collector keeps the previous config and logs `CONFIG load failed`.
Nothing is deleted when you swap. Removed series simply stop being polled.

## Health
- `/workspace/lab/.venv/bin/python tools/health.py [since_iso]` gives a read-only summary: per-stream and per-station counts, poll ok/fail counts, and gaps.
- `cat status.json` shows the heartbeat, phase, spacing, cooldowns, open gaps and hourly Kalshi counts.
- `tail logs/supervisor.log` shows relaunches, and `tail -f logs/collector_*.log` follows the collector log.
- To stop everything cleanly: `kill -TERM $(cat supervisor.pid)`. The supervisor forwards TERM to the collector.

## Known limitations
- Kalshi's settlement source is The Weather Company (weather.com/kalshi). That page is NOT captured here. The NWS CLI/CF6 products are the Source Agency record.
- The IEM ASOS 1-min/5-min feed is not used, because this box IP is blocked by mesonet.agron.iastate.edu (302 to the "sorry/blocked" page).
- The shared IP is heavily 429'd. Expect gaps in Kalshi streams, which are recorded as gaps and never filled.
