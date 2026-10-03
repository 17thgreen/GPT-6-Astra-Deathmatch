import random
import unittest

import support  # noqa: F401
from artifacts import constancy_sha, four_shas
from canonical import write_json
from orchestrator import RESULTS, games_for_artifacts, invariance_blobs, measure


def _permute(games, pairs):
    events = sorted(games)
    out = {}
    for event, (away, home) in zip(events, pairs):
        row = dict(games[event])
        row["away_score"] = away
        row["home_score"] = home
        out[event] = row
    return out


def _pairs(games):
    return [(games[event]["away_score"], games[event]["home_score"]) for event in sorted(games)]


class T01LabelPermutation(unittest.TestCase):
    def test_fixture_swap_keeps_gate_and_changes_settlement(self):
        from artifacts import artifact_bytes

        portions = [
            _portion("a", "g1", dev=-0.10, inventory=10, entry=0.4, team="H"),
            _portion("b", "g2", dev=0.10, inventory=10, entry=0.4, team="H"),
        ]
        base = {
            "g1": {"away_team": "A", "home_team": "H", "away_score": "0", "home_score": "10"},
            "g2": {"away_team": "A", "home_team": "H", "away_score": "10", "home_score": "0"},
        }
        swapped_scores = {
            "g1": dict(base["g1"], away_score="10", home_score="0"),
            "g2": dict(base["g2"], away_score="0", home_score="10"),
        }
        left = artifact_bytes(portions, base)
        right = artifact_bytes(portions, swapped_scores)
        self.assertGreaterEqual(sum(token == "REFUSE" for token in left and []), 0)
        assignments = __import__("json").loads(left["gate_assignments"])
        self.assertIn("REFUSE", assignments["a"].values())
        self.assertIn("KEEP", assignments["b"].values())
        for name in ("gate_assignments", "splits", "uch", "markouts_h"):
            self.assertEqual(left[name], right[name])
        self.assertNotEqual(left["settle"], right["settle"])

    def test_pinned_label_permutation_constancy(self):
        measurement = measure(write=True)
        games = games_for_artifacts(measurement)
        base_pairs = _pairs(games)
        base_blobs = invariance_blobs(measurement, games)
        base_four = four_shas(base_blobs)
        constancy = constancy_sha(base_blobs)
        rng = random.Random(20261003)
        for _ in range(1000):
            pairs = list(base_pairs)
            rng.shuffle(pairs)
            blobs = invariance_blobs(measurement, _permute(games, pairs))
            self.assertEqual(four_shas(blobs), base_four)
        shifted = base_pairs[1:] + base_pairs[:1]
        shifted_blobs = invariance_blobs(measurement, _permute(games, shifted))
        self.assertEqual(four_shas(shifted_blobs), base_four)
        self.assertNotEqual(shifted_blobs["settle"], base_blobs["settle"])
        record = {
            "gate_assignments_sha256": base_four["gate_assignments"],
            "splits_sha256": base_four["splits"],
            "uch_sha256": base_four["uch"],
            "markouts_h_sha256": base_four["markouts_h"],
            "constancy_sha256": constancy,
            "permutations": 1000,
            "derangement": "shift-1",
            "seed": 20261003,
            "constancy_definition": "sha256 of name-prefixed canonical bytes of gate_assignments, splits, uch, markouts_h",
            "counts_toward_keep": False,
            "results": None,
            "pnl": None,
            "roi": None,
            "verdict": measurement["verdict"],
        }
        from report import stamp_ex_post
        write_json(RESULTS / "INVARIANCE.json", stamp_ex_post(record))
        print(base_four["gate_assignments"])
        print(base_four["splits"])
        print(base_four["uch"])
        print(base_four["markouts_h"])
        print(constancy)


def _portion(portion_id, event, dev, inventory, entry, team):
    return {
        "portion_id": portion_id,
        "event": event,
        "team_long": team,
        "p_entry": entry,
        "inventory_after": inventory,
        "dev_proportional": dev,
        "dev_shin": dev,
        "s_dev": "AGAINST" if dev < -0.005 else "ON",
        "s_fav": "ON",
        "uch": 1.25,
        "markouts": {
            "60": {"gross": 0.01, "net": 0.0},
            "300": {"gross": 0.02, "net": 0.01},
            "1800": {"gross": 0.03, "net": 0.02},
            "3600": {"gross": None, "net": None},
            "CLOSE": {"gross": 0.04, "net": 0.03},
            "SETTLE": {"gross": 0.5, "net": 0.49},
        },
    }


if __name__ == "__main__":
    unittest.main()
