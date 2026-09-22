# M4: independent CFB evaluation, MLB transport and separate sizing studies

Authorized September 22 after M3. Preserve every NFL/Q7/M2/M3 source and result.
Commit this specification before new metadata/tapes/outcomes, then commit the
cohort and source/input freeze before simulation. No live orders or transfers.

## Reserved cohorts and admission

- CFB evaluation: all eight NCAAF reservations in M3 MARKET_AVAILABILITY.json,
  unchanged. Assert zero overlap with M2. These are unseen-by-replay historical
  games from earlier September, not chronological forward or live validation.
- MLB transport: all eight MLB reservations from that same file, including the
  Detroit/Cleveland G1 doubleheader. Do not replace failed or quiet events.
- NHL: review all seven reservations for schedule identity, season phase,
  full-game rules, tie/fractional payouts and collateral compatibility. This
  stage is admission research, not a required profit replay on unsupported rules.
- NBA: separately query May 1-20, 2026 event dates. Union live and historical
  metadata for KXNBAGAME (historical series filter has no date filter); at most
  twenty 1000-market pages per endpoint. Require exhausted pagination before
  round-robin selection across ascending dates, ticker order within date, up to
  eight events. Retain zero/sparse/failure outcomes. Freeze the reservation before
  any future tape replay. This stage establishes an admitted season cohort.

Retrieve public series/event metadata and exact related full-game milestones.
Require two $1 binary, linear-cent markets, opposite participants, MECNET and
mutual exclusivity; one exact-event Sports milestone of the appropriate type;
listing before the replay entry stop. Never use close_time or ticker time as
actual start. Record title/rules/date/team/game-number checks, event fee overrides,
and exception mechanics. A historical milestone is a reconstructed schedule,
not proof of what was known at the time. Retain original responses/receipt times.
CFB/MLB ordinary scheduled-game replay is conditional on this reconstruction;
postponement/lifecycle histories and immediate collateral release remain limits.
Ambiguous identity or incompatible rules block the sport's full reserved cohort.

Resolve current series/event quadratic fee coefficients. New-cohort replay
requires one common coefficient pair within that sport; incompatible or mixed
fee rules block that sport rather than silently applying NFL fees. These are
current-rule counterfactual costs, not verified historical fee schedules. Reused
M3 development controls retain M3's original modeled fees for exact comparison.

## Data

Read historical/cutoff and route trade intervals across live/historical storage
boundaries; candles route by market settlement tier. Require complete pagination,
identity, fixed-point prices and sizes, no blocks, no conflicting duplicates.
Public GET only, three attempts per request, 15-second timeout, four workers,
200 trade pages per ticker/tier, candles in three-day slices. Preserve partial
captures and failures. Per sport, all reserved markets must capture successfully;
no profitable subset replay. Missing quote minutes remain missing.

For CFB/MLB capture max(listing,T-7d) through T-30m+5m. Delayed candle bid/ask
closes use 60-second hypothetical delivery and 300-second quote-age limits. No
terminal result, closing price or future volume enters decision observations.

## Frozen experiments

1. New CFB cohort: cutoff T-3h/T-30m x NFL final-12h/constant queue profile x
   early queue 3300/10000 x delay .25s/5s = 16 alternatives.
2. New MLB cohort: the identical 16 alternatives, with its admitted fees.
3. Reused CFB development games: T-30m and constant assumed queues only;
   coupled order size/event cap 25/100/250 x original Q7/complete-first policy x
   queue 3300/10000 x delay .25s/5s = 24 alternatives.
4. Reused WNBA development games: the same 24 sizing/completion alternatives.

Total 80 declared cases if CFB/MLB admission and capture both complete. All cases
have independent $5000 alternative accounts. They are NOT concurrent bots and
their returns must not be summed as portfolio profit. Constant queue is an
environmental sensitivity, never a dial controlled by the bot or measured access.
Retain the actual-start clock adapter, price guard, route selection, priority,
.5 participation and five-minute winddown. Total taker exit allowance remains
250/game even when order/cap is smaller; do not claim smaller-size gains come
from greater assumed liquidity. No entry margin or flow-window threshold search.

Complete-first changes one inventory policy: when abs(event inventory)>=.01,
keep only selected Q7 routes that offset inventory; bound each offset by current
inventory minus other pending offsets. Request cancellation of exposure-adding
orders and refresh immediately after a public-print fill. Cancellation latency
still permits pending fills; no retroactive cancel or free priority. Once flat,
ordinary pair admission resumes. No new forced taker exit or price concession.
Original mode delegates unchanged and must exactly reproduce eight M3 constant
T-30m size-250 control fill/order histories across CFB/WNBA/queues/delays.

## Audits and decision rules

Unit-test changed sizing, latency/pending offsets, metadata/tier/quote schema and
independent financial validation. Audit all scenarios for fees, cash, inventory,
entry/cutoff timing, maker order quantities and shared per-game exit allowance.
Any residual position means completed net is null, never terminal-winner credit.
Preserve failed runs and all tried variants. Hash imported frozen inputs/source.

Report per-game net, net/$1000 initial bankroll, net/1000 filled contracts,
completion cost/volume, inventory duration/cost-hours, coverage and concentration.
Distinguish deployed inventory cost from resting reservations and total bankroll.
CFB's later window earns further evaluation only if completed net and the paired
cutoff improvement are positive at BOTH constant queue depths and BOTH delays,
all cases are flat, and late-window net remains positive after removing its best
game; report NFL-profile differences separately. This is a research continuation
screen, not statistical significance or live promotion. All sizing variants use
development games; record mechanism effects, never call a winner validated.

## Capital allocation and feasible compounding

After these results, publish readiness for equal-total-capital fixed versus
shared funding, matched-calendar capacity and reinvestment studies. A development
winner alone cannot justify a fleet profit claim. Do not compound short-sample
percentages or double-count public flow. Freeze the next portfolio experiment
separately only when candidates/cohorts support it. User handles forward work.

Official API references consulted before implementation:
- https://docs.kalshi.com/getting_started/historical_data
- https://docs.kalshi.com/api-reference/historical/get-historical-markets
- https://docs.kalshi.com/api-reference/historical/get-historical-trades
- https://docs.kalshi.com/api-reference/historical/get-historical-market-candlesticks
- https://docs.kalshi.com/api-reference/market/get-series
