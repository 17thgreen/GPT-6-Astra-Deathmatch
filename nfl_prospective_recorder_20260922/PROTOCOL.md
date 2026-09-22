# Prospective NFL recorder admission

Status: **SPECIFIED BEFORE CAPTURE**. This file freezes the admission rules
before any prospective tape and before any strategy outcome on these games.
Committing it does not start a recorder, admit a cohort, or place an order.

This directory is the reviewed path for a GET-only durable recorder. The Q4
collector at `nfl_timing_lab_20260921/collector/record.py` stays frozen. That
snapshot still rejects every panel whose `purpose` is not `development`. Do
not edit it to sneak a holdout cohort into an old database.

## Question this path can support later

Can a predeclared schedule-only cohort be recorded, with public books and
trades only, from each game's T−7d start through T−3h, without backfilling a
missed open and without reading outcomes to choose the games?

This protocol does not answer that question. It only makes a later admission
checkable. No profit comparison is authorized here.

## Freeze-before-window

1. Freeze these rules, the recorder allowlist, and the panel's event list
   before each included game's T−7d instant.
2. Admission time is the actual UTC time `admit.py` stamps. It is not a
   reconstructed earlier time. The recorder accepts a new database only when
   that stamp is within ten minutes of process start and is **strictly before**
   every included T−7d start.
3. A restart of an existing database may continue inside an open window. The
   restart records a book gap. It does not move the original admission time
   backward and it does not make a late first start into a full window.
4. If a window has already started, move that game to `ineligible_incomplete`
   in a **new** panel version. Do not put it in `events`. Do not point the
   late panel at the previous database (the panel hash would not match, and
   must not be overridden).
5. Do not replace a game, drop a loss, or choose a cohort after seeing a
   score, settlement, price, or strategy result.

T−7d is exactly 604800 seconds before the scheduled kickoff in UTC. That is
the same cutoff the recorder uses when it decides a market is active. The
active poll continues until T−3h plus five minutes, matching the Q4 recorder.

## Already missed, do not backfill

`2026_03_PHI_CHI` / `KXNFLGAME-26SEP28PHICHI` kicks off
`2026-09-29T00:15:00Z`. Its full window opened `2026-09-22T00:15:00Z`
(2026-09-21 20:15 America/New_York). No durable recorder was running at that
instant. The prior 32-game reservation
(`nfl_factorial_lab_20260921/RESERVED_HOLDOUT.json`, same schedule as the Q3
holdout manifest, frozen `2026-09-21T15:29:51Z`) is therefore **ineligible as
a complete-cohort profit comparison**. Label PHI@CHI incomplete. Do not
rewrite its admission time.

## Next clock, and the cohort this path actually admits

The next reserved kickoff is PIT@CLE, `2026-10-02T00:15:00Z`. Its T−7d starts
`2026-09-25T00:15:00Z` (**2026-09-24 20:15 America/New_York**). A full window
for that game exists only if the stamped admission and the first recorder
process both happen before that instant.

The cohort is a **new schedule-only version**, `cohort_kind:
schedule_only_new`. It is not a silent edit of the 32-game registry.

- Include a reserved game only when its entire T−7d is still in the future at
  admission and a public listing row has been matched to a venue event ticker.
- Leave unmatched games in `unresolved_identities` with `event: null`. Do not
  invent a ticker from the date pattern.
- Week-5 games that are absent from the open listing stay unresolved until a
  later public listing, a new panel version, and a new database, still before
  their own T−7d starts.
- `complete_prior_32_game_cohort` must be false. Setting it true is a failed
  validation, not a claim.

`purpose: prospective` is the label for this new version. `purpose: holdout`
is accepted only when `reviewed` is true and the same no-backfill rules hold.
A bare `{purpose: holdout}` panel still fails. Neither label revives the
32-game gate.

## Identity resolution (public listing GET only)

Venue tickers are filled from:

`GET https://api.elections.kalshi.com/trade-api/v2/events`

with `series_ticker=KXNFLGAME`, `status` of `open` or `unopened`,
`with_nested_markets=false`, `limit`, and a pagination `cursor` only.

Match a schedule row only when the listing contains
`KXNFLGAME-{YY}{MON}{DD}{AWAY}{HOME}` for the kickoff's America/New_York
calendar date and the subtitle begins with those ticker team codes. The only
schedule-to-ticker aliases are ones already published on earlier games:
`JAX`→`JAC` and `LA`→`LAR`. If the row is missing or the subtitle disagrees,
the game stays unresolved.

Do not request settled or closed events. Do not request nested markets. Do
not keep scores, results, settlement values, bids, or volumes in the panel or
the listing snapshot. The long-running recorder allowlist stays the Q4 set:
one event metadata GET, one market order book GET, and the public trades GET.
The recorder does not gain the events-collection route, so a panel cannot
redirect it at an arbitrary query.

## Admission log

Each real admission appends one record. Required fields:

- `admitted_at` — actual UTC stamp, never backfilled
- `panel_version`, `cohort_id`, `cohort_kind`, `purpose`
- `panel_sha256` — hash of the stamped panel bytes the process will read
- `events` — `game_id`, venue `event`, kickoff, `t_minus_7d_start`
- `not_backfilled` — games whose windows were already open, with the reason
- `collector_running: false` until an operator has actually started a host
- `production_claim: false`

`admission_log.template.json` is the empty form. `admit.py` writes the host
copy under `capture-data/` and refuses a stamp that is already too late for
any included game. There is no flag to choose an earlier timestamp.

## What this repository state is not

- Not a running collector. Docker files are instructions for a durable host.
- Not a full-window capture of PHI@CHI or of the original 32 games.
- Not a strategy result, a shadow P&L, or a live order.
- Not permission to use account, portfolio, or order endpoints.
