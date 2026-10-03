import hashlib
import subprocess
import unittest
from pathlib import Path

import support  # noqa: F401
from constants import (
    FILLS_SHA256,
    ORDERS_SHA256,
    PINS_REL,
    QUEUE_POLICIES_SHA256,
    REPLAY_SHA256,
    RUN_EXPERIMENT_SHA256,
    SUMMARY_SHA256,
)
from pins_io import LAB, manifest_map, tree_root


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class T13Untouched(unittest.TestCase):
    def test_000_bytes_match_the_pins_and_the_factorial_tree_is_clean(self):
        repo = LAB.parent
        factorial = repo / "nfl_factorial_lab_20260921"
        self.assertEqual(_sha(factorial / "replay_v2.py"), REPLAY_SHA256)
        self.assertEqual(_sha(factorial / "queue_policies.py"), QUEUE_POLICIES_SHA256)
        self.assertEqual(_sha(factorial / "run_experiment.py"), RUN_EXPERIMENT_SHA256)
        self.assertEqual(_sha(factorial / "results" / "q3300_d0.25_000.json"), SUMMARY_SHA256)
        root = tree_root()
        self.assertEqual(_sha(root / PINS_REL["replay"]), REPLAY_SHA256)
        self.assertEqual(_sha(root / PINS_REL["queue"]), QUEUE_POLICIES_SHA256)
        self.assertEqual(_sha(root / PINS_REL["fills"]), FILLS_SHA256)
        self.assertEqual(_sha(root / PINS_REL["orders"]), ORDERS_SHA256)
        self.assertEqual(_sha(root / PINS_REL["summary"]), SUMMARY_SHA256)
        decisions = factorial / "results" / "q3300_d0.25_000_decisions.jsonl.gz"
        self.assertFalse(decisions.exists())
        self.assertFalse(any(path.endswith("q3300_d0.25_000_decisions.jsonl.gz") for path in manifest_map()))
        diff = subprocess.check_output(
            ["git", "diff", "--", "nfl_factorial_lab_20260921"],
            cwd=repo,
        )
        status = subprocess.check_output(
            ["git", "status", "--porcelain", "--", "nfl_factorial_lab_20260921"],
            cwd=repo,
        )
        self.assertEqual(diff, b"")
        self.assertEqual(status, b"")


if __name__ == "__main__":
    unittest.main()
