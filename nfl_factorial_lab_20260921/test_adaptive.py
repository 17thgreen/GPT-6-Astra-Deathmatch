import unittest
from dataclasses import replace
from adaptive_policy import AdaptiveReplay
from replay_v2 import Config,Order,OrderFees
from test_replay_v2 import markets,trade

KO=1000000;AT=KO-100000

def engine(mode='inventory',delay=.25):
    r=AdaptiveReplay(markets(KO),replace(Config(),quote_source='candles',queue_early=100,
        queue_last12h=100,liquidation_lead_seconds=300,cancel_delay_seconds=delay),mode)
    for t in ('A','B'):r.books[t]=dict(bid=.49,ask=.51,bid_at=AT,ask_at=AT)
    return r

def cs(r):return r.event_candidates('G',AT)

def position(r,size):
    o=Order(999,'A','yes',1,.49,size,0,AT-1,OrderFees())
    r.account_fill(o,size,AT-1,'maker','test setup')

class AdaptiveTests(unittest.TestCase):
    def test_no_flow_inventory_target_25(self):
        r=engine();c=cs(r);self.assertEqual(r.inventory_target(c[0],c,AT),25)
    def test_high_opposing_flow_allows_250(self):
        r=engine();c=cs(r)
        for x in c:x['rate']=1
        self.assertEqual(r.inventory_target(c[0],c,AT),250)
    def test_routes_not_summed_as_independent_depth(self):
        r=engine();c=cs(r)
        for x in c:x['rate']=.1
        self.assertEqual(r.inventory_target(c[0],c,AT),40)
    def test_exit_budget_limits_target(self):
        r=engine();r.exit_remaining['G']=10;c=cs(r)
        self.assertEqual(r.inventory_target(c[0],c,AT),10)
    def test_pending_cancel_counts_against_directional_room(self):
        r=engine();r.quote('B','no',.49,20,AT);r.cancel(r.orders['B','no'],AT,'test')
        c=next(x for x in cs(r) if x['key']==('A','yes'))
        self.assertEqual(r.bounded_quantity(c,25),(5,20))
    def test_existing_inventory_uses_target_room(self):
        r=engine();position(r,20);c=next(x for x in cs(r) if x['key']==('A','yes'))
        self.assertEqual(r.bounded_quantity(c,25)[0],5)
    def test_resize_does_not_release_capacity_early(self):
        r=engine();r.quote('A','yes',.49,100,AT);o=r.orders['A','yes'];identity=o.identity
        r.quote('A','yes',.49,25,AT)
        self.assertEqual(o.remaining,100);r.advance(AT+.25)
        self.assertEqual(o.remaining,25);self.assertEqual(o.identity,identity);self.assertEqual(o.queue,100)
    def test_pending_old_order_can_fill_above_new_soft_target(self):
        r=engine(delay=5);r.quote('A','yes',.49,100,AT);o=r.orders['A','yes'];o.queue=0
        r.quote('A','yes',.49,25,AT)
        r.on_trade(dict(ticker='A',at=AT+1,yes_price=.49,size=200,taker_side='no'))
        self.assertEqual(r.holdings['G'],100);r.assert_limits()
    def test_same_timestamp_trade_flow_excluded(self):
        r=engine();r.flow.add(dict(ticker='A',at=AT,yes_price=.49,size=1000,taker_side='no'))
        self.assertEqual(r.flow.rate(('A','yes'),.49,AT),0)
        self.assertGreater(r.flow.rate(('A','yes'),.49,AT+.01),0)
    def test_markout_waits_for_actual_asof_horizon(self):
        r=engine('patience');r.pending_marks['A'].append(dict(due=AT+300,price=.49,outcome='yes',size=25))
        r.mature_marks(dict(ticker='A',asof=AT+299,at=AT+359,bid=.4,ask=.42))
        self.assertEqual(len(r.pending_marks['A']),1)
        r.mature_marks(dict(ticker='A',asof=AT+300,at=AT+360,bid=.4,ask=.42))
        self.assertEqual(len(r.pending_marks['A']),0);self.assertAlmostEqual(r.marks['A','yes'][0]['markout'],-.08)
    def test_missing_markout_not_backfilled(self):
        r=engine('patience');r.pending_marks['A'].append(dict(due=AT,price=.49,outcome='yes',size=25))
        r.mature_marks(dict(ticker='A',asof=AT+301,at=AT+361,bid=.4,ask=.42))
        self.assertFalse(r.marks['A','yes']);self.assertEqual(r.metrics['markouts_missing'],1)
    def test_markout_same_time_and_insufficient_samples_excluded(self):
        r=engine('patience');key=('A','yes')
        for i in range(5):r.marks[key].append(dict(observed_at=AT,markout=-.03,size=5))
        self.assertIsNone(r.markout_mean(key,AT));self.assertAlmostEqual(r.markout_mean(key,AT+1),-.03)
        self.assertIsNone(r.markout_mean(key,AT+3601))
    def test_toxicity_veto_and_offset_exemption(self):
        r=engine('patience');c=cs(r);a=next(x for x in c if x['key']==('A','yes'))
        for i in range(5):r.marks['A','yes'].append(dict(observed_at=AT-1,markout=-.03,size=5))
        self.assertFalse(r.patience_decision(a,c,AT)[0])
        r.holdings['G']=-25;self.assertTrue(r.patience_decision(a,c,AT)[0])
    def test_unserved_order_expires_with_cooldown(self):
        r=engine('patience');r.quote('A','yes',.49,250,AT-200);c=cs(r);a=next(x for x in c if x['key']==('A','yes'))
        allow,reason,_=r.patience_decision(a,c,AT)
        self.assertFalse(allow);self.assertEqual(reason,'patience_expired')
        self.assertEqual(r.patience_decision(a,c,AT+1)[1],'cooldown')
    def test_depleted_queue_not_cancelled_for_age(self):
        r=engine('patience');r.quote('A','yes',.49,250,AT-5000);r.orders['A','yes'].queue=0
        c=cs(r);a=next(x for x in c if x['key']==('A','yes'))
        self.assertTrue(r.patience_decision(a,c,AT)[0])
    def test_future_quote_cannot_affect_earlier_timer_markout(self):
        r=engine('patience');r.pending_marks['A'].append(dict(due=AT+300,price=.49,outcome='yes',size=25))
        seen=[];original=r.refresh
        def observe(event,now):
            if now==AT+330:seen.append(len(r.marks['A','yes']))
            return original(event,now)
        r.refresh=observe;r.scheduled['G']=AT+330;r.push(AT+330,3,'refresh','G')
        r.on_quote(dict(ticker='A',at=AT+360,asof=AT+300,bid=.4,ask=.42))
        self.assertEqual(seen,[0]);self.assertEqual(len(r.marks['A','yes']),1)
    def test_portfolio_score_values_existing_queue(self):
        r=engine('allocation');c=cs(r)
        for x in c:x['rate']=1
        fresh=r.portfolio_rank(c,AT)
        for x in c:x['queue']=0
        older=r.portfolio_rank(c,AT)
        self.assertGreater(older['score'],fresh['score']);self.assertGreater(older['lost_queue_wait_seconds'],0)
    def test_portfolio_abstains_without_observed_flow(self):
        r=engine('allocation');self.assertIsNone(r.portfolio_rank(cs(r),AT))
    def test_portfolio_budgets_do_not_reuse_protected_cash(self):
        r=engine('allocation');position(r,25)
        for ticker in ('A','B'):
            for side in ('yes','no'):r.flow.add(dict(ticker=ticker,at=AT-1,yes_price=.49 if side=='no' else .51,size=10000,taker_side=side))
        r.rebalance(AT);d=r.decisions[-1]
        self.assertLessEqual(sum(d['allocations'].values())+d['protected'],r.cash+1e-8)
    def test_portfolio_offset_preserved_without_entry_budget(self):
        r=engine('allocation');position(r,25);r.refresh('G',AT)
        self.assertTrue(r.orders);self.assertTrue(all(o.direction==-1 for o in r.orders.values()))
        self.assertLessEqual(sum(o.remaining for o in r.orders.values()),25)
    def test_invalid_policy_rejected(self):
        with self.assertRaises(ValueError):engine('combined')

if __name__=='__main__':unittest.main()
