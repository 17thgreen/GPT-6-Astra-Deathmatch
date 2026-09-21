import copy
import inspect
import unittest
from dataclasses import replace
from pair_policy import GuardedRouter, PairAllocator, chosen_margin, make_engine
from factorial_policy import FactorialReplay, Factors
from adaptive_policy import AdaptiveReplay
from replay_v2 import Config
from test_replay_v2 import markets
from test_adaptive import AT, KO, position


def engine(arm):
    r=make_engine(markets(KO), replace(Config(), quote_source='candles', queue_early=100,
                  queue_last12h=100, liquidation_lead_seconds=300), arm)
    for t in ('A','B'):r.books[t]=dict(bid=.49,ask=.51,bid_at=AT,ask_at=AT)
    return r


def bad_pair():
    return [dict(key=key,direction=d,cost=cost,service=service,rate=1,
                 queue=100,wanted=250,price=cost,inside=False)
            for key,d,cost,service in [(('A','yes'),1,.4,.01),(('B','no'),1,.55,1),
                                      (('B','yes'),-1,.4,.01),(('A','no'),-1,.55,1)]]


class PairPolicyTests(unittest.TestCase):
    def test_router_off_is_original_class(self):
        self.assertIs(type(engine('router_off')),AdaptiveReplay)

    def test_expensive_chosen_pair_rejected_without_rerouting(self):
        a=engine('router_off');b=engine('router_on')
        self.assertEqual(a.choose(bad_pair()),{('A','no'),('B','no')})
        self.assertEqual(b.choose(bad_pair()),set())
        self.assertEqual(b.pair_records[-1]['reason'],'nonpositive_margin')

    def test_passing_guard_preserves_choice_size_and_candidate_values(self):
        a=engine('router_off');b=engine('router_on')
        ca=a.event_candidates('G',AT);cb=copy.deepcopy(ca)
        self.assertEqual(a.choose(ca),b.choose(cb));self.assertEqual(ca,cb)

    def test_guard_preserves_partial_fill_offset_only(self):
        r=engine('router_on');position(r,25);cs=bad_pair()
        self.assertEqual(r.choose(cs),{('A','no')})
        self.assertEqual(next(c for c in cs if c['key']==('A','no'))['wanted'],25)

    def test_pending_offset_cancel_still_consumes_offset_room(self):
        r=engine('router_on');position(r,25)
        r.quote('B','yes',.4,20,AT);old=r.orders['B','yes'];r.cancel(old,AT,'test')
        cs=bad_pair();self.assertEqual(r.choose(cs),{('A','no')})
        self.assertEqual(next(c for c in cs if c['key']==('A','no'))['wanted'],5)
        self.assertEqual(old.remaining,20)

    def test_existing_own_offset_excluded_from_pending_subtraction(self):
        r=engine('router_on');position(r,25);r.quote('A','no',.55,25,AT)
        cs=bad_pair();self.assertEqual(r.choose(cs),{('A','no')})
        self.assertEqual(next(c for c in cs if c['key']==('A','no'))['wanted'],25)

    def test_rejection_cancellation_is_delayed(self):
        r=engine('router_on');r.quote('B','no',.55,25,AT)
        old=r.orders['B','no'];reserved=r.reservations()
        cs={c['key']:c for c in bad_pair()};r.candidate=lambda t,o,now:copy.deepcopy(cs[t,o])
        r.refresh('G',AT)
        self.assertEqual(old.cancel_at,AT+.25);self.assertEqual(r.reservations(),reserved)
        r.advance(AT+.25);self.assertNotIn(('B','no'),r.orders)

    def test_allocator_off_admits_negative_score_with_neutral_rank(self):
        a=engine('allocator_on');b=engine('allocator_off')
        self.assertIsNone(a.portfolio_rank(bad_pair(),AT))
        rank=b.portfolio_rank(bad_pair(),AT)
        self.assertLess(rank['score'],0);self.assertEqual(rank['adjusted'],1)

    def test_allocator_off_funds_unprofitable_pair(self):
        r=engine('allocator_off');r.event_candidates=lambda event,now:bad_pair()
        r.rebalance(AT);self.assertGreater(r.allocations['G'],0)

    def test_off_method_diff_is_only_margin_rejection(self):
        def normalized(method):
            lines=inspect.getsource(method).splitlines()[1:]
            return [x.strip() for x in lines if x.strip() and not x.strip().startswith('#')]
        old=normalized(FactorialReplay.portfolio_rank)
        old.remove('if margin<=0:return None')
        self.assertEqual(old,normalized(PairAllocator.rank_without_margin_rejection))

    def test_allocator_on_observer_preserves_original_return(self):
        a=engine('allocator_on');b=FactorialReplay(a.markets,a.cfg,Factors(False,False,False))
        for cs in [bad_pair(),a.event_candidates('G',AT),[]]:
            self.assertEqual(a.portfolio_rank(copy.deepcopy(cs),AT),b.portfolio_rank(copy.deepcopy(cs),AT))

    def test_allocator_off_does_not_invent_missing_flow(self):
        r=engine('allocator_off');cs=bad_pair()
        for c in cs:c['rate']=0
        rank=r.portfolio_rank(cs,AT)
        self.assertEqual(rank['adjusted'],1);self.assertEqual(rank['score'],0)
        self.assertIsNone(rank['wait_seconds'])

    def test_no_new_allocator_timing(self):
        r=engine('allocator_off');r.rebalance(AT);r.rebalance(AT+599)
        self.assertEqual(len(r.decisions),1)
        r.rebalance(AT+600);self.assertEqual(len(r.decisions),2)

    def test_guard_uses_buffer_not_raw_cost_only(self):
        r=engine('router_on');legs=[dict(direction=1,cost=.5),dict(direction=-1,cost=.4999)]
        self.assertLess(chosen_margin(r,legs),0)
        self.assertIsNone(chosen_margin(r,legs[:1]))

    def test_invalid_arm(self):
        with self.assertRaises(ValueError):engine('unknown')


if __name__=='__main__':unittest.main()
