"""v2 fee-state consumers. Synthetic gates only.

A gate computes only when fee_admission is ADMITTED_INDEX_ONLY and the
caller supplied the fee-source sha and accept sha. A legacy two-field
ATTEST_PASS does not admit.
"""
from __future__ import annotations

import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from card01_amc.entry_gate import gate_v2
from card01_amc.fee_admission import FEE_FORMULA_ID, SENSITIVITY_ROWS_STATUS
from card01_amc.pinload import sha256_bytes
from card01_amc.swing_stress import evaluate
from card01_amc.verdict import apply_verdict
from tests.support import LAB
from tests.test_fee_admission_v2 import ADMITTED_ID, _copy_kit, _row

RETIRED = (
    "PENDING_ADOPTION_RULE_AMENDMENT",
    "FEE_ATTESTATION_MISSING",
    "FEE_REATTEST_NOT_PASS",
)
FORMULA_MISMATCH = "FEE_FORMULA_ID_MISMATCH"
BLOCK_REASONS = (
    "FEE_SOURCE_NOT_ADMITTED_V1_ATTEST_FAIL",
    "FEE_SOURCE_PAIR_MISSING",
    "FEE_SOURCE_REHASH_MISMATCH",
    "FEE_SOURCE_NOT_ANCHORED",
    "FEE_SOURCE_STATUS_NOT_ADOPTED",
    "FEE_ACCEPT_MISSING",
    "FEE_ACCEPT_REHASH_MISMATCH",
    "FEE_SOURCE_IN_FILE_UNEXPECTED",
    FORMULA_MISMATCH,
    "SERIES_NOT_PINNED",
    "HEADLINE_SCOPE_MISMATCH",
)
_BANNED_NUMBERS = {
    "fee",
    "fee_decimal",
    "fee_headline",
    "expected_net",
    "expected_net_gate",
    "expected_gross",
    "gross",
    "net_headline",
    "net_fees_2x",
}


def _no_numeric_fee(obj) -> bool:
    def walk(node):
        if isinstance(node, dict):
            for key, val in node.items():
                if key in _BANNED_NUMBERS and isinstance(val, (int, float)):
                    return False
                if key in _BANNED_NUMBERS and isinstance(val, str):
                    try:
                        Decimal(val)
                    except Exception:
                        pass
                    else:
                        if val != "BLOCKED_FEE_UNVERIFIED":
                            return False
                if not walk(val):
                    return False
        elif isinstance(node, list):
            for item in node:
                if not walk(item):
                    return False
        return True

    return walk(obj)


def _score():
    return {
        "all_admitted": {
            "n": 2,
            "states": 2,
            "arms": {
                "0.5": {
                    "CI95_D_raw": [-0.02, -0.01],
                    "CI95_D_rc": [-0.03, -0.02],
                }
            },
        }
    }


def _clear_cd():
    return {"n_signals": 1, "reject_c": False, "reject_d": False}


def _blocked_gate(reason):
    return {
        "status": "OK",
        "n_selected": 1,
        "signals": [{
            "race_id": "G1-01",
            "side": "D_YES",
            "price": 0.055,
            "fee": 0.005,
            "fee_decimal": "0.005",
            "series": "XS1",
            "fee_source": ADMITTED_ID,
            "fee_source_sha256": "ab" * 32,
        }],
        "fee_admission": "BLOCKED_FEE_UNVERIFIED",
        "fee_block_reason": reason,
        "fee_formula_id": FEE_FORMULA_ID,
        "adoption_mode": "INDEX_ONLY",
        "fee_source": ADMITTED_ID,
        "fee_source_sha256": "ab" * 32,
    }


def _admitted_shape(**overrides):
    gate = {
        "status": "OK",
        "n_selected": 0,
        "signals": [],
        "fee_admission": "ADMITTED_INDEX_ONLY",
        "adoption_mode": "INDEX_ONLY",
        "fee_formula_id": FEE_FORMULA_ID,
        "fee_source": ADMITTED_ID,
        "fee_source_sha256": "cd" * 32,
    }
    gate.update(overrides)
    return gate


def _assert_retired(testcase, blob, reason=None):
    for retired in RETIRED:
        testcase.assertNotIn(retired, blob)
    if reason != FORMULA_MISMATCH:
        testcase.assertNotIn(FORMULA_MISMATCH, blob)


class SwingConsumerTests(unittest.TestCase):
    def _assert_blocked(self, out, reason):
        self.assertEqual(out["stress_status"], "BLOCKED_FEE_UNVERIFIED")
        self.assertEqual(out["fragility"], "NOT_EVALUATED_FEE_BLOCKED")
        self.assertIsNone(out["rows"])
        self.assertEqual(out["fee_block_reason"], reason)
        self.assertEqual(out["net_block_reason"], reason)
        self.assertTrue(_no_numeric_fee(out))
        self.assertNotIn("NO_SIGNALS_SELECTED", json.dumps(out))
        _assert_retired(self, json.dumps(out), reason)

    def test_swing_admitted_computes_headline(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = _copy_kit(Path(tmp))
            digest = sha256_bytes(paths[0].read_bytes())
            gated = gate_v2(
                [_row()],
                fee_source_path=paths[0],
                fee_source_id=ADMITTED_ID,
                fee_source_sha256=digest,
                packet_index_path=paths[2],
                fee_accept_path=paths[1],
            )
            self.assertEqual(gated["status"], "OK")
            self.assertEqual(gated["fee_admission"], "ADMITTED_INDEX_ONLY")
            self.assertGreater(gated["n_selected"], 0)
            out = evaluate(
                [_row()],
                gated,
                "r",
                "g",
                "g",
                fee_source_path=paths[0],
                packet_index_path=paths[2],
                fee_accept_path=paths[1],
                fee_source_expected_id=ADMITTED_ID,
                fee_source_expected_sha256=digest,
                fee_source_expected_accept=gated["fee_source_accept_sha256"],
                fee_source_expected_formula=FEE_FORMULA_ID,
            )
            self.assertEqual(out["stress_status"], "OK")
            for signal in gated["signals"]:
                signal["fee"] = 9.0
            again = evaluate(
                [_row()],
                gated,
                "r",
                "g",
                "g",
                fee_source_path=paths[0],
                packet_index_path=paths[2],
                fee_accept_path=paths[1],
                fee_source_expected_id=ADMITTED_ID,
                fee_source_expected_sha256=digest,
                fee_source_expected_accept=gated["fee_source_accept_sha256"],
            )
        self.assertIsInstance(out["rows"][0]["expected_net"], float)
        self.assertIsInstance(out["rows"][0]["expected_gross"], float)
        self.assertNotIn("expected_net_sensitivity_direct_member", out["rows"][0])
        self.assertEqual(out["sensitivity_rows_status"], SENSITIVITY_ROWS_STATUS)
        self.assertEqual(again["rows"][0]["expected_net"], out["rows"][0]["expected_net"])
        blob = json.dumps(out)
        for key in (
            "fee_only_ceil",
            "fee_direct_0001",
            "net_fee_only_ceil",
            "net_direct_0001",
            "fee_sensitivity_direct_member",
            "expected_net_sensitivity_direct_member",
            "FEE_ONLY_CEIL",
            "DIRECT_MEMBER_GRID",
        ):
            self.assertNotIn(key, blob)
        _assert_retired(self, blob)

    def test_swing_blocked_gate_absent(self):
        out = evaluate(
            [_row()],
            None,
            "r",
            None,
            fee_source_path="fee.json",
            packet_index_path="index.md",
            fee_accept_path="accept.json",
        )
        self._assert_blocked(out, "GATE_MISSING")

    def test_swing_blocked_gate_status_not_ok(self):
        gate = {
            "status": "MAYBE",
            "fee_formula_id": FEE_FORMULA_ID,
            "fee_admission": "ADMITTED_INDEX_ONLY",
        }
        out = evaluate([_row()], gate, "r", "g")
        self._assert_blocked(out, "GATE_STATUS_NOT_OK")

    def test_swing_blocked_pair_mismatch(self):
        out = evaluate(
            [_row()],
            _admitted_shape(fee_source_accept_sha256="ee" * 32),
            "r",
            "g",
            fee_source_expected_sha256="ab" * 32,
            fee_source_expected_accept="ee" * 32,
        )
        self._assert_blocked(out, "FEE_SOURCE_PAIR_MISMATCH")

    def test_swing_blocked_pair_missing(self):
        out = evaluate([_row()], _admitted_shape(), "r", "g")
        self._assert_blocked(out, "FEE_SOURCE_PAIR_MISSING")

    def test_swing_blocked_fee_admission_missing(self):
        gate = _admitted_shape()
        del gate["fee_admission"]
        out = evaluate(
            [_row()],
            gate,
            "r",
            "g",
            fee_source_expected_id=ADMITTED_ID,
            fee_source_expected_sha256="cd" * 32,
            fee_source_expected_formula=FEE_FORMULA_ID,
        )
        self._assert_blocked(out, "FEE_ADMISSION_MISSING")

    def test_swing_blocked_fee_admission_other(self):
        out = evaluate(
            [_row()],
            _admitted_shape(fee_admission="SOFT_PASS"),
            "r",
            "g",
            fee_source_expected_id=ADMITTED_ID,
            fee_source_expected_sha256="cd" * 32,
            fee_source_expected_formula=FEE_FORMULA_ID,
        )
        self._assert_blocked(out, "FEE_ADMISSION_NOT_ADMITTED")

    def test_unattested_empty_gate_is_blocked_before_zero_signals(self):
        gate = {
            "status": "OK",
            "n_selected": 0,
            "signals": [],
            "fee_source": "SYNTH_V1_GATE",
            "fee_source_sha256": "ab" * 32,
            "fee_attest_verdict": "ATTEST_PASS",
            "fee_attest_fee_source_sha256": "ab" * 32,
        }
        out = evaluate([_row()], gate, "r", "g")
        self._assert_blocked(out, "FEE_ADMISSION_MISSING")

    def test_legacy_attest_pass_does_not_admit(self):
        digest = "ab" * 32
        refused = {
            "status": "OK",
            "n_selected": 0,
            "signals": [],
            "fee_source": "FEE_SOURCE_CARD01_v1",
            "fee_source_sha256": digest,
            "fee_attest_verdict": "ATTEST_PASS",
            "fee_attest_fee_source_sha256": digest,
        }
        plain = {
            "status": "OK",
            "n_selected": 0,
            "signals": [],
            "fee_source": "SYNTH_V1_GATE",
            "fee_source_sha256": digest,
            "fee_attest_verdict": "ATTEST_PASS",
            "fee_attest_fee_source_sha256": "cd" * 32,
        }
        self._assert_blocked(
            evaluate([_row()], refused, "r", "g"),
            "FEE_SOURCE_NOT_ADMITTED_V1_ATTEST_FAIL",
        )
        self._assert_blocked(evaluate([_row()], plain, "r", "g"), "FEE_ADMISSION_MISSING")


class VerdictConsumerTests(unittest.TestCase):
    def _assert_blocked(self, verdict, reason):
        self.assertEqual(verdict["fee_state"], "BLOCKED_FEE_UNVERIFIED")
        self.assertEqual(verdict["fee_block_reason"], reason)
        self.assertEqual(verdict["evaluations"]["reject_c"], "BLOCKED_FEE_UNVERIFIED")
        self.assertEqual(verdict["evaluations"]["reject_d"], "BLOCKED_FEE_UNVERIFIED")
        self.assertNotEqual(verdict["verdict"], "PASS-FORECAST")
        self.assertNotEqual(verdict["verdict"], "REJECT")
        self.assertNotEqual(verdict["verdict"], "FULL_VERDICT_REQUIRES_EXAMINER")
        self.assertTrue(verdict["verdict"].startswith("FORECAST_ONLY_FEE_BLOCKED"))
        self.assertTrue(_no_numeric_fee(verdict))
        _assert_retired(self, json.dumps(verdict), reason)

    def _apply(self, gate, **kwargs):
        return apply_verdict(_score(), gate=gate, cd=_clear_cd(), **kwargs)

    def test_verdict_admitted_computes(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = _copy_kit(Path(tmp))
            digest = sha256_bytes(paths[0].read_bytes())
            gated = gate_v2(
                [_row()],
                fee_source_path=paths[0],
                fee_source_id=ADMITTED_ID,
                fee_source_sha256=digest,
                packet_index_path=paths[2],
                fee_accept_path=paths[1],
            )
        common = {
            "gate": gated,
            "expected_fee_sha256": digest,
            "expected_accept_sha256": gated["fee_source_accept_sha256"],
        }
        rejected = apply_verdict(
            _score(),
            cd={"n_signals": 1, "reject_c": True, "reject_d": False},
            **common,
        )
        cleared = apply_verdict(
            _score(),
            cd={"n_signals": 1, "reject_c": False, "reject_d": False},
            **common,
        )
        self.assertEqual(rejected["fee_state"], "ADMITTED")
        self.assertIsNone(rejected["fee_block_reason"])
        self.assertEqual(rejected["verdict"], "REJECT")
        self.assertEqual(rejected["firing"], ["(c)"])
        self.assertEqual(cleared["fee_state"], "ADMITTED")
        self.assertEqual(cleared["verdict"], "PASS-FORECAST")
        self.assertEqual(cleared["firing"], [])
        _assert_retired(self, json.dumps(rejected) + json.dumps(cleared))

    def test_verdict_blocked_gate_absent(self):
        self._assert_blocked(apply_verdict(_score(), gate=None, cd=_clear_cd()), "GATE_MISSING")

    def test_verdict_blocked_gate_status_not_ok(self):
        gate = {
            "status": "MAYBE",
            "fee_formula_id": FEE_FORMULA_ID,
            "fee_admission": "ADMITTED_INDEX_ONLY",
        }
        self._assert_blocked(self._apply(gate), "GATE_STATUS_NOT_OK")

    def test_verdict_blocked_pair_mismatch(self):
        verdict = apply_verdict(
            _score(),
            gate=_admitted_shape(fee_source_accept_sha256="ee" * 32),
            cd=_clear_cd(),
            expected_fee_sha256="ab" * 32,
            expected_accept_sha256="ee" * 32,
        )
        self._assert_blocked(verdict, "FEE_SOURCE_PAIR_MISMATCH")

    def test_verdict_blocked_pair_missing(self):
        verdict = apply_verdict(_score(), gate=_admitted_shape(), cd=_clear_cd())
        self._assert_blocked(verdict, "FEE_SOURCE_PAIR_MISSING")

    def test_verdict_blocked_fee_admission_missing(self):
        gate = _admitted_shape()
        del gate["fee_admission"]
        verdict = apply_verdict(
            _score(),
            gate=gate,
            cd=_clear_cd(),
            expected_fee_sha256="cd" * 32,
            expected_accept_sha256="ee" * 32,
        )
        self._assert_blocked(verdict, "FEE_ADMISSION_MISSING")

    def test_verdict_blocked_fee_admission_other(self):
        verdict = apply_verdict(
            _score(),
            gate=_admitted_shape(fee_admission="SOFT_PASS"),
            cd=_clear_cd(),
            expected_fee_sha256="cd" * 32,
            expected_accept_sha256="ee" * 32,
        )
        self._assert_blocked(verdict, "FEE_ADMISSION_NOT_ADMITTED")

    def test_verdict_v1_pair_has_no_default(self):
        refused = "d4dc8e72ae2b2a72824487eb386d6684c451a5e3b2e9dce58c1a68aaea9436cd"
        gate = _admitted_shape(
            fee_source="FEE_SOURCE_CARD01_v1",
            fee_source_sha256=refused,
            fee_source_accept_sha256="22" * 32,
        )
        verdict = apply_verdict(
            _score(),
            gate=gate,
            cd=_clear_cd(),
            expected_fee_sha256=refused,
            expected_accept_sha256="22" * 32,
        )
        self._assert_blocked(verdict, "FEE_SOURCE_NOT_ADMITTED_V1_ATTEST_FAIL")
        bare = apply_verdict(_score(), cd=_clear_cd())
        self.assertEqual(bare["fee_state"], "BLOCKED_FEE_UNVERIFIED")
        self.assertEqual(bare["fee_block_reason"], "GATE_MISSING")


def _swing_reason(reason):
    def test(self):
        self._assert_blocked(evaluate([_row()], _blocked_gate(reason), "r", "g"), reason)
    test.__name__ = "test_swing_blocked_" + reason
    return test


def _verdict_reason(reason):
    def test(self):
        self._assert_blocked(self._apply(_blocked_gate(reason)), reason)
    test.__name__ = "test_verdict_blocked_" + reason
    return test


for _reason in BLOCK_REASONS:
    setattr(SwingConsumerTests, "test_swing_blocked_" + _reason, _swing_reason(_reason))
    setattr(VerdictConsumerTests, "test_verdict_blocked_" + _reason, _verdict_reason(_reason))


class SyntheticV1GateTests(unittest.TestCase):
    def test_synthetic_v1_gate_blocks_in_swing_verdict_and_regime(self):
        from card01_amc.entry_gate import gate
        from card01_amc.regime_split_secondary import build_report
        from tests.test_regime_split_secondary import _selection, fixture_a

        digest = "ab" * 32
        legacy = {
            "status": "OK",
            "n_selected": 1,
            "signals": [{
                "race_id": "G1-01",
                "side": "D_YES",
                "price": 0.055,
                "fee": 0.005,
                "fee_decimal": "0.005",
                "series": "XS1",
                "fee_source": "SYNTH_V1_GATE",
                "fee_source_sha256": digest,
            }],
            "fee_source": "SYNTH_V1_GATE",
            "fee_source_sha256": digest,
            "fee_attest_verdict": "ATTEST_PASS",
            "fee_attest_fee_source_sha256": digest,
        }
        swing = evaluate([_row()], legacy, "r", "g", "g")
        self.assertEqual(swing["stress_status"], "BLOCKED_FEE_UNVERIFIED")
        self.assertEqual(swing["fee_block_reason"], "FEE_ADMISSION_MISSING")
        self.assertIsNone(swing["rows"])
        self.assertTrue(_no_numeric_fee(swing))
        verdict = apply_verdict(
            _score(),
            gate=legacy,
            cd=_clear_cd(),
            expected_fee_sha256=digest,
            expected_accept_sha256="22" * 32,
        )
        self.assertEqual(verdict["fee_state"], "BLOCKED_FEE_UNVERIFIED")
        self.assertEqual(verdict["fee_block_reason"], "FEE_ADMISSION_MISSING")
        self.assertTrue(verdict["verdict"].startswith("FORECAST_ONLY_FEE_BLOCKED"))
        minted = gate([_row()], b'{"manifest_id":"SYNTH_V1_GATE"}')
        self.assertEqual(minted["status"], "BLOCKED_FEE_UNVERIFIED")
        self.assertEqual(minted["reason"], "FEE_SOURCE_NOT_ADMITTED_V1_ATTEST_FAIL")
        self.assertIsNone(minted["signals"])
        self.assertNotIn("FEE_ONLY_CEIL", json.dumps(minted))
        self.assertNotIn("fee_sensitivity_direct_member", json.dumps(minted))
        with tempfile.TemporaryDirectory() as tmp:
            paths = _copy_kit(Path(tmp))
            report = build_report(
                fixture_a(),
                selection=_selection(),
                gate=legacy,
                fee_source_path=paths[0],
                fee_source_id=ADMITTED_ID,
                fee_source_sha256=sha256_bytes(paths[0].read_bytes()),
                packet_index_path=paths[2],
                fee_accept_path=paths[1],
            )
        self.assertEqual(report["fee_admission"]["fee_admission"], "ADMITTED_INDEX_ONLY")
        self.assertEqual(report["verdict_fee_branch"], "FORECAST_ONLY_FEE_BLOCKED")
        self.assertEqual(report["fee_state"], "BLOCKED_FEE_UNVERIFIED")
        self.assertEqual(report["fee_block_reason"] if "fee_block_reason" in report else report["secondary"]["fee_block_reason"], "FEE_ADMISSION_MISSING")
        self.assertIsNone(report["fee_views"])
        self.assertNotIn('"fee_headline": "0"', json.dumps(report))
        self.assertTrue(_no_numeric_fee(report["secondary"]))


class RetiredStringTests(unittest.TestCase):
    def test_t23_retired_strings_absent_from_card01_amc(self):
        root = LAB / "card01_amc"
        for path in sorted(root.glob("*.py")):
            text = path.read_text()
            for retired in RETIRED:
                self.assertNotIn(retired, text, path.name)


if __name__ == "__main__":
    unittest.main()
