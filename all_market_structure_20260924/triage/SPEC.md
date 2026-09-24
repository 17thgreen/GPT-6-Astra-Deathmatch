# AMS-003: compare mechanisms, do not extend a failed screen indefinitely

AMS-002 static same-event threshold arbitrage is parked on current evidence.
That is not a universal disproof. This new bounded study examines independent
economics; public GET only, no credentials, no orders, no account changes.

## A. Perpetual/spot entry basis
Fixed universe BTC, ETH, SOL, chosen for straightforward underlying units and
independent Coinbase USD spot books, not for observed basis. Three rounds. Each
round requests current Kalshi margin metadata, three Kalshi depth-100 books and
three Coinbase level-2 books. Maximum four concurrent requests, 12-second timeout,
no retry. Kalshi uses the documented legacy host that worked in prior studies.
Save each receipt immediately including raw bytes, hashes, wall and monotonic clocks.

Use current contract_size * underlying_multiplier to match spot units for 10 Kalshi
contracts. Walk bids/asks on both venues, refuse partial depth, nonfinite/negative
values, auction-mode spot books, inactive perps, or unverified instrument mapping.
Measure short-perp/buy-spot and buy-perp/sell-spot entry basis per unit and in bps.
The latter requires inventory/borrow not established here. These are entry-basis
observations, NOT realized arbitrage; no common expiry, no convergence guarantee.
Fees, unwind spread, funding and borrow all consume the basis. Report combined
entry-fee sensitivity 0/5/10/25/50 bps, explicitly assumptions, not account fees.
Do not apply the event-contract quadratic fee formula to perps or spot.

Report pair receipt skew, RTT and available source timestamp ages. Source times
more than 10 seconds old or more than 1 second ahead of local receipt invalidate
timeliness admission. A book without a source timestamp has unverified age.
No stream means no latency ranking, lead/lag proof or quote-survival claim.
If no positive timely entry basis exists even before fees, deprioritize immediate
taker-basis trading in this sample; funding-carry remains separately untested.

## B. Public liquidity-program economics
Using AMS-001's retained, capped program sample, select the highest dollars/hour
program whose listed period contains the recorded selection time in each primary
category; ties by market ticker then program ID. Selection
uses no books or returns. This is a deliberately enriched candidate sample, not
representative. Do not infer no other programs exist. Retain full selected records.
Get each market's current metadata and full book (depth=0), once. No replacements.
Check open status and whether the listed program period contains the book receipt.
Program terms may have changed since AMS-001: fresh program/account entitlement is
unverified, so all reward calculations are conditional on the retained schedule.

Check whether both YES and NO bid sides meet the target size. Compute the reference
price where cumulative quantity first reaches one fifth of target. Report side
depth and any target deficit, not our scoring share or future fill probabilities.
No exact individual reward score: aggregated books omit order-level boundary and
ownership information. State 1%, 5%, 10% share dollar/hour scenarios with 100%
qualifying time, plus 50% qualifying-time sensitivity. These are loss budgets before
fees/adverse selection, not expected earnings. Do not sum overlapping pools, treat
our quoted orders as riskless, or assume competition stays fixed.

## C. Event volume-reward upper bound
For the ordinary 0.07*p*(1-p) taker fee (multiplier 1), compare with the public
program's maximum $0.005 reward per eligible contract. Compute prices at which the
unrounded fee alone exceeds the maximum reward; include zero spread/slippage as an
optimistic bound. No claim of account eligibility, actual payment, fixed-rate rebates,
special negotiated maker terms, or applicability of this formula to perps. This tests
whether reward alone could justify an otherwise zero-edge genuine trade, not a
proposal to manufacture volume. Gross reward must exceed fees AND trading losses.

## Decision
After these bounded observations, rank which hypothesis earns further measurement.
No lane is promoted without net execution evidence. Preserve failed requests and
negative results. No background process or paid service is started. Official-source
interpretation remains a separate candidate; do not force it to explain these data.
