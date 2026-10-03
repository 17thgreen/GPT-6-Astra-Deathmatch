"""Substring scan of a synthetic part (b) run. Conductor ruling sha prefix 6142d4c7.

The runner's aggregate check exact-matches t0 trade_ids and traded market
tickers only. This test does not change that runner. It scans every file the
synthetic end-to-end path writes, including the pre-run receipt, for any
synthetic trade_id, market ticker, or event ticker as a substring.
"""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tests.test_part_b import _market, _trade


def _fixtures():
    """Same synthetic universe as the existing untraded-market publish test."""
    keep_event = "KXNFLGAME-25SEP04AAAAAA"
    excl_event = "KXNFLGAME-25SEP04BBBBBB"
    alone_event = "KXNFLGAME-25SEP05CCCCCC"
    keep = "KXNFLGAME-25SEP04AAAAAA-AA"
    direct = "KXNFLGAME-25SEP04BBBBBB-BB"
    sibling = "KXNFLGAME-25SEP04BBBBBB-CC"
    alone = "KXNFLGAME-25SEP05CCCCCC-DD"
    inside = "KXNFLGAME-25SEP04BBBBBB-EE"
    earlier = "2025-11-01T00:00:00Z"
    later = "2025-12-16T01:15:00Z"
    markets = [
        _market(keep, keep_event, "no", earlier),
        _market(direct, excl_event, "", earlier),
        _market(sibling, excl_event, "yes", earlier),
        _market(alone, alone_event, "", later),
        _market(inside, excl_event, "", later),
    ]
    markets[-2]["status"] = "active"
    markets[-1]["status"] = "active"
    trades = [
        _trade("syn-keep", keep),
        _trade("syn-direct", direct),
        _trade("syn-sibling", sibling),
    ]
    return markets, trades


def _freeze_text():
    return "\n".join([
        "| Trade rows / traded tickers / traded events | **3 / 3 / 2** |",
        "| **Open at trade fetch** (clock) | **0 tickers**, 0 rows |",
        "| No yes/no `result` | 0 open + **1 closed** (1 rows) |",
        "| **Excluded** (ticker-level union = event-level closure) | **2 tickers / 1 events / 2 rows** |",
        "| **Eligible** | **1 tickers / 1 events / 1 rows** |",
        "",
        "or it has no markets row (0).",
        "",
        "Selection-bias statement (binding): synthetic selection text for the untraded fixture.",
        "",
        "coverage statement: synthetic coverage sentence.",
        "",
    ])


def banned_identifiers(markets, trades):
    """t0 trade ids, every market ticker, and every event ticker.

    This fixture has no t1–t4 trade rows. Those ids are included only when a
    synthetic row actually carries one.
    """
    trade_ids = {row["trade_id"] for row in trades}
    for row in trades:
        for tier in ("t1", "t2", "t3", "t4"):
            extra = row.get(tier + "_trade_id") or row.get(tier)
            if isinstance(extra, str) and extra:
                trade_ids.add(extra)
    market_tickers = {market["ticker"] for market in markets}
    event_tickers = {market["event_ticker"] for market in markets}
    banned = trade_ids | market_tickers | event_tickers
    if "" in banned:
        raise AssertionError("empty identifier")
    return trade_ids, market_tickers, event_tickers, banned


def substring_hits(text, banned):
    """Flag a banned identifier wherever it occurs inside a longer string."""
    return sorted(item for item in banned if item in text)


def scan_directory(root, banned):
    hits = []
    files = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        files.append(path)
        text = path.read_text(encoding="utf-8")
        for item in substring_hits(text, banned):
            hits.append((path.name, item))
    return files, hits


class TestPartBSubstringIdentifierScan(unittest.TestCase):
    def test_synthetic_run_has_no_identifier_substrings(self):
        from becker_pipeline.exclusion import empty_scan, exclusion_from_scan, note_trade
        from becker_pipeline.run_part_b import (
            _receipt,
            _run_after_receipt,
            _write_receipt,
            directory_hash,
        )
        from shared.canonical import canon_bytes

        markets, trades = _fixtures()
        trade_ids, market_tickers, event_tickers, banned = banned_identifiers(markets, trades)
        traded = {row["ticker"] for row in trades}
        untraded = sorted(market_tickers - traded)
        self.assertTrue(untraded)
        self.assertTrue(event_tickers)
        self.assertTrue(trade_ids)
        self.assertTrue(all(market["event_ticker"] for market in markets))
        self.assertIn("syn-keep", trade_ids)

        scan = empty_scan()
        for row in trades:
            note_trade(scan, row)
        traded_markets = [market for market in markets if market["ticker"] in scan["n_rows"]]
        pinned = exclusion_from_scan(
            traded_markets, scan,
            source_trades_sha256="aa" * 32,
            source_markets_sha256="bb" * 32,
            rule="event level",
        )
        for ticker in untraded:
            self.assertNotIn(ticker, scan["n_rows"])

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = root / "data"
            data.mkdir()
            trade_path = data / "trades.parquet"
            market_path = data / "markets.parquet"
            trade_path.write_bytes(b"synthetic-trades")
            market_path.write_bytes(b"synthetic-markets")
            exclusion = root / "exclusion.json"
            exclusion.write_bytes(canon_bytes(pinned))
            freeze_path = root / "freeze.md"
            freeze_path.write_text(_freeze_text(), encoding="utf-8")
            out = root / "out"
            _write_receipt(out, _receipt("0" * 40, "ab" * 32, "cd" * 32, "ef" * 32, "12" * 32, "34" * 32, None))
            calls = {"n": 0}

            def fake_rows(path, columns):
                del path, columns
                calls["n"] += 1
                if calls["n"] == 1:
                    return iter(markets)
                return iter(trades)

            with patch("becker_pipeline.run_part_b.iter_parquet_rows", fake_rows):
                _run_after_receipt(
                    {}, [], exclusion, freeze_path, out, data, directory_hash(data),
                    {"sha256": "aa" * 32}, trade_path,
                    {"sha256": "bb" * 32}, market_path,
                    frozenset(),
                )
            files, hits = scan_directory(out, banned)
            names = {path.name for path in files}
            self.assertIn("PRE_RUN_RECEIPT.json", names)
            self.assertIn("PART_B_AGGREGATES.json", names)
            self.assertIn("BOX_ONLY_OUTPUT_SHA256.json", names)
            self.assertEqual(hits, [])

            event_ticker = sorted(event_tickers)[0]
            untraded_ticker = untraded[0]
            source = (out / "PART_B_AGGREGATES.json").read_text(encoding="utf-8")
            self.assertNotIn(event_ticker, source)
            self.assertNotIn(untraded_ticker, source)
            event_wrapper = "lead-" + event_ticker + "-tail"
            untraded_wrapper = "lead-" + untraded_ticker + "-tail"
            self.assertGreater(len(event_wrapper), len(event_ticker))
            self.assertGreater(len(untraded_wrapper), len(untraded_ticker))
            self.assertNotIn(event_wrapper, banned)
            self.assertNotIn(untraded_wrapper, banned)
            event_copy = root / "event_inject.json"
            untraded_copy = root / "untraded_inject.json"
            event_copy.write_text(source.replace("{", '{"probe":"%s",' % event_wrapper, 1), encoding="utf-8")
            untraded_copy.write_text(source.replace("{", '{"probe":"%s",' % untraded_wrapper, 1), encoding="utf-8")
            event_text = event_copy.read_text(encoding="utf-8")
            untraded_text = untraded_copy.read_text(encoding="utf-8")
            self.assertNotEqual(event_text, event_ticker)
            self.assertNotEqual(untraded_text, untraded_ticker)
            self.assertIn(event_ticker, substring_hits(event_text, banned))
            self.assertIn(untraded_ticker, substring_hits(untraded_text, banned))
            self.assertNotIn(event_ticker, {event_text})
            self.assertNotIn(untraded_ticker, {untraded_text})
            parsed = json.loads(event_text)
            self.assertIn(event_ticker, parsed["probe"])
            self.assertNotEqual(parsed["probe"], event_ticker)
