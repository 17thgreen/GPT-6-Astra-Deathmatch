# COLLECTOR STUB: CARD02 station weather (GET-only)

**Ask:** 60-day GET-only archive for KXHIGHLAX, KXHIGHMIA, KXHIGHNY and KXHIGHCHI, plus receipt-time METARs and first non-preliminary NWS CLIs. The full spec is in `COLLECTOR_HANDOFF_STATION_LIST_2026-09-24.md`.
**Pins:**
- R1-P1 feebook @ `22371178cb2663250b4762f328069571c48cb551`
- R1-P5 rails @ `6a28e0d6254327ea4e6451c781bec56215ac6cac`
**Rules:**
- No orders and no authenticated endpoints.
- Throttle 2–3 s. On a 429, back off 60–90 s and log it.
- Never backfill or impute.
- Reuse the C3 capture (`/workspace/lab/astra-capture/c3-kxhighny/`) for NY/CHI books.
- Coordinate with `/workspace/lab/astra-capture/weather-nowcast/` (same egress IP).
**Out of scope:** modeling, scoring, fees beyond pin citation, KXLOWT*, other cities, Q6-000, S2/R2-P4.
**Suggested landing:** `/workspace/lab/astra-capture/card02-station-weather/<YYYY-MM-DD>/{kalshi,metar,cli,forecast}/` with `received_at_utc` on every file and one `http_log.jsonl`.
