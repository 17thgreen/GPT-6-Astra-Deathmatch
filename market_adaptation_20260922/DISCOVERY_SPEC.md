# Bounded six-market historical availability audit

Specified before queries. This is metadata discovery only; no prices or outcomes
enter selection and no profitability experiment is run by this audit.

Query KXNFLGAME, KXNCAAFGAME, KXWNBAGAME, KXMLBGAME, KXNHLGAME and KXNBAGAME.
Use market close timestamps from September 1 00:00 UTC through September 21
00:00 UTC, 2026. Exhaust at most 20 pages per series, limit 1000, three attempts
and 15-second timeout per request. Record full raw responses and source times.
Require ticker-encoded date in September 1-20 for the candidate list; that date
is only a selection key, never a substituted game start.

Count unique event IDs and distinct dates independently by series. Reserve up to
eight event IDs by round-robin across ascending dates, within each date sorted
by full ticker. This is a deterministic bounded engineering sample, not an
estimate of whole-calendar trading capacity. No fill tapes are fetched here.
Zero/few events and pagination failures remain explicit. No substitution with
another season, sport or future games. Contract/schedule/fee admission and a
policy/cohort freeze are required separately before replay.

This audit prioritizes the next independent market adapters. It does not certify
the selected events as full-game two-outcome contracts, prove historical tape
availability, assert a matched profitability cohort, or create a live bot.
