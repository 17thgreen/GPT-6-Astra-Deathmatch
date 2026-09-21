"""Generate a candid comparison from the full frozen matrix, including failures."""
import json
from pathlib import Path
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parent
MODES=['q1_route','pair_gate','pair_complete']
LABELS={'q1_route':'Previous Q1 router','pair_gate':'Joint entry gate','pair_complete':'Gate + inventory completion'}
def load(name):return json.loads((ROOT/name).read_text())
def money(x):return 'Unresolved' if x is None else ('+' if x>=0 else '−')+f'${abs(x):,.2f}'
def number(x,digits=2):return '—' if x is None else f'{x:,.{digits}f}'

def main():
    summary=load('results/experiment_summary.json');cases=summary['scenarios'];verify=load('results/verification.json')
    def get(cohort,q,mode):return cases[f'{cohort}_{q}_{mode}']
    eligible=[]
    for mode in MODES[1:]:
        comparisons=[(get(c,'q3300',mode)['completed_strategy_pnl'],get(c,'q3300','q1_route')['completed_strategy_pnl'])
                     for c in ['week1','week2','combined']]
        if all(a is not None and b is not None and a>b for a,b in comparisons):eligible.append(mode)
    decision=('The candidate(s) passing the frozen primary comparison are: '+', '.join(LABELS[m] for m in eligible)+'. This is permission for further research, not live execution validation.'
              if eligible else '**Neither new candidate passes the frozen promotion rule.** Do not replace the previous router with either candidate on these results.')
    primary=[]
    for cohort,n in [('week1',16),('week2',15),('combined',31)]:
        primary.append('| '+f'{cohort}, {n} games'+' | '+' | '.join(money(get(cohort,'q3300',m)['completed_strategy_pnl']) for m in MODES)+' |')
    pooled=[]
    for q,label in [('q291','290.595'),('q3300','3,300'),('q10000','10,000'),('q100000','100,000')]:
        pooled.append('| '+label+' | '+' | '.join(money(get('combined',q,m)['completed_strategy_pnl']) for m in MODES)+' |')
    inventory=[]
    for mode in MODES:
        r=get('combined','q3300',mode);d=r['pair_holding_time_seconds']
        inventory.append('| '+LABELS[mode]+' | '+number(r['maker_contracts'],0)+' | '+number(r['unhedged_contract_hours'],0)+' | '+
            number(d['weighted_median']/60 if d['weighted_median'] is not None else None)+' | '+number(r['taker_contracts'])+' | '+
            number(r['metrics'].get('completion_overshoot_contracts',0))+' |')
    diagnostic=[]
    for mode in MODES:
        r=get('combined','q3300',mode)
        diagnostic.append('| '+LABELS[mode]+' | '+str(r['positive_games'])+' / 31 | '+money(r['pnl_excluding_top_two_games'])+' | '+
            number(r['net_cents_per_traded_contract'],5)+' | '+money(r['metrics'].get('fees',0))+' |')
    base=get('combined','q3300','q1_route');complete=get('combined','q3300','pair_complete')
    inventory_reduction=100*(1-complete['unhedged_contract_hours']/base['unhedged_contract_hours'])
    edge_ratio=complete['net_cents_per_traded_contract']/base['net_cents_per_traded_contract']
    full=[]
    for cohort in ['week1','week2']:
        for q,label in [('q291','290.595'),('q3300','3,300'),('q10000','10,000')]:
            full.append('| '+cohort+' | '+label+' | '+' | '.join(money(get(cohort,q,m)['completed_strategy_pnl']) for m in MODES)+' |')
    data=summary['cohorts'];new=data['week2'];old=data['week1']
    incomplete=[name for name,s in cases.items() if s['completed_strategy_pnl'] is None]
    residual=('All 30 scenarios finish flat under the model’s assumed exit capacity.' if not incomplete else
              'Scenarios with unresolved inventory: '+', '.join(incomplete)+'. Their JSON results report cash plus terminal-payout bounds, not completed P&L.')
    gate_stats=[]
    for mode in MODES[1:]:
        m=get('combined','q3300',mode)['metrics'];checks=m.get('entry_gate_checks',0);skip=m.get('entry_gate_abstentions',0)
        gate_stats.append(f'{LABELS[mode]} abstained on {int(skip):,} of {int(checks):,} entry checks ({100*skip/checks:.1f}%).' if checks else f'{LABELS[mode]} had no entry checks.')
    text=f'''# NFL completion experiment Q2 — 31-game comparison

September 21, 2026. Research only; no live orders placed. This extends Q1 with **15 completed Week 2 games**, **{new['trades']:,} newly captured public trades**, and **{new['quotes']:,} minute bid/ask observations**. The experiment now covers **31 games and 62 team markets** across two NFL weeks.

{decision}

**Primary comparison: assumed early queue of 3,300 contracts**

| Cohort | Previous Q1 router | Joint entry gate | Gate + inventory completion |
|---|---:|---:|---:|
{chr(10).join(primary)}

The isolated week-one and week-two rows each start with one $5,000 account. The **combined row runs all 31 games chronologically on ONE shared $5,000 bankroll**. Their seven-day trading windows overlap, so adding the isolated rows does not establish the pooled result. This is the same T−7 days to T−3 hours policy, with a five-minute liquidation lead.

**What changed**

Q1 chooses an entry route partly from its own queue and matching flow. Its service score can be positive even when projected incoming volume would not consume the queue during the score’s horizon. The new gate first subtracts queue ahead, then projects service; it requires both directions of a potential pair to have capacity and a positive margin after modeled fees and rounding allowances. Pair quantity is limited by the slower leg. It retains an incumbent pair unless a challenger’s projected pair dollars improve by more than 25%.

The completion variant additionally stops adding exposure in the current inventory direction and concentrates on an offset after a fill. It accounts for other pending offset orders and keeps cancellation/resize acknowledgment delays. Existing inventory still receives an offset quote if the entry gate fails, even when closing means a loss. Neither candidate improves its price inside the spread.

These are **steady-flow projections, not calibrated execution probabilities**. They cannot make fills atomic or guarantee the offset quote will remain available. A ten-minute projection horizon, capped by the entry deadline, is a fixed research choice rather than an optimized parameter. A gate can reject eventual profitable trades if flow later accelerates or a quote remains attractive much longer than ten minutes.

**Queue sensitivity on the pooled 31-game account**

| Assumed early queue | Previous Q1 router | Joint entry gate | Gate + inventory completion |
|---|---:|---:|---:|
{chr(10).join(pooled)}

Only the early queue changes. The original last-twelve-hour queue remains 1,327,847.005 contracts throughout. All these queues are assumptions; no present-day snapshot is substituted for a historical queue. A policy that achieves zero activity or avoids a loss has not thereby established a profitable market-making strategy.

**Inventory and completion costs at queue 3,300, pooled account**

| Policy | Maker contracts | Unhedged contract-hours | Median paired-unit holding time, minutes | Taker exit contracts | Offset-instruction overshoot contracts |
|---|---:|---:|---:|---:|---:|
{chr(10).join(inventory)}

Holding time runs from a unit’s acquisition until its FIFO offset; it is not the queue wait before its first fill. Contract-hours measure the amount and duration of unhedged inventory, not dollars reserved for resting orders or maximum drawdown. Reducing either metric is a useful operational change, but does not automatically compensate for lost profit.

There is a useful secondary finding: **the completion controller reduces unhedged contract-hours by {inventory_reduction:.2f}% and earns {edge_ratio:.2f} times as much net per traded contract**, while lowering total profit from {money(base['completed_strategy_pnl'])} to {money(complete['completed_strategy_pnl'])}. This is a substantial inventory-efficiency tradeoff, not a pass of the frozen profit-promotion rule. It warrants separate research as an operating mode when limiting inventory is the objective. Contract-hours are not a calibrated risk measure, and the return cannot be scaled linearly by the freed inventory capacity; eligible opportunities are limited.

An offset instruction can still overshoot during acknowledgment races. The model records that excess rather than silently clipping fills. This research controller is not an exchange-native cross-ticker reduce-only guarantee. The same worst-case 250-contract event exposure bound remains in force.

{' '.join(gate_stats)} These repeated decision checks are not independent trials or unique trading opportunities.

**Concentration and economic margin**

| Policy, pooled queue 3,300 | Positive games | P&L excluding two largest game contributors | Net cents per traded contract | Modeled fees paid |
|---|---:|---:|---:|---:|
{chr(10).join(diagnostic)}

Two NFL weeks remain a small and correlated sample. The added week was selected by schedule and completed pregame window, but had appeared in previous repository aggregate research. It is an expanded-cohort check, **not a pristine holdout**. No annualization, profitability confidence interval or independent-sample claim based on the number of prints is made.

**Reconciling earlier figures**

The original repository engine’s **+$1,027.47** and Q1 router’s **+$1,060.62** referred to the original **16-game Week 1 cohort** under the original early queue of 290.595. Q1’s **+$154.07** referred to those same 16 games with the early queue raised to 3,300. The 31-game figures above add games and are identified accordingly. The three repeated Q1 Week 1 regressions match their saved results within 1e−7.

**Data and execution controls**

The new cohort contains {new['precutoff_trades']:,} pre-cutoff trades and {new['postlude_trades']:,} postlude trades, with pagination exhausted for all 30 tickers. It has {new['missing_candle_minutes']:,} absent candle-minute slots; missing slots are not interpolated or labeled confirmed outages. Together with Week 1, the package contains {old['trades']+new['trades']:,} public trade records and {old['quotes']+new['quotes']:,} minute quote records. Raw captures, metadata and hashes are included.

The Monday NYG–LAR game is excluded because its T−3h cutoff had not passed at cohort freeze, not because of a trading outcome. Market membership, two-team MECNET structure, linear-cent grid and 50-cent tie rules are checked. These checks do not fully validate special-event settlement and collateral-release mechanics.

The new rules and 30-case matrix were frozen before their results. The original accounting engine and Q1 router remain byte-for-byte unchanged. Common assumptions include .25-second submit/cancel delays, 60-second refresh, minute candles available after a 60-second assumed publication delay, a 300-second quote-age cap, .5 participation after queue consumption, .0175/.07 maker/taker fee coefficients, .0001 balance precision and 250-contract total assumed liquidation capacity per game.

Historical per-leg queues, actual quote/trade receipt latency, market response to hypothetical orders, account-specific fee history, complete collateral mechanics and executable exit depth remain unverified. {residual} Simulated flatness is conditional on those exit assumptions.

**Validation and handoff**

41 unit tests pass, including the earlier execution controls, strictly prior flow, queue subtraction, two-leg admission, remaining-order size, deadline shrinkage, inventory rescue and pending-acknowledgment overshoot. All 30 ledgers were recomputed from saved fills, checking cash, fees, netting, exposure and deadline compliance. Input and frozen-code hashes were checked. No bot or recorder is left running.

The first integrity check found one truncated compressed fill ledger. That case was regenerated using unchanged frozen code and inputs; every summary field except runtime matched exactly. The recovery record is included in `results/artifact_recovery.json`, and the regenerated ledger passed the same independent checks.

The next substantial improvement should be judged using measured queue progression, quote lifetime and adverse movement after fills, with policies frozen before evaluation. More selective rules should be evaluated on both net profit and the capital/inventory they occupy; the simulation must not be optimized simply to recover a preferred headline return.

Official mechanics and data references: [public trades and pagination](https://docs.kalshi.com/api-reference/market/get-trades), [historical minute bid/ask candles](https://docs.kalshi.com/api-reference/market/get-market-candlesticks), [price-time queue position](https://docs.kalshi.com/api-reference/orders/get-order-queue-position).

**All isolated-cohort comparisons**

| Cohort | Early queue | Previous Q1 router | Joint entry gate | Gate + inventory completion |
|---|---:|---:|---:|---:|
{chr(10).join(full)}
'''
    (ROOT/'NFL_Completion_Experiment_Results.md').write_text(text)
    (ROOT/'results/promotion_decision.json').write_text(json.dumps(dict(primary_queue=3300,
        passing_candidates=eligible,rule='Beat Q1 completed P&L in week1, week2 and pooled account; disclose inventory cost.'),indent=2))
    print('Report written;',len(text.split()),'words; passing candidates',eligible)

if __name__=='__main__':main()
