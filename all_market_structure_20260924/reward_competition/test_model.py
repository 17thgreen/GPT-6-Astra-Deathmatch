import unittest
from decimal import Decimal as D
from model import score_side,proposals,scenario,depth,admitted

class ModelTests(unittest.TestCase):
    def test_target_required(self):
        self.assertIsNone(score_side([(D('.01'),D(999),True)],D(1000),D('.5')))
        self.assertEqual(score_side([(D('.01'),D(1000),True)],D(1000),D('.5'))['own_share'],1)
    def test_reference_cliff(self):
        def sc(q):return score_side([(D('.10'),D(q),False),(D('.01'),D(1000-q),True)],D(1000),D('.5'))
        self.assertEqual(sc(199)['reference'],'0.01');self.assertAlmostEqual(sc(199)['own_share'],.801)
        self.assertEqual(sc(200)['reference'],'0.10');self.assertAlmostEqual(sc(200)['own_share'],(800*.5**9)/(200+800*.5**9))
    def test_queue_and_boundary_bracket(self):
        rows=[(D('.01'),D(1000),True),(D('.01'),D(1000),False)]
        self.assertEqual(score_side(rows,D(1000),D('.5'))['own_share'],0)
        self.assertEqual(score_side(rows,D(1000),D('.5'),'whole_level')['own_share'],.5)
    def test_buffer_qualification(self):
        self.assertIsNone(score_side([(D('.01'),D(999),True)],D(1000),D('.5')))
        self.assertIsNotNone(score_side([(D('.01'),D(1100-100),True)],D(1000),D('.5')))
        self.assertIsNone(score_side([(D('.01'),D(1100-101),True)],D(1000),D('.5')))
    def test_two_sided_completion_and_normalization(self):
        b={'yes':[],'no':[]};o,c=proposals(b,D(1000));s=scenario(b,D(1000),D('.5'),o,'none')
        self.assertEqual(c,'resting_completion');self.assertEqual(sum(o.values()),D(2000))
        self.assertEqual(s['scores']['capped']['overall_share'],1)
    def test_crossing_and_missing_not_empty(self):
        o,c=proposals({'yes':[],'no':[(D('.99'),D(1000),False)]},D(1000));self.assertEqual(c,'one_cent_would_cross')
        with self.assertRaises(KeyError):depth({'yes_dollars':[]})
        with self.assertRaises(ValueError):depth({'yes_dollars':[],'no_dollars':None})
    def test_one_side_competition(self):
        b={'yes':[],'no':[(D('.90'),D(1000),False)]};o,c=proposals(b,D(1000))
        s=scenario(b,D(1000),D('.5'),o,'better_200')
        self.assertAlmostEqual(s['scores']['capped']['overall_share'],1/3)
        self.assertAlmostEqual(s['scores']['whole_level']['overall_share'],500/700/2)
    def test_zero_discount_and_invalid_duration(self):
        s=score_side([(D('.02'),D(200),False),(D('.01'),D(800),True)],D(1000),D(0));self.assertEqual(s['own_share'],0)
        self.assertFalse(admitted({'target_size_fp':'1000','period_reward':1000000,'start_date':'2026-09-24T04:00:00Z','end_date':'2026-09-24T04:00:00Z'},1790222400))

if __name__=='__main__':unittest.main()
