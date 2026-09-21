# Recorder operations

The recorder has no order-entry capability. It issues public market-data GETs.
The included panel contains two development events already observed in Q1/Q3;
it is not the reserved future evaluation cohort.

For a finite local session, from the kit root:

```bash
python3 collector/record.py --panel collector/development_panel.json --database capture-data/capture.sqlite --seconds 3600
python3 collector/inspect_capture.py capture-data/capture.sqlite
```

Repeat the same command to resume. Completed trade-pagination watermarks survive
restart. Queries overlap by 120 seconds, and trade IDs deduplicate. A process
restart always records a book-observation gap; snapshots during the outage
cannot be recovered. A failed or incomplete page sequence never advances its
watermark. The default one-day session is finite.

For continuous collection on an existing Docker host:

```bash
docker compose up -d --build
docker compose logs --tail=30
docker compose stop
```

The supervisor restarts finite daily sessions and failed processes. Store
`capture-data` on durable local disk, not an ephemeral container filesystem.
Back up SQLite using its backup API or after stopping the recorder, rather than
copying a live WAL database incompletely. Reserve disk space and monitor growth.
No cloud host, credentials, account charges or unattended service was created
by preparing these files. Docker deployment commands are provided, not claimed
to have been executed in this workspace.

Panel entries require a returned Kalshi event ticker and a verified scheduled
kickoff. The collector checks the event's identity, complementary market
structure, cent-price grid and tie-rule metadata before recording. It polls only
from T−7d through T−3h plus five minutes. Schedule changes must be reviewed and
dated. A changed panel hash cannot silently resume an existing database; retain
that database and start a separate collection directory.

Expand the development panel deliberately as more games become available.
This implementation rejects `purpose: holdout`: admission of the reserved
future cohort requires a separately reviewed configuration with code/settings
frozen before its windows and verified identities. `RESERVED_HOLDOUT.json` is
a prior registry, not proof that its games are being recorded.

Use receipt/commit times for feature availability. Cursor exhaustion means
retrieval completion for that request, not certainty that no delayed trade will
be published later. Public depth is not an authenticated own-order queue
position. Neither this capture nor a restart test proves simulated fills.
