import copy
import unittest
from core import *

class CausalAndLedgerTests(unittest.TestCase):
    def setUp(self):
        self.f={'race_id':'PA-SEN','p_dem':.8,'available_at':'2024-10-27T16:00:00Z','source':'synthetic',
                'provenance_status':'contemporaneous'}
        self.q={'race_id':'PA-SEN','yes_bid':.5,'yes_ask':.52,'observed_at':DECISIONS[0],'kind':'synthetic'}
        self.r={'race_id':'PA-SEN','ticker':'SYNTHETIC','state':'PA','mapping_status':'verified_democratic_party_yes',
                'outcome_dem':1,'resolution_source':'synthetic','open_at':'2024-10-01T00:00:00Z','close_at':'2024-11-06T00:00:00Z'}
    def test_timezone_required(self):
        with self.assertRaises(ValueError):instant('2024-10-28')
    def test_forecast_lag_rejects_latest(self):
        late=dict(self.f,p_dem=.99,available_at='2024-10-29T15:59:00Z')
        self.assertEqual(forecast_asof([self.f,late],DECISIONS[0])['p_dem'],.8)
    def test_postdecision_and_unproven_forecasts_rejected(self):
        self.assertIsNone(forecast_asof([dict(self.f,available_at='2024-11-06T00:00:00Z')],DECISIONS[0]))
        self.assertIsNone(forecast_asof([dict(self.f,provenance_status='retrospective')],DECISIONS[0]))
    def test_stale_forecast_rejected(self):
        self.assertIsNone(forecast_asof([dict(self.f,available_at='2024-10-01T00:00:00Z')],DECISIONS[0]))
    def test_conflicting_forecasts_refused(self):
        with self.assertRaises(ValueError):forecast_asof([self.f,dict(self.f,p_dem=.3)],DECISIONS[0])
    def test_future_stale_crossed_and_missing_quote(self):
        for updates in [{'observed_at':'2024-10-29T17:00:00Z'},{'observed_at':'2024-10-29T14:59:59Z'},
                        {'yes_bid':.8,'yes_ask':.7},{'yes_ask':None}]:
            self.assertIsNone(quote_asof([dict(self.q,**updates)],DECISIONS[0]))
    def test_probability_nan_rejected(self):
        for p in [float('nan'),float('inf'),-.1,1.1]:
            with self.assertRaises(ValueError):probability(p)
    def test_no_reciprocity_and_cash(self):
        t=trade(.1,.7,.72,0)
        self.assertEqual(t['side'],'no');self.assertAlmostEqual(t['price'],.3)
        self.assertAlmostEqual(t['fee'],.0147)
        self.assertAlmostEqual(t['capital'],.3347)
        self.assertAlmostEqual(t['net'],.6653)
    def test_loss_debits_principal_and_costs(self):
        t=trade(.9,.5,.52,0)
        self.assertAlmostEqual(t['net'],-t['capital'])
    def test_market_mid_abstains(self):
        self.assertIsNone(trade(.51,.5,.52,1))
    def test_strict_margin_threshold(self):
        cost=.5+fee(.5)+.02
        self.assertIsNone(trade(cost+.03,.49,.5,1))
        self.assertIsNotNone(trade(cost+.030001,.49,.5,1))
    def test_duplicate_race_refused(self):
        with self.assertRaises(ValueError):evaluate({'races':[self.r,self.r],'forecasts':[self.f],'quotes':[self.q]})
    def test_hybrid_score_and_frozen_cost_stress(self):
        res=evaluate({'races':[self.r],'forecasts':[self.f],'quotes':[self.q]},[DECISIONS[0]])
        r=res['horizons'][0]['rows'][0]
        self.assertAlmostEqual(r['arms']['hybrid_50']['p'],.655)
        s=res['horizons'][0]['summary']['hybrid_50']
        self.assertAlmostEqual(s['hypothetical_net_dollars']-s['extra_3c_cost_same_trades_net'],.03)
        self.assertFalse(res['live_validation'])
    def test_unresolved_is_not_zero_loss(self):
        res=evaluate({'races':[dict(self.r,outcome_dem=None)],'forecasts':[self.f],'quotes':[self.q]},[DECISIONS[0]])
        self.assertEqual(res['horizons'][0]['admitted_races'],0)
        self.assertIsNone(res['horizons'][0]['summary'])
    def test_logloss_only_clipped(self):
        self.assertAlmostEqual(logloss(1,0),-math.log(.001))
    def test_boundary_quotes_refuse_absent_side_midpoint(self):
        for bid,ask in [(0,.01),(0,0),(.99,1)]:
            self.assertIsNone(quote_asof([dict(self.q,yes_bid=bid,yes_ask=ask)],DECISIONS[0]))
    def test_closed_contract_refused(self):
        res=evaluate({'races':[dict(self.r,close_at=DECISIONS[0])],'forecasts':[self.f],'quotes':[self.q]},[DECISIONS[0]])
        self.assertEqual(res['horizons'][0]['exclusion_counts'],{'not_open_at_decision':1})

if __name__=='__main__':unittest.main()
