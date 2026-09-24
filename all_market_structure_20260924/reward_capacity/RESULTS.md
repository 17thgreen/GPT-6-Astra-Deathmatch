# AMS-012: $2.50 capacity and a hypothetical $5,000 deployment

The retained evidence supports at most **two $2.50 candidate orders in one public
book response**, not thousands. That is $5 of quote capital plus a $0.50 fee reserve.
The strict version that only joins already sufficient public depth supports at
most one candidate per recorded response. The two-order maximum includes one
small gap-completion quote. Both markets concern the same Miami hourly event.
These are historical snapshot opportunities, not currently available orders.

## Observed capacity

We reapplied the existing AMS-011 rules at exactly 250 contracts at one cent,
including programs with target sizes other than 1,000. Across 752 admitted
market observations, 96 side observations had a baseline qualifying quote;
17 passed the positive-cushion stress and 79 did not. These repeat observations
of books, not 96 independent trades. The passing observations reduce to three
distinct program/side combinations across two hourly Miami events. Sixteen
passing observations joined supported levels; one completed a smaller depth gap.

| Source | Baseline-qualified side observations | Positive cushion observations |
|---|---:|---:|
| AMS-005 | 7 | 0 |
| AMS-007 | 47 | 8 |
| AMS-009 | 19 | 0 |
| AMS-010 exploratory overlay | 23 | 9 |

The maximum pair occurred in the same response at 2026-09-24 05:04:07.893666 UTC,
AMS-010 cycle 8: KXTEMPMIAH-26SEP2402-T76.99 NO (supported level) and T79.99 YES
(gap completion). Combined conditional remaining rewards were $7.75; deducting
all $5 principal and the $0.50 reserve left $2.25, or 45% of quote capital / 40.91%
of capital plus reserve. This assumes future qualifying time and is not earned P&L.
Separate reward pools permit arithmetic addition here, but the event is correlated.
No observed count is a bound on every future market or hour across the venue.

## Timing and later screen states

| First passing program/side | Reward | Principal + reserve | Conditional cushion | Remaining minutes |
|---|---:|---:|---:|---:|
| 1am Miami T79.99 YES | $3.56 | $2.75 | $0.81 | 56.23 |
| 2am Miami T79.99 YES | $3.71 | $2.75 | $0.96 | 56.87 |
| 2am Miami T76.99 NO | $3.48 | $2.75 | $0.73 | 55.87 |

The 1am case passed first at cycle 3, failed the new-entry budget at cycle 4,
then passed cycles 5–11. Later AMS-009 observations at 04:29–04:30 UTC had
insufficient remaining reward budgets. The 2am T79.99 quote passed at cycles 7–8,
changed from supported to gap completion, and had no baseline qualifying $2.50
quote at cycles 9–14. The 2am T76.99 quote passed all seven observations 8–14.

Thus two of three distinct examples later failed a new-entry screen at least
once. **This is not a 67% order loss rate.** Later budgets start a new reward
clock and do not account for rewards an earlier order might have accumulated.
Nor do unmodified public books replay the hypothetical order's effect. We have
no observed order execution, credited rewards, settlement P&L or measured failure
probability. Canceled unfilled orders can avoid principal losses; fills may lose
principal and may stop reward accrual early. Correlated failures are possible.

The declared $3.71 illustration comes from a 57.93-minute program with 56.87
minutes remaining at observation. It assumes 50% future qualifying time, roughly
28.43 minutes, with the stressed score held constant. At that same score, about
21.03 actual qualifying minutes cover the $2.75 stake-plus-reserve deduction,
or about 42.06 elapsed minutes at 50% qualification. These are conditional
arithmetic thresholds, not measured order survival or a guaranteed minimum hold.
Scoring is per second; the $1 payment floor and cent rounding are applied by the
imported model. See the clean terms in the July 15, 2026 filing (pages 7–10):
https://www.cftc.gov/filings/orgrules/rules07152610358.pdf

## Hypothetical $5,000 quote capital

Assume 2,000 **distinct equivalent reward pools** with the previously declared
$3.71 conditional reward each. This is a capacity counterfactual, not a claim
that such markets exist. Splitting one large order into many small orders in
the same pool does not reproduce this calculation: those orders share its pool.

Quote capital is $5,000; the chosen fee stress is another $500. Under the
zero-failure scenario, reward receipts total $7,420. Deducting the entire $5,000
stake and consuming the $500 reserve leaves $1,920: 38.40% of quote capital,
or 34.91% of the $5,500 funding requirement. Losing all principal is a deduction
in this scenario, not a prediction about fills. This is not a worst-case return,
because actual rewards can be far lower than $3.71 per order.

For the sensitivity below, a failed order earns zero reward and loses its entire
stake; other orders earn $3.71 but also lose their entire stake. Every order uses
the full fee reserve. Failure fractions are assumptions, not estimates.

| Zero-reward orders | Assumed fraction | Rewards | Net after all stakes and reserves | Return on $5,000 quote capital |
|---:|---:|---:|---:|---:|
| 0 | 0% | $7,420 | $1,920 | 38.40% |
| 200 | 10% | $6,678 | $1,178 | 23.56% |
| 400 | 20% | $5,936 | $436 | 8.72% |
| 500 | 25% | $5,565 | $65 | 1.30% |
| 600 | 30% | $5,194 | -$306 | -6.12% |
| 1,000 | 50% | $3,710 | -$1,790 | -35.80% |
| 2,000 | 100% | $0 | -$5,500 | -110.00% |

Algebraic break-even is a 25.876% zero-reward fraction under exactly this severity
model. It does not mean the strategy is safe below a measured failure rate;
there is no measured rate, and the remaining orders' modeled rewards may change.

## Strict $5,000 total budget

Including the fee reserve within $5,000 permits 1,818 quotes: $4,545 of quote
capital plus $454.50 reserve, leaving $0.50 cash. The same zero-failure conditional
scenario gives $6,744.78 rewards and $1,745.28 net after deducting stakes and
reserves, a 34.91% return on the total $5,000 account rounded to two decimals.
SUMMARY.json also carries percentage-weighted failure scenarios for that size;
fractional failed-order counts there are sensitivity weights, not executions.

The reward horizon is approximately 57 minutes, but proceeds were not observed
and this is not a measured cash cycle. Filled capital can remain tied up until
exit or settlement; reward credit timing is separate. No hourly repetition,
daily extrapolation or compounding is justified by these observations.

## Verification and restoration

The protocol was published before fixed-size aggregation; code and five financial
and concurrency tests were frozen in commit 7f59d2d22a3de8950af88a865c894d766bc81c98.
Three independent selected-row ledger checks passed after calculation. Used
receipt hashes match the prior replay on all shared input paths. The case already
shown to the user ($3.71 for $2.50) was declared in the protocol, not newly chosen
after aggregating capacity. This remains reused descriptive analysis.

Restore the raw AMS-005, AMS-007, AMS-009 and AMS-010 archives identified by their
existing ARCHIVE.json files, keep reward_boundary/screen.py and
reward_competition/model.py at the hashes in FREEZE.json, then run
`python3 -m unittest -v test_analyze` and `python3 analyze.py` in this directory.
INPUT_HASHES.json records all input bytes read. SUMMARY.json contains the full
passing batch list, first examples, later observed states and scenario arithmetic.
No original experiment files were modified. No orders or new risk limits were set.
