import unittest
from tape import compatible
class DirectionTests(unittest.TestCase):
    def sample(self):return {'yes_price_dollars':'.01','no_price_dollars':'.99','taker_outcome_side':'no','taker_book_side':'ask','taker_side':'no','is_block_trade':False}
    def test_yes_bid_direction(self):self.assertTrue(compatible(self.sample(),'yes'));self.assertFalse(compatible(self.sample(),'no'))
    def test_direction_conflict(self):
        t=self.sample();t['taker_side']='yes';self.assertIsNone(compatible(t,'yes'))
    def test_block_is_not_book_execution(self):
        t=self.sample();t['is_block_trade']=True;self.assertFalse(compatible(t,'yes'))
    def test_legacy_direction(self):
        t=self.sample();del t['taker_outcome_side'];del t['taker_book_side'];self.assertTrue(compatible(t,'yes'))
if __name__=='__main__':unittest.main()
