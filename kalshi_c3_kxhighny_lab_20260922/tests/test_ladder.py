"""Unit checks for the C3-KXHIGHNY bordering-strike scaffold.

Code verification only. The checks do not fill results, pnl, MZ, or ROI.
"""
import copy
import json
import sys
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import ladder


class BindingTests(unittest.TestCase):
    def test_imports_feebook_and_rails_without_a_retune(self):
        binding = ladder.instrument_binding()
        self.assertEqual(binding['examiner_formula_id'], ladder.feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(binding['fee_credit_rule_id'], ladder.rails.FEE_CREDIT_RULE_ID)
        self.assertEqual(binding['feebook_commit'], '22371178cb2663250b4762f328069571c48cb551')
        self.assertEqual(binding['rails_commit'], '6a28e0d6254327ea4e6451c781bec56215ac6cac')
        self.assertEqual(binding['queue_q3300'], ladder.rails.scenario_queue('q3300'))
        self.assertEqual(binding['queue_q10000'], ladder.rails.scenario_queue('q10000'))
        self.assertFalse(binding['queue_labels_are_a_knob'])
        self.assertFalse(binding['q6_000_retune'])
        self.assertFalse(binding['algo_ported'])
        self.assertEqual(binding['stations']['KXHIGHNY']['nws_station'], 'KNYC')
        self.assertEqual(binding['stations']['KXHIGHCHI']['nws_station'], 'KMDW')
        self.assertFalse(binding['later_r3_p3_panel']['joined_now'])

    def test_hypothesis_carries_no_roi(self):
        record = ladder.weather_spread_hypothesis()
        self.assertEqual(record['blob_sha'], '323463cd7538464dfe90ec8b6acea9c76e10ee29')
        self.assertFalse(record['algo_ported'])
        self.assertFalse(record['sum_of_mids_computed_here'])
        self.assertIsNone(record['ROI'])
        self.assertIsNone(record['pnl'])
        self.assertIsNone(record['MZ'])
        self.assertIsNone(record['results'])

    def test_collector_stub_is_ready_and_the_clock_is_refused(self):
        stub = ladder.collector_stub()
        self.assertEqual(stub['status'], 'READY')
        self.assertEqual(stub['clock'], 'REFUSED')
        self.assertEqual(stub['settled_n'], 0)
        self.assertFalse(stub['admitted_settled_panel'])
        self.assertFalse(stub['later_r3_p3_panel']['native_taker_fields_present'])
        for key in ladder.OUTPUT_KEYS:
            self.assertIsNone(stub[key])

    def test_refused_paths_raise(self):
        with self.assertRaises(ladder.AdmitRefused):
            ladder.clock_admit()
        with self.assertRaises(ladder.ScorecardRefused):
            ladder.scorecard_refuse()
        with self.assertRaises(ladder.ScorecardRefused):
            ladder.write_scorecard({'pnl': Decimal('1')})
        with self.assertRaises(ladder.ScorecardRefused):
            ladder.mincer_zarnowitz()
        with self.assertRaises(ladder.ScorecardRefused):
            ladder.roi()
        with self.assertRaises(ladder.LiveOrdersForbidden):
            ladder.execution_adapter()
        with self.assertRaises(ladder.AlgoPortRefused):
            ladder.port_weather_algorithm()
        with self.assertRaises(ladder.InventedFillRefused):
            ladder.award_queue_fill()


class LadderShapeTests(unittest.TestCase):
    def setUp(self):
        self.walk = ladder.simulate_ladder()
        self.by_id = {event['schema_id']: event for event in self.walk['events']}
        self.refusals = {row['schema_id']: row for row in self.walk['refusals']}

    def test_new_york_has_two_borders_and_one_gap(self):
        event = self.by_id['ny_documented_shape']
        self.assertEqual(event['station']['nws_station'], 'KNYC')
        self.assertEqual(
            [pair['colder_ticker'] + '|' + pair['warmer_ticker'] for pair in event['borders']],
            [
                'KXHIGHNY-26SEP23-T75|KXHIGHNY-26SEP23-B7677',
                'KXHIGHNY-26SEP23-B7677|KXHIGHNY-26SEP23-B7879',
            ],
        )
        self.assertEqual(len(event['gaps']), 1)
        gap = event['gaps'][0]
        self.assertEqual(gap['degree_gap'], Decimal('4'))
        self.assertEqual(gap['uncovered_degrees'], Decimal('3'))
        self.assertFalse(gap['inserted_rung'])
        self.assertEqual(event['freshness']['reason'], 'initial')
        self.assertTrue(event['freshness']['fresh'])
        self.assertIsNone(event['sum_of_mids'])
        self.assertFalse(event['native_taker_fields_present'])

    def test_input_order_does_not_decide_the_border(self):
        event = ladder.load_schema_fixture()['events'][0]
        reversed_rungs = list(reversed(event['rungs']))
        parsed = ladder._parse_event(dict(event, rungs=reversed_rungs))
        paired = ladder.bordering_pairs(parsed['rungs'])
        self.assertEqual(paired['borders'][0]['colder_ticker'], 'KXHIGHNY-26SEP23-T75')
        self.assertEqual(len(paired['borders']), 2)
        self.assertEqual(len(paired['gaps']), 1)

    def test_chicago_interior_is_one_border(self):
        event = self.by_id['chi_interior_border']
        self.assertEqual(event['station']['nws_station'], 'KMDW')
        self.assertEqual(event['station']['identity_note'], 'Midway')
        self.assertEqual(len(event['borders']), 1)
        self.assertEqual(event['borders'][0]['degree_gap'], Decimal('1'))
        self.assertEqual(event['gaps'], [])

    def test_reciprocal_spread_uses_the_imported_book(self):
        event = self.by_id['ny_documented_shape']
        rung = next(row for row in event['rungs'] if row['ticker'].endswith('B7677'))
        self.assertEqual(rung['book']['bid_yes'], Decimal('0.40'))
        self.assertEqual(rung['book']['bid_no'], Decimal('0.55'))
        self.assertEqual(rung['book']['spread_yes'], Decimal('0.05'))
        self.assertEqual(rung['book']['ask_yes'], Decimal('0.45'))
        admission = rung['maker_admission']
        self.assertEqual(admission['formula_id'], ladder.feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(admission['rule_id'], ladder.rails.FEE_CREDIT_RULE_ID)
        self.assertEqual(admission['series_resolution'], 'default_unknown_series')
        self.assertTrue(admission['admitted'])
        self.assertEqual(admission['contracts'], Decimal('1'))
        self.assertIsNone(rung['awarded_fill'])
        for key in ladder.OUTPUT_KEYS:
            self.assertIsNone(rung[key])

    def test_one_cent_yes_bid_is_refused_by_the_rail(self):
        event = self.by_id['chi_fee_blind_cent']
        self.assertEqual(event['borders'], [])
        rung = event['rungs'][0]
        self.assertFalse(rung['maker_admission']['admitted'])
        self.assertEqual(rung['maker_admission']['credit'], Decimal('0.00'))
        parsed = ladder._parse_event(
            next(row for row in ladder.load_schema_fixture()['events']
                 if row['schema_id'] == 'chi_fee_blind_cent')
        )
        with self.assertRaises(ladder.rails.MakerCreditRefused):
            ladder.admit_rung_quote(parsed['rungs'][0])
        for key in ladder.OUTPUT_KEYS:
            self.assertIsNone(event[key])

    def test_missing_yes_bid_stays_unset(self):
        event = self.by_id['ny_missing_yes']
        book = event['rungs'][0]['book']
        self.assertIsNone(book['bid_yes'])
        self.assertIsNone(book['spread_yes'])
        self.assertEqual(book['ask_yes'], Decimal('0.38'))
        self.assertIsNone(event['rungs'][0]['maker_admission'])

    def test_overlap_and_miami_are_refusals(self):
        self.assertEqual(self.refusals['chi_overlap']['reason'], 'LadderDefect')
        self.assertEqual(self.refusals['mia_out_of_scope']['reason'], 'SeriesRefused')
        self.assertNotIn('chi_overlap', self.by_id)
        for row in self.refusals.values():
            self.assertIsNone(row['awarded_fill'])
            for key in ladder.OUTPUT_KEYS:
                self.assertIsNone(row[key])

    def test_fractional_strike_is_a_defect(self):
        event = copy.deepcopy(ladder.load_schema_fixture()['events'][1])
        event['rungs'][0]['floor_strike'] = '64.5'
        with self.assertRaises(ladder.LadderDefect):
            ladder._parse_event(event)

    def test_float_strike_is_rejected(self):
        event = copy.deepcopy(ladder.load_schema_fixture()['events'][1])
        event['rungs'][0]['floor_strike'] = 64.0
        with self.assertRaises(TypeError):
            ladder._parse_event(event)


class ScorecardTests(unittest.TestCase):
    def test_walk_and_freeze_stay_null(self):
        frozen_before = ladder.FROZEN_EXPERIMENT.read_text()
        empty_before = ladder.EMPTY_RESULTS.read_text()
        walked = ladder.simulate_ladder()
        self.assertEqual(walked['collector'], 'READY')
        self.assertEqual(walked['clock'], 'REFUSED')
        self.assertEqual(walked['settled_n'], 0)
        self.assertFalse(walked['invented_fills'])
        self.assertFalse(walked['later_r3_p3_panel']['joined_now'])
        self.assertFalse(walked['later_r3_p3_panel']['native_taker_fields_present'])
        for key in ladder.OUTPUT_KEYS:
            self.assertIsNone(walked[key])
            self.assertIsNone(ladder.frozen_output_snapshot()[key])
        self.assertEqual(ladder.FROZEN_EXPERIMENT.read_text(), frozen_before)
        self.assertEqual(ladder.EMPTY_RESULTS.read_text(), empty_before)
        empty = json.loads(empty_before)
        self.assertEqual(ladder.empty_outputs(), empty)
        self.assertIsNone(empty['ROI'])

    def test_in_memory_settled_fill_is_refused(self):
        text = ladder.SCHEMA_FIXTURE.read_text()
        for banned in ('"result"', '"fill"', '"fills"', '"resolution"', '"pnl"'):
            self.assertNotIn(banned, text)
        event = copy.deepcopy(ladder.load_schema_fixture()['events'][0])
        event['rungs'][0]['result'] = 'yes'
        with self.assertRaises(ladder.SettledFillRefused):
            ladder._parse_event(event)
        self.assertEqual(ladder.SCHEMA_FIXTURE.read_text(), text)

    def test_freshness_keepalive_is_not_a_new_book(self):
        event = ladder._parse_event(ladder.load_schema_fixture()['events'][0])
        first = ladder.ladder_observation(event)
        second = ladder.ladder_observation(event)
        initial = ladder.judge_ladder_freshness(None, first)
        unchanged = ladder.judge_ladder_freshness(first, second)
        kept = ladder.judge_ladder_freshness(first, second, keepalive=True)
        self.assertEqual(initial.reason, 'initial')
        self.assertTrue(initial.fresh)
        self.assertEqual(unchanged.reason, 'unchanged')
        self.assertFalse(unchanged.fresh)
        self.assertEqual(kept.reason, 'keepalive_ignored')
        self.assertFalse(kept.fresh)

    def test_module_has_no_forecast_client(self):
        source = (ROOT / 'ladder.py').read_text()
        for banned in ('open-meteo', 'api.weather.gov', 'urllib', 'requests', 'QueueInstrument', 'role_pnl'):
            self.assertNotIn(banned, source)


if __name__ == '__main__':
    unittest.main()
