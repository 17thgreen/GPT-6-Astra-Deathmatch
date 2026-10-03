"""Counterfactual queue policies layered on the unchanged research accounting engine.

No network or live order methods. Flow scores are heuristics, not fitted probabilities.
"""
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
import math
from replay_v2 import Replay


@dataclass(frozen=True)
class Policy:
    name: str = 'preserve'
    flow_window: float = 3600
    service_horizon: float = 600
    switch_ratio: float = 1.25
    pair_buffer: float = .001
    inside_race_queue: float = 0
    use_flow: bool = True

    def validate(self):
        if self.name not in ('preserve', 'churn60', 'route', 'improve_exit', 'combined'):
            raise ValueError('Unknown policy')
        if self.flow_window <= 0 or self.service_horizon <= 0 or self.switch_ratio < 1:
            raise ValueError('Invalid policy controls')
        if self.pair_buffer < 0 or self.inside_race_queue < 0:
            raise ValueError('Invalid policy controls')


class Flow:
    def __init__(self, window):
        self.window = window
        self.rows = defaultdict(deque)
        self.totals = defaultdict(lambda: defaultdict(float))

    def add(self, row):
        outcome = 'no' if row['taker_side'] == 'yes' else 'yes'
        key = (row['ticker'], outcome)
        price = round(row['yes_price'] if outcome == 'yes' else 1-row['yes_price'], 4)
        self.rows[key].append((row['at'], price, row['size']))
        self.totals[key][price] += row['size']

    def rate(self, key, price, now):
        rows = self.rows[key]; totals = self.totals[key]
        while rows and rows[0][0] < now-self.window:
            _, p, q = rows.popleft(); totals[p] -= q
            if abs(totals[p]) < 1e-7: totals.pop(p)
        volume = sum(q for p, q in totals.items() if p <= price+1e-9)
        # Earlier rows sharing this exact timestamp must not affect this decision.
        for at, p, q in reversed(rows):
            if at < now: break
            if p <= price+1e-9: volume -= q
        return max(0, volume) / self.window


class QueueReplay(Replay):
    def __init__(self, markets, config, policy=Policy()):
        policy.validate(); self.policy = policy
        self.flow = Flow(policy.flow_window)
        self.lots = defaultdict(deque)
        self.pair_durations = []
        self.inventory_area = defaultdict(float)
        self.inventory_clock = {}
        self.improved_ids = set()
        self.route_last = {}
        self._candidate_is_inside = False
        super().__init__(markets, config)

    def on_trade(self, row):
        super().on_trade(row)
        if not row.get('is_block_trade', False): self.flow.add(row)

    def queue(self, ticker, now):
        if self._candidate_is_inside: return self.policy.inside_race_queue
        return super().queue(ticker, now)

    def quote(self, ticker, outcome, price, wanted, now):
        key = (ticker, outcome); before = self.orders.get(key)
        identity = before.identity if before else None
        if before and abs(before.price-price) < 1e-9 and before.cancel_at is None:
            self.metrics['same_price_keep_decisions'] += 1
        super().quote(ticker, outcome, price, wanted, now)
        after = self.orders.get(key)
        if after and after.identity != identity and self._candidate_is_inside:
            self.improved_ids.add(after.identity)
            self.metrics['improved_orders'] += 1

    def account_fill(self, order, qty, now, kind, reason):
        event = self.event(order.ticker); previous = self.holdings[event]
        if event in self.inventory_clock:
            self.inventory_area[event] += abs(previous)*(now-self.inventory_clock[event])
        self.inventory_clock[event] = now
        super().account_fill(order, qty, now, kind, reason)
        f = self.fills[-1]
        f.update(order_id=order.identity, improved=order.identity in self.improved_ids,
                 resting_seconds=max(0, now-order.active_at), queue_remaining=order.queue)
        b = self.books.get(order.ticker)
        if b and self.book_valid(order.ticker, now):
            mid = (b['bid']+b['ask'])/2
            f['outcome_mid_at_fill'] = mid if order.outcome == 'yes' else 1-mid
        pending = qty; lots = self.lots[event]
        while pending > 1e-8 and lots and lots[0]['direction'] != order.direction:
            lot = lots[0]; paired = min(pending, lot['size'])
            self.pair_durations.append((now-lot['at'], paired))
            pending -= paired; lot['size'] -= paired
            if lot['size'] < 1e-8: lots.popleft()
        if pending > 1e-8:
            lots.append(dict(direction=order.direction, size=pending,
                             unit_cost=order.price+f['fee']/qty, at=now))
        if abs(sum(l['direction']*l['size'] for l in lots)-self.holdings[event]) > 1e-6:
            raise AssertionError('FIFO inventory reconciliation')
        if f['improved']:
            self.metrics['improved_filled_contracts'] += qty
            self.metrics['improved_paired_contracts'] += f['paired']

    def candidate(self, ticker, outcome, now):
        if not self.eligible(ticker, now): return None
        b = self.books[ticker]
        if not .05 <= (b['bid']+b['ask'])/2 <= .95: return None
        key = (ticker, outcome); old = self.orders.get(key)
        price = b['bid'] if outcome == 'yes' else 1-b['ask']
        queue = super().queue(ticker, now)
        wanted = min(self.cfg.order_size, queue) if queue > 0 else self.cfg.order_size
        inside = False; event = self.event(ticker); direction = self.direction(ticker, outcome)
        inventory = self.holdings[event]
        if self.policy.name in ('improve_exit', 'combined') and direction*inventory < -1e-8:
            if b['ask']-b['bid'] >= .02-1e-9:
                improved = round(price+.01, 4)
                opposite_ask = b['ask'] if outcome == 'yes' else 1-b['bid']
                offset_reserved = sum(o.remaining for o in self.orders.values()
                                      if self.event(o.ticker)==event and o.direction==direction
                                      and o is not old)
                available = max(0, abs(inventory)-offset_reserved)
                worst_entry = max((l['unit_cost'] for l in self.lots[event]), default=math.inf)
                # .0001 bounds six-decimal fee rounding per .01 minimum fill;
                # one precision unit/quantity conservatively bounds remaining account rounding.
                q = math.floor(min(wanted, available)*100+1e-8)/100
                cost = improved+self.cfg.maker_coefficient*improved*(1-improved)+.0001
                if (q >= .01 and improved < opposite_ask-1e-9 and
                    1-worst_entry-cost-float(self.cfg.balance_precision)/q >= self.policy.pair_buffer):
                    price = improved; wanted = q; inside = True; queue = self.policy.inside_race_queue
        if old and old.cancel_at is None and abs(old.price-price)<1e-9:
            queue = old.queue
        rate = self.flow.rate(key, price, now)
        cost = price+self.cfg.maker_coefficient*price*(1-price)
        service = min(1, rate*self.policy.service_horizon/(queue+wanted/self.cfg.fill_participation))
        return dict(key=key, direction=direction, price=price, wanted=wanted,
                    inside=inside, queue=queue, cost=cost, rate=rate, service=service)

    def choose(self, candidates):
        chosen = set()
        for direction in (-1, 1):
            same = [c for c in candidates if c['direction']==direction]
            other = [c for c in candidates if c['direction']==-direction]
            if not same or not other: continue
            offset = min(c['cost'] for c in other)
            for c in same:
                c['pair_margin'] = 1-c['cost']-offset
                c['score'] = max(0, c['pair_margin'])*(c['service'] if self.policy.use_flow else 1)
            same = [c for c in same if c['pair_margin']>0]
            if not same: continue
            best = min(same, key=lambda c:(-c['score'], c['cost'], c['key']))
            incumbents = [c for c in same if c['key'] in self.orders and
                          self.orders[c['key']].cancel_at is None]
            if incumbents:
                incumbent = min(incumbents, key=lambda c:(-c['score'], c['cost'], c['key']))
                if best['score'] <= self.policy.switch_ratio*incumbent['score']+1e-15:
                    best = incumbent
            chosen.add(best['key'])
        return chosen

    def refresh(self, event, now):
        if self.policy.name == 'preserve': return super().refresh(event, now)
        if self.policy.name == 'churn60':
            for o in list(self.orders.values()):
                if self.event(o.ticker)==event and now-o.active_at>=60:
                    if o.cancel_at is None: self.metrics['forced_refresh_cancels'] += 1
                    self.cancel(o, now, 'forced churn control')
            return super().refresh(event, now)
        candidates = []
        for ticker in sorted(self.groups[event]):
            for outcome in ('yes', 'no'):
                c = self.candidate(ticker, outcome, now)
                if c: candidates.append(c)
        chosen = self.choose(candidates) if self.policy.name in ('route','combined') else {c['key'] for c in candidates}
        for o in list(self.orders.values()):
            if self.event(o.ticker)==event and (o.ticker,o.outcome) not in chosen:
                self.cancel(o, now, 'route/eligibility')
        for c in candidates:
            if c['key'] not in chosen: continue
            route_key=(event,c['direction'])
            if self.policy.name in ('route','combined'):
                if route_key in self.route_last and self.route_last[route_key] != c['key']:
                    self.metrics['route_switch_decisions'] += 1
                self.route_last[route_key]=c['key']
            self._candidate_is_inside = c['inside']
            try: self.quote(*c['key'],c['price'],c['wanted'],now)
            finally: self._candidate_is_inside = False
        if any(self.eligible(t,now) for t in self.groups[event]):
            at=now+self.cfg.requote_seconds;self.scheduled[event]=at;self.push(at,3,'refresh',event)

    def finish(self, coverage_end):
        result = super().finish(coverage_end)
        for event, at in self.inventory_clock.items():
            end = min(coverage_end, self.markets[self.groups[event][0]]['kickoff']-10800)
            self.inventory_area[event] += abs(self.holdings[event])*max(0, end-at)
        ordered = sorted(self.pair_durations); total = sum(q for _,q in ordered)
        def quantile(fraction):
            accumulated=0
            for duration,q in ordered:
                accumulated+=q
                if accumulated>=total*fraction:return duration
            return None
        result['queue_policy']=asdict(self.policy)
        result['pair_holding_time_seconds'] = dict(paired_units=total,
            weighted_mean=sum(t*q for t,q in ordered)/total if total else None,
            weighted_median=quantile(.5), weighted_p90=quantile(.9))
        result['unhedged_contract_hours']=sum(self.inventory_area.values())/3600
        result['improved_unpaired_contracts']=self.metrics['improved_filled_contracts']-self.metrics['improved_paired_contracts']
        result['metrics']=dict(self.metrics)
        return result
