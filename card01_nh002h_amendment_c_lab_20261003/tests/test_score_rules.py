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
        # Mixed y and distinct prices, so a boundary hit depends on which states
        # the seed draws. Identical rows would make the count 10000 and the CI
        # a point, and an extra rng draw would still match.
        specs = (
            ("PA", 1, 0.20, 0.25),
            ("PA", 1, 0.30, 0.35),
            ("OH", 1, 0.22, 0.40),
            ("NY", 0, 0.70, 0.65),
            ("NY", 0, 0.80, 0.75),
            ("TX", 0, 0.60, 0.55),
            ("CA", 1, 0.45, 0.50),
            ("CA", 0, 0.55, 0.48),
            ("FL", 1, 0.33, 0.62),
            ("FL", 0, 0.71, 0.28),
        )
        self.assertGreaterEqual(len({spec[0] for spec in specs}), 5)
        self.assertGreaterEqual(len(specs), 8)
        self.assertLessEqual(len(specs), 12)
        rows = []
        for i, (state, y, p_market, p_model) in enumerate(specs):
            row = _race(i, state, y)
            row["p_market"] = p_market
            row["p_model"] = p_model
            rows.append(row)
        self.assertGreater(len({r["y"] for r in rows}), 1)
        self.assertGreater(len({r["p_market"] for r in rows}), 1)
        self.assertGreater(len({r["p_model"] for r in rows}), 1)

        block = block_with_boundary_count(rows, pinned)
        counts = block["n_boundary_resamples"]

        states_sorted = sorted({r["state"] for r in rows})
        by = {s: [r for r in rows if r["state"] == s] for s in states_sorted}
        rng = random.Random(20261102)
        independent = {str(w): 0 for w in pinned.WS}
        for _ in range(pinned.B_RESAMPLES):
            rs = [r for s in rng.choices(states_sorted, k=len(states_sorted)) for r in by[s]]
            st = pinned.stats(rs)
            for w in pinned.WS:
                if st[str(w)]["boundary"] is True:
                    independent[str(w)] += 1
        self.assertEqual(counts, independent)
        self.assertTrue(any(0 < value < 10000 for value in counts.values()))

        ci = pinned.boot(rows)
        spread = False
        for w in pinned.WS:
            arm = block["arms"][str(w)]
            self.assertEqual(arm["CI95_D_raw"], ci[str(w)]["D_raw"])
            self.assertEqual(arm["CI95_D_rc"], ci[str(w)]["D_rc"])
            if arm["CI95_D_raw"][0] != arm["CI95_D_raw"][1]:
                spread = True
        self.assertTrue(spread)


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

    def _pair(self):
        return ("FEE_SOURCE_CARD01_v1", "ab" * 32)

    def _gate(self):
        fee_id, digest = self._pair()
        return {
            "status": "OK",
            "fee_source": fee_id,
            "fee_source_sha256": digest,
            "fee_attest_verdict": "ATTEST_PASS",
            "fee_attest_fee_source_sha256": digest,
        }

    def _attestation(self, series_status="PINNED", digest=None):
        from card01_amc.fee_source import CONDUCTOR_ACCEPT_SHA256
        fee_id, default_digest = self._pair()
        return {
            "fee_source": fee_id,
            "fee_source_sha256": default_digest if digest is None else digest,
            "rehash_ok": True,
            "packet_index_anchor_ok": True,
            "status": "ADOPTED",
            "conductor_accept_sha256": CONDUCTOR_ACCEPT_SHA256,
            "series": [{"series": "KXHOUSERACE", "series_status": series_status}],
            "examiner": "synthetic-examiner",
            "time": "2026-11-03T00:00:00Z",
        }

    def _admitted(self, score, cd=None, **kwargs):
        return apply_verdict(
            score,
            gate=self._gate(),
            attestation=self._attestation(),
            cd=cd,
            expected_fee_source=self._pair(),
            **kwargs,
        )

    def test_fee_unblocked_requires_examiner(self):
        verdict = self._admitted(self._score(-0.01, -0.02), cd=None)
        self.assertEqual(verdict["verdict"], "FULL_VERDICT_REQUIRES_EXAMINER")
        self.assertEqual(verdict["fee_state"], "ADMITTED")
        self.assertIsNone(verdict["evaluations"]["reject_c"])
        self.assertIsNone(verdict["evaluations"]["reject_d"])

    def test_validity_and_degenerate_outrank_fee_branch(self):
        degenerate = {
            "headline_status": "INCONCLUSIVE_DEGENERATE_BLOCK",
            "degenerate_reason": "N_ZERO",
            "all_admitted": {"n": 0},
        }
        void = apply_verdict(
            degenerate,
            validity={"licence_gate": "REFUSED"},
            gate=self._gate(),
            attestation=self._attestation(),
            cd={"n_signals": 0, "reject_c": None, "reject_d": None},
            expected_fee_source=self._pair(),
        )
        self.assertEqual(void["verdict"], "VOID")
        self.assertEqual(void["reason"], "LICENCE_GATE_REFUSED")
        self.assertEqual(void["firing"], [])

        outranked = self._admitted(
            degenerate,
            cd={"n_signals": 0, "reject_c": None, "reject_d": None},
        )
        self.assertEqual(outranked["verdict"], "INCONCLUSIVE_DEGENERATE_BLOCK")
        self.assertEqual(outranked["firing"], [])
        self.assertTrue(outranked["evaluations"]["reject_c"])
        self.assertTrue(outranked["evaluations"]["reject_d"])
        self.assertIn("NO_SIGNALS_SELECTED", outranked["notes"])

        admitted_a = self._admitted(
            self._score(0.0, -0.02),
            cd={"n_signals": 2, "reject_c": False, "reject_d": False},
        )
        self.assertEqual(admitted_a["verdict"], "REJECT")
        self.assertEqual(admitted_a["firing"], ["(a)"])
        self.assertNotIn("FORECAST_ONLY", admitted_a["verdict"])

    def test_admitted_c_and_d_and_missing_attestation(self):
        zero = self._admitted(
            self._score(-0.01, -0.02),
            cd={"n_signals": 0, "reject_c": None, "reject_d": None},
        )
        self.assertEqual(zero["verdict"], "REJECT")
        self.assertEqual(zero["firing"], ["(c)", "(d)"])
        self.assertIn("NO_SIGNALS_SELECTED", zero["notes"])
        self.assertTrue(zero["evaluations"]["reject_d"])

    def test_reject_d_is_literal_at_zero_signals(self):
        zero = self._admitted(
            self._score(-0.01, -0.02),
            cd={"n_signals": 0, "reject_c": False, "reject_d": False},
        )
        self.assertEqual(zero["verdict"], "REJECT")
        self.assertEqual(zero["firing"], ["(c)", "(d)"])
        self.assertNotIn("FORECAST_ONLY", zero["verdict"])
        self.assertIn("NO_SIGNALS_SELECTED", zero["notes"])
        self.assertTrue(zero["evaluations"]["reject_c"])
        self.assertIs(zero["evaluations"]["reject_d"], True)
        blocked = apply_verdict(
            self._score(-0.01, -0.02),
            cd={"n_signals": 0, "reject_c": False, "reject_d": False},
        )
        self.assertEqual(blocked["verdict"], "FORECAST_ONLY_FEE_BLOCKED: PASS-FORECAST")
        self.assertEqual(blocked["evaluations"]["reject_c"], "BLOCKED_FEE_UNVERIFIED")
        self.assertEqual(blocked["evaluations"]["reject_d"], "BLOCKED_FEE_UNVERIFIED")

        only_c = self._admitted(
            self._score(-0.01, -0.02),
            cd={"n_signals": 2, "reject_c": True, "reject_d": False},
        )
        self.assertEqual(only_c["verdict"], "REJECT")
        self.assertEqual(only_c["firing"], ["(c)"])

        only_d = self._admitted(
            self._score(-0.01, -0.02),
            cd={"n_signals": 2, "reject_c": False, "reject_d": True},
        )
        self.assertEqual(only_d["firing"], ["(d)"])

        clear = self._admitted(
            self._score(-0.01, -0.02),
            cd={"n_signals": 2, "reject_c": False, "reject_d": False},
        )
        self.assertEqual(clear["verdict"], "PASS-FORECAST")
        self.assertEqual(clear["firing"], [])

        missing = apply_verdict(
            self._score(-0.01, -0.02),
            gate=self._gate(),
            expected_fee_source=self._pair(),
        )
        self.assertEqual(missing["fee_state"], "BLOCKED")
        self.assertIn("FEE_ATTESTATION_MISSING", missing["notes"])
        self.assertEqual(missing["verdict"], "FORECAST_ONLY_FEE_BLOCKED: PASS-FORECAST")

        wrong = apply_verdict(
            self._score(-0.01, -0.02),
            gate=self._gate(),
            attestation=self._attestation(digest="cd" * 32),
            cd={"n_signals": 2, "reject_c": False, "reject_d": False},
            expected_fee_source=self._pair(),
        )
        self.assertEqual(wrong["fee_state"], "BLOCKED")
        self.assertNotIn("FEE_ATTESTATION_MISSING", wrong["notes"])

        unpinned = apply_verdict(
            self._score(-0.01, -0.02),
            gate=self._gate(),
            attestation=self._attestation(series_status="BLOCKED_FEE_UNVERIFIED"),
            cd={"n_signals": 2, "reject_c": False, "reject_d": False},
            expected_fee_source=self._pair(),
        )
        self.assertEqual(unpinned["fee_state"], "BLOCKED")
        self.assertEqual(unpinned["verdict"], "FORECAST_ONLY_FEE_BLOCKED: PASS-FORECAST")

        bare = self._gate()
        bare.pop("fee_attest_verdict")
        bare.pop("fee_attest_fee_source_sha256")
        alone = apply_verdict(
            self._score(-0.01, -0.02),
            gate=bare,
            attestation=self._attestation(),
            cd={"n_signals": 2, "reject_c": False, "reject_d": False},
            expected_fee_source=self._pair(),
        )
        self.assertEqual(alone["fee_state"], "BLOCKED")
        self.assertEqual(alone["verdict"], "FORECAST_ONLY_FEE_BLOCKED: PASS-FORECAST")


if __name__ == "__main__":
    unittest.main()
