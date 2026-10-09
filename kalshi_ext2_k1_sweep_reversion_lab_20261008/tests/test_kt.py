import argparse
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

import support
from ext2k1.canonical import canonical_bytes, canonical_sha256
from ext2k1.constants import REPORTING_DEFECT
from ext2k1.pins_io import sweeps_module_sha256
from ext2k1.report import build_results, published_results
from ext2k1.verdict import evaluate
from ext2k1.__main__ import build_parser

_METRIC = (
    "per_sweep",
    "primary",
    "cells",
    "impact_profile",
    "loo",
    "placebo",
    "b2_join",
)


def _fresh():
    tape = support.FIXTURES["tape"]
    _receipt, _document, body = build_results(
        tape["rows"],
        tape["markets"],
        tape["week_membership"],
        support.synthetic_pins(),
        builder_sha256=support.BUILDER_SHA256,
        source_pins=support.SOURCE_PINS,
        sweeps_module_sha256=sweeps_module_sha256(),
        b2_rows=tape["b2_fills"],
    )
    return canonical_bytes(published_results(body)), published_results(body)["output_sha256"]


class KT1Blocks(unittest.TestCase):
    def test_expected_blocks(self):
        _receipt, _document, body = support.full_run()
        published = published_results(body)
        expected = support.EXPECTED
        self.assertTrue(support.near(body["per_sweep"], expected["per_sweep"]))
        for key in ("primary", "cells", "impact_profile", "loo", "placebo", "b2_join"):
            self.assertTrue(support.near(published[key], expected[key]), key)
        self.assertEqual(published["sweeps_sha256"], expected["sweeps_sha256"])
        self.assertEqual(published["IDX_sha256"], expected["IDX_sha256"])
        self.assertEqual(published["verdict_table_evaluation"]["verdict"], expected["verdict"])
        self.assertEqual(published["verdict_table_evaluation"]["rule"], expected["verdict_rule"])
        self.assertEqual(published["primary"]["YES"]["kept"], expected["primary"]["YES"]["kept"])
        self.assertEqual(published["primary"]["NO"]["dropped"], expected["primary"]["NO"]["dropped"])
        for key in _METRIC:
            self.assertIn(key, body if key == "per_sweep" else published)


class KT2Defect(unittest.TestCase):
    def test_one_nonblocking_defect(self):
        receipt, _document, body = support.full_run()
        published = published_results(body)
        self.assertEqual(receipt["reporting_defects"], [REPORTING_DEFECT])
        self.assertEqual(published["reporting_defects"], [REPORTING_DEFECT])
        self.assertIs(published["reporting_defects"][0]["blocking"], False)
        removed = dict(published)
        removed.pop("reporting_defects")
        self.assertNotIn("reporting_defects", removed)
        held = evaluate(
            published["primary"]["YES"],
            published["primary"]["NO"],
            count_pass=True,
            structure_pass=True,
        )
        self.assertEqual(held["verdict"], published["verdict_table_evaluation"]["verdict"])
        self.assertEqual(held["rule"], published["verdict_table_evaluation"]["rule"])


class KT3PublicSafety(unittest.TestCase):
    def test_forbidden_substrings(self):
        always = (
            "/" + "workspace",
            "/" + "home",
            "evidence" + "_private",
            "astra" + "-capture",
            "scr" + "atch",
            "." + "cursor",
            "agent" + "-tools",
        )
        limited = (
            "be" + "cker",
            "capture" + ".sqlite",
            "*." + "parquet",
        )
        allowed = {
            "ext2k1/refusals.py",
            "tests/test_t08_refusals.py",
        }
        roots = [support.LAB]
        registry = support.LAB.parent / "docs" / "EXPERIMENT_REGISTRY.md"
        paths = []
        for root in roots:
            for path in root.rglob("*"):
                if not path.is_file():
                    continue
                if "__pycache__" in path.parts or path.suffix == ".pyc":
                    continue
                paths.append(path)
        paths.append(registry)
        for path in paths:
            text = path.read_text(encoding="utf-8")
            if path == registry:
                rel = "docs/EXPERIMENT_REGISTRY.md"
            else:
                rel = path.relative_to(support.LAB).as_posix()
            class_name = "Be" + "ckerRefused"
            scanned = text if rel in allowed else text.replace(class_name, "")
            folded = scanned.lower()
            for token in always:
                self.assertNotIn(token.lower(), folded, rel)
            if rel not in allowed:
                for token in limited:
                    self.assertNotIn(token.lower(), folded, "%s contains %s" % (rel, token))


class KT4Cli(unittest.TestCase):
    def test_option_surface(self):
        parser = build_parser()
        found = set()

        def collect(item):
            for action in item._actions:
                found.update(action.option_strings)
                if isinstance(action, argparse._SubParsersAction):
                    for sub in action.choices.values():
                        collect(sub)

        collect(parser)
        self.assertEqual(found, {"-h", "--help", "--out-dir", "--receipt", "--receipt-sha256"})

    def test_repo_out_dir_and_wrong_receipt_sha(self):
        lab = support.LAB
        receipt = subprocess.run(
            [sys.executable, "-m", "ext2k1", "receipt", "--out-dir", str(lab)],
            cwd=str(lab),
            capture_output=True,
            text=True,
            timeout=60,
        )
        self.assertEqual(receipt.returncode, 2)
        self.assertIn("OUTPUT_PATH_IN_REPO", receipt.stderr)
        self.assertFalse((lab / "RECEIPT.json").exists())
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            payload = root / "RECEIPT.json"
            payload.write_text("{}", encoding="utf-8")
            score = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "ext2k1",
                    "score",
                    "--receipt",
                    str(payload),
                    "--receipt-sha256",
                    "ab" * 32,
                    "--out-dir",
                    str(root),
                ],
                cwd=str(lab),
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(score.returncode, 2)
            self.assertIn("RECEIPT_NOT_VERIFIED", score.stderr)
            self.assertFalse((root / "RESULTS.json").exists())


class KT5Determinism(unittest.TestCase):
    def test_in_process_and_hashseed(self):
        first, sha_a = _fresh()
        second, sha_b = _fresh()
        self.assertEqual(first, second)
        self.assertEqual(sha_a, sha_b)
        script = textwrap.dedent(
            """
            import json
            import sys
            from pathlib import Path

            lab = Path(sys.argv[1])
            sys.path.insert(0, str(lab))
            from ext2k1.constants import BUILDER_SHA256, Pins
            from ext2k1.pins_io import sweeps_module_sha256
            from ext2k1.report import build_results, published_results
            from ext2k1.canonical import canonical_bytes

            fixtures = json.loads((lab / "tests" / "fixtures" / "SYNTH_EXT2K1_FIXTURES.json").read_text())
            expected = json.loads((lab / "tests" / "fixtures" / "SYNTH_EXT2K1_EXPECTED.json").read_text())
            counts = dict(expected["structural_counts_synth"])
            counts["events"] = len(expected["EVENTS"])
            tape = fixtures["tape"]
            source_pins = [
                {
                    "role": "synthetic tape fixture",
                    "path": "tests/fixtures/SYNTH_EXT2K1_FIXTURES.json",
                    "bytes": 521486,
                    "sha256": "4f6791ee4cce5baa3f67acb29c563c0823b36f6ecea420a03cabe95e8efca430",
                }
            ]
            body = build_results(
                tape["rows"],
                tape["markets"],
                tape["week_membership"],
                Pins(counts, BUILDER_SHA256),
                builder_sha256=BUILDER_SHA256,
                source_pins=source_pins,
                sweeps_module_sha256=sweeps_module_sha256(),
                b2_rows=tape["b2_fills"],
            )[2]
            Path(sys.argv[2]).write_bytes(canonical_bytes(published_results(body)))
            """
        ).strip()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            worker = root / "worker.py"
            worker.write_text(script, encoding="utf-8")
            outs = []
            for seed in ("0", "1"):
                target = root / ("out-%s.json" % seed)
                env = os.environ.copy()
                env["PYTHONHASHSEED"] = seed
                proc = subprocess.run(
                    [sys.executable, str(worker), str(support.LAB), str(target)],
                    cwd=str(support.LAB),
                    capture_output=True,
                    text=True,
                    timeout=180,
                    env=env,
                )
                self.assertEqual(proc.returncode, 0, proc.stderr)
                outs.append(target.read_bytes())
        self.assertEqual(outs[0], outs[1])
        self.assertEqual(outs[0], first)
        parsed = json_loads_bytes(first)
        self.assertEqual(parsed["output_sha256"], sha_a)
        without = {key: value for key, value in parsed.items() if key != "output_sha256"}
        self.assertEqual(canonical_sha256(without), sha_a)
        print("KT5_output_sha256 " + sha_a)


def json_loads_bytes(payload):
    import json

    return json.loads(payload.decode("utf-8"))


if __name__ == "__main__":
    unittest.main()
