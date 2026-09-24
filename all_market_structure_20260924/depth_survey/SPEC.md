# AMS-004: bounded prospective liquidity-depth survey

Question: how often is the two-sided target requirement missing among currently
listed liquidity-reward markets? This is a descriptive screen, not a profit test.

Before observing books, fetch up to two pages of active liquidity incentives,
limit 10000 each. Retain raw receipts and report any cursor left at the cap.
Filter positive reward and target, unpaid, listed period containing catalog
receipt; deduplicate by market ticker, retaining the lexicographically smallest
program ID when overlapping programs exist. This gives one requirement per market,
not necessarily every overlapping program requirement.

Select up to 200 unique markets by ascending SHA256 of
`AMS-004-20260924|` plus ticker. Preserve the catalog and fixed selection before
book acquisition. No selection using depth, prices or outcomes. One snapshot per
market; no replacements for failures. Fetch metadata and books in batches of 50.
If public batch books fail or omit members, use one individual depth=0 GET for
each affected ticker. Batch metadata may similarly fall back to individual GETs.
At most four concurrent requests, 12-second timeout, no retries, 240-second total
acquisition budget; retain incomplete cases explicitly. No credentials or orders.

Classify current open markets during their listed reward period as: both sides
meet target; YES short only; NO short only; both short. Also count empty sides and
missing/invalid data separately. Sum full resting quantities, not just top quotes.
Do not equate a missing side with an executable profitable quote. Do not extrapolate
to all Kalshi markets or all times, and disclose catalog truncation, timestamp skew,
selection, metadata uncertainty and program/account eligibility uncertainty.

Report candidate identifiers and shortages. Reward dollars = period_reward/10000
(centi-cents); do not assume all pool money belongs to our account. A future
persistence and adverse-fill study would be required before any deployment.

Sources:
- https://docs.kalshi.com/api-reference/incentive-programs/get-incentives
- https://docs.kalshi.com/api-reference/market/get-multiple-market-orderbooks
- https://help.kalshi.com/en/articles/13823851-liquidity-incentive-program
