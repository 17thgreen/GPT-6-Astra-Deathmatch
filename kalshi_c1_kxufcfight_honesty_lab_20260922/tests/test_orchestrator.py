"""Unit pins for the C1 KXUFCFIGHT fee and queue honesty harness.

In-memory labels are not a walk and they are not profit. Freeze outputs stay
null. The subject is the admitted panel, not the pre-admit stub.
"""
import json
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(PARENT / 'kalshi_feebook_lab_20260922'))
sys.path.insert(0, str(PARENT / 'kalshi_rails_lab_20260922'))
sys.path.insert(0, str(PARENT / 'kalshi_r2p1_hygiene_000_lab_20260922'))

import feebook
import hygiene
import orchestrator
import rails

BASE = 'd8957a0061ba601a11b3b03145b1516937239988'


def schema_panel():
    """Panel object for in-memory labels.

    The canonical path is ``panel_admitted.json``. When those bytes are in the
    checkout, this returns them. A stamped copy of the pre-admit stub is only
    a schema stand-in for label algebra and is not the sha pin.
    """
    if orchestrator.PANEL_ADMITTED.is_file():
        return orchestrator.load_panel()
    payload = json.loads(orchestrator.PANEL_STUB.read_text())

    def stamp(obj):
        if isinstance(obj, dict):
            if 'admitted_at' in obj:
                obj['admitted_at'] = orchestrator.ADMITTED_AT
            for value in obj.values():
                stamp(value)
        elif isinstance(obj, list):
            for item in obj:
                stamp(item)

    stamp(payload)
    return payload


class PinTests(unittest.TestCase):
    def test_binding_pins_the_admitted_panel_and_the_instruments(self):
        self.assertTrue(
            orchestrator.PANEL_ADMITTED.is_file(),
            'panel_admitted.json is not in the checkout',
        )
        binding = orchestrator.instrument_binding()
        panel = orchestrator.load_panel()
        self.assertEqual(binding['experiment_id'], 'c1_kxufcfight_honesty_20260922')
        self.assertEqual(binding['panel_version'], '2026-09-22.c1-kxufcfight-v0')
        self.assertEqual(panel['panel_version'], '2026-09-22.c1-kxufcfight-v0')
        self.assertEqual(panel['admitted_at'], '2026-09-23T00:49:43Z')
        self.assertEqual(binding['admitted_at'], '2026-09-23T00:49:43Z')
        self.assertEqual(binding['feebook_commit'], '22371178cb2663250b4762f328069571c48cb551')
        self.assertEqual(binding['rails_commit'], '6a28e0d6254327ea4e6451c781bec56215ac6cac')
        self.assertEqual(binding['examiner_formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(binding['fee_credit_rule_id'], rails.FEE_CREDIT_RULE_ID)
        self.assertEqual(binding['series_resolution'], 'default_unknown_series')
        self.assertEqual(binding['multiplier'], Decimal('1'))
        self.assertIsNone(binding['strategy_pointer'])
        self.assertIs(binding['strategy_claim'], False)
        self.assertIs(binding['q6_000_retune'], False)
        self.assertIs(binding['allocator_ported'], False)
        self.assertIs(binding['live_orders'], False)
        self.assertIs(binding['forbid_capital_A2_A3'], True)
        self.assertEqual(binding['capital']['bakeoff_capital_usd_label'], Decimal('5000'))
        self.assertIs(binding['capital']['bakeoff_capital_is_strategy_claim'], False)
        self.assertIsNone(binding['capital']['capital_structure_arm'])
        self.assertEqual(binding['instrument_contrast'], 'Q6-000-instruments')
        self.assertTrue(binding['panel_admitted_sha256'].startswith('24426d80'))
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.PANEL_ADMITTED),
            binding['panel_admitted_sha256'],
        )
        self.assertEqual(binding['panel_stub_sha256'], orchestrator.PANEL_STUB_SHA256)
        self.assertEqual(binding['kernel_sha256'], orchestrator.KERNEL_SHA256)
        self.assertEqual(
            sorted(path.name for path in PARENT.glob('kalshi_c1_kxufcfight_honesty_lab_*')),
            ['kalshi_c1_kxufcfight_honesty_lab_20260922'],
        )

    def test_admitted_panel_is_the_subject_and_the_stub_is_refused(self):
        self.assertTrue(orchestrator.PANEL_ADMITTED.is_file())
        digest = orchestrator.sha256_file(orchestrator.PANEL_ADMITTED)
        self.assertTrue(digest.startswith(orchestrator.PANEL_SHA256_PREFIX))
        frozen = json.loads(orchestrator.FROZEN_EXPERIMENT.read_text())
        self.assertEqual(frozen['panel_version'], '2026-09-22.c1-kxufcfight-v0')
        self.assertEqual(frozen['admitted_at'], '2026-09-23T00:49:43Z')
        self.assertEqual(frozen['panel_admitted_sha256'], digest)
        self.assertEqual(frozen['panel_stub_sha256'], orchestrator.PANEL_STUB_SHA256)
        self.assertEqual(
            orchestrator.sha256_file(orchestrator.PANEL_STUB),
            orchestrator.PANEL_STUB_SHA256,
        )
        with self.assertRaises(orchestrator.OrchestratorError) as refused:
            orchestrator.load_panel(orchestrator.PANEL_STUB)
        self.assertEqual(str(refused.exception), 'stub is not the admitted panel')
        payload = json.loads(orchestrator.PANEL_ADMITTED.read_text())
        payload['panel_version'] = '2026-09-22.c1-kxufcfight-v1'
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'panel_admitted.json'
            path.write_text(json.dumps(payload))
            with self.assertRaises(orchestrator.PanelVersionRefused):
                orchestrator.load_panel(path)
        self.assertIsNone(payload.get('results'))
        panel = orchestrator.load_panel()
        self.assertIsNone(panel['results'])
        self.assertIsNone(panel['pnl'])
        self.assertIsNone(panel['volume'])
        for market in panel['markets']:
            self.assertIsNone(market['volume_fp'])
            self.assertIsNone(market['volume_24h_fp'])
            self.assertIsNone(market['open_interest_fp'])
            self.assertEqual(market['panel_version'], orchestrator.PANEL_VERSION)
        self.assertEqual(panel['cohort_counts']['markets_n'], 4)
        self.assertIn('KXUFCFIGHT-26SEP22ORTDAS-ORT', panel['dropped_from_seed'])

    def test_pinned_cores_are_unmodified(self):
        for commit, path in (
            (orchestrator.FEEBOOK_COMMIT, 'kalshi_feebook_lab_20260922'),
            (orchestrator.RAILS_COMMIT, 'kalshi_rails_lab_20260922'),
        ):
            proc = subprocess.run(
                ['git', 'diff', '--exit-code', commit, '--', path],
                cwd=PARENT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        frozen = json.loads(orchestrator.FROZEN_EXPERIMENT.read_text())
        for path in frozen['does_not_modify']:
            proc = subprocess.run(
                ['git', 'diff', '--exit-code', BASE, '--', path],
                cwd=PARENT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, path + proc.stdout + proc.stderr)

    def test_freeze_outputs_stay_null(self):
        frozen = json.loads(orchestrator.FROZEN_EXPERIMENT.read_text())
        empty = json.loads(orchestrator.EMPTY_RESULTS.read_text())
        scout_results = json.loads(orchestrator.SCOUT_RESULTS.read_text())
        scout_empty = json.loads(orchestrator.SCOUT_EMPTY.read_text())
        scout = json.loads(orchestrator.SCOUT_FROZEN.read_text())
        for payload in (frozen, empty, scout_results, scout_empty):
            for key in orchestrator.OUTPUT_KEYS:
                self.assertIsNone(payload[key])
        self.assertIsNone(scout['results'])
        self.assertIsNone(scout['pnl'])
        self.assertEqual(empty['status'], 'NOT_RUN')
        self.assertEqual(scout_results['status'], 'NOT_RUN')
        self.assertEqual(frozen['status'], 'FROZEN_NOT_RUN')
        self.assertIs(frozen['live_orders'], False)
        self.assertIs(frozen['no_000_retune'], True)
        self.assertIs(frozen['forbid_capital_A2_A3'], True)
        self.assertIs(frozen['strategy_claim'], False)
        snapshot = orchestrator.frozen_output_snapshot()
        for key in orchestrator.OUTPUT_KEYS:
            self.assertIsNone(snapshot['frozen.%s' % key])
            self.assertIsNone(snapshot['empty.%s' % key])

    def test_reciprocal_book_on_the_extreme_favorite(self):
        report = orchestrator.conduct(schema_panel())
        by_ticker = {row['market_ticker']: row for row in report['labels']}
        favorite = by_ticker['KXUFCFIGHT-26SEP22DEGMOR-DEG']
        book = favorite['reciprocal_book']
        self.assertEqual(book['bid_yes'], Decimal('0.98'))
        self.assertEqual(book['bid_no'], Decimal('0.01'))
        self.assertEqual(book['ask_yes'], Decimal('0.99'))
        self.assertEqual(book['ask_no'], Decimal('0.02'))
        self.assertEqual(book['spread_yes'], Decimal('0.01'))
        self.assertGreater(book['bid_yes'], Decimal('0.95'))
        underdog = by_ticker['KXUFCFIGHT-26SEP22DEGMOR-MOR']['reciprocal_book']
        self.assertEqual(underdog['ask_yes'], feebook.ONE - underdog['bid_no'])
        mid = by_ticker['KXUFCFIGHT-26SEP22CONGUA-CON']['reciprocal_book']
        self.assertEqual(mid['bid_yes'], Decimal('0.40'))
        self.assertEqual(mid['bid_no'], Decimal('0.45'))
        self.assertEqual(mid['ask_yes'], Decimal('0.55'))
        self.assertEqual(mid['spread_yes'], Decimal('0.15'))
        incomplete = by_ticker['KXUFCFIGHT-26SEP22CONGUA-GUA']
        self.assertIs(incomplete['incomplete_book'], True)
        self.assertIsNone(incomplete['reciprocal_book']['ask_yes'])
        self.assertIsNone(incomplete['reciprocal_book']['spread_yes'])
        self.assertIsNone(incomplete['fee_channel'])
        panel = schema_panel()
        stub_price = next(
            row['last_price_dollars_raw_get']
            for row in panel['markets']
            if row['market_ticker'] == 'KXUFCFIGHT-26SEP22DEGMOR-DEG'
        )
        self.assertNotEqual(Decimal(stub_price), book['bid_yes'])

    def test_order_fee_binds_the_examiner_formula(self):
        report = orchestrator.conduct(schema_panel())
        favorite = next(
            row for row in report['labels']
            if row['market_ticker'] == 'KXUFCFIGHT-26SEP22DEGMOR-DEG'
        )
        direct = feebook.order_fee(
            'taker',
            '10',
            favorite['reciprocal_book']['ask_yes'],
            round_up=True,
            series='KXUFCFIGHT',
        )
        self.assertEqual(favorite['taker_fee'], direct)
        self.assertEqual(direct['formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertIs(direct['rounded_up'], True)
        self.assertEqual(direct['series_resolution'], 'default_unknown_series')
        self.assertEqual(favorite['fee_channel']['formula_id'], feebook.EXAMINER_FORMULA_ID)
        with self.assertRaises(TypeError):
            orchestrator.bind_order_fee('taker', '1', 0.50, panel=schema_panel())

    def test_rails_labels_match_the_000_instrument(self):
        self.assertEqual(
            orchestrator.queue_attribution_bin(rails.QUEUE_AHEAD_DEFAULT),
            hygiene.queue_attribution_bin(rails.QUEUE_AHEAD_DEFAULT),
        )
        self.assertEqual(orchestrator.queue_attribution_bin(rails.QUEUE_AHEAD_DEFAULT), 'q3300')
        self.assertEqual(
            orchestrator.queue_attribution_bin(rails.STRESS_QUEUE_AHEAD),
            'q10000',
        )
        outside = rails.QUEUE_AHEAD_DEFAULT + 1
        self.assertEqual(orchestrator.queue_attribution_bin(outside), orchestrator.OUTSIDE_BIN)
        self.assertEqual(
            orchestrator.queue_attribution_bin(outside),
            hygiene.queue_attribution_bin(outside),
        )
        for price, contracts in (('0.01', '1'), ('0.50', '1')):
            ours = orchestrator.maker_credit_floor_zero_refuse(price, contracts)
            theirs = hygiene.maker_credit_floor_zero_refuse(Decimal(price), Decimal(contracts))
            self.assertEqual(ours['maker_credit_floor_zero_refuse'], theirs['maker_credit_floor_zero_refuse'])
            self.assertEqual(ours['credit'], theirs['credit'])
            self.assertEqual(ours['formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertIs(
            orchestrator.maker_credit_floor_zero_refuse('0.01', '1')['maker_credit_floor_zero_refuse'],
            True,
        )
        self.assertIs(
            orchestrator.maker_credit_floor_zero_refuse('0.50', '1')['maker_credit_floor_zero_refuse'],
            False,
        )
        content = rails.canonical_book_content({'yes_dollars': [['0.50', '1']], 'no_dollars': [['0.50', '1']]})
        book = rails.BookObservation(content, 't1')
        first = orchestrator.content_fresh_flag(None, book)
        ping = orchestrator.content_fresh_flag(book, book, keepalive=True)
        same = orchestrator.content_fresh_flag(book, book, keepalive=False)
        self.assertIs(first['content_fresh_flag'], True)
        self.assertEqual(first['reason'], 'initial')
        self.assertIs(ping['content_fresh_flag'], False)
        self.assertEqual(ping['reason'], 'keepalive_ignored')
        self.assertIs(same['content_fresh_flag'], False)
        self.assertEqual(
            ping['content_fresh_flag'],
            hygiene.content_fresh_flag(book, book, keepalive=True)['content_fresh_flag'],
        )
        report = orchestrator.conduct(schema_panel())
        by_ticker = {row['market_ticker']: row for row in report['labels']}
        self.assertEqual(by_ticker['KXUFCFIGHT-26SEP22DEGMOR-DEG']['queue_attribution_bin'], 'q3300')
        self.assertEqual(by_ticker['KXUFCFIGHT-26SEP22DEGMOR-MOR']['queue_attribution_bin'], 'q10000')
        self.assertEqual(
            by_ticker['KXUFCFIGHT-26SEP22CONGUA-CON']['queue_attribution_bin'],
            orchestrator.OUTSIDE_BIN,
        )
        self.assertIs(by_ticker['KXUFCFIGHT-26SEP22DEGMOR-MOR']['maker_credit_floor_zero_refuse'], True)
        self.assertIs(by_ticker['KXUFCFIGHT-26SEP22DEGMOR-DEG']['maker_credit_floor_zero_refuse'], False)
        self.assertIs(by_ticker['KXUFCFIGHT-26SEP22DEGMOR-DEG']['content_fresh_flag'], True)
        self.assertEqual(
            by_ticker['KXUFCFIGHT-26SEP22DEGMOR-DEG']['timing_minutes'],
            Decimal('40'),
        )
        self.assertIsNone(report['timing_shape'])
        self.assertIsNone(report['published']['content_fresh_flag'])
        self.assertIsNone(report['published']['maker_credit_floor_zero_refuse'])
        self.assertIsNone(report['published']['queue_attribution_bin'])

    def test_completed_profit_without_feebook_is_refused(self):
        with self.assertRaises(feebook.CompletedProfitRefused):
            orchestrator.classify_completed_profit({'inventory_flat': True})
        grok = feebook.grok_unrounded_maker_per_unit('0.50')
        with self.assertRaises(feebook.CompletedProfitRefused):
            orchestrator.classify_completed_profit({
                'inventory_flat': True,
                'fee_channel': {
                    'formula_id': grok['formula_id'],
                    'taker_fee': '0.01',
                    'maker_fee': '0.01',
                },
            })
        panel = schema_panel()
        taker = orchestrator.bind_order_fee('taker', '1', '0.50', panel=panel)
        maker = orchestrator.bind_order_fee('maker', '1', '0.50', panel=panel)
        channel = feebook.examiner_fee_channel(taker, maker)
        kind = orchestrator.classify_completed_profit({
            'inventory_flat': True,
            'fee_channel': channel,
        })
        self.assertEqual(kind, 'completed_profit')
        filled = dict(orchestrator.published_scorecard())
        filled['completed_profit'] = kind
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard(filled)
        with self.assertRaises(feebook.CompletedProfitRefused):
            orchestrator.classify_completed_profit({
                'inventory_flat': False,
                'fee_channel': channel,
            })

    def test_shadow_fee_literals_are_refused(self):
        source = (ROOT / 'orchestrator.py').read_text()
        for banned in (
            'maker_coefficient',
            'taker_coefficient',
            'common_config',
            '0.0175',
            '0.07',
            'factorial_policy',
            'paircheck_policy',
            'replay_v2',
            'class KalshiExecutionAdapter',
            'import hygiene',
            'import queue_fragility',
            'fixture_join',
            'q3300_d0.25_000',
            'urlopen',
        ):
            self.assertNotIn(banned, source)
        grok = feebook.grok_unrounded_maker_per_unit('0.50')
        with self.assertRaises(orchestrator.ShadowFeeLiteralRefused):
            orchestrator.assert_examiner_quote(grok)
        inherited = {
            'formula_id': 'q6.order_fees.fixed_point_balance.v1',
            'fee': '1',
            'role': 'maker',
        }
        with self.assertRaises(orchestrator.ShadowFeeLiteralRefused):
            orchestrator.assert_examiner_quote(inherited)

    def test_no_invented_open_interest_and_scorecard_stays_unwritten(self):
        before = {
            path: path.read_bytes()
            for path in (
                orchestrator.FROZEN_EXPERIMENT,
                orchestrator.EMPTY_RESULTS,
                orchestrator.SCOUT_FROZEN,
                orchestrator.SCOUT_RESULTS,
                orchestrator.SCOUT_EMPTY,
                orchestrator.KERNEL,
            )
        }
        status = orchestrator.production_orderbook_status()
        report = orchestrator.conduct(schema_panel())
        self.assertEqual(report['source'], 'synthetic_schema_standin')
        self.assertEqual(
            report['production_orderbooks_present'],
            status['status'] == 'PINNED',
        )
        self.assertEqual(report['production_orderbook_status'], status['status'])
        self.assertEqual(report['score_status'], 'NOT_SCORED')
        self.assertIs(report['examiner_ready'], False)
        self.assertEqual(report['production_capture_path'], 'lab/astra-capture/c1-kxufcfight/')
        self.assertFalse(report['promoted'])
        self.assertIsNone(report['strategy_pointer'])
        self.assertEqual(report['row_count'], 4)
        for row in report['labels']:
            self.assertIsNone(row['volume_fp'])
            self.assertIsNone(row['open_interest_fp'])
            self.assertIsNone(row['pnl'])
            self.assertIsNone(row['results'])
            self.assertIsNone(row['strategy_ev'])
            self.assertIsNone(row['completed_profit'])
        orchestrator.assert_null_scorecard(report)
        orchestrator.assert_null_scorecard(report['published'])
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard(report['published'])
        for key in orchestrator.OUTPUT_KEYS:
            filled = dict(report['published'])
            filled[key] = Decimal('1')
            with self.assertRaises(orchestrator.ScorecardPromotionRefused):
                orchestrator.write_scorecard(filled)
        payload = schema_panel()
        payload['markets'][0]['open_interest_fp'] = '1'
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'panel.json'
            path.write_text(json.dumps(payload))
            with self.assertRaises(orchestrator.InventedInventoryRefused):
                orchestrator.load_panel(path)
        dropped = {
            'market_ticker': 'KXUFCFIGHT-26SEP22ORTDAS-ORT',
            'hypothetical_contracts': '1',
            'queue_ahead': '500',
            'orderbook_fp': {'yes_dollars': [['0.50', '1']], 'no_dollars': [['0.50', '1']]},
        }
        with self.assertRaises(orchestrator.OrchestratorError) as caught:
            orchestrator._label_book(schema_panel(), dropped, 'synthetic_schema_standin')
        self.assertEqual(str(caught.exception), 'dropped market')
        for path, raw in before.items():
            self.assertEqual(path.read_bytes(), raw)

    def test_live_orders_capital_arms_and_unpinned_orderbooks_are_refused(self):
        with self.assertRaises(orchestrator.LiveOrdersForbidden):
            orchestrator.execution_adapter()
        for mode in orchestrator.CAPITAL_ARMS:
            with self.assertRaises(orchestrator.CapitalArmForbidden):
                orchestrator.bakeoff_capital(mode)
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / 'book.json').write_text('{}')
            original = orchestrator.PRODUCTION_ORDERBOOK_DIR
            orchestrator.PRODUCTION_ORDERBOOK_DIR = Path(tmp)
            try:
                with self.assertRaises(orchestrator.OrchestratorError) as caught:
                    orchestrator.resolve_orderbooks()
                self.assertEqual(str(caught.exception), 'production orderbook pin')
            finally:
                orchestrator.PRODUCTION_ORDERBOOK_DIR = original
        choice = orchestrator.resolve_orderbooks()
        status = orchestrator.production_orderbook_status()
        self.assertEqual(choice['source'], 'synthetic_schema_standin')
        self.assertEqual(choice['production_orderbooks_present'], status['status'] == 'PINNED')
        self.assertEqual(choice['score_status'], 'NOT_SCORED')
        self.assertIs(choice['examiner_ready'], False)
        pin = (ROOT / 'fixtures' / 'PIN.md').read_text()
        self.assertIn('lab/astra-capture/c1-kxufcfight/orderbooks/', pin)
        self.assertIn('24426d80', pin)
        self.assertIn(orchestrator.FEEBOOK_COMMIT, pin)
        self.assertIn(orchestrator.RAILS_COMMIT, pin)

    def test_implementation_hashes_match_source(self):
        frozen = json.loads(orchestrator.FROZEN_EXPERIMENT.read_text())
        recorded = frozen['implementation_sha256']
        self.assertIsInstance(recorded, dict)
        for name, digest in recorded.items():
            self.assertEqual(orchestrator.sha256_file(ROOT / name), digest)
        spec = frozen['specification_sha256']
        for name, digest in spec.items():
            candidates = (ROOT / name, PARENT / name)
            path = next(candidate for candidate in candidates if candidate.is_file())
            self.assertEqual(orchestrator.sha256_file(path), digest, name)
        self.assertIn('ORDERBOOK_CAPTURE_SPEC.md', spec)
        admitted_key = 'lab/astra-capture/c1-kxufcfight/panel_admitted.json'
        if orchestrator.PANEL_ADMITTED.is_file():
            self.assertEqual(
                orchestrator.sha256_file(orchestrator.PANEL_ADMITTED),
                spec[admitted_key],
            )
        else:
            self.assertNotIn(admitted_key, spec)


if __name__ == '__main__':
    unittest.main()
