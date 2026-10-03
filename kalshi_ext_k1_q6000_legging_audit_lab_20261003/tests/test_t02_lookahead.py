import random
import unittest

import support  # noqa: F401
from errors import LookaheadRefused
from gate import gate_from_context, gate_on_fill
from orchestrator import measure


class T02Lookahead(unittest.TestCase):
    def test_signature_rejects_tape_score_and_markout(self):
        fill = {"at": 1.0, "outcome_mid_at_fill": 0.5, "inventory_after": 10}
        for kwargs in ({"tape": []}, {"score": 1}, {"markout": 0.1}):
            with self.assertRaises(LookaheadRefused):
                gate_on_fill(fill, p_cons=0.4, x=0.02, exposure_floor=0, **kwargs)

    def test_two_hundred_truncated_fills_are_unchanged(self):
        measurement = measure(write=True)
        fills = measurement["fills"]
        ats = measurement["tape_ats"]
        self.assertEqual(ats, sorted(ats))
        by_portion = {portion["row_index"]: portion for portion in measurement["lots"]["portions"]}
        rng = random.Random(20261003)
        for index in rng.sample(range(len(fills)), 200):
            fill = fills[index]
            portion = by_portion.get(index)
            p_cons = portion["p_cons_proportional"] if portion else None
            full = gate_on_fill(fill, p_cons=p_cons, x=0.02, exposure_floor=0.0)
            truncated = gate_from_context(
                fill, ats, fills, p_cons=p_cons, x=0.02, exposure_floor=0.0,
            )
            self.assertEqual(full, truncated)


if __name__ == "__main__":
    unittest.main()
