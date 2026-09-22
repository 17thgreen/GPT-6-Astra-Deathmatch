# Other-market progress — September 22, 2026

New result: a six-sport book census and tested adapter components now exist. No
non-NFL historical replay or profitability result has been produced yet.

Snapshot window: 2026-09-22T17:03:26.487090+00:00 through 2026-09-22T17:06:28.125672+00:00 (UTC).

| Market | Events / tickers attempted | Usable two-sided books | Positive buffered margin | Median margin (cents/pair) | Median larger best-bid level (contracts) | Errors |
|---|---:|---:|---:|---:|---:|---:|
| NFL control | 5 / 10 | 8 | 8 | 0.148 | 114,571 | 2 |
| College football | 5 / 10 | 8 | 8 | 0.532 | 9,445 | 2 |
| NBA | 3 / 6 | 6 | 6 | 1.111 | 387 | 0 |
| WNBA | 5 / 10 | 8 | 8 | 0.432 | 29,344 | 2 |
| MLB | 5 / 10 | 10 | 10 | 0.554 | 408,194 | 0 |
| NHL | 5 / 10 | 10 | 10 | 0.275 | 3,265 | 0 |

The margin is a static same-contract YES+NO bid-pair estimate after nominal
maker fees and the inherited comparison buffer. It is cents per one matched
pair, NOT dollars of profit, ROI, fill probability or an executable simultaneous
purchase. Both orders must receive fills; one-sided fills can lose money.
Displayed best-level depth is not authenticated queue position. No future
cancellations, matched volume or turnover have been assumed.

Sampling: first five open events in API order, first two sorted tickers per event.
NBA returned three events. All six failures were book-request timeouts, retained
without retries or replacements. The sample is small, nonrandom and observed at
different times to game start; two tickers of one game are not independent
opportunities. No event has been pregame-admitted by this census. A current book
cannot stand in for a historical order-book series.

## What this changes

- **College football stays first for full-core adaptation.** Its sampled median
  buffered spread is .532 cents versus NFL's .148, and larger best-level depth
  is roughly 9,445 versus 114,571 contracts. This supports investigating queue
  access there; neither number establishes better fill rates or profitability.
- **NBA is attractive structurally, but its sample is not comparable to near-game
  NFL.** All three event tickers refer to October 20 games. The six markets show
  median reported 24-hour volume around 213 contracts. Wider spreads and low
  displayed depth can coexist with very slow fills. Do not transplant the NFL
  seven-day window or infer frequent capital recycling from these books.
- **WNBA offers a closer-dated basketball path.** This sample has same-day game
  tickers, .432-cent median indicative margin and deeper queues than NBA's sample.
  Start-time linkage and state handling determine usable pregame windows.
- **NHL deserves a parallel queue study.** Displayed depth is lower here; observed
  flow, exceptional tie settlement and game timing still need separate treatment.
- **MLB is not automatically easier access.** The median larger best level is
  roughly 408,194 contracts. Higher activity may service those queues, but total
  daily volume is not direction- and price-specific service to our orders.

These are engineering inferences from this snapshot, not a performance ranking.

## Built this turn

1. `adapter.py`: listing-relative windows, explicit start-time inputs, schedule
   freshness and identity checks, pause on exceptional/in-play state, actual
   series/event fee override resolution, gross fractional-settlement payout and
   fixed-point best-bid diagnostics. A zero fee multiplier is preserved.
2. `schedule_bridge.py`: exact event-to-milestone matching with timezone-aware
   starts; missing/ambiguous matches fail instead of substituting close_time.
   This bridge was added after the census implementation freeze, is tested with
   fixtures and did not affect census selection or results. It still requires
   a fetched milestone response and an independently resolved event state.
3. `census.py`: bounded, GET-only discovery with retained source responses,
   receipt timestamps, fee inputs, raw books and errors in `CENSUS.json`.
4. Sixteen focused tests pass, and independent arithmetic checks match all 50
   usable snapshots. Frozen source hashes match before and after collection.

These components are execution-neutral. They do not yet wire a complete
cross-sport portfolio replay, cancel existing orders on a changed schedule,
verify exhaustive special-settlement states, or implement live order management.
Fractional settlement returns gross payout; it does not book that cash or deduct
historical cost inside Q7's portfolio. Older frozen engines remain untouched.

## Remaining adaptation map

| Market family | Carryover | Remaining mechanics |
|---|---|---|
| College football | Q7 guard, fees, passive routing, reservation logic | Historical schedule/receipt-time normalization and complete exceptional states |
| NBA/WNBA | Same maker kernel | Listing-relative windows, schedule linkage and market-specific flow/queue profiles |
| MLB/NHL | Same kernel for matching full-game outcomes | Doubleheader/period identity, postponement/tie rules, flow and depth |
| Tennis | Quote/fee logic and two-player ordinary outcome structure | First-ball, walkover/retirement rules and shifting starts |
| Spreads/totals | Same-contract YES/NO pairs | Exact strike identity, correlated game limits, no assumed cross-threshold netting |
| Soccer three-way | Same-contract binary maker components | Three-state inventory for cross-team/draw routing |

The next substantial milestone is a frozen historical NCAAF/WNBA comparison
with verified game-start mappings, explicit window settings and one shared cash
account. That is research work, separate from user-owned forward validation.

## Provenance

Specification commit: cfe48ab. Adapter/census freeze: 079d7c7. Snapshot collection
followed those commits. No configuration search or strategy promotion occurred.
This report and all raw JSON are small enough for Git; no archive upload is needed.

Primary documentation:
- https://docs.kalshi.com/getting_started/orderbook_responses
- https://docs.kalshi.com/api-reference/market/get-series
- https://docs.kalshi.com/api-reference/milestone/get-milestones

Exact API request URLs and response receipt times are preserved per request in
CENSUS.json. Series and event metadata remain attached to each sampled book.
