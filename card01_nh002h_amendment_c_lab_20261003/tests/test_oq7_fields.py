"""OQ-7 builder fields and the T14 isolation check. Synthetic inputs only."""
from __future__ import annotations

import ast
import copy
import json
import unittest
from pathlib import Path

from card01_amc.score import score_document
from card01_amc.verdict import apply_verdict
from tests.support import LAB, build_from, universe
from tests.test_builder_gate import _built, _fc, _inputs, _map, _snap


_OQ7 = ("mid_raw", "p_model_raw", "depth_rejected")
_READERS = ("score.py", "verdict.py", "swing_stress.py")


def _score_rows():
    return [
        {
            "race_id": "XA-01",
            "state": "XA",
            "mapping_status": "KXHOUSERACE",
            "y": 1,
            "p_market": 0.4,
            "p_model": 0.6,
            "mid_raw": 0.4,
            "p_model_raw": 0.6,
            "depth_rejected": [{"race_id": "XA-09"}],
        },
        {
            "race_id": "XB-01",
            "state": "XB",
            "mapping_status": "LEGACY",
            "y": 0,
            "p_market": 0.3,
            "p_model": 0.2,
            "mid_raw": 0.3,
            "p_model_raw": 0.2,
        },
    ]


class OQ7BuilderTests(unittest.TestCase):
    def test_two_sided_mid_and_raw_forecast_survive_a_book_exclusion(self):
        codes, forecast, mapping, book = _inputs()
        index = codes.index("AL-02")
        built = _built(forecast, mapping, book)
        row = built["rows"][index]
        self.assertEqual(row["mid_raw"], 0.5)
        self.assertEqual(row["mid_raw_status"], "OK")
        self.assertEqual(row["p_model_raw"], 0.55)
        self.assertEqual(row["p_model_raw_status"], "OK")
        self.assertEqual(row["p_model"], 0.55)

        book2 = copy.deepcopy(book)
        _snap(book2, "AL-02")["yes_bid"] = 0.0
        excluded = _built(forecast, mapping, book2)["rows"][index]
        self.assertEqual(excluded["exclusion_reason"], "no_two_sided_book")
        self.assertIsNone(excluded["p_model"])
        self.assertIsNone(excluded["p_market"])
        self.assertIsNone(excluded["mid_raw"])
        self.assertEqual(excluded["mid_raw_status"], "no_two_sided_book")
        self.assertEqual(excluded["p_model_raw"], 0.55)
        self.assertEqual(excluded["p_model_raw_status"], "OK")

    def test_mid_status_follows_the_first_listed_book_reason(self):
        codes, forecast0, mapping0, book0 = _inputs()
        index = codes.index("AL-02")
        cases = {
            "snapshot_outside_window": lambda f, m, b: _snap(b, "AL-02").update(
                {"received_at_utc": "2026-11-02T21:44:59Z"}
            ),
            "no_ticker_for_mapped_race": lambda f, m, b: _map(m, "AL-02").update({"chosen_ticker": ""}),
            "mapping_unresolved": lambda f, m, b: _map(m, "AL-02").update(
                {"status": "unresolved_rate_limited"}
            ),
            "no_admissible_forecast": lambda f, m, b: _fc(f, "AL-02").update({"dem_prob": "55"}),
        }
        for reason, mutate in cases.items():
            forecast, mapping, book = (
                copy.deepcopy(forecast0),
                copy.deepcopy(mapping0),
                copy.deepcopy(book0),
            )
            mutate(forecast, mapping, book)
            row = _built(forecast, mapping, book)["rows"][index]
            self.assertEqual(row["exclusion_reason"], reason, reason)
            if reason == "no_admissible_forecast":
                self.assertIsNone(row["p_model_raw"])
                self.assertEqual(row["p_model_raw_status"], "no_admissible_forecast")
                self.assertEqual(row["mid_raw_status"], "OK")
            else:
                self.assertIsNone(row["mid_raw"], reason)
                self.assertEqual(row["mid_raw_status"], reason, reason)
                self.assertEqual(row["p_model_raw"], 0.55, reason)

    def test_file_level_forecast_reason_sets_p_model_raw_status(self):
        doc, raw = universe()
        codes = doc["universe_2026_house"]
        from tests.support import full_books

        forecast, mapping, book = full_books(codes)
        forecast["source_fetched_at_utc"] = "2026-11-01T22:00:01Z"
        built = build_from(doc, raw, forecast, mapping, book)
        row = built["rows"][0]
        self.assertEqual(row["exclusion_reason"], "no_admissible_forecast")
        self.assertIsNone(row["p_model"])
        self.assertIsNone(row["p_model_raw"])
        self.assertEqual(row["p_model_raw_status"], "no_admissible_forecast")


class T14IsolationTests(unittest.TestCase):
    def test_scorer_verdict_and_swing_do_not_name_oq7_fields(self):
        for name in _READERS:
            tree = ast.parse((LAB / "card01_amc" / name).read_text())
            hits = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value in _OQ7:
                    hits.append((name, node.value, node.lineno))
                if isinstance(node, ast.Attribute) and node.attr in _OQ7:
                    hits.append((name, node.attr, node.lineno))
                if isinstance(node, ast.Name) and node.id in _OQ7:
                    hits.append((name, node.id, node.lineno))
            self.assertEqual(hits, [])

    def test_gate_writes_depth_rejected_and_does_not_name_raw_fields(self):
        tree = ast.parse((LAB / "card01_amc" / "entry_gate.py").read_text())
        reads = []
        writes = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and node.value in ("mid_raw", "p_model_raw"):
                reads.append(node.value)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr == "get" and node.args:
                    arg = node.args[0]
                    if isinstance(arg, ast.Constant) and arg.value == "depth_rejected":
                        reads.append("get")
            if isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Constant):
                if node.slice.value == "depth_rejected" and isinstance(node.ctx, ast.Load):
                    reads.append("subscript")
            if isinstance(node, ast.Dict):
                for key in node.keys:
                    if isinstance(key, ast.Constant) and key.value == "depth_rejected":
                        writes += 1
        self.assertEqual(reads, [])
        self.assertGreaterEqual(writes, 1)

    def test_deleting_or_replacing_oq7_fields_leaves_score_and_verdict_identical(self):
        base = {"rows": _score_rows()}
        original = score_document(base)
        verdict = apply_verdict(original)
        deleted = {"rows": []}
        for row in _score_rows():
            clone = dict(row)
            clone.pop("mid_raw", None)
            clone.pop("p_model_raw", None)
            clone.pop("depth_rejected", None)
            deleted["rows"].append(clone)
        replaced = {"rows": []}
        for row in _score_rows():
            clone = dict(row)
            clone["mid_raw"] = "replaced"
            clone["p_model_raw"] = -1
            clone["depth_rejected"] = [9]
            replaced["rows"].append(clone)
        self.assertEqual(json.dumps(score_document(deleted), sort_keys=True), json.dumps(original, sort_keys=True))
        self.assertEqual(json.dumps(score_document(replaced), sort_keys=True), json.dumps(original, sort_keys=True))
        self.assertEqual(json.dumps(apply_verdict(score_document(deleted)), sort_keys=True), json.dumps(verdict, sort_keys=True))
        self.assertEqual(json.dumps(apply_verdict(score_document(replaced)), sort_keys=True), json.dumps(verdict, sort_keys=True))


class T16IgnoreTests(unittest.TestCase):
    def test_lab_gitignore_covers_regime_output(self):
        text = (LAB / ".gitignore").read_text()
        self.assertIn("CARD01_REGIME_SPLIT_SECONDARY_*.json", text)

    def test_committed_fixtures_are_the_synthetic_kit(self):
        names = {path.name for path in (LAB / "tests" / "fixtures").glob("SYNTH_*")}
        self.assertTrue(
            {
                "SYNTH_CONDUCTOR_ACCEPT_FEE_FILL.json",
                "SYNTH_FEE_SOURCE_v2_example.json",
                "SYNTH_PACKET_INDEX_excerpt.md",
                "SYNTH_R1_EXPECTED_VALUES.json",
            }.issubset(names)
        )


if __name__ == "__main__":
    unittest.main()
