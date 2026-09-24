# Research decisions after AMS-003

## Allocation of research effort

| Mechanism | Decision | Evidence and next trigger |
|---|---|---|
| Static same-event threshold arbitrage | Park | AMS-002 found no positive gross floor margin among 180 depth-complete cases. Revisit on a new regime or a streaming signal; do not keep scanning the same quiet panel. |
| Volume subsidy as sole reason for a zero-edge taker trade | Reject the ordinary middle-price version | Standard M=1 unrounded taker fee exceeds the maximum public event-volume reward between about 7.74 and 92.26 cents. This is a cost bound, not a universal rejection of volume rewards. |
| Perpetual/spot entry basis | Data-blocked | Coinbase and Kraken returned HTML unavailable pages. No independent spot basis was measured; neither acceptance nor economic rejection is justified. Stop provider hopping in this environment. |
| Missing-side liquidity incentive | Advance to a focused prospective study | One selected program had an empty YES book in three observations. A hypothetical genuine order can change qualification and reward share. Dynamic competition, account eligibility, exact governing terms and adverse fills remain unmeasured. |
| Official-report interpretation | Retain as an independent candidate | Rules identify company-report hierarchy as a tractable information problem. CPI post-release taking is excluded for the tested contract because trading closes first. No observed corporate information edge yet. |
| Deadline nesting / exhaustive baskets | Backlog | Separate payoff proof and failure modes; do not stretch the prior threshold proof to cover them. |

## Why the incentive gap deserves a test

The selected Florida gas program offered a $100 pool across 4.15 hours with a
1,000-contract target. Its observed YES book was empty, while NO depth exceeded
the target. That prevents the displayed snapshot from meeting the public program's
two-sided condition. A legitimate YES bid could change that condition.

For a single unreplenished 1,000-contract YES order at 1 cent, principal exposure
would be $10 if fully filled and losing, plus any applicable fees. The observed
NO bids did not make that price marketable, and it matched the permitted tick.
If it became the entire qualifying YES side, with the other side qualifying and
no competition, the published normalization suggests a 50% snapshot share. This
is an idealized model, not a verified reward quote or an instruction to trade.

That model gives $12.0482/hour, approximately $7.37 of remaining gross reward at
the last follow-up, and 49.8 minutes to match $10 of principal loss. Only about
36.7 minutes remained. Thus even the ideal remaining reward does not cover a full
losing fill. Earlier arrival, lower adverse-fill exposure or a different program
could change the economics; none is proven here. Replenishing after fills would
increase total exposure beyond this one-order bound.

The observation appeared three times across about 217 seconds; REST observations
do not prove an uninterrupted gap. We placed no order, earned no reward, and have
no measured share, fill rate, realized loss or net return.

## Next study design, before committing risk

Screen programs for missing or under-target sides, valid ticks, time remaining and
reward dollars per unit of quoted principal. Include all cases and failures, not
only high headline yields. Separate fresh governing terms from cached schedules.
Use only genuine executable orders in any later authorized trading test; no
self-trading, coordination or orders intended to mislead other participants.

The next research measurement should first replay virtual quotes against a full
receipt stream. Recompute the reference and qualifying depth after hypothetical
insertion; compare shares under competing entries and boundary allocation rules.
Explicitly debit fills, fees, inventory marks, loss on losing outcomes, missed
reward seconds, cancellation delay and competition. No disappearance-as-fill rule.
Model re-quoting as new exposure, not free restoration of lost size. Validate scoring
and account entitlement before treating a simulated share as expected payment.

Stop or deprioritize the lane if actual qualification cannot be established, if
competing quotes rapidly erase the budget, or if conservative inventory losses
consume the rewards. A positive static share estimate alone is not promotion.

## Scope of discretion

These decisions concern research allocation. Existing financial-risk limits and
the prohibition on live orders under a research task remain in force. No strategy
has earned deployment. No background service is running.
