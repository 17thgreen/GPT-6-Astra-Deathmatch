import unittest
from decimal import Decimal as D
from screen import buy,template
class PayoffTests(unittest.TestCase):
    def test_nested_floor(self):
        for equal in (False,True):
            for x in (-1,0,.5,1,2):
                yes=(x>=0 if equal else x>0);no=not(x>=1 if equal else x>1)
                self.assertGreaterEqual(int(yes)+int(no),1)
    def test_walk_and_complement(self):
        b={'no_dollars':[['.6','2'],['.5','3']], 'yes_dollars':[['.7','5']]}
        c,f=buy(b,'yes',4);self.assertEqual(c,D('1.8'));self.assertEqual(f,D('.0686'))
        self.assertIsNone(buy(b,'yes',6));self.assertEqual(buy(b,'no',1)[0],D('.3'))
    def test_strike_format_and_dates(self):
        a,n=template('Above $4.3700 on Sep 24, 2026',D('4.37'))
        self.assertEqual(a,'above $<STRIKE> on sep 24, 2026');self.assertEqual(n,1)
    def test_comma_strike(self):self.assertEqual(template('above 83,500 MW',D('83500'))[0],'above <STRIKE> mw')
if __name__=='__main__':unittest.main()
