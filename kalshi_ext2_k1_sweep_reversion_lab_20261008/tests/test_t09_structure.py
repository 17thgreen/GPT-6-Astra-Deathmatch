import tempfile
import unittest
from pathlib import Path
from unittest import mock

import support
from ext2k1.constants import BUILDER_SHA256, Pins
from ext2k1.gates import structural_counts, structure_gate
from ext2k1.pins_io import REPO_ROOT, sha256_file, sweeps_module_sha256
from ext2k1.report import build_results, published_results

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


def _matching_pins(rows):
    observed = structural_counts(rows)
    observed["events"] = 1
    return Pins(observed, BUILDER_SHA256)


def _score(rows, markets, week, pins, builder_sha):
    return build_results(
        rows,
        markets,
        week,
        pins,
        builder_sha256=builder_sha,
        source_pins=support.SOURCE_PINS,
        sweeps_module_sha256=sweeps_module_sha256(),
        b2_rows=[],
        git_commit="synthetic",
    )


class T09Structure(unittest.TestCase):
    def test_structure_cases(self):
        markets = {"T-X": {"event": "XH-1"}}
        week = {"XH-1": 1}
        for case in support.FIXTURES["t09_structure_cases"]:
            got = structure_gate(case["rows"])
            self.assertEqual(got, case["expect"], case["id"])
            if case["expect"]["pass"]:
                continue
            with mock.patch("ext2k1.quotes.QuoteBook", side_effect=AssertionError("mid")) as book:
                _receipt, _document, body = _score(
                    case["rows"],
                    markets,
                    week,
                    _matching_pins(case["rows"]),
                    BUILDER_SHA256,
                )
            book.assert_not_called()
            published = published_results(body)
            self.assertEqual(published["verdict_table_evaluation"]["verdict"], "INCONCLUSIVE(STRUCTURE)")
            self.assertEqual(published["verdict_table_evaluation"]["rule"], "V1s")
            for key in _METRIC_KEYS:
                self.assertNotIn(key, published, case["id"])

    def test_count_gate_mismatch_is_v1_without_metrics(self):
        tape = support.FIXTURES["tape"]
        rows = tape["rows"][:-1]
        with mock.patch("ext2k1.quotes.QuoteBook", side_effect=AssertionError("mid")) as book:
            _receipt, _document, body = _score(
                rows,
                tape["markets"],
                tape["week_membership"],
                support.synthetic_pins(),
                BUILDER_SHA256,
            )
        book.assert_not_called()
        published = published_results(body)
        self.assertEqual(published["verdict_table_evaluation"]["verdict"], "INCONCLUSIVE")
        self.assertEqual(published["verdict_table_evaluation"]["rule"], "V1")
        for key in _METRIC_KEYS:
            self.assertNotIn(key, published)

    def test_builder_byte_flip_or_missing_is_structure(self):
        source = REPO_ROOT / "nfl_completion_lab_20260921" / "load_data.py"
        payload = bytearray(source.read_bytes())
        payload[-1] ^= 0x01
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "load_data.py"
            path.write_bytes(payload)
            flipped = sha256_file(path)
        self.assertNotEqual(flipped, BUILDER_SHA256)
        tape = support.FIXTURES["tape"]
        for observed in (flipped, None):
            with mock.patch("ext2k1.quotes.QuoteBook", side_effect=AssertionError("mid")) as book:
                _receipt, _document, body = _score(
                    tape["rows"],
                    tape["markets"],
                    tape["week_membership"],
                    support.synthetic_pins(),
                    observed,
                )
            book.assert_not_called()
            published = published_results(body)
            self.assertEqual(published["verdict_table_evaluation"]["verdict"], "INCONCLUSIVE(STRUCTURE)")
            self.assertEqual(published["verdict_table_evaluation"]["rule"], "V1s")
            for key in _METRIC_KEYS:
                self.assertNotIn(key, published)


if __name__ == "__main__":
    unittest.main()
