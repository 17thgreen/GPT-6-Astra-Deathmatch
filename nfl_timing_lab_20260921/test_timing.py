import unittest
from dataclasses import replace
from replay_v2 import Config,Order,OrderFees
from timing_policy import TimingReplay
from test_replay_v2 import markets,trade


KO=1000000


def engine(band='d7_d3',variant='route',size=25,cap=250):
    r=TimingReplay(markets(KO),replace(Config(),quote_source='candles',order_size=size,
        exposure_cap=cap,queue_early=100,queue_last12h=100,liquidation_lead_seconds=300),band,variant)
    return r


def books(r,at):
    for t in ('A','B'):r.books[t]=dict(bid=.49,ask=.51,bid_at=at,ask_at=at)


def inventory(r,at,size=25):
    o=Order(999,'A','yes',1,.49,size,0,at,OrderFees())
    r.account_fill(o,size,at,'maker','test initial position')


class TimingTests(unittest.TestCase):
    def test_entry_start_is_inclusive_and_stop_accounts_for_ack(self):
        r=engine();start,end=r.entry_bounds('G')
        self.assertFalse(r.entry_open('G',start-.001));self.assertTrue(r.entry_open('G',start))
        self.assertFalse(r.entry_open('G',end-.5));self.assertTrue(r.entry_open('G',end-.501))

    def test_no_entries_before_selected_band(self):
        r=engine('d3_d1');at=KO-100*3600;books(r,at);r.refresh('G',at)
        self.assertFalse(r.orders)

    def test_boundary_cancels_without_needing_trade(self):
        r=engine();start,end=r.entry_bounds('G');at=end-60;books(r,at);r.refresh('G',at)
        self.assertTrue(r.orders);r.on_boundary('G',end-.25)
        self.assertTrue(all(o.cancel_at==end for o in r.orders.values()))
        r.advance(end);self.assertFalse(r.orders)

    def test_offset_inventory_survives_entry_window(self):
        r=engine();_,end=r.entry_bounds('G');books(r,end);inventory(r,end,25);r.refresh('G',end)
        self.assertTrue(r.orders)
        self.assertTrue(all(o.direction==-1 for o in r.orders.values()))
        self.assertLessEqual(sum(o.remaining for o in r.orders.values()),25)

    def test_flat_after_band_cannot_reopen(self):
        r=engine();_,end=r.entry_bounds('G');books(r,end);r.refresh('G',end)
        self.assertFalse(r.orders)

    def test_remainder_offset_accounts_for_pending_order(self):
        r=engine();_,end=r.entry_bounds('G');books(r,end);inventory(r,end,25)
        r.quote('A','no',.49,20,end);r.cancel(r.orders['A','no'],end,'test pending')
        r.refresh('G',end)
        self.assertLessEqual(sum(o.remaining for o in r.orders.values() if o.direction==-1),25)

    def test_smaller_order_retains_same_event_cap(self):
        r=engine('full',size=10);at=KO-100000;books(r,at);r.refresh('G',at)
        self.assertTrue(all(o.remaining<=10 for o in r.orders.values()));self.assertEqual(r.cfg.exposure_cap,250)

    def test_cap_restricts_aggregate_same_direction_orders(self):
        r=engine('full',size=25,cap=25);at=KO-100000;books(r,at)
        r.quote('A','yes',.49,25,at);r.quote('B','no',.49,25,at)
        self.assertEqual(sum(o.remaining for o in r.orders.values() if o.direction==1),25)
        r.assert_limits()

    def test_cap_does_not_increase_exit_depth(self):
        r=engine('full',cap=500);at=KO-10800;books(r,at);inventory(r,at-1,500)
        r.flatten('G',at)
        self.assertEqual(r.holdings['G'],250);self.assertEqual(r.exit_remaining['G'],0)
        self.assertIsNone(r.finish(at+300)['completed_strategy_pnl'])

    def test_stability_resets_on_price_change(self):
        r=engine('full','stable');at=KO-100000
        for dt,bid in [(0,.49),(60,.49),(120,.49),(180,.49)]:
            r.on_quote(dict(kind='quote',ticker='A',at=at+dt,asof=at+dt-60,bid=bid,ask=.51))
        self.assertEqual(r.patience('A',at+180),180)
        r.on_quote(dict(kind='quote',ticker='A',at=at+240,asof=at+180,bid=.48,ask=.50))
        self.assertEqual(r.patience('A',at+240),120)

    def test_stability_resets_on_observation_gap(self):
        r=engine('full','stable');at=KO-100000
        r.stability['A']=dict(valid=True,bid=.49,ask=.51,last_at=at,since=at-1800)
        r.on_quote(dict(kind='quote',ticker='A',at=at+181,asof=at+121,bid=.49,ask=.51))
        self.assertEqual(r.patience('A',at+181),120)

    def test_unknown_and_stale_stability_cannot_get_long_budget(self):
        r=engine('full','stable');at=KO-100000
        self.assertEqual(r.patience('A',at),120)
        r.stability['A']=dict(valid=True,last_at=at-181,since=at-9999)
        self.assertEqual(r.patience('A',at),120)

    def test_long_patience_is_capped_and_shrinks_at_entry_end(self):
        r=engine('d7_d3','stable');_,end=r.entry_bounds('G');at=end-30;books(r,at)
        for t in ('A','B'):r.stability[t]=dict(valid=True,last_at=at,since=at-9999)
        self.assertEqual(r.patience('A',at),1800)
        self.assertTrue(all(c['horizon']==29.5 for c in r.candidates('G',at)))

    def test_new_quote_is_not_visible_to_earlier_timer(self):
        r=engine('full','stable');at=KO-100000
        r.stability['A']=dict(valid=True,bid=.49,ask=.51,last_at=at,since=at-1200)
        seen=[];original=r.refresh
        def observe(event,now):
            if now==at+60:seen.append(r.stability['A']['bid'])
            return original(event,now)
        r.refresh=observe;r.scheduled['G']=at+60;r.push(at+60,3,'refresh','G')
        r.on_quote(dict(kind='quote',ticker='A',at=at+120,asof=at+60,bid=.48,ask=.50))
        self.assertEqual(seen,[.49])


if __name__=='__main__':unittest.main()
