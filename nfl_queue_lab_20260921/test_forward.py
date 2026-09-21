import unittest
from analyze_forward import eligible_volume,normalize,best

class ForwardTests(unittest.TestCase):
    def test_late_received_trade_excluded_from_decision_but_allowed_ex_post(self):
        ts=[dict(ticker='A',outcome='yes',price=.49,size=100,at=100,known_at=120)]
        self.assertEqual(eligible_volume(ts,'A','yes',.49,90,110,110),0)
        self.assertEqual(eligible_volume(ts,'A','yes',.49,90,110),100)

    def test_wrong_side_price_or_window_not_eligible(self):
        ts=[dict(ticker='A',outcome='yes',price=.50,size=100,at=100,known_at=100)]
        self.assertEqual(eligible_volume(ts,'A','no',.60,90,110),0)
        self.assertEqual(eligible_volume(ts,'A','yes',.49,90,110),0)
        self.assertEqual(eligible_volume(ts,'A','yes',.50,100,100),0)

    def test_duplicate_trade_keeps_earliest_actual_availability(self):
        t=dict(trade_id='x',ticker='A',taker_side='no',yes_price_dollars='.49',no_price_dollars='.51',
               count_fp='100',created_time='2026-09-21T00:00:00Z',is_block_trade=False)
        def response(received,recorded):return dict(kind='trades',ticker='A',received_at=received,
               recorded_at=recorded,params={'max_ts':200},body={'cursor':'','trades':[t]})
        _,trades,_,_,_=normalize([response(110,120),response(130,140)])
        self.assertEqual(len(trades),1);self.assertEqual(trades[0]['known_at'],120)

    def test_best_level_uses_last_sorted_bid_without_inventing_extra_queue(self):
        r=dict(body={'orderbook_fp':{'yes_dollars':[['.40','10'],['.49','500']],
                                   'no_dollars':[['.50','600']]}})
        self.assertEqual(best(r,'yes'),(.49,500));self.assertEqual(best(r,'no'),(.50,600))

if __name__=='__main__':unittest.main()
