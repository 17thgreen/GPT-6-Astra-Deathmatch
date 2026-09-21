import copy,itertools,unittest
from dataclasses import replace
from decimal import Decimal
from replay_v2 import Replay,Config,OrderFees


def markets(kickoff=20000):
    return {'A':dict(event='G',direction=1,kickoff=kickoff,verified_mecnet=True),
            'B':dict(event='G',direction=-1,kickoff=kickoff,verified_mecnet=True)}


def trade(at,side,price,size=1,ticker='A'):
    return dict(at=at,ticker=ticker,taker_side=side,yes_price=price,size=size)


def engine(**kwargs):return Replay(markets(),replace(Config(),queue_early=0,queue_last12h=0,**kwargs))


class Tests(unittest.TestCase):
    def test_cutoff_before_matching_and_silent_clock(self):
        r=engine();r.on_trade(trade(9197,'no',.49));r.on_trade(trade(9198,'yes',.50))
        self.assertTrue(r.orders)
        r.on_trade(trade(9200,'no',.49,100))
        self.assertFalse(r.orders);self.assertFalse(r.fills)
        r=engine();r.on_trade(trade(9197,'no',.49));r.on_trade(trade(9198,'yes',.50))
        r.advance(9200);self.assertFalse(r.orders)

    def test_same_price_downsize_waits_for_ack(self):
        r=engine();r.quote('A','yes',.49,100,100)
        r.quote('A','yes',.49,5,101)
        self.assertEqual(r.orders['A','yes'].remaining,100)
        r.advance(101.25);self.assertEqual(r.orders['A','yes'].remaining,5)
        r.quote('A','yes',.49,100,102)
        self.assertEqual(r.orders['A','yes'].remaining,5)

    def test_joint_exposure_cap_and_pending_cancels(self):
        r=engine();r.holdings['G']=200
        r.quote('A','yes',.49,250,100);r.quote('B','no',.49,250,100)
        self.assertEqual(sum(o.remaining for o in r.orders.values()),50)
        r.cancel(r.orders['A','yes'],101,'test');r.quote('B','no',.49,250,101.1)
        self.assertNotIn(('B','no'),r.orders)
        r.advance(101.25);r.quote('B','no',.49,250,101.3)
        self.assertEqual(r.orders['B','no'].remaining,50)

    def test_crossed_proxy_cancels_old_orders(self):
        r=engine();r.on_trade(trade(100,'no',.49));r.on_trade(trade(101,'yes',.50))
        r.on_trade(trade(102,'no',.60));r.on_trade(trade(103,'no',.49,100))
        self.assertFalse(r.fills)

    def test_stale_one_side_cancels_despite_other_side_activity(self):
        r=engine();r.on_trade(trade(100,'no',.49));r.on_trade(trade(101,'yes',.50))
        r.on_trade(trade(399,'yes',.50));r.advance(400.25)
        self.assertFalse(r.orders)

    def test_cancel_pending_fills_are_accounted_and_reserved(self):
        r=engine();r.quote('A','yes',.49,100,100);r.cancel(r.orders['A','yes'],101,'test')
        r.on_trade(trade(101.1,'no',.49,100))
        self.assertEqual(r.holdings['G'],50)
        self.assertEqual(r.metrics['fills_while_cancel_pending'],1)
        r.advance(101.25);self.assertFalse(r.orders);r.assert_limits()

    def test_queue_is_consumed_once_and_replenishment_goes_to_back(self):
        r=Replay(markets(),replace(Config(),queue_early=100,queue_last12h=100,fill_participation=1))
        r.books['A']=dict(bid=.49,ask=.50,bid_at=100,ask_at=100)
        r.quote('A','yes',.49,50,100)
        r.on_trade(trade(101,'no',.49,80));self.assertFalse(r.fills)
        r.on_trade(trade(102,'no',.49,70));self.assertEqual(r.holdings['G'],50)
        r.quote('A','yes',.49,50,103);self.assertEqual(r.orders['A','yes'].queue,100)

    def test_global_cash_reservations(self):
        m=markets();m.update({k+'2':v|{'event':'H'} for k,v in markets().items()})
        r=Replay(m,replace(Config(),starting_cash=50,queue_early=0))
        for t in m:
            for side in ('yes','no'):r.quote(t,side,.50,250,100)
        self.assertLessEqual(r.reservations(),50+1e-8)
        self.assertLess(sum(o.remaining for o in r.orders.values()),100)
        r.assert_limits()

    def test_fee_accumulator_split_and_unsplit(self):
        for precision in ['.0001','.01']:
            f=OrderFees(Decimal(precision));parts=[f.charge(.5,1,.0175) for _ in range(4)]
            whole=OrderFees(Decimal(precision)).charge(.5,4,.0175)
            self.assertAlmostEqual(sum(parts),whole,places=8)
            self.assertTrue(all(v>=0 for v in parts))
        self.assertEqual(OrderFees().charge(.5,1,.0175),.0044)

    def test_fee_rounding_is_not_affected_by_binary_float_complements(self):
        a=OrderFees();b=OrderFees()
        self.assertEqual([a.charge(.3,.01,.0175) for _ in range(20)],
                         [b.charge(1-.7,.01,.0175) for _ in range(20)])
        with self.assertRaises(ValueError):OrderFees().charge(.3,.005,.0175)

    def test_unfinished_capture_is_not_completed_pnl(self):
        r=engine();s=r.finish(9000)
        self.assertIsNone(s['completed_strategy_pnl']);self.assertEqual(s['completed_window_games'],0)

    def test_unresolved_inventory_has_no_fictitious_exit(self):
        r=engine();r.quote('A','yes',.49,10,100);r.on_trade(trade(101,'no',.49,20))
        s=r.finish(9200)
        self.assertIsNone(s['completed_strategy_pnl']);self.assertEqual(s['unresolved_contracts'],10)
        self.assertEqual(s['taker_contracts'],0)
        self.assertAlmostEqual(s['terminal_payout_bounds'][1]-s['terminal_payout_bounds'][0],10)

    def test_exit_uses_single_game_depth_budget(self):
        r=engine(assumed_exit_depth=7)
        r.holdings['G']=20
        for ticker in ['A','B']:r.books[ticker]=dict(bid=.49,ask=.50,bid_at=9199,ask_at=9199)
        s=r.finish(9200)
        self.assertEqual(s['taker_contracts'],7);self.assertEqual(s['unresolved_contracts'],13)

    def test_payoff_identity_rejects_unverified_events(self):
        m=markets();m['A']['verified_mecnet']=False
        with self.assertRaises(ValueError):Replay(m)

    def test_cross_ticker_pair_releases_one_dollar_per_pair(self):
        r=engine()
        r.quote('A','no',.50,10,100);r.quote('B','no',.49,10,100)
        r.match(trade(101,'yes',.50,20,'A'));r.match(trade(102,'yes',.51,20,'B'))
        self.assertEqual(r.holdings['G'],0)
        self.assertAlmostEqual(r.cash,5000+10-5-4.9-sum(f['fee'] for f in r.fills))
        r.assert_limits()

    def test_all_full_fill_orders_respect_risk_for_every_permutation(self):
        r=engine(fill_participation=1)
        for ticker in ['A','B']:
            for side in ['yes','no']:r.quote(ticker,side,.49,125,100)
        self.assertEqual(len(r.orders),4)
        for ordering in itertools.permutations(list(r.orders)):
            candidate=copy.deepcopy(r)
            for i,(ticker,side) in enumerate(ordering):
                candidate.match(trade(101+i,'no' if side=='yes' else 'yes',.49 if side=='yes' else .51,125,ticker))
                candidate.assert_limits()
            self.assertEqual(candidate.holdings['G'],0)

    def test_future_print_does_not_change_prior_fills(self):
        first=[trade(100,'no',.49),trade(101,'yes',.50),trade(102,'no',.49,100)]
        a=engine();b=engine()
        for x in first:a.on_trade(x);b.on_trade(x)
        prior=copy.deepcopy(a.fills)
        a.on_trade(trade(200,'yes',.9,100));b.on_trade(trade(200,'yes',.1,100))
        self.assertEqual(a.fills[:len(prior)],prior);self.assertEqual(b.fills[:len(prior)],prior)

    def test_candle_mode_does_not_invent_quotes_from_trades(self):
        r=engine(quote_source='candles')
        r.on_trade(trade(100,'no',.49));r.on_trade(trade(101,'yes',.50))
        self.assertFalse(r.books);self.assertFalse(r.orders)
        r.on_quote(dict(ticker='A',at=160,asof=100,bid=.49,ask=.50))
        self.assertTrue(r.orders)
        with self.assertRaises(ValueError):r.on_quote(dict(ticker='A',at=161,asof=162,bid=.49,ask=.50))

    def test_early_liquidation_and_retries_never_reuse_depth(self):
        r=engine(liquidation_lead_seconds=300,assumed_exit_depth=7)
        r.holdings['G']=20
        for ticker in ['A','B']:r.books[ticker]=dict(bid=.49,ask=.50,bid_at=8899,ask_at=8899)
        s=r.finish(9200)
        self.assertEqual(s['taker_contracts'],7)
        self.assertEqual(r.fills[0]['at'],8900)
        self.assertEqual(s['unresolved_contracts'],13)
        self.assertEqual(s['metrics']['events_with_unresolved_exit'],1)


if __name__=='__main__':unittest.main()
