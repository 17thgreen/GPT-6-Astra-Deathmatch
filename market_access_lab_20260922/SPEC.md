# M1: other-market adapter and public-book access census

Scope frozen before census, September 22 2026. This is engineering and descriptive
market research, not a profitability experiment or strategy promotion.

Build an execution-neutral adapter for listing-relative pregame windows, explicit
trusted start times, resolved series/event fees, fractional settlement bookkeeping,
and exceptional-state suspension. No use of close_time as a game start. Retain
Q7/Q8 frozen implementations unchanged; no live orders or increased risk limits.

Public GET-only census: NFL control plus NCAAF, NBA, WNBA, MLB and NHL. Take the
first five open events returned for each series (API ordering, not a random sample).
Inspect at most the first two sorted market tickers per event. Preserve source
metadata, request receipt timestamps, all errors and missing/one-sided books.
Evaluate only same-contract YES+NO passive bid pairs, never cross-team equivalence.
Use actual event fee overrides when present, otherwise series fees. For supported
quadratic fees, estimate nominal fees at each bid, subtract Q7's .0002 + 2*.0001/250
buffer for comparison; label indicative margin, not fill-level actual fee or P&L.

Summarize two-sided availability, positive buffered pair margin, displayed
best-level sizes and request errors by series. No queue fill probabilities,
turnover assumptions, annualization or profitability ranking. Counts are ticker
snapshots, not independent games. No cohort swapping or retrying until attractive.
Census is not pregame-admitted without independent trustworthy start timestamps.

Adapter tests: truncated listing windows, unavailable/moved start times, stop
cutoff, exception pause, unknown fee modes, zero fee overrides, .5 or fair-price
settlement without treating inventory as binary or realized profit beforehand.
This creates reusable inputs and accounting pieces, not a full non-NFL replay.
Commit spec, then source/tests before census, then findings. Next stage is a
separately frozen historical comparison using schedule provenance and shared cash.
