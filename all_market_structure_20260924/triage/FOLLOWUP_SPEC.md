# AMS-003 follow-up, frozen after first triage and before new observations

Coinbase returned non-JSON Site Unavailable pages for all nine requests; HTTP 200
was not a usable-data success. Preserve those failures. Give the independent spot
lane one alternative provider, then stop: Kraken public Depth, count=100, pairs
XBTUSD/ETHUSD/SOLUSD, two rounds with fresh matching Kalshi books and margin
metadata. Return keys XXBTZUSD/XETHZUSD/SOLUSD must be checked explicitly. Kraken
price-level timestamps are not whole-book freshness timestamps; do not use an old
unchanged resting level as proof that the entire book is stale. No timeliness or
execution admission without complete source-age evidence. Same quantity and fee
sensitivity as original spec. No retries or third provider.

New exploratory mechanism selected from the first observations: missing-side
liquidity reward activation. Only KXAAAGASDFL-26SEP24-4.4400 was missing a complete
side in the selected panel. Make two additional full-book and metadata reads, one
each round. No replacement if the gap disappears. No orders.

For this mechanism, evaluate a hypothetical genuine 1000-contract YES bid at
$0.01 only if the market remains open, the published period remains current,
the price is a permitted tick, the YES side remains empty, NO depth meets 1000,
and the order would rest without crossing the current best NO bid.
If our hypothetical order supplies the entire qualifying YES side, its idealized
snapshot share is one of two normalized side scores, i.e. 50%. Under unchanged
program rules and no competition/interruptions, the gross reward rate is half the
pool dollars/hour. Cap time by min(program end, market close) minus receipt.
Report $10 quote principal at risk if fully filled and losing, plus unspecified
fees. Compare the remaining ideal gross reward with that exposure. No payout or
fill probability is known; competition can eliminate the apparent opportunity.
This is not a risk-free-income claim or a trading instruction. Eligibility,
current program terms, exact scoring and executed risk still need validation.

Source: https://docs.kraken.com/api-reference/market-data/get-order-book and
https://help.kalshi.com/en/articles/13823851-liquidity-incentive-program.
