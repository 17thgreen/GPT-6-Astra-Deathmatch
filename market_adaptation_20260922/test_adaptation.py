import copy
import unittest
from dataclasses import replace
from clock_policy import ClockRouter, ListingRouter, Config
from inputs import merge
from metrics import inventory_cost_hours

KO = 2_000_000


def markets():
    return {t:dict(event='G', direction=d, kickoff=KO, listed_at=KO-700000, verified_mecnet=True)
            for t,d in [('A',1),('B',-1)]}


def make(cutoff=180, profile='nfl'):
    return ClockRouter(markets(), replace(Config(),queue_early=3300,
        quote_source='candles',liquidation_lead_seconds=300),cutoff,profile)


def books(engine, at):
    for ticker in ('A','B'):
        engine.books[ticker]=dict(bid=.49,ask=.51,bid_at=at,ask_at=at)


class ClockTests(unittest.TestCase):
    def test_real_start_and_input_metadata_preserved(self):
        original=markets();saved=copy.deepcopy(original)
        r=ClockRouter(original,replace(Config(),quote_source='candles'),30)
        self.assertEqual(original,saved)
        self.assertEqual(r.markets['A']['actual_start'],KO)
        self.assertEqual(r.markets['A']['kickoff'],KO+9000)

    def test_opening_window_does_not_shift_with_internal_anchor(self):
        r=make(30);at=KO-604800;books(r,at)
        self.assertTrue(r.eligible('A',at))
        self.assertTrue(r.entry_open('G',at))
        self.assertFalse(r.eligible('A',at-1))

    def test_late_cutoff_opens_after_old_cutoff_but_before_new_winddown(self):
        old,new=make(),make(30)
        at=KO-3600
        books(old,at);books(new,at)
        self.assertFalse(old.eligible('A',at))
        self.assertTrue(new.eligible('A',at))
        self.assertFalse(new.eligible('A',KO-2100))

    def test_late_depth_transition_uses_real_start(self):
        r=make(30)
        self.assertEqual(r.queue('A',KO-43200),3300)
        self.assertEqual(r.queue('A',KO-43200+1),1327847.005)
        books(r,KO-39600)
        self.assertEqual(r.candidate('A','yes',KO-39600)['queue'],1327847.005)

    def test_constant_depth_used_in_candidate_and_submitted_order(self):
        r=make(30,'constant');at=KO-3600;books(r,at)
        self.assertEqual(r.candidate('A','yes',at)['queue'],3300)
        r.quote('A','yes',.49,250,at)
        self.assertEqual(r.orders['A','yes'].queue,3300)

    def test_incumbent_keeps_accumulated_priority(self):
        r=make(30,'constant');at=KO-3600;books(r,at)
        r.quote('A','yes',.49,250,at);r.orders['A','yes'].queue=123
        self.assertEqual(r.candidate('A','yes',at)['queue'],123)

    def test_winddown_clock_is_at_target_and_retries_until_target(self):
        r=make(30)
        times=[(x[0],x[3]) for x in r.clock]
        self.assertIn((KO-2100,'close'),times)
        self.assertIn((KO-2100-.25,'stop'),times)
        # No books: the open position forces all scheduled close retries.
        r.holdings['G']=1
        observed=[]
        original=r.flatten
        def record(event,at):
            observed.append(at);original(event,at)
        r.flatten=record
        r.advance(KO-1500)
        self.assertEqual(observed,list(range(KO-2100,KO-1800+1,60)))

    def test_old_profile_exact_synthetic_control(self):
        r=make();old=ListingRouter(markets(),r.cfg)
        at=KO-100000
        for engine in (r,old):
            for t in ('A','B'):
                engine.on_quote(dict(ticker=t,at=at,asof=at-60,bid=.49,ask=.51))
            for i in range(8):
                engine.on_trade(dict(ticker='A',at=at+i+1,yes_price=.49 if i%2 else .51,
                    taker_side='no' if i%2 else 'yes',size=10000,trade_id=str(i)))
            engine.finish(KO-10500)
        self.assertTrue(r.fills)
        self.assertEqual(r.fills,old.fills)
        self.assertEqual(r.order_records,old.order_records)

    def test_unfrozen_profile_rejected(self):
        with self.assertRaises(ValueError):make(60)


class MetricsTests(unittest.TestCase):
    def test_inventory_cost_hours_and_partial_pairing(self):
        fills=[dict(event='G',at=0,direction=1,size=10,price=.4,fee=1,inventory_after=10),
               dict(event='G',at=3600,direction=-1,size=4,price=.5,fee=0,inventory_after=6),
               dict(event='G',at=7200,direction=-1,size=6,price=.5,fee=0,inventory_after=0)]
        self.assertAlmostEqual(inventory_cost_hours(fills,9000)['total'],8)

    def test_conflicting_overlap_rejected(self):
        a=dict(at=0,ticker='A',trade_id='x',size=1)
        with self.assertRaises(ValueError):merge([a],[dict(a,size=2)])

    def test_identical_overlap_consumed_once(self):
        a=dict(at=0,ticker='A',trade_id='x',size=1)
        tape,overlaps=merge([a],[a.copy()])
        self.assertEqual(len(tape),1);self.assertEqual(overlaps,1)


if __name__=='__main__':unittest.main()
