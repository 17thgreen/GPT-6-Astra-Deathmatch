# A bot fleet with explicit capital ownership

The proposed operating unit is a distinct viable market family/strategy, with
event-level positions underneath it. Its own ledger and hard exposure limit
make performance and risk attributable. That does not require permanently
locking the same cash allocation in every bot or granting independent wallets
permission to consume the same liquidity twice.

| Design | Benefit | Cost or untested question |
|---|---|---|
| Fixed funding for each bot | Clear cash isolation and easy attribution | Idle capital cannot serve opportunities elsewhere |
| Shared treasury with per-bot limits | Cash can follow nonoverlapping opportunities | Requires joint reservations, exposure and exit accounting |
| Protected bot allocation plus common reserve | Preserves minimum operating capacity with room to reallocate | More rules; must earn its complexity in an equal-capital experiment |

A sensible architecture to evaluate is distinct bots under one treasury/risk
controller. Actual custody or venue subaccounts are implementation choices whose
capabilities have not been established by this research. An internal budget is
not a claim of legal or venue-enforced asset segregation.

The amount X should reflect an admitted strategy's executable capacity, peak
simultaneous inventory, outstanding order reservations, completion costs and
correlated game exposure. A sport does not receive equal funding merely because
another sport has a bot. Losing strategies must not receive more capital as a
loss-recovery rule. Pending cancels retain cash and exposure until acknowledgment.

The controller needs one source of truth for total cash and outstanding orders;
per-bot and per-event ceilings; linked exposures across moneylines/spreads/totals;
and a complete fill/fee/inventory/exit ledger. Bot count is not a return multiplier.
When strategies overlap, they must consume one shared tape in price-time order.

## What is established now

Q7 is the selected NFL development candidate, based on reused data. M2's unchanged
CFB/WNBA transport pilot produced insufficient CFB profit and negative WNBA net.
All eight games remain in the record. Neither new sport is currently qualified
as a profitable fleet member. The M2 combined $5000 account had ample free cash
and unchanged economic fills relative to standalone accounts; money scarcity
did not explain those losses. Funding more bots is therefore not the present
mechanism to fix this pilot's completion problem.

## Next research comparison

First establish a viable strategy for each included market using separately
frozen sport-appropriate windows/queue/flow settings, reporting all outcomes.
Then preregister equal TOTAL funding alternatives: fixed per-bot allocations,
shared allocation, and (only if justified) protected allocations plus reserve.
Hold signals, eligible opportunities, order limits and total risk limits constant
where possible; identify any unavoidable policy differences.

Compare completed net, peak loss, exposure, cash utilization, unpaired inventory
time, passive completion, taker completion costs, and incremental contribution
after shared liquidity and correlated-event constraints. Preserve negative and
unresolved cases. Do not choose X by maximizing this eight-game cohort's output.
This is an experiment direction, not a completed fixed-versus-shared comparison.

The user owns forward validation. This design does not place live bets or fund
accounts, and it does not make forward validation a blocker to continued research.
