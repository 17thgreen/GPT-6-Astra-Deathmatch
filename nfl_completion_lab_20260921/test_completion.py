import unittest
from dataclasses import replace
from completion_policy import CompletionReplay,projected_capacity
from replay_v2 import Config
from test_replay_v2 import markets,trade
from test_queue_policies import entry

def engine(mode='pair_gate',kickoff=100000):
    r=CompletionReplay(markets(kickoff),replace(Config(),quote_source='candles',
        queue_early=100,queue_last12h=100,liquidation_lead_seconds=300),mode)
    for t in ('A','B'):r.books[t]=dict(bid=.49,ask=.51,bid_at=100,ask_at=100)
    return r

def flow(r,ticker='A',both=True):
    r.flow.add(trade(99,'no',.49,100000,ticker))
    if both:r.flow.add(trade(99,'yes',.51,100000,ticker))

class CompletionTests(unittest.TestCase):
    def test_queue_must_clear_before_service_starts(self):
        self.assertEqual(projected_capacity(10,600,60,.5,250),0)
        self.assertEqual(projected_capacity(10,500,60,.5,250),50)
        self.assertEqual(projected_capacity(10,0,60,.5,250),250)

    def test_capacity_respects_fractional_grid_and_deadline(self):
        self.assertEqual(projected_capacity(1,0,.019,.5,250),0)
        self.assertEqual(projected_capacity(1,0,.021,.5,250),.01)
        self.assertEqual(projected_capacity(100,0,0,.5,250),0)
        with self.assertRaises(ValueError):projected_capacity(float('nan'),0,1,.5,250)

    def test_fast_first_leg_cannot_admit_unserviceable_pair(self):
        r=engine();flow(r,both=False)
        self.assertIsNone(r.choose_pair(r.candidates('G',100)))
        r.refresh('G',100);self.assertFalse(r.orders)

    def test_both_legs_and_fees_required(self):
        r=engine();flow(r)
        pair=r.choose_pair(r.candidates('G',100));self.assertIsNotNone(pair)
        r.books['A']['bid']=.505;r.books['A']['ask']=.506
        r.books['B']['bid']=.494;r.books['B']['ask']=.495
        flow(r,'B')
        self.assertIsNone(r.choose_pair(r.candidates('G',100)))

    def test_incumbent_remaining_quantity_cannot_get_free_priority(self):
        r=engine();flow(r);r.refresh('G',100)
        for o in r.orders.values():o.remaining=3
        pair=r.choose_pair(r.candidates('G',101));self.assertEqual(pair['size'],3)

    def test_ten_minute_horizon_shrinks_near_stop(self):
        r=engine(kickoff=20000);flow(r)
        for b in r.books.values():b['bid_at']=8899;b['ask_at']=8899
        cs=r.candidates('G',8899)
        self.assertTrue(cs);self.assertAlmostEqual(cs[0]['horizon'],.5)
        self.assertTrue(all(c['capacity']==0 for c in cs))

    def test_failed_entry_gate_does_not_abandon_inventory(self):
        r=engine();entry(r,size=50)
        r.refresh('G',100)
        self.assertTrue(r.orders)
        self.assertTrue(all(o.direction==-1 for o in r.orders.values()))
        self.assertLessEqual(sum(o.remaining for o in r.orders.values()),50)

    def test_completion_cancels_same_direction_after_first_fill(self):
        r=engine('pair_complete');flow(r);r.refresh('G',100)
        r.on_trade(trade(101,'no',.49,200))
        self.assertEqual(r.holdings['G'],50)
        self.assertAlmostEqual(r.orders['A','yes'].cancel_at,101.25)
        self.assertAlmostEqual(r.orders['A','no'].resize_at,101.25)
        r.assert_limits()

    def test_pending_resize_race_is_counted_not_silently_clipped(self):
        r=engine('pair_complete');flow(r);r.refresh('G',100)
        r.on_trade(trade(101,'no',.49,200))
        r.on_trade(trade(101.1,'yes',.51,500))
        self.assertEqual(r.holdings['G'],-50)
        self.assertEqual(r.metrics['completion_overshoot_contracts'],50)
        r.assert_limits()

    def test_pending_offset_reservation_prevents_double_hedge(self):
        r=engine();entry(r,size=50)
        r.quote('B','yes',.49,45,99);r.cancel(r.orders['B','yes'],100,'test')
        r.refresh('G',100)
        self.assertLessEqual(r.orders['A','no'].remaining,5)
        r.assert_limits()

if __name__=='__main__':unittest.main()
