import copy,unittest
from dataclasses import replace
from joint_policy import JointRouter,rank_pairs
from pair_policy import GuardedRouter,chosen_margin
from test_pair_policy import bad_pair
from test_replay_v2 import markets
from test_adaptive import AT,KO,position
from replay_v2 import Config


def engine(mode):
    return JointRouter(markets(KO),replace(Config(),quote_source='candles',queue_early=100,queue_last12h=100,liquidation_lead_seconds=300),mode)

class JointTests(unittest.TestCase):
    def test_rejected_pair_recovered(self):
        for mode in ['rescue','joint']:
            r=engine(mode);cs=bad_pair();chosen=r.choose(cs)
            self.assertEqual(len(chosen),2)
            self.assertGreater(chosen_margin(r,[c for c in cs if c['key'] in chosen]),0)
            self.assertLess(r.pair_records[-1]['original_margin'],0)

    def test_rescue_passing_decision_matches_q7(self):
        r=engine('rescue');b=GuardedRouter(r.markets,r.cfg);cs=bad_pair()
        for c in cs:c['cost']=.4
        a=copy.deepcopy(cs);bb=copy.deepcopy(cs)
        self.assertEqual(r.choose(a),b.choose(bb));self.assertEqual(a,bb)
        self.assertEqual(r.pair_records,b.pair_records)

    def test_no_profitable_pair_exact_offset_fallback(self):
        for mode in ['rescue','joint']:
            r=engine(mode);b=GuardedRouter(r.markets,r.cfg)
            position(r,25);position(b,25);cs=bad_pair()
            for c in cs:c['cost']=.7
            a=copy.deepcopy(cs);bb=copy.deepcopy(cs)
            self.assertEqual(r.choose(a),b.choose(bb));self.assertEqual(a,bb)
            self.assertEqual(r.pair_records,b.pair_records)

    def test_joint_optimizes_pair_bottleneck(self):
        r=engine('joint');cs=bad_pair()
        expected=rank_pairs(r,cs)[0]
        self.assertEqual(r.choose(cs),set(expected['keys']))
        self.assertNotEqual(r.choose(cs),{('A','no'),('B','no')})

    def test_zero_flow_deterministic_cheapest(self):
        r=engine('joint');cs=bad_pair()
        for c in cs:c['service']=0;c['rate']=0
        self.assertEqual(r.choose(cs),{('A','yes'),('B','yes')})
        self.assertEqual(r.choose(list(reversed(cs))),{('A','yes'),('B','yes')})

    def test_same_price_incumbent_retention(self):
        r=engine('joint');cs=bad_pair()
        for c in cs:c['cost']=.4;c['price']=.4;c['service']=.9 if c['key'][1]=='yes' else 1
        r.quote('A','yes',.4,25,AT);r.quote('B','yes',.4,25,AT)
        self.assertEqual(r.choose(cs),{('A','yes'),('B','yes')})
        for c in cs:
            if c['key'][1]=='yes':c['service']=.5
        self.assertEqual(r.choose(cs),{('A','no'),('B','no')})

    def test_price_change_and_cancel_are_not_incumbent(self):
        r=engine('joint');cs=bad_pair()
        r.quote('A','yes',.4,25,AT);r.quote('B','yes',.4,25,AT)
        self.assertTrue(any(p['incumbent'] for p in rank_pairs(r,cs)))
        r.cancel(r.orders['A','yes'],AT,'test')
        self.assertFalse(any(p['incumbent'] for p in rank_pairs(r,cs)))
        r.orders['A','yes'].cancel_at=None;r.orders['A','yes'].price=.39
        self.assertFalse(any(p['incumbent'] for p in rank_pairs(r,cs)))

    def test_pending_reservation_preserved_on_reroute(self):
        r=engine('rescue');r.quote('B','no',.55,25,AT);old=r.orders['B','no']
        cs={c['key']:c for c in bad_pair()};r.candidate=lambda t,o,now:copy.deepcopy(cs[t,o])
        r.refresh('G',AT)
        self.assertGreaterEqual(r.reservations(),0)
        self.assertIn(old.identity,[o.identity for o in r.orders.values()])
        r.assert_limits()

    def test_empty_and_invalid_mode(self):
        self.assertEqual(engine('joint').choose([]),set())
        with self.assertRaises(ValueError):engine('bad')

if __name__=='__main__':unittest.main()
