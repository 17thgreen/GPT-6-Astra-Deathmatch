# Pound-for-pound comparison and the path to feasible compounding

Existing frozen results, normalized without changing any historical experiment.
Primary rows use early queue 3300, .25-second delays, $5000 initial cash and the
NFL final-12h queue assumption. Filled-contract volume includes both maker and
taker contracts, so expensive completion is not omitted from the denominator.

| Market | Games | Net per $1000 starting cash | Net per 1000 filled contracts | Median time to pair | Passive completion |
|---|---:|---:|---:|---:|---:|
| NFL Q7 | 31 | +$70.87 | +$1.08 | 16.5 minutes | 98.74% |
| NCAAF M2 | 4 | +$0.49 | +$0.46 | 129.6 minutes | 100.00% |
| WNBA M2 | 4 | -$9.04 | -$30.12 | 1388.8 minutes | 0.00% |

At queue 10000, net per $1000 starting cash becomes NFL +$18.09,
NCAAF -$0.56 and WNBA -$7.06. NFL's selected candidate has the strongest evidence
in this comparison. Different cohorts, calendars and opportunity counts prevent
interpreting these rows as an equal-opportunity sport ranking. The NFL cohort is
reused development data; the expansion pilots are small development samples.

The respective reconstructed calendar spans are 17.875, 8 and 2.9722 days.
Observed net per $1000 initial cash per day is +$3.965, +$0.0617 and -$3.0405.
These are arithmetic averages across the observed spans, including idle cash;
they are neither matched-calendar trials nor annualized forecasts. NFL's span
uses its nominal seven-day windows; the expansion spans are listing-bounded.
EXISTING_COMPARISON.json contains exact inputs and definitions; reproduce with
`python compare_existing.py`. No return on actually deployed capital is claimed.

NBA, MLB and NHL have descriptive book snapshots, but no admitted historical
profit replay in this repository yet. Their spreads and depths cannot fill a
profitability table. This missing evidence is explicit, not a zero-return result.

## Protect the NFL result while adapting each market

Q7 stays frozen. Each market gets its own profile and experimental directory,
with the NFL settings as a reference arm. Shared accounting, cash reservations,
fee handling, price guard and priority retention remain governed by regression
checks. Market-specific windows, order size/cap, flow horizon, inventory age and
completion policy are separate research levers. They are not changed all at once.

Crucially, queue depth, cancellation ahead and executable exit liquidity are
environmental assumptions or observations. They are not knobs we can turn to
make a bot profitable. Queue scenarios measure robustness; favorable assumed
execution cannot qualify a market. Kalshi documents price-time queue priority:
https://docs.kalshi.com/api-reference/orders/get-order-queue-position

M3 first isolates the clock: T-3h versus T-30m, with unchanged limits, compared
under both the NFL late-depth profile and constant-depth sensitivities. Next,
test coupled order-size/inventory caps and completion rules within each market.
Small orders failed in NFL's Q4; that finding remains intact and does not prove
the same sizing is correct for a much thinner sport. Preserve all trials.

## What maximum compounding needs

The target is completed net growth of a finite bankroll under explicit drawdown,
exposure and liquidity limits. A high return percentage on a tiny trade may lack
capacity; high volume can lose money; rapid turnover can multiply costs.

Use two complementary comparisons:

1. Mechanism efficiency: net after modeled costs per filled contract, completion
   rate and cost, inventory duration, and acquisition-cost dollar-hours.
2. Portfolio economics: the SAME initial bankroll over the SAME calendar span,
   including idle time and all admitted opportunities, with aggregate risk and
   queue/exit constraints. Measure net dollars, downside and cash utilization.

Only then evaluate reinvestment. A compounding simulation must update available
cash from realized outcomes, resize feasibly, retain limits and avoid awarding
the same tape twice. Do not multiply a short-sample percentage through a season.
Test capital capacity at declared levels and compare fixed bot funding with a
shared reserve at equal total funding. Capital reallocation is useful only where
profitable capacity exists. The M2 combined account had excess cash; that was
not its bottleneck.

The user handles forward validation. The research work continues through source,
data, controlled historical experiments and explicit limitations without making
live deployment a prerequisite.
