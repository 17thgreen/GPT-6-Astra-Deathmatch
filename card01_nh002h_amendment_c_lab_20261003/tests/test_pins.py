"""Pinned-sha checks. The two full self-test reproductions live in test_selftest.py."""
from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.support import BASE, INPUT_SHA, LAB, OUTPUT_SHA, PIN_SHA, REPO, UNIVERSE_SHA, sha256_bytes


class PinTests(unittest.TestCase):
    def test_vendored_script_and_fixtures(self):
        pins = LAB / "pins"
        self.assertEqual(sha256_bytes((pins / "NH002H_AMENDMENT_B_national_miss.py").read_bytes()), PIN_SHA)
        self.assertEqual(sha256_bytes((pins / "SELFTEST_SYNTHETIC_input.json").read_bytes()), INPUT_SHA)
        self.assertEqual(sha256_bytes((pins / "SELFTEST_SYNTHETIC_output.json").read_bytes()), OUTPUT_SHA)
        self.assertEqual(sha256_bytes((pins / "UNIVERSE_2026_HOUSE_FROZEN.json").read_bytes()), UNIVERSE_SHA)

    def test_pins_json_matches_bytes(self):
        doc = json.loads((LAB / "PINS.json").read_text())
        self.assertNotIn("sha256", {k for k in doc if k == "self"})
        seen = set()
        for entry in doc["pins"]:
            path = LAB / entry["path"]
            seen.add(entry["path"])
            if entry["vendored"] is False:
                self.assertFalse(path.exists(), entry["path"])
                continue
            self.assertEqual(sha256_bytes(path.read_bytes()), entry["sha256"], entry["path"])
        for py in (LAB / "card01_amc").glob("*.py"):
            rel = "card01_amc/" + py.name
            self.assertIn(rel, seen)

    def test_pinload_refuses_modified_bytes(self):
        from card01_amc.pinload import PIN_SHA256, PinMismatch, load_national_miss

        src = (LAB / "pins" / "NH002H_AMENDMENT_B_national_miss.py").read_bytes()
        self.assertEqual(hashlib.sha256(src).hexdigest(), PIN_SHA256)
        flipped = src[:-1] + bytes([src[-1] ^ 0x01])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "NH002H_AMENDMENT_B_national_miss.py"
            path.write_bytes(flipped)
            with self.assertRaises(PinMismatch):
                load_national_miss(path)

    def test_governance_diff_empty(self):
        try:
            proc = subprocess.run(
                ["git", "diff", "--name-only", BASE, "--", "lab/governance"],
                cwd=REPO,
                capture_output=True,
                text=True,
                check=False,
            )
        except OSError:
            self.skipTest("git unavailable")
        if proc.returncode != 0 and "not a git repository" in proc.stderr:
            self.skipTest("git unavailable")
        self.assertEqual(proc.stdout.strip(), "")

    def test_pinned_script_diff_is_only_the_vendored_copy(self):
        proc = subprocess.run(
            ["git", "diff", "--name-only", BASE, "--", "*NH002H_AMENDMENT_B_national_miss.py"],
            cwd=REPO,
            capture_output=True,
            text=True,
            check=False,
        )
        names = [line for line in proc.stdout.splitlines() if line]
        self.assertEqual(
            names,
            ["card01_nh002h_amendment_c_lab_20261003/pins/NH002H_AMENDMENT_B_national_miss.py"],
        )
        got = sha256_bytes((LAB / "pins" / "NH002H_AMENDMENT_B_national_miss.py").read_bytes())
        self.assertEqual(got, PIN_SHA)


if __name__ == "__main__":
    unittest.main()
