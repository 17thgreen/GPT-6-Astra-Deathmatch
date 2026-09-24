# AMS-013: original missing-depth strategy capacity

The first strategy completes deficient reward-qualifying depth with a one-cent
bid and a 10% target buffer. Applying the same AMS-010 economic stress to retained
books found **13 distinct passing market/program pools in two hourly Miami
campaigns**, at most **seven at once**. Maximum quote capital was **$77**, plus
the modeled **$7.70 fee reserve**. These are historical candidate snapshots, not
current availability, actual orders or earned returns.

## What counts as a window

Several market-specific reward pools can exist within the same hourly event.
Thirteen distinct pools here do not mean thirteen hours of sequential deployment.

| Miami event ending, EDT | Basic gaps previously found | Distinct pools passing buffered economic stress | Maximum passing together | Maximum simultaneous quote capital |
|---|---:|---:|---:|---:|
| Midnight | 7 | 0 at the late captured times | 0 | $0 |
| 1am | 7 | 7 | 7 | $77 |
| 2am | 6 distinct original scanner alerts | 6 | 5 | $55 |

The midnight observation was too late for the stricter reward budget; it does not
establish that the earlier part of that hour had no opportunity. Thus basic depth
gaps appeared across three consecutive hourly campaigns, while the retained
stricter economic replay supports entry in two of them. No 24-hour recurrence,
daily opportunity count, geographic diversification or venue-wide maximum is
established. All passing pools were Miami hourly temperature markets.

The seven-pool peak occurred at 2026-09-24 04:02:46.610095 UTC, with 57.223 minutes
left. Each had $11 principal, $1.10 reserve and $16.52 conditional remaining reward.
Combined modeled rewards were $115.64. Deducting all $77 principal and $7.70
reserve left $30.94 conditional cushion. This is 40.18% of quote principal or
36.53% of principal plus reserve. It is not a measured investment return.

At the next hourly campaign's first alert, five pools coexisted with $55 principal,
$5.50 reserve, $81.80 conditional rewards and $21.30 cushion. A sixth pool alerted
later after one earlier gap ceased qualifying for that strategy, so six is the
distinct-pool count and five is the maximum simultaneous count. Four remained
passing at the last capture, but samples do not establish uninterrupted uptime.

## Same $5,000 model as AMS-012

The comparison uses the example declared before aggregation: $11 principal,
$1.10 fee reserve and $16.36 conditional reward per market-specific pool, with
about 57 minutes remaining. The stress removes the best opposite public level,
adds a rival quote one-fifth of target in size, assumes 50% future qualifying
time and tests consumption of the full 100-contract buffer. It keeps the older
capped scoring as an extra conservative stress; formal terms use whole-level
inclusion (see ../SOURCE_UPDATE_20260924.md).

A strict total $5,000 budget funds 413 such orders:

- Quote principal: $4,543.00.
- Chosen fee reserve: $454.30.
- Unallocated cash: $2.70.
- Conditional rewards if every order earns $16.36: $6,756.68.
- Net after losing all quote principal and consuming the entire reserve: $1,759.38.
- Return on the complete $5,000 account: 35.19% under these assumptions.

This needs **413 equivalent distinct pools concurrently**, compared with seven
observed: a 59-fold opportunity-count expansion. More size or more bots in those
same seven pools does not reproduce 413 separate reward budgets. This model is
not an expected return or a guaranteed lower bound: reward earnings and order
survival are unknown, and a full early fill can stop earnings.

As in AMS-012, failure here means an order earns zero rewards and loses all its
principal. The other orders earn $16.36 but also lose their principal. Every
order consumes its fee reserve. These percentage-weighted scenarios are not
estimated probabilities or execution outcomes; fractional order counts in the
JSON represent weights. Correlated failures do not require independence for this
arithmetic, but they could dominate realized results.

| Assumed zero-reward share | Rewards | Net after all principal and reserves | Return on $5,000 |
|---:|---:|---:|---:|
| 0% | $6,756.68 | $1,759.38 | 35.19% |
| 10% | $6,081.01 | $1,083.71 | 21.67% |
| 20% | $5,405.34 | $408.04 | 8.16% |
| 25% | $5,067.51 | $70.21 | 1.40% |
| 30% | $4,729.68 | -$267.62 | -5.35% |
| 50% | $3,378.34 | -$1,618.96 | -32.38% |
| 100% | $0 | -$4,997.30 | -99.95% |

Break-even is 26.039% zero-reward orders under those exact severity assumptions.
No actual failure rate has been measured. Unfilled canceled orders can avoid
principal losses, and public one-cent trades are not fills assigned to our orders.
The observation horizon does not establish a cash-reuse cycle; filled capital and
reward proceeds can become available on different schedules. No compounding.

If $5,000 means quote principal with fees funded separately, 454 $11 quotes use
$4,994 principal plus $499.40 reserve. Conditional rewards are $7,427.44 and
net is $1,934.04. The main table instead keeps the reserve inside $5,000.

## Comparison and evidence limits

The first strategy had $77 peak quote capacity against AMS-012's $5, approximately
15.4 times as much. Its declared full-capital conditional return is similar:
35.19% versus 34.91% for the smaller strategy. That similarity does not validate
either return; both rely on hypothetical qualifying time and a full-principal
deduction rather than actual execution. Larger missing-depth quotes expose more
principal per pool and do not have the same existing same-price depth ahead.

The reanalysis evaluated 752 previously admitted market observations. Of 182
observations with a baseline gap proposal, 107 passed the buffered test: 70 in
AMS-007 and 37 in AMS-010. Repeated observations are not independent opportunities.
All seven AMS-007 candidates passed ten sampled economic checks each; AMS-010's
original source reports the six candidates' varying persistence and compatible
public trades. A later new-entry failure does not measure the P&L of an earlier
hypothetical order. We made no loss-rate estimate.

The high-rate, at-most-two-hour admission gate is retained. AMS-010's START and
five-minute discovery rule are not applied retroactively to older data. This is
a harmonized, reused economic replay, not a prospective admission rerun. Original
captures and frozen reports are unchanged. The broader census's 811 depth gaps
and 91 loose ideal-budget candidates are not 811 or 91 viable examples of this
strict strategy.

## Verification and reproduction

The spec was published before aggregation. Four capital and concurrency tests
passed before source freeze 6b8e3604253e2f29e5b0c558d3de6eece29ff21d. All 303 input
hashes shared with AMS-012 match; the original FIRST_ALERTS artifact is an extra
hashed pointer. SUMMARY.json preserves passing response groups, first candidates,
event counts and all model arithmetic. INPUT_HASHES.json records every input read.

Restore raw AMS-005, 007, 009 and 010 evidence using the existing sibling
ARCHIVE.json pointers. Preserve imported source hashes in FREEZE.json. Run
`python3 -m unittest -v test_analyze` then `python3 analyze.py` in this directory.
The model uses no account credentials or order routes. No current financial risk
limits were set, no orders placed, and no background process remains running.

Primary source for scoring and payout mechanics:
https://www.cftc.gov/filings/orgrules/rules07152610358.pdf (clean pages 7–10).
