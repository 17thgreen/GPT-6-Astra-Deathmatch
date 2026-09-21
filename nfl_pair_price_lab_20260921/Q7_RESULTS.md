# Q7 chosen-pair price study

Same 31 repeatedly examined games, two weeks and one shared $5,000 account per alternative. All returns below are completed hypothetical historical net after modeled fees. Zero fresh validation games.

| Architecture / guard | Queue 3,300; .25s | Queue 3,300; 5s | Queue 10,000; .25s | Queue 10,000; 5s |
|---|---:|---:|---:|---:|
| router_off | $+201.52 | $+198.41 | $+10.35 | $+0.32 |
| router_on | $+354.33 | $+353.89 | $+90.45 | $+79.08 |
| allocator_off | $+205.94 | $+203.26 | $+14.29 | $+6.69 |
| allocator_on | $+345.24 | $+345.42 | $+75.90 | $+69.06 |

## Within-simulator contrasts

| Scenario | Guard effect, router | Guard effect, allocator | Interaction |
|---|---:|---:|---:|
| q3300_d0.25 | $+152.81 | $+139.30 | $-13.51 |
| q3300_d5 | $+155.49 | $+142.16 | $-13.33 |
| q10000_d0.25 | $+80.09 | $+61.61 | $-18.48 |
| q10000_d5 | $+78.75 | $+62.37 | $-16.38 |

The interaction is allocator guard effect minus router guard effect. The guard uses existing refresh timing in the router and existing ten-minute budget timing in the allocator. These are policy effects within the same simulator, not live causal-effect estimates.

## Predeclared selection

Selected simpler router: **router_on**. Retained shadow research candidate: **router_on**.
Failed criteria: none.
The 95% retention test is an engineering tolerance, not statistical noninferiority or live promotion.

## Primary scenario diagnostics

| Arm | Week 1 | Week 2 | Without best two | Inventory contract-hours | Taker contracts | Residual |
|---|---:|---:|---:|---:|---:|---:|
| router_off | $+154.07 | $+47.46 | $+31.46 | 667,959 | 2,477.87 | 0.00 |
| router_on | $+219.57 | $+134.76 | $+184.28 | 627,760 | 2,063.70 | 0.00 |
| allocator_off | $+160.70 | $+45.24 | $+41.44 | 645,660 | 2,482.83 | 0.00 |
| allocator_on | $+215.70 | $+129.54 | $+180.75 | 603,263 | 2,068.66 | 0.00 |

Inventory contract-hours are not monetary drawdown. Residual inventory is excluded from completed profit.

## Five-minute adverse movement diagnostics

| Arm, primary scenario | Contract coverage | Midpoint change, cents | Entry-fee-adjusted midpoint markout, cents | Adverse fraction |
|---|---:|---:|---:|---:|
| router_off | 92.46% | -0.00988 | 0.10237 | 1.20% |
| router_on | 92.30% | -0.00638 | 0.10486 | 0.95% |
| allocator_off | 92.63% | -0.00846 | 0.10367 | 1.13% |
| allocator_on | 92.38% | -0.00643 | 0.10495 | 0.95% |

Marks use only quotes received by fill+300 seconds, with post-fill asof time and at most 120 seconds of age. Missing quotes remain missing. These are midpoint diagnostics, not executable exit prices; they omit exit fees. Different policies select different fill populations.

## Verification and limits

All sixteen financial ledgers reconcile independently, including fixed-point fees, paired payouts, cash, positions, deadlines, quantities, exit capacity and week contributions. All eight unchanged Q6 controls match exact uncompressed fill/order hashes and financial aggregates. Source/input hashes are frozen and checked; new guard decisions were independently inspected. See results/verification.json and results/unit_tests.txt.

Historical queue position, cancellation allocation, publication and order latency, fee history, collateral/netting, market response and executable exit liquidity remain assumptions. No live orders, fresh holdout completion or continuous recorder deployment occurred. The prior full-window reservation begins 2026-09-22T00:15Z and cannot be backdated.
