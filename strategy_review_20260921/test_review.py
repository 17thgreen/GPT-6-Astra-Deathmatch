import itertools
import unittest
from quote_guards import Candidate,in_quote_window,quote_admission,reserve_candidates,conservative_remaining_size,marginal_pair_value
from reproduce_defects import evidence


class ReviewTests(unittest.TestCase):
    def test_original_defects_are_reproduced(self):
        x=evidence()
        self.assertEqual(x['late_fill']['maker_contracts_at_or_after_cutoff'],50)
        self.assertEqual(x['same_price_downsize']['actual_resting_size'],100)
        self.assertEqual(x['event_cap']['possible_exposure_after_fill'],450)
        self.assertEqual(x['invalid_book_retains_quote']['maker_contracts_after_invalid_book'],50)

    def test_exact_seven_day_three_hour_window(self):
        kickoff=1000000
        self.assertTrue(in_quote_window(now_seconds=kickoff-604800,kickoff_seconds=kickoff))
        self.assertFalse(in_quote_window(now_seconds=kickoff-604801,kickoff_seconds=kickoff))
        self.assertTrue(in_quote_window(now_seconds=kickoff-10801,kickoff_seconds=kickoff))
        self.assertFalse(in_quote_window(now_seconds=kickoff-10800,kickoff_seconds=kickoff))
        self.assertFalse(in_quote_window(now_seconds=kickoff,kickoff_seconds=kickoff))

    def test_joint_leg_reservations_cover_every_subset_of_fills(self):
        proposals=[Candidate('home_yes',1,250,.49,.005),Candidate('away_no',1,250,.50,.005),
                   Candidate('home_no',-1,250,.50,.005),Candidate('away_yes',-1,250,.49,.005)]
        orders,status=reserve_candidates(proposals,current_home_exposure=200,resting=[],free_cash=500,exposure_cap=250)
        for fill_pattern in itertools.product([0,1],repeat=len(orders)):
            exposure=200+sum(f*o.size*o.home_payoff_direction for f,o in zip(fill_pattern,orders))
            self.assertLessEqual(abs(exposure),250+1e-9)
        self.assertGreaterEqual(status['unreserved_cash'],0)
        self.assertEqual(sum(o.size for o in orders if o.home_payoff_direction==1),50)

    def test_invalid_stale_and_expired_quotes_require_cancel(self):
        args=dict(now_seconds=10000,kickoff_seconds=50000,bid=.49,ask=.50,
                  book_received_seconds=9999,max_book_age_seconds=2,sequence_valid=True)
        self.assertEqual(quote_admission(**args)['action'],'ELIGIBLE_FOR_RISK_CHECK')
        for change in [dict(bid=.51),dict(book_received_seconds=9900),dict(sequence_valid=False),
                       dict(now_seconds=39200,book_received_seconds=39200)]:
            self.assertEqual(quote_admission(**(args|change))['action'],'CANCEL_AND_BLOCK')

    def test_pending_cancel_still_reserves_risk_and_cash(self):
        pending=Candidate('pending_cancel',1,240,.50,.005)
        proposed=Candidate('replacement',1,250,.49,.005)
        orders,status=reserve_candidates([proposed],current_home_exposure=0,resting=[pending],free_cash=500,exposure_cap=250)
        self.assertEqual(orders[0].size,10)
        self.assertAlmostEqual(status['exposure_high'],250)

    def test_cash_reserved_across_orders(self):
        proposals=[Candidate('a',1,100,.5,0),Candidate('b',-1,100,.5,0)]
        admitted,status=reserve_candidates(proposals,current_home_exposure=0,resting=[],free_cash=50,exposure_cap=250)
        self.assertEqual(sum(o.size*o.price for o in admitted),50)
        self.assertEqual(status['unreserved_cash'],0)

    def test_size_reduction_and_pair_economics(self):
        self.assertEqual(conservative_remaining_size(old_remaining=100,requested_size=5),5)
        self.assertEqual(conservative_remaining_size(old_remaining=5,requested_size=100),5)
        x=marginal_pair_value(completion_probability=.90,paired_profit=.00125175,forced_exit_loss=.02186625)
        self.assertLess(x['expected_value'],0)
        self.assertGreater(x['break_even_completion'],.94)

    def test_invalid_inputs_and_existing_breach(self):
        with self.assertRaises(ValueError):in_quote_window(now_seconds=float('nan'),kickoff_seconds=1)
        a=Candidate('same',1,10,.5,0)
        with self.assertRaises(ValueError):reserve_candidates([a],current_home_exposure=0,resting=[a],free_cash=100,exposure_cap=250)
        orders,status=reserve_candidates([],current_home_exposure=260,resting=[],free_cash=500,exposure_cap=250)
        self.assertFalse(orders);self.assertEqual(status['status'],'EXISTING_OBLIGATIONS_EXCEED_LIMITS')


if __name__=='__main__':unittest.main()
