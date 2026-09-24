# AMS-002: nested-threshold executable-cost discovery

Public GET research; no orders or credentials. This is a new screen, not a replay
of AMS-001. Outcomes are descriptive asynchronous quote observations, never fills.

Before new metadata observations, select the most represented series in each of
the 12 primary categories in AMS-001's capped incentive sample (ties lexical).
Add a mechanism-directed supplement: KXCPIYOY, KXAAAGASDFL, KXBTCPRICE,
KXBIGGESTQUAKE, KXAPSMM, KXMLBPLAYOFFHOST, KXEURUSD. Deduplicate. This is a
development sample selected for coverage and interpretable thresholds, not a
random sample or an incentive census. No choice uses market price or returns.

Fetch one open-market page per series, limit 1000, on the documented legacy
production API that worked in AMS-001. Retain cursors, errors and receipt times;
no implied completeness. Read selected series fee metadata and contract terms.
Maximum four concurrent requests, 12-second request timeout; no retries.

Group by event_ticker, strike_type, close_time and expiration_time. Only strictly
nested greater/greater_or_equal floor-strike ladders or less/less_or_equal
cap-strike ladders qualify for rules review. Do not mix comparator types. Exclude
range baskets, incomparable underlyings, missing strikes and ambiguous rules.
Within each series choose earliest close then lexical event with at least two
distinct strikes; first four strikes in numeric order. Freeze the exact admission
manifest and human rule review before fetching any books. At most six series,
selected lexically among rule-approved groups. Record rejected cases and reasons.

Read the contract rules and cancellation/exception provisions. A normal-resolution
implication is not an unconditional guarantee if exceptional treatment remains
unresolved. In that case retain the group as conditional screen only, never label
it riskless. For A implies B, buy YES B and NO A; $1 is the normal-resolution
payoff floor. The reverse pair does not have that floor.

Fetch depth 100 books for admitted markets twice (two sequential rounds; up to four
parallel requests within a round). Evaluate all strike pairs at 1, 10 and 100
contracts. Walk full available depth using Decimal arithmetic. Both legs must have
complete quantity or score missing. Missing sides do not become zero-cost fills.
Each pair is a standalone opportunity screen; scores cannot be summed across
pairs sharing liquidity. Report book receipt-time skew, gross floor-minus-cost,
raw quadratic taker fee with observed series multiplier, and conservative per-level
cent rounding sensitivity. No rebate. Costs include both entry legs; holding to
normal settlement, so no assumed exit. Missing fee types block fee-adjusted scores.

General fee source: https://kalshi.com/docs/kalshi-fee-schedule.pdf, effective
July 7 2026 when retrieved. Formula uses 0.07*M*C*P*(1-P); text describes centicent
rounding of fee+cost while its illustrative table shows cent rounding. Report raw
unrounded cost as an optimistic fee lower bound and round fee per consumed level
up to a cent as sensitivity. Neither is claimed to match unknown fill fragmentation
or account-specific FCM charges. A positive optimistic result is only a candidate;
a nonpositive zero-fee result already fails this gross screen.

No production WS key or independent lead feed is supplied. Sequential REST data
cannot establish simultaneous executability, quote lifetime, latency edge or P&L.
Stop after the two rounds and report every pair/size result and exclusion. If no
groups qualify, retain that negative result without substituting a winning group.
