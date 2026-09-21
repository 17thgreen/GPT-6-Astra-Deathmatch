# Q7 proposal: isolate chosen-pair price consistency

Status: PROPOSED, NOT IMPLEMENTED, NOT RUN. This proposal is committed before any
Q7 outputs. Implementation details and exact code must be frozen before execution.

## Question

Does checking the combined acquisition cost of the two routes actually chosen
explain the improvement, or do the allocator's scheduling and sizing rules matter?
The Q6 synthetic probe establishes that the original router can choose two routes
that look attractive against different alternative counterparties yet jointly
cost more than their paired payout. It does not establish historical P&L impact.

## Controlled design

Use a 2×2 comparison of architecture and actual-pair check:

1. Original router, check off: untouched reference.
2. Original router, check on: change only admission of new paired exposure.
3. Q6 simplified allocator, check off: preserve its timing/sizing/offset rules.
4. Q6 simplified allocator, check on: untouched Q6 reference.

Keep the $5,000 account, 31-game development cohort, 250 event cap, 250 total
assumed game exit budget, fee model, quote timing and queue assumptions fixed.
Run the same queues 3,300/10,000 and delays .25/5 seconds: 16 scenarios.
Do not optimize route choices, thresholds, patience or size at the same time.

Before coding, define the treatment of offset-only orders and partially filled
pairs. A check must not block necessary inventory reduction, assume simultaneous
fills, inspect future quotes, or cancel instantly. Record rejected pairs and
why they were rejected, without treating skipped hypothetical profits as money.
For the allocator check-off arm, remove only the combined-cost filter; do not
accidentally retain it through another score or eligibility condition. Use the
neutral ranking already selected by Q6. Match all positive controls exactly.

## Decision and next gate

Report guard effects within each architecture and their interaction, completed
net after fees, adverse fills, residuals, per-week contributions and inventory
duration. Preserve losses and exclude unresolved cases from completed-profit
claims. Declare the candidate-selection rule and freeze source before outcomes.

If a simpler guard-only router retains the improvement, freeze it for prospective
shadow testing. If it does not, the allocator's common rules remain a combined
mechanism requiring further isolation. Neither result substitutes for fresh data.

In parallel planning, establish a durable GET-only public collector and admit a
future cohort before its full T−7d windows. Deployment is not accomplished by
committing a Docker file. Live execution is outside this research proposal.
