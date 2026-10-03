import json
import unittest

import support  # noqa: F401
from constants import EX_POST_SENTENCE
from orchestrator import RESULTS, measure

DERIVED = {
    "p_home_prop",
    "p_home_shin",
    "p_cons_proportional",
    "overround",
    "s_dev",
    "s_fav",
    "delta_star_gross",
    "dev_proportional",
    "by_s_dev",
    "contrast",
}


R33_FLAGS = (
    "DEV_GRADE_REUSED_31_GAME_COHORT",
    "HYPOTHETICAL_REPLAY_FILLS",
    "IN_SAMPLE_DEV",
)


class T14Tags(unittest.TestCase):
    def test_consensus_objects_carry_the_ex_post_sentence(self):
        measure(write=True)
        saw_derived = False
        names = []
        for path in sorted(RESULTS.glob("*.json")):
            names.append(path.name)
            payload = json.loads(path.read_text(encoding="utf-8"))
            for flag in R33_FLAGS:
                self.assertIs(payload.get(flag), True, path.name)
            if path.name == "INVARIANCE.json":
                self._assert_invariance_labels(payload)
            saw_derived = self._walk(payload, path.name) or saw_derived
        self.assertIn("INVARIANCE.json", names)
        self.assertTrue(saw_derived)

    def _assert_invariance_labels(self, payload):
        self.assertEqual(payload["permutations"], 1000)
        self.assertEqual(payload["seed"], 20261003)
        self.assertEqual(payload["derangement"], "shift-1")
        self.assertEqual(payload["cached_test_scope"], "settle_artifact_only_cached_portions")
        rebuild = payload["end_to_end_rebuild"]
        self.assertEqual(rebuild["seed"], 7)
        self.assertEqual(rebuild["shuffles"], 25)
        self.assertEqual(rebuild["derangement"], "shift-1")
        self.assertEqual(rebuild["rebuilds"], ["join", "consensus", "gate", "markouts"])
        self.assertIs(rebuild["moneyline_positive_control"], True)
        self.assertEqual(rebuild["constancy_sha256"], payload["constancy_sha256"])
        self.assertTrue(payload["constancy_sha256"].startswith("a73a90e0"))

    def _walk(self, obj, name):
        saw = False
        if isinstance(obj, dict):
            if DERIVED.intersection(obj):
                saw = True
                self.assertIs(obj.get("EX_POST_ANCHOR_U"), True, name)
                self.assertEqual(obj.get("ex_post_sentence"), EX_POST_SENTENCE, name)
            for value in obj.values():
                saw = self._walk(value, name) or saw
        elif isinstance(obj, list):
            for value in obj:
                saw = self._walk(value, name) or saw
        return saw


if __name__ == "__main__":
    unittest.main()
