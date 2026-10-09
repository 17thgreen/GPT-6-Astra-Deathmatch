"""Box notes N-1, N-2, and N-3. Synthetic rows only."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import support
from ext2k1.constants import BUILDER_SHA256, Pins
from ext2k1.errors import Admit1WindowRejected, SourcePinMismatch
from ext2k1.gates import structural_counts, structure_gate
from ext2k1.pins_io import sha256_file, sweeps_module_sha256, verify_run_pins
from ext2k1.report import body_if_sweeps_sha_differs, build_receipt, build_results, published_results

_METRIC_KEYS = (
    "primary",
    "cells",
    "impact_profile",
    "loo",
    "placebo",
    "b2_join",
    "IDX_sha256",
    "bootstrap",
)


def _pins_for(rows):
    observed = structural_counts(rows)
    observed["events"] = 1
    return Pins(observed, BUILDER_SHA256)


def _score(rows, builder_sha):
    markets = {"T-X": {"event": "XH-1"}}
    week = {"XH-1": 1}
    return build_results(
        rows,
        markets,
        week,
        _pins_for(rows),
        builder_sha256=builder_sha,
        source_pins=support.SOURCE_PINS,
        sweeps_module_sha256=sweeps_module_sha256(),
        b2_rows=[],
        git_commit="synthetic",
    )


class NFollowup(unittest.TestCase):
    def test_n1_changed_or_missing_builder_writes_structure(self):
        markets_body = b'{"ok": true}\n'
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            markets = root / "markets.json"
            markets.write_bytes(markets_body)
            changed = root / "load_data.py"
            changed.write_bytes(b"changed-builder\n")
            pins = {
                "pins": [
                    {
                        "role": "B1 markets",
                        "path": "markets.json",
                        "bytes": markets.stat().st_size,
                        "sha256": sha256_file(markets),
                    },
                    {
                        "role": "B1 quote builder",
                        "path": "load_data.py",
                        "bytes": 5284,
                        "sha256": BUILDER_SHA256,
                    },
                ]
            }
            pin_path = root / "SOURCE_PINS.json"
            pin_path.write_text(json.dumps(pins), encoding="utf-8")
            checked = verify_run_pins(root, pin_path)
            builder = [entry for entry in checked if entry["role"] == "B1 quote builder"][0]
            self.assertEqual(builder["sha256"], sha256_file(changed))
            self.assertNotEqual(builder["sha256"], BUILDER_SHA256)
            self.assertFalse((root / "RESULTS.json").exists())

            pins["pins"][1]["path"] = "missing_load_data.py"
            pin_path.write_text(json.dumps(pins), encoding="utf-8")
            missing = verify_run_pins(root, pin_path)
            missed = [entry for entry in missing if entry["role"] == "B1 quote builder"][0]
            self.assertIsNone(missed["sha256"])

            pins["pins"][0]["sha256"] = "0" * 64
            pin_path.write_text(json.dumps(pins), encoding="utf-8")
            with self.assertRaises(SourcePinMismatch):
                verify_run_pins(root, pin_path)
            self.assertFalse((root / "RESULTS.json").exists())

        rows = [
            {"kind": "quote", "ticker": "T-X", "at": 120, "asof": 60, "bid": 0.4, "ask": 0.42},
            {"ticker": "T-X", "at": 100.25, "taker_side": "yes", "size": 1.0},
        ]
        for observed, reason in ((builder["sha256"], "C2_BUILDER_SHA_MISMATCH"), (None, "C2_BUILDER_SHA_MISSING")):
            with mock.patch("ext2k1.quotes.QuoteBook", side_effect=AssertionError("mid")) as book:
                _receipt, _document, body = _score(rows, observed)
            book.assert_not_called()
            published = published_results(body)
            verdict = published["verdict_table_evaluation"]
            self.assertEqual(verdict["verdict"], "INCONCLUSIVE(STRUCTURE)")
            self.assertEqual(verdict["rule"], "V1s")
            self.assertEqual(verdict["reason"], reason)
            self.assertEqual(_receipt["b1_quote_builder"]["reason"], reason)
            for key in _METRIC_KEYS:
                self.assertNotIn(key, published)

    def test_n2_sweeps_sha_mismatch_writes_v1(self):
        rows = [
            {"ticker": "T-X", "at": 10.0, "taker_side": "yes", "size": 1000.0},
            {"kind": "quote", "ticker": "T-X", "at": 120, "asof": 60, "bid": 0.4, "ask": 0.42},
        ]
        with mock.patch("ext2k1.quotes.QuoteBook", side_effect=AssertionError("mid")) as book:
            receipt, _document = build_receipt(
                rows,
                {"T-X": {"event": "XH-1"}},
                {"XH-1": 1},
                _pins_for(rows),
                builder_sha256=BUILDER_SHA256,
                source_pins=support.SOURCE_PINS,
                sweeps_module_sha256=sweeps_module_sha256(),
            )
            body = body_if_sweeps_sha_differs(receipt, "0" * 64, "synthetic")
        book.assert_not_called()
        self.assertIsNotNone(body)
        published = published_results(body)
        verdict = published["verdict_table_evaluation"]
        self.assertEqual(verdict["verdict"], "INCONCLUSIVE")
        self.assertEqual(verdict["rule"], "V1")
        self.assertEqual(verdict["reason"], "SWEEPS_SHA_MISMATCH")
        for key in _METRIC_KEYS:
            self.assertNotIn(key, published)
        self.assertIsNone(body_if_sweeps_sha_differs(receipt, receipt["sweeps_sha256"], "synthetic"))

    def test_n3_malformed_timestamp_is_structure(self):
        base_quote = {"kind": "quote", "ticker": "T-X", "at": 120, "asof": 60, "bid": 0.4, "ask": 0.42}
        base_trade = {"ticker": "T-X", "at": 100.25, "taker_side": "yes", "size": 1.0}
        cases = []
        for bad in (float("nan"), float("inf"), "not-a-time"):
            quote = dict(base_quote)
            quote["asof"] = bad
            cases.append([quote, dict(base_trade)])
            trade = dict(base_trade)
            trade["at"] = bad
            cases.append([dict(base_quote), trade])
        for rows in cases:
            gate = structure_gate(rows)
            self.assertFalse(gate["pass"])
            self.assertEqual(gate["reason"], "STRUCTURE_TIMESTAMP_MALFORMED")
            with mock.patch("ext2k1.quotes.QuoteBook", side_effect=AssertionError("mid")) as book:
                _receipt, _document, body = _score(rows, BUILDER_SHA256)
            book.assert_not_called()
            published = published_results(body)
            verdict = published["verdict_table_evaluation"]
            self.assertEqual(verdict["verdict"], "INCONCLUSIVE(STRUCTURE)")
            self.assertEqual(verdict["rule"], "V1s")
            self.assertEqual(verdict["reason"], "STRUCTURE_TIMESTAMP_MALFORMED")
            for key in _METRIC_KEYS:
                self.assertNotIn(key, published)
        from datetime import datetime, timezone

        instant = datetime(2026, 9, 27, 0, 0, tzinfo=timezone.utc).timestamp()
        with self.assertRaises(Admit1WindowRejected):
            structure_gate(
                [{"kind": "quote", "ticker": "T-X", "at": instant + 60, "asof": instant, "bid": 0.4, "ask": 0.42}]
            )

    def test_n3_malformed_at_inside_headline_sweep_skips_builder(self):
        """A size>=1000 group with a bad trade time must not reach the sweep builder."""
        quote = {"kind": "quote", "ticker": "T-X", "at": 120, "asof": 60, "bid": 0.4, "ask": 0.42}
        for bad in (float("nan"), float("inf"), "not-a-time", None):
            rows = [
                dict(quote),
                {"ticker": "T-X", "at": 50.5, "taker_side": "no", "size": 1000.0},
                {"ticker": "T-X", "at": bad, "taker_side": "yes", "size": 1000.0},
                {"ticker": "T-X", "at": bad, "taker_side": "yes", "size": 1.0},
            ]
            gate = structure_gate(rows)
            self.assertFalse(gate["pass"])
            self.assertEqual(gate["reason"], "STRUCTURE_TIMESTAMP_MALFORMED")
            with mock.patch("ext2k1.report.build_sweeps", side_effect=AssertionError("builder")) as sweeps:
                with mock.patch("ext2k1.quotes.QuoteBook", side_effect=AssertionError("mid")) as book:
                    receipt, document, body = _score(rows, BUILDER_SHA256)
            sweeps.assert_not_called()
            book.assert_not_called()
            self.assertEqual(document["sweeps"], [])
            self.assertEqual(receipt["structure_gate"]["reason"], "STRUCTURE_TIMESTAMP_MALFORMED")
            published = published_results(body)
            verdict = published["verdict_table_evaluation"]
            self.assertEqual(verdict["verdict"], "INCONCLUSIVE(STRUCTURE)")
            self.assertEqual(verdict["rule"], "V1s")
            self.assertEqual(verdict["reason"], "STRUCTURE_TIMESTAMP_MALFORMED")
            for key in _METRIC_KEYS:
                self.assertNotIn(key, published)


if __name__ == "__main__":
    unittest.main()
