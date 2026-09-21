import unittest
from payoff_gate import classify_routes,ResearchProfile

def check(routes,states):return classify_routes(routes,states,state_space_reviewed=True)

class PayoffTests(unittest.TestCase):
    def test_two_winner_equivalence(self):
        r=check({'Ayes':dict(A=1,B=0),'Bno':dict(A=1,B=0),'Ano':dict(A=0,B=1),'Byes':dict(A=0,B=1)},['A','B'])
        self.assertTrue(r['current_two_direction_kernel_compatible']);self.assertIn(['Ayes','Bno'],r['equivalent_routes'])
    def test_draw_breaks_two_team_equivalence(self):
        r=check({'Ayes':dict(A=1,B=0,draw=0),'Bno':dict(A=1,B=0,draw=1),'Ano':dict(A=0,B=1,draw=1),'Byes':dict(A=0,B=1,draw=0)},['A','B','draw'])
        self.assertFalse(r['current_two_direction_kernel_compatible']);self.assertNotIn(['Ayes','Bno'],r['equivalent_routes'])
    def test_same_contract_complement_in_three_way_event(self):
        r=check({'yes':dict(A=1,B=0,draw=0),'no':dict(A=0,B=1,draw=1)},['A','B','draw'])
        self.assertTrue(r['current_two_direction_kernel_compatible'])
    def test_different_thresholds_not_complementary(self):
        r=check({'over40':dict(low=0,middle=1,high=1),'under45':dict(low=1,middle=1,high=0)},['low','middle','high'])
        self.assertFalse(r['current_two_direction_kernel_compatible']);self.assertEqual(r['complementary_pairs'],[])
    def test_fractional_void_complement_is_not_binary_engine(self):
        r=check({'yes':dict(A=1,B=0,void='.5'),'no':dict(A=0,B=1,void='.5')},['A','B','void'])
        self.assertEqual(r['complementary_pairs'],[['no','yes']]);self.assertFalse(r['current_two_direction_kernel_compatible'])
    def test_missing_state_and_unreviewed_fail(self):
        with self.assertRaises(ValueError):check({'a':dict(A=1),'b':dict(A=0,B=1)},['A','B'])
        with self.assertRaises(ValueError):classify_routes({'a':dict(A=1,B=0),'b':dict(A=0,B=1)},['A','B'])
    def test_invalid_payouts(self):
        for bad in ['NaN','Infinity','1.01','-.1']:
            with self.assertRaises(ValueError):check({'a':dict(A=bad,B=0),'b':dict(A=0,B=1)},['A','B'])
    def test_profile_no_implicit_nfl_defaults(self):
        p=ResearchProfile('EXAMPLE',86400,10800,300,3600,300,.0175,.07,'.01',250,250,'same_market_netting')
        self.assertIs(p.validate(),p)
        with self.assertRaises(TypeError):ResearchProfile('EXAMPLE')

if __name__=='__main__':unittest.main()
