import time
import unittest

import support
from ext2k1.bootstrap import make_idx, resample, row_mean, sufficient_mean
from ext2k1.canonical import canonical_bytes, canonical_sha256
from ext2k1.constants import IDX_SHA256_N31
from ext2k1.metrics import primary_side
from ext2k1.pins_io import sweeps_module_sha256
from ext2k1.quotes import classify_sweeps
from ext2k1.report import build_results, published_results
from ext2k1.sweeps import build


def _run_once():
    tape = support.FIXTURES["tape"]
    _receipt, _document, body = build_results(
        tape["rows"],
        tape["markets"],
        tape["week_membership"],
        support.synthetic_pins(),
        builder_sha256=support.BUILDER_SHA256,
        source_pins=support.SOURCE_PINS,
        sweeps_module_sha256=sweeps_module_sha256(),
        b2_rows=tape["b2_fills"],
    )
    return canonical_bytes(published_results(body))


class T06Bootstrap(unittest.TestCase):
    def test_p8_row_mean_matches_sufficient_stats(self):
        tape = support.FIXTURES["tape"]
        document = build(tape["rows"], tape["markets"])
        records = classify_sweeps(document["sweeps"], tape["rows"])
        events = sorted(tape["week_membership"])
        idx = make_idx(len(events))
        self.assertEqual(canonical_sha256(idx), IDX_SHA256_N31)
        self.assertEqual(canonical_sha256(idx), support.EXPECTED["IDX_sha256"])
        for side in (1, -1):
            estimate = primary_side(events, records, side, idx)
            for draw in idx[:200]:
                naive = row_mean(events, estimate["_lists"], draw)
                packed = sufficient_mean(events, estimate["_stats"], draw)
                if naive is None:
                    self.assertIsNone(packed)
                else:
                    self.assertLessEqual(abs(naive - packed), 1e-12)

    def test_hand3_and_zero_sweep_draw(self):
        hand = support.FIXTURES["t06_hand3"]
        idx = make_idx(3, draws=hand["B"], seed=hand["seed"])
        self.assertEqual(idx, hand["IDX"])
        events = hand["events"]
        stats = {event: tuple(pair) for event, pair in hand["per_event_n_sum"].items()}
        draw = resample(events, stats, idx)
        self.assertEqual(draw["dropped"], 1)
        self.assertEqual(draw["dropped"], hand["dropped"])
        self.assertTrue(support.near(draw["kept_values"], hand["kept_sorted"]))
        self.assertEqual(draw["L"], hand["L"])
        self.assertEqual(draw["U"], hand["U"])
        means = [sufficient_mean(events, stats, one) for one in idx]
        self.assertTrue(support.near(means, hand["stat_per_draw"]))
        zero = resample(events, stats, [[0, 0, 0]])
        self.assertEqual(zero["dropped"], 1)
        self.assertEqual(zero["kept"], 0)
        self.assertIsNone(zero["L"])
        self.assertIsNone(zero["U"])

    def test_two_runs_match_and_wall_time_is_recorded(self):
        started = time.perf_counter()
        first = _run_once()
        second = _run_once()
        elapsed = time.perf_counter() - started
        print("T06_bootstrap_wall_s %.6f" % elapsed)
        self.assertEqual(first, second)
        self.assertLess(elapsed, 120.0)


if __name__ == "__main__":
    unittest.main()
