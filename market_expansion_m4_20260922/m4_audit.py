"""M4 independent fixed-point audit adapted from preserved M2. No strategy import."""
import gzip
import json
from collections import defaultdict
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def close(a, b, tolerance=1e-6):
    if abs(a - b) > tolerance:
        raise AssertionError((a, b))


def rows(name, suffix):
    with gzip.open(ROOT / 'results' / f'{name}_{suffix}.jsonl.gz', 'rt') as stream:
        yield from (json.loads(line) for line in stream)


def verify(name, result, market_map):
    config = result['config']
    assert config['starting_cash'] == 5000
    assert config['order_size'] == config['exposure_cap'] and config['order_size'] in (25,100,250)
    assert config['assumed_exit_depth'] == 250
    orders = {o['order_id']: o for o in rows(name, 'orders')}
    inventory, cashflows, executed, exits = (defaultdict(float) for _ in range(4))
    remainders = defaultdict(Decimal)
    cash, count, maker, taker, fees, pairs = 5000., 0, 0., 0., 0., 0.
    last = float('-inf')
    for f in rows(name, 'fills'):
        count += 1
        assert f['at'] >= last and f['size'] > 0 and 0 < f['price'] < 1
        last = f['at']
        m, event = market_map[f['ticker']], f['event']
        assert m['event'] == event
        direction = m['direction'] * (1 if f['outcome'] == 'yes' else -1)
        assert direction == f['direction']
        paired = min(abs(inventory[event]), f['size']) if inventory[event] * direction < 0 else 0
        close(paired, f['paired'])
        p, q, precision = Decimal(str(f['price'])), Decimal(str(f['size'])), Decimal(config['balance_precision'])
        coefficient = Decimal(str(config['maker_coefficient'] if f['kind'] == 'maker' else config['taker_coefficient']))
        nominal = (coefficient * q * p * (1-p)).quantize(Decimal('.000001'), rounding=ROUND_CEILING)
        aligned = ((-p*q-nominal)/precision).to_integral_value(rounding=ROUND_FLOOR)*precision
        rounding = -p*q-nominal-aligned
        identity = f['order_id'] if f['kind'] == 'maker' else ('exit', count)
        remainder = remainders[identity] + rounding
        rebate = min((remainder/precision).to_integral_value(rounding=ROUND_FLOOR)*precision,
                     ((nominal+rounding)/precision).to_integral_value(rounding=ROUND_FLOOR)*precision)
        remainders[identity] = remainder - rebate
        close(float(nominal+rounding-rebate), f['fee'], 1e-8)
        delta = paired-f['size']*f['price']-f['fee']
        cash += delta
        cashflows[event] += delta
        inventory[event] += direction*f['size']
        fees += f['fee']
        pairs += paired
        close(cash, f['cash_after'])
        close(inventory[event], f['inventory_after'])
        assert cash >= -1e-7 and abs(inventory[event]) <= config['exposure_cap']+1e-6
        if f['kind'] == 'maker':
            o = orders[f['order_id']]
            maker += f['size']
            executed[f['order_id']] += f['size']
            assert max(o['active_at'], m['listed_at']) <= f['at'] < m['kickoff']-10800
            assert (f['ticker'], f['outcome'], f['price']) == (o['ticker'], o['outcome'], o['price'])
            if o['cancel_requested_at'] is not None:
                assert f['at'] < o['cancel_requested_at']+config['cancel_delay_seconds']+1e-8
        else:
            assert f['kind'] == 'taker'
            taker += f['size']
            exits[event] += f['size']
    residual = sum(abs(v) for v in inventory.values())
    close(residual, result['unresolved_contracts'])
    close(maker+taker-2*pairs, residual, 1e-5)
    close(maker, result['maker_contracts'], 1e-5)
    close(taker, result['taker_contracts'], 1e-5)
    close(fees, result['metrics'].get('fees', 0))
    assert count == result['fills'] and max(exits.values(), default=0) <= 250+1e-6
    assert result['all_flat'] == (residual < .009)
    if result['completed_strategy_pnl'] is None:
        assert residual >= .009
    else:
        assert residual < .009
        close(cash-5000, result['completed_strategy_pnl'])
    for g in result['per_game']:
        close(g['cashflow'], cashflows[g['event']])
        close(g['net_inventory'], inventory[g['event']])
    close(cash-5000, sum(result['sport_cashflows'].values()))
    for identity, o in orders.items():
        close(o['filled_quantity'], executed.pop(identity, 0))
        assert o['submitted_quantity'] <= config['order_size']+1e-8 and o['filled_quantity'] <= o['submitted_quantity']+1e-6
        assert o['submitted_at'] >= market_map[o['ticker']]['listed_at']
    assert not executed and len(orders) == result['submitted_maker_orders']
    return dict(scenario=name, passed=True, fills=count, orders=len(orders),
                completed_net=result['completed_strategy_pnl'], residual=residual)
