# AMS-010: prospective early-window reward scanner

Continue the short-window missing-depth reward mechanism only. Freeze the scanner
and admission policy before observing a new reward period. The AMS-009 38–42
minute illustration motivates an economic gate, not a hard-coded clock cutoff.

## Acquisition and admission

Freeze a START timestamp with this specification. Scheduled catalog cycles are
2026-09-24 04:56:00 through 05:10:00 UTC inclusive, at one-minute intervals. Skip
missed scheduled cycles explicitly rather than backfilling. Stop after that fixed
window; no extension seeking successful outcomes. Capture active liquidity
programs across every category, at most two pages of 10000. Four concurrent public
GETs, 12-second request timeout, no retries. No account or order endpoint.

Admit only current, unpaid, positive programs starting at or after START, lasting
at most two hours, with ideal half-pool hourly reward / (target*0.01) >= 1/hour.
For first admission the program age must be at most five minutes. Select at most
300 distinct tickers, ranking new programs by start, descending ratio, then ticker
and ID. Retain the first admitted program per ticker; track it until its period
ends. Write each selection before requesting books and market metadata. Retain
catalog failures, pagination/selection caps, disappearance and changed terms.

## Frozen scoring and rank

Import the verified AMS-009 reference/discount/target-capped scoring functions by
file hash. On cent-grid books, propose genuine one-cent bids completing deficient
sides only. Compare exact completion and an additional 10% of target on each
proposed side. Retain the whole-boundary-level interpretation as sensitivity;
it is not verified account scoring. Do not infer individual queue from price-level
aggregates. Reject proposals crossing public opposite orders or each other.

Primary stress: remove each best public opposite price level facing a proposed
side, once per book side; then add same-side rival size equal to one fifth of
target at two cents, or one cent if two cents would cross. If neither price can
rest, mark scenario unavailable. If either side lacks target after the change,
the snapshot qualifies for no reward. Both own proposals and rivals must be
mutually noncrossing. Existing crossed public books are refused.

Compute remaining gross reward at the conservative target-capped score and 50%
future qualifying time. Round down to cents and apply the published $1 minimum as
a conservative per-program candidate gate. Subtract full one-order-set purchase
principal and a chosen $1-per-1000-contract fee stress reserve. This is a
conditional budget cushion, not expected profit or credited income. Rank positive
candidates by cushion/principal, then ticker. The fee stress is not a venue quote.
Programs carrying max_reward_per_account are refused pending unit/scope handling;
absence of that optional field is not proof of account entitlement.

For each buffered plan also subtract the full added buffer from our hypothetical
remaining quantity and recompute the same stressed score; retain the original
principal and reserve. This is a declared fill sensitivity, not an inferred or
assigned execution. A primary buffered alert must pass both unconsumed and consumed
buffer scenarios. Record current opposite total depth and best-level size.

Preserve first-alert timing and proposed quantities. Later scans may produce fresh
candidate proposals but must not claim they maintained the original order. Report
first-alert age, time left, snapshot pass/fail counts and sampled span; never
integrate minute snapshots into earnings or continuous uptime. Group by event and
distinct reward pool; never sum repeated observations as profit.

At the end, fetch up to two public trade pages (1000 each) for the first 20 buffered
alert tickers in first-alert order. Classify direction/price and time relative to
first alert without awarding trades to our absent orders. No fitting a fill model
from the absence of trades. Report pagination and missing requests honestly.

## Checks and decision

Before acquisition test: target qualification, crossed book refusal, one-fifth
competitor size on target=300 and 1000, top-level removal, buffer-consumed scoring,
floor/minimum payouts, age admission, and loss of opposite depth. Verify frozen
hashes and receipt hashes; emit raw evidence and source restoration pointers.

Promote only the scanner mechanism if fresh-window buffered alerts occur under
these frozen gates. A missing new window is inconclusive. No actual order,
settlement, fill, account entitlement, payout or profitability validation is implied.

Primary sources:
https://help.kalshi.com/en/articles/13823851-liquidity-incentive-program
https://docs.kalshi.com/api-reference/incentive-programs/get-incentives
