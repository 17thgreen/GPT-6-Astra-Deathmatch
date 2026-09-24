import unittest
from decimal import Decimal as D
from screen import whole_share,cases,model

class Tests(unittest.TestCase):
    def test_whole_level_includes_size_beyond_target(self):
        b={'yes':[(D('.01'),D(1000),False)],'no':[(D('.98'),D(2000),False)]}
        x=whole_share(b,D(1000),D('.5'),'yes',D(100));self.assertAlmostEqual(x['overall_share'],100/1100/2)
    def test_order_permutation_invariance(self):
        rows=[(D('.01'),D(500),False),(D('.01'),D(100),True),(D('.01'),D(500),False)]
        a=model.score_side(rows,D(1000),D('.5'),'whole_level');b=model.score_side(list(reversed(rows)),D(1000),D('.5'),'whole_level');self.assertEqual(a,b)
    def test_no_credit_below_qualifying_level(self):
        b={'yes':[(D('.02'),D(1000),False)],'no':[(D('.90'),D(2000),False)]}
        self.assertEqual(whole_share(b,D(1000),D('.5'),'yes',D(100))['overall_share'],0)
    def test_reference_discount(self):
        b={'yes':[(D('.02'),D(200),False),(D('.01'),D(800),False)],'no':[(D('.90'),D(2000),False)]}
        self.assertAlmostEqual(whole_share(b,D(1000),D('.5'),'yes',D(100))['overall_share'],50/650/2)
    def test_supported_classification_and_depth_loss(self):
        p={'id':'x','market_ticker':'TEST','start_date':'2026-09-24T05:00:00Z','end_date':'2026-09-24T06:00:00Z','period_reward':1000000,'target_size_fp':'1000','discount_factor_bps':5000,'paid_out':False}
        m={'status':'active','event_ticker':'E','close_time':p['end_date'],'price_level_structure':'linear_cent','price_ranges':[{'start':'0','end':'1','step':'.01'}]}
        ns=int((model.stamp(p['start_date'])+60)*1e9);b={'yes_dollars':[['.01','1000']],'no_dollars':[['.98','1000']]}
        xs=cases(p,m,b,ns);self.assertTrue(xs);self.assertTrue(all(x['classification']=='supported_level' for x in xs));self.assertTrue(all(not x['passes'] for x in xs))
        b['yes_dollars']=[];xs=cases(p,m,b,ns);self.assertTrue(all(x['classification']=='gap_completion' for x in xs))

if __name__=='__main__':unittest.main()
