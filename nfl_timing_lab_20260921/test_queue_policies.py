import unittest
from dataclasses import replace
from queue_policies import QueueReplay, Policy, Flow
from replay_v2 import Config, Order, OrderFees
from test_replay_v2 import markets, trade

def engine(name='preserve', **policy):
    r=QueueReplay(markets(100000),replace(Config(),quote_source='candles',queue_early=100,queue_last12h=100),Policy(name=name,**policy))
    for t in ('A','B'):r.books[t]=dict(bid=.49,ask=.51,bid_at=100,ask_at=100)
    return r

def entry(r,size=50,price=.40):
    o=Order(999,'A','yes',1,price,size,0,99,OrderFees())
    r.account_fill(o,size,100,'maker','test entry')

class QueueTests(unittest.TestCase):
    def test_keep_price_retains_identity_and_consumed_queue(self):
        r=engine();r.refresh('G',100);old=r.orders['A','yes'];old.queue=7
        r.refresh('G',110)
        self.assertIs(r.orders['A','yes'],old);self.assertEqual(old.queue,7)

    def test_churn_requests_cancel_without_freeing_reservations(self):
        r=engine('churn60');r.refresh('G',100);reserved=r.reservations()
        r.refresh('G',161)
        self.assertTrue(all(o.cancel_at is not None for o in r.orders.values()))
        self.assertEqual(r.reservations(),reserved)
        r.advance(161.25);self.assertFalse(r.orders)

    def test_strictly_prior_eligible_flow_only(self):
        f=Flow(60)
        f.add(trade(100,'no',.49,60));f.add(trade(101,'no',.50,120));f.add(trade(101,'yes',.49,999))
        self.assertEqual(f.rate(('A','yes'),.49,101),1)
        self.assertEqual(f.rate(('A','yes'),.50,101),1)
        self.assertEqual(f.rate(('A','yes'),.50,102),3)
        self.assertEqual(f.rate(('A','yes'),.50,162),0)

    def test_route_favors_service_with_equal_price_and_margin(self):
        r=engine('route')
        r.flow.add(trade(99,'yes',.51,3600,ticker='B'))
        cs=[r.candidate(t,o,100) for t in ('A','B') for o in ('yes','no')]
        self.assertIn(('B','no'),r.choose(cs))

    def test_challenger_does_not_cancel_good_incumbent_for_tiny_gain(self):
        r=engine('route');r.quote('A','yes',.49,100,90)
        r.orders['A','yes'].queue=0
        r.flow.add(trade(99,'no',.49,3600,ticker='A'))
        r.flow.add(trade(99,'yes',.51,3610,ticker='B'))
        cs=[r.candidate(t,o,100) for t in ('A','B') for o in ('yes','no')]
        self.assertIn(('A','yes'),r.choose(cs))

    def test_switch_keeps_pending_risk_reserved(self):
        r=engine('route');r.quote('A','yes',.49,250,90)
        r.flow.add(trade(99,'yes',.51,36000,ticker='B'))
        r.refresh('G',100)
        self.assertIsNotNone(r.orders['A','yes'].cancel_at)
        self.assertNotIn(('B','no'),r.orders)
        r.assert_limits()

    def test_improvement_requires_inventory_and_pair_margin(self):
        r=engine('improve_exit');c=r.candidate('A','no',100)
        self.assertFalse(c['inside'])
        entry(r,price=.50);c=r.candidate('A','no',100)
        self.assertFalse(c['inside'])
        r=engine('improve_exit');entry(r,price=.40);c=r.candidate('A','no',100)
        self.assertTrue(c['inside']);self.assertAlmostEqual(c['price'],.50)
        self.assertEqual(c['wanted'],50)

    def test_one_tick_spread_never_crossed(self):
        r=engine('improve_exit');entry(r);r.books['A']['ask']=.50
        self.assertFalse(r.candidate('A','no',100)['inside'])

    def test_inside_race_queue_applies_only_to_new_improvement(self):
        r=engine('improve_exit',inside_race_queue=250);entry(r);r.refresh('G',100)
        o=r.orders['A','no'];self.assertEqual(o.queue,250)
        o.queue=3;r.refresh('G',101);self.assertEqual(o.queue,3)
        self.assertEqual(r.queue('B',101),100)

    def test_other_offset_orders_reduce_improvement_quantity(self):
        r=engine('improve_exit');entry(r)
        r.quote('B','yes',.49,45,99)
        self.assertEqual(r.candidate('A','no',100)['wanted'],5)

    def test_fifo_matching_cost_and_duration(self):
        r=engine();entry(r,size=50)
        o=Order(998,'B','yes',-1,.50,20,0,100,OrderFees())
        r.account_fill(o,20,110,'maker','test offset')
        self.assertEqual(r.lots['G'][0]['size'],30)
        self.assertEqual(r.pair_durations,[(10,20)])
        self.assertEqual(r.inventory_area['G'],500)

    def test_worst_remaining_lot_controls_improvement_gate(self):
        r=engine('improve_exit');entry(r,size=10,price=.40);entry(r,size=10,price=.55)
        self.assertFalse(r.candidate('A','no',100)['inside'])

if __name__=='__main__':unittest.main()
