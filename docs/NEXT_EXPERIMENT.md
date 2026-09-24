# Q7 proposal: isolate chosen-pair price consistency

Status: IMPLEMENTED and FROZEN in `nfl_paircheck_lab_20260922`. Later registry
rows record a Q7 Arm B kill, plus frozen rehab pass 1 (PR38) and pass 2 (PR47),
citing desk-verified `q3300_d0.25_B.json` and `q3300_d0.25_D.json` summary
hashes. The in-tree pair-check result file remains `NOT_RUN_INPUTS_MISSING`
with `scenarios_executed` 0, and the rehab result files in this checkout also
record `scenarios_executed` 0. This file does not report Q7 P&L. The read-only
reconciliation memo on main
(`lab/governance/astra/packets/q7_reconciliation_20260924/Q7_RECONCILIATION_MEMO_2026-09-24.md`)
is documentation and is not a score. The hypothesis was committed before the
source freeze. Historical replay waits on the owner kit; see that directory's
README. Live execution remains outside this experiment.

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
That collector work is specified separately in
`nfl_prospective_recorder_20260922/PROTOCOL.md` and is not part of the Q7 2×2.
