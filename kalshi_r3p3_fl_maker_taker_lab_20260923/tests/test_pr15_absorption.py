"""PR15 unit ideas absorbed into the 20260923 harness.

Draft PR15's lab directory is not created. Native taker_* fields classify.
Lee-Ready raises. The pinned 10¢ registry is not rebinned. Feebook quotes
stay off the freeze scorecard. MZ and band_roi stay null.
"""
import inspect
import json
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT.parent
import sys
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(PARENT / 'kalshi_feebook_lab_20260922'))

import feebook
import orchestrator


def _freeze_bytes():
    return {
        orchestrator.FROZEN_EXPERIMENT: orchestrator.FROZEN_EXPERIMENT.read_bytes(),
        orchestrator.EMPTY_RESULTS: orchestrator.EMPTY_RESULTS.read_bytes(),
    }


class AbsorptionTests(unittest.TestCase):
    def test_pr15_lab_directory_is_not_created(self):
        self.assertFalse((PARENT / orchestrator.SUPERSEDED_LAB).exists())
        binding = orchestrator.instrument_binding()
        self.assertEqual(binding['supersedes_pr'], 15)
        self.assertIs(binding['superseded_lab_present'], False)
        self.assertIs(binding['feebook_imported'], True)
        self.assertIs(binding['feebook_copied'], False)
        self.assertEqual(
            binding['symbols'],
            ('order_fee', 'examiner_fee_channel', 'TAKER_FILLS_RESTING'),
        )
        self.assertFalse((ROOT / 'feebook.py').exists())
        self.assertEqual(
            Path(feebook.__file__).resolve(),
            (PARENT / 'kalshi_feebook_lab_20260922' / 'feebook.py').resolve(),
        )

    def test_lee_ready_has_no_successful_path(self):
        samples = (
            {'price': '0.80', 'mid': '0.50'},
            {'price': '0.20', 'mid': '0.50'},
            {'price': '0.50', 'mid': '0.50', 'prev_price': '0.49'},
            {'price': '0.50', 'mid': '0.50', 'prev_price': '0.51'},
            {'taker_outcome_side': 'yes', 'yes_price_dollars': '0.40', 'no_price_dollars': '0.60'},
        )
        for sample in samples:
            with self.assertRaises(orchestrator.LeeReadyRefused):
                orchestrator.lee_ready(sample)
        with self.assertRaises(orchestrator.LeeReadyRefused):
            orchestrator.classify_taker({
                'taker_outcome_side': 'yes',
                'taker_book_side': 'bid',
                'lee_ready': True,
            })
        with self.assertRaises(orchestrator.LeeReadyRefused):
            orchestrator.classify_taker({
                'yes_price_dollars': '0.80',
                'classifier': 'Lee-Ready',
            })
        source = inspect.getsource(orchestrator.lee_ready)
        self.assertNotIn('return', source)
        self.assertNotIn('mid', source)
        self.assertIn('LeeReadyRefused', source)
        text = (ROOT / 'orchestrator.py').read_text()
        for banned in ('2.6', '0.026', '-9.64', '-31.46', 'classify_scorecard', '0.0175', '0.07'):
            self.assertNotIn(banned, text)

    def test_native_taker_fields_agree_and_quote_fields_do_not_vote(self):
        classified = orchestrator.classify_taker({
            'taker_outcome_side': 'yes',
            'taker_book_side': 'bid',
            'taker_side': 'yes',
            'lee_ready': 'REFUSED',
        })
        self.assertEqual(classified['taker_outcome_side'], 'yes')
        self.assertEqual(classified['taker_book_side'], 'bid')
        self.assertEqual(classified['maker_outcome_side'], 'no')
        self.assertEqual(
            classified['maker_outcome_side'],
            feebook.TAKER_FILLS_RESTING['yes'],
        )
        self.assertIsNone(classified['lee_ready'])
        book_only = orchestrator.classify_taker({'taker_book_side': 'ask'})
        self.assertEqual(book_only['taker_outcome_side'], 'no')
        self.assertEqual(book_only['maker_outcome_side'], 'yes')
        self.assertEqual(book_only['native_fields'], ['taker_book_side'])
        legacy = orchestrator.classify_taker({'taker_side': 'yes'})
        self.assertEqual(legacy['native_fields'], ['taker_side'])
        self.assertEqual(legacy['taker_book_side'], 'bid')
        with self.assertRaises(orchestrator.TakerFieldRefused):
            orchestrator.classify_taker({'is_taker': True, 'side': 'yes', 'action': 'buy'})
        with self.assertRaises(orchestrator.TakerFieldRefused):
            orchestrator.classify_taker({
                'taker_outcome_side': 'yes',
                'taker_fees_dollars': '1',
            })
        with self.assertRaises(orchestrator.TakerFieldRefused):
            orchestrator.classify_taker({
                'taker_outcome_side': 'yes',
                'taker_book_side': 'ask',
            })
        with self.assertRaises(orchestrator.TakerFieldRefused):
            orchestrator.classify_taker({
                'yes_price_dollars': '0.80',
                'no_price_dollars': '0.20',
                'mid': '0.40',
                'prev_price': '0.30',
            })

    def test_outcomes_do_not_rebin_and_floats_are_rejected(self):
        with self.assertRaises(orchestrator.RebinRefused):
            orchestrator.assign_band('0.40', outcome='yes')
        with self.assertRaises(orchestrator.RebinRefused):
            orchestrator.assign_band('0.40', outcome=None)
        with self.assertRaises(orchestrator.RebinRefused):
            orchestrator.rebin_after_outcomes([{'price': '0.40', 'outcome': 1}])
        with self.assertRaises(TypeError):
            orchestrator.assign_band(0.4)
        with self.assertRaises(TypeError):
            orchestrator.assign_band(True)
        self.assertEqual(orchestrator.assign_band('0.10'), 'b01')
        self.assertEqual(orchestrator.assign_band('1.00'), 'b09')

    def test_schema_walk_joins_three_rows_and_leaves_mz_null(self):
        before = _freeze_bytes()
        walk = orchestrator.walk_schema()
        joined = {row['schema_id']: row for row in walk['joined']}
        self.assertEqual(set(joined), {
            'schema_yes_bid',
            'schema_no_ask',
            'schema_legacy_taker_side',
        })
        self.assertEqual(joined['schema_yes_bid']['taker_band'], 'b04')
        self.assertEqual(joined['schema_yes_bid']['maker_band'], 'b06')
        self.assertEqual(joined['schema_no_ask']['taker_outcome_side'], 'no')
        self.assertEqual(joined['schema_no_ask']['taker_band'], 'b07')
        self.assertEqual(joined['schema_no_ask']['maker_band'], 'b02')
        legacy = joined['schema_legacy_taker_side']
        self.assertEqual(legacy['native_fields'], ['taker_side'])
        self.assertEqual(legacy['taker_band'], 'b01')
        self.assertEqual(legacy['maker_band'], 'b09')
        self.assertEqual(
            legacy['taker_quote']['fee'],
            feebook.order_fee('taker', legacy['contracts'], legacy['taker_price'], round_up=True)['fee'],
        )
        self.assertEqual(legacy['formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertIsNone(legacy['scorecard_label'])
        self.assertIs(legacy['numeric_fee_on_scorecard'], False)
        channel = feebook.examiner_fee_channel(legacy['taker_quote'], legacy['maker_quote'])
        label = feebook.classify_scorecard({
            'kind': 'execution',
            'inventory_flat': True,
            'fee_channel': channel,
        })
        self.assertEqual(label, 'completed_profit')
        self.assertIsNone(legacy['scorecard_label'])
        self.assertIsNone(legacy['MZ'])
        self.assertIsNone(legacy['band_roi'])
        reasons = {row['schema_id']: row['reason'] for row in walk['refusals']}
        self.assertEqual(reasons['schema_missing_taker'], 'TakerFieldRefused')
        self.assertEqual(reasons['schema_taker_fields_disagree'], 'TakerFieldRefused')
        for refusal in walk['refusals']:
            self.assertNotIn('taker_outcome_side', refusal)
            self.assertIsNone(refusal['MZ'])
            self.assertIsNone(refusal['band_roi'])
            self.assertIsNone(refusal['results'])
            self.assertIsNone(refusal['pnl'])
        self.assertIs(walk['admitted_settled_panel'], False)
        self.assertIsNone(walk['MZ'])
        self.assertIsNone(walk['band_roi'])
        self.assertIsNone(walk['results'])
        self.assertIsNone(walk['pnl'])
        self.assertIsNone(walk['post_fee_roi_by_band'])
        self.assertIsNone(walk['maker_vs_taker_roi_delta'])
        quoted = orchestrator.join_schema_row({
            'schema_id': 'schema_quote_ignored',
            'schema_only': True,
            'count_fp': '1',
            'yes_price_dollars': '0.80',
            'no_price_dollars': '0.20',
            'taker_outcome_side': 'no',
            'taker_book_side': 'ask',
            'mid': '0.20',
            'prev_price': '0.10',
        })
        self.assertEqual(quoted['taker_outcome_side'], 'no')
        self.assertEqual(quoted['taker_price'], Decimal('0.20'))
        self.assertEqual(quoted['maker_price'], Decimal('0.80'))
        self.assertEqual(quoted['taker_band'], 'b02')
        self.assertEqual(quoted['maker_band'], 'b08')
        self.assertEqual(quoted['yes_band'], 'b08')
        self.assertEqual(quoted['ignored_quote_fields'], ['mid', 'prev_price'])
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.mincer_zarnowitz([{'price': '0.40', 'outcome': 1}])
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.band_roi([{'band_id': 'b05', 'roi': '0'}])
        with self.assertRaises(orchestrator.AdmitRefused):
            orchestrator.clock_admit()
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)
        empty = json.loads(orchestrator.EMPTY_RESULTS.read_text())
        frozen = json.loads(orchestrator.FROZEN_EXPERIMENT.read_text())
        self.assertIsNone(empty['results'])
        self.assertIsNone(empty['pnl'])
        self.assertIsNone(empty['mz_alpha'])
        self.assertIsNone(empty['post_fee_roi_by_band'])
        self.assertIsNone(frozen['results'])
        self.assertIsNone(frozen['pnl'])

    def test_panel_partitions_keep_the_resting_side_and_a_null_scorecard(self):
        before = _freeze_bytes()
        report = orchestrator.conduct(orchestrator.R3P3A0)
        partitions = {
            (row['taker_outcome_side'], row['taker_book_side']): row
            for row in report['partitions']
        }
        self.assertEqual(partitions[('yes', 'bid')]['maker_outcome_side'], 'no')
        self.assertEqual(partitions[('no', 'ask')]['maker_outcome_side'], 'yes')
        self.assertIsNone(report['MZ'])
        self.assertIsNone(report['band_roi'])
        self.assertIsNone(report['maker_vs_taker_roi_delta'])
        self.assertIsNone(report['post_fee_roi_by_band'])
        for row in report['partitions']:
            self.assertNotIn('taker_fee', row['fee_schema'])
            self.assertNotIn('maker_fee', row['fee_schema'])
            self.assertIsNone(row['fee_schema']['MZ'])
            self.assertIsNone(row['fee_schema']['band_roi'])
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)


if __name__ == '__main__':
    unittest.main()
