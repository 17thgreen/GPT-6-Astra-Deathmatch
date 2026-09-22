# M3: CFB gains from later trading if near-game queues are accessible

All 32 frozen individual-sport scenarios completed, finished flat and passed
independent financial audits. All eight unchanged controls reproduce exact M2
fill and order histories. Q7 remains the selected NFL development candidate;
its source, parameters and evidence were not changed.

The useful new finding is conditional: **CFB benefits from extending pregame
trading to a T-30m cutoff under constant-depth queue environments.** WNBA remains
negative under every tested combination. This supports separate market research,
not a claim that an adapted CFB bot already beats NFL or has verified live access.

## Complete fast-delay comparison

Net completed simulated dollars, one $5000 account per row/sport alternative,
four reused games per sport, .25-second submit/cancel delays. Winddown begins
five minutes before the stated cutoff. All modeled fees are included.

| Queue environment | Cutoff | CFB, q3300 | CFB, q10000 | WNBA, q3300 | WNBA, q10000 |
|---|---|---:|---:|---:|---:|
| NFL final-12h depth | T-3h | +$2.47 | -$2.80 | -$45.18 | -$35.29 |
| NFL final-12h depth | T-30m | +$2.47 | -$2.80 | -$47.42 | -$32.83 |
| Constant assumed depth | T-3h | +$16.01 | +$6.37 | -$45.18 | -$35.29 |
| Constant assumed depth | T-30m | +$79.02 | +$30.51 | -$39.17 | -$34.31 |

Constant depth is an unverified environmental sensitivity: 3300 or 10000 ahead
throughout, instead of the inherited 1,327,847.005 inside the final 12 hours.
It is NOT a setting that changes venue queues. Both cutoffs are compared under
each environment. The clean late-cutoff effects for CFB at constant depth are
**+$63.01** and **+$24.13**, not the full jump from the NFL-profile controls.
The latter would bundle a changed queue assumption with changed trading hours.

Five-second latency yields $75.85/$29.90 for CFB's later/constant cases versus
$79.02/$30.51 at .25 seconds. The old-cutoff constant/q10000 case differs by
$0.0001; all other net values are unchanged by the delay sensitivity. Full exact
values and contrasts are in results/summary.json and results/contrasts.json.

## The CFB improvement changes completion, not just the headline

At constant q3300, extending the cutoff raises maker contracts from 18,956.84 to
43,347.43 while reducing taker closing contracts from 500 to 139.63. Passive
completion rises from 94.86% to 99.36%. Median pairing time in the later case
is 5.56 minutes, versus 129.61 minutes in the original M2 NFL-profile case.
That last comparison combines timing and queue changes; it is descriptive.

The later q3300 net comes from three positive games: Syracuse/Pittsburgh
$11.6833, Houston/Texas Tech $35.2126, Miami/Wake Forest $32.1241; Portland
State/Oregon has zero fills. Removing the two best leaves $11.6833. At q10000
all three trading games remain positive, but only four games were reserved.
These concentration diagnostics are not an independent holdout or robust
expected-return estimate. No post-result threshold search was performed.

Inventory acquisition-cost exposure is $24,927.65-hours for later constant q3300,
versus $24,416.31-hours for its T-3h constant-depth control. This is FIFO cost of
carried inventory including entry fees; it omits resting-order reservations and
must not be described as total committed capital or bankroll turnover.

## Pound-for-pound interpretation

On filled-contract efficiency, later/constant CFB earns $1.82 per 1000 filled
contracts at q3300 and $1.54 at q10000. NFL Q7's preserved figures are $1.08 and
$0.75, but NFL uses the large final-12h queue profile and a different 31-game
calendar. **This is insufficient to rank CFB above NFL.** It identifies a
market-specific hypothesis worth a separately frozen evaluation.

CFB's later/constant q3300 case earns $15.804 per $1000 initial bankroll over an
8.104-day reconstructed window; NFL's existing result is $70.866 over 17.875
nominal days. The corresponding descriptive daily averages are $1.95 and $3.96
per $1000 initial cash. These include idle cash and differing opportunity counts.
Neither is an annualized forecast or an actually-invested-capital return.
The full existing-control comparison is in COMPARISON.md.

WNBA still requires different entry/sizing/completion research. Later constant
q3300 gets some passive completion (56.55%) but remains $39.17 negative. More
trading and improved completion percentages did not make this cohort profitable.
Do not deploy it or declare the sport inherently unprofitable from four games.

## What comes next, independently by market

1. **CFB:** evaluate the late-window hypothesis on the next frozen cohort, keep
   queue stresses separate, then test a small declared set of coupled size/cap
   profiles and completion-aware admission. Do not retune NFL to fit CFB.
2. **MLB:** complete full-game/doubleheader/postponement and schedule admission,
   then run its own control and timing study. The new metadata audit found 268
   candidate events across 20 dates in the declared window; eight are reserved
   by date/ticker only. Abundant events do not prove profitable fills.
3. **WNBA:** prioritize preventing unpaired inventory and evaluating smaller
   coupled order/cap profiles. Prior NFL Q2/Q4 failures remain preserved.
4. **NHL:** seven candidates across two dates were found; resolve rule, period,
   season-phase and fractional-settlement compatibility. It remains a sparse,
   unscored market, with all seven retained in the metadata reservation.
5. **NBA:** no matching events were returned in the declared September 1-20
   date/close window. A separately declared prior-season cohort is needed; do
   not substitute October snapshot spreads for historical profit evidence.

NFL metadata discovery found 30 events/six dates; NCAAF 372/twelve dates; WNBA
14/four dates. These are bounded query results, not full league schedules.
No discovery request failed and pagination was exhausted for all six series.
All reservations are metadata-only, require admission, and carry no new profit
claim. Raw responses and selection logic are preserved.

After strategy candidates survive independent market testing, compare equal
total capital over a matched calendar, then capital capacity and reinvestment.
Actual compounding requires feasible resizing from realized cash while preserving
cash/exposure/exit limits; a repeated short-sample percentage does not measure it.

## Verification, source and data

- M3 spec committed before extension/outcomes: 58ae378.
- Source/input freeze committed before outcomes: f20bd36.
- Twelve new tests plus 162 inherited tests pass (174 total).
- All 32 financial ledgers independently reconcile. Eight original-profile
  controls exactly match M2 fills/orders. All 140 frozen file hashes match.
- Six-market metadata audit specified before queries at f80f984. Every original
  response, receipt timestamp, reservation and zero/sparse result is retained.
- Extension: 11,971 trades and 2,158 candle records; merged tape has 84,447
  observations after 15 identical overlap records were deduplicated.
- Historical queues, lifecycle/receipt times, fee history, collateral release,
  market response and executable exit depth remain assumptions/limits inherited
  from M2. No terminal winner settlement is used to rescue residual inventory.

All M3 raw inputs, financial outcome ledgers and the sixteen M2 control ledger
files needed for verification fit in Git and are included in this checkpoint.
No external outcome archive is required for this study. From this directory,
`python verify.py` audits all 32 outcomes and eight controls; `python analyze.py`
recreates the descriptive contrasts. Running run.py over existing results is
deliberately refused. Full pair-decision logs are not retained in M3; repeated
checks/rejections are counters, while all financial fills and orders are retained.

A one-off post-result latency-inspection command had a scenario-name slicing
KeyError. It did not modify any outcome; analyze.py uses the corrected lookup
and records all sixteen latency contrasts. The matrix and financial audit had
no failures. No live orders, transfers or always-on services were created.
