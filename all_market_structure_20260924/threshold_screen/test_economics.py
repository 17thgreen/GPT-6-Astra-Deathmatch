import unittest
from decimal import Decimal
from economics import pair,purchase
def book(y,n):return {'orderbook_fp':{'yes_dollars':y,'no_dollars':n}}
class Tests(unittest.TestCase):
    def test_greater_direction(self):
        low=book([['.5','10']],[['.6','10']]);high=book([['.7','10']],[['.1','10']])
        self.assertEqual(pair(low,high,'greater',1,1)['gross'],Decimal('.3'))
    def test_less_reverses_direction(self):
        low=book([['.5','10']],[['.6','10']]);high=book([['.7','10']],[['.1','10']])
        self.assertEqual(pair(low,high,'less',1,1)['gross'],Decimal('-.4'))
    def test_depth_and_duplicate_levels(self):
        x=purchase(book([],[['.6','1'],['.6','1'],['.4','5']]),'yes',3,1)
        self.assertEqual(x['cost'],Decimal('1.4'))
        self.assertEqual(len(x['consumed']),2)
    def test_partial_not_scored(self):
        x=pair(book([],[['.6','.99']]),book([['.7','3']],[]),'greater',1,1)
        self.assertFalse(x['complete']);self.assertNotIn('gross',x)
    def test_fees_kill_small_gross(self):
        x=pair(book([],[['.51','10']]),book([['.5','10']],[]),'greater',1,1)
        self.assertGreater(x['gross'],0);self.assertLess(x['net_raw_fee'],0)
    def test_invalid_price(self):
        with self.assertRaises(ValueError):purchase(book([],[['1.1','1']]),'yes',1,1)
    def test_all_outcomes_floor(self):
        for x in [0,1,1.5,2,3]:
            self.assertGreaterEqual(int(x>1)+int(not x>2),1)
            self.assertGreaterEqual(int(x<2)+int(not x<1),1)
if __name__=='__main__':unittest.main()
