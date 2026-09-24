import unittest
from decimal import Decimal
from mathcore import walk,basis,side_depth,volume_bound
class Tests(unittest.TestCase):
    def test_matched_units(self):
        p={'orderbook':{'bids':[['10.2','10']],'asks':[['10.3','10']]}}
        s={'bids':[['100','1',9]],'asks':[['101','1',9]]}
        r=basis(p,s,'.1',1)
        self.assertEqual(r['underlying_units'],Decimal(1))
        self.assertEqual(r['directions']['sell_perp_buy_spot']['entry_basis_dollars'],Decimal(1))
    def test_depth_not_order_count(self):
        self.assertFalse(walk([['100','.5',200]],1,True)['complete'])
    def test_walk_prices(self):
        self.assertEqual(walk([['101','2'],['100','1']],2,True)['value'],201)
    def test_auction(self):
        self.assertEqual(basis({}, {'auction_mode':True},1,1)['status'],'AUCTION_REJECTED')
    def test_reference_not_tiny_best_bid(self):
        r=side_depth([['.60','1'],['.59','199'],['.50','800']],1000)
        self.assertEqual(r['reference_price'],Decimal('.59'));self.assertTrue(r['target_met'])
    def test_missing_depth(self):
        r=side_depth([],1000);self.assertFalse(r['target_met']);self.assertIsNone(r['reference_price'])
    def test_reward_cap(self):
        self.assertEqual(volume_bound('.5')['reward_minus_fee'],Decimal('-.0125'))
        self.assertIsNone(volume_bound('.01'))
    def test_nonfinite(self):
        with self.assertRaises(ValueError):walk([['NaN','1']],1,True)
if __name__=='__main__':unittest.main()
