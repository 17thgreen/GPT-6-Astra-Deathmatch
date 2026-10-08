"""dem_name step, retired same-party triggers, and Q6 linkage."""
from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from card01_amc.build_rows import NO_DEMOCRAT_RE, BuilderError, build, dumps, q5_orderbook_status
from card01_amc.dem_name_step import (
    ADD_DEM_NAME_SHA256,
    run_dem_name_step,
    validate_dem_name_doc,
)
from tests.support import LAB, full_books, sha256_bytes, universe

ORIGINAL = LAB / "tests" / "fixtures" / "SYNTH_forecast_original_dem_prob_92.json"
V1 = LAB / "tests" / "fixtures" / "SYNTH_forecast_original_dem_prob_92.dem_name_v1.json"


def _codes():
    doc, raw = universe()
    return doc, raw, doc["universe_2026_house"]


def _accepted(codes, forecast, edits=None, drop=()):
    by_code = {row["race_code"]: row for row in forecast["rows"]}
    rows = []
    for code in codes:
        if code in drop:
            continue
        row = {
            "race_code": code,
            "dem_prob": by_code[code]["dem_prob"],
            "dem_name": "Synthetic Placeholder",
            "dem_name_status": "RESOLVED",
            "same_party_excluded_s5": False,
        }
        if edits and code in edits:
            row.update(edits[code])
        rows.append(row)
    return {
        "status": "DEM_NAME_ACCEPTED",
        "reason": None,
        "expected_script_sha256": ADD_DEM_NAME_SHA256,
        "observed_script_sha256": ADD_DEM_NAME_SHA256,
        "original_sha256": None,
        "v1_sha256": None,
        "check": {"byte_identical": True, "sha256": "ab" * 32},
        "v1": {"version": "dem_name_v1", "rows": rows},
    }


def _assemble(forecast, mapping, book, universe_doc, universe_raw, selection, step):
    blobs = {
        "forecast": json.dumps(forecast).encode() if forecast is not None else None,
        "mapping": json.dumps(mapping).encode(),
        "book": json.dumps(book).encode(),
        "selection": json.dumps(selection, sort_keys=True).encode(),
    }
    shas = {
        "universe": sha256_bytes(universe_raw),
        "forecast": sha256_bytes(blobs["forecast"]) if blobs["forecast"] is not None else None,
        "mapping": sha256_bytes(blobs["mapping"]),
        "book": sha256_bytes(blobs["book"]),
        "selection": sha256_bytes(blobs["selection"]),
    }
    if selection.get("status") == "SELECTED" and blobs["forecast"] is not None:
        selection = dict(selection)
        selection["selected_derived_sha256"] = shas["forecast"]
        blobs["selection"] = json.dumps(selection, sort_keys=True).encode()
        shas["selection"] = sha256_bytes(blobs["selection"])
    return build(
        universe_doc,
        forecast,
        mapping,
        book,
        shas,
        selection=selection,
        dem_name_step=step,
    )


class DemNameBuilderTests(unittest.TestCase):
    def _world(self):
        doc, raw, codes = _codes()
        forecast, mapping, book = full_books(codes)
        return doc, raw, codes, forecast, mapping, book

    def _row(self, built, code):
        return next(row for row in built["rows"] if row["race_id"] == code)

    def test_no_democrat_same_party_and_case(self):
        doc, raw, codes, forecast, mapping, book = self._world()
        edits = {
            "AL-02": {"dem_name": "(No Democrat)", "same_party_excluded_s5": True},
            "AZ-01": {"dem_name": "(no Democrat — top-two)", "same_party_excluded_s5": True},
            "CA-22": {"dem_name": "(NO DEMOCRAT)", "same_party_excluded_s5": True},
        }
        built = _assemble(
            forecast, mapping, book, doc, raw,
            {"status": "SELECTED"},
            _accepted(codes, forecast, edits),
        )
        for code in edits:
            row = self._row(built, code)
            self.assertEqual(row["exclusion_reason"], "NO_DEMOCRAT", code)
            self.assertIn("SAME_PARTY_S5", row["exclusion_reasons"], code)
            self.assertIsNone(row["p_model"], code)
            self.assertTrue(row["dem_name_flags"]["no_democrat"], code)
            self.assertTrue(row["dem_name_flags"]["same_party_s5"], code)

    def test_prefix_matches_the_add_dem_name_boundary(self):
        def prefix_test(name):
            token = "(no democrat"
            folded = name.casefold()
            if not folded.startswith(token):
                return False
            if len(folded) == len(token):
                return True
            nxt = folded[len(token)]
            return not (nxt.isalnum() or nxt == "_")

        positive = (
            "(No Democrat)",
            "(no democrat)",
            "(NO DEMOCRAT)",
            "(no Democrat — top-two)",
            "(No Democrat.)",
        )
        negative = (
            "(No Democratic primary)",
            "No Democratic…",
            "No Democrat",
            "(no democrats)",
            "(No DemocratX)",
            "Synthetic Placeholder",
            "quoted no democrat later",
            "",
        )
        for name in positive:
            self.assertTrue(prefix_test(name), name)
            self.assertIsNotNone(NO_DEMOCRAT_RE.match(name), name)
            self.assertEqual(prefix_test(name), NO_DEMOCRAT_RE.match(name) is not None, name)
        for name in negative:
            self.assertFalse(prefix_test(name), name)
            self.assertIsNone(NO_DEMOCRAT_RE.match(name), name)
            self.assertEqual(prefix_test(name), NO_DEMOCRAT_RE.match(name) is not None, name)

        doc, raw, codes, forecast, mapping, book = self._world()
        edits = {
            "AL-02": {"dem_name": "(No Democratic primary)", "same_party_excluded_s5": False},
            "AZ-01": {"dem_name": "No Democratic…", "same_party_excluded_s5": False},
        }
        built = _assemble(
            forecast, mapping, book, doc, raw,
            {"status": "SELECTED"},
            _accepted(codes, forecast, edits),
        )
        for code in edits:
            row = self._row(built, code)
            self.assertNotIn("NO_DEMOCRAT", row["exclusion_reasons"], code)
            self.assertIsNone(row["exclusion_reason"], code)
            self.assertFalse(row["dem_name_flags"]["no_democrat"], code)
        self.assertEqual(q5_orderbook_status(), "UNAVAILABLE_NEEDS_EGRESS")
        self.assertEqual(built["q5_status"], "UNAVAILABLE_NEEDS_EGRESS")
        self.assertIsNone(built["closed_result"])

    def test_same_party_s5_alone_and_a_later_mention(self):
        doc, raw, codes, forecast, mapping, book = self._world()
        edits = {
            "AL-02": {"dem_name": "Synthetic Placeholder", "same_party_excluded_s5": True},
            "AZ-01": {"dem_name": "Alex Quoted no democrat later", "same_party_excluded_s5": False},
        }
        built = _assemble(
            forecast, mapping, book, doc, raw,
            {"status": "SELECTED"},
            _accepted(codes, forecast, edits),
        )
        alone = self._row(built, "AL-02")
        self.assertEqual(alone["exclusion_reason"], "SAME_PARTY_S5")
        self.assertNotIn("NO_DEMOCRAT", alone["exclusion_reasons"])
        later = self._row(built, "AZ-01")
        self.assertIsNone(later["exclusion_reason"])
        self.assertFalse(later["dem_name_flags"]["no_democrat"])

    def test_unresolved_null_unapplyable_and_missing(self):
        doc, raw, codes, forecast, mapping, book = self._world()
        edits = {
            "AL-02": {"dem_name": None, "dem_name_status": "RESOLVED", "same_party_excluded_s5": False},
            "AZ-01": {"dem_name": None, "dem_name_status": "EXCLUSION_UNAPPLYABLE", "same_party_excluded_s5": None},
            "CA-22": {"dem_name": "Synthetic Placeholder", "dem_name_status": "RESOLVED", "same_party_excluded_s5": None},
        }
        built = _assemble(
            forecast, mapping, book, doc, raw,
            {"status": "SELECTED"},
            _accepted(codes, forecast, edits, drop=("CO-04",)),
        )
        self.assertEqual(self._row(built, "AL-02")["exclusion_reason"], "DEM_NAME_UNRESOLVED")
        self.assertEqual(self._row(built, "AZ-01")["exclusion_reason"], "DEM_NAME_UNRESOLVED")
        self.assertEqual(self._row(built, "CA-22")["exclusion_reason"], "DEM_NAME_UNRESOLVED")
        self.assertIsNone(self._row(built, "CA-22")["dem_name_flags"]["same_party_s5"])
        self.assertEqual(self._row(built, "CO-04")["exclusion_reason"], "DEM_NAME_UNRESOLVED")
        self.assertIsNone(self._row(built, "AZ-02")["exclusion_reason"])

    def test_old_forecast_triggers_do_not_exclude(self):
        doc, raw, codes, forecast, mapping, book = self._world()
        forecast = copy.deepcopy(forecast)
        forecast["rows"][0]["same_party"] = True
        forecast["rows"][0]["rep_name"] = "(No Republican)"
        forecast["rows"][0]["dem_name"] = "(No Democrat)"
        built = _assemble(
            forecast, mapping, book, doc, raw,
            {"status": "SELECTED"},
            _accepted(codes, forecast),
        )
        self.assertIsNone(built["rows"][0]["exclusion_reason"])
        self.assertNotIn("same_party_race", json.dumps(built))

    def test_base_sha_mismatch_excludes_admissible_rows(self):
        doc, raw, codes = _codes()
        original = ORIGINAL.read_bytes()
        v1 = V1.read_bytes()
        refused = validate_dem_name_doc(original + b"\n", v1, {"sha256": sha256_bytes(v1)}, codes)
        self.assertEqual(refused["status"], "DEM_NAME_STEP_REFUSED")
        self.assertEqual(refused["reason"], "BASE_SHA_MISMATCH")
        forecast = json.loads(original)
        _doc, _raw, mapping, book = None, None, None, None
        _forecast, mapping, book = full_books(codes)
        forecast_rows = {row["race_code"]: row for row in forecast["rows"]}
        for row in _forecast["rows"]:
            row["dem_prob"] = forecast_rows[row["race_code"]]["dem_prob"]
        _forecast["source_fetched_at_utc"] = forecast["source_fetched_at_utc"]
        built = _assemble(_forecast, mapping, book, doc, raw, {"status": "SELECTED"}, refused)
        self.assertEqual(built["dem_name_step"]["status"], "DEM_NAME_STEP_REFUSED")
        self.assertEqual(built["dem_name_step"]["reason"], "BASE_SHA_MISMATCH")
        self.assertEqual(len(built["rows"]), 92)
        self.assertTrue(all(row["exclusion_reason"] == "DEM_NAME_UNRESOLVED" for row in built["rows"]))
        self.assertNotIn("v1", built["dem_name_step"])
        self.assertEqual(built["closed_result"], "INCONCLUSIVE_DEGENERATE_BLOCK")
        self.assertEqual(built["q5_status"], "UNAVAILABLE_NEEDS_EGRESS")
        scored_rows = copy.deepcopy(built["rows"])
        for row in scored_rows:
            row["y"] = 1
        from card01_amc.score import score_document
        from card01_amc.verdict import apply_verdict
        scored = score_document({"rows": scored_rows})
        self.assertEqual(scored["counts"]["scored"], 0)
        self.assertEqual(scored["headline_status"], "INCONCLUSIVE_DEGENERATE_BLOCK")
        self.assertEqual(scored["degenerate_reason"], "N_ZERO")
        verdict = apply_verdict(scored)
        self.assertEqual(verdict["verdict"], "INCONCLUSIVE_DEGENERATE_BLOCK")
        self.assertEqual(verdict["firing"], [])

    def test_fixture_names_are_not_copied(self):
        doc, raw, codes = _codes()
        forecast = json.loads(ORIGINAL.read_bytes())
        v1 = json.loads(V1.read_bytes())
        _fc, mapping, book = full_books(codes)
        for row in _fc["rows"]:
            row["dem_prob"] = 55.0
        _fc["source_fetched_at_utc"] = forecast["source_fetched_at_utc"]
        step = {
            "status": "DEM_NAME_ACCEPTED",
            "reason": None,
            "expected_script_sha256": ADD_DEM_NAME_SHA256,
            "observed_script_sha256": ADD_DEM_NAME_SHA256,
            "original_sha256": sha256_bytes(ORIGINAL.read_bytes()),
            "v1_sha256": sha256_bytes(V1.read_bytes()),
            "check": {"byte_identical": True},
            "v1": v1,
        }
        built = _assemble(_fc, mapping, book, doc, raw, {"status": "SELECTED"}, step)
        text = dumps(built)
        for row in v1["rows"]:
            self.assertNotIn(row["dem_name"], text)
        self.assertNotIn("dem_name_source", text)
        self.assertNotIn("base_derived", text)
        self.assertNotIn("SYNTHETIC_NOT_A_PATH", text)
        self.assertEqual([row["race_id"] for row in built["rows"]], codes)
        again = _assemble(_fc, mapping, book, doc, raw, {"status": "SELECTED"}, step)
        self.assertEqual(dumps(built), dumps(again))

    def test_q6_linkage(self):
        doc, raw, codes, forecast, mapping, book = self._world()
        step = _accepted(codes, forecast)
        bad = {"status": "SELECTED", "selected_derived_sha256": "ab" * 32}
        blobs = {
            "forecast": json.dumps(forecast).encode(),
            "mapping": json.dumps(mapping).encode(),
            "book": json.dumps(book).encode(),
        }
        shas = {
            "universe": sha256_bytes(raw),
            "forecast": sha256_bytes(blobs["forecast"]),
            "mapping": sha256_bytes(blobs["mapping"]),
            "book": sha256_bytes(blobs["book"]),
            "selection": sha256_bytes(json.dumps(bad).encode()),
        }
        with self.assertRaises(BuilderError):
            build(doc, forecast, mapping, book, shas, selection=bad, dem_name_step=step)
        missing = _assemble(
            None, mapping, book, doc, raw,
            {"status": "FORECAST_FILE_MISSING", "selected_derived_sha256": None},
            None,
        )
        self.assertEqual(missing["q6_status"], "FORECAST_FILE_MISSING")
        self.assertEqual(len(missing["rows"]), 92)
        self.assertTrue(all(row["exclusion_reason"] == "no_admissible_forecast" for row in missing["rows"]))
        with self.assertRaises(BuilderError):
            _assemble(forecast, mapping, book, doc, raw, {"status": "FORECAST_FILE_CORRUPT"}, step)


class DemNameRunnerTests(unittest.TestCase):
    def test_check_failure_does_not_accept(self):
        doc, _raw, codes = _codes()
        script = b"fake-script"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            script_path = root / "add.py"
            script_path.write_bytes(script)
            original = root / "original.json"
            original.write_bytes(ORIGINAL.read_bytes())

            def runner(argv, **kwargs):
                class Proc:
                    returncode = 0
                    stdout = ""
                if "--check" in argv:
                    Proc.returncode = 3
                    Proc.stdout = json.dumps({"byte_identical": False, "out": "x", "sha256": "cd" * 32}) + "\n"
                return Proc()

            result = run_dem_name_step(
                script_path,
                original,
                root,
                runner=runner,
                expected_script_sha256=sha256_bytes(script),
                universe_codes=codes,
            )
        self.assertEqual(result["reason"], "CHECK_FAILED")
        self.assertEqual(result["status"], "DEM_NAME_STEP_REFUSED")

    def test_script_sha_mismatch_does_not_call_runner(self):
        _doc, _raw, codes = _codes()
        calls = []

        def runner(argv, **kwargs):
            calls.append(argv)
            raise AssertionError("runner must not be called")

        with tempfile.TemporaryDirectory() as tmp:
            script_path = Path(tmp) / "add.py"
            script_path.write_bytes(b"different")
            result = run_dem_name_step(
                script_path,
                ORIGINAL,
                tmp,
                runner=runner,
                universe_codes=codes,
            )
        self.assertEqual(result["reason"], "SCRIPT_SHA_MISMATCH")
        self.assertEqual(calls, [])

    def test_positive_fake_runner_accepts_the_fixture(self):
        _doc, _raw, codes = _codes()
        script = b"synthetic-runner-stand-in"
        v1 = V1.read_bytes()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            script_path = root / "add.py"
            script_path.write_bytes(script)
            original = root / "original.json"
            original.write_bytes(ORIGINAL.read_bytes())
            out = root / "original.dem_name_v1.json"

            def runner(argv, **kwargs):
                class Proc:
                    returncode = 0
                    stdout = ""
                if "--check" in argv:
                    Proc.stdout = json.dumps({
                        "derived": "original.json",
                        "out": str(out),
                        "byte_identical": True,
                        "sha256": sha256_bytes(v1),
                    }) + "\n"
                else:
                    out.write_bytes(v1)
                    Proc.stdout = json.dumps({"status": "WROTE"}) + "\n"
                return Proc()

            result = run_dem_name_step(
                script_path,
                original,
                root,
                runner=runner,
                expected_script_sha256=sha256_bytes(script),
                universe_codes=codes,
            )
        self.assertEqual(result["status"], "DEM_NAME_ACCEPTED")
        self.assertNotIn("out", result["check"])
        self.assertTrue(result["check"]["byte_identical"])
        self.assertNotIn("dem_name", json.dumps(result["check"]))

    def test_cli_refuses_a_mismatched_forecast(self):
        doc, raw, codes, forecast, mapping, book = DemNameBuilderTests()._world()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "universe.json").write_bytes(raw)
            (root / "forecast.json").write_bytes(json.dumps(forecast).encode())
            (root / "mapping.json").write_bytes(json.dumps(mapping).encode())
            (root / "book.json").write_bytes(json.dumps(book).encode())
            (root / "selection.json").write_bytes(json.dumps({
                "status": "SELECTED",
                "selected_derived_sha256": "ab" * 32,
            }).encode())
            proc = subprocess.run(
                [
                    sys.executable, "-m", "card01_amc.build_rows",
                    "--universe", str(root / "universe.json"),
                    "--selection", str(root / "selection.json"),
                    "--forecast", str(root / "forecast.json"),
                    "--mapping", str(root / "mapping.json"),
                    "--book", str(root / "book.json"),
                ],
                cwd=LAB,
                capture_output=True,
            )
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(proc.stdout, b"")
        self.assertIn(b"FORECAST_SHA_MISMATCH", proc.stderr)


if __name__ == "__main__":
    unittest.main()
