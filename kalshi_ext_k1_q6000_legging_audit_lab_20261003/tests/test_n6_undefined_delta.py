"""Prospective N6 rule. The PR66 run is unchanged: ON and AGAINST are both populated."""

import unittest

import support  # noqa: F401
from report import contrast, decide_verdict


def _portion(event, bucket):
    return {
        "event": event,
        "s_dev": bucket,
        "size": 10.0,
        "markouts": {"1800": {"gross": 0.01, "net": 0.005}},
    }


def _verdict_from_contrast(report, censored_on=0.0, censored_against=0.0):
    # Conductor ruling CONDUCTOR_RULING_EXT_K1_N6_UNDEFINED_DELTA_2026-10-03,
    # sha256 prefix 0b68c4bf. Prospective only.
    return decide_verdict(
        join_ok=True,
        structural_ok=True,
        unclassified_share=0.0,
        censored_on=censored_on,
        censored_against=censored_against,
        open_at_window_end_contracts=0,
        ci_excludes_0=report["ci_excludes_0"],
        delta_star=report["delta_star_gross"],
        ci_low=report["ci95_low"],
        ci_high=report["ci95_high"],
    )


class N6UndefinedDelta(unittest.TestCase):
    def test_empty_on_or_against_bucket_is_inconclusive(self):
        against_only = contrast([_portion("g1", "AGAINST")], events=["g1"])
        on_only = contrast([_portion("g1", "ON")], events=["g1"])
        for report in (against_only, on_only):
            self.assertIsNone(report["delta_star_gross"])
            self.assertIsNone(report["ci95_low"])
            self.assertIsNone(report["ci95_high"])
            self.assertEqual(report["bootstrap_replicates_dropped_empty_bucket"], report["bootstrap_B"])
            verdict, reasons = _verdict_from_contrast(report, censored_on=None, censored_against=None)
            self.assertEqual(verdict, "INCONCLUSIVE")
            self.assertIn("delta_star_or_ci_undefined", reasons)

    def test_defined_delta_and_ci_stay_descriptive(self):
        # PR66 headlines. Δ* gross does not exclude 0, so the verdict stays DESCRIPTIVE.
        verdict, reasons = decide_verdict(
            join_ok=True,
            structural_ok=True,
            unclassified_share=0.0,
            censored_on=0.0,
            censored_against=0.0,
            open_at_window_end_contracts=0,
            ci_excludes_0=False,
            delta_star=-0.000205,
            ci_low=-0.000577,
            ci_high=0.000188,
        )
        self.assertEqual(verdict, "DESCRIPTIVE")
        self.assertEqual(reasons, ["delta_star_ci95_does_not_exclude_0"])


if __name__ == "__main__":
    unittest.main()
