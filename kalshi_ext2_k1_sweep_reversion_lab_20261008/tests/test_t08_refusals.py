"""R19 refusals. The strings becker, *.parquet, and capture.sqlite are the refusal list."""

import ast
import unittest

import support
from ext2k1.errors import (
    Admit1WindowRejected,
    BeckerRefused,
    ClosedUniverseRefused,
    HoldoutRefused,
    OutcomeFieldRefused,
)
from ext2k1.gates import count_gate
from ext2k1.refusals import (
    BECKER_TOKEN,
    CAPTURE_DB_NAME,
    PARQUET_SUFFIX,
    assert_no_result_fields,
    assert_not_holdout,
    assert_source_path,
    assert_timestamp_allowed,
)
from ext2k1.sweeps import build

_IMPORTS = {"sqlite3", "urllib", "requests", "http", "socket", "subprocess"}


class T08Refusals(unittest.TestCase):
    def test_admit1_half_open_window(self):
        with self.assertRaises(Admit1WindowRejected):
            assert_timestamp_allowed("2026-09-27T00:00:00Z")
        with self.assertRaises(Admit1WindowRejected):
            assert_timestamp_allowed("2026-09-30T03:59:59.999Z")
        assert_timestamp_allowed("2026-09-30T04:00:00Z")
        assert_timestamp_allowed("2026-09-26T23:59:59Z")

    def test_holdout_ids_from_the_public_list(self):
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
        with self.assertRaises(HoldoutRefused):
            assert_not_holdout(ticker="KXNFLGAME-26SEP28PHICHI-PHI")
        self.assertTrue(assert_not_holdout(event="KXNFLGAME-26SEP09NESEA"))

    def test_unknown_ticker_and_event(self):
        markets = {"T-X": {"event": "XH-1"}}
        with self.assertRaises(ClosedUniverseRefused):
            build(
                [{"ticker": "NO-SUCH", "at": 1.0, "taker_side": "yes", "size": 10.0}],
                markets,
            )
        with self.assertRaises(ClosedUniverseRefused):
            count_gate(
                [{"ticker": "T-X", "at": 1.0, "taker_side": "yes", "size": 1.0}],
                {"T-X": {"event": "NOT-IN-WEEK"}},
                {"XH-1": 1},
                support.synthetic_pins(),
            )

    def test_production_import_scan(self):
        package = support.LAB / "ext2k1"
        for path in sorted(package.glob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    names = [alias.name.split(".")[0] for alias in node.names]
                elif isinstance(node, ast.ImportFrom):
                    names = [node.module.split(".")[0]] if node.module else []
                else:
                    continue
                self.assertFalse(_IMPORTS.intersection(names), path.name)

    def test_becker_parquet_and_capture_db_paths(self):
        self.assertEqual(BECKER_TOKEN, "becker")
        self.assertEqual(PARQUET_SUFFIX, "*.parquet")
        self.assertEqual(CAPTURE_DB_NAME, "capture.sqlite")
        with self.assertRaises(BeckerRefused):
            assert_source_path("extracts/becker/trades.csv")
        with self.assertRaises(BeckerRefused):
            assert_source_path("tables/book.parquet")
        with self.assertRaises(HoldoutRefused):
            assert_source_path("var/lib/capture.sqlite")

    def test_outcome_fields_and_b2_allowlist(self):
        for key in ("result", "settlement", "settled"):
            with self.assertRaises(OutcomeFieldRefused):
                assert_no_result_fields({key: 1})
        with self.assertRaises(OutcomeFieldRefused):
            assert_no_result_fields({"outcome": "yes"})
        from ext2k1.b2join import guard_row

        guard_row({"outcome": "yes", "outcome_mid_at_fill": 0.5, "kind": "maker"}, allow_fill_fields=True)
        package = support.LAB / "ext2k1"
        for path in sorted(package.glob("*.py")):
            if path.name == "b2join.py":
                continue
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("outcome", text, path.name)
            self.assertNotIn("outcome_mid_at_fill", text, path.name)


if __name__ == "__main__":
    unittest.main()
