"""Unit checks for the C1 KXUFCFIGHT null-scorecard scaffold.

Schema rows are field shapes. A passing test is not a fill and not profit.
"""
import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

import bakeoff
import feebook
import rails


ROOT = Path(__file__).resolve().parents[1]


def _by_id(rows):
    return {row['schema_id']: row for row in rows}


class BakeoffScaffoldTests(unittest.TestCase):
    def test_binding_imports_feebook_and_rails(self):
        binding = bakeoff.instrument_binding()
        pins = json.loads(bakeoff.SOURCE_PINS.read_text())
        hashes = bakeoff.dependency_hashes()
        self.assertEqual(binding['feebook_commit'], pins['feebook_dependency']['commit'])
        self.assertEqual(binding['rails_commit'], pins['rails_dependency']['commit'])
        self.assertTrue(binding['feebook_imported'])
        self.assertFalse(binding['feebook_copied'])
        self.assertTrue(binding['rails_imported'])
        self.assertFalse(binding['rails_copied'])
        self.assertEqual(binding['examiner_formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(binding['fee_credit_rule_id'], rails.FEE_CREDIT_RULE_ID)
        self.assertEqual(hashes['feebook_py_sha256'], pins['feebook_dependency']['feebook_py_sha256'])
        self.assertEqual(hashes['rails_py_sha256'], pins['rails_dependency']['rails_py_sha256'])
        self.assertEqual(binding['series'], 'KXUFCFIGHT')
        self.assertEqual(binding['series_resolution'], 'default_unknown_series')
        self.assertFalse(binding['series_override_added'])
        table = feebook.load_series_table()
        self.assertEqual(table.get('overrides'), {})

    def test_000_pointer_hashes_shadow_without_parsing(self):
        pointer = bakeoff.instrument_000_pointer()
        self.assertEqual(pointer['instrument_id'], '000')
        self.assertEqual(pointer['shadow_sha256'], bakeoff.SHADOW_SHA256)
        self.assertFalse(pointer['parsed_shadow_json'])
        self.assertFalse(pointer['reads_common_config'])
        self.assertFalse(pointer['retune'])
        self.assertFalse(pointer['strategy_port'])
        self.assertEqual(pointer['measurement_budget_usd'], Decimal('5000'))
        self.assertEqual(pointer['measurement_budget_role'], bakeoff.BUDGET_ROLE)

    def test_source_has_no_fee_literals_or_shadow_config(self):
        text = (ROOT / 'bakeoff.py').read_text()
        for token in (
            '0.07', '0.0175', 'starting_cash',
            'grok_unrounded', 'replay_v2', 'QueueInstrument',
            "['common_config']", '["common_config"]', '.common_config',
        ):
            self.assertNotIn(token, text)
        self.assertNotIn("Decimal('3300')", text)
        self.assertNotIn("Decimal('10000')", text)
        self.assertNotIn("'3300'", text)
        self.assertNotIn("'10000'", text)

    def test_budget_is_a_shared_label_and_not_spendable(self):
        binding = bakeoff.instrument_binding()
        self.assertEqual(binding['measurement_budget_usd'], Decimal('5000'))
        self.assertEqual(binding['measurement_budget_role'], 'measurement_contrast_label')
        self.assertFalse(binding['strategy_claim'])
        self.assertFalse(binding['q6_000_retune'])
        with self.assertRaises(bakeoff.MeasurementBudgetNotCapital):
            bakeoff.spend_measurement_budget(Decimal('1'))
        with self.assertRaises(bakeoff.StrategyPortRefused):
            bakeoff.port_strategy('KXUFCFIGHT')
        with self.assertRaises(bakeoff.Q6RetuneRefused):
            bakeoff.retune_000()
        with self.assertRaises(bakeoff.LiveOrdersForbidden):
            bakeoff.execution_adapter()

    def test_clock_admits_stamp_and_refuses_mz_and_roi(self):
        stub = bakeoff.collector_stub()
        self.assertEqual(stub['status'], 'READY')
        self.assertEqual(stub['clock'], 'ADMITTED')
        self.assertEqual(stub['stub_status'], 'PANEL_ADMITTED_C1_UFC_ONLY')
        self.assertEqual(stub['panel_version'], '2026-09-22.c1-kxufcfight-v0')
        self.assertEqual(stub['admitted_at'], '2026-09-23T00:49:43Z')
        self.assertEqual(stub['reported_settled_n'], 4)
        self.assertEqual(stub['admitted_settled_n'], 0)
        self.assertEqual(stub['events_n'], 2)
        self.assertEqual(stub['markets_n'], 4)
        self.assertEqual(stub['settled_n'], 0)
        self.assertTrue(stub['admitted'])
        self.assertFalse(stub['scorecard_filled_from_reported_settles'])
        for key in bakeoff.OUTPUT_KEYS:
            self.assertIsNone(stub[key])
        admitted = bakeoff.clock_admit()
        self.assertEqual(admitted['clock_admit'], 'ADMITTED')
        self.assertEqual(admitted['panel_sha256'], bakeoff.PANEL_SHA256)
        self.assertEqual(admitted['events_n'], 2)
        self.assertEqual(admitted['markets_n'], 4)
        self.assertTrue(admitted['fixture_join'])
        self.assertFalse(admitted['scorecard_filled_from_settles'])
        for key in bakeoff.OUTPUT_KEYS:
            self.assertIsNone(admitted[key])
        same = bakeoff.clock_admit('PANEL_ADMITTED_C1_UFC_ONLY')
        self.assertEqual(same['clock_admit'], 'ADMITTED')
        stamped = bakeoff.clock_admit('CONDITIONS_MET_COLLECTOR_STAMPED')
        self.assertEqual(stamped['panel_clock_admit'], 'CONDITIONS_MET_COLLECTOR_STAMPED')
        with self.assertRaises(bakeoff.ClockRefused):
            bakeoff.clock_admit('ADMIT_PASS')
        with self.assertRaises(bakeoff.ClockRefused):
            bakeoff.clock_admit('NOT_ADMITTED')
        with self.assertRaises(bakeoff.ScorecardRefused):
            bakeoff.mz([Decimal('0.5')])
        with self.assertRaises(bakeoff.ScorecardRefused):
            bakeoff.roi(Decimal('0.01'))
        rejoin = bakeoff.clock_rejoin()
        self.assertEqual(rejoin['clock_rejoin'], 'ADMITTED')
        self.assertEqual(rejoin['prior_scaffold_rejoin'], 'KICKED')
        self.assertEqual(rejoin['reported_settled_n'], 4)
        self.assertEqual(rejoin['resolutions_applied'], 4)
        self.assertTrue(rejoin['admitted'])
        self.assertFalse(rejoin['scorecard_filled_from_settles'])
        for key in bakeoff.OUTPUT_KEYS:
            self.assertIsNone(rejoin[key])
        with self.assertRaises(bakeoff.ClockRefused):
            bakeoff.apply_resolutions([{'resolution': 'yes'}])
        with self.assertRaises(bakeoff.ScorecardRefused):
            bakeoff.apply_resolutions([{'pnl': '1.00'}])
        with self.assertRaises(bakeoff.ScorecardRefused):
            bakeoff.write_scorecard(results=None, pnl=None, MZ=None, roi=None)
        with self.assertRaises(bakeoff.ScorecardRefused):
            bakeoff.write_scorecard(results='1', pnl='1')

    def test_lee_ready_refused_even_with_native_fields_and_a_mid(self):
        with self.assertRaises(bakeoff.LeeReadyRefused):
            bakeoff.lee_ready(price='0.60', mid='0.50')
        with self.assertRaises(bakeoff.LeeReadyRefused):
            bakeoff.lee_ready(price='0.40', mid='0.50')
        row = {
            'schema_only': True,
            'lee_ready': True,
            'taker_outcome_side': 'yes',
            'taker_book_side': 'bid',
            'mid': '0.50',
            'yes_price_dollars': '0.60',
        }
        with self.assertRaises(bakeoff.LeeReadyRefused):
            bakeoff.classify_taker(row)
        arm = {'arm_id': 'KXUFCFIGHT', 'series': 'KXUFCFIGHT'}
        with self.assertRaises(bakeoff.LeeReadyRefused):
            bakeoff.label_schema_row(row, arm, bakeoff.FreshnessCursor())

    def test_native_taker_fields(self):
        yes = bakeoff.classify_taker({
            'taker_outcome_side': 'yes',
            'taker_book_side': 'bid',
            'mid': '0.40',
        })
        self.assertEqual(yes['taker_outcome_side'], 'yes')
        self.assertEqual(yes['maker_outcome_side'], 'no')
        self.assertEqual(yes['classification'], 'native_public_taker')
        self.assertIsNone(yes['lee_ready'])
        no = bakeoff.classify_taker({
            'taker_outcome_side': 'no',
            'taker_book_side': 'ask',
        })
        self.assertEqual(no['taker_outcome_side'], 'no')
        self.assertEqual(no['maker_outcome_side'], 'yes')
        legacy = bakeoff.classify_taker({'taker_side': 'yes'})
        self.assertEqual(legacy['native_fields'], ['taker_side'])
        self.assertEqual(legacy['taker_outcome_side'], 'yes')
        with self.assertRaises(bakeoff.TakerFieldRefused):
            bakeoff.classify_taker({
                'taker_outcome_side': 'yes',
                'taker_book_side': 'ask',
            })
        with self.assertRaises(bakeoff.TakerFieldRefused):
            bakeoff.classify_taker({'yes_price_dollars': '0.40', 'is_taker': True})
        with self.assertRaises(bakeoff.TakerFieldRefused):
            bakeoff.classify_taker({'taker_sign': 'yes'})

    def test_queue_labels_come_from_rails_and_absent_stays_null(self):
        pinned = bakeoff.pinned_queue_labels()
        self.assertEqual(pinned['q3300'], rails.scenario_queue('q3300'))
        self.assertEqual(pinned['q10000'], rails.scenario_queue('q10000'))
        missing = bakeoff.queue_label(None)
        self.assertIsNone(missing['queue_attribution_bin'])
        self.assertIsNone(missing['observed_queue_ahead'])
        self.assertIsNone(missing['awarded_fill'])
        exact = bakeoff.queue_label(pinned['q3300'], 'q3300')
        self.assertEqual(exact['queue_attribution_bin'], 'q3300')
        self.assertFalse(exact['queue_bin_mismatch'])
        self.assertIsNone(exact['observed_queue_ahead'])
        stress = bakeoff.queue_label(pinned['q10000'], 'q3300')
        self.assertEqual(stress['queue_attribution_bin'], 'q10000')
        self.assertTrue(stress['queue_bin_mismatch'])
        outside = bakeoff.queue_label('100', 'q3300')
        self.assertEqual(outside['queue_attribution_bin'], 'outside_pinned_bins')
        self.assertTrue(outside['queue_bin_mismatch'])
        with self.assertRaises(TypeError):
            bakeoff.queue_label(3300.0)
        with self.assertRaises(ValueError):
            bakeoff.queue_label('-1')

    def test_freshness_labels_follow_rails(self):
        cursor = bakeoff.FreshnessCursor()
        book = {'yes_dollars': [['0.4200', '12']], 'no_dollars': [['0.5100', '9']]}
        first = cursor.observe(book, '2026-09-22T18:00:00Z', False)
        self.assertTrue(first['content_fresh_flag'])
        self.assertEqual(first['reason'], 'initial')
        keepalive = cursor.observe(book, '2026-09-22T18:00:01Z', True)
        self.assertFalse(keepalive['content_fresh_flag'])
        self.assertEqual(keepalive['reason'], 'keepalive_ignored')
        same = cursor.observe(book, '2026-09-22T18:00:00Z', False)
        self.assertFalse(same['content_fresh_flag'])
        self.assertEqual(same['reason'], 'unchanged')
        timed = cursor.observe(book, '2026-09-22T18:00:02Z', False)
        self.assertTrue(timed['content_fresh_flag'])
        self.assertEqual(timed['reason'], 'transaction_time_changed')
        other = {'yes_dollars': [['0.3000', '5']], 'no_dollars': [['0.6000', '5']]}
        changed = cursor.observe(other, '2026-09-22T18:00:03Z', False)
        self.assertTrue(changed['content_fresh_flag'])
        self.assertEqual(changed['reason'], 'content_changed')

    def test_maker_credit_refuse_is_a_label(self):
        refused = bakeoff.maker_credit_label('0.01', '1', series='KXUFCFIGHT')
        self.assertTrue(refused['maker_credit_floor_zero_refuse'])
        self.assertFalse(refused['admitted'])
        self.assertFalse(refused['placed_order'])
        self.assertEqual(refused['rule_id'], rails.FEE_CREDIT_RULE_ID)
        self.assertEqual(refused['formula_id'], feebook.EXAMINER_FORMULA_ID)
        direct = rails.maker_quote_credit('0.01', '1', series='KXUFCFIGHT')
        self.assertEqual(refused['credit'], direct['credit'])

    def test_fee_probe_matches_feebook_and_does_not_award_a_fill(self):
        payload = bakeoff.load_schema_fixture()
        arm = payload['arms'][0]
        row = arm['rows'][0]
        labeled = bakeoff.label_schema_row(row, arm, bakeoff.FreshnessCursor())
        probe = feebook.polarity_fill(
            {'orderbook_fp': row['orderbook_fp']},
            'yes',
            '1',
            round_up=True,
            series='KXUFCFIGHT',
        )
        self.assertEqual(labeled['taker_quote']['fee'], probe['taker_fee']['fee'])
        self.assertEqual(labeled['maker_quote']['fee'], probe['maker_fee']['fee'])
        self.assertEqual(labeled['formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(labeled['series_resolution'], 'default_unknown_series')
        self.assertEqual(labeled['maker_outcome_side'], 'no')
        self.assertIsNone(labeled['awarded_fill'])
        self.assertFalse(labeled['size_exceeds_touch'])
        self.assertFalse(labeled['maker_credit']['placed_order'])
        self.assertEqual(labeled['maker_credit']['fee'], labeled['maker_quote']['fee'])
        self.assertIsNone(labeled['scorecard_label'])
        for key in bakeoff.OUTPUT_KEYS:
            self.assertIsNone(labeled[key])
        channel = labeled['fee_channel']
        would = feebook.classify_scorecard({
            'inventory_flat': True,
            'fee_channel': channel,
        })
        self.assertEqual(would, 'completed_profit')
        self.assertIsNone(labeled['scorecard_label'])

    def test_missing_taker_and_incomplete_book_do_not_invent_a_side(self):
        payload = bakeoff.load_schema_fixture()
        arm = payload['arms'][0]
        rows = _by_id(arm['rows'])
        missing = bakeoff.label_schema_row(
            rows['schema_ufc_no_taker'], arm, bakeoff.FreshnessCursor(),
        )
        self.assertIsNone(missing['taker_outcome_side'])
        self.assertIsNone(missing['taker_quote'])
        self.assertIsNone(missing['maker_quote'])
        self.assertIsNone(missing['awarded_fill'])
        self.assertEqual(missing['freshness']['reason'], 'initial')
        with self.assertRaises(feebook.BookIncomplete):
            bakeoff.label_schema_row(
                rows['schema_ufc_incomplete_book'], arm, bakeoff.FreshnessCursor(),
            )
        book = feebook.reciprocal_book(
            {'orderbook_fp': rows['schema_ufc_incomplete_book']['orderbook_fp']},
        )
        self.assertIsNone(book['ask_yes'])
        self.assertIsNone(book['spread_yes'])

    def test_invented_fill_key_is_refused(self):
        arm = {'arm_id': 'KXUFCFIGHT', 'series': 'KXUFCFIGHT'}
        row = {
            'schema_id': 'bad_fill',
            'schema_only': True,
            'series': 'KXUFCFIGHT',
            'taker_outcome_side': 'yes',
            'fill_count': '1',
        }
        with self.assertRaises(bakeoff.InventedFillRefused):
            bakeoff.label_schema_row(row, arm, bakeoff.FreshnessCursor())

    def test_walk_keeps_both_arms_on_one_label_and_a_null_scorecard(self):
        frozen_before = bakeoff.FROZEN_EXPERIMENT.read_bytes()
        empty_before = bakeoff.EMPTY_RESULTS.read_bytes()
        walked = bakeoff.walk_schema()
        self.assertEqual(bakeoff.FROZEN_EXPERIMENT.read_bytes(), frozen_before)
        self.assertEqual(bakeoff.EMPTY_RESULTS.read_bytes(), empty_before)
        self.assertTrue(walked['same_measurement_budget'])
        self.assertEqual(walked['measurement_budget_usd'], Decimal('5000'))
        self.assertEqual(walked['measurement_budget_role'], 'measurement_contrast_label')
        self.assertFalse(walked['strategy_claim'])
        self.assertIsNone(walked['winner'])
        self.assertEqual(walked['clock'], 'NOT_ADMITTED')
        self.assertEqual(walked['clock_rejoin'], 'KICKED')
        self.assertEqual(walked['awaiting'], 'CLOCK_ADMIT_PASS')
        self.assertEqual(walked['reported_settled_n'], 4)
        self.assertEqual(walked['admitted_settled_n'], 0)
        self.assertEqual(walked['settled_n'], 0)
        for key in bakeoff.OUTPUT_KEYS:
            self.assertIsNone(walked[key])
        ufc, pointer = walked['arms']
        self.assertEqual(ufc['arm_id'], 'KXUFCFIGHT')
        self.assertEqual(ufc['series_resolution'], 'default_unknown_series')
        self.assertEqual(pointer['arm_id'], '000')
        self.assertIsNone(pointer['series'])
        self.assertEqual(pointer['series_resolution'], 'default')
        self.assertEqual(ufc['measurement_budget_usd'], pointer['measurement_budget_usd'])
        self.assertFalse(pointer['retune'])
        self.assertIsNone(ufc['observed_queue_ahead'])
        self.assertIsNone(pointer['observed_queue_ahead'])
        self.assertIsNone(ufc['queue_bin_mismatch_rate'])
        self.assertIsNone(ufc['awarded_fill'])
        self.assertIsNone(pointer['awarded_fill'])
        ufc_labeled = _by_id(ufc['labeled'])
        self.assertEqual(ufc_labeled['schema_ufc_yes_bid']['freshness']['reason'], 'initial')
        self.assertEqual(
            ufc_labeled['schema_ufc_keepalive']['freshness']['reason'],
            'keepalive_ignored',
        )
        self.assertIsNone(ufc_labeled['schema_ufc_keepalive']['taker_quote'])
        self.assertEqual(
            ufc_labeled['schema_ufc_time_changed']['freshness']['reason'],
            'transaction_time_changed',
        )
        self.assertIsNotNone(ufc_labeled['schema_ufc_time_changed']['taker_quote'])
        self.assertIsNone(ufc_labeled['schema_ufc_time_changed']['awarded_fill'])
        self.assertEqual(
            ufc_labeled['schema_ufc_no_taker']['freshness']['reason'],
            'content_changed',
        )
        self.assertIsNone(ufc_labeled['schema_ufc_no_taker']['classification'])
        q3300 = ufc_labeled['schema_queue_q3300_vector']['queue']
        self.assertEqual(q3300['queue_attribution_bin'], 'q3300')
        self.assertFalse(q3300['queue_bin_mismatch'])
        self.assertFalse(q3300['queue_ahead_is_observation'])
        outside = ufc_labeled['schema_queue_outside_vector']['queue']
        self.assertEqual(outside['queue_attribution_bin'], 'outside_pinned_bins')
        self.assertTrue(outside['queue_bin_mismatch'])
        reasons = {item['schema_id']: item['reason'] for item in ufc['refusals']}
        self.assertEqual(reasons['schema_ufc_taker_disagree'], 'TakerFieldRefused')
        self.assertEqual(reasons['schema_ufc_incomplete_book'], 'BookIncomplete')
        self.assertEqual(reasons['schema_ufc_lee_ready'], 'LeeReadyRefused')
        self.assertEqual(reasons['schema_ufc_invented_fill'], 'InventedFillRefused')
        for item in ufc['refusals']:
            self.assertIsNone(item['awarded_fill'])
            for key in bakeoff.OUTPUT_KEYS:
                self.assertIsNone(item[key])
        pointer_labeled = _by_id(pointer['labeled'])
        first = pointer_labeled['schema_000_yes_bid']
        self.assertEqual(first['freshness']['reason'], 'initial')
        self.assertEqual(first['series_resolution'], 'default')
        self.assertEqual(first['taker_outcome_side'], 'yes')
        self.assertIsNone(first['awarded_fill'])
        probe = feebook.polarity_fill(
            {'orderbook_fp': {
                'yes_dollars': [['0.5500', '4']],
                'no_dollars': [['0.4000', '6']],
            }},
            'yes',
            '1',
            round_up=True,
            series=None,
        )
        self.assertEqual(first['taker_quote']['fee'], probe['taker_fee']['fee'])
        self.assertEqual(
            pointer_labeled['schema_000_keepalive']['freshness']['reason'],
            'keepalive_ignored',
        )
        unchanged = pointer_labeled['schema_000_unchanged']
        self.assertEqual(unchanged['freshness']['reason'], 'unchanged')
        self.assertEqual(unchanged['taker_outcome_side'], 'no')
        self.assertEqual(unchanged['maker_outcome_side'], 'yes')
        self.assertIsNone(unchanged['awarded_fill'])
        self.assertEqual(pointer['refusals'], [])
        snapshot = bakeoff.frozen_output_snapshot()
        for key in bakeoff.OUTPUT_KEYS:
            self.assertIsNone(snapshot[key])
        self.assertIsNone(snapshot['winner'])
        empty = json.loads(bakeoff.EMPTY_RESULTS.read_text())
        for key in bakeoff.OUTPUT_KEYS:
            self.assertIsNone(empty[key])
        self.assertIsNone(empty['winner'])
        self.assertEqual(empty['status'], 'EMPTY')
        self.assertEqual(empty['measurement_budget_role'], 'measurement_contrast_label')
        self.assertEqual(empty['clock'], 'ADMITTED')
        self.assertEqual(empty['panel_version'], '2026-09-22.c1-kxufcfight-v0')
        self.assertEqual(empty['admitted_at'], '2026-09-23T00:49:43Z')
        self.assertEqual(empty['panel_sha256'], bakeoff.PANEL_SHA256)
        self.assertEqual(empty['reported_settled_n'], 4)
        self.assertEqual(empty['admitted_settled_n'], 0)
        self.assertFalse(empty['scorecard_filled_from_reported_settles'])

    def test_resolution_hook_joins_admitted_labels_and_refuses_pnl(self):
        frozen_before = bakeoff.FROZEN_EXPERIMENT.read_bytes()
        empty_before = bakeoff.EMPTY_RESULTS.read_bytes()
        panel_bytes = bakeoff.CAPTURE_PANEL.read_bytes()
        fixture_bytes = bakeoff.FIXTURE_PANEL.read_bytes()
        self.assertEqual(fixture_bytes, panel_bytes)
        self.assertEqual(bakeoff._sha256(bakeoff.FIXTURE_PANEL), bakeoff.PANEL_SHA256)
        wired = bakeoff.wire_resolution_hook()
        self.assertEqual(bakeoff.FROZEN_EXPERIMENT.read_bytes(), frozen_before)
        self.assertEqual(bakeoff.EMPTY_RESULTS.read_bytes(), empty_before)
        self.assertEqual(bakeoff.CAPTURE_PANEL.read_bytes(), panel_bytes)
        self.assertEqual(wired['label'], 'ADMITTED_FIXTURE_JOIN')
        self.assertEqual(wired['clock_admit'], 'ADMITTED')
        self.assertEqual(wired['stub_status'], 'PANEL_ADMITTED_C1_UFC_ONLY')
        self.assertEqual(wired['panel_version'], '2026-09-22.c1-kxufcfight-v0')
        self.assertEqual(wired['panel_sha256'], bakeoff.PANEL_SHA256)
        self.assertEqual(wired['reported_settled_n'], 4)
        self.assertEqual(wired['admitted_settled_n'], 0)
        self.assertEqual(wired['events_n'], 2)
        self.assertEqual(wired['markets_n'], 4)
        self.assertEqual(wired['resolutions_applied'], 4)
        self.assertEqual(
            wired['result_labels'],
            ['yes', 'no', 'no', 'yes'],
        )
        self.assertFalse(wired['payoff_computed'])
        self.assertFalse(wired['resolution_capture_bytes_in_checkout'])
        self.assertFalse(wired['scorecard_filled_from_settles'])
        self.assertTrue(wired['admitted'])
        self.assertIsNone(wired['winner'])
        for key in bakeoff.OUTPUT_KEYS:
            self.assertIsNone(wired[key])
        capture = bakeoff.resolution_capture_status()
        self.assertFalse(capture['bytes_in_checkout'])
        self.assertEqual(capture['files'], [])
        with self.assertRaises(bakeoff.ClockRefused):
            bakeoff.wire_resolution_hook(bakeoff.NOT_ADMITTED_FIXTURE)
        payload = json.loads(bakeoff.RESOLUTION_FIXTURE.read_text())
        payload['rows'][0]['result_observed_live_get'] = 'no'
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'flipped.json'
            path.write_text(json.dumps(payload))
            with self.assertRaises(bakeoff.BakeoffError):
                bakeoff.wire_resolution_hook(path)
        payload = json.loads(bakeoff.RESOLUTION_FIXTURE.read_text())
        payload['rows'][1]['pnl'] = '1.00'
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'pnl.json'
            path.write_text(json.dumps(payload))
            with self.assertRaises(bakeoff.ScorecardRefused):
                bakeoff.load_resolution_hook(path)
        self.assertEqual(bakeoff.FROZEN_EXPERIMENT.read_bytes(), frozen_before)
        self.assertEqual(bakeoff.EMPTY_RESULTS.read_bytes(), empty_before)

    def test_loader_rejects_a_different_budget_and_an_observed_queue(self):
        payload = json.loads(bakeoff.SCHEMA_FIXTURE.read_text())
        payload['arms'][1]['measurement_budget_usd'] = '4999'
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'budget.json'
            path.write_text(json.dumps(payload))
            with self.assertRaises(bakeoff.BudgetContrastRefused):
                bakeoff.load_schema_fixture(path)
        payload = json.loads(bakeoff.SCHEMA_FIXTURE.read_text())
        payload['arms'][0]['rows'][0]['queue_ahead_is_observation'] = True
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'queue.json'
            path.write_text(json.dumps(payload))
            with self.assertRaises(bakeoff.SchemaOnlyRefused):
                bakeoff.load_schema_fixture(path)


if __name__ == '__main__':
    unittest.main()
