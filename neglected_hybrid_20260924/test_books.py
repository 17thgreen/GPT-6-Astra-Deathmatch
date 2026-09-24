import unittest
from capture_books import book_summary

def book(yes=None,no=None):
    return {'orderbook_fp':{'yes_dollars':yes if yes is not None else [['.42','12.50']],
                           'no_dollars':no if no is not None else [['.56','3.25']]}}

class DepthTests(unittest.TestCase):
    def test_reciprocal_ask_keeps_opposite_quantity(self):
        r=book_summary(book());self.assertEqual(r['yes_ask'],'0.44')
        self.assertEqual(r['yes_ask_visible_quantity'],'3.25')
        self.assertEqual(r['no_ask_visible_quantity'],'12.50')
    def test_unsorted_levels_zero_quantity_and_decimal_prices(self):
        r=book_summary(book([['.4250','2.5'],['.43','0'],['.40','3']]))
        self.assertEqual(r['yes_bid'],'0.4250')
    def test_missing_crossed_negative_nan_and_duplicate_refused(self):
        for yes in [[],[['.5','1']],[['.4','-1']],[['NaN','2']],[['.4','1'],['.4','2']]]:
            with self.assertRaises(ValueError):book_summary(book(yes))
    def test_old_cent_schema_not_misinterpreted(self):
        with self.assertRaises(KeyError):book_summary({'orderbook':{'yes':[[42,10]],'no':[[56,10]]}})

if __name__=='__main__':unittest.main()
