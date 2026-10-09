import copy
import unittest

import support
from ext2k1.verdict import evaluate


class T07Verdict(unittest.TestCase):
    def test_table_cases(self):
        cases = support.FIXTURES["t07_verdict_cases"]
        self.assertEqual(len(cases), 17)
        for case in cases:
            got = evaluate(
                case["YES"],
                case["NO"],
                count_pass=not case["v1_fail"],
                structure_pass=not case["v1s_fail"],
            )
            self.assertEqual(got["verdict"], case["expect_verdict"], case["id"])
            self.assertEqual(got["rule"], case["expect_rule"], case["id"])
            self.assertEqual(got["owner"], "Examiner")
            self.assertEqual(got["status"], "RUNNER_EVALUATION_NOT_A_SCORE")

    def test_synthetic_tape_kills_on_primary_only(self):
        published = support.published()
        self.assertEqual(published["verdict_table_evaluation"]["verdict"], "KILL_EXT2K1")
        self.assertEqual(published["verdict_table_evaluation"]["rule"], "V3")
        self.assertTrue(support.near(published["primary"], support.EXPECTED["primary"]))
        again = evaluate(
            published["primary"]["YES"],
            published["primary"]["NO"],
            count_pass=True,
            structure_pass=True,
        )
        self.assertEqual(again, published["verdict_table_evaluation"])
        mutated = copy.deepcopy(published)
        mutated["cells"]["YES"]["ENTRY_MID_BAND"]["point"] = -1.0
        mutated["cells"]["YES"]["ENTRY_MID_BAND"]["L"] = -1.0
        mutated["cells"]["NO"]["S5K"] = {"point": 5.0, "L": 4.0, "U": 6.0}
        mutated["placebo"] = {"D_obs": 99.0}
        mutated["loo"] = {"label": "CHANGED"}
        mutated["impact_profile"] = {"YES": {"E+900": None}, "NO": {}}
        self.assertEqual(mutated["verdict_table_evaluation"]["verdict"], "KILL_EXT2K1")
        del mutated["cells"]["YES"]["ENTRY_MID_BAND"]
        del mutated["placebo"]
        del mutated["loo"]
        del mutated["impact_profile"]
        held = evaluate(
            mutated["primary"]["YES"],
            mutated["primary"]["NO"],
            count_pass=True,
            structure_pass=True,
        )
        self.assertEqual(held["verdict"], "KILL_EXT2K1")
        self.assertEqual(held["rule"], "V3")


if __name__ == "__main__":
    unittest.main()
