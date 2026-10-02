import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import unittest

import support
from settled_join import (
    PreCloseJoinRefused,
    SettlementValueRefused,
    settled_join,
)
from tape_quotes import ClosedUniverseRefused


class T2PreClose(unittest.TestCase):
    def _join(self, directory, fill_time):
        payload = support.fills_bytes([support.filled_row(support.DET, fill_time)])
        import hashlib
        digest = hashlib.sha256(payload).hexdigest()
        return settled_join(payload, digest, directory)

    def test_response_not_after_close(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as directory:
            support.write_settlement(directory, response_utc=support.CLOSE)
            with self.assertRaises(PreCloseJoinRefused):
                self._join(directory, '2026-09-25T05:00:02Z')

    def test_settlement_not_after_close(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as directory:
            support.write_settlement(directory, settlement_ts=support.CLOSE)
            with self.assertRaises(PreCloseJoinRefused):
                self._join(directory, '2026-09-25T05:00:02Z')

    def test_status_not_finalized(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as directory:
            support.write_settlement(directory, status='active')
            with self.assertRaises(PreCloseJoinRefused):
                self._join(directory, '2026-09-25T05:00:02Z')

    def test_missing_close(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as directory:
            support.write_settlement(directory, close_time=None)
            with self.assertRaises(PreCloseJoinRefused):
                self._join(directory, '2026-09-25T05:00:02Z')

    def test_fill_at_close(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as directory:
            support.write_settlement(directory)
            with self.assertRaises(PreCloseJoinRefused):
                self._join(directory, support.CLOSE)

    def test_value_domain(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as directory:
            support.write_settlement(directory, value='0.5')
            with self.assertRaises(SettlementValueRefused):
                self._join(directory, '2026-09-25T05:00:02Z')

    def test_sep24_ticker(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as directory:
            support.write_settlement(directory, ticker=support.SEP24)
            payload = support.fills_bytes([support.filled_row(support.SEP24, '2026-09-25T05:00:02Z')])
            import hashlib
            digest = hashlib.sha256(payload).hexdigest()
            with self.assertRaises(ClosedUniverseRefused):
                settled_join(payload, digest, directory)

    def test_dollars_win_over_contradicting_field(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as directory:
            support.write_settlement(directory, value='0.0000', contradict=True)
            joined = self._join(directory, '2026-09-25T05:00:02Z')
            self.assertEqual(joined['values'][support.DET], '0.0000')
            support.write_settlement(directory, value='1.0000', contradict=True)
            joined = self._join(directory, '2026-09-25T05:00:02Z')
            self.assertEqual(joined['values'][support.DET], '1.0000')


if __name__ == '__main__':
    unittest.main()
