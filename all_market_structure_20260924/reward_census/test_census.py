import unittest
from census import score,stamp

class EntryTests(unittest.TestCase):
    def setup_case(self,bid):
        p={'start_date':'2026-09-24T00:00:00Z','end_date':'2026-09-25T00:00:00Z','period_reward':1000000,'target_size_fp':'1000'}
        m={'status':'active','close_time':p['end_date'],'price_level_structure':'linear_cent','price_ranges':[{'start':'0','end':'1','step':'.01'}]}
        return p,m,{'yes_dollars':[],'no_dollars':[[bid,'1000']]}
    def test_equality_crosses(self):
        p,m,b=self.setup_case('.99');r=score('T',p,m,b,int(stamp('2026-09-24T01:00:00Z')*1e9))
        self.assertFalse(r['quote']['would_rest']);self.assertIsNone(r['quote']['ideal_remaining_gross'])
    def test_empty_side_half_pool_bound(self):
        p,m,b=self.setup_case('.98');r=score('T',p,m,b,int(stamp('2026-09-24T01:00:00Z')*1e9))
        self.assertTrue(r['quote']['priority']);self.assertEqual(r['quote']['principal'],10)
        self.assertAlmostEqual(r['quote']['ideal_remaining_gross'],100/24/2*23)
    def test_missing_metadata_is_unavailable(self):
        p,m,b=self.setup_case('.98');self.assertEqual(score('T',p,None,b,1)['class'],'unavailable')

if __name__=='__main__':unittest.main()
