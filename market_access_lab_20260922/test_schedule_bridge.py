import unittest
from schedule_bridge import from_milestones

class ScheduleBridgeTests(unittest.TestCase):
    def fixture(self):return {'milestones':[dict(id='example',category='Sports',type='football_game',related_event_tickers=['G'],start_date='2026-09-22T20:00:00Z')]}
    def test_exact_match(self):
        s=from_milestones('G',self.fixture(),100,'football_game');self.assertEqual(s.event,'G');self.assertEqual(s.observed_at,100)
    def test_wrong_event_and_type(self):
        for event,kind in [('H','football_game'),('G','basketball_game')]:
            with self.assertRaises(ValueError):from_milestones(event,self.fixture(),100,kind)
    def test_ambiguity(self):
        r=self.fixture();r['milestones']*=2
        with self.assertRaises(ValueError):from_milestones('G',r,100,'football_game')
    def test_no_close_time_substitute(self):
        r=self.fixture();m=r['milestones'][0];m['close_time']=m.pop('start_date')
        with self.assertRaises(ValueError):from_milestones('G',r,100,'football_game')
    def test_requires_timezone(self):
        r=self.fixture();r['milestones'][0]['start_date']='2026-09-22T20:00:00'
        with self.assertRaises(ValueError):from_milestones('G',r,100,'football_game')
