import ast
import unittest
from pathlib import Path

import support  # noqa: F401
from errors import Admit1WindowRejected, HoldoutRefused, SqlitePathRefused
from pins_io import LAB, assert_path_allowed
from refusals import assert_not_holdout, assert_timestamp_allowed

FORBIDDEN = {"sqlite3", "urllib", "requests", "http", "socket", "aiohttp", "websockets"}


class T04Refusals(unittest.TestCase):
    def test_admit1_half_open_window(self):
        with self.assertRaises(Admit1WindowRejected):
            assert_timestamp_allowed("2026-09-27T00:00:00Z")
        with self.assertRaises(Admit1WindowRejected):
            assert_timestamp_allowed("2026-09-30T03:59:59.999Z")
        assert_timestamp_allowed("2026-09-30T04:00:00Z")
        assert_timestamp_allowed("2026-09-26T23:59:59Z")

    def test_holdout_and_sqlite_paths(self):
        for event in (
            "KXNFLGAME-26SEP28PHICHI",
            "KXNFLGAME-26SEP21NYGLAR",
            "KXNFLGAME-26SEP24ATLGB",
        ):
            with self.assertRaises(HoldoutRefused):
                assert_not_holdout(event=event)
        with self.assertRaises(HoldoutRefused):
            assert_not_holdout(game_id="2026_03_PHI_CHI")
        with self.assertRaises(HoldoutRefused):
            assert_not_holdout(ticker="KXMLBSPREAD-26SEP25TEST-A")
        for path in (
            "lab/astra-capture/prospective/capture.sqlite",
            "lab/astra-capture/weather-nowcast/archive.sqlite",
        ):
            with self.assertRaises(SqlitePathRefused):
                assert_path_allowed(path)

    def test_lab_sources_have_no_network_or_sqlite_imports(self):
        for path in LAB.glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    names = [alias.name.split(".")[0] for alias in node.names]
                elif isinstance(node, ast.ImportFrom):
                    names = [node.module.split(".")[0]] if node.module else []
                else:
                    continue
                self.assertFalse(FORBIDDEN.intersection(names), path.name)


if __name__ == "__main__":
    unittest.main()
