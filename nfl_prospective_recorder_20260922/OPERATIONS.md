# Durable recorder operations

This directory is the reviewed admission path. The frozen Q4 collector
(`nfl_timing_lab_20260921/collector/`) still rejects any panel whose purpose
is not `development`, and its Docker file remains a historical note that no
host was started. Do not edit that snapshot to point it at a holdout cohort.

Nothing in this checkout is a running collector. The commands below are for a
durable host an operator controls. They issue public GETs only. Do not add
credentials, account routes, or order routes.

## What gets recorded

`record.py` polls a panel from each kickoff's T−7d through T−3h plus five
minutes. It stores raw responses, deduplicated trades, and watermarks in
SQLite. A restart records a book gap; missed book snapshots are not
reconstructed. A changed panel hash cannot resume an old database.

Two databases, on purpose:

| Role | Panel | Database |
|---|---|---|
| Smoke | `development_panel.json` | `capture-data/development/capture.sqlite` |
| Prospective | stamped copy of `prospective_panel.json` | `capture-data/prospective/capture.sqlite` |

The development panel is the already-observed NYG–LAR and ATL–GB events. It is
not the reserved cohort. Smoke it first. Then switch processes. Do not point
the prospective panel at the development database.

## Host

Use a machine whose disk survives reboot. Bind `./capture-data` only when that
directory is on persistent disk; otherwise change the compose volume source to
an absolute path on that disk. Do not use a container-local filesystem or a
tmpfs. Leave disk headroom and watch file growth. Back up with SQLite's backup
API, or copy the database only while the recorder is stopped. Copying a live
WAL file drops pages.

No secret, API key, or account id belongs in the image, the compose file, or
the panel.

## 1. Smoke the development panel

From this directory, on the durable host:

```bash
docker compose up -d --build
docker compose logs --tail=30
docker compose stop
```

The default command is the development panel and
`/data/development/capture.sqlite`. `stop_grace_period` is 120 seconds so
SIGTERM can finish the open session. A finite local session without Docker is:

```bash
python3 record.py --panel development_panel.json \
  --database capture-data/development/capture.sqlite --seconds 3600
```

Repeat the same command to resume that database. Confirm the process starts
and writes the development database before any prospective admission. Stop it
before the next step so the host is not polling two panels at once.

## 2. Resolve venue tickers (public listing GET only)

`prospective_panel.json` already matches a listing retrieved
`2026-09-22T20:57:58Z`. PIT@CLE is `KXNFLGAME-26OCT01PITCLE`. Fifteen week-5
games were absent from that open/unopened listing and stay `event: null`.
PHI@CHI is listed under `ineligible_incomplete` because its T−7d opened
`2026-09-22T00:15:00Z`. Do not move it back into `events`.

Re-check the public listing before admission if the schedule may have changed:

```bash
python3 resolve_event_tickers.py --live \
  --registry ../nfl_factorial_lab_20260921/RESERVED_HOLDOUT.json \
  --snapshot /tmp/kxnflgame-listing.json \
  --panel /tmp/prospective-panel.json
```

That command GETs `/trade-api/v2/events` with `series_ticker=KXNFLGAME`,
status `open` or `unopened`, and `with_nested_markets=false`. It does not
request settled markets, nested prices, or any order route. Compare
`/tmp/prospective-panel.json` to the committed panel. A different ticker or a
newly listed week-5 game is a new `panel_version` and a new database, still
stamped only if that game's entire T−7d is in the future. Do not paste a
ticker the listing did not return. `JAX` matches Kalshi `JAC`, and `LA`
matches `LAR`; those are the only aliases.

## 3. Admit, then switch

The earliest included window is PIT@CLE at `2026-09-25T00:15:00Z`
(2026-09-24 20:15 America/New_York). `admit.py` stamps the actual UTC time and
refuses the whole panel if that instant, or any later included T−7d, has
already passed. There is no flag to choose an earlier time.

```bash
python3 admit.py \
  --panel prospective_panel.json \
  --out capture-data/prospective/admitted_panel.json \
  --log capture-data/prospective/admission_log.jsonl
```

The log line records `admitted_at`, `panel_version`, `panel_sha256`, each
event id, each `t_minus_7d_start`, and the games that were not backfilled.
`collector_running` and `production_claim` stay false in the log. Starting
the process is a separate step. `admission_log.template.json` shows the fields
with `admitted_at` null; do not fill that template in by hand.

If `admit.py` exits because PIT@CLE's window has opened, leave this panel
file unchanged. Build a new panel version that moves PIT@CLE into
`ineligible_incomplete`, and admit only the games whose windows are still
entirely in the future. Start a new database for that version.

Start the stamped panel only after the smoke container is stopped:

```bash
docker compose -f compose.yaml -f compose.prospective.yaml up -d --build
docker compose logs --tail=30
```

The override reads `/data/prospective/admitted_panel.json`. The unstamped
panel in the image is refused. Keep the development database. Supervisor
restarts are finite one-day sessions (`--seconds 86400`), not a new admission.

## 4. After a restart

A restart of the same stamped panel and the same database continues inside
windows that are already open and records the book gap. It does not rewrite
`admitted_at`. It does not turn a late first start into a full window.

Coverage is incomplete for any game whose first process start was after
T−7d. Do not describe that game as a full-window holdout, and do not drop it
from the log.

## Explicit non-claims

Preparing these files does not start a host, create a cloud bill, or collect
a prospective tape. The prior 32-game registry is not a complete cohort.
Week-5 identities are unresolved. No strategy profit is measured here.
