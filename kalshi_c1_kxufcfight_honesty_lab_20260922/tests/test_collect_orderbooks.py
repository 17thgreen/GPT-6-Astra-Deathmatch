"""Pin and refuse checks for the C1 GET-only orderbook collector.

No socket is opened. Freeze measurement fields stay null.
"""
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import collect_orderbooks
import orchestrator

BOOK = b'{"orderbook_fp":{"yes_dollars":[["0.4200","1.00"]],"no_dollars":[]}}'
EMPTY_BOOK = b'{"orderbook":{"yes":[],"no":[]}}'


def _dest(root):
    path = Path(root) / 'lab' / 'astra-capture' / 'c1-kxufcfight' / 'orderbooks'
    path.mkdir(parents=True)
    return path


def _transport(bodies):
    calls = []

    def transport(url):
        calls.append(url)
        ticker = url.rsplit('/', 2)[-2]
        status, body = bodies[ticker]
        return status, body

    transport.calls = calls
    return transport


class RouteTests(unittest.TestCase):
    def test_public_get_allowlist_refuses_private_and_unpinned_routes(self):
        ticker = orchestrator.ADMITTED_ORDERBOOK_TICKERS[0]
        url = collect_orderbooks.orderbook_url(ticker)
        self.assertEqual(collect_orderbooks.assert_public_get('GET', url), ticker)
        with self.assertRaises(collect_orderbooks.RouteRefused) as method:
            collect_orderbooks.assert_public_get('POST', url)
        self.assertEqual(str(method.exception), 'method')
        with self.assertRaises(collect_orderbooks.RouteRefused) as host:
            collect_orderbooks.assert_public_get('GET', 'https://trading.example/trade-api/v2/markets/%s/orderbook' % ticker)
        self.assertEqual(str(host.exception), 'host')
        with self.assertRaises(collect_orderbooks.RouteRefused) as query:
            collect_orderbooks.assert_public_get('GET', url + '?depth=1')
        self.assertEqual(str(query.exception), 'query')
        private = 'https://api.elections.kalshi.com/trade-api/v2/portfolio/orders'
        with self.assertRaises(collect_orderbooks.RouteRefused) as route:
            collect_orderbooks.assert_public_get('GET', private)
        self.assertEqual(str(route.exception), 'route')
        dropped = 'https://api.elections.kalshi.com/trade-api/v2/markets/KXUFCFIGHT-26SEP22ORTDAS-ORT/orderbook'
        with self.assertRaises(collect_orderbooks.RouteRefused) as ticker_refused:
            collect_orderbooks.assert_public_get('GET', dropped)
        self.assertEqual(str(ticker_refused.exception), 'ticker')
        with self.assertRaises(collect_orderbooks.RouteRefused) as header:
            collect_orderbooks.assert_public_get('GET', url, headers={'Authorization': 'secret'})
        self.assertEqual(str(header.exception), 'header')
        with TemporaryDirectory() as tmp:
            outside = Path(tmp) / 'orderbooks'
            outside.mkdir()
            with self.assertRaises(collect_orderbooks.RouteRefused) as dest:
                collect_orderbooks.assert_orderbook_dir(outside)
            self.assertEqual(str(dest.exception), 'destination')
        with self.assertRaises(collect_orderbooks.RouteRefused):
            collect_orderbooks._RefuseRedirect().redirect_request(None, None, 302, 'found', None, url)

    def test_failed_get_writes_nothing_and_records_fixture_gap(self):
        bodies = {ticker: (200, BOOK) for ticker in orchestrator.ADMITTED_ORDERBOOK_TICKERS}
        bodies['KXUFCFIGHT-26SEP22DEGMOR-DEG'] = (429, b'{}')
        with TemporaryDirectory() as tmp:
            dest = _dest(tmp)
            report = collect_orderbooks.collect(
                _transport(bodies),
                dest,
                gap_seconds=0,
                sleep=lambda _seconds: None,
            )
            self.assertEqual(report['status'], 'FIXTURE_GAP')
            self.assertEqual(report['score_status'], 'NOT_SCORED')
            self.assertIs(report['examiner_ready'], False)
            self.assertIsNone(report['results'])
            self.assertIsNone(report['pnl'])
            self.assertEqual(report['written'], [])
            self.assertEqual(list(dest.iterdir()), [])
            self.assertTrue(any(row['http_status'] == 429 for row in report['tickers']))

    def test_economics_payload_and_existing_json_are_refused(self):
        priced = b'{"orderbook_fp":{"yes_dollars":[],"no_dollars":[]},"pnl":"1.00"}'
        self.assertFalse(collect_orderbooks.capture_bytes_acceptable(priced))
        self.assertTrue(collect_orderbooks.capture_bytes_acceptable(EMPTY_BOOK))
        bodies = {ticker: (200, EMPTY_BOOK) for ticker in orchestrator.ADMITTED_ORDERBOOK_TICKERS}
        with TemporaryDirectory() as tmp:
            dest = _dest(tmp)
            (dest / 'stray.json').write_text('{}')
            before = (dest / 'stray.json').read_bytes()
            with self.assertRaises(orchestrator.OrchestratorError) as caught:
                collect_orderbooks.collect(_transport(bodies), dest, gap_seconds=0)
            self.assertEqual(str(caught.exception), 'production orderbook pin')
            self.assertEqual((dest / 'stray.json').read_bytes(), before)

    def test_complete_get_pins_bytes_and_score_stays_closed(self):
        bodies = {}
        for index, ticker in enumerate(orchestrator.ADMITTED_ORDERBOOK_TICKERS):
            bodies[ticker] = (
                200,
                b'{"orderbook_fp":{"yes_dollars":[["0.%02d00","1.00"]],"no_dollars":[]}}' % index,
            )
        sleeps = []
        with TemporaryDirectory() as tmp:
            dest = _dest(tmp)
            report = collect_orderbooks.collect(
                _transport(bodies),
                dest,
                gap_seconds=12,
                sleep=sleeps.append,
            )
            self.assertEqual(sleeps, [12, 12, 12])
            self.assertEqual(report['status'], 'PINNED_CANDIDATE')
            self.assertEqual(report['score_status'], 'NOT_SCORED')
            self.assertIsNone(report['pnl'])
            self.assertEqual(len(report['written']), 4)
            pins = {row['path']: row['sha256'] for row in report['written']}
            self.assertEqual(set(pins), set(orchestrator.expected_orderbook_pin_keys()))
            status = orchestrator.production_orderbook_status(dest, pins)
            self.assertEqual(status['status'], 'PINNED')
            self.assertEqual(status['score_status'], 'NOT_SCORED')
            self.assertIs(status['examiner_ready'], False)
            gate = orchestrator.examiner_gate(status)
            self.assertEqual(gate['score_status'], 'NOT_SCORED')
            self.assertEqual(gate['reason'], 'PINNED_AWAITING_EXAMINER')
            self.assertIsNone(gate['results'])
            self.assertIsNone(gate['pnl'])
            self.assertIn('NOT_SCORED', gate['note'])
            choice = {
                'source': 'production_pin',
                'production_orderbook_status': 'PINNED',
                'examiner_ready': True,
            }
            with self.assertRaises(orchestrator.ScorecardPromotionRefused):
                orchestrator.assert_score_gate(choice)
            with self.assertRaises(orchestrator.ScorecardPromotionRefused):
                orchestrator.assert_score_gate({
                    'source': 'synthetic_schema_standin',
                    'production_orderbook_status': 'FIXTURE_GAP',
                    'examiner_ready': False,
                })
            target = dest / (orchestrator.ADMITTED_ORDERBOOK_TICKERS[0] + '.json')
            target.write_bytes(target.read_bytes() + b' ')
            with self.assertRaises(orchestrator.OrchestratorError) as caught:
                orchestrator.production_orderbook_status(dest, pins)
            self.assertEqual(str(caught.exception), 'production orderbook pin')


class GateTests(unittest.TestCase):
    def test_checkout_gate_matches_the_freeze_and_stays_unscored(self):
        frozen = json.loads(orchestrator.FROZEN_EXPERIMENT.read_text())
        status = orchestrator.production_orderbook_status()
        gate = orchestrator.examiner_gate(status)
        self.assertEqual(frozen['examiner_score_status'], 'NOT_SCORED')
        self.assertIs(frozen['examiner_ready'], False)
        self.assertIsNone(frozen['results'])
        self.assertIsNone(frozen['pnl'])
        self.assertEqual(frozen['production_orderbook_status'], status['status'])
        self.assertEqual(frozen['production_orderbook_pins'], status['pins'])
        self.assertEqual(gate['score_status'], 'NOT_SCORED')
        self.assertIn('orderbooks/', gate['note'])
        self.assertIn(orchestrator.EXAMINER_GATE_NOTE, frozen['examiner_gate'])
        choice = orchestrator.resolve_orderbooks()
        self.assertEqual(choice['source'], 'synthetic_schema_standin')
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.assert_score_gate(choice)
        with self.assertRaises(orchestrator.ScorecardPromotionRefused):
            orchestrator.write_scorecard(orchestrator.published_scorecard())


if __name__ == '__main__':
    unittest.main()
