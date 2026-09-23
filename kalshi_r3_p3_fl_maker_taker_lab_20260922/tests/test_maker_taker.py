"""Unit pins for the R3-P3 maker/taker scaffold.

Schema rows are not a settled panel. Lee-Ready raises. Freeze results, pnl,
MZ, and band_roi stay null.
"""
import hashlib
import json
import subprocess
import sys
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT.parent
FEEBOOK = PARENT / 'kalshi_feebook_lab_20260922'
sys.path.insert(0, str(ROOT))

import maker_taker
import feebook


def _walk():
    return maker_taker.walk_schema()


def _by_id(walk=None):
    if walk is None:
        walk = _walk()
    return {row['schema_id']: row for row in walk['joined']}


class PinTests(unittest.TestCase):
    def test_binding_cites_packet_collector_and_imported_feebook(self):
        binding = maker_taker.instrument_binding()
        self.assertEqual(binding['packet_id'], 'R3-P3-FL-MAKER-TAKER')
        self.assertEqual(binding['panel_version'], '2026-09-22.r3-p3-fl-maker-taker-v0')
        self.assertEqual(binding['collector'], 'READY')
        self.assertEqual(binding['clock'], 'REFUSED')
        self.assertEqual(binding['settled_n'], 0)
        self.assertEqual(binding['examiner'], 'NOT_NOW')
        self.assertEqual(binding['feebook_commit'], maker_taker.FEEBOOK_COMMIT)
        self.assertEqual(
            binding['feebook_commit'],
            '22371178cb2663250b4762f328069571c48cb551',
        )
        self.assertIs(binding['feebook_imported'], True)
        self.assertIs(binding['feebook_copied'], False)
        self.assertEqual(binding['examiner_formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(
            binding['symbols'],
            ('order_fee', 'examiner_fee_channel', 'TAKER_FILLS_RESTING'),
        )
        self.assertEqual(
            binding['price_bands_registry_id'],
            'astra.r3p3.fl_maker_taker.price_bands_10c.v0',
        )
        self.assertIs(binding['lee_ready'], False)
        self.assertIs(binding['live_orders'], False)
        self.assertIs(binding['q6_000_retune'], False)
        self.assertIs(binding['signal_retune'], False)
        table = feebook.load_series_table()
        self.assertEqual(
            binding['taker_rate'],
            feebook.as_decimal(table['rates']['taker'], 'taker'),
        )
        self.assertEqual(
            binding['maker_rate'],
            feebook.as_decimal(table['rates']['maker'], 'maker'),
        )
        self.assertNotEqual(binding['taker_rate'], binding['maker_rate'])

    def test_feebook_import_is_the_sibling_pin(self):
        self.assertFalse((ROOT / 'feebook.py').exists())
        resolved = Path(maker_taker.feebook.__file__).resolve()
        self.assertEqual(resolved, (FEEBOOK / 'feebook.py').resolve())
        proc = subprocess.run(
            [
                'git', 'diff', '--exit-code', maker_taker.FEEBOOK_COMMIT, '--',
                maker_taker.FEEBOOK_DIRECTORY,
            ],
            cwd=PARENT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        frozen = json.loads((FEEBOOK / 'FROZEN_EXPERIMENT.json').read_text())
        digest = hashlib.sha256((FEEBOOK / 'feebook.py').read_bytes()).hexdigest()
        self.assertEqual(digest, frozen['implementation_sha256']['feebook.py'])
        pins = json.loads((ROOT / 'SOURCE_PINS.json').read_text())
        self.assertEqual(digest, pins['feebook_dependency']['feebook_py_sha256'])
        self.assertIs(pins['feebook_dependency']['imported'], True)
        self.assertIs(pins['feebook_dependency']['copied'], False)

    def test_naked_fee_literals_and_paper_returns_are_absent_from_source(self):
        source = (ROOT / 'maker_taker.py').read_text()
        for banned in (
            '0.0175',
            '0.07',
            '.0175',
            '2.6',
            '0.026',
            '-9.64',
            '-31.46',
            'maker_coefficient',
            'taker_coefficient',
            'common_config',
            'factorial_policy',
            'paircheck_policy',
            'replay_v2',
            'class KalshiExecutionAdapter',
            'portfolio',
            'urllib',
            'requests',
            'socket',
            'api.kalshi',
            'ROUND_CEILING',
            'classify_scorecard',
            'q3300',
            'nfl_factorial_lab',
            'nfl_paircheck_lab',
        ):
            self.assertNotIn(banned, source)
        self.assertIn('feebook.order_fee', source)
        self.assertIn('feebook.examiner_fee_channel', source)
        self.assertIn('feebook.TAKER_FILLS_RESTING', source)
        self.assertFalse(hasattr(maker_taker, 'KalshiExecutionAdapter'))
        self.assertIs(maker_taker.LEE_READY, False)
        self.assertIs(maker_taker.LIVE_ORDERS, False)
        self.assertIs(maker_taker.Q6_000_RETUNE, False)

    def test_freeze_and_empty_results_stay_null(self):
        frozen = json.loads(maker_taker.FROZEN_EXPERIMENT.read_text())
        empty = json.loads(maker_taker.EMPTY_RESULTS.read_text())
        for key in maker_taker.OUTPUT_KEYS:
            self.assertIsNone(frozen[key])
            self.assertIsNone(empty[key])
            self.assertIsNone(maker_taker.frozen_output_snapshot()[key])
            self.assertIsNone(maker_taker.empty_outputs()[key])
        self.assertEqual(empty['status'], 'EMPTY')
        self.assertEqual(empty['clock'], 'REFUSED')
        self.assertEqual(empty['collector'], 'READY')
        self.assertEqual(empty['settled_n'], 0)
        self.assertEqual(empty['panel_version'], maker_taker.PANEL_VERSION)
        self.assertEqual(frozen['packet_id'], maker_taker.PACKET_ID)
        self.assertEqual(frozen['clock'], 'REFUSED')
        self.assertEqual(frozen['collector'], 'READY')
        self.assertEqual(frozen['settled_n'], 0)
        self.assertEqual(frozen['examiner'], 'NOT_NOW')
        self.assertIs(frozen['lee_ready'], False)
        self.assertIs(frozen['lee_ready_successful_path'], False)
        self.assertIs(frozen['q6_000_retune'], False)
        self.assertIs(frozen['signal_retune'], False)
        self.assertIs(frozen['live_orders'], False)
        self.assertIs(frozen['forbid_invented_pnl'], True)
        self.assertIs(frozen['forbid_naked_q6_q7_fee_literals'], True)
        self.assertIs(frozen['forbid_paper_return_as_evidence'], True)
        self.assertIs(frozen['rebinned_after_outcomes'], False)
        self.assertIs(frozen['not_a_strategy'], True)
        for name, digest in frozen['specification_sha256'].items():
            self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), digest)
        self.assertIsInstance(frozen['implementation_sha256'], dict)
        for name, digest in frozen['implementation_sha256'].items():
            self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), digest)
        bands_digest = hashlib.sha256((ROOT / 'price_bands_10c.v0.json').read_bytes()).hexdigest()
        pins = json.loads((ROOT / 'SOURCE_PINS.json').read_text())
        self.assertEqual(bands_digest, pins['price_bands']['sha256'])
        self.assertIsNone(pins['results'])
        self.assertIsNone(pins['pnl'])
        self.assertIsNone(pins['MZ'])
        self.assertIsNone(pins['band_roi'])


class BandTests(unittest.TestCase):
    def test_registry_is_ten_contiguous_absolute_bands(self):
        table = maker_taker.load_bands()
        self.assertEqual(table['registry_id'], maker_taker.BANDS_REGISTRY_ID)
        self.assertIs(table['rebinned_after_outcomes'], False)
        self.assertEqual(len(table['bands']), 10)
        self.assertEqual(
            [band['id'] for band in table['bands']],
            ['b%02d' % index for index in range(10)],
        )
        self.assertEqual(table['bands'][0]['lo'], 0)
        self.assertEqual(table['bands'][-1]['hi'], feebook.ONE)
        previous = None
        for band in table['bands']:
            self.assertEqual(band['hi'] - band['lo'], table['width_dollars'])
            if previous is not None:
                self.assertEqual(band['lo'], previous)
            previous = band['hi']
        self.assertNotIn('0.10', (ROOT / 'maker_taker.py').read_text())

    def test_edges_follow_the_pin_file(self):
        table = maker_taker.load_bands()
        ids = [band['id'] for band in table['bands']]
        for index, band in enumerate(table['bands']):
            self.assertEqual(maker_taker.assign_band(band['lo'])['band_id'], band['id'])
            if band['id'] != 'b09':
                self.assertEqual(
                    maker_taker.assign_band(band['hi'])['band_id'],
                    ids[index + 1],
                )
        self.assertEqual(maker_taker.assign_band('1')['band_id'], 'b09')
        self.assertEqual(maker_taker.assign_band('1.00')['band_id'], 'b09')
        self.assertEqual(maker_taker.assign_band('0')['band_id'], 'b00')
        assigned = maker_taker.assign_band(table['bands'][5]['lo'])
        self.assertEqual(assigned['band_id'], 'b05')
        self.assertEqual(assigned['registry_id'], maker_taker.BANDS_REGISTRY_ID)

    def test_prices_outside_the_unit_interval_and_floats_are_rejected(self):
        with self.assertRaises(ValueError):
            maker_taker.assign_band('-0.01')
        with self.assertRaises(ValueError):
            maker_taker.assign_band('1.01')
        with self.assertRaises(TypeError):
            maker_taker.assign_band(0.4)
        with self.assertRaises(TypeError):
            maker_taker.assign_band(True)

    def test_outcomes_do_not_rebin(self):
        with self.assertRaises(maker_taker.RebinRefused):
            maker_taker.assign_band('0.40', outcome='yes')
        with self.assertRaises(maker_taker.RebinRefused):
            maker_taker.assign_band('0.40', outcome=None)
        with self.assertRaises(maker_taker.RebinRefused):
            maker_taker.rebin_after_outcomes([{'price': '0.40', 'outcome': 1}])
        table = maker_taker.load_bands()
        table['rebinned_after_outcomes'] = True
        with self.assertRaises(maker_taker.RebinRefused):
            maker_taker.assign_band('0.40', bands=table)
        fresh = maker_taker.load_bands()
        fresh['registry_id'] = 'astra.other'
        with self.assertRaises(ValueError):
            maker_taker.assign_band('0.40', bands=fresh)


class TakerTests(unittest.TestCase):
    def test_native_fields_agree_and_set_the_maker_side(self):
        classified = maker_taker.classify_taker({
            'taker_outcome_side': 'yes',
            'taker_book_side': 'bid',
            'taker_side': 'yes',
        })
        self.assertEqual(classified['taker_outcome_side'], 'yes')
        self.assertEqual(classified['taker_book_side'], 'bid')
        self.assertEqual(classified['maker_outcome_side'], 'no')
        self.assertEqual(
            classified['maker_outcome_side'],
            feebook.TAKER_FILLS_RESTING[classified['taker_outcome_side']],
        )
        self.assertEqual(
            classified['native_fields'],
            ['taker_outcome_side', 'taker_book_side', 'taker_side'],
        )
        self.assertEqual(classified['classification'], 'native_public_taker')
        self.assertIsNone(classified['lee_ready'])

    def test_book_side_alone_is_the_public_bit(self):
        classified = maker_taker.classify_taker({'taker_book_side': 'ask'})
        self.assertEqual(classified['taker_outcome_side'], 'no')
        self.assertEqual(classified['maker_outcome_side'], 'yes')
        self.assertEqual(classified['native_fields'], ['taker_book_side'])

    def test_missing_private_and_unknown_fields_do_not_classify(self):
        with self.assertRaises(maker_taker.TakerFieldRefused):
            maker_taker.classify_taker({'is_taker': True, 'side': 'yes', 'action': 'buy'})
        with self.assertRaises(maker_taker.TakerFieldRefused):
            maker_taker.classify_taker({
                'taker_outcome_side': 'yes',
                'taker_fees_dollars': '1',
            })
        with self.assertRaises(maker_taker.TakerFieldRefused):
            maker_taker.classify_taker({
                'taker_outcome_side': 'yes',
                'taker_side': 'no',
            })
        with self.assertRaises(maker_taker.TakerFieldRefused):
            maker_taker.classify_taker({
                'yes_price_dollars': '0.80',
                'no_price_dollars': '0.20',
                'mid': '0.40',
                'prev_price': '0.30',
            })

    def test_lee_ready_has_no_successful_path(self):
        samples = [
            {'price': '0.80', 'mid': '0.50'},
            {'price': '0.20', 'mid': '0.50'},
            {'price': '0.50', 'mid': '0.50', 'prev_price': '0.49'},
            {'price': '0.50', 'mid': '0.50', 'prev_price': '0.51'},
            {'taker_outcome_side': 'yes', 'yes_price_dollars': '0.40', 'no_price_dollars': '0.60'},
        ]
        for sample in samples:
            with self.assertRaises(maker_taker.LeeReadyRefused):
                maker_taker.lee_ready(sample)
        with self.assertRaises(maker_taker.LeeReadyRefused):
            maker_taker.classify_taker({
                'taker_outcome_side': 'yes',
                'taker_book_side': 'bid',
                'lee_ready': True,
            })
        with self.assertRaises(maker_taker.LeeReadyRefused):
            maker_taker.classify_taker({
                'yes_price_dollars': '0.80',
                'classifier': 'Lee-Ready',
            })
        import inspect
        source = inspect.getsource(maker_taker.lee_ready)
        self.assertNotIn('return', source)
        self.assertNotIn('mid', source)
        self.assertIn('LeeReadyRefused', source)


class FeeJoinTests(unittest.TestCase):
    def _row(self, **extra):
        row = {
            'schema_id': 'unit-schema',
            'schema_only': True,
            'count_fp': '2',
            'yes_price_dollars': '0.40',
            'no_price_dollars': '0.60',
            'taker_outcome_side': 'yes',
            'taker_book_side': 'bid',
        }
        row.update(extra)
        return row

    def test_quotes_match_the_imported_order_fee(self):
        joined = maker_taker.join_fees(self._row())
        taker = feebook.order_fee('taker', joined['contracts'], joined['taker_price'], round_up=True)
        maker = feebook.order_fee('maker', joined['contracts'], joined['maker_price'], round_up=True)
        self.assertEqual(joined['taker_quote']['fee'], taker['fee'])
        self.assertEqual(joined['maker_quote']['fee'], maker['fee'])
        self.assertEqual(joined['taker_quote']['formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(joined['maker_quote']['formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertIs(joined['taker_quote']['rounded_up'], True)
        self.assertIs(joined['maker_quote']['rounded_up'], True)
        self.assertEqual(joined['formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(joined['fee_channel']['formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(joined['taker_band'], 'b04')
        self.assertEqual(joined['maker_band'], 'b06')
        self.assertEqual(joined['maker_outcome_side'], 'no')
        self.assertIsNone(joined['scorecard_label'])
        for key in maker_taker.OUTPUT_KEYS:
            self.assertIsNone(joined[key])
        channel = feebook.examiner_fee_channel(taker, maker)
        label = feebook.classify_scorecard({
            'kind': 'execution',
            'inventory_flat': True,
            'fee_channel': channel,
        })
        self.assertEqual(label, 'completed_profit')
        self.assertIsNone(joined['scorecard_label'])
        with self.assertRaises(maker_taker.ScorecardRefused):
            maker_taker.scorecard_refuse(label)

    def test_quote_fields_do_not_override_a_native_taker_side(self):
        joined = maker_taker.join_fees(self._row(
            taker_outcome_side='no',
            taker_book_side='ask',
            yes_price_dollars='0.80',
            no_price_dollars='0.20',
            mid='0.20',
            prev_price='0.10',
        ))
        self.assertEqual(joined['taker_outcome_side'], 'no')
        self.assertEqual(joined['taker_price'], Decimal('0.20'))
        self.assertEqual(joined['maker_price'], Decimal('0.80'))
        self.assertEqual(joined['taker_band'], 'b02')
        self.assertEqual(joined['maker_band'], 'b08')
        self.assertEqual(joined['ignored_quote_fields'], ['mid', 'prev_price'])
        self.assertIsNone(joined['lee_ready'])

    def test_a_missing_price_is_not_invented(self):
        with self.assertRaises(ValueError):
            maker_taker.join_fees(self._row(no_price_dollars=None))
        with self.assertRaises(ValueError):
            maker_taker.join_fees(self._row(no_price_dollars='0.50'))
        with self.assertRaises(TypeError):
            maker_taker.join_fees(self._row(yes_price_dollars=0.4))
        with self.assertRaises(ValueError):
            maker_taker.join_fees(self._row(count='3'))
        with self.assertRaises(TypeError):
            maker_taker.join_fees(self._row(is_block_trade='yes'))

    def test_settled_fields_are_refused_before_a_scorecard_fill(self):
        with self.assertRaises(maker_taker.ScorecardRefused):
            maker_taker.join_fees(self._row(resolution='yes'))
        with self.assertRaises(maker_taker.ScorecardRefused):
            maker_taker.join_fees(self._row(outcome=1, pnl='1'))
        with self.assertRaises(maker_taker.ScorecardRefused):
            maker_taker.join_fees(self._row(band_roi='0'))
        bare = maker_taker.join_fees(self._row(series='SCHEMA'))
        plain = maker_taker.join_fees(self._row())
        self.assertEqual(bare['taker_quote']['fee'], plain['taker_quote']['fee'])
        self.assertEqual(bare['series'], 'SCHEMA')
        self.assertIsNone(plain['series'])

    def test_live_orders_are_refused(self):
        with self.assertRaises(maker_taker.LiveOrdersForbidden):
            maker_taker.execution_adapter()


class ScorecardTests(unittest.TestCase):
    def test_mz_and_band_roi_have_no_successful_path(self):
        with self.assertRaises(maker_taker.ScorecardRefused):
            maker_taker.mincer_zarnowitz([
                {'price': '0.40', 'outcome': 1},
                {'price': '0.60', 'outcome': 0},
            ])
        with self.assertRaises(maker_taker.ScorecardRefused):
            maker_taker.band_roi([{'band_id': 'b05', 'roi': '0'}])
        with self.assertRaises(maker_taker.ScorecardRefused):
            maker_taker.scorecard_refuse({'results': '1', 'pnl': '1', 'MZ': '1', 'band_roi': '1'})
        stub = maker_taker.collector_stub()
        self.assertEqual(stub['status'], 'READY')
        self.assertEqual(stub['panel_version'], maker_taker.PANEL_VERSION)
        self.assertIs(stub['admitted'], False)
        self.assertIs(stub['admitted_settled_panel'], False)
        self.assertEqual(stub['clock'], 'REFUSED')
        self.assertEqual(stub['settled_n'], 0)
        for key in maker_taker.OUTPUT_KEYS:
            self.assertIsNone(stub[key])
        with self.assertRaises(maker_taker.AdmitRefused):
            maker_taker.clock_admit(stub)


class SchemaWalkTests(unittest.TestCase):
    def test_fixture_is_schema_only_and_has_no_resolution_keys(self):
        payload = maker_taker.load_schema_fixture()
        self.assertEqual(payload['label'], 'SCHEMA_ONLY')
        self.assertIs(payload['admitted_settled_panel'], False)
        self.assertEqual(payload['collector'], 'READY')
        self.assertEqual(payload['clock'], 'REFUSED')
        self.assertEqual(payload['settled_n'], 0)
        self.assertEqual(payload['panel_version'], maker_taker.PANEL_VERSION)
        forbidden = ('resolution', 'result', 'outcome', 'pnl', 'roi', 'MZ', 'band_roi', 'settled')
        for row in payload['rows']:
            self.assertIs(row['schema_only'], True)
            self.assertEqual(row['ticker'], 'SCHEMA-ONLY')
            for key in forbidden:
                self.assertNotIn(key, row)

    def test_walk_joins_three_rows_and_refuses_two_without_a_side(self):
        walk = _walk()
        joined = _by_id(walk)
        self.assertEqual(set(joined), {
            'schema_yes_bid',
            'schema_no_ask',
            'schema_legacy_taker_side',
        })
        self.assertEqual(joined['schema_yes_bid']['taker_outcome_side'], 'yes')
        self.assertEqual(joined['schema_yes_bid']['taker_band'], 'b04')
        self.assertEqual(joined['schema_yes_bid']['maker_band'], 'b06')
        self.assertEqual(joined['schema_no_ask']['taker_outcome_side'], 'no')
        self.assertEqual(joined['schema_no_ask']['taker_band'], 'b07')
        self.assertEqual(joined['schema_no_ask']['maker_band'], 'b02')
        legacy = joined['schema_legacy_taker_side']
        self.assertEqual(legacy['native_fields'], ['taker_side'])
        self.assertEqual(legacy['taker_outcome_side'], 'yes')
        self.assertEqual(legacy['taker_band'], 'b01')
        self.assertEqual(legacy['maker_band'], 'b09')
        self.assertEqual(
            legacy['taker_quote']['fee'],
            feebook.order_fee('taker', legacy['contracts'], legacy['taker_price'], round_up=True)['fee'],
        )
        self.assertEqual(len(walk['refusals']), 2)
        reasons = {row['schema_id']: row['reason'] for row in walk['refusals']}
        self.assertEqual(reasons['schema_missing_taker'], 'TakerFieldRefused')
        self.assertEqual(reasons['schema_taker_fields_disagree'], 'TakerFieldRefused')
        for refusal in walk['refusals']:
            self.assertNotIn('taker_outcome_side', refusal)
            self.assertIsNone(refusal['lee_ready'])
            for key in maker_taker.OUTPUT_KEYS:
                self.assertIsNone(refusal[key])
        self.assertEqual(walk['status'], 'SCHEMA_ONLY')
        self.assertIs(walk['admitted_settled_panel'], False)
        self.assertEqual(walk['settled_n'], 0)
        self.assertIsNone(walk['lee_ready'])
        for key in maker_taker.OUTPUT_KEYS:
            self.assertIsNone(walk[key])

    def test_walking_the_schema_does_not_fill_the_freeze(self):
        empty_path = maker_taker.EMPTY_RESULTS
        freeze_path = maker_taker.FROZEN_EXPERIMENT
        before_empty = empty_path.read_bytes()
        before_freeze = freeze_path.read_bytes()
        maker_taker.walk_schema()
        maker_taker.collector_stub()
        self.assertEqual(empty_path.read_bytes(), before_empty)
        self.assertEqual(freeze_path.read_bytes(), before_freeze)
        stored = json.loads(before_empty)
        frozen = json.loads(before_freeze)
        for key in maker_taker.OUTPUT_KEYS:
            self.assertIsNone(stored[key])
            self.assertIsNone(frozen[key])
        self.assertEqual(stored['status'], 'EMPTY')
        self.assertEqual(maker_taker.empty_outputs()['status'], 'EMPTY')
