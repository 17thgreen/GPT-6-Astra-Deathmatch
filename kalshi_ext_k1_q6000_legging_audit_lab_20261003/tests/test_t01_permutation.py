import json
import random
import unittest

import support  # noqa: F401
from artifacts import constancy_sha, four_shas
from canonical import write_json
from orchestrator import RESULTS, _common_header, games_for_artifacts, invariance_blobs, measure
from tools.probe_invariance import (
    CONSTANCY_SHA256,
    MONEYLINE_COLUMNS,
    PROBE_SEED,
    PROBE_SHUFFLES,
    RECORDED_ARTIFACT_SHAS,
    SCORE_COLUMNS,
    games_csv_text,
    moneyline_control_order,
    permute_csv_columns,
    rebuild_blobs,
    run_score_probe,
    score_permutation_orders,
)


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


def _label_snapshot(measurement):
    return [
        (portion["portion_id"], portion["s_dev"], portion["dev_proportional"])
        for portion in measurement["lots"]["portions"]
    ]


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
        assignments = json.loads(left["gate_assignments"])
        tokens = [token for cells in assignments.values() for token in cells.values()]
        self.assertIn("REFUSE", tokens)
        self.assertIn("KEEP", tokens)
        self.assertIn("REFUSE", assignments["a"].values())
        self.assertIn("KEEP", assignments["b"].values())
        for name in ("gate_assignments", "splits", "uch", "markouts_h"):
            self.assertEqual(left[name], right[name])
        self.assertNotEqual(left["settle"], right["settle"])

    def test_end_to_end_score_csv_rebuild(self):
        """Permute score columns in the csv and rebuild join, consensus, gate and markouts.

        random.Random(7), 25 shuffles, plus the shift-1 derangement. The four
        invariance artifact shas stay on the recorded constancy sha. This is
        the end-to-end coverage. T01(b) below does not rebuild those steps.
        """
        measurement = measure(write=True)
        before = _label_snapshot(measurement)
        csv_text = games_csv_text()
        self.assertEqual(len(score_permutation_orders()), 26)
        baseline, rebuilt = run_score_probe(measurement, csv_text)
        self.assertEqual(four_shas(baseline), RECORDED_ARTIFACT_SHAS)
        self.assertEqual(constancy_sha(baseline), CONSTANCY_SHA256)
        cached = invariance_blobs(measurement, games_for_artifacts(measurement))
        self.assertEqual(four_shas(baseline), four_shas(cached))
        shift = rebuilt[-1]
        self.assertNotEqual(shift["settle"], baseline["settle"])
        for blobs in rebuilt:
            self.assertEqual(four_shas(blobs), RECORDED_ARTIFACT_SHAS)
            self.assertEqual(constancy_sha(blobs), CONSTANCY_SHA256)
        self.assertEqual(_label_snapshot(measurement), before)

    def test_moneyline_permutation_changes_artifacts(self):
        measurement = measure(write=True)
        before = _label_snapshot(measurement)
        csv_text = games_csv_text()
        permuted = permute_csv_columns(csv_text, MONEYLINE_COLUMNS, moneyline_control_order())
        self.assertNotEqual(permuted, csv_text)
        blobs = rebuild_blobs(measurement, permuted)
        self.assertNotEqual(four_shas(blobs), RECORDED_ARTIFACT_SHAS)
        self.assertNotEqual(constancy_sha(blobs), CONSTANCY_SHA256)
        self.assertEqual(_label_snapshot(measurement), before)

    def test_pinned_label_permutation_constancy(self):
        """T01(b). Cached portions only. This covers settle_artifact.

        The 1,000 Random(20261003) shuffles and the shift-1 derangement edit
        scores on the games dict passed into artifact_bytes. Join, consensus,
        the refusal gate and horizon markouts are not rebuilt, so the four
        constancy artifacts do not read those permuted scores. End-to-end
        rebuild coverage is test_end_to_end_score_csv_rebuild.
        """
        measurement = measure(write=True)
        games = games_for_artifacts(measurement)
        base_pairs = _pairs(games)
        base_blobs = invariance_blobs(measurement, games)
        base_four = four_shas(base_blobs)
        constancy = constancy_sha(base_blobs)
        self.assertEqual(base_four, RECORDED_ARTIFACT_SHAS)
        self.assertEqual(constancy, CONSTANCY_SHA256)
        rng = random.Random(20261003)
        for _ in range(1000):
            pairs = list(base_pairs)
            rng.shuffle(pairs)
            blobs = invariance_blobs(measurement, _permute(games, pairs))
            # Cached path: the four artifacts ignore the permuted scores.
            self.assertEqual(four_shas(blobs), base_four)
        shifted = base_pairs[1:] + base_pairs[:1]
        shifted_blobs = invariance_blobs(measurement, _permute(games, shifted))
        self.assertEqual(four_shas(shifted_blobs), base_four)
        self.assertNotEqual(shifted_blobs["settle"], base_blobs["settle"])
        header = _common_header()
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
            "DEV_GRADE_REUSED_31_GAME_COHORT": header["DEV_GRADE_REUSED_31_GAME_COHORT"],
            "HYPOTHETICAL_REPLAY_FILLS": header["HYPOTHETICAL_REPLAY_FILLS"],
            "IN_SAMPLE_DEV": header["IN_SAMPLE_DEV"],
        }
        from report import stamp_ex_post
        stamped = stamp_ex_post(record)
        # Label the cached 1000-shuffle fields. They are not the end-to-end rebuild.
        stamped["cached_test_scope"] = "settle_artifact_only_cached_portions"
        stamped["end_to_end_rebuild"] = {
            "seed": PROBE_SEED,
            "shuffles": PROBE_SHUFFLES,
            "derangement": "shift-1",
            "rebuilds": ["join", "consensus", "gate", "markouts"],
            "moneyline_positive_control": True,
            "constancy_sha256": constancy,
        }
        write_json(RESULTS / "INVARIANCE.json", stamped)
        written = __import__("json").loads((RESULTS / "INVARIANCE.json").read_text(encoding="utf-8"))
        self.assertEqual(written["permutations"], 1000)
        self.assertEqual(written["seed"], 20261003)
        self.assertEqual(written["derangement"], "shift-1")
        self.assertEqual(written["cached_test_scope"], "settle_artifact_only_cached_portions")
        self.assertEqual(written["end_to_end_rebuild"]["constancy_sha256"], CONSTANCY_SHA256)
        self.assertEqual(written["constancy_sha256"], CONSTANCY_SHA256)
        for flag in ("DEV_GRADE_REUSED_31_GAME_COHORT", "HYPOTHETICAL_REPLAY_FILLS", "IN_SAMPLE_DEV"):
            self.assertIs(written[flag], True)
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
