import unittest
from decimal import Decimal as D
from policy import admission,payable,public_crossed,stressed,evaluate,stamp

def terms():return {'id':'fixture','market_ticker':'TEST','target_size_fp':'1000','discount_factor_bps':5000,'period_reward':1000000,'start_date':'2026-09-24T05:00:00Z','end_date':'2026-09-24T06:00:00Z','paid_out':False}
def meta():return {'status':'active','event_ticker':'EVENT','close_time':'2026-09-24T06:00:00Z','price_level_structure':'linear_cent','price_ranges':[{'start':'0','end':'1','step':'.01'}]}
class Tests(unittest.TestCase):
    def test_age_and_frozen_start(self):
        p=terms();a=stamp(p['start_date']);self.assertTrue(admission(p,a,a+300));self.assertFalse(admission(p,a,a+301));self.assertTrue(admission(p,a,a+301,new=False));self.assertFalse(admission(p,a+1,a+100))
    def test_payout_floor_and_minimum(self):
        self.assertEqual(payable('0.9999'),0);self.assertEqual(payable('1.0099'),D('1.00'));self.assertEqual(payable('12.7899'),D('12.78'))
    def test_crossed_book(self):
        self.assertTrue(public_crossed({'yes':[(D('.98'),D(1),False)],'no':[(D('.02'),D(1),False)]}))
    def test_one_fifth_rival(self):
        for target in (D(300),D(1000)):
            b={'yes':[],'no':[(D('.98'),D(12),False),(D('.97'),target*2,False)]}
            c=stressed(b,target,D('.5'),{'yes':target})
            self.assertEqual(D(c['rivals']['yes']['quantity']),target/5);self.assertAlmostEqual(c['scores']['capped']['overall_share'],1/3)
    def test_top_removal_and_buffer_consumption(self):
        b={'yes':[],'no':[(D('.98'),D(12),False),(D('.97'),D(1500),False)]}
        c=stressed(b,D(1000),D('.5'),{'yes':D(1100)},D(100))
        self.assertEqual(c['removed_levels']['no']['quantity'],'12');self.assertEqual(c['rivals']['yes']['price'],'0.02');self.assertTrue(c['scores']['capped']['qualified'])
        self.assertAlmostEqual(c['scores']['capped']['overall_share'],1/3)
    def test_loss_of_opposite_target(self):
        c=stressed({'yes':[],'no':[(D('.98'),D(1000),False)]},D(1000),D('.5'),{'yes':D(1100)},D(100))
        self.assertFalse(c['scores']['capped']['qualified']);self.assertEqual(c['scores']['capped']['overall_share'],0)
    def test_early_pass_late_refuse_and_original_principal(self):
        p=terms();b={'yes_dollars':[],'no_dollars':[['.98','12'],['.97','1500']]};a=stamp(p['start_date'])
        early=evaluate('TEST',p,meta(),b,int((a+60)*1e9));late=evaluate('TEST',p,meta(),b,int((a+1800)*1e9))
        self.assertTrue(early['buffered_alert']);self.assertFalse(late['buffered_alert']);self.assertEqual(early['plans'][1]['principal'],11)
        self.assertEqual(early['plans'][1]['cases'][1]['assumed_own_quantity_consumed_per_side'],'100.0')
    def test_missing_and_account_cap_refused(self):
        p=terms();a=int((stamp(p['start_date'])+60)*1e9)
        self.assertEqual(evaluate('TEST',p,meta(),None,a)['class'],'unavailable')
        p['max_reward_per_account']=100
        self.assertEqual(evaluate('TEST',p,meta(),{},a)['class'],'account_cap_unhandled')

if __name__=='__main__':unittest.main()
