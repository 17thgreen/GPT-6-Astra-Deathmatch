# AMS-007: a fresh hourly reward gap recurs

The bounded watch completed 12 cycles across 30 newly active programs in 10 series. Selection was based on reward duration, start time and rate before each book observation, across all categories. The 30-ticker selection cap was reached; no catalog pagination cap was reached. There were 320 market observations and 30 usable final trade pages, with no returned pagination cursors.

Seven fresh Miami 1am EDT temperature contracts met the original empty-side, opposite-depth, one-cent-resting and remaining-budget gates. Their $100 pools began at 04:02:16.975350 UTC and ended at 05:00 UTC. This is a different reward window from the midnight contracts discovered in AMS-005, but the same city and mechanism; it is not independent geographic or regime validation.

| Candidate | Strict passes / observations | Below-target observations | Snapshot span, minutes | Returned historical trades |
|---|---:|---:|---:|---:|
| KXTEMPMIAH-26SEP2401-T71.99 | 10/10 | 10 | 8.995 | 0 |
| KXTEMPMIAH-26SEP2401-T72.99 | 10/10 | 10 | 8.995 | 0 |
| KXTEMPMIAH-26SEP2401-T73.99 | 10/10 | 10 | 8.995 | 0 |
| KXTEMPMIAH-26SEP2401-T74.99 | 10/10 | 10 | 8.995 | 0 |
| KXTEMPMIAH-26SEP2401-T75.99 | 10/10 | 10 | 8.995 | 0 |
| KXTEMPMIAH-26SEP2401-T76.99 | 3/10 | 10 | 8.995 | 0 |
| KXTEMPMIAH-26SEP2401-T80.99 | 10/10 | 10 | 8.995 | 0 |

Six candidates passed all ten available observations across roughly nine minutes. A seventh passed the first three strict observations; a one-contract competing bid then made its side nonempty while leaving it 999 contracts below target. All seven remained below target in every observed snapshot. None of these seven returned any historical trades as of the final page reads. Nearby central strikes did trade, including one-cent prints, so the absence of trades must not be generalized to the entire weather family.

Each original hypothetical 1000-contract one-cent quote committed $10 principal. The ideal full-side reward rate was about $51.98/hour, with approximately $41.78 remaining for each of the six strict candidates at the last book read. That is a conditional budget at a past observation time, not current availability, earned money or an expected return. About 11.54 minutes at the ideal rate would match one full losing fill before fees; the nine-minute observation span did not even cover that duration.

## The small competing bid

The separately labelled post-hoc extension in SUMMARY.json shows why a single competing contract does not mechanically destroy this mechanism. With 1 existing contract, a 1000-contract target, a cent grid and the opposite book permitting a resting one-cent price, a 999-contract completing bid would set the one-fifth-target reference at one cent. All 1000 contracts would have full distance weight; our conditional side share would be 999/1000 and overall snapshot share 49.95%, for $9.99 principal. This extension was not added to the preregistered pass count and has no account-scoring validation.

## What has and has not been learned

Repeated, high-rate depth gaps have now been observed in two consecutive Miami hourly reward windows. The setup merits a targeted mechanics validation. Profit has not been established. Our own executable bid would create a better trading opportunity for others, so no-trade history from an empty side cannot estimate fills after insertion. Snapshots are not continuous uptime; changing competition, partial fills, account entitlement and actual credited rewards remain unresolved.

At exactly the target, even a partial fill can stop qualification unless other depth or a buffer keeps the total above target. Replenishment increases cumulative exposure. The seven strikes depend on one temperature observation and are correlated. The $100-per-market reward campaigns last less than an hour; multiplying the instantaneous rate across a day would be unsupported.

## Verification and evidence

66 HTTP 200 receipts. Four prospective-admission tests passed before acquisition. Frozen source/input hashes, all receipt body hashes and selection-before-book timestamps verified. The watch ended after 713.90 seconds with twelve completed cycles; it was not extended to seek a favorable result.

Specification/start commit 82debd0abd99436d9c08565798b632aff277eab7; acquisition/test freeze 2856308905ab0416907002c8034e52e47c5b07d8. Original metrics remain unchanged after observing the one-contract bid.

Raw catalogs, book/metadata receipts, trade pages, selections, frames and full results are in AMS_007_Raw_Evidence.zip. Code, summary, report and checksums remain in the repository. Restore the raw artifact into this experiment directory to rerun the report.

Primary scoring source: https://help.kalshi.com/en/articles/13823851-liquidity-incentive-program .

No credentials, live/demo orders, imputed fills, earned rewards or realized P&L. All bounded processes have ended.
