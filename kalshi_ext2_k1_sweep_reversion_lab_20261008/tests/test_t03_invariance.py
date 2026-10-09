import copy
import unittest

import support
from ext2k1.canonical import canonical_sha256
from ext2k1.quotes import classify_sweeps
from ext2k1.sweeps import build


class T03Invariance(unittest.TestCase):
    def test_quote_and_b2_permutations_leave_sweeps_fixed(self):
        import random

        tape = support.FIXTURES["tape"]
        rows = tape["rows"]
        markets = tape["markets"]
        base = build(rows, markets)
        base_sha = canonical_sha256(base)
        base_rv = canonical_sha256([record["RV"] for record in classify_sweeps(base["sweeps"], rows)])
        rng = random.Random(20261008)
        b2 = tape["b2_fills"]
        for _ in range(20):
            mutated = copy.deepcopy(rows)
            quotes = [row for row in mutated if row.get("kind") == "quote"]
            for field in ("bid", "ask", "asof"):
                values = [row[field] for row in quotes]
                rng.shuffle(values)
                for row, value in zip(quotes, values):
                    row[field] = value
            fills = copy.deepcopy(b2)
            if fills:
                keys = sorted({key for row in fills for key in row})
                for key in keys:
                    values = [row.get(key) for row in fills]
                    rng.shuffle(values)
                    for row, value in zip(fills, values):
                        row[key] = value
            document = build(mutated, markets)
            self.assertEqual(canonical_sha256(document), base_sha)
            self.assertEqual(document, base)
            changed = canonical_sha256(
                [record["RV"] for record in classify_sweeps(document["sweeps"], mutated)]
            )
            self.assertNotEqual(changed, base_rv)


if __name__ == "__main__":
    unittest.main()
