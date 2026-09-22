"""Descriptive efficiency metrics; none is an annualized compounding forecast."""
from collections import defaultdict, deque


def inventory_cost_hours(fills, end):
    lots = defaultdict(deque)
    last, area = {}, defaultdict(float)
    for f in fills:
        event, now = f['event'], f['at']
        if event in last:
            if now < last[event]:
                raise ValueError('Time reversal')
            area[event] += sum(q['size']*q['cost'] for q in lots[event])*(now-last[event])/3600
        last[event] = now
        remaining = f['size']
        queue = lots[event]
        while remaining > 1e-8 and queue and queue[0]['direction'] != f['direction']:
            qty = min(remaining, queue[0]['size'])
            remaining -= qty
            queue[0]['size'] -= qty
            if queue[0]['size'] < 1e-8:
                queue.popleft()
        if remaining > 1e-8:
            queue.append(dict(size=remaining, cost=f['price']+f['fee']/f['size'], direction=f['direction']))
        if abs(sum(q['size']*q['direction'] for q in queue)-f['inventory_after']) > 1e-6:
            raise ValueError('FIFO inventory does not reconcile')
    for event, queue in lots.items():
        area[event] += sum(q['size']*q['cost'] for q in queue)*max(0,end-last[event])/3600
    return dict(total=sum(area.values()), per_event=dict(area),
                definition='FIFO inventory acquisition cost including entry fees; excludes resting-order reservations')


def efficiencies(result, calendar_days=None):
    net = result['completed_strategy_pnl']
    volume = result['maker_contracts']+result['taker_contracts']
    cash = result['config']['starting_cash']
    return dict(net_per_1000_initial_cash=net/cash*1000 if net is not None else None,
        net_per_1000_filled_contracts=net/volume*1000 if net is not None and volume else None,
        net_per_game=net/len(result['per_game']) if net is not None else None,
        return_on_initial_cash_pct=net/cash*100 if net is not None else None,
        calendar_days=calendar_days,
        observed_net_per_1000_initial_cash_per_day=net/cash*1000/calendar_days
            if net is not None and calendar_days and calendar_days > 0 else None)
