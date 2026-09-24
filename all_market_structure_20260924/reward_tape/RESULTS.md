# AMS-006: cheap quotes do get hit

The public tape confirms three Truflation candidates had full target-sized one-cent executions during their reward periods, with taker direction compatible with selling into the proposed cheap bid. The seven Miami weather candidates had no returned trades within their reward period as of acquisition. Neither finding establishes what would happen after our own quote changes the book.

| Market | Contracts returned | Within program | Direction/price compatible within program | Pagination complete |
|---|---:|---:|---:|---|
| KXTEMPMIAH-26SEP2400-T75.99 | 0 | 0 | 0 | True |
| KXTEMPMIAH-26SEP2400-T76.99 | 0 | 0 | 0 | True |
| KXTEMPMIAH-26SEP2400-T80.99 | 1.00 | 0 | 0 | True |
| KXTEMPMIAH-26SEP2400-T81.99 | 1.00 | 0 | 0 | True |
| KXTEMPMIAH-26SEP2400-T82.99 | 0 | 0 | 0 | True |
| KXTEMPMIAH-26SEP2400-T83.99 | 0 | 0 | 0 | True |
| KXTEMPMIAH-26SEP2400-T84.99 | 0 | 0 | 0 | True |
| KXTRUEV-26SEP24-T1324.21 | 1000.00 | 1000.00 | 1000.00 | True |
| KXTRUEV-26SEP24-T1314.21 | 1000.00 | 1000.00 | 1000.00 | True |
| KXTRUEV-26SEP24-T1194.21 | 1014.00 | 1014.00 | 1014.00 | True |

## Timing matters

| Compatible print | Time after reward start, minutes | Contract count | Ideal half-pool accrual since program start, dollars |
|---|---:|---:|---:|
| KXTRUEV-26SEP24-T1324.21 at 2026-09-24T01:04:59.182508Z | 2.701 | 1000.00 | 0.05012 |
| KXTRUEV-26SEP24-T1314.21 at 2026-09-24T01:05:06.428552Z | 2.822 | 1000.00 | 0.05237 |
| KXTRUEV-26SEP24-T1194.21 at 2026-09-24T01:04:52.172997Z | 2.584 | 1000.00 | 0.04796 |
| KXTRUEV-26SEP24-T1194.21 at 2026-09-24T01:04:52.172997Z | 2.584 | 14.00 | 0.04796 |

Each Truflation market had a 1000-contract print about 2.6–2.8 minutes after its program began. That corresponds to $10 of one-cent purchase principal, while an ideal half-pool quote could have accrued only approximately five cents since program start. One market also had a 14-contract print at the same timestamp. This is substantial evidence against assuming that cheap orders will reliably sit untouched for the roughly nine hours needed to earn back a full losing fill in these programs.

We do not know participant identity, entry time, strategy, queue rank, reward credits, terminal outcome or realized P&L. The observed contracts might later win. The calculation is a conditional reward-versus-principal comparison, not a claim that a named maker lost money, that wash trading occurred, or that our own order would receive the same fills.

For Miami, five markets returned zero historical prints; two returned one contract each at a YES price of five cents around 03:00 UTC, before the 03:02:14 UTC reward start. No reward-period trades appeared as of these requests. This supports examining the short, high-rate weather programs separately from the slower Truflation programs. It cannot demonstrate safety after adding a new bid.

## Decision

Deprioritize these three Truflation markets for a subsidy-only strategy without a separate fair-value edge. Advance the high-rate, short-window hypothesis to a fresh-window replication across any newly active reward markets meeting the same rate and duration gates. Do not restrict that search to Miami or to weather. No strategy is admitted for trading.

## Verification

Ten public HTTP 200 receipts, ten complete returned pagination sequences, four direction/block/legacy tests passed before acquisition. Frozen files and raw-body hashes verified. Acquisition took 16.41 seconds. No credentials, orders, imputed fills or P&L.

Spec commit a59c9e331dcfcd71c957e753bc4fd2460df403c0; acquisition/test freeze 6c5c059043bd8c569711c607c56ae44a8ae6cf82.

Sources: https://docs.kalshi.com/api-reference/market/get-trades and https://docs.kalshi.com/openapi.yaml. The schema defines taker_outcome_side as directional exposure; taker_book_side is the equivalent bid/ask vocabulary. Block trades are excluded from order-book compatibility. Returned legacy and new direction fields agreed in observed prints.

All acquisition processes ended.
