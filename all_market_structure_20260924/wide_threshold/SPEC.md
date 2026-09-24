# AMS-008: one broad threshold screen on the retained census

This revisits the parked AMS-002 static-threshold lane once because AMS-005 captured
5444 rewarded markets rather than 24 selected contracts. It uses already collected
development data, some previously inspected for rewards; it is not a new holdout.
Freeze this specification and source before calculating pair outcomes. No network
calls in this stage. A positive screen would require a separately frozen fresh
quote/rule check; asynchronous historical snapshots are not executable profit.

Only use AMS-005 rows observed open/current-window with usable full books and
metadata. Require binary markets, cap_strike absent, finite floor_strike, and
strike_type greater or greater_or_equal. Form pairs within the same event, exact
strike type, close_time and expiration_time. Normalize each contract's own numeric
strike in primary and secondary rules, preserving other words/numbers. Require
equal templates and evidence the strike was replaced in primary rules. Exclude
explicit fair-value settlement language. This conservative matching can miss
valid pairs; positive pairs still require manual settlement-proof review.

For lower threshold a and upper b>a, buying YES(a) and NO(b) pays at least $1 under
ordinary common-source binary resolution. Walk actual opposite bids to buy both
legs for quantities 1, 10 and 100. No last-price or best-quote-only fills. Report
missing depth, gross floor minus cost, and an ordinary M=1 unrounded taker-fee
sensitivity, summed across consumed levels. This fee is a benchmark, not confirmed
account/series fees. Negative gross margin already fails before fees. Retain
receipt skew; even zero receipt skew is not synchronized exchange execution.

Preserve all pair/size outcomes and the ten best depth-complete margins. No
counterfactual orders, settlement imputation, realized P&L or reranking of existing
strategies. Stop after this single pass if no positive gross candidate appears.

Sources: Kalshi binary order-book API and July 7, 2026 fee schedule cited in AMS-005.
