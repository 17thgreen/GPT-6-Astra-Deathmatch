import unittest
from watch import admitted,stamp
class AdmissionTests(unittest.TestCase):
    def p(self):return {'start_date':'2026-09-24T04:00:00Z','end_date':'2026-09-24T05:00:00Z','target_size_fp':'1000','period_reward':1000000,'market_ticker':'ANY_CATEGORY'}
    def test_new_short_high_rate(self):self.assertTrue(admitted(self.p(),stamp('2026-09-24T03:58:00Z'),stamp('2026-09-24T04:01:00Z')))
    def test_old_program_excluded(self):self.assertFalse(admitted(self.p(),stamp('2026-09-24T04:01:00Z'),stamp('2026-09-24T04:02:00Z')))
    def test_slow_reward_excluded(self):
        p=self.p();p['period_reward']=10000;self.assertFalse(admitted(p,0,stamp('2026-09-24T04:01:00Z')))
    def test_ended_excluded(self):self.assertFalse(admitted(self.p(),0,stamp('2026-09-24T05:00:00Z')))
if __name__=='__main__':unittest.main()
