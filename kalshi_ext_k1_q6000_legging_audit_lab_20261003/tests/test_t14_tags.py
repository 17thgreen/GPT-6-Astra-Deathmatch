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


class T14Tags(unittest.TestCase):
    def test_consensus_objects_carry_the_ex_post_sentence(self):
        measure(write=True)
        saw_derived = False
        for path in sorted(RESULTS.glob("*.json")):
            payload = json.loads(path.read_text(encoding="utf-8"))
            saw_derived = self._walk(payload, path.name) or saw_derived
        self.assertTrue(saw_derived)

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
