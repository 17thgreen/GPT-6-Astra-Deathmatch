"""AF-5 counting, degenerate blocks, the verdict helper, and P8 strings."""
from __future__ import annotations

import platform
import random
import sys
import unittest

from card01_amc.pinload import load_national_miss
from card01_amc.score import block_with_boundary_count, score_document
from card01_amc.verdict import apply_verdict


def _race(i, state, y, mapping="KXHOUSERACE"):
    return {
        "race_id": f"R{i}",
        "state": state,
        "mapping_status": mapping,
        "p_market": 0.40,
        "p_model": 0.55,
        "y": y,
    }


class BoundaryCountTests(unittest.TestCase):
    def test_counter_matches_independent_stream_and_pinned_ci(self):
        pinned = load_national_miss()
        rows = []
        states = ("PA", "OH", "NY")
        for i in range(8):
            rows.append(_race(i, states[i % 3], 1))
        block = block_with_boundary_count(rows, pinned)
        counts = block["n_boundary_resamples"]

        states_sorted = sorted({r["state"] for r in rows})
        by = {s: [r for r in rows if r["state"] == s] for s in states_sorted}
        rng = random.Random(pinned.SEED)
        independent = {str(w): 0 for w in pinned.WS}
        for _ in range(pinned.B_RESAMPLES):
            rs = [r for s in rng.choices(states_sorted, k=len(states_sorted)) for r in by[s]]
            st = pinned.stats(rs)
            for w in pinned.WS:
                if st[str(w)]["boundary"] is True:
                    independent[str(w)] += 1
        self.assertEqual(counts, independent)
        for value in counts.values():
            self.assertEqual(value, 10000)

        ci = pinned.boot(rows)
        for w in pinned.WS:
            arm = block["arms"][str(w)]
            self.assertEqual(arm["CI95_D_raw"], ci[str(w)]["D_raw"])
            self.assertEqual(arm["CI95_D_rc"], ci[str(w)]["D_rc"])


class DegenerateTests(unittest.TestCase):
    def test_zero_races(self):
        rows = [
            {"race_id": "R0", "state": "PA", "mapping_status": "UNRESOLVED",
             "p_market": None, "p_model": None, "y": None},
            {"race_id": "R1", "state": "OH", "mapping_status": "LEGACY",
             "p_market": 0.4, "p_model": 0.5, "y": None},
        ]
        scored = score_document({"rows": rows})
        self.assertEqual(scored["all_admitted"], {"n": 0})
        self.assertNotIn("n_boundary_resamples", scored["all_admitted"])
        self.assertEqual(scored["headline_status"], "INCONCLUSIVE_DEGENERATE_BLOCK")
        self.assertEqual(scored["degenerate_reason"], "N_ZERO")
        verdict = apply_verdict(scored)
        self.assertEqual(verdict["verdict"], "INCONCLUSIVE_DEGENERATE_BLOCK")
        self.assertEqual(verdict["firing"], [])

    def test_one_state_outranks_reject_b(self):
        rows = [_race(i, "PA", y) for i, y in enumerate((1, 0, 1))]
        for row in rows:
            row["p_model"] = row["p_market"]
        scored = score_document({"rows": rows})
        block = scored["all_admitted"]
        self.assertEqual(block["states"], 1)
        for arm in block["arms"].values():
            self.assertEqual(arm["CI95_D_raw"][0], arm["CI95_D_raw"][1])
            self.assertEqual(arm["CI95_D_rc"][0], arm["CI95_D_rc"][1])
        self.assertGreaterEqual(block["arms"]["0.5"]["CI95_D_rc"][1], 0)
        self.assertEqual(scored["headline_status"], "INCONCLUSIVE_DEGENERATE_BLOCK")
        self.assertEqual(scored["degenerate_reason"], "FEWER_THAN_2_STATES")
        self.assertEqual(scored["leave_one_state_out"]["by_state"]["PA"], "UNDEFINED")
        verdict = apply_verdict(scored)
        self.assertEqual(verdict["verdict"], "INCONCLUSIVE_DEGENERATE_BLOCK")
        self.assertNotIn("REJECT", verdict["verdict"])
        self.assertEqual(verdict["firing"], [])

    def test_two_states_defined(self):
        rows = [
            _race(0, "PA", 1),
            _race(1, "PA", 0),
            _race(2, "OH", 1),
            _race(3, "OH", 0),
        ]
        scored = score_document({"rows": rows})
        self.assertEqual(scored["headline_status"], "DEFINED")
        self.assertIsNone(scored["degenerate_reason"])
        self.assertEqual(scored["split_status"]["split_KXHOUSERACE"]["status"], "DEFINED")
        lo = scored["leave_one_state_out"]
        self.assertEqual(set(lo["by_state"]), {"OH", "PA"})
        self.assertNotEqual(lo["by_state"]["PA"], "UNDEFINED")
        self.assertEqual(scored["python_version"], sys.version)
        self.assertEqual(scored["platform"], platform.platform())
        self.assertEqual(
            scored["bootstrap_sampler"],
            "random.Random(20261102).choices(sorted_states, k=len(sorted_states)), fresh per block",
        )
        self.assertEqual(
            scored["percentile_method"],
            "order statistics xs[250], xs[9749] of 10000 ascending",
        )
        self.assertEqual(scored["state_encoding"], "USPS2 from universe code")
        self.assertEqual(scored["rows_order"], "UNIVERSE_2026_HOUSE_FROZEN order")
        self.assertIsInstance(scored["python_version"], str)
        self.assertIsInstance(scored["platform"], str)


class VerdictTests(unittest.TestCase):
    def _score(self, raw_hi, rc_hi, rc_lo=None):
        return {
            "headline_status": "DEFINED",
            "all_admitted": {
                "n": 4,
                "states": 2,
                "arms": {
                    "0.5": {
                        "CI95_D_raw": [-0.2, raw_hi],
                        "CI95_D_rc": [rc_hi - 0.1 if rc_lo is None else rc_lo, rc_hi],
                    }
                },
            },
        }

    def test_pass_forecast(self):
        verdict = apply_verdict(self._score(-0.01, -0.02))
        self.assertEqual(verdict["verdict"], "FORECAST_ONLY_FEE_BLOCKED: PASS-FORECAST")
        self.assertEqual(verdict["firing"], [])
        self.assertEqual(verdict["evaluations"]["reject_c"], "BLOCKED_FEE_UNVERIFIED")
        self.assertEqual(verdict["evaluations"]["reject_d"], "BLOCKED_FEE_UNVERIFIED")

    def test_reject_a(self):
        verdict = apply_verdict(self._score(0.0, -0.02))
        self.assertEqual(verdict["verdict"], "FORECAST_ONLY_FEE_BLOCKED: REJECT")
        self.assertEqual(verdict["firing"], ["(a)"])

    def test_reject_b_at_zero(self):
        verdict = apply_verdict(self._score(-0.05, 0.0))
        self.assertEqual(verdict["verdict"], "FORECAST_ONLY_FEE_BLOCKED: REJECT")
        self.assertEqual(verdict["firing"], ["(b)"])

    def test_af1_gap_is_reject_b(self):
        verdict = apply_verdict(self._score(-0.01, 0.04, rc_lo=0.01))
        self.assertEqual(verdict["verdict"], "FORECAST_ONLY_FEE_BLOCKED: REJECT")
        self.assertEqual(verdict["firing"], ["(b)"])
        self.assertTrue(verdict["evaluations"]["pass_i"])
        self.assertTrue(verdict["evaluations"]["reject_b"])

    def test_fee_unblocked_requires_examiner(self):
        verdict = apply_verdict(self._score(-0.01, -0.02), fee_blocked=False)
        self.assertEqual(verdict["verdict"], "FULL_VERDICT_REQUIRES_EXAMINER")
        self.assertIsNone(verdict["evaluations"]["reject_c"])
        self.assertIsNone(verdict["evaluations"]["reject_d"])


if __name__ == "__main__":
    unittest.main()
