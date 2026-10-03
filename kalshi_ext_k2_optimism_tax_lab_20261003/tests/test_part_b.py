"""T05–T15 and T17. Part (b) is exercised on synthetic rows only."""

import ast
import json
import os
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from tests.support import lab_root, repo_root

BOX_SHA = frozenset({
    "a1e1027e8fd1e5bda30c3a4124e990048d5a7700cf2b08df24c1fbc5a0054e99",
    "7238e85874f3e231a9719aaa66847bd166c51c746f92f2e2ccc737ed96e439dd",
    "61a4c993fbea5940e5999177ffb5a0e3161219a8f84812af2d2f44d9f556641b",
    "fd5e10531f488f30baf05e2dd6f17c8f8823603ecbae457170dbbde66126fb95",
    "6f5af9071dd72dc398b0180b779a78da3cb2bfbb88a75217d9c6e65e3fb58819",
    "79be0f4e42e913c341b9186a9b7ee2e02bbb9c4d95d97368176b682e2e5e15ab",
    "ea354f2f4cf75a1a395fed7044c3a05ba0644a93852eb51adce16d8a5f226ef4",
})
FORBIDDEN_IMPORTS = {
    "sqlite3", "urllib", "requests", "http", "socket", "subprocess", "aiohttp", "websockets",
}
NAME_TOKENS = ("fill", "queue", "depth", "book", "quote", "replay", "simulate")
KEY_RE = __import__("re").compile(r"(^|_)(pnl|roi|keep|profit|sharpe)(_|$)", __import__("re").I)


def _py_files():
    root = lab_root()
    for folder in ("shared", "dev_pipeline", "becker_pipeline", "tests"):
        for path in (root / folder).glob("*.py"):
            yield path


def _imports(tree):
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.append(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            found.append(node.module.split(".")[0])
    return found


def _names(tree):
    found = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            found.append(node.name)
        elif isinstance(node, ast.Name):
            found.append(node.id)
        elif isinstance(node, ast.Attribute):
            found.append(node.attr)
        elif isinstance(node, ast.alias):
            found.append(node.name)
            if node.asname:
                found.append(node.asname)
    return found


def _registry():
    from shared.bands import load_registry
    return load_registry(lab_root() / "pins" / "bands_registry_10c.json")


def _market(ticker, event, result, close_time):
    return {
        "ticker": ticker,
        "event_ticker": event,
        "status": "finalized",
        "result": result,
        "close_time": close_time,
        "_fetched_at": "2025-11-25T00:00:00Z",
        "volume": 100,
    }


def _trade(trade_id, ticker, side="yes", yes_price=50, count=10, created="2025-09-04T18:00:00Z"):
    return {
        "trade_id": trade_id,
        "ticker": ticker,
        "count": count,
        "yes_price": yes_price,
        "no_price": 100 - yes_price,
        "taker_side": side,
        "created_time": created,
        "_fetched_at": "2025-11-25T12:00:00Z",
    }


class TestT05MixRefusal(unittest.TestCase):
    def test_concat_merge_join_compare(self):
        from shared.exceptions import BeckerMixRefused
        from shared.provenance import Provenanced

        dev = Provenanced([{"trade_id": "d"}], "DEV_B1B2")
        becker = Provenanced([{"trade_id": "b"}], "BECKER_A")
        for method in ("concat", "merge", "join", "zip_with", "compare"):
            with self.assertRaises(BeckerMixRefused):
                getattr(dev, method)(becker)

    def test_path_and_sha_refusals(self):
        from becker_pipeline.guards import refuse_becker_input
        from becker_pipeline.pins import cloud_input_shas
        from dev_pipeline.pins import BECKER_BOXONLY_SHA256, refuse_dev_input
        from shared.exceptions import BeckerMixRefused

        with self.assertRaises(BeckerMixRefused):
            refuse_dev_input("/tmp/somewhere/rows.parquet")
        with self.assertRaises(BeckerMixRefused):
            refuse_dev_input("/tmp/becker/rows.json")
        with self.assertRaises(BeckerMixRefused):
            refuse_dev_input("plain.json", sha=next(iter(BECKER_BOXONLY_SHA256)))
        with self.assertRaises(BeckerMixRefused):
            refuse_becker_input("lab/astra-science/nfl_factorial_lab_20260921/inputs/events.jsonl.gz")
        with self.assertRaises(BeckerMixRefused):
            refuse_becker_input("pins/EXT_K1_authentic_pins_2026-10-03.tgz")
        with self.assertRaises(BeckerMixRefused):
            refuse_becker_input("pins/EXT_K2_authentic_pins_2026-10-03.tgz")
        cloud = cloud_input_shas()
        self.assertIn(
            "cd300e664c2c5f2ff344c4b1eb17dd3f8e5f3326168b9dd8e3ade94a3a7382b4",
            cloud,
        )
        with self.assertRaises(BeckerMixRefused):
            refuse_becker_input("synthetic.json", sha=next(iter(cloud)), cloud_shas=cloud)

    def test_import_graph(self):
        for folder, banned in (
            ("dev_pipeline", "becker_pipeline"),
            ("becker_pipeline", "dev_pipeline"),
        ):
            for path in (lab_root() / folder).glob("*.py"):
                tree = ast.parse(path.read_text(encoding="utf-8"))
                for module in _imports(tree):
                    self.assertNotEqual(module, banned)
        for path in (lab_root() / "shared").glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for module in _imports(tree):
                self.assertNotIn(module, ("dev_pipeline", "becker_pipeline"))


class TestT06CrossCheck(unittest.TestCase):
    def test_trade_id_only(self):
        from shared.exceptions import CrossCheckKeyRefused
        from shared.provenance import cross_check, trade_id_overlap_count

        overlap = trade_id_overlap_count({"a", "b"}, {"b", "c"})
        self.assertIsInstance(overlap, int)
        self.assertEqual(overlap, 1)
        self.assertEqual(cross_check("trade_id", set(), set()), 0)
        for key in ("ticker", "price", "count", "side", "time", ("ticker", "price", "count", "side", "time")):
            with self.assertRaises(CrossCheckKeyRefused):
                cross_check(key, {"a"}, {"a"})


class TestT07Exclusion(unittest.TestCase):
    def test_open_no_result_and_sibling(self):
        from becker_pipeline.exclusion import assert_none_excluded, recompute_exclusion
        from shared.exceptions import OpenTickerRefused

        fetch = "2025-11-25T12:00:00Z"
        later = "2025-12-16T01:15:00Z"
        earlier = "2025-11-01T00:00:00Z"
        markets = [
            _market("OPEN-YES", "EVT-OPEN", "yes", later),
            _market("OPEN-SIB", "EVT-OPEN", "yes", earlier),
            _market("BLANK", "EVT-BLANK", "", earlier),
            _market("VOID", "EVT-VOID", "void", earlier),
            _market("KEEP", "EVT-KEEP", "no", earlier),
        ]
        trades = [
            _trade("t-open", "OPEN-YES"),
            _trade("t-sib", "OPEN-SIB"),
            _trade("t-blank", "BLANK"),
            _trade("t-void", "VOID"),
            _trade("t-keep", "KEEP"),
        ]
        for row in trades:
            row["_fetched_at"] = fetch
        doc = recompute_exclusion(markets, trades)
        self.assertIn("OPEN-YES", doc["open_at_trade_fetch_tickers"])
        self.assertIn("BLANK", doc["closed_no_result_tickers"])
        self.assertIn("VOID", doc["closed_no_result_tickers"])
        self.assertIn("OPEN-SIB", doc["excluded_tickers"])
        self.assertNotIn("KEEP", doc["excluded_tickers"])
        with self.assertRaises(OpenTickerRefused):
            assert_none_excluded(["KEEP", "OPEN-SIB"], doc["excluded_tickers"])
        box = repo_root() / "lab/astra-capture/external/becker_2026-10-03/data"
        self.assertFalse(box.exists())

    def test_excluded_ticker_cannot_enter_a_cell(self):
        from becker_pipeline.metrics import build_cells
        from shared.exceptions import OpenTickerRefused

        ticker = "KXNFLGAME-25SEP04AAAAAA-AA"
        rows = [_trade("s1", ticker)]
        markets = {
            ticker: _market(ticker, "KXNFLGAME-25SEP04AAAAAA", "no", "2025-09-05T00:00:00Z"),
        }
        with self.assertRaises(OpenTickerRefused):
            build_cells(rows, markets, _registry(), Decimal(1), [ticker], bootstrap_scale=0)


class TestT08HoldoutAdmit(unittest.TestCase):
    def test_window_and_identities(self):
        from dev_pipeline.pins import assert_dev_row, load_holdout_sets
        from shared.exceptions import Admit1WindowRejected, HoldoutRefused, SqlitePathRefused
        from shared.refusals import assert_not_holdout, assert_sqlite_path_refused, assert_timestamp_allowed

        with self.assertRaises(Admit1WindowRejected):
            assert_timestamp_allowed("2026-09-27T00:00:00Z")
        with self.assertRaises(Admit1WindowRejected):
            assert_timestamp_allowed("2026-09-30T03:59:59.999Z")
        assert_timestamp_allowed("2026-09-30T04:00:00Z")
        events, game_ids = load_holdout_sets()
        self.assertIn("KXNFLGAME-26SEP28PHICHI", events)
        self.assertIn("2026_03_PHI_CHI", game_ids)
        for event, game_id, ticker in (
            ("KXNFLGAME-26SEP28PHICHI", None, None),
            (None, "2026_03_PHI_CHI", None),
            ("KXNFLGAME-26SEP21NYGLAR", None, None),
            ("KXNFLGAME-26SEP24ATLGB", None, None),
            (None, None, "KXMLBSPREAD-26SEP28PHICHI-P3"),
        ):
            with self.assertRaises(HoldoutRefused):
                assert_not_holdout(
                    event=event, game_id=game_id, ticker=ticker,
                    holdout_events=events, holdout_game_ids=game_ids,
                )
        with self.assertRaises(HoldoutRefused):
            assert_dev_row(
                {"at": "2026-09-10T00:00:00Z", "ticker": "KXNFLGAME-26SEP28PHICHI-PHI", "event": "KXNFLGAME-26SEP28PHICHI"},
                events, game_ids,
                {"KXNFLGAME-26SEP28PHICHI-PHI": {}},
                {"KXNFLGAME-26SEP28PHICHI": {}},
            )
        with self.assertRaises(Admit1WindowRejected):
            assert_dev_row(
                {"at": "2026-09-27T00:00:00Z", "ticker": "KEEP", "event": "KEEP"},
                events, game_ids, {"KEEP": {}}, {"KEEP": {}},
            )
        from becker_pipeline.metrics import build_cells
        ticker = "KXNFLGAME-25SEP04AAAAAA-AA"
        market = _market(ticker, "KXNFLGAME-26SEP28PHICHI", "no", "2025-09-05T00:00:00Z")
        with self.assertRaises(HoldoutRefused):
            build_cells([_trade("h1", ticker)], {ticker: market}, _registry(), Decimal(1), [], bootstrap_scale=0)
        admit = _trade("h2", ticker, created="2026-09-27T00:00:00Z")
        market_ok = _market(ticker, "KXNFLGAME-25SEP04AAAAAA", "no", "2025-09-05T00:00:00Z")
        with self.assertRaises(Admit1WindowRejected):
            build_cells([admit], {ticker: market_ok}, _registry(), Decimal(1), [], bootstrap_scale=0)
        with self.assertRaises(SqlitePathRefused):
            assert_sqlite_path_refused("/var/lib/capture.sqlite")
        with self.assertRaises(SqlitePathRefused):
            assert_sqlite_path_refused("/var/lib/weather/archive.sqlite")

    def test_ast_import_ban(self):
        for path in _py_files():
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for module in _imports(tree):
                self.assertNotIn(module, FORBIDDEN_IMPORTS, path.name)


class TestT09Fees(unittest.TestCase):
    def test_part_a_vectors_and_part_b_proxy(self):
        from dev_pipeline.load import load_dev
        from shared.fees import (
            FEE_LABEL,
            MAKER_COEF,
            TAKER_COEF,
            ceil_6dp,
            model_quadratic,
            part_a_order_headline,
            part_b_group_cent,
            part_b_row_fee,
            read_kxnflgame_multiplier,
        )

        schedule = load_dev()["fee_schedule_text"]
        multiplier = read_kxnflgame_multiplier(schedule)
        self.assertEqual(multiplier, Decimal(1))
        one = Decimal(1)
        headline, _ = part_a_order_headline([(1, Decimal("0.50"))], one)
        self.assertEqual(headline, Decimal("0.01"))
        self.assertEqual(ceil_6dp(model_quadratic(MAKER_COEF, 1, Decimal("0.50"), one)), Decimal("0.004375"))
        vectors = (
            (Decimal("247.5"), Decimal("0.37"), Decimal("1.009615"), Decimal("1.01")),
            (Decimal("2.5"), Decimal("0.37"), Decimal("0.010199"), Decimal("0.02")),
            (Decimal("100"), Decimal("0.50"), Decimal("0.437500"), Decimal("0.44")),
            (Decimal("1"), Decimal("0.05"), Decimal("0.000832"), Decimal("0.01")),
            (Decimal("250"), Decimal("0.95"), Decimal("0.207813"), Decimal("0.21")),
        )
        for contracts, price, six, cent in vectors:
            model = model_quadratic(MAKER_COEF, contracts, price, one)
            self.assertEqual(ceil_6dp(model), six)
            got, _ = part_a_order_headline([(contracts, price)], one)
            self.assertEqual(got, cent)
        combined, _ = part_a_order_headline(
            [(Decimal("247.5"), Decimal("0.37")), (Decimal("2.5"), Decimal("0.37"))],
            one,
        )
        self.assertEqual(combined, Decimal("1.02"))
        part_b = (
            (MAKER_COEF, 1, 50, Decimal("0.004375"), Decimal("0.01"), Decimal("0.0044")),
            (MAKER_COEF, 100, 50, Decimal("0.4375"), Decimal("0.44"), Decimal("0.4375")),
            (MAKER_COEF, 10, 97, Decimal("0.0050925"), Decimal("0.01"), Decimal("0.0051")),
            (MAKER_COEF, 250, 37, Decimal("1.0198125"), Decimal("1.02"), Decimal("1.0199")),
            (MAKER_COEF, 1, 1, Decimal("0.00017325"), Decimal("0.01"), Decimal("0.0002")),
            (TAKER_COEF, 1, 50, Decimal("0.0175"), Decimal("0.02"), Decimal("0.0175")),
            (TAKER_COEF, 100, 50, Decimal("1.75"), Decimal("1.75"), Decimal("1.7500")),
            (TAKER_COEF, 10, 97, Decimal("0.02037"), Decimal("0.03"), Decimal("0.0204")),
            (TAKER_COEF, 1, 97, Decimal("0.002037"), Decimal("0.01"), Decimal("0.0021")),
            (TAKER_COEF, 250, 37, Decimal("4.07925"), Decimal("4.08"), Decimal("4.0793")),
            (TAKER_COEF, 1000, 99, Decimal("0.693"), Decimal("0.70"), Decimal("0.6930")),
        )
        for coef, contracts, cents, model, cent, subcent in part_b:
            got_model, got_cent, got_sub = part_b_row_fee(coef, contracts, cents, one)
            self.assertEqual(got_model, model)
            self.assertEqual(got_cent, cent)
            self.assertEqual(got_sub, subcent)
            self.assertNotEqual(got_cent, got_sub) if cent != subcent else None
        left = part_b_row_fee(TAKER_COEF, 2, 37, one)[1]
        self.assertEqual(left + left, Decimal("0.08"))
        self.assertEqual(part_b_group_cent([(2, 37), (2, 37)], TAKER_COEF, one), Decimal("0.07"))
        for cents in (1, 37, 50, 63, 99):
            self.assertEqual(
                part_b_row_fee(MAKER_COEF, 10, cents, one),
                part_b_row_fee(MAKER_COEF, 10, 100 - cents, one),
            )
        self.assertEqual(FEE_LABEL, "CACHE_NOT_R1P1")

    def test_net_fields_null_when_proxy_disabled(self):
        from becker_pipeline.metrics import build_cells

        ticker_a = "KXNFLGAME-25SEP04AAAAAA-AA"
        ticker_b = "KXNFLGAME-25SEP04BBBBBB-BB"
        rows = []
        for index in range(12):
            rows.append(_trade("na-%02d" % index, ticker_a, side="yes", count=3))
        for index in range(12):
            rows.append(_trade("nb-%02d" % index, ticker_b, side="no", count=3))
        markets = {
            ticker_a: _market(ticker_a, "KXNFLGAME-25SEP04AAAAAA", "no", "2025-09-05T00:00:00Z"),
            ticker_b: _market(ticker_b, "KXNFLGAME-25SEP04BBBBBB", "yes", "2025-09-05T00:00:00Z"),
        }
        doc = build_cells(
            rows, markets, _registry(), Decimal(1), [], net_enabled=False, bootstrap_scale=0,
        )
        net_cells = [cell for cell in doc["cells"] if cell["fee_variant"] == "NET_ILLUSTRATIVE"]
        self.assertTrue(net_cells)
        for cell in net_cells:
            self.assertIsNone(cell["value"])
            self.assertEqual(cell["fee_label"], "CACHE_NOT_R1P1")
            self.assertEqual(cell["net_label"], "NET_ILLUSTRATIVE_2026_SCHEDULE_NOT_HISTORICAL")
        gross = [cell for cell in doc["cells"] if cell["fee_variant"] == "GROSS" and cell["flag"] is None]
        self.assertTrue(gross)
        self.assertTrue(all(cell["gross_is_headline"] for cell in gross))


class TestT10ManifestTamper(unittest.TestCase):
    def test_one_byte_tamper_fails_before_parse(self):
        from dev_pipeline.pins import checked_bytes, verify_manifest
        from shared.canonical import sha256_file
        from shared.exceptions import ManifestTamper

        pin = (
            lab_root()
            / "pins/k1/EXT_K1_authentic_pins_2026-10-03/lab/astra-science"
            / "nfl_factorial_lab_20260921/inputs/markets.json"
        )
        source = (
            lab_root()
            / "pins/k2/EXT_K2_authentic_pins_2026-10-03/lab/governance/astra/packets"
            / "EXT_K2_OPTIMISM_TAX/SOURCE_PINS.json"
        )
        manifest = lab_root() / "pins/k2/EXT_K2_authentic_pins_2026-10-03/MANIFEST.sha256"
        part = lab_root() / "pins/EXT_K1_authentic_pins_2026-10-03.tgz.part-01"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for label, path in (("pin", pin), ("source", source), ("part", part)):
                raw = bytearray(path.read_bytes())
                raw[0] ^= 0x01
                flipped = root / (label + ".bin")
                flipped.write_bytes(raw)
                with self.assertRaises(ManifestTamper):
                    checked_bytes(flipped, sha256_file(path))
            man = bytearray(manifest.read_bytes())
            man[0] ^= 0x01
            (root / "MANIFEST.sha256").write_bytes(man)
            with self.assertRaises(ManifestTamper):
                verify_manifest(root, "MANIFEST.sha256", sha256_file(manifest))
            listed = root / "listed.json"
            listed.write_bytes(b"{\"ok\":true}")
            expected = sha256_file(listed)
            listed.write_bytes(b"{\"ok\":false}")
            from becker_pipeline.run_part_b import sha256_file as runner_sha
            self.assertNotEqual(runner_sha(listed), expected)
            with self.assertRaises(ManifestTamper):
                checked_bytes(listed, expected)

    def test_wrong_exclusion_sha_is_inconclusive_without_aggregates(self):
        from becker_pipeline.run_part_b import start_box_run
        from shared.exceptions import ReceiptMismatchRefused

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = root / "data"
            data.mkdir()
            (data / "note.txt").write_text("synthetic-not-becker", encoding="utf-8")
            manifest = root / "BECKER_BOXONLY_PIN_MANIFEST.json"
            exclusion = root / "BECKER_EXCLUSION_LIST_KXNFLGAME.json"
            manifest.write_text("{}\n", encoding="utf-8")
            exclusion.write_text("{}\n", encoding="utf-8")
            out = root / "out"
            with self.assertRaises(ReceiptMismatchRefused) as caught:
                start_box_run(data, manifest, exclusion, out, repo=repo_root())
            self.assertIn("INCONCLUSIVE", str(caught.exception))
            self.assertTrue((out / "PRE_RUN_RECEIPT.json").is_file())
            self.assertFalse((out / "PART_B_AGGREGATES.json").exists())
            self.assertFalse((lab_root() / "results_b" / "PART_B_AGGREGATES.json").exists())


class TestT11NoRowOutput(unittest.TestCase):
    def test_synthetic_writer_suppresses_small_cells(self):
        from becker_pipeline.metrics import build_cells
        from becker_pipeline.writer import FORBIDDEN_KEYS, write_aggregates

        ticker_a = "KXNFLGAME-25SEP04AAAAAA-AA"
        ticker_b = "KXNFLGAME-25SEP04BBBBBB-BB"
        ticker_c = "KXNFLGAME-25SEP01CCCCCC-CC"
        rows = []
        trade_ids = []
        for index in range(12):
            trade_id = "syn-a-%02d" % index
            trade_ids.append(trade_id)
            rows.append(_trade(trade_id, ticker_a, count=2, yes_price=37))
        for index in range(12):
            trade_id = "syn-b-%02d" % index
            trade_ids.append(trade_id)
            rows.append(_trade(trade_id, ticker_b, side="no", count=2, yes_price=63))
        trade_ids.append("syn-c-00")
        rows.append(_trade("syn-c-00", ticker_c, count=1, yes_price=10))
        markets = {
            ticker_a: _market(ticker_a, "KXNFLGAME-25SEP04AAAAAA", "no", "2025-09-05T00:00:00Z"),
            ticker_b: _market(ticker_b, "KXNFLGAME-25SEP04BBBBBB", "yes", "2025-09-05T00:00:00Z"),
            ticker_c: _market(ticker_c, "KXNFLGAME-25SEP01CCCCCC", "no", "2025-09-02T00:00:00Z"),
        }
        doc = build_cells(rows, markets, _registry(), Decimal(1), [], net_enabled=True, bootstrap_scale=0)
        flags = [cell for cell in doc["cells"] if cell["n_trade_rows"] < 20 or cell["n_events"] < 2]
        self.assertTrue(flags)
        for cell in flags:
            self.assertIsNone(cell["value"])
            self.assertEqual(cell["flag"], "SUPPRESSED_SMALL_CELL")
            self.assertNotIn("count", cell)
        kept = [cell for cell in doc["cells"] if cell["flag"] is None and cell["metric"] == "S"]
        self.assertTrue(any(cell["value"] is not None for cell in kept))
        with tempfile.TemporaryDirectory() as tmp:
            target = write_aggregates(doc, Path(tmp), trade_ids, [ticker_a, ticker_b, ticker_c])
            payload = json.loads(target.read_text(encoding="utf-8"))
            keys = []

            def walk(node):
                if isinstance(node, dict):
                    for key, value in node.items():
                        keys.append(key)
                        walk(value)
                elif isinstance(node, list):
                    for value in node:
                        walk(value)
                elif isinstance(node, str):
                    self.assertNotIn(node, set(trade_ids) | {ticker_a, ticker_b, ticker_c})

            walk(payload)
            self.assertTrue(set(keys).isdisjoint(FORBIDDEN_KEYS))
            self.assertIn("Derived aggregates from Jon Becker's prediction-market-analysis dataset", payload["attribution"])

    def test_repo_has_no_becker_bytes(self):
        from shared.canonical import sha256_file

        hits = []
        for dirpath, dirnames, filenames in os.walk(repo_root()):
            if ".git" in dirnames:
                dirnames.remove(".git")
            for name in filenames:
                if name.endswith(".parquet") or name.startswith("becker_kalshi_"):
                    hits.append(os.path.join(dirpath, name))
        self.assertEqual(hits, [])
        hashed = []
        pipe = os.popen("git ls-files")
        listed = pipe.read().splitlines()
        pipe.close()
        for rel in listed:
            path = repo_root() / rel
            if path.is_file():
                hashed.append(sha256_file(path))
        for path in lab_root().rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts:
                hashed.append(sha256_file(path))
        self.assertTrue(set(hashed).isdisjoint(BOX_SHA))


class TestT12NoQuoteModel(unittest.TestCase):
    def test_refused_columns_and_ast_names(self):
        from becker_pipeline.guards import REFUSED_MARKET_FIELDS, read_market_field
        from shared.exceptions import BeckerQuoteFieldRefused

        for field in REFUSED_MARKET_FIELDS:
            with self.assertRaises(BeckerQuoteFieldRefused):
                read_market_field({field: 1}, field)
        for path in (lab_root() / "becker_pipeline").glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for name in _names(tree):
                lowered = name  # case-sensitive: lowercase tokens only
                for token in NAME_TOKENS:
                    self.assertNotIn(token, lowered, "%s in %s" % (token, path.name))


class TestT13CloseTime(unittest.TestCase):
    def test_close_time_only_in_the_recompute(self):
        root = lab_root() / "becker_pipeline"
        for path in root.glob("*.py"):
            if path.name == "exclusion.py":
                continue
            self.assertNotIn("close_time", path.read_text(encoding="utf-8"))
        tree = ast.parse((root / "exclusion.py").read_text(encoding="utf-8"))
        holders = []
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                segment = ast.get_source_segment((root / "exclusion.py").read_text(encoding="utf-8"), node)
                if segment and "close_time" in segment:
                    holders.append(node.name)
        self.assertEqual(sorted(holders), ["market_columns", "recompute_exclusion"])


class TestT14TiersWeeksBands(unittest.TestCase):
    def test_tiers_weeks_and_registry_bands(self):
        from becker_pipeline.guards import refuse_tier_path
        from shared.bands import REGISTRY_SHA256, band_id_for_yes_price, refuse_custom_edges
        from shared.canonical import sha256_file
        from shared.exceptions import RebinRefused, TierRefused
        from shared.weeks import week_from_date
        import datetime as dt

        for path in (
            "becker_kalshi_trades_t1_KXNFLGAME.parquet",
            "data/becker_kalshi_markets_t3_KXNFLGAME_part000.parquet",
            "becker_kalshi_trades_t4.parquet",
        ):
            with self.assertRaises(TierRefused):
                refuse_tier_path(path)
        refuse_tier_path("becker_kalshi_trades_t0_KXNFLGAME_part000.parquet")
        fixtures = (
            (dt.date(2025, 9, 1), "PRE"),
            (dt.date(2025, 9, 2), "W01"),
            (dt.date(2025, 9, 4), "W01"),
            (dt.date(2025, 9, 8), "W01"),
            (dt.date(2025, 9, 9), "W02"),
            (dt.date(2025, 11, 24), "W12"),
            (dt.date(2025, 11, 25), "W13"),
        )
        for day, label in fixtures:
            self.assertEqual(week_from_date(day)[0], label)
        registry = _registry()
        mapping = {1: "b00", 9: "b00", 10: "b01", 89: "b08", 90: "b09", 99: "b09"}
        for cents, band in mapping.items():
            self.assertEqual(band_id_for_yes_price(cents, registry), band)
        path = lab_root() / "pins" / "bands_registry_10c.json"
        self.assertEqual(sha256_file(path), REGISTRY_SHA256)
        self.assertTrue(REGISTRY_SHA256.startswith("0860cbe2"))
        with self.assertRaises(RebinRefused):
            refuse_custom_edges([0.0, 0.2, 0.8, 1.0])


class TestT15Framing(unittest.TestCase):
    def test_null_results_and_label_cannot_move_the_gate(self):
        from dev_pipeline.orchestrator import refuse_becker_value
        from shared.exceptions import LabelDependentToGateRefused

        empty = json.loads((
            lab_root()
            / "pins/k2/EXT_K2_authentic_pins_2026-10-03/lab/governance/astra/packets"
            / "EXT_K2_OPTIMISM_TAX/EMPTY_RESULTS.json"
        ).read_text(encoding="utf-8"))
        self.assertIsNone(empty["results"])
        self.assertIsNone(empty["pnl"])
        self.assertIsNone(empty["roi"])
        self._assert_keys(empty)
        committed = lab_root() / "results_a" / "EMPTY_RESULTS.json"
        if committed.is_file():
            doc = json.loads(committed.read_text(encoding="utf-8"))
            self.assertIsNone(doc["results"])
            self.assertIsNone(doc["pnl"])
            self.assertIsNone(doc["roi"])
            self.assertIn(doc["verdict"], ("DESCRIPTIVE", "ITERATE", "INCONCLUSIVE", None))
            self.assertIsNone(doc["part_b"]["verdict"])
            self._assert_keys(doc)
        with self.assertRaises(LabelDependentToGateRefused):
            refuse_becker_value(0.1, "BECKER_A")
        with self.assertRaises(LabelDependentToGateRefused):
            refuse_becker_value(0.1, "SYNTHETIC_NOT_BECKER")

    def _assert_keys(self, node):
        if isinstance(node, dict):
            for key, value in node.items():
                if KEY_RE.search(str(key)):
                    self.assertIn(value, (None, False), key)
                if key in ("verdict",) and value is not None:
                    self.assertIn(value, ("DESCRIPTIVE", "ITERATE", "INCONCLUSIVE"))
                self._assert_keys(value)
        elif isinstance(node, list):
            for value in node:
                self._assert_keys(value)


class TestT17ExecutionSplit(unittest.TestCase):
    def test_runner_refuses_on_this_checkout(self):
        from becker_pipeline.run_part_b import start_box_run
        from shared.exceptions import BoxOnlyRefused

        missing = repo_root() / "lab/astra-capture/external/becker_2026-10-03/data"
        self.assertFalse(missing.exists())
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out"
            with self.assertRaises(BoxOnlyRefused):
                start_box_run(missing, Path(tmp) / "manifest.json", Path(tmp) / "exclusion.json", out)
            self.assertFalse(out.exists())
            data = Path(tmp) / "data"
            data.mkdir()
            (data / "placeholder.txt").write_text("not becker", encoding="utf-8")
            with self.assertRaises(BoxOnlyRefused):
                start_box_run(data, data / "placeholder.txt", data / "placeholder.txt", lab_root() / "results_b")
            self.assertFalse((lab_root() / "results_b" / "PRE_RUN_RECEIPT.json").exists())
            self.assertFalse((lab_root() / "results_b" / "PART_B_AGGREGATES.json").exists())


if __name__ == "__main__":
    unittest.main()
