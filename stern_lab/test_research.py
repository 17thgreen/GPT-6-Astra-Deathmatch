import unittest
import numpy as np
import pandas as pd
from stern_state import design, stern_probability, state_probability, anchored_update, assess_buy, remaining_diffusion_variance


class TestResearchContract(unittest.TestCase):
    def test_integrated_variance_is_monotone_in_time_remaining(self):
        from scipy.integrate import quad
        for k in [0., .3, .6, 1.]:
            values=[remaining_diffusion_variance(r,13.7,k) for r in np.linspace(0,1,50)]
            self.assertTrue(np.all(np.diff(values)>=0))
            self.assertEqual(values[0],0.)
            expected=quad(lambda u:13.7**2*(1+k*u)**2,.63,1)[0]
            self.assertAlmostEqual(remaining_diffusion_variance(.37,13.7,k),expected)

    def frame(self):
        return pd.DataFrame(dict(r=[.1,.4,.8],margin=[0,7,-3],spread_line=[0,3,-4],possession=[1,-1,1],
            yardline_100=[5,80,40],down=[1,3,2],ydstogo=[5,9,3],
            home_timeouts_remaining=[2,1,3],away_timeouts_remaining=[1,2,3]))

    def test_reduces_to_original_when_state_corrections_zero(self):
        beta=np.zeros(11);beta[:2]=1
        np.testing.assert_allclose(state_probability(self.frame(),beta),stern_probability(self.frame()))

    def test_team_swap_symmetry(self):
        d=self.frame();swapped=d.copy()
        for key in ['margin','spread_line','possession']:swapped[key]=-d[key]
        swapped['home_timeouts_remaining']=d.away_timeouts_remaining
        swapped['away_timeouts_remaining']=d.home_timeouts_remaining
        beta=np.array([1.1,.8,1,2,3,-1,-2,-3,-1,2,.5])
        np.testing.assert_allclose(state_probability(d,beta)+state_probability(swapped,beta),1.)

    def test_no_silent_extrapolation_to_endgame(self):
        d=self.frame();d.loc[0,'r']=0.
        with self.assertRaises(ValueError):design(d)

    def test_probability_transport_invariants(self):
        self.assertAlmostEqual(anchored_update(.6,.7,.7),.6)
        self.assertAlmostEqual(anchored_update(.6,.7,.9,0),.6)
        self.assertAlmostEqual(anchored_update(.7,.7,.9),.9)
        self.assertGreater(anchored_update(.6,.7,.8),.6)
        self.assertAlmostEqual(anchored_update(.4,.3,.2),1-anchored_update(.6,.7,.8))

    def test_transport_refuses_nonfinite_or_terminal_inputs(self):
        for v in [float('nan'),0,1,-.1]:
            with self.assertRaises(ValueError):anchored_update(v,.4,.6)

    def test_gate_blocks_data_and_execution_defects(self):
        args=dict(expected_payout=.64,ask=.58,quantity=10,total_fee=.18,uncertainty_buffer=.02,
                  latency_buffer=.01,state_received_ms=900,quote_received_ms=950,decision_ms=1000,
                  max_age_ms=200,settlement_verified=True,model_admitted=True,available_quantity=10)
        self.assertTrue(assess_buy(**args).eligible)
        for key,value,reason in [
            ('state_received_ms',1001,'future_information'),
            ('quote_received_ms',100,'stale_information'),
            ('settlement_verified',False,'settlement_unverified'),
            ('model_admitted',False,'research_model_not_admitted'),
            ('available_quantity',9,'insufficient_depth_at_ask'),
            ('total_fee',.5,'costs_exceed_edge')]:
            a=args|{key:value};result=assess_buy(**a)
            self.assertFalse(result.eligible);self.assertEqual(result.reason,reason)

if __name__=='__main__':unittest.main()
