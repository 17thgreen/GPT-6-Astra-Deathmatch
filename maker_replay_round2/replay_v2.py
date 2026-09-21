"""Research replay with clock events and joint reservations; public-print quotes are proxies.

This is a counterfactual sensitivity model, not proof of actual executable historical fills.
No network or order-placement methods. Prices and queues inferred from prints remain assumptions.
"""
from dataclasses import dataclass, field, asdict
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR
from collections import defaultdict
import heapq, math


def dec(x):return Decimal(str(x))


@dataclass
class OrderFees:
    precision: Decimal = Decimal('0.0001')
    accumulator: Decimal = Decimal(0)

    def charge(self, price, quantity, coefficient):
        p=dec(price).quantize(Decimal('.0001'));q=dec(quantity).quantize(Decimal('.01'))
        if abs(p-dec(price))>Decimal('.00000001') or abs(q-dec(quantity))>Decimal('.00000001'):
            raise ValueError('Price/quantity outside supported fixed-point grid')
        revenue=-p*q
        fee=(dec(coefficient)*q*p*(1-p)).quantize(Decimal('.000001'),rounding=ROUND_CEILING)
        aligned=((revenue-fee)/self.precision).to_integral_value(rounding=ROUND_FLOOR)*self.precision
        rounding=revenue-fee-aligned
        self.accumulator+=rounding
        available=(self.accumulator/self.precision).to_integral_value(rounding=ROUND_FLOOR)*self.precision
        cap=((fee+rounding)/self.precision).to_integral_value(rounding=ROUND_FLOOR)*self.precision
        rebate=min(available,cap)
        self.accumulator-=rebate
        return float(fee+rounding-rebate)


@dataclass(frozen=True)
class Config:
    starting_cash: float=5000
    order_size: float=250
    exposure_cap: float=250
    queue_early: float=290.595
    queue_last12h: float=1327847.005
    fill_participation: float=.5
    requote_seconds: float=60
    proxy_max_age_seconds: float=300
    cancel_delay_seconds: float=.25
    order_delay_seconds: float=.25
    maker_coefficient: float=.0175
    taker_coefficient: float=.07
    balance_precision: str='.0001'
    assumed_exit_depth: float=250
    inventory_reduce_only: bool=False
    event_netting: bool=True
    quote_source: str='prints'
    liquidation_lead_seconds: float=0

    def validate(self):
        for k,v in asdict(self).items():
            if isinstance(v,(int,float)) and not isinstance(v,bool) and (not math.isfinite(v) or v<0):raise ValueError(k)
        if not 0<self.fill_participation<=1:raise ValueError('participation')
        if min(self.starting_cash,self.order_size,self.exposure_cap,self.requote_seconds,self.proxy_max_age_seconds)<=0:raise ValueError('positive controls required')
        if dec(self.balance_precision) not in (dec('.0001'),dec('.01')):raise ValueError('balance precision')
        if not self.event_netting:raise ValueError('This implementation requires verified two-team MECNET events')
        if self.quote_source not in ('prints','candles'):raise ValueError('Quote source')
        if self.liquidation_lead_seconds>=604800-10800:raise ValueError('Liquidation lead exceeds window')


@dataclass
class Order:
    identity: int
    ticker: str
    outcome: str
    direction: int
    price: float
    remaining: float
    queue: float
    active_at: float
    fees: OrderFees
    cancel_at: float|None=None
    resize_at: float|None=None


class Replay:
    def __init__(self,markets,config=Config()):
        """markets[ticker] contains event, direction (+1/-1), kickoff epoch and verified_mecnet.

        Opposite directions must represent complementary settlement payoffs. Metadata is validated
        by the input runner; the engine refuses events with any other structure.
        """
        config.validate();self.cfg=config;self.markets=markets
        groups=defaultdict(list)
        for ticker,m in markets.items():
            if m.get('verified_mecnet') is not True or m['direction'] not in (-1,1):raise ValueError('Unverified payoff map')
            if not math.isfinite(m['kickoff']):raise ValueError('Kickoff')
            groups[m['event']].append(ticker)
        for ts in groups.values():
            if len(ts)!=2 or {markets[t]['direction'] for t in ts}!={-1,1}:raise ValueError('Two complementary team tickers required')
            if len({markets[t]['kickoff'] for t in ts})!=1:raise ValueError('Conflicting kickoff')
        self.groups=dict(groups);self.cash=config.starting_cash;self.holdings=defaultdict(float)
        self.event_cashflow=defaultdict(float);self.books={};self.orders={};self.fills=[];self.actions=[]
        self.clock=[];self.serial=0;self.next_id=0;self.now=-math.inf;self.scheduled={}
        self.metrics=defaultdict(float);self.min_cash=self.cash;self.max_reserved=0.;self.max_exposure=0.
        self.closed=set();self.coverage_end=None;self.trade_count=0
        self.exit_remaining={event:config.assumed_exit_depth for event in self.groups}
        for event,ts in self.groups.items():
            cutoff=markets[ts[0]]['kickoff']-10800
            first_exit=cutoff-config.liquidation_lead_seconds
            self.push(first_exit-config.cancel_delay_seconds,0,'stop',event)
            self.push(first_exit,2,'close',event)

    def push(self,at,priority,kind,payload):
        self.serial+=1;heapq.heappush(self.clock,(at,priority,self.serial,kind,payload))

    def event(self,ticker):return self.markets[ticker]['event']
    def direction(self,ticker,outcome):return self.markets[ticker]['direction']*(1 if outcome=='yes' else -1)
    def queue(self,ticker,now):
        return self.cfg.queue_last12h if self.markets[ticker]['kickoff']-now<43200 else self.cfg.queue_early

    def book_valid(self,ticker,now):
        b=self.books.get(ticker,{})
        if not all(k in b for k in ('bid','ask','bid_at','ask_at')):return False
        return (0<b['bid']<b['ask']<1 and 0<=now-b['bid_at']<self.cfg.proxy_max_age_seconds
                and 0<=now-b['ask_at']<self.cfg.proxy_max_age_seconds)

    def eligible(self,ticker,now):
        k=self.markets[ticker]['kickoff']
        return (k-604800<=now and now+self.cfg.order_delay_seconds<k-10800-self.cfg.liquidation_lead_seconds-self.cfg.cancel_delay_seconds
                and self.event(ticker) not in self.closed and self.book_valid(ticker,now))

    def reserve_cost(self,order):
        # Extra .0001/contract bounds six-decimal fee rounding for .01-contract minimum fills.
        # One balance-precision unit bounds the order's outstanding balance-rounding remainder.
        p=order.price
        return order.remaining*(p+self.cfg.maker_coefficient*p*(1-p)+.0001)+float(dec(self.cfg.balance_precision))

    def reservations(self,event=None,exclude=None):
        orders=[o for o in self.orders.values() if o.identity!=exclude and (event is None or self.event(o.ticker)==event)]
        cash=sum(self.reserve_cost(o) for o in orders)
        if event is None:return cash
        pos=self.holdings[event]
        return pos-sum(o.remaining for o in orders if o.direction<0),pos+sum(o.remaining for o in orders if o.direction>0)

    def assert_limits(self):
        reserved=self.reservations();self.max_reserved=max(self.max_reserved,reserved)
        self.min_cash=min(self.min_cash,self.cash)
        if self.cash<-1e-7 or reserved>self.cash+1e-6:raise AssertionError(('cash reservation',self.cash,reserved))
        for ev in self.groups:
            lo,hi=self.reservations(ev);self.max_exposure=max(self.max_exposure,abs(self.holdings[ev]))
            if lo < -self.cfg.exposure_cap-1e-6 or hi>self.cfg.exposure_cap+1e-6:raise AssertionError(('exposure',ev,lo,hi))

    def cancel(self,order,now,reason):
        if order.cancel_at is not None:return
        order.cancel_at=now+self.cfg.cancel_delay_seconds
        self.push(order.cancel_at,1,'cancel',order.identity)
        self.metrics['cancel_requests']+=1

    def cancel_event(self,event,now,reason):
        for o in list(self.orders.values()):
            if self.event(o.ticker)==event:self.cancel(o,now,reason)

    def quote(self,ticker,outcome,price,wanted,now):
        price=round(price,4)
        key=(ticker,outcome);old=self.orders.get(key)
        if old and old.cancel_at is not None:return
        if old and abs(old.price-price)>1e-9:
            self.cancel(old,now,'price change');return
        if old:
            wanted=min(old.remaining,wanted) # No free priority for increasing an existing order.
            if wanted<old.remaining-1e-8 and old.resize_at is None:
                old.resize_at=now+self.cfg.cancel_delay_seconds
                self.push(old.resize_at,1,'resize',(old.identity,wanted))
            return
        if wanted<=0:return
        ev=self.event(ticker);direction=self.direction(ticker,outcome);lo,hi=self.reservations(ev)
        room=self.cfg.exposure_cap-hi if direction>0 else lo+self.cfg.exposure_cap
        budget=max(0,self.cash-self.reservations()-float(dec(self.cfg.balance_precision)))
        cost=price+self.cfg.maker_coefficient*price*(1-price)+.0001
        quantity=math.floor(max(0,min(wanted,room,budget/cost))*100+1e-8)/100
        if quantity<.01:return
        self.next_id+=1
        self.orders[key]=Order(self.next_id,ticker,outcome,direction,price,quantity,self.queue(ticker,now),
                               now+self.cfg.order_delay_seconds,OrderFees(dec(self.cfg.balance_precision)))
        self.metrics['new_orders']+=1;self.assert_limits()

    def refresh(self,event,now):
        for ticker in sorted(self.groups[event]):
            eligible=self.eligible(ticker,now)
            b=self.books.get(ticker,{})
            if eligible and not .05<=(b['bid']+b['ask'])/2<=.95:eligible=False
            for outcome in ('yes','no'):
                old=self.orders.get((ticker,outcome));d=self.direction(ticker,outcome)
                allow=eligible and not (self.cfg.inventory_reduce_only and d*self.holdings[event]>1e-8)
                if not allow:
                    if old:self.cancel(old,now,'eligibility/inventory')
                    continue
                price=b['bid'] if outcome=='yes' else 1-b['ask']
                wanted=min(self.cfg.order_size,self.queue(ticker,now)) if self.queue(ticker,now)>0 else self.cfg.order_size
                self.quote(ticker,outcome,price,wanted,now)
        if any(self.eligible(t,now) for t in self.groups[event]):
            at=now+self.cfg.requote_seconds
            self.scheduled[event]=at;self.push(at,3,'refresh',event)

    def account_fill(self,order,qty,now,kind,reason):
        coefficient=self.cfg.maker_coefficient if kind=='maker' else self.cfg.taker_coefficient
        fee=order.fees.charge(order.price,qty,coefficient)
        ev=self.event(order.ticker);previous=self.holdings[ev]
        paired=min(abs(previous),qty) if previous*order.direction<0 else 0
        cash_change=-qty*order.price-fee+paired
        self.cash+=cash_change;self.event_cashflow[ev]+=cash_change
        self.holdings[ev]+=order.direction*qty
        if abs(self.holdings[ev])<1e-8:self.holdings[ev]=0.
        self.fills.append({'at':now,'ticker':order.ticker,'event':ev,'outcome':order.outcome,'direction':order.direction,
                          'price':order.price,'size':qty,'fee':fee,'kind':kind,'paired':paired,'reason':reason,
                          'inventory_after':self.holdings[ev],'cash_after':self.cash})
        self.metrics['fees']+=fee;self.metrics['paired_units']+=paired

    def match(self,row):
        key=(row['ticker'],'no' if row['taker_side']=='yes' else 'yes');o=self.orders.get(key)
        if o is None or row['at']<o.active_at:return
        px=1-row['yes_price'] if o.outcome=='no' else row['yes_price']
        if px>o.price+1e-9:return
        volume=row['size'];consumed=min(o.queue,volume);o.queue-=consumed;volume-=consumed
        qty=math.floor(min(o.remaining,volume*self.cfg.fill_participation)*100+1e-8)/100
        if qty<.01:return
        o.remaining=round(o.remaining-qty,8)
        if o.remaining<.01:self.orders.pop(key)
        self.account_fill(o,qty,row['at'],'maker','public tape hypothetical match')
        if o.cancel_at is not None:self.metrics['fills_while_cancel_pending']+=1
        self.assert_limits()
        if self.cfg.inventory_reduce_only:
            for other in list(self.orders.values()):
                if self.event(other.ticker)==self.event(o.ticker) and other.direction*self.holdings[self.event(o.ticker)]>0:
                    self.cancel(other,row['at'],'inventory increased')

    def flatten(self,event,now):
        # Each close event attempts a sweep, with one cumulative game depth budget across retries.
        # Unknown depth is an explicit sensitivity input, never inferred from print count.
        inventory=self.holdings[event]
        if abs(inventory)<.01:return
        wanted_direction=-1 if inventory>0 else 1;candidates=[]
        for ticker in self.groups[event]:
            if not self.book_valid(ticker,now):continue
            outcome='yes' if self.direction(ticker,'yes')==wanted_direction else 'no'
            b=self.books[ticker];price=b['ask'] if outcome=='yes' else 1-b['bid']
            candidates.append((price,ticker,outcome))
        # Cross-ticker liquidity may be linked. Treat the depth as a TOTAL game budget.
        remaining_depth=self.exit_remaining[event]
        for price,ticker,outcome in sorted(candidates):
            quantity=min(abs(self.holdings[event]),remaining_depth)
            if quantity<.01:break
            order=Order(-1,ticker,outcome,wanted_direction,price,quantity,0,now,OrderFees(dec(self.cfg.balance_precision)))
            self.account_fill(order,quantity,now,'taker','assumed-depth exit at fresh print-derived proxy')
            remaining_depth-=quantity
        self.exit_remaining[event]=remaining_depth
        if abs(self.holdings[event])>.009:self.metrics['unresolved_exit_attempts']+=1
        self.assert_limits()

    def advance(self,now):
        if now<self.now:raise ValueError('Time reversal')
        while self.clock and self.clock[0][0]<=now:
            at,_,_,kind,payload=heapq.heappop(self.clock)
            if kind=='stop':
                self.closed.add(payload);self.cancel_event(payload,at,'cutoff lead time')
            elif kind in ('cancel','resize'):
                identity=payload if kind=='cancel' else payload[0]
                for key,o in list(self.orders.items()):
                    if o.identity!=identity:continue
                    if kind=='cancel':self.orders.pop(key);self.metrics['cancels_acknowledged']+=1
                    else:
                        o.remaining=min(o.remaining,payload[1]);o.resize_at=None
                        if o.remaining<.01:self.orders.pop(key)
                    break
            elif kind=='close':
                self.flatten(payload,at)
                cutoff=self.markets[self.groups[payload][0]]['kickoff']-10800
                if at<cutoff and abs(self.holdings[payload])>=.01:
                    self.push(min(at+60,cutoff),2,'close',payload)
            elif kind=='stale':
                ticker=payload
                if not self.book_valid(ticker,at):
                    for key,o in list(self.orders.items()):
                        if o.ticker==ticker:self.cancel(o,at,'stale proxy')
            elif kind=='refresh':
                if self.scheduled.get(payload)==at:
                    self.scheduled.pop(payload);self.refresh(payload,at)
        self.now=now

    def on_trade(self,row):
        if row.get('is_block_trade',False):return
        if row['ticker'] not in self.markets:raise ValueError('Unmapped market')
        if not all(math.isfinite(row[k]) for k in ('at','yes_price','size')):raise ValueError('Nonfinite trade')
        if not 0<row['yes_price']<1 or row['size']<=0 or row['taker_side'] not in ('yes','no'):raise ValueError('Invalid trade')
        now=row['at'];self.advance(now);self.trade_count+=1
        self.match(row)
        if self.cfg.quote_source=='candles':return
        ticker=row['ticker'];b=self.books.setdefault(ticker,{})
        side='ask' if row['taker_side']=='yes' else 'bid';b[side]=row['yes_price'];b[side+'_at']=now
        self.push(now+self.cfg.proxy_max_age_seconds,2,'stale',ticker)
        event=self.event(ticker)
        if not self.book_valid(ticker,now):
            for o in list(self.orders.values()):
                if o.ticker==ticker:self.cancel(o,now,'invalid proxy')
        if event not in self.scheduled:self.refresh(event,now)

    def on_quote(self,row):
        if self.cfg.quote_source!='candles':raise ValueError('External quotes not enabled')
        now=row['at'];asof=row['asof']
        if asof>now:raise ValueError('Future quote')
        if row['ticker'] not in self.markets:raise ValueError('Unknown quote ticker')
        if not all(math.isfinite(row[k]) for k in ('at','asof','bid','ask')):raise ValueError('Invalid quote')
        self.advance(now)
        ticker=row['ticker'];self.books[ticker]=dict(bid=row['bid'],ask=row['ask'],bid_at=asof,ask_at=asof)
        if asof+self.cfg.proxy_max_age_seconds>now:self.push(asof+self.cfg.proxy_max_age_seconds,2,'stale',ticker)
        self.refresh(self.event(ticker),now)

    def finish(self,coverage_end):
        self.advance(coverage_end);self.coverage_end=coverage_end
        per_game=[]
        for event,ts in self.groups.items():
            cutoff=self.markets[ts[0]]['kickoff']-10800
            net=self.holdings[event];flow=self.event_cashflow[event]
            per_game.append({'event':event,'window_complete':coverage_end>=cutoff,'net_inventory':net,
                             'cashflow':flow,'pnl_lower_payout_bound':flow,'pnl_upper_payout_bound':flow+abs(net),
                             'flat':abs(net)<.009})
        unresolved=sum(abs(v) for v in self.holdings.values())
        cashflow=self.cash-self.cfg.starting_cash
        complete=all(g['window_complete'] for g in per_game)
        all_flat=unresolved<.009
        self.metrics['events_with_unresolved_exit']=sum(g['window_complete'] and not g['flat'] for g in per_game)
        return {'evidence':'EXPLORATORY_PUBLIC_PRINT_REPLAY_NOT_EXECUTION_VALIDATION','config':asdict(self.cfg),
                'trades':self.trade_count,'fills':len(self.fills),'maker_contracts':sum(f['size'] for f in self.fills if f['kind']=='maker'),
                'taker_contracts':sum(f['size'] for f in self.fills if f['kind']=='taker'),
                'completed_window_games':sum(g['window_complete'] for g in per_game),'all_flat':all_flat,
                'completed_strategy_pnl':cashflow if complete and all_flat else None,
                'terminal_payout_bounds':[cashflow,cashflow+unresolved],
                'bound_note':'Bounds value unresolved binary payouts in [0,1], before any future exit fees; not mark-to-market or confidence intervals.',
                'unresolved_contracts':unresolved,'min_cash':self.min_cash,'max_reserved_cash':self.max_reserved,
                'max_abs_event_exposure':self.max_exposure,'metrics':dict(self.metrics),'per_game':per_game}
