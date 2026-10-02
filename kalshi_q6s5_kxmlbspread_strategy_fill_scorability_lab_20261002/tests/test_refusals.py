import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import ast
import unittest
from decimal import Decimal
from pathlib import Path

import support
from orchestrator import LABELS, check_pin
from scoring import score
from tape_quotes import (
    Admit1WindowRejected,
    CaptureSqliteRefused,
    ClosedUniverseRefused,
    LookaheadRefused,
    PinMismatch,
    refuse_sqlite_path,
)


LAB = Path(__file__).resolve().parents[1]


class Refusals(unittest.TestCase):
    def test_admit1_book_get_and_print(self):
        from tape_quotes import build_quotes
        stamped = '2026-09-28T00:00:00Z'
        with self.assertRaises(Admit1WindowRejected):
            support.quote([support.snapshot(support.DET, stamped)])
        with self.assertRaises(Admit1WindowRejected):
            build_quotes(
                [support.snapshot(support.DET, support.T0)],
                [support.market(support.DET, stamped)],
                {support.DET: support.TAPE_END},
                trades=None,
            )
        import fill_engine
        quotes = support.quote([support.snapshot(support.DET, support.T0)])
        with self.assertRaises(Admit1WindowRejected):
            fill_engine.run_fills(quotes, [support.trade(
                support.DET, stamped, 'no', '0.3000', '0.7000', trade_id='win',
            )])

    def test_admit1_settlement_clocks(self):
        from tempfile import TemporaryDirectory
        import hashlib
        from settled_join import settled_join
        payload = support.fills_bytes([support.filled_row(support.DET, '2026-09-25T05:00:02Z')])
        digest = hashlib.sha256(payload).hexdigest()
        with TemporaryDirectory() as directory:
            support.write_settlement(directory, response_utc='2026-09-28T00:00:00Z', settlement_ts='2026-09-26T12:00:00Z')
            with self.assertRaises(Admit1WindowRejected):
                settled_join(payload, digest, directory)
        with TemporaryDirectory() as directory:
            support.write_settlement(
                directory,
                settlement_ts='2026-09-28T01:00:00Z',
                response_utc='2026-10-02T03:29:21Z',
            )
            with self.assertRaises(Admit1WindowRejected):
                settled_join(payload, digest, directory)

    def test_pin_tamper(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as directory:
            path = Path(directory) / 'pin.txt'
            path.write_bytes(b'abc')
            expected = __import__('hashlib').sha256(b'abc').hexdigest()
            check_pin(path, expected)
            path.write_bytes(b'abd')
            with self.assertRaises(PinMismatch):
                check_pin(path, expected)

    def test_lee_ready_native_block_and_price(self):
        import fill_engine
        quotes = support.quote([
            support.snapshot(support.DET, support.T0, yes=('0.4000', '1.00')),
        ])
        lee = support.trade(
            support.DET, '2026-09-25T05:00:02Z', 'no', '0.2000', '0.8000', trade_id='lee',
        )
        lee['lee_ready'] = True
        with self.assertRaises(fill_engine.LeeReadyRefused):
            fill_engine.run_fills(quotes, [lee])
        conflict = support.trade(
            support.DET, '2026-09-25T05:00:02Z', 'yes', '0.2000', '0.8000',
            count='5.00', trade_id='conflict',
        )
        conflict['taker_outcome_side'] = 'no'
        fills = fill_engine.run_fills(quotes, [conflict])
        self.assertEqual(fills['counts']['excluded_native_conflict_n'], 1)
        self.assertFalse(any(row['filled'] and row['leg'] == 'maker' for row in fills['rows']))

    def test_queue_boundary(self):
        import fill_engine
        quotes = support.quote([
            support.snapshot(support.DET, support.T0, yes=('0.4000', '2.00'), no=('0.4000', '2.00')),
        ])

        def yes_filled(prints):
            fills = fill_engine.run_fills(quotes, prints)
            return [row for row in fills['rows'] if row['leg'] == 'maker' and row['side'] == 'yes'][0]['filled']

        self.assertFalse(yes_filled([support.trade(
            support.DET, '2026-09-25T05:00:02Z', 'no', '0.3000', '0.7000', count='2.00', trade_id='eq',
        )]))
        self.assertTrue(yes_filled([support.trade(
            support.DET, '2026-09-25T05:00:02Z', 'no', '0.3000', '0.7000', count='3.00', trade_id='over',
        )]))
        self.assertFalse(yes_filled([support.trade(
            support.DET, '2026-09-25T05:00:02Z', 'no', '0.4000', '0.6000', count='9.00', trade_id='touch',
        )]))
        touched = support.trade(
            support.DET, '2026-09-25T05:00:02Z', 'no', '0.4000', '0.6000', count='2.00', trade_id='touch-2',
        )
        through = support.trade(
            support.DET, '2026-09-25T05:00:03Z', 'no', '0.3000', '0.7000', count='1.00', trade_id='then',
        )
        fills = fill_engine.run_fills(quotes, [touched, through])
        yes = [row for row in fills['rows'] if row['leg'] == 'maker' and row['side'] == 'yes'][0]
        self.assertTrue(yes['filled'])
        self.assertEqual(yes['fill_price'], '0.4000')
        self.assertEqual(yes['fill_time'], '2026-09-25T05:00:03Z')

    def test_no_invent_and_missing_settlement(self):
        import fill_engine
        quotes = support.quote([support.snapshot(support.DET, support.T0, yes=('0.4000', '2.00'))])
        fills = fill_engine.run_fills(quotes, [])
        makers = [row for row in fills['rows'] if row['leg'] == 'maker']
        self.assertTrue(makers)
        self.assertTrue(all(row['filled'] is False for row in makers))
        document = {'rows': [support.filled_row(support.DET, '2026-09-25T05:00:02Z')]}
        scored = score(document, {})
        self.assertIsNone(scored['pnl'])
        self.assertEqual(scored['unresolved_inventory'], 1)
        self.assertFalse(scored['counts_toward_keep'])

    def test_closed_universe_and_sqlite(self):
        with self.assertRaises(ClosedUniverseRefused):
            support.quote([support.snapshot(support.SEP24, support.T0)])
        with self.assertRaises(ClosedUniverseRefused):
            support.quote([support.snapshot('KXHIGHNY-26SEP25-T70', support.T0)])
        with self.assertRaises(CaptureSqliteRefused):
            refuse_sqlite_path('lab/astra-capture/capture.sqlite')
        with self.assertRaises(CaptureSqliteRefused):
            refuse_sqlite_path('lab/astra-capture/weather-nowcast/archive.sqlite')

    def test_import_graph_and_sources(self):
        banned = {'urllib', 'requests', 'http', 'socket', 'sqlite3', 'settled_join'}
        for name in ('tape_quotes.py', 'fill_engine.py'):
            tree = ast.parse((LAB / name).read_text())
            found = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    found.update(alias.name.split('.')[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    found.add(node.module.split('.')[0])
            self.assertTrue(found.isdisjoint(banned))
        for name in ('tape_quotes.py', 'fill_engine.py', 'scoring.py', 'settled_join.py', 'orchestrator.py'):
            tree = ast.parse((LAB / name).read_text())
            found = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    found.update(alias.name.split('.')[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    found.add(node.module.split('.')[0])
            self.assertTrue(found.isdisjoint({'urllib', 'requests', 'http', 'socket', 'sqlite3'}))
        self.assertNotIn('settlement_value_dollars', (LAB / 'tape_quotes.py').read_text())
        self.assertNotIn('settlement_value_dollars', (LAB / 'fill_engine.py').read_text())
        join_source = (LAB / 'settled_join.py').read_text()
        self.assertNotIn('expiration_time', join_source)
        self.assertNotIn('result', join_source)

    def test_committed_results_stay_null(self):
        payload = __import__('json').loads((LAB / 'results' / 'EMPTY_RESULTS.json').read_text())
        self.assertIsNone(payload['results'])
        self.assertIsNone(payload['pnl'])
        self.assertIsNone(payload['roi'])
        self.assertIsNone(payload['metrics']['Q6S5A0_maker_vs_taker_roi_delta'])
        self.assertIsNone(payload['metrics']['Q6S5A1_fresh_vs_stale_gap'])
        self.assertFalse(payload['counts_toward_keep'])
        self.assertEqual(payload['evidence_class'], LABELS['evidence_class'])
        self.assertEqual(payload['A1_null_reason'], 'STALE_BIN_EMPTY')
        self.assertFalse((LAB / 'results' / 'quotes.json').exists())
        self.assertFalse((LAB / 'results' / 'fills.json').exists())
        with self.assertRaises(TypeError):
            from tape_quotes import build_quotes
            build_quotes([], [], {}, trades=None, size=2)

    def test_extra_snapshot_key_refused(self):
        row = support.snapshot(support.DET, support.T0)
        row['settlement_ts'] = '2026-10-02T00:00:00Z'
        with self.assertRaises(LookaheadRefused):
            support.quote([row])

    def test_missing_settlement_row_is_unresolved(self):
        from tempfile import TemporaryDirectory
        import hashlib
        from settled_join import settled_join
        rows = [
            support.filled_row(support.DET, '2026-09-25T05:00:02Z'),
            support.filled_row(support.PIT, '2026-09-25T05:00:02Z'),
        ]
        payload = support.fills_bytes(rows)
        digest = hashlib.sha256(payload).hexdigest()
        with TemporaryDirectory() as directory:
            support.write_settlement(directory, ticker=support.DET)
            joined = settled_join(payload, digest, directory)
        self.assertEqual(joined['unresolved_tickers'], [support.PIT])
        self.assertNotIn(support.PIT, joined['values'])
        mapped = {support.DET: Decimal(joined['values'][support.DET])}
        scored = score({'rows': rows}, mapped)
        self.assertEqual(scored['unresolved_inventory'], 1)
        self.assertIsNotNone(scored['pnl'])


if __name__ == '__main__':
    unittest.main()
