"""WX-FL scaffolding tests. ROI is synthetic. Pinned tape tests are counts only."""

import ast
import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

import orchestrator
import snapshot_loader


TICKER = 'KXHIGHNY-26SEP25-B67.5'
EVENT = 'KXHIGHNY-26SEP25'


def _trade(**overrides):
    body = {
        'ticker': TICKER,
        'event': EVENT,
        'city': 'KXHIGHNY',
        'date': '26SEP25',
        'created_time': '2026-09-25T18:00:00Z',
        'close_time': '2026-09-26T05:00:00Z',
        'settlement_ts': '2026-09-26T11:19:36Z',
        'received_at': '2026-09-25T18:00:01Z',
        'result': 'yes',
        'is_block_trade': False,
        'taker_outcome_side': 'yes',
        'taker_book_side': 'bid',
        'taker_side': 'yes',
        'yes_price_dollars': '0.10',
        'no_price_dollars': '0.90',
        'count_fp': '1',
        'synthetic': False,
    }
    body.update(overrides)
    return body


def _obs(arm, event, price, outcome, quantity='1', date=None, city=None):
    if date is None:
        date = event.split('-', 1)[1]
    if city is None:
        city = event.split('-')[0]
    return {
        'synthetic': True,
        'arm': arm,
        'event': event,
        'city': city,
        'date': date,
        'ticker': event + '-SYN',
        'p_taker': Decimal(price),
        'q': Decimal(quantity),
        'y_s': outcome,
    }


class AuthorityTests(unittest.TestCase):
    def test_pins_manifest_accept_ruling_and_bundle(self):
        report = orchestrator.verify_pins_manifest()
        self.assertTrue(report['pins_manifest_ok'])
        self.assertIsNone(report['results'])
        self.assertIsNone(report['pnl'])
        self.assertEqual(orchestrator.ACCEPT_SHA256, snapshot_loader.sha256_file(orchestrator.ACCEPT_PATH))
        self.assertEqual(orchestrator.RULING_SHA256, snapshot_loader.sha256_file(orchestrator.RULING_PATH))
        self.assertEqual(orchestrator.BUNDLE_SHA256, snapshot_loader.sha256_file(orchestrator.BUNDLE_TGZ))
        authority = json.loads(
            (orchestrator.ROOT / 'AUTHORITY_VERIFICATION.json').read_text(encoding='utf-8')
        )
        self.assertEqual(authority['accept_sha256'], orchestrator.ACCEPT_SHA256)
        self.assertEqual(authority['ruling_sha256'], orchestrator.RULING_SHA256)
        self.assertEqual(authority['freeze_sha256'], orchestrator.FREEZE_SHA256)
        self.assertEqual(authority['snapshot_sha256'], orchestrator.SNAPSHOT_SHA256)
        self.assertEqual(authority['bundle_sha256'], orchestrator.BUNDLE_SHA256)
        self.assertFalse(authority['pre_admitted_at_flag_possible'])
        self.assertEqual(authority['evidence_class'], 'IN_SAMPLE_DEV / HISTORICAL_REPLAY')
        self.assertIsNone(authority['results'])
        self.assertIsNone(authority['pnl'])

    def test_vendored_text_matches_the_bundle_manifest(self):
        root = orchestrator.PINS / 'vendored'
        manifest = (root / 'MANIFEST.sha256').read_text(encoding='utf-8')
        checked = 0
        for line in manifest.splitlines():
            digest, relative = line.split('  ', 1)
            path = root / relative
            if not path.is_file():
                continue
            self.assertEqual(snapshot_loader.sha256_file(path), digest, relative)
            checked += 1
        self.assertGreater(checked, 40)
        freeze = root / 'lab/governance/astra/packets/WX_FL_KXHIGH_SETTLED_TAPE/WX_FL_KXHIGH_SETTLED_TAPE_FREEZE_2026-10-01.md'
        self.assertEqual(snapshot_loader.sha256_file(freeze), orchestrator.FREEZE_SHA256)
        self.assertEqual(snapshot_loader.sha256_file(orchestrator.VENDORED_REGISTRY), orchestrator.REGISTRY_SHA256)
        self.assertFalse(list(root.rglob('archive.sqlite')))

    def test_sha_mismatch_does_not_open_sqlite(self):
        calls = []
        original = snapshot_loader.sqlite3.connect

        def boom(*args, **kwargs):
            calls.append((args, kwargs))
            raise AssertionError('sqlite opened')

        snapshot_loader.sqlite3.connect = boom
        try:
            with tempfile.NamedTemporaryFile() as handle:
                handle.write(b'not a database')
                handle.flush()
                with self.assertRaises(snapshot_loader.SnapshotShaMismatch):
                    snapshot_loader.open_snapshot(handle.name, '0' * 64)
        finally:
            snapshot_loader.sqlite3.connect = original
        self.assertEqual(calls, [])

    def test_live_db_and_capture_are_refused_before_open(self):
        with self.assertRaises(snapshot_loader.LiveDatabaseRefused):
            snapshot_loader.open_snapshot(
                '/tmp/lab/astra-capture/weather-nowcast/archive.sqlite',
                orchestrator.SNAPSHOT_SHA256,
            )
        with self.assertRaises(snapshot_loader.CaptureSqliteRefused):
            snapshot_loader.open_snapshot('/tmp/capture.sqlite', orchestrator.SNAPSHOT_SHA256)
        with self.assertRaises(snapshot_loader.CaptureSqliteRefused):
            orchestrator.read_capture_sqlite('capture.sqlite')
        with self.assertRaises(snapshot_loader.LiveDatabaseRefused):
            orchestrator.open_live_database('weather-nowcast/archive.sqlite')


class RefusalTests(unittest.TestCase):
    def test_live_order_http_get_lee_ready_and_rebin_raise(self):
        with self.assertRaises(orchestrator.LiveOrderRefused):
            orchestrator.live_order()
        with self.assertRaises(orchestrator.LiveHttpGetRefused):
            orchestrator.live_http_get('https://example.invalid/trade-api/v2/markets/trades')
        with self.assertRaises(orchestrator.LeeReadyRefused):
            orchestrator.infer_lee_ready({'yes_price_dollars': '0.10'})
        with self.assertRaises(orchestrator.LeeReadyRefused):
            orchestrator.classify_trade(_trade(lee_ready=True))
        with self.assertRaises(orchestrator.RebinRefused):
            orchestrator.rebin([{'band_id': 'custom'}])
        with self.assertRaises(orchestrator.KeepRefused):
            orchestrator.claim_keep()
        with self.assertRaises(orchestrator.CacheNotLiveR1P1):
            orchestrator.claim_live_r1p1()
        with self.assertRaises(orchestrator.RealTapeRoiRefused):
            orchestrator.measure_synthetic([_obs('WXFL0', EVENT, '0.10', 0, date='26SEP25') | {'synthetic': False}])

    def test_registry_boundaries(self):
        registry = orchestrator.load_band_registry()
        self.assertEqual(orchestrator.assign_arm('0.00', registry), ('WXFL0', 'b00'))
        self.assertEqual(orchestrator.assign_arm('0.1999999', registry), ('WXFL0', 'b01'))
        self.assertEqual(orchestrator.assign_arm('0.20', registry), ('WXFL1', 'b02'))
        self.assertEqual(orchestrator.assign_arm('0.7999999', registry), ('WXFL1', 'b07'))
        self.assertEqual(orchestrator.assign_arm('0.80', registry), ('WXFL2', 'b08'))
        self.assertEqual(orchestrator.assign_arm('1.00', registry), ('WXFL2', 'b09'))
        with self.assertRaises(orchestrator.RebinRefused):
            orchestrator.assign_arm('1.01', registry)

    def test_admit1_no_result_post_close_block_and_conflict(self):
        with self.assertRaises(orchestrator.Admit1WindowRejected):
            orchestrator.classify_trade(_trade(created_time='2026-09-27T00:00:00Z'))
        with self.assertRaises(orchestrator.Admit1WindowRejected):
            orchestrator.classify_trade(_trade(settlement_ts='2026-09-27T00:00:01Z'))
        missing = orchestrator.classify_trade(_trade(result=None))
        self.assertFalse(missing['included'])
        self.assertEqual(missing['reason'], 'market_result_not_yes_no')
        self.assertNotIn('row', missing)
        post = orchestrator.classify_trade(_trade(created_time='2026-09-26T05:00:00Z'))
        self.assertEqual(post['reason'], 'post_close')
        block = orchestrator.classify_trade(_trade(is_block_trade=True))
        self.assertEqual(block['reason'], 'block')
        conflict = orchestrator.classify_trade(_trade(taker_book_side='ask'))
        self.assertEqual(conflict['reason'], 'taker_conflict')
        price = orchestrator.classify_trade(_trade(no_price_dollars='0.80'))
        self.assertEqual(price['reason'], 'price_inconsistent')
        sep26 = orchestrator.classify_trade(_trade(
            ticker='KXHIGHNY-26SEP26-B67.5', event='KXHIGHNY-26SEP26', date='26SEP26',
        ))
        self.assertEqual(sep26['reason'], 'out_of_scope_sep26')
        included = orchestrator.classify_trade(_trade())
        self.assertTrue(included['included'])
        self.assertEqual(included['row']['arm'], 'WXFL0')
        self.assertIsNone(included['row']['pre_admitted_at'])
        self.assertFalse(included['row']['pre_admitted_at_flag_possible'])
        self.assertNotIn('p_taker', included['row'])
        self.assertNotIn('y_s', included['row'])

    def test_result_disagreement_is_a_hard_fail(self):
        rows = [
            {'ticker': 'T', 'status': 'finalized', 'result': 'yes'},
            {'ticker': 'T', 'status': 'finalized', 'result': 'no'},
        ]
        with self.assertRaises(snapshot_loader.ResultDisagreement):
            orchestrator.assert_finalized_results_agree(rows)
        self.assertTrue(orchestrator.assert_finalized_results_agree([
            {'ticker': 'T', 'status': 'finalized', 'result': 'yes'},
            {'ticker': 'T', 'status': 'finalized', 'result': 'yes'},
        ]))


class SyntheticMetricTests(unittest.TestCase):
    def test_threshold_is_six_of_eight_and_h2_is_less_or_equal(self):
        self.assertEqual(orchestrator.locdo_vote_threshold(8), 6)
        self.assertIsNone(orchestrator.locdo_vote_threshold(2))
        self.assertEqual(orchestrator.H2, 'maker_gross_roi_delta_FL2_minus_FL1 <= 0')
        votes = [Decimal('-1')] * 6 + [Decimal('1'), Decimal('1')]
        self.assertEqual(orchestrator.reading_h1(Decimal('-0.1'), votes), 'contradicts_H1')
        self.assertEqual(orchestrator.reading_h1(Decimal('0.1'), votes), 'inconclusive')
        self.assertEqual(orchestrator.reading_h2(Decimal('-0.1'), votes), 'consistent_with_H2')
        self.assertEqual(orchestrator.reading_h2(Decimal('0.1'), [Decimal('1')] * 6 + [Decimal('-1')] * 2), 'inconsistent_with_H2')
        self.assertEqual(orchestrator.reading_h1(Decimal('1'), [Decimal('1'), Decimal('1')]), 'inconclusive')
        self.assertEqual(orchestrator.verdict_for('contradicts_H1'), 'ITERATE')
        self.assertEqual(orchestrator.KILL_SCOPE, 'KXHIGHCHI/KXHIGHLAX/KXHIGHMIA/KXHIGHNY only')

    def test_equal_weighted_differs_from_trade_weighted_and_sep25_split(self):
        # City-day A: small FL0 win versus FL1. City-day B: large FL0 loss.
        # EW treats the two days equally. TW is dominated by day B's size.
        rows = [
            _obs('WXFL0', 'KXHIGHCHI-26SEP24', '0.10', 0, '1'),
            _obs('WXFL1', 'KXHIGHCHI-26SEP24', '0.50', 0, '1'),
            _obs('WXFL2', 'KXHIGHCHI-26SEP24', '0.90', 1, '1'),
            _obs('WXFL0', 'KXHIGHNY-26SEP25', '0.10', 1, '100'),
            _obs('WXFL1', 'KXHIGHNY-26SEP25', '0.50', 0, '100'),
            _obs('WXFL2', 'KXHIGHNY-26SEP25', '0.90', 0, '100'),
        ]
        measured = orchestrator.measure_synthetic(rows)
        ew = measured['full']['EW_delta_FL0_minus_FL1']
        tw = measured['full']['TW_delta_FL0_minus_FL1']
        self.assertIsNotNone(ew)
        self.assertIsNotNone(tw)
        self.assertNotEqual(ew, tw)
        self.assertEqual(measured['full']['n_eff_D01'], 2)
        self.assertIsNone(measured['reading'])
        self.assertIsNone(measured['results'])
        self.assertIsNone(measured['pnl'])
        self.assertIsNone(measured['maker_net_roi_cache'])
        self.assertEqual(len(measured['locdo']), 2)
        self.assertTrue(all(item['verdict_input'] for item in measured['locdo']))
        self.assertEqual(len(measured['lodo']), 2)
        self.assertTrue(all(item['verdict_input'] is False for item in measured['lodo']))
        self.assertEqual(len(measured['loco']), 2)
        self.assertTrue(all(item['verdict_input'] is False for item in measured['loco']))
        self.assertIsNone(measured['without_sep25']['lodo'])
        self.assertEqual(measured['without_sep25']['full']['n_eff_D01'], 1)
        # one_tick_worse moves maker return down and capital up versus the gross delta.
        stressed = orchestrator.measure_synthetic(rows, one_tick=True)
        self.assertNotEqual(
            stressed['full']['EW_delta_FL0_minus_FL1'],
            measured['full']['EW_delta_FL0_minus_FL1'],
        )
        # Hand check: q=1, p=0.10, Y=0 → roi = 0.10/0.90.
        solo = orchestrator.measure_synthetic([
            _obs('WXFL0', 'KXHIGHCHI-26SEP24', '0.10', 0, '2'),
            _obs('WXFL1', 'KXHIGHCHI-26SEP24', '0.50', 0, '2'),
        ])
        # Both arms are constant across the single city-day, so EW equals TW.
        self.assertEqual(solo['full']['EW_delta_FL0_minus_FL1'], solo['full']['TW_delta_FL0_minus_FL1'])
        expected = (Decimal('0.10') / Decimal('0.90')) - (Decimal('0.50') / Decimal('0.50'))
        self.assertEqual(solo['full']['EW_delta_FL0_minus_FL1'], expected)

    def test_locdo_reading_ignores_lodo_and_loco(self):
        # Eight city-days. FL0 beats FL1 on every day, so H1 is supported on LOCDO.
        # The two dates and four cities are not what the reading function receives.
        rows = []
        for event in orchestrator.CITY_DAYS:
            rows.append(_obs('WXFL0', event, '0.05', 0, '1'))
            rows.append(_obs('WXFL1', event, '0.50', 1, '1'))
            rows.append(_obs('WXFL2', event, '0.90', 1, '1'))
        measured = orchestrator.measure_synthetic(rows)
        votes = [item['EW_delta_FL0_minus_FL1'] for item in measured['locdo']]
        self.assertEqual(len(votes), 8)
        self.assertEqual(orchestrator.reading_h1(measured['full']['EW_delta_FL0_minus_FL1'], votes), 'supports_H1')
        h2_votes = [item['EW_delta_FL2_minus_FL1'] for item in measured['locdo']]
        self.assertEqual(
            orchestrator.reading_h2(measured['full']['EW_delta_FL2_minus_FL1'], h2_votes),
            'consistent_with_H2',
        )
        self.assertEqual(measured['verdict'], 'ITERATE')


class RealTapeCountTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.counts = orchestrator.build_counts()

    def test_timestamp_universe_and_gap_sensitivities(self):
        timestamp = self.counts['timestamp_universe']
        self.assertEqual(timestamp['trades_in_scope_pre_w0'], 33757)
        self.assertEqual(timestamp['by_date'], {'26SEP24': 638, '26SEP25': 33119})
        self.assertEqual(timestamp['by_city_day'], orchestrator.TRADES_BY_CITY_DAY)
        self.assertEqual(timestamp['n_markets'], 48)
        self.assertEqual(timestamp['trades_created_ge_w0'], 0)
        lit = self.counts['gm_lit']['timestamp_only']
        self.assertEqual(lit['dropped_n'], 27199)
        self.assertEqual(lit['kept_n'], 6558)
        self.assertEqual(lit['kept_by_city_day'], orchestrator.GM_LIT_KEPT_BY_CITY_DAY)
        pad = self.counts['gm_lit_pad']['timestamp_only']
        self.assertEqual(pad['dropped_n'], 33622)
        self.assertEqual(pad['kept_n'], 135)
        self.assertEqual(self.counts['gm_lit_pad']['role'], 'counts_only')
        self.assertFalse(self.counts['gm_lit']['decisive'])
        self.assertEqual(
            self.counts['gm_lit']['components_timestamp_only']['budget_only']['dropped_pct'],
            '53.61',
        )

    def test_gm_cov_reports_unproven_windows_without_loosening(self):
        windows = self.counts['gm_cov']['windows']
        budget = windows['budget']
        ticker_429 = windows['per_ticker_429']
        storm = windows['storm']
        self.assertEqual(budget['n_windows'], budget['proven'] + budget['not_proven'])
        self.assertEqual(ticker_429['n_windows'], ticker_429['proven'] + ticker_429['not_proven'])
        self.assertEqual(storm['n_windows'], storm['proven'] + storm['not_proven'])
        self.assertGreater(budget['not_proven'], 0)
        self.assertGreater(ticker_429['not_proven'], 0)
        self.assertGreater(storm['not_proven'], 0)
        self.assertEqual(budget['open_ended'], 36)
        self.assertEqual(ticker_429['open_ended'], 9)
        self.assertFalse(self.counts['cursor_minus_1s_assumed'])
        self.assertGreater(self.counts['gm_cov']['near_miss_complete_poll_requested_at_before_window_end'], 0)
        dropped = self.counts['gm_cov']['per_arm']['dropped_per_arm']
        kept = self.counts['gm_cov']['per_arm']['kept_per_arm']
        self.assertEqual(set(dropped), {'WXFL0', 'WXFL1', 'WXFL2'})
        self.assertEqual(
            sum(dropped.values()) + sum(kept.values()),
            self.counts['row_rule_included_n'],
        )
        city = self.counts['gm_lit']['per_arm']['kept_per_arm_city_day']
        for arm in orchestrator.ARMS:
            self.assertEqual(set(city[arm]), set(orchestrator.CITY_DAYS))

    def test_count_files_keep_results_null_and_omit_prices(self):
        with tempfile.TemporaryDirectory() as tmp:
            written = orchestrator.write_count_files(self.counts, tmp)
            self.assertIn('GM_COV_COUNTS.json', written)
            for name in written:
                payload = json.loads((Path(tmp) / name).read_text(encoding='utf-8'))
                self.assertIsNone(payload['results'])
                self.assertIsNone(payload['pnl'])
                self.assertIsNone(payload['net'])
                self.assertFalse(payload['pre_admitted_at_flag_possible'])
                self.assertEqual(payload['evidence_class'], 'IN_SAMPLE_DEV / HISTORICAL_REPLAY')
                self.assertEqual(payload['family_size'], 1)
                self.assertEqual(payload['verdict_ceiling'], 'ITERATE')
                self.assertFalse(payload['counts_toward_keep'])
                self.assertFalse(payload['promote'])
                self.assertEqual(payload['fee_label'], 'CACHE_NOT_R1P1')
                self.assertEqual(payload['out_of_domain_replication_of'], orchestrator.FL_BAND_FREEZE_SHA256)
                self.assertEqual(payload['accept_sha256'], orchestrator.ACCEPT_SHA256)
                self.assertEqual(payload['caveats'][2], 'Sep-25 carries 33,119 of 33,757 trades')
                self.assertNotIn('yes_price_dollars', payload)
                self.assertNotIn('no_price_dollars', payload)
                self.assertNotIn('p_taker', payload)
                self.assertIsNone(payload.get('maker_gross_roi'))
                self.assertIsNone(payload.get('EW_delta_FL0_minus_FL1'))

    def test_snapshot_open_is_readonly(self):
        frame = snapshot_loader.load_frame()
        self.assertEqual(frame['snapshot_sha256'], orchestrator.SNAPSHOT_SHA256)
        self.assertEqual(frame['snapshot_uri_suffix'], 'mode=ro&immutable=1')
        root = Path(tempfile.mkdtemp(prefix='wxfl-ro-'))
        archive_module = __import__('tarfile')
        with archive_module.open(orchestrator.BUNDLE_TGZ, 'r:*') as archive:
            archive.extractall(root, filter='data')
        snapshot = root / snapshot_loader.BUNDLE_DIRNAME / snapshot_loader.SNAPSHOT_REL
        connection = snapshot_loader.open_snapshot(snapshot, orchestrator.SNAPSHOT_SHA256)
        try:
            with self.assertRaises(Exception) as caught:
                connection.execute('CREATE TABLE wxfl_refused(x INT)')
            self.assertIn('readonly', str(caught.exception).lower())
        finally:
            connection.close()

    def test_published_card_stays_null(self):
        card = orchestrator.published_scorecard()
        self.assertIsNone(card['results'])
        self.assertIsNone(card['pnl'])
        shell = orchestrator.scorecard_shell()
        self.assertIsNone(shell['results'])
        self.assertIsNone(shell['pnl'])
        self.assertIsNone(shell['EW_delta_FL0_minus_FL1'])
        self.assertEqual(shell['status'], 'HOLD_PRE_PR')
        self.assertFalse(shell['scored'])
        hold = json.loads(
            (orchestrator.ROOT / 'EXAMINER_HOLD_PRE_PR.json').read_text(encoding='utf-8')
        )
        self.assertEqual(hold['status'], 'HOLD_PRE_PR')
        self.assertFalse(hold['scored'])
        self.assertIsNone(hold['results'])
        self.assertIsNone(hold['pnl'])


class SourceShapeTests(unittest.TestCase):
    def test_measure_synthetic_is_the_only_roi_entry_and_conduct_does_not_call_it_on_tape(self):
        source = (orchestrator.ROOT / 'orchestrator.py').read_text(encoding='utf-8')
        tree = ast.parse(source)
        called_from_build = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == 'build_counts':
                for child in ast.walk(node):
                    if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                        called_from_build.append(child.func.id)
        self.assertNotIn('measure_synthetic', called_from_build)
        self.assertNotIn('reading_h1', called_from_build)


if __name__ == '__main__':
    unittest.main()
