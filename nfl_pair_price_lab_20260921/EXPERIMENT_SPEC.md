# Q7: chosen-pair price consistency

Status: specified before Q7 code and outcomes. September 21, 2026.
Implements the approved proposal in docs/NEXT_EXPERIMENT.md. Q1–Q6 outcomes
are already known. This remains the same 31-game development cohort.

## Hypothesis and four arms

Does the acquisition-cost check on the two routes actually selected explain
Q6's gain, or does the allocator's other common machinery matter?

| Label | Architecture | Chosen-pair guard |
|---|---|---|
| router_off | Untouched AdaptiveReplay baseline | Off |
| router_on | Same router, guarded admission | On |
| allocator_off | Q6 000, margin rejection removed only | Off |
| allocator_on | Untouched Q6 FactorialReplay 000 | On |

No route optimization, threshold search, flow gate, cash earmark, opportunity
ranking, capital buffer, new predictor, or multi-wallet treatment is added.
Queues 3,300/10,000 × equal submit/cancel delays 0.25/5 seconds × four arms =
16 scenarios. Each alternative owns one shared $5,000 account. Desired order
size, hard event cap and total assumed exit depth all remain 250. Keep T−7d
through T−3h, five-minute winddown, final-12h queue 1,327,847.005, prior fees,
precision, participation, delayed historical quotes and all execution assertions.

## Exact guard and inventory semantics

Use the inherited router's chosen keys without substituting cheaper routes.
For two selected complementary directions define:

    margin = 1 - sum(selected cost) - 0.0002 - 2 * balance_precision / order_size

Cost includes the inherited maker fee estimate. New paired exposure is admitted
only when there are two selected opposite directions and margin > 0. This is
the existing Q6 threshold, not an optimized or atomic-arbitrage guarantee.

router_on evaluates the check at the router's existing refresh calls, without
adding timers or immediate post-fill refreshes. On rejection, selected entry
directions disappear from the desired order set. An already selected inventory
offset remains, capped to current absolute inventory minus other outstanding
offset quantities, including pending cancellations; exclude its own current
order from that subtraction. Floor to 0.01 and cap by the original wanted size.
Do not reroute to find an offset, promise a loss-free exit, or block an available
selected offset merely because the new-pair margin fails. Record candidates,
selected prices/costs, inventory, allowed offset size, and rejection reason.

Existing opening orders cancel normally when rejected; reductions use the
existing delayed resize/cancel mechanics. Partial fills remain real inventory.
Until acknowledgment, reservations and possible fills remain. A passing margin
does not assure simultaneous fills or protect against later adverse prices.

allocator_on is the untouched Q6 000 positive control: its check runs at its
inherited ten-minute budget updates, not continuously. allocator_off removes
only `if margin <= 0: return None` from that rank calculation. Keep neutral
adjusted rank 1 even for negative diagnostic score; no score-sign eligibility
filter may recreate the removed guard. Keep len-two requirement, proportional
budget sizing and inventory-offset floor. Guard cadence therefore differs by
architecture; the interaction includes that existing scheduling distinction.

## Controls, diagnostics and selection

All eight unchanged controls must reproduce Q6 financial aggregates AND exact
uncompressed fill/order ledger hashes. Independently reconcile all sixteen
financial ledgers, per-fill fees, cash, inventory, exits, deadlines and weeks.
Check input/source hashes before and after execution. Preserve failures and
unresolved runs; unresolved inventory gives null completed P&L.

Report within-architecture guard-on minus guard-off differences and their
difference-in-differences. Include both weeks, best-two-game exclusion,
inventory contract-hours, taker exits, residuals and fee totals. Report the
300-second midpoint change and entry-fee-adjusted markout for maker fills,
contract-weighted and by game, with missing coverage explicit. Use the latest
quote received by fill+300 seconds, asof after the fill, age <=120 seconds;
do not treat midpoint marks as executable exits or profit. No future diagnostic
may enter a policy decision. Count guard rejections as decisions, not independent
opportunities or hypothetical saved profit.

Select router_on as a simpler DEVELOPMENT_SHADOW_CANDIDATE only if it:

- finishes flat, positive, and strictly ahead of router_off in all four settings;
- retains at least 95% of allocator_on completed net in every setting;
- improves both primary (3,300/.25s) week contributions over router_off;
- remains positive excluding its best two primary games;
- has at most 1.25× router_off inventory contract-hours in every setting.

Otherwise retain the frozen Q6 candidate; do not select allocator_off based on
its observed profit. The 95% criterion is an engineering tolerance, not a
statistical noninferiority claim. Two reused weeks support no fresh validation,
annualized return or live promotion. No parameter tuning after outcomes.

## Persistence and forward boundary

Commit this specification before implementation. Freeze and commit implementation,
tests, analyses and reference/input hashes before running the matrix; commit
verified results afterward. Keep inherited directories unchanged.

The earlier 32-game reservation remains schedule-only, first full-window start
2026-09-22T00:15Z. No continuous recorder or live trading is operating. A missed
window remains incomplete; no backdated admission. Durable GET-only collection
and venue identity verification are separate pending operational requirements.
