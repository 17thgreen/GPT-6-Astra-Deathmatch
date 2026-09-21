"""Entry-band and observed-stability experiments atop unchanged Q1/Q2 engines."""
import math
from collections import defaultdict
from completion_policy import CompletionReplay,projected_capacity

BANDS={'full':(168,3),'d7_d3':(168,72),'d3_d1':(72,24),'h24_h12':(24,12),'h12_h3':(12,3)}


class TimingReplay(CompletionReplay):
    def __init__(self,markets,config,band='full',variant='route'):
        if band not in BANDS or variant not in ('route','stable'):raise ValueError('Unknown policy')
        self.band=band;self.variant=variant;self.stability={};self.order_records={}
        super().__init__(markets,config,'q1_route' if variant=='route' else 'pair_complete')

    def entry_bounds(self,event):
        ko=self.markets[self.groups[event][0]]['kickoff'];start,end=BANDS[self.band]
        return ko-start*3600,min(ko-end*3600,ko-10800-self.cfg.liquidation_lead_seconds)

    def entry_open(self,event,now):
        if self.band=='full':
            # Eligibility in the unchanged engine supplies the original deadline.
            ko=self.markets[self.groups[event][0]]['kickoff']
            return ko-604800<=now and now+self.cfg.order_delay_seconds<ko-10800-self.cfg.liquidation_lead_seconds-self.cfg.cancel_delay_seconds
        start,end=self.entry_bounds(event)
        return start<=now and now+self.cfg.order_delay_seconds<end-self.cfg.cancel_delay_seconds

    def on_boundary(self,event,now):
        self.advance(now);self.refresh(event,now)

    def on_quote(self,row):
        if self.variant=='stable':
            # Process earlier timers before exposing the new observation.
            self.advance(row['at']);ticker=row['ticker'];old=self.stability.get(ticker)
            valid=0<row['bid']<row['ask']<1
            same=old and old['valid'] and valid and old['bid']==row['bid'] and old['ask']==row['ask'] and 0<=row['at']-old['last_at']<=180
            self.stability[ticker]=dict(valid=valid,bid=row['bid'],ask=row['ask'],last_at=row['at'],
                since=old['since'] if same else row['at'])
        return super().on_quote(row)

    def patience(self,ticker,now):
        state=self.stability.get(ticker)
        age=now-state['since'] if state and state['valid'] and 0<=now-state['last_at']<=180 else 0
        return min(1800,max(120,age))

    def candidates(self,event,now):
        candidates=super().candidates(event,now)
        if self.variant!='stable':return candidates
        for c in candidates:
            ticker=c['key'][0]
            end=self.markets[ticker]['kickoff']-10800-self.cfg.liquidation_lead_seconds
            if abs(self.holdings[event])<.01:end=min(end,self.entry_bounds(event)[1])
            horizon=max(0,min(self.patience(ticker,now),end-now-self.cfg.cancel_delay_seconds-self.cfg.order_delay_seconds))
            old=self.current_order(c);limit=min(c['wanted'],old.remaining) if old else c['wanted']
            c['capacity']=projected_capacity(c['rate'],c['queue'],horizon,self.cfg.fill_participation,limit)
            c['horizon']=horizon
        return candidates

    def refresh(self,event,now):
        if self.band=='full' or self.entry_open(event,now):return super().refresh(event,now)
        if abs(self.holdings[event])<.01:
            self.cancel_event(event,now,'outside entry band');return
        mode=self.mode
        try:
            self.mode='pair_complete'
            return super().refresh(event,now)
        finally:self.mode=mode

    def quote(self,ticker,outcome,price,wanted,now):
        key=(ticker,outcome);before=self.orders.get(key);identity=before.identity if before else None
        super().quote(ticker,outcome,price,wanted,now)
        after=self.orders.get(key)
        if after and after.identity!=identity:
            self.order_records[after.identity]=dict(order_id=after.identity,ticker=ticker,event=self.event(ticker),
                outcome=outcome,direction=after.direction,submitted_at=now,active_at=after.active_at,
                submitted_quantity=after.remaining,price=after.price,entry_window_open=self.entry_open(self.event(ticker),now),
                inventory_at_submission=self.holdings[self.event(ticker)],filled_quantity=0.,cancel_requested_at=None)

    def cancel(self,order,now,reason):
        if order.cancel_at is None and order.identity in self.order_records:
            self.order_records[order.identity]['cancel_requested_at']=now
        return super().cancel(order,now,reason)

    def account_fill(self,order,qty,now,kind,reason):
        super().account_fill(order,qty,now,kind,reason)
        if kind=='maker' and order.identity in self.order_records:
            self.order_records[order.identity]['filled_quantity']+=qty
        self.fills[-1]['entry_window_open']=self.entry_open(self.event(order.ticker),now)

    def match(self,row):
        count=len(self.fills);super().match(row)
        if self.band!='full' and len(self.fills)>count and not self.entry_open(self.event(row['ticker']),row['at']):
            self.refresh(self.event(row['ticker']),row['at'])

    def finish(self,end):
        result=super().finish(end)
        records=list(self.order_records.values());units=result['metrics'].get('paired_units',0)
        maker_pairs=sum(f['paired'] for f in self.fills if f['kind']=='maker')
        result.update(entry_band=self.band,variant=self.variant,
            passive_pairing_fraction=maker_pairs/units if units else None,
            submitted_maker_orders=len(records),fully_filled_submitted_orders=sum(r['filled_quantity']>=r['submitted_quantity']-.009 for r in records),
            never_filled_submitted_orders=sum(r['filled_quantity']<.01 for r in records),
            maker_exposure_added_outside_entry_window=sum(max(0,f['size']-f['paired']) for f in self.fills if f['kind']=='maker' and not f['entry_window_open']))
        return result
