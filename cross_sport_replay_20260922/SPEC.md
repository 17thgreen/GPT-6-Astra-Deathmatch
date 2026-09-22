# M2: bounded historical transport pilot — specified before outcomes

Question: does frozen Q7 passive making produce completed simulated net profit
on an initial NCAAF/WNBA cohort under the same execution stresses? This is a
small retrospective engineering pilot, not validation or a ranking of sports.

Discover markets with close times from 2026-09-14T00:00Z through 2026-09-22T00:00Z
for KXNCAAFGAME and KXWNBAGAME. Exhaust pagination (max 20 pages). Deduplicate event
IDs, retain IDs whose encoded event date is Sep 14–20 2026, sort event ticker
ascending and reserve the first FOUR per series before inspecting price tapes.
The ticker date selects candidates only, never supplies game-start time. Retrieve
exact event-linked sport milestones for starts. Missing/ambiguous schedules or
unsupported event structure remain failed slots, never replaced by other games.
Commit resolved cohort before downloading trade/quote tapes.

Require two binary $1 tickers, opposite normal-game outcomes, MECNET and mutual
exclusivity, one-cent grids. Reconstruct schedule as retrieved now; do not claim
historically captured receipt-time schedules. Preserve rule text and exceptions.
Q7's cross-market immediate netting remains a hypothetical inherited assumption;
no residual inventory is settled at an inferred binary payoff. Special outcomes
are not traded through; unresolved positions invalidate completed profit.

Collect seven days before reconstructed start through T-3h plus five minutes,
bounded by each market's listing time. Exhaust public non-block trades, retain
1-minute bid/ask close quotes with Q7's 60s receipt delay and 300s age cap. Missing
quotes are not interpolated. Maximum 200 trade pages per ticker, 3 request
attempts per page, 15-second timeout. Save progress and errors; failure does not
permit skipping the game. Quote coverage and execution eligibility are reported.
Historical series/event fee verification is separate from current metadata:
use Q7's .0175/.07 coefficients explicitly as standardized hypothetical costs,
not a claim of exact past charged fees.

Import Q7 GuardedRouter and underlying accounting without changing their source.
NCAAF-only, WNBA-only, combined x early queues 3300/10000 x delays .25/5 = 12
counterfactual runs. One $5000 account per alternative, 250 desired order/event
cap/assumed total exit depth, inherited 1,327,847.005 final-12h queue, T-7d to T-3h
entry and five-minute winddown. Keeping NFL assumptions is a transport control,
not a calibrated non-NFL model. Never sum standalone profits as one $5000 result.

Freeze source/input hashes before replay. Verify inherited unit tests and
independently reconcile fills/fees/cash/inventory/exits before reporting profit.
Report per-game and sport contributions, fills, unhedged hours, taker exits,
residuals and actual window coverage. No parameter tuning or promotion gate.
If capture/admission is incomplete, publish the failure and null profit, build
what can be verified, and do not fabricate or silently shrink the cohort.

Code/spec/results in Git; larger raw captures/ledgers in checksum-indexed archives.
User owns forward validation. No live orders or risk-limit changes.
