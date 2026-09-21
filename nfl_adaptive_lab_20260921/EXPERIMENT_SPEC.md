# Q5: three isolated adaptive-control experiments

Frozen before this experiment's historical outcomes. September 21, 2026.

## Cohort and common engine

Reuse Q4's 31 games (16 Week 1, 15 Week 2), 62 complementary team markets,
1,046,720 normalized records. These are development data, not a holdout.
One shared $5,000 account across overlapping games; no game/week cash resets.
T−7d to T−3h, five-minute winddown. Desired order size and hard worst-case
inventory/reservation cap both 250. Total assumed taker exit depth stays 250
per game. Keep Q4 fee, precision, minute-quote delay, freshness, participation,
netting and matching assumptions unchanged. Baseline source is copied unchanged
and hashed. No API orders, external price predictors, fit, or parameter search.

Run 16 cases: baseline, inventory, patience, allocation × early queues 3,300 and
10,000 × equal submit/cancel delays 0.25 and 5 seconds. The final-12h queue stays
1,327,847.005. The 5-second case is a sensitivity, not measured trading latency.
Each candidate changes one control family; no combinations will be tried here.

## 1. Inventory: conditional soft targets within a fixed hard cap

Keep the existing router. At each refresh, compute each side's opposing service
capacity from only strictly earlier trades over one hour: maximum across
alternative equivalent routes of max(0, rate × horizon − remaining queue) × 0.5.
Do not sum linked routes. Horizon is 1,800 seconds or time to winddown minus
cancel delay, whichever is shorter. Target is floor-to-.01 of min(250, remaining
assumed exit budget, max(25, opposing service capacity)). Desired new/resting
quantity is min(250, target − direction × inventory − other same-direction
outstanding quantities), floored at zero. Pending cancels and pending resizes
still reserve their full current quantities. Recheck after a maker fill.

This is a soft inventory target: reducing it cannot revoke an already executable
order. Keep fills above a newly reduced target during acknowledgment races;
never clip them. The preexisting hard 250 worst-case cap remains binding.
Same-price reductions preserve the existing identity and queue only after the
normal delay. Increased size cannot acquire free priority.

## 2. Patience: flow, depletion and adverse selection

Keep baseline route selection, wanted size, hard cap and exit policy. Only
entry-side order retention/admission changes. Inventory-offsetting orders are
exempt, retaining baseline behavior (including possible subsequent reversal).

For maker fills adding inventory, observe midpoint minus acquisition price after
300 seconds, using the first received quote whose as-of time reaches that
horizon. Reject observations over 300 seconds late or invalid. No interpolation.
Use only observations received strictly before a decision, within the last hour,
with at least five fill observations and 25 contracts. This is price markout,
not executable profit or an independent-sample significance test.

For an entry side, veto if weighted mean markout < −2 cents; also veto if mean
< −0.5 cents and trailing service rate on that side exceeds 3× the opposite
rate. Rates are maxima across equivalent routes, not sums. Missing markouts
mean no toxicity veto, not evidence of safety.

For a resting order with queue still ahead, service score is
min(1, own rate × 600 / (remaining queue + remaining quantity / .5)). Patience
is 120 + 1,680 × score seconds. If at least half the initial queue has depleted
and own flow is not >3× opposing flow, patience is 1,800 seconds. On expiry,
cancel and impose a 60-second route cooldown. A zero-ahead order is not canceled
merely because of age. Existing price-change/staleness/winddown rules remain.

This is a predeclared heuristic, not a fitted fill or competing-risk probability.
It is a single retention-control bundle; this run cannot separate its individual
flow, markout and age components.

## 3. Allocation: ranked prospective paired return per cash-hour

Keep the existing per-game router. Recompute portfolio budgets every 600 seconds
when a refresh occurs, using current eligible books and strictly earlier flow.
First protect cash for existing net-inventory offsets: per game, max(current
cash reserved by opposite-direction orders, net inventory × largest current
offset unit cost). If no offset candidate is eligible use $1 per unit. This can
exceed available cash; then no entry budget is issued.

For each event use its two chosen routes. Require positive trailing rate on both
and a positive pair margin after maker fees, .0002 extra unit-cost allowance,
and two account-precision units per 250-unit pair. Forecast completion time as
max((remaining queue + 250/.5)/rate) across the two legs. Score is prospective
250-unit pair profit / (reserved pair cash × max(wait in hours, 1/60)).
These quantities are ranking heuristics, not calibrated expected returns.

Multiply incumbent scores by 1.25 to discourage switching. Existing queues are
used only at the same current price; changed-price/new routes use the queue at
the back. Record the difference between wait using retained and reset queues.
Priority cost is represented by these waits and actual replay queue resets,
not by an invented cash charge or transferable queue credit.

Rank by adjusted score then event ID. Allocate remaining cash greedily up to each
pair's estimated reservation requirement, including partial last allocations.
At refresh, divide event budget proportionately across its chosen routes;
preserve enough desired offset quantity to close existing net inventory.
Nonselected orders cancel normally. Until acknowledgments, their cash and
inventory reservations remain binding and can delay new allocations. Budgets
are targets refreshed every 10 minutes, not promises of fills or instantaneous
capital release. Actual 5k cash and 250 event reservation limits always apply.

## Declared evaluation and decision

Reconcile all fill/order ledgers and frozen hashes. Require both .25-second
baselines to reproduce Q2's financial aggregates within 1e−7. Report each
candidate against its identical queue/delay baseline, including net after fees,
week contributions, maker/taker quantities, inventory contract-hours, paired
holding time, peak order reservations, and residuals. Report profit excluding
the candidate's two best games as a concentration diagnostic.

A DEVELOPMENT_CHALLENGER must be flat and earn more than its baseline in all
four scenarios; improve both week contributions at q3300/.25s; have positive
absolute net in every scenario; have primary profit excluding its two best
games >0; and have unhedged contract-hours no more than 1.25× baseline in every
scenario. This is an engineering screen, not a statistical or live promotion.
All other candidates remain RESEARCH_NOT_PROMOTED. No threshold retuning after
these outputs. Preserve negative results. No combinations, added cap sweeps,
or selecting a subset of games based on the outcomes.

## Fresh-data boundary

The existing reserved 32-game schedule is carried forward without reading
outcomes. It is not yet an admitted executable market cohort; most venue IDs
are missing and complete public-book capture is unavailable. This run contains
zero fresh completed games. The attached forward protocol specifies capture,
latency and cohort admission gates. No live or always-on service is deployed by
this experiment. Historical public prints cannot reveal actual queue positions
or canceled volume ahead; forward public data alone still cannot verify those.
