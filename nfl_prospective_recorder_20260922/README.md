# Prospective NFL recorder

Reviewed GET-only recorder for a new schedule-only cohort. Read
[PROTOCOL.md](PROTOCOL.md) and [OPERATIONS.md](OPERATIONS.md). The frozen Q4
collector is unchanged and still rejects an unreviewed holdout panel.

`prospective_panel.json` version `2026-09-22.1` is not admitted
(`admitted_at` is null). It will not record until `admit.py` stamps a copy
strictly before every included T−7d start. The earliest of those starts is
PIT@CLE at `2026-09-25T00:15:00Z` (2026-09-24 20:15 America/New_York), venue
id `KXNFLGAME-26OCT01PITCLE` from a public events listing. PHI@CHI is not in
the poll list. Week-5 games have no venue id yet.

This directory does not run a collector and does not place orders. The engine
is adapted from `nfl_timing_lab_20260921/collector/record.py`. No
redistribution license is added.

Unit tests, from this directory:

```bash
python3 -m unittest -v test_prospective_recorder
```
