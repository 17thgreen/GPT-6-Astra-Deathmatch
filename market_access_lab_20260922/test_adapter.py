import unittest
from adapter import Schedule,entry_window,maker_coefficient,settlement_payout,indicative_pair
from decimal import Decimal as D

class AdapterTests(unittest.TestCase):
    def window(self,**overrides):
        args=dict(event='G',listed_at=800,now=850,schedule=Schedule('G',1000,840,'fixture schedule'),max_schedule_age=30,entry_lead=400,stop_lead=100,state='scheduled');args.update(overrides);return entry_window(**args)
    def test_late_listing_and_exclusive_stop(self):
        self.assertEqual(self.window()['opens'],800);self.assertTrue(self.window()['eligible'])
        self.assertFalse(self.window(now=900,schedule=Schedule('G',1000,890,'fixture'))['eligible'])
    def test_missing_start_not_replaced_by_close(self):self.assertEqual(self.window(schedule=None)['reason'],'missing_start_time')
    def test_future_stale_wrong_identity(self):
        for s in [Schedule('G',1000,851,'x'),Schedule('G',1000,700,'x'),Schedule('H',1000,840,'x')]:self.assertFalse(self.window(schedule=s)['eligible'])
    def test_moved_start_recomputes_cutoff(self):self.assertFalse(self.window(schedule=Schedule('G',900,840,'x'))['eligible'])
    def test_exception_pauses(self):
        for state in ['postponed','cancelled','inplay','unknown']:self.assertFalse(self.window(state=state)['eligible'])
    def test_fractional_payout_is_not_binary(self):
        self.assertEqual(settlement_payout(10,0,'.5'),D(5));self.assertEqual(settlement_payout(10,4,'.3'),D('5.8'))
    def test_same_contract_pairs_constant_even_fractional(self):
        for v in ['0','.23','.5','1']:self.assertEqual(settlement_payout(10,10,v),D(10))
    def test_invalid_settlement(self):
        for v in ['NaN','1.1','-.1']:
            with self.assertRaises(ValueError):settlement_payout(10,0,v)
    def test_fee_override_zero_preserved(self):
        s=dict(fee_type='quadratic_with_maker_fees',fee_multiplier=1)
        self.assertEqual(maker_coefficient(s,{}),D('.0175'))
        self.assertEqual(maker_coefficient(s,dict(fee_multiplier_override=0)),0)
        self.assertEqual(maker_coefficient(s,dict(fee_type_override='quadratic')),0)
        with self.assertRaises(ValueError):maker_coefficient(dict(fee_type='unknown',fee_multiplier=1),{})
    def test_two_sided_margin_and_depth(self):
        b={'orderbook_fp':dict(yes_dollars=[['.4','20'],['.4','30']],no_dollars=[['.59','10']])}
        r=indicative_pair(b,'.0175');self.assertTrue(r['positive_margin']);self.assertEqual(r['yes_best_level_size'],'50')
        self.assertEqual(D(r['buffered_pair_margin']),D('.01')-D('.0175')*(D('.4')*D('.6')+D('.59')*D('.41'))-D('.0002008'))
    def test_one_sided_and_crossed(self):
        self.assertFalse(indicative_pair({'orderbook_fp':{}},0)['two_sided'])
        self.assertFalse(indicative_pair({'orderbook_fp':dict(yes_dollars=[['.6','1']],no_dollars=[['.5','1']])},0)['usable'])
if __name__=='__main__':unittest.main()
