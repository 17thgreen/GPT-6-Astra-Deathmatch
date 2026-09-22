# M3: isolate the pregame clock from queue assumptions

Specified after M2 outcomes, before extension tapes or M3 outcomes. This is a
new experiment; every NFL/Q7/M2 source, input and outcome remains unchanged.
M2's eight events are reused development data, never called fresh validation.

## Objective and first question

Seek completed net growth of a finite shared bankroll, accounting for cash tied
up, turnover, unpaired inventory and completion costs. More fills or a thinner
assumed queue alone do not establish an improvement. The immediate question is
whether ending at T-3h, and transplanting the NFL final-12h queue assumption,
explain the poor CFB/WNBA transport result. Study the two sports independently.

## Frozen matrix

Two sports (NCAAF/WNBA) x two cutoffs (T-3h/T-30m) x two queue environments
(NFL late-depth profile/constant-depth profile) x early queues (3300/10000)
x submit/cancel delays (.25s/5s) = 32 cases.

The NFL profile retains queue 1,327,847.005 inside the final 12 hours before the
REAL scheduled start. Constant-depth scenarios hold the same 3300 or 10000
queue throughout. These are unknown-environment sensitivity cases, not measured
sport-specific queues and not tunable strategy parameters. Compare the two
cutoffs WITHIN each identical environment. Never select the queue that wins.

Both policies start at max(listing,T-7d), stop opening five minutes before their
cutoff with inherited latency allowance, and wind down through the cutoff. No
in-play trading. Keep Q7's pair-cost gate, route selection, priority retention,
$5000 cash, 250 desired order/event cap/total exit allowance, .5 participation,
.0175/.07 hypothetical costs, precision, 60-second quote delay and 300-second age
limit. NFL pricing/accounting code is imported unchanged. No size, margin,
flow-window, event-selection, exit-depth or fee search.

## Data and implementation

Keep all 16 M2 market inputs. Extend each from its old endpoint (T-3h+5m) through
T-30m+5m with non-block trades and one-minute close bid/ask quotes. Bounds:
200 trade pages, 3 request attempts, 15-second timeout, four workers. Preserve
all failures; do not replace events or shrink to successful markets. Validate
pagination, identities, hashes and fixed-point values. Deduplicate overlapping
trade IDs and quote minutes, rejecting conflicting normalized observations.
Missing minutes remain absent. Schedule/lifecycle and historical-fee limitations
from M2 remain; no claim of historical receipt-time capture or actual fills.

The inherited kernel names its clock anchor `kickoff`. A boundary adapter may
set that INTERNAL anchor to desired cutoff+3h to reuse its unmodified winddown
and retries, provided actual scheduled start is retained separately. Eligibility
must still open at real-start-minus-7d/listing; queue transition must remain
real-start-minus-12h. Explicit tests must verify both distinctions. Output must
record real schedule and the derived internal anchor; never pass the anchor off
as the actual start. No real timestamp on the tape is changed.

## Checks and reporting

Before outcomes, commit this spec; then commit implementation, tests and all
input/source hashes. The eight T-3h/NFL-profile cases must reproduce exact M2
fill and order histories and financial aggregates, despite the additional tape.
Independently reconcile every new fee/cash/inventory/order/exit ledger with its
declared cutoff. Residual positions give null completed profit.

Report net, net per $1000 initial cash, net per 1000 filled contracts (maker AND
taker), passive completion, taker quantity, inventory contract-hours, FIFO cost
of carried inventory in dollar-hours, and listing/quote coverage. Inventory
cost-hours omit resting-order reservations and are NOT total committed capital
or compounding capacity. Do not annualize or apply a full-bankroll compounding
formula. Those require equal calendar exposure and feasible reinvestment.

Use the exact M2 controls to check code transport. Analyze cutoff effects within
each sport/queue profile/depth/delay. A favorable constant-depth result is evidence
conditional on that queue, not proof of real queue access. No production or
market promotion from this eight-game study. Preserve all negative outcomes.

## Subsequent separate stages

1. Within-market sizing and completion experiments: couple order size with event
   inventory cap; compare capacity-aware entry and loss-aware completion. Q2/Q4's
   negative NFL findings stay intact; a sport can have different economics.
2. Independent MLB/NHL/NBA full-game moneyline admission and historical replay,
   with game/period/doubleheader/schedule rules and market-specific fees explicit.
   Missing/offseason or sparse cohorts remain unscored. Use a matched calendar
   window for currently active markets and label separate-season cohorts clearly.
3. Freeze new evaluation cohorts by schedule before outcome/price inspection.
   Compare candidates with the preserved NFL baseline under the same initial
   capital, calendar window, costs and risk controls; keep selection multiplicity
   and all tried variants visible.
4. Test capital capacity and feasible reinvestment only for surviving candidates:
   fixed versus shared funding at equal total bankroll, then explicit resizing
   after realized profits subject to unchanged risk/liquidity constraints.

User owns forward validation. No deployment, live orders or funding transfers.
