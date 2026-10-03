import hashlib
import json
import unittest
from pathlib import Path

import support  # noqa: F401
from consensus import join_cohort
from constants import PINS_REL
from orchestrator import measure
from pins_io import verified_bytes

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "CONSENSUS_FIXTURE.json"
FIXTURE_SHA256 = "9996b19888bf49cffdd9a35d1cc05d45f7bb28c77af06d9f85d977babfac3c38"


class T11Devig(unittest.TestCase):
    def test_published_examples_and_fixture_reproduction(self):
        measurement = measure(write=True)
        rows = {row["game_id"]: row for row in measurement["joined"]["rows"]}
        self.assertAlmostEqual(rows["2026_01_NE_SEA"]["p_home_prop"], 0.599639, delta=1e-6)
        self.assertAlmostEqual(rows["2026_01_NE_SEA"]["p_home_shin"], 0.603697, delta=1e-6)
        self.assertAlmostEqual(rows["2026_01_BUF_HOU"]["p_home_prop"], 0.495670, delta=1e-6)
        self.assertAlmostEqual(rows["2026_02_MIA_SF"]["p_home_prop"], 0.863014, delta=1e-6)
        self.assertEqual(len(rows), 31)
        for row in rows.values():
            self.assertFalse(row["unclassified"])
            self.assertNotEqual(row["p_home_prop"], 0.5)
            self.assertEqual((row["p_home_prop"] > 0.5), (row["p_home_shin"] > 0.5))
            self.assertAlmostEqual(row["p_away_shin"] + row["p_home_shin"], 1.0, delta=1e-9)
            self.assertAlmostEqual(row["overround"], row["q_away"] + row["q_home"], delta=1e-12)
        again = join_cohort(
            measurement["markets"],
            measurement["weeks"],
            verified_bytes(PINS_REL["games"]).decode("utf-8"),
        )
        raw = FIXTURE.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), FIXTURE_SHA256)
        frozen = json.loads(raw.decode("utf-8"))
        by_id = {row["game_id"]: row for row in frozen}
        self.assertEqual(len(by_id), 31)
        for left, right in zip(measurement["joined"]["rows"], again["rows"]):
            self.assertAlmostEqual(left["p_home_prop"], right["p_home_prop"], delta=1e-6)
            self.assertAlmostEqual(left["p_home_shin"], right["p_home_shin"], delta=1e-6)
            self.assertAlmostEqual(left["overround"], right["overround"], delta=1e-6)
            stored = by_id[left["game_id"]]
            self.assertAlmostEqual(stored["p_home_prop"], left["p_home_prop"], delta=1e-6)
            self.assertAlmostEqual(stored["p_home_shin"], left["p_home_shin"], delta=1e-6)
            # Frozen fixture overround is q_away + q_home - 1. This lab stores q_away + q_home.
            self.assertAlmostEqual(stored["overround"], left["overround"] - 1.0, delta=1e-6)


if __name__ == "__main__":
    unittest.main()
