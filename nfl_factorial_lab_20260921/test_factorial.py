import unittest
from dataclasses import replace
from factorial_policy import Factors,FactorialReplay
from adaptive_policy import AdaptiveReplay
from replay_v2 import Config
from test_adaptive import AT,KO,cs,position
from test_replay_v2 import markets

def engine(bits):
    r=FactorialReplay(markets(KO),replace(Config(),quote_source='candles',queue_early=100,
        queue_last12h=100,liquidation_lead_seconds=300),Factors(*(x=='1' for x in bits)))
    for t in ('A','B'):r.books[t]=dict(bid=.49,ask=.51,bid_at=AT,ask_at=AT)
    return r

def with_rates(r,rate=1):
    candidates=cs(r)
    for c in candidates:c['rate']=rate
    return candidates

class FactorialTests(unittest.TestCase):
    def test_all_eight_labels_unique(self):
        self.assertEqual(len({Factors(bool(f),bool(p),bool(r)).label for f in [0,1] for p in [0,1] for r in [0,1]}),8)
    def test_factor_type_checked(self):
        with self.assertRaises(ValueError):Factors(flow=1)
    def test_gate_on_rejects_zero_flow(self):
        r=engine('111');self.assertIsNone(r.portfolio_rank(cs(r),AT))
    def test_gate_off_admits_zero_flow_without_invention(self):
        r=engine('011');rank=r.portfolio_rank(cs(r),AT)
        self.assertIsNotNone(rank);self.assertEqual(rank['score'],0);self.assertIsNone(rank['wait_seconds'])
    def test_gate_off_neutral_rank_still_admits(self):
        r=engine('000');rank=r.portfolio_rank(cs(r),AT)
        self.assertEqual(rank['adjusted'],1);self.assertFalse(rank['has_observed_flow'])
    def test_gate_off_does_not_remove_margin_guard(self):
        r=engine('000');c=with_rates(r)
        for row in c:row['cost']=.51
        self.assertIsNone(r.portfolio_rank(c,AT))
    def test_all_on_rank_matches_q5(self):
        r=engine('111');old=AdaptiveReplay(r.markets,r.cfg,'allocation');old.books=r.books.copy()
        a=r.portfolio_rank(with_rates(r),AT);b=old.portfolio_rank(with_rates(old),AT)
        self.assertTrue(a.pop('has_observed_flow'));self.assertEqual(a,b)
    def test_neutral_only_changes_adjusted_score(self):
        a=engine('111');b=engine('110');ra=a.portfolio_rank(with_rates(a),AT);rb=b.portfolio_rank(with_rates(b),AT)
        self.assertEqual(rb['adjusted'],1);ra.pop('adjusted');rb.pop('adjusted');self.assertEqual(ra,rb)
    def test_protection_switch_only_changes_budget_holdback(self):
        a=engine('111');b=engine('101')
        for r in (a,b):
            position(r,25)
            for t in ('A','B'):
                for side in ('yes','no'):r.flow.add(dict(ticker=t,at=AT-1,yes_price=.49 if side=='no' else .51,size=10000,taker_side=side))
            r.rebalance(AT)
        da=a.decisions[-1];db=b.decisions[-1]
        self.assertEqual(da['ranks'],db['ranks']);self.assertEqual(da['offset_cash_need'],db['offset_cash_need'])
        self.assertGreater(da['protected'],0);self.assertEqual(db['protected'],0)
    def test_protection_off_still_preserves_offset_quote_safety(self):
        r=engine('100');position(r,25);r.refresh('G',AT)
        self.assertTrue(r.orders);self.assertTrue(all(o.direction<0 for o in r.orders.values()))
    def test_all_off_is_not_original_router(self):
        r=engine('000');r.refresh('G',AT)
        self.assertEqual(r.metrics['portfolio_rebalances'],1);self.assertIn('G',r.allocations)
    def test_budget_sum_does_not_exceed_available_cash(self):
        for bits in ['000','010','100','110','001','011','101','111']:
            r=engine(bits);r.cash=100;position(r,25);r.rebalance(AT);d=r.decisions[-1]
            self.assertLessEqual(sum(d['allocations'].values()),max(0,r.cash-d['protected'])+1e-8)
    def test_pending_cancel_cash_is_not_released_by_switch(self):
        r=engine('000');r.quote('A','yes',.49,100,AT);o=r.orders['A','yes'];reserved=r.reservations()
        r.cancel(o,AT,'test');r.rebalance(AT)
        self.assertEqual(r.reservations(),reserved);r.advance(AT+.25);self.assertEqual(r.reservations(),0)
    def test_rebalance_does_not_run_early(self):
        r=engine('000');r.rebalance(AT);r.rebalance(AT+599)
        self.assertEqual(len(r.decisions),1);r.rebalance(AT+600);self.assertEqual(len(r.decisions),2)
    def test_gate_excludes_same_timestamp_flow(self):
        r=engine('111')
        for t in ('A','B'):
            for side in ('yes','no'):r.flow.add(dict(ticker=t,at=AT,yes_price=.49 if side=='no' else .51,size=10000,taker_side=side))
        self.assertIsNone(r.portfolio_rank(cs(r),AT))
    def test_new_quote_not_visible_to_prior_allocation_timer(self):
        r=engine('000');seen=[];original=r.refresh
        def observe(event,now):
            if now==AT+60:seen.append(r.books['A']['bid'])
            return original(event,now)
        r.refresh=observe;r.scheduled['G']=AT+60;r.push(AT+60,3,'refresh','G')
        r.on_quote(dict(ticker='A',at=AT+120,asof=AT+60,bid=.40,ask=.42))
        self.assertEqual(seen,[.49])

if __name__=='__main__':unittest.main()
