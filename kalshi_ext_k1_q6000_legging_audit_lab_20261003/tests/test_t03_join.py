import unittest

import support  # noqa: F401
from consensus import join_cohort
from constants import PINNED_GAME_IDS
from errors import JoinRefused
from orchestrator import measure
from pins_io import verified_bytes
from constants import PINS_REL


class T03Join(unittest.TestCase):
    def test_join_31_of_31_and_alias_map(self):
        measurement = measure(write=True)
        joined = measurement["joined"]
        self.assertEqual(joined["game_ids"], PINNED_GAME_IDS)
        self.assertEqual(len(set(joined["game_ids"])), 31)
        self.assertEqual(joined["exact_without_alias"], 28)
        self.assertEqual(
            joined["alias_events"],
            {
                "KXNFLGAME-26SEP10SFLAR": ["LAR"],
                "KXNFLGAME-26SEP13CLEJAC": ["JAC"],
                "KXNFLGAME-26SEP20JACDEN": ["JAC"],
            },
        )

    def test_removed_alias_duplicate_row_and_time_mismatch_refuse(self):
        measurement = measure(write=True)
        csv_text = verified_bytes(PINS_REL["games"]).decode("utf-8")
        with self.assertRaises(JoinRefused):
            join_cohort(measurement["markets"], measurement["weeks"], csv_text, alias_map={})
        lines = csv_text.splitlines()
        header, body = lines[0], lines[1:]
        duplicate = None
        for line in body:
            if line.startswith("2026_01_NE_SEA,"):
                duplicate = line
                break
        self.assertIsNotNone(duplicate)
        with self.assertRaises(JoinRefused):
            join_cohort(
                measurement["markets"],
                measurement["weeks"],
                "\n".join([header, duplicate, *body]),
            )
        mismatched = csv_text.replace("2026-09-09,Wednesday,20:20,NE,", "2026-09-09,Wednesday,20:21,NE,", 1)
        self.assertNotEqual(mismatched, csv_text)
        with self.assertRaises(JoinRefused):
            join_cohort(measurement["markets"], measurement["weeks"], mismatched)


if __name__ == "__main__":
    unittest.main()
