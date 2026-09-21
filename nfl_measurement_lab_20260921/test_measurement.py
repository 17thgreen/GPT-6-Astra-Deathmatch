import copy
import json
import unittest
from datetime import datetime,timezone
from pathlib import Path

from capture import allowed
from evaluation_gate import check
from historical import future_mark
from measure import analyze,best,matching,markout,normalize,service,spans_cover


def book(at,yes=.4,no=.59,q=100):
    return dict(kind='book',ticker='T',request_at=at-1,received_at=at,recorded_at=at,
        body={'orderbook_fp':{'yes_dollars':[[str(yes),str(q)]],'no_dollars':[[str(no),str(q)]]}})


def tape(at=1005,size=300,known=1010,price=.4,trade_id='a',**kwargs):
    t=dict(trade_id=trade_id,ticker='T',taker_side='no',yes_price_dollars=str(price),
           no_price_dollars=str(1-price),count_fp=str(size),
           created_time=datetime.fromtimestamp(at,timezone.utc).isoformat(),is_block_trade=False)
    t.update(kwargs)
    return dict(kind='trades',ticker='T',page=0,poll=0,request_at=known-1,received_at=known,recorded_at=known,
                params=dict(min_ts=0,max_ts=10000),body=dict(trades=[t],cursor=''))


class MeasurementTests(unittest.TestCase):
    def test_best_price_independent_of_array_order(self):
        for levels in [[['.4','10'],['.6','20']],[['.6','20'],['.4','10']]]:
            self.assertEqual(best({'orderbook_fp':{'yes_dollars':levels}},'yes'),(.6,20))

    def test_zero_size_level_is_not_best(self):
        self.assertEqual(best({'orderbook_fp':{'yes_dollars':[['.7','0'],['.4','10']]}},'yes'),(.4,10))

    def test_nonfinite_depth_rejected(self):
        with self.assertRaises(ValueError):best({'orderbook_fp':{'yes_dollars':[['.4','nan']]}},'yes')

    def test_trade_only_service_subtracts_queue_once(self):
        r=service([dict(size=80,at=1),dict(size=40,at=2),dict(size=480,at=3)],100)
        self.assertEqual((r['first_service_at'],r['full_service_at'],r['serviced_contracts']),(2,3,250))

    def test_no_service_before_depth_clears(self):
        self.assertEqual(service([dict(size=100,at=1)],100)['serviced_contracts'],0)

    def test_future_received_trade_cannot_enter_feature(self):
        _,trades,_,_=normalize([tape(at=900,known=1001)])
        self.assertEqual(matching(trades,'T','yes',.4,0,1000,1000),[])

    def test_equal_receive_time_not_strictly_prior(self):
        _,trades,_,_=normalize([tape(at=900,known=1000)])
        self.assertEqual(matching(trades,'T','yes',.4,0,1000,1000),[])

    def test_dedup_retains_first_receipt(self):
        _,trades,_,_=normalize([tape(known=1010),tape(known=1020)])
        self.assertEqual(len(trades),1);self.assertEqual(trades[0]['known_at'],1010)

    def test_conflicting_duplicate_rejected(self):
        with self.assertRaises(ValueError):normalize([tape(),tape(size=301)])

    def test_block_trade_excluded(self):
        self.assertEqual(normalize([tape(is_block_trade=True)])[1],[])

    def test_missing_page_not_complete_coverage(self):
        r=tape();r['page']=1
        self.assertFalse(spans_cover(normalize([r])[2]['T'],1000,1010))

    def test_depth_decline_not_credited_as_own_service(self):
        result,features,labels,spells,changes=analyze([book(1000,q=500),book(1010,q=1),tape(size=1)])
        self.assertEqual(labels[0]['serviced_contracts'],0)
        self.assertGreater(changes[0]['decline_unexplained_by_prints'],0)

    def test_gap_censors_and_does_not_count_unseen_service(self):
        _,_,labels,_,_=analyze([book(1000),book(1040),tape(size=1000)])
        self.assertEqual(labels[0]['end_reason'],'gap')
        self.assertEqual(labels[0]['serviced_contracts'],0)
        self.assertTrue(labels[0]['censored_before_full'])

    def test_price_change_interval_not_silently_filled(self):
        _,_,labels,spells,_=analyze([book(1000),book(1010),book(1020,.41,.58),tape(at=1015,size=1000)])
        self.assertEqual(labels[0]['end_at'],1010)
        self.assertEqual(labels[0]['serviced_contracts'],0)
        self.assertEqual(spells[0]['change_interval_upper'],1020)

    def test_markout_requires_continuous_observation(self):
        books,_,_,_=normalize([book(1000),book(1060,.5,.49)])
        self.assertIsNone(markout(books['T'],1005,'yes',.4,30))

    def test_markout_no_side_sign(self):
        books,_,_,_=normalize([book(1000),book(1020,.41,.58),book(1040,.42,.57)])
        m=markout(books['T'],1005,'no',.59,30)
        self.assertAlmostEqual(m['midpoint_change_cents'],-2)

    def test_historical_future_publication_excluded(self):
        f=dict(at=1000,outcome='yes',price=.4,fee=0,size=1,outcome_mid_at_fill=.405)
        q=dict(at=1130,asof=1070,bid=.4,ask=.41)
        self.assertIsNone(future_mark([1130],[q],f,120))

    def test_historical_prefill_quote_not_markout(self):
        f=dict(at=1000,outcome='yes',price=.4,fee=0,size=1,outcome_mid_at_fill=.405)
        q=dict(at=1060,asof=1000,bid=.4,ask=.41)
        self.assertIsNone(future_mark([1060],[q],f,120))

    def test_historical_stale_quote_excluded(self):
        f=dict(at=1000,outcome='yes',price=.4,fee=0,size=1,outcome_mid_at_fill=.405)
        q=dict(at=1100,asof=1040,bid=.4,ask=.41)
        self.assertIsNone(future_mark([1100],[q],f,300))

    def test_historical_markout_sign_and_fee(self):
        f=dict(at=1000,outcome='no',price=.59,fee=.01,size=10,outcome_mid_at_fill=.595)
        q=dict(at=1120,asof=1060,bid=.42,ask=.43)
        m=future_mark([1120],[q],f,120)
        self.assertAlmostEqual(m['midpoint_change_cents'],-2)
        self.assertAlmostEqual(m['fee_adjusted_midpoint_markout_cents'],-1.6)

    def test_private_routes_are_unavailable(self):
        self.assertFalse(allowed('portfolio/orders'))
        self.assertFalse(allowed('markets/../portfolio/orders'))
        self.assertTrue(allowed('markets/trades'))

    def test_empty_holdout_cannot_pass(self):
        m=json.loads((Path(__file__).parent/'HOLDOUT_MANIFEST.json').read_text())
        r=check(m,{})
        self.assertEqual(r['status'],'INSUFFICIENT');self.assertEqual(r['completed_games'],0)

    def test_holdout_overlap_rejected(self):
        m=json.loads((Path(__file__).parent/'HOLDOUT_MANIFEST.json').read_text())
        r=check(m,dict(games=[dict(game_id=m['holdout_games'][0]['game_id'],event=m['development_events'][0])]))
        self.assertIn('Development/holdout overlap',r['reasons'])


if __name__=='__main__':unittest.main()
