import unittest
from decimal import Decimal as D
from core import event_top,walk_asks,guaranteed_edge
class Measurements(unittest.TestCase):
 def test_complement_uses_opposite_bid_depth(self):
  r=event_top({'orderbook_fp':{'yes_dollars':[['0.40','2']], 'no_dollars':[['0.55','3']]}})
  self.assertEqual(r['yes_ask'],'0.45');self.assertEqual(r['yes_ask_size'],'3')
 def test_missing_side_not_zero_price(self):
  r=event_top({'orderbook_fp':{'yes_dollars':[['0.4','1']]}})
  self.assertIsNone(r['yes_ask']);self.assertFalse(r['two_sided'])
 def test_nonfinite_refused(self):
  with self.assertRaises(ValueError):walk_asks([['NaN','2']],1)
 def test_margin_book_not_event_book(self):
  with self.assertRaises(ValueError):event_top({'orderbook':{'bids':[['50000','1']]}})
 def test_depth_not_touch(self):
  r=walk_asks([['0.4','2'],['0.6','3']],4)
  self.assertEqual(r['cost'],D('2.0'))
 def test_partial_cannot_be_guaranteed_profit(self):
  self.assertIsNone(guaranteed_edge(1,[walk_asks([['0.2','1']],2)],0,2))
 def test_fees_can_kill_gross_edge(self):
  a=walk_asks([['0.49','1']],1)
  self.assertEqual(guaranteed_edge(1,[a,a],'0.03',1),D('-0.01'))
if __name__=='__main__':unittest.main()
