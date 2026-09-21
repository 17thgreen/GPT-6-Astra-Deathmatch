import unittest
import numpy as np
from settlement import expected_payout, payout_bounds


class TestSettlement(unittest.TestCase):
    def test_tied_game_does_not_become_away_win(self):
        for side in ["home", "away"]:
            self.assertEqual(expected_payout(home_win=0,away_win=0,tie=1,side=side,tie_payout=.5),.5)
        # Tie payoff belongs to the contract, not to the forecast engine.
        self.assertEqual(expected_payout(home_win=0,away_win=0,tie=1,side="away",tie_payout=0),0.)

    def test_rectangle_bounds_cover_all_interior_values(self):
        for side in ["home","away"]:
            b=payout_bounds(conditional_home_win_bounds=(.61,.72),tie_probability_bounds=(0,.04),side=side,tie_payout=.5)
            for q in np.linspace(.61,.72,19):
                for t in np.linspace(0,.04,17):
                    value=expected_payout(home_win=(1-t)*q,away_win=(1-t)*(1-q),tie=t,side=side,tie_payout=.5)
                    self.assertGreaterEqual(value+1e-15,b.lower)
                    self.assertLessEqual(value-1e-15,b.upper)
        h=payout_bounds(conditional_home_win_bounds=(.61,.72),tie_probability_bounds=(0,.04),side="home",tie_payout=.5)
        a=payout_bounds(conditional_home_win_bounds=(.61,.72),tie_probability_bounds=(0,.04),side="away",tie_payout=.5)
        self.assertAlmostEqual(h.lower,1-a.upper)
        self.assertAlmostEqual(h.upper,1-a.lower)

    def test_unknown_tie_probability_rejects_unjustified_precision(self):
        b=payout_bounds(conditional_home_win_bounds=(.64,.64),tie_probability_bounds=(0,1),side="home",tie_payout=.5)
        self.assertAlmostEqual(b.lower,.5)
        self.assertAlmostEqual(b.upper,.64)
        with self.assertRaises(ValueError):
            expected_payout(home_win=.6,away_win=.5,tie=0,side="home",tie_payout=.5)
        with self.assertRaises(ValueError):
            payout_bounds(conditional_home_win_bounds=(.7,.6),tie_probability_bounds=(0,.02),side="home",tie_payout=.5)


if __name__ == '__main__':unittest.main()
