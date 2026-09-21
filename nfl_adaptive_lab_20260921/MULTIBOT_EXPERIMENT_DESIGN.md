# Multi-bot question: experimental design and capital-only controls

Added after the user's question during Q5 execution. This is separate from the
frozen three-candidate matrix. The three first q3300/.25 results were already
visible when these capital controls were specified. No multi-bot outcomes have
been computed, and these controls must not be represented as such.

## What can be checked now

Run the unchanged baseline router on all 31 development games with a shared
$1,000 account and a shared $4,000 account, at q3300 and .25-second submit/cancel
delay. Compare with the already-running $5,000 baseline. Keep desired order250,
eventcap250 and exitdepth250 constant. This isolates capitalization only.
It says nothing by itself about four independent accounts' total profits.

## Required fair multi-bot comparison

Compare one $4,000 account with four $1,000 accounts, and one $5,000 account with
five $1,000 accounts. Then compare identical bots with predeclared variants.
Keep the combined worst-case event exposure cap250 and combined total assumed
exit depth250 fixed in the first experiment. A second, clearly separate risk
experiment may raise the aggregate cap. Do not silently give every wallet its
own 250-event limit and claim a diversification benefit.

One common market simulator must own the public trade volume and external
queue. It must insert bot orders in price-time order, charge every hypothetical
fill against a shared available-volume budget, account for other bots' orders
ahead, and preserve cancel/resize latency. Distinct contracts/tickers may share
linked liquidity; venue market mapping must remain consistent with the baseline.
Never replay the full print independently into each wallet and sum the results.
Internal wallet transfers, collateral netting and opposite positions must not
be assumed unless supported by the actual account structure. Opposite holdings
in separate accounts do not automatically release pooled cash. Self-matching
and its prevention policy require explicit treatment. No synthetic self-trade
may manufacture economic profit.

For the tweaked-bot arm use the baseline, inventory, patience and allocation
policies already frozen in Q5, without post-result parameter tuning; a fifth bot
would need its role frozen before this new experiment. A portfolio allocator
cannot treat an independent $1k wallet as if it owns all $5k. Define coordination
and information-sharing explicitly. Compare independent vs a shared event risk
controller if testing coordination, and report that as a separate treatment.

Primary metric: aggregate completed net P&L after fees, at the same aggregate
capital, reservation cap and exit budget. Also report worst game loss, unresolved
inventory, net and gross cross-wallet exposure, cash fragmentation, missed fills,
queue churn, capital duration and correlation of per-game contributions.
Evaluate one named NFL event and the full cohort separately; selecting a game
based on past profitability would be exploratory. No individual game was named
in the user's question, so these capital-only controls retain the full cohort.

Hypothesis, not a result: identical bots offer no automatic extra edge. Different
rules help only if their contributions complement one another after competition
for fills, fees, duplicated exposure and separate-wallet capital constraints.
The exact shared-queue multi-wallet simulator is not part of Q5 or supplied as
validated code in this package.
