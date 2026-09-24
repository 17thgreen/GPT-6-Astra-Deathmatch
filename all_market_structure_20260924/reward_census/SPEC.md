# AMS-005: current reward census and executable-price filter

Motivation: AMS-004 found 32 depth gaps among 199 evaluable sampled markets. A
post-hoc screen revealed that empty-side quotes can cross the opposite 99-cent
bid at the minimum one-cent price. A large displayed reward is not attainable by
a resting order when no legal resting price exists. A full bounded census should
separate this mechanical issue from genuine quote candidates.

Before observing new outcomes: refresh up to two pages of active liquidity
programs (10000 per page). Apply AMS-004's positive reward/target, unpaid,
current-window and deterministic per-ticker deduplication. Fetch up to 6000 tickers
in lexical order. Report any catalog/market cap. First probe the public batch-book
endpoint using two repeated ticker query parameters. On schema/auth failure stop
the census and retain the error; do not perform thousands of fallback requests.
Otherwise fetch full books in batches of 50 with repeated ticker parameters and
metadata in batches of 50 with comma-joined parameters. Four concurrent requests,
12-second timeout, 300-second total soft budget checked before each group of four,
no retry or order placement. Keep every response and receipt timestamp.

For each open market within its listed window, classify both targets, one-sided
shortage, or both shortages; report missing/invalid data and outside-window cases.
For the subset with exactly one empty side and the opposite side meeting target:
verify a linear-cent grid; model a single target-sized bid at one cent only if
one cent plus the opposite best bid is strictly below one dollar. Equality crosses
and is excluded. Do not model partial fills while claiming an entirely resting
target. The idealized share is 50% only while our quote owns the qualifying empty
side, opposite depth stays sufficient, and no competitor/eligibility issue arises.

Rank those candidates by ideal half-pool dollars/hour divided by single-order
principal, then ticker. Record remaining gross budget capped at market close and
program end, time required to earn one full losing fill's principal, market rules,
and expected settlement time if provided. Prioritize candidates whose ideal
remaining gross exceeds one order's principal. All estimates omit unknown fees,
fills, account entitlement and changing competition; none is expected profit.

After the census, freeze up to 10 highest-ranked priority candidates before any
follow-up reads. Two additional metadata+full-book rounds, 30 seconds apart, within
120 seconds total, no replacements. This tests recurrence, not continuous uptime
or executed economics. Do not infer hypothetical fills from book disappearance.
No deployment, no real/demo orders, no credential use, no claim of earned rewards.

Stop conditions: batch route inaccessible, no eligible resting-price candidates,
or no candidates with sufficient ideal remaining budget. Preserve the negative
result and reconsider other mechanisms instead of relaxing admission gates.

Primary sources:
- https://help.kalshi.com/en/articles/13823851-liquidity-incentive-program
- https://docs.kalshi.com/api-reference/market/get-multiple-market-orderbooks
- https://docs.kalshi.com/api-reference/incentive-programs/get-incentives
