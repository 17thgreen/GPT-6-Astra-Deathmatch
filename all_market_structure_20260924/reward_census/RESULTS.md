# AMS-005: reward-depth census and recurrence

Observation window: 2026-09-24T03:41:46.073090+00:00 through 2026-09-24T03:48:40.623625+00:00.

Catalog entries 5450; distinct eligible listed tickers 5444; requested 5444. Catalog cursor remaining: False; market cap applied: False.

Evaluable open/current-window markets: 5432; gaps on one or both sides: 811 (14.9% of evaluable markets). A single snapshot is not a duration estimate.

| Classification | Count |
|---|---:|
| both_meet | 4621 |
| both_short | 27 |
| no_short | 322 |
| outside_open_window | 12 |
| yes_short | 462 |

Exactly one empty side while the other meets target: 705. A one-cent bid could rest in 390. Of these, 91 had ideal remaining half-pool rewards exceeding one unreplenished order's principal. These are candidates, not profitable-trade findings.

| Priority candidate | Ideal $/hour | Principal | Ideal remaining $ | Hours to cover one full losing fill | Follow-up passes |
|---|---:|---:|---:|---:|---:|
| KXTEMPMIAH-26SEP2400-T75.99 | 51.938 | 10.00 | 12.76 | 0.19 | 2/2 |
| KXTEMPMIAH-26SEP2400-T76.99 | 51.938 | 10.00 | 12.76 | 0.19 | 2/2 |
| KXTEMPMIAH-26SEP2400-T80.99 | 51.938 | 10.00 | 12.76 | 0.19 | 2/2 |
| KXTEMPMIAH-26SEP2400-T81.99 | 51.938 | 10.00 | 12.76 | 0.19 | 2/2 |
| KXTEMPMIAH-26SEP2400-T82.99 | 51.938 | 10.00 | 12.76 | 0.19 | 1/2 |
| KXTEMPMIAH-26SEP2400-T83.99 | 51.938 | 10.00 | 12.76 | 0.19 | 1/2 |
| KXTEMPMIAH-26SEP2400-T84.99 | 51.938 | 10.00 | 12.76 | 0.19 | 1/2 |
| KXTRUEV-26SEP24-T1324.21 | 1.113 | 10.00 | 26.97 | 8.98 | 2/2 |
| KXTRUEV-26SEP24-T1314.21 | 1.113 | 10.00 | 26.97 | 8.98 | 2/2 |
| KXTRUEV-26SEP24-T1194.21 | 1.113 | 10.00 | 26.97 | 8.98 | 2/2 |

## Recurrence and concentration

All ten shortlisted candidates retained the empty-side, opposite-target and non-crossing one-cent conditions in both follow-up rounds. Seventeen of twenty follow-up observations still passed the remaining-gross-versus-principal screen. The three failures were Miami contracts whose ideal remaining budget fell below $10 as the clock ran down; their book gaps persisted.

Seven Miami hourly-temperature strikes dominate the nominal hourly budget: each showed an ideal $51.94/hour and a $10 one-order principal, requiring about 11.55 minutes to earn that principal before fees. They share one underlying weather event and are correlated. Their $100 pools ran from 03:02:14 UTC to 04:00 UTC, less than an hour; the rate is not durable hourly income. The source specifies Synoptic Data and the Kalshi Weather Index Methodology; other weather reports cannot establish settlement.

At the last metadata reads, five of these weather markets showed zero lifetime volume and two showed one contract each. That is evidence of little prior trading, not evidence that our new executable bids would avoid fills. Two slower Truflation candidates instead showed 1000 contracts of volume and last prices of one cent; a subsequent tape study is needed to establish timestamps and taker direction before interpreting them.

The API OpenAPI schema explicitly describes period_reward as centi-cents, confirming division by 10000 for dollars (https://docs.kalshi.com/openapi.yaml).

## Economics and decisive limitations

The 50% reward share is an idealized consequence of owning all qualifying liquidity on one side, while the opposite side qualifies. It is not an account payout quote. Competition, price changes, account eligibility, governing terms and reward changes can reduce it. Reward for excluded time before arrival cannot be recovered.

At exactly the target size, even one contract filled can put our side below target and stop qualification until depth is restored. Increasing the quote to buffer fills commits more capital without increasing the ideal 50% share. Replenishment accumulates inventory risk: the $10 example bounds only one unreplenished 1000-contract order at one cent.

CANDIDATES.json gives conditional break-even losing-fill flow at 100%, 50%, and 25% retention of the ideal reward, with maker fee multipliers 0, 1 and 2. The maker fee sensitivity uses the published unrounded formula 0.0175*M*p*(1-p); per-trade rounding and account-specific terms can worsen it. These are loss budgets, not measured fill rates or expected returns. The model assumes the full reward rate continues, so lost qualifying seconds require an additional reduction.

Two short follow-up rounds test whether the gap recurs. They cannot show continuous availability, response to our inserted order, actual fills, actual reward credits, or stability over the many hours often needed to offset a losing fill. No public passive observation proves those counterfactual execution outcomes.

No live or demo orders were placed, no credential was used, and no profit was realized. The strategy has not earned deployment or a cash-cow label.

## Verification and provenance

HTTP statuses: {'200': 260}. Census elapsed 280.26 seconds. Three focused entry tests passed before acquisition. All receipt body hashes, source freezes, both panel hashes and census row reconstruction passed after acquisition.

Specification commit: c6e99c8090d977ff1665949443ddab2159a4b765. Source/test freeze: 48a635f10505bb94141fef503ed17e39ddb30a2c. Follow-up selection was saved and committed before its observations.

Large raw receipts are preserved in the separate AMS_005_Raw_Evidence.zip artifact; EVIDENCE_HASHES.json verifies its individual members. Code and reports remain in the repository. An index is not a substitute for the raw bytes.

Sources:
- https://help.kalshi.com/en/articles/13823851-liquidity-incentive-program
- https://kalshi.com/docs/kalshi-fee-schedule.pdf
- https://docs.kalshi.com/api-reference/market/get-multiple-market-orderbooks
- https://docs.kalshi.com/api-reference/incentive-programs/get-incentives

All bounded acquisition processes have ended.
