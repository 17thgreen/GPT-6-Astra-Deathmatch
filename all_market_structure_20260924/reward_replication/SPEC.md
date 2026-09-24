# AMS-007: prospectively watch fresh short reward windows

Hypothesis: newly active short reward periods with large reward per target-sized
one-cent quote principal can repeatedly present missing-side quote opportunities.
AMS-005 found a promising single Miami hour. AMS-006 showed that slow Truflation
rewards were accompanied by full-size cheap executions within minutes. Neither
establishes a profitable strategy. Search all categories, not a weather-only list.

Before new observations: run twelve catalog cycles at one-minute start intervals,
with a 780-second soft wall budget. Refresh active liquidity programs, limit 10000;
if a cursor remains, fetch one additional page and report any cap. Only admit
programs whose start is at or after this experiment's frozen start timestamp,
whose positive duration is at most two hours, whose positive reward and target
give an ideal half-pool rate / (target*0.01) of at least 1 per hour, and whose period
is current and unpaid. Rank newly seen programs by start time, descending ratio,
then ticker and ID. Track at most the first 30 distinct tickers; retain the first
program per ticker. Select on program metadata before inspecting any book. No
replacement based on prices, depth or trading activity.

Each cycle: save the fixed-to-date selection, then fetch full books and metadata
for still-current selections in batches of 50. Reuse AMS-005 classification and
the one-cent non-crossing gate. Preserve receipt timestamps and program changes.
On the final cycle fetch one public trade page per selected ticker (limit 1000),
report remaining cursors; classify with AMS-006's direction/price function. Four
concurrent requests, 12-second timeout, no retries, public GET only.

Report program/ticker/series counts, eligible and failed observations, whether
fresh-window gaps recur, target depths, ideal reward rates and remaining budgets.
Describe compatible prints in the new program window. No continuous-uptime claim
from minute snapshots. Never mark a virtual order filled from disappearance or
assign public prints as our fills. Do not count a book-only hypothetical reward
as income: inserting an order changes executable prices and can attract takers.

Stop after the bounded window whether results are positive, negative or missing.
Do not extend the watch to chase a favorable new program. A failure to observe
enough new programs is an inconclusive replication, not a successful strategy.
No real or demo orders, no credentials and no change to financial risk limits.

Primary sources: Kalshi liquidity help, incentive API, batch books API and public
trades API cited in AMS-005 and AMS-006.
