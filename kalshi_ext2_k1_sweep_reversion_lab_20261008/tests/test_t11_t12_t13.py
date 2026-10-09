import ast
import unittest

import support
from ext2k1.constants import (
    ACCEPT_SHA256,
    ADVERSARY_PASS_SHA256,
    AGGREGATION,
    FEE_ADMISSION,
    FEE_BLOCK_REASON,
    FREEZE_JSON_SHA256,
    FREEZE_MD_SHA256,
    PERCENTILE_METHOD,
    SAMPLER_STRING,
    TAGS,
)
from ext2k1.gates import structural_counts
from ext2k1.sweeps import build


class _Spy(dict):
    def __init__(self, row):
        super().__init__(row)
        self.touched = set()

    def __getitem__(self, key):
        self.touched.add(key)
        return super().__getitem__(key)

    def get(self, key, default=None):
        self.touched.add(key)
        return super().get(key, default)


class T11Provenance(unittest.TestCase):
    def test_header(self):
        published = support.published()
        provenance = published["provenance"]
        self.assertEqual(
            set(provenance),
            {
                "python_version",
                "platform",
                "git_commit",
                "freeze_md_sha256",
                "freeze_json_sha256",
                "accept_sha256",
                "adversary_pass_sha256",
                "tags",
            },
        )
        self.assertEqual(provenance["freeze_md_sha256"], FREEZE_MD_SHA256)
        self.assertEqual(provenance["freeze_json_sha256"], FREEZE_JSON_SHA256)
        self.assertEqual(provenance["accept_sha256"], ACCEPT_SHA256)
        self.assertEqual(provenance["adversary_pass_sha256"], ADVERSARY_PASS_SHA256)
        self.assertEqual(provenance["tags"], list(TAGS))
        commit = provenance["git_commit"]
        self.assertTrue(commit is None or (len(commit) == 40 and all(c in "0123456789abcdef" for c in commit)))
        self.assertEqual(published["bootstrap"]["sampler"], SAMPLER_STRING)
        self.assertEqual(published["bootstrap"]["percentile_method"], PERCENTILE_METHOD)
        self.assertEqual(published["bootstrap"]["aggregation"], AGGREGATION)
        self.assertEqual(published["fee_admission"], FEE_ADMISSION)
        self.assertEqual(published["fee_block_reason"], FEE_BLOCK_REASON)
        self.assertIn("output_sha256", published)
        self.assertEqual(len(published["output_sha256"]), 64)


class T12Flags(unittest.TestCase):
    def test_null_profit_keys_and_false_flags(self):
        published = support.published()
        self._walk(published)
        self.assertIsNone(published["results"])
        self.assertIsNone(published["pnl"])
        self.assertIsNone(published["roi"])
        self.assertIsNone(published["keep"])

    def _walk(self, obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                folded = str(key).lower()
                if folded in {"roi", "pnl", "keep"}:
                    self.assertIsNone(value, key)
                if key in {"counts_toward_keep", "promote", "live_promotion", "feeds_gate"}:
                    self.assertIs(value, False, key)
                self._walk(value)
        elif isinstance(obj, list):
            for value in obj:
                self._walk(value)


class T13SweepAccess(unittest.TestCase):
    def test_key_spy_and_ast(self):
        tape = support.FIXTURES["tape"]
        kinds = [row.get("kind") for row in tape["rows"]]
        spies = [_Spy(dict(row)) for row in tape["rows"]]
        build(spies, tape["markets"])
        trade_keys = {"kind", "ticker", "at", "taker_side", "size"}
        for kind, spy in zip(kinds, spies):
            if kind == "quote":
                self.assertEqual(spy.touched, {"kind"})
            else:
                self.assertEqual(spy.touched, trade_keys)
        tree = ast.parse((support.LAB / "ext2k1" / "sweeps.py").read_text(encoding="utf-8"))
        banned = {"bid", "ask", "asof"}
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                self.assertNotIn(node.id, banned)
            elif isinstance(node, ast.Attribute):
                self.assertNotIn(node.attr, banned)
            elif isinstance(node, ast.Constant):
                self.assertNotIn(node.value, banned)
        counted = structural_counts(tape["rows"])
        self.assertEqual(
            counted["per_print_counts"],
            support.EXPECTED["structural_counts_synth"]["per_print_counts"],
        )
        self.assertEqual(
            {key: counted[key] for key in ("trades", "quotes", "tickers", "taker_yes_trades", "taker_no_trades")},
            {
                key: support.EXPECTED["structural_counts_synth"][key]
                for key in ("trades", "quotes", "tickers", "taker_yes_trades", "taker_no_trades")
            },
        )


if __name__ == "__main__":
    unittest.main()
