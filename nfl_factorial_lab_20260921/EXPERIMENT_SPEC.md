# Q6 allocation mechanism study: frozen 2×2×2 design

September 21, 2026. Rules fixed before Q6 outcomes. Existing Q5 outcomes are
known and motivated this study. The same 31 games are reused development data,
not an untouched holdout, and not 36 independent game samples.

## Factors and common machinery

Factor order is F/P/R. Eight combinations000 through111:

- F: require strictly positive trailing observed trade flow on BOTH chosen
  complementary directions before granting an entry budget.
- P: subtract the estimated cash needed to offset existing net inventory from
  cash available for new entry budgets.
- R: rank eligible event budgets by estimated paired profit per cash-hour,
  including the inherited1.25 incumbent multiplier, rather than constant-score
  ordering with event-ID tie breaks.

For F=off, pairs with zero flow are admitted if all other guards pass. Unknown
flow is never invented: estimated wait is null, score0, and R=on puts those
pairs after positive-score pairs. R=off assigns adjusted score1 to every
admitted pair. R includes the incumbent bonus as one ranking-policy component;
this study does not separately isolate that bonus.

For P=off only the earmarked cash subtraction disappears. Actual cash/inventory
reservations, cancel/resize delays, and the common offset-quantity floor remain
intact. Allowing a risk-limit violation would be a different experiment.

All eight arms retain the ten-minute budget update cadence, inherited per-event
router, positive pair-margin cushion, proportional sizing to event budgets,
normal order matching/fees, and permission to quote an inventory offset even
without an entry budget. The all-off000 arm is therefore NOT the original
router. Its difference from the original router measures the common allocator
machinery as a bundle. Do not attribute that residual to F, P or R.

111 must reproduce the original Q5 allocation arm. 110 must reproduce Q5's
neutral-ordering diagnostic at the two previously tested .25-second scenarios.
Preserve original reference summaries and uncompressed fill/order ledger hashes.

## Scenarios and execution

Eight factor arms plus the untouched original router, at early queues3300 and
10000, with equal submit/cancel delays.25 and5seconds:36completed-case targets.
Reuse all31games (16 Week1,15 Week2), one pooled$5000 account, desired order250,
hard event exposure/reservation limit250, total assumed game exit depth250,
T−7d to T−3h, and five-minute winddown. All inherited fee coefficients,
precision, delayed minute quotes, .5 participation and last12h queue remain
unchanged. The supplemental Q5 two-cent capital buffer is NOT used here.
The earlier tight-wallet reservation issue remains documented in Q5; keep
assertions enabled. On an assertion stop, retain the failure and do not silently
relax limits or count it as a loss. No parameter tuning after results.

No paid data, live orders, external predictors or multi-wallet simulation.
Financial and price-time accounting source is copied unchanged and hashed.

## Evaluation and attribution

For every arm/scenario report net completed P&L after fees, both pooled-account
week contributions, unhedged contract-hours, taker exit volume, peak reserved
cash, and P&L excluding its two best games. Unresolved inventory means null
completed P&L, not a successful return. Residual payout bounds remain visible.

Within each of four queue/latency scenarios compute:

1. F/P/R main effects: average on-minus-off P&L across the other four settings.
2. Every conditional on-minus-off contrast, showing whether signs depend on
   the other components.
3. Pairwise differences-in-differences averaged over the third factor, plus the
   three-way interaction.
4. Shapley attribution of111 minus000: average each factor's marginal effect
   over all six factor-addition orders. Sum must reconcile exactly to111−000.
5. Common-machinery residual000 minus original router. Residual plus the three
   Shapley contributions must equal111 minus original router.

These are deterministic within-simulator policy comparisons, not estimated live
causal effects. All accounts replay the same development observations separately;
there is no cross-arm competition for fills because these are counterfactual
alternatives, not concurrent bots. Portfolio cash coupling prevents treating each
fill or game as an independent random observation. Two weeks are insufficient
for a persuasive cluster-based significance claim. No p-value or confidence
interval is used to disguise this limitation.

## Predeclared simplest-candidate selection

Eligibility as a DEVELOPMENT_CANDIDATE requires completed flat inventory and
positive P&L in all four scenarios, strictly beating the matched original router
in all four; improved contributions from BOTH weeks at q3300/.25; positive
primary P&L excluding its two best games; and unhedged contract-hours at most
1.25× original-router hours in each scenario.

To retain the full bundle's economics, require P&L at least95% of111 in EVERY
scenario (if111 has nonpositive or unresolved P&L, selection is withheld). This
5% tolerance is an engineering simplification criterion, not statistical
noninferiority. Among eligible arms, choose the fewest enabled factors, then
largest worst-scenario ratio to111, then ascending bit label. Do not run new
thresholds, combinations or optimizations after examining these results.

Freeze the selected exact source/config hashes and criteria for future shadow
research. It is not a production promotion or evidence of fresh profitability.
If no arm passes, report no selection. Do not replace the original router live.

## Forward boundary

Carry the existing schedule-only32-game reservation and prior admission protocol
without reading future outcomes. Most venue identities remain unresolved and no
complete forward book collection is established. The first reserved T−7d window
begins2026-09-22T00:15Z. If missed, mark the game incomplete; a new complete
cohort requires a new schedule-only admission before its windows/outcomes.
No always-on recorder is running. This task completes the offline mechanism
study and a reproducible shadow candidate freeze; future outcomes require time
and an actual durable data collection deployment.
