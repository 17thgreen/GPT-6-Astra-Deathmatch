import unittest
from survey import classify

class DepthTests(unittest.TestCase):
    def test_full_depth_and_exact_target(self):
        self.assertEqual(classify({'yes_dollars':[['.01','999.5'],['.02','.5']], 'no_dollars':[['.4','1000']]},'1000')['class'],'both_meet')
    def test_empty_and_partial_are_distinct(self):
        r=classify({'yes_dollars':[], 'no_dollars':[['.01','99']]},'100')
        self.assertEqual(r['class'],'both_short')
        self.assertEqual(r['empty_sides'],['yes'])
        self.assertEqual(r['shortfall']['no'],'1')
    def test_missing_is_not_empty(self):
        with self.assertRaises(KeyError): classify({'yes_dollars':[]},'100')

if __name__=='__main__': unittest.main()
