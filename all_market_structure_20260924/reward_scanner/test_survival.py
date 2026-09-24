import math,unittest
from survival import expected_net

class Tests(unittest.TestCase):
    def test_limits(self):
        self.assertEqual(expected_net(20,10,1,math.inf),20)
        self.assertEqual(expected_net(20,10,1,0),-10)
        self.assertEqual(expected_net(20,10,0,0),0)
    def test_break_even(self):
        for horizon in (.1,1,3):self.assertAlmostEqual(expected_net(20,10,horizon,.5),0)
    def test_closed_form(self):
        self.assertAlmostEqual(expected_net(20,10,1,1),10*(1-math.exp(-1)))
    def test_longer_survival_improves(self):
        values=[expected_net(20,10,1,m) for m in (.01,.1,.5,1,10)]
        self.assertEqual(values,sorted(values))

if __name__=='__main__':unittest.main()
