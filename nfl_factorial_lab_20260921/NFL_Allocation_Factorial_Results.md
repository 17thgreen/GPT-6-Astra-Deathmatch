# NFL allocation mechanism study Q6

September 21, 2026. The predeclared rule selects **000**, retaining **none of the three optional factors**, for further shadow research.

This study separates three optional features of the Q5 allocator: a two-sided
observed-flow admission gate (F), cash earmarking for inventory offsets (P), and
cross-game opportunity ranking with incumbent preference (R). It evaluates all
eight on/off combinations, plus the original router, under four queue/latency
scenarios: **36 runs of the same 31 previously examined games, two weeks and one
shared $5,000 account per alternative**. None is an independently validated live
strategy. Zero fresh holdout games have completed in this study.

The selected primary case earns **+$345.24**, versus
+$201.52 for the original router and
+$342.76 for the full 111 policy. Its week
contributions are +$215.70 and
+$129.54. Removing its two best games leaves
+$180.75. Unhedged contract-hours are
603,263, versus 667,959
for the original router; taker closing volume is 2,068.66
contracts. Peak order reservations are $3,964.35.
These inventory metrics are not monetary drawdown or maximum-loss estimates.

## Results of all eight combinations

| F/P/R | Extra flow gate | Offset cash earmark | Portfolio ranking | Queue 3,300; .25s | Queue 3,300; 5s | Queue 10,000; .25s | Queue 10,000; 5s |
|---|---|---|---|---:|---:|---:|---:|
| baseline | — | — | — | +$201.52 | +$198.41 | +$10.35 | +$0.32 |
| 000 | Off | Off | Off | +$345.24 | +$345.42 | +$75.90 | +$69.06 |
| 001 | Off | Off | On | +$345.24 | +$345.42 | +$75.90 | +$69.06 |
| 010 | Off | On | Off | +$327.52 | +$331.63 | +$78.37 | +$71.61 |
| 011 | Off | On | On | +$343.03 | +$341.83 | +$67.55 | +$62.43 |
| 100 | On | Off | Off | +$345.96 | +$346.14 | +$75.90 | +$69.06 |
| 101 | On | Off | On | +$345.96 | +$346.14 | +$75.90 | +$69.06 |
| 110 | On | On | Off | +$328.35 | +$333.46 | +$78.52 | +$71.75 |
| 111 | On | On | On | +$342.76 | +$340.99 | +$67.55 | +$62.43 |

The delay shown applies to both order submission and cancellation. Early queue
assumptions are 3,300 or 10,000; the last 12h queue remains 1,327,847.005. Desired
order size, hard event exposure/reservation cap, and total assumed exit depth
remain 250. Entries run from T−7d to T−3h, with five-minute final winddown.
All cases use the same historical quotes, trades, fees and account precision.
No multi-bot competition or independent-wallet multiplication is simulated.

## The control that prevents a misleading conclusion

**000 is not the original router.** It still uses ten-minute event-budget
updates, proportional quote sizing, a pair-margin cushion, the inherited
within-game route selection and the common inventory-offset quantity floor.
Actual cash, pending-order reservations, event limits and cancellation delays
remain enforced. Turning P off removes only the additional cash earmark;
turning F off does not remove all uses of flow from the inherited router.

At the primary assumption, 000 earns +$345.24,
compared with +$201.52 for the original router.
That difference, +$143.72, belongs to the
**common allocator machinery as a bundle**, not automatically to F, P or R.
The three optional factors jointly change 000 into 111 by
−$2.48.

A retrospective read of the primary 000 decision log finds
21 budget updates with a funding
shortfall out of 2558 updates. This diagnostic
counts requested target budgets, not executable fills or actual idle capital.
The full 111 policy has funding shortfalls in
736 of its
2558 updates. Its additional earmark thus
changes which targets can be funded even while all arms retain the same actual
cash-reservation safeguards; the contrast tables measure the resulting policy
outcomes, not a universal benefit or cost of protecting cash.

A separate post-result synthetic probe identifies a concrete possible mechanism:
the original router scores a route against the cheapest possible opposite leg,
but can select two more expensive routes whose combined cost exceeds the paired
payout. In the probe it selects a pair costing $1.10 per $1 payout. The common
allocator rejects that chosen pair. This illustrates the added joint-margin
check; it does not measure how much historical P&L it caused. The probe source
and result are included, and no new strategy or threshold was added to the matrix.
The common allocator also changes timing and sizing, so its mechanisms remain
bundled. A follow-up isolated joint-margin-gate test would distinguish them.

## Which components account for the difference?

The following allocation of effects averages each component's contribution over
all six orders in which the three factors could be added (Shapley attribution).
The three factor contributions sum to 111−000; adding the common-machinery
residual reproduces 111−original. It is an exact accounting of these model runs,
not a live causal-effect estimate. Interactions are shared across their members.

| Contribution to 111 minus original router | Queue 3,300; .25s | Queue 3,300; 5s | Queue 10,000; .25s | Queue 10,000; 5s |
|---|---:|---:|---:|---:|
| Common allocator machinery | +$143.72 | +$147.01 | +$65.55 | +$68.73 |
| Additional flow gate | +$0.41 | +$0.38 | +$0.02 | +$0.02 |
| Cash earmark | −$10.28 | −$9.02 | −$2.92 | −$2.02 |
| Portfolio ranking | +$7.39 | +$4.21 | −$5.46 | −$4.64 |
| Total improvement | +$141.24 | +$142.58 | +$57.19 | +$62.10 |

A second view averages each component's on-minus-off contrast over all four
settings of the other two components. These main effects need not sum to the
full improvement when interactions exist.

| Component | Mean on-minus-off, primary scenario | Range across four primary contrasts | Positive contrasts across all 16 contexts |
|---|---:|---:|---:|
| Extra flow gate | +$0.50 | −$0.27 to +$0.82 | 10 / 16 |
| Cash earmark | −$10.19 | −$17.72 to −$2.22 | 4 / 16 |
| Portfolio ranking | +$7.48 | +$0.00 to +$15.51 | 4 / 16 |

Primary pairwise interactions (averaged over the remaining factor) are:
flow×protection −$0.44,
flow×ranking −$0.55, and
protection×ranking +$14.96.
The three-way interaction is −$1.09.
All conditional contrasts and all four scenario decompositions are retained in
results/factor_effects.json. A sign change across settings means a feature's
value depends on the rest of the policy; it should not be called universally
helpful or harmful from one result.

## Selection was fixed before results

To qualify, an arm must finish flat and positive, beat the original router at
all four queue/latency settings, improve both primary week contributions, remain
positive without its best two primary games, and keep inventory contract-hours
within 1.25× the original router in every scenario. It must also retain at least
95% of 111 P&L in every scenario. Then select the fewest enabled factors; ties
use the highest worst-scenario retention ratio, then ascending bit label.

The 95% threshold is an engineering tolerance, not a statistical noninferiority
claim. Fewer flags means simpler within this allocator framework, not necessarily
fewer total rules than the original router. No parameters were retuned after
viewing the matrix, and the selection is not a production promotion.

| F/P/R | Enabled factors | Passes all declared criteria? | Worst P&L retention versus 111 | Failed criteria |
|---|---:|---|---:|---|
| 000 | 0 | Yes | 100.7% | None |
| 001 | 1 | Yes | 100.7% | None |
| 010 | 1 | Yes | 95.6% | None |
| 011 | 2 | Yes | 100.0% | None |
| 100 | 1 | Yes | 100.9% | None |
| 101 | 2 | Yes | 100.9% | None |
| 110 | 2 | Yes | 95.8% | None |
| 111 | 3 | Yes | 100.0% | None |

SHADOW_CANDIDATE_FREEZE.json records the selected flags, exact code/input hashes,
common configuration, stress assumptions and selection record. That file is an
immutable research handoff for the delivered version; it does not launch or
operate a collector or trading service.

## Verification and limitations

94 preregistered unit tests passed, plus the separate synthetic probe described
above. The tests cover inherited accounting, partial fills, delayed
cancels/resizes, queue priority, factor isolation, missing flow, timer causality,
and known analytical main/interaction/Shapley effects. The 36 fill/order/decision
ledgers were independently checked for cash, fees, paired payouts, exposure,
exit-depth use, deadlines, order quantities, week attribution and factor/budget
rules. Frozen-source and input hashes match; all compressed ledgers read through
EOF. Ten prior Q5 cases reproduce both their financial aggregates and exact
uncompressed fill/order ledger hashes: four original-router cases, four 111
cases and two 110 neutral controls.

These checks establish reproducibility, not actual historical execution. Queue
positions, cancellations ahead, quote timing, market impact, exit liquidity,
fee history and netting/collateral mechanics remain execution assumptions.
Inventory contract-hours measure quantity and time, not cash drawdown. Comparing
36 versions on repeatedly examined 31 games does not create new evidence or 36
independent samples. Only two weeks are represented; no precise confidence
interval or p-value is supplied as evidence of a durable live edge.

The inherited execution engine is unchanged. Q5's small-wallet reservation
failure and two-cent capital-control workaround are not silently introduced
into this $5k factorial study. Assertions remain enabled, and failures cannot
be presented as completed P&L. No real orders were placed.

## Fresh-data next step

Use the frozen selected configuration alongside the original router and full 111
on an admitted fresh cohort, preserving the same receipt stream, budget, risk
limits and conservative queue treatment. The existing 32-game schedule-only
reservation and admission protocol are supplied. Most venue IDs remain
unresolved; continuous book capture has not been deployed. The first reserved
window starts 2026-09-22 at 00:15 UTC. A missed full window must be marked incomplete;
replacement requires a new pre-outcome schedule admission.

No always-on recorder is running, and this task has not created fresh future
outcomes. Establish durable collection before treating the selected candidate
as a prospective test. Combining additional strategies or wallets now would
introduce new variables before this mechanism is checked on unseen games.
