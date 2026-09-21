# Continuity recovery — September 21, 2026

The user transferred the conversation “Adapt Stern For Sports Betting” after
its length limit, with the instruction: “Got it. Next steps are approved for
a go once youre done with git.” This authorizes completion of the interrupted
checkpoint and the previously proposed Q7 experiment, plus routine research
commits. It does not authorize live orders.

## Recovery evidence

Recovered prior-conversation excerpts and the complete surviving original
workspace at `/workspace/scratch/25b7b116f529`. No claim is made of access to a
verbatim export of every chat message. Original code, protocols, result reports,
negative outcomes, frozen manifests, compressed ledgers and eight research kits
survived. The tracked checkpoint covers 936 files.

At takeover, GitHub main contained only README.md at 65e355e. Local checkpoint
9ebf10c contained the full import. Completed the interrupted upload as 7da067a,
preserving the existing remote parent. Remote and original local tree both
equal 0fadd18c5c2ef3c71d96c15f2cdd1dbe0b63a9c2. The 94-test Q6 suite passes.
Large captures/ledgers remain external artifacts indexed by the original
provenance files; cloning alone does not restore their bytes.

## Goal and research progression

Build a reproducible, executable NFL prediction-market edge for Logan's Kalshi
research project. Better forecasts, optimistic fills and attractive backtests
are insufficient. Started with Hal Stern's Brownian score model; state-conditioned
V1 improved historical forecast scores. Later complexity did not reliably beat
V1. Trading value of the market-anchored event update remains untested; final
three minutes, ties and overtime need distinct treatment. The live research
priority moved to NFL moneyline passive making, T−7d to T−3h.

| Stage | Preserved conclusion |
|---|---|
| Maker audit/replay | Correct execution defects; distinguish per-game accounts, pooled capital, windows and queues. |
| Q1 | Preserve queue priority and research equivalent-payoff routing; early queue remains assumed. |
| Q2 | Completion controller reduced inventory duration 99.77%, but primary net fell from $201.52 to $57.63; no profit promotion. |
| Q3 | Better receipt-time and queue-service measurement; zero completed fresh validation games. |
| Q4 | Small early-week orders failed. Size and cap interact; unresolved cap-500 cases remain unresolved. |
| Q5 | Allocation bundle improved development results; ranking alone did not explain the gain. |
| Q6 | 000 removed the optional flow gate, offset-cash earmark and ranking while preserving the common allocator. |
| Q7 | Approved next: 2×2 architecture × chosen-pair guard study, not yet run at takeover. |

Q6 primary completed simulated net: $345.24 versus original router $201.52;
queue-10,000 comparison: $75.90 versus $10.35. Same reused 31 games, two weeks,
one shared $5,000 account, 250-event cap and 250 assumed exit budget. Q6 included
36 scenarios, 94 unit tests and ten exact prior ledger regressions. These are
development results, not actual trading returns. The pair-cost synthetic probe
motivates Q7 but did not establish historical profit attribution.

## Multi-bot and forward boundaries

Four/five $1,000 bots require shared market volume, price-time queue ordering,
combined exposure and exit liquidity. Never multiply independent $1,000 replays.
The prior $1k/$4k/$5k controls tested one account at each funding level, with a
separately documented two-cent reservation buffer. The proper multi-wallet
simulator is designed but unimplemented. That buffer is not in Q6 or Q7.

No always-on recorder is running. The 32-game forward reservation is schedule-only
with most venue IDs unresolved; its first full T−7d window starts 2026-09-22
00:15 UTC. Missed capture cannot be backdated. Queue position, actual receipt and
order delay, executable exit depth, historical fees and collateral mechanics
remain unverified. Do not repeat rejected hypotheses as new discoveries.

Current working branch: research/q7-paired-price. Use Q7's frozen spec and future
results record to advance this handoff without editing old experiment snapshots.

## Work completed in the replacement chat

All eight original kit checksums verified (RECOVERY_ARCHIVE_VERIFICATION.json).
Q7 specification committed at d15f57c; implementation frozen at f0a2692 before
outcomes. Completed 16 scenarios, 115 unit tests, independent ledger/fee audits
and eight exact Q6 fill/order control matches. All declared selection criteria
pass for router_on. Primary net is $354.33; queue-10,000/.25s net is $90.45;
slow-delay values are $353.89 and $79.08. Same reused games and execution
assumptions. The current candidate is Q7's frozen guarded router; Q6 stays as
an immutable prior reference. See Q7_RESULTS.md and SHADOW_CANDIDATE_FREEZE.json.

Removing the guard from the Q6 allocator reduces primary net to $205.94,
close to the original router's $201.52. Adding it to the original router beats
the Q6 allocator in every scenario. This supports the admission mechanism
within this simulator; it does not prove a durable market edge. Offset-order
handling and each architecture's original timing remain explicit in the spec.

Next gate: durable forward collection and pre-window cohort admission. The
collector currently rejects holdout configuration, so a future admission and
capture version needs explicit review and freeze, plus an actual persistent
host. No host deployment or background collection was performed by this chat.


## Latest active mandate and Q8 checkpoint

User directs queue access, profitability and market expansion research; user
owns forward validation. Keep GitHub current. Do not make capture readiness a
blocker for this lane. No live orders or higher risk limits authorized.

Branch: research/q8-joint-routing. Q8 spec commit 4e48fa6; implementation freeze
410dc16; portability build dda1b29. Twelve frozen scenarios completed. Recovery
and joint routing improve the queue-3300 headline but underperform Q7 at queue
10000 and fail the two-week improvement screen. Retain Q7 GuardedRouter.
Independent verification: all 12 ledgers, four exact Q7 fill/order controls;
128 replay tests plus eight separate portability tests. No outcome-driven tuning.
Read Q8_RESULTS.md, selection.json, verification.json and archive indexes.

New market_portability module checks payout vectors, exposes an explicit profile
schema and GET-only series inspector. It is not a full non-NFL replay adapter.
Research priority: NCAAF and basketball pregame adapters; exact-threshold
spreads/totals separately. Three-way soccer requires a different cross-outcome
inventory model. All sampled current fees/ticks and exceptional rules are in
SERIES_SNAPSHOT.json; sample discovery is not an exhaustive admission process.

Next queue hypothesis should explicitly value unbalanced inventory and
completion costs: Q8's static margin times bottleneck service was insufficient.
Do not tune Q8 after its negative result. See market_portability/RESEARCH_ROADMAP.md.
