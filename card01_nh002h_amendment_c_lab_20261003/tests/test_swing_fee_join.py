"""AF-7 swing stress, AF-4 fee block, and the post-settlement join."""
from __future__ import annotations

import ast
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from card01_amc.entry_gate import gate
from card01_amc.fee_admission import FEE_FORMULA_ID
from card01_amc.join_outcomes import join
from card01_amc.pinload import load_national_miss
from card01_amc.swing_stress import FORBIDDEN_OUTCOME_KEYS, OutcomePresent, evaluate
from tests.support import LAB, adopted_manifest


def _row(race_id, p_model, p_market, y=None):
    return {
        "race_id": race_id,
        "state": race_id[:2],
        "mapping_status": "KXHOUSERACE",
        "series": "KXHOUSERACE",
        "p_market": p_market,
        "p_model": p_model,
        "y": y,
        "ticker": "T-" + race_id,
        "yes_bid": 0.40,
        "yes_ask": 0.60,
        "yes_bid_qty": 5,
        "yes_ask_qty": 5,
        "exclusion_reason": None,
    }


def _signal(race_id, side, price, fee, source="entry-KXHOUSERACE"):
    return {
        "race_id": race_id,
        "side": side,
        "price": price,
        "fee": fee,
        "fee_source": source,
        "visible_qty": 5,
        "expected_net_gate": 0.0,
    }


_V2_SHA = "11" * 32
_V2_ACCEPT = "22" * 32


def _ok_gate(signals, adopted=None):
    del adopted
    prepared = []
    for signal in signals:
        item = dict(signal)
        item.setdefault("series", "XS1")
        item.setdefault("fee_source", "FEE_SOURCE_SYNTH_v2")
        item.setdefault("fee_source_sha256", _V2_SHA)
        if item.get("fee_decimal") is None and item.get("fee") is not None:
            item["fee_decimal"] = str(item["fee"])
        prepared.append(item)
    return {
        "status": "OK",
        "n_selected": len(prepared),
        "signals": prepared,
        "fee_admission": "ADMITTED_INDEX_ONLY",
        "adoption_mode": "INDEX_ONLY",
        "fee_formula_id": FEE_FORMULA_ID,
        "fee_source": "FEE_SOURCE_SYNTH_v2",
        "fee_source_sha256": _V2_SHA,
        "fee_source_accept_sha256": _V2_ACCEPT,
    }


def _admitted(**extra):
    kwargs = {
        "fee_source_expected_sha256": _V2_SHA,
        "fee_source_expected_accept": _V2_ACCEPT,
    }
    kwargs.update(extra)
    return kwargs


class SwingTests(unittest.TestCase):
    def test_null_y_runs_and_non_null_refuses(self):
        rows = [_row("AL-02", 0.60, 0.40, y=None)]
        blocked = {"status": "BLOCKED_FEE_UNVERIFIED", "signals": None, "reason": "MANIFEST_ABSENT"}
        out = evaluate(rows, blocked, "rows-sha", "gate-sha")
        self.assertEqual(out["stress_status"], "BLOCKED_FEE_UNVERIFIED")
        self.assertEqual(out["fragility"], "NOT_EVALUATED_FEE_BLOCKED")
        self.assertIsNone(out["rows"])
        self.assertIn("output_sha256", out)
        with self.assertRaises(OutcomePresent):
            evaluate([_row("AL-02", 0.60, 0.40, y=1)], blocked, "rows-sha", "gate-sha")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            row_path = root / "rows.json"
            gate_path = root / "gate.json"
            row_path.write_text(json.dumps({"rows": [_row("AL-02", 0.60, 0.40, y=1)]}))
            gate_path.write_text(json.dumps(blocked))
            proc = subprocess.run(
                [sys.executable, "-m", "card01_amc.swing_stress", "--rows", str(row_path), "--gate", str(gate_path)],
                cwd=LAB,
                capture_output=True,
            )
        self.assertNotEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout, b"")

    def _strip_outcomes(self, rows, labels):
        stripped = []
        for row, y in zip(rows, labels):
            copied = dict(row)
            copied["y"] = y
            copied["result"] = "yes" if y else "no"
            for key in FORBIDDEN_OUTCOME_KEYS:
                copied.pop(key, None)
            stripped.append(copied)
        return stripped

    def test_label_permutation_is_invariant_and_source_does_not_subscript_y(self):
        base = [_row("AL-02", 0.55, 0.45), _row("OH-01", 0.40, 0.50), _row("NY-02", 0.70, 0.30)]
        labels_set = ((0, 1, 0), (1, 0, 1), (0, 0, 0), (1, 1, 1))
        blocked = {"status": "BLOCKED_FEE_UNVERIFIED", "signals": None, "reason": "MANIFEST_ABSENT"}
        dumps = []
        for labels in labels_set:
            stripped = self._strip_outcomes(base, labels)
            dumps.append(json.dumps(evaluate(stripped, blocked, "same", "same"), indent=1))
        self.assertEqual(len(set(dumps)), 1)

        signals = [
            _signal("AL-02", "D_YES", 0.42, 0.01),
            _signal("OH-01", "D_NO", 0.55, 0.02),
            _signal("NY-02", "D_YES", 0.40, 0.015),
        ]
        self.assertGreaterEqual(len(signals), 3)
        ok = _ok_gate(signals)
        ok_dumps = []
        for labels in labels_set:
            stripped = self._strip_outcomes(base, labels)
            ok_dumps.append(json.dumps(evaluate(stripped, ok, "same", "gate-sha", "gate-sha", **_admitted()), indent=1))
        self.assertEqual(len(set(ok_dumps)), 1)
        ok_obj = json.loads(ok_dumps[0])
        self.assertEqual(ok_obj["stress_status"], "OK")
        self.assertGreaterEqual(ok_obj["n_signals"], 3)

        self.assertIn("y", FORBIDDEN_OUTCOME_KEYS)
        tree = ast.parse((LAB / "card01_amc" / "swing_stress.py").read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Subscript):
                sl = node.slice
                if isinstance(sl, ast.Constant) and sl.value == "y":
                    self.fail("swing_stress subscripts y")
            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Attribute) and func.attr == "get":
                    for arg in list(node.args) + [kw.value for kw in node.keywords]:
                        if isinstance(arg, ast.Constant) and arg.value == "y":
                            self.fail("swing_stress calls .get('y')")
            if isinstance(node, ast.Dict):
                for key in node.keys:
                    if isinstance(key, ast.Constant) and key.value == "y":
                        self.fail("swing_stress uses y as a dict key")

    def test_formula_matches_pinned_stress_and_hash(self):
        from card01_amc.fee_admission import admit_fee_source_v2, pinned_entry_v2
        from card01_amc.fee_source import pinned_taker_fee
        from card01_amc.pinload import sha256_bytes
        from tests.test_fee_admission_v2 import ADMITTED_ID, _copy_kit

        pinned = load_national_miss()
        rows = [
            _row("AL-02", 0.62, 0.48),
            _row("OH-01", 0.41, 0.52),
            _row("NY-02", 0.73, 0.33),
        ]
        prices = (0.42, 0.55, 0.40)
        sides = ("D_YES", "D_NO", "D_YES")
        with tempfile.TemporaryDirectory() as tmp:
            paths = _copy_kit(Path(tmp))
            digest = sha256_bytes(paths[0].read_bytes())
            accept_sha = sha256_bytes(paths[1].read_bytes())
            admission = admit_fee_source_v2(
                fee_source_path=paths[0],
                fee_source_id=ADMITTED_ID,
                fee_source_sha256=digest,
                packet_index_path=paths[2],
                fee_accept_path=paths[1],
                series_used=["XS1"],
            )
            entry = pinned_entry_v2(admission, "XS1")
            signals = []
            for row, side, price in zip(rows, sides, prices):
                quoted = pinned_taker_fee(entry, price)
                signal = _signal(row["race_id"], side, price, 9.0, source=ADMITTED_ID)
                signal["fee_decimal"] = str(quoted["headline"])
                signal["fee_source_sha256"] = digest
                signal["series"] = "XS1"
                signals.append(signal)
            with_y = [dict(row, y=1) for row in rows]
            compare = []
            for signal, price in zip(signals, prices):
                quoted = pinned_taker_fee(entry, price)
                item = dict(signal)
                item["fee"] = float(quoted["headline"])
                compare.append(item)
            pinned_out = pinned.stress(with_y, compare)
            gate_doc = _ok_gate(signals)
            gate_doc["fee_source"] = ADMITTED_ID
            gate_doc["fee_source_sha256"] = digest
            gate_doc["fee_source_accept_sha256"] = accept_sha
            ours = evaluate(
                rows,
                gate_doc,
                "rows-sha",
                "gate-sha",
                "gate-sha",
                fee_source_path=paths[0],
                packet_index_path=paths[2],
                fee_accept_path=paths[1],
                fee_source_expected_sha256=digest,
                fee_source_expected_accept=accept_sha,
            )
        self.assertEqual(ours["stress_status"], "OK")
        frozen = [row for row in ours["rows"] if row["informational"] is False]
        self.assertEqual(len(frozen), len(pinned_out["rows"]))
        for got, exp in zip(frozen, pinned_out["rows"]):
            self.assertEqual(got["swing_logit"], exp["swing_logit"])
            self.assertEqual(got["expected_gross"], exp["expected_gross"])
            self.assertEqual(got["expected_net"], exp["expected_net"])
            self.assertEqual(got["n_sign_flips_vs_s0"], exp["n_sign_flips_vs_s0"])
            self.assertEqual(got["share_sign_flips_vs_s0"], exp["share_sign_flips_vs_s0"])
        info = [row for row in ours["rows"] if row["informational"] is True]
        self.assertEqual([row["swing_logit"] for row in info], [-1.0, 1.0])
        body = {k: v for k, v in ours.items() if k != "output_sha256"}
        digest = hashlib.sha256(json.dumps(body, indent=1).encode()).hexdigest()
        self.assertEqual(ours["output_sha256"], digest)

    def test_fragility_uses_half_logit_only(self):
        # p=0.8, price 0.65: ±0.5 stays positive; s=-1 flips.
        calm = evaluate(
            [_row("AL-02", 0.80, 0.80)],
            _ok_gate([_signal("AL-02", "D_YES", 0.65, 0.01)]),
            "a",
            "b",
            **_admitted(),
        )
        self.assertEqual(calm["fragility"], "NOT_FRAGILE_AT_PM0.5")
        halves = [r for r in calm["rows"] if r["swing_logit"] in (-0.5, 0.5)]
        infos = [r for r in calm["rows"] if r["informational"]]
        self.assertTrue(all(r["expected_gross"] > 0 and r["share_sign_flips_vs_s0"] < 0.5 for r in halves))
        self.assertTrue(any(r["share_sign_flips_vs_s0"] >= 0.5 or r["expected_gross"] <= 0 for r in infos))

        gross = evaluate(
            [_row("AL-02", 0.80, 0.80)],
            _ok_gate([_signal("AL-02", "D_YES", 0.90, 0.01)]),
            "a",
            "b",
            **_admitted(),
        )
        self.assertEqual(gross["fragility"], "FRAGILE_NATIONAL_SWING")
        self.assertTrue(any(r["swing_logit"] in (-0.5, 0.5) and r["expected_gross"] <= 0 for r in gross["rows"]))

        share_rows = [_row("AL-02", 0.90, 0.90), _row("OH-01", 0.50, 0.50)]
        share_signals = [
            _signal("AL-02", "D_YES", 0.20, 0.01),
            _signal("OH-01", "D_YES", 0.45, 0.01),
        ]
        share = evaluate(share_rows, _ok_gate(share_signals), "a", "b", **_admitted())
        self.assertEqual(share["fragility"], "FRAGILE_NATIONAL_SWING")
        minus = next(r for r in share["rows"] if r["swing_logit"] == -0.5)
        self.assertGreater(minus["expected_gross"], 0)
        self.assertGreaterEqual(minus["share_sign_flips_vs_s0"], 0.5)

    def test_status_vocabulary(self):
        rows = [_row("AL-02", 0.60, 0.40), _row("OH-01", 0.55, 0.45)]
        blocked = evaluate(
            rows,
            {"status": "BLOCKED_FEE_UNVERIFIED", "signals": None, "reason": "MANIFEST_ABSENT"},
            "r",
            "g",
        )
        self.assertEqual(blocked["stress_status"], "BLOCKED_FEE_UNVERIFIED")
        self.assertEqual(blocked["fragility"], "NOT_EVALUATED_FEE_BLOCKED")
        self.assertIsNone(blocked["rows"])

        empty = evaluate(rows, _ok_gate([]), "r", "g", **_admitted())
        # n_selected 0. _ok_gate([]) has n_selected 0 and signals [].
        self.assertEqual(empty["stress_status"], "NO_SIGNALS_SELECTED")
        self.assertIsNone(empty["fragility"])
        self.assertEqual(empty["gate_n_selected"], 0)
        self.assertIsNone(empty["rows"])

        missing = _ok_gate([])
        missing["n_selected"] = 2
        defect = evaluate(rows, missing, "r", "g", **_admitted())
        self.assertEqual(defect["stress_status"], "REPORTING_DEFECT")
        self.assertEqual(defect["fragility"], "FRAGILE_NOT_CLEARED_REPORTING_DEFECT")
        self.assertNotEqual(defect["fragility"], "NOT_FRAGILE_AT_PM0.5")

        unknown_race = _ok_gate([_signal("ZZ-99", "D_YES", 0.4, 0.01)])
        self.assertEqual(
            evaluate(rows, unknown_race, "r", "g", **_admitted())["stress_status"],
            "REPORTING_DEFECT",
        )

        null_model = [_row("AL-02", None, 0.40)]
        self.assertEqual(
            evaluate(null_model, _ok_gate([_signal("AL-02", "D_YES", 0.4, 0.01)]), "r", "g", **_admitted())["stress_status"],
            "REPORTING_DEFECT",
        )
        mismatch = evaluate(rows, _ok_gate([_signal("AL-02", "D_YES", 0.4, 0.01)]), "r", "abc", "deadbeef")
        self.assertEqual(mismatch["stress_status"], "REPORTING_DEFECT")
        self.assertEqual(mismatch["reason"], "GATE_SHA_MISMATCH")
        maybe = evaluate(rows, {"status": "MAYBE"}, "r", "g")
        self.assertEqual(maybe["stress_status"], "BLOCKED_FEE_UNVERIFIED")
        self.assertEqual(maybe["fee_block_reason"], "GATE_STATUS_NOT_OK")
        self.assertIsNone(maybe["rows"])
        missing_gate = evaluate(rows, None, "r", None)
        self.assertEqual(missing_gate["stress_status"], "BLOCKED_FEE_UNVERIFIED")
        self.assertEqual(missing_gate["fragility"], "NOT_EVALUATED_FEE_BLOCKED")
        self.assertEqual(missing_gate["fee_block_reason"], "GATE_MISSING")

        unsigned = evaluate(rows, _ok_gate([_signal("AL-02", "D_YES", 0.40, 0.01)]), "r", "gate-sha", **_admitted())
        self.assertEqual(unsigned["stress_status"], "OK")
        self.assertEqual(unsigned["net_block_reason"], "GATE_SHA_NOT_SUPPLIED")
        self.assertTrue(unsigned["rows"])
        for stress_row in unsigned["rows"]:
            self.assertEqual(stress_row["expected_net"], "BLOCKED_FEE_UNVERIFIED")
            self.assertEqual(stress_row["net_block_reason"], "GATE_SHA_NOT_SUPPLIED")
            self.assertIsInstance(stress_row["expected_gross"], float)
        self_certified = _ok_gate([_signal("AL-02", "D_YES", 0.40, 0.01)])
        self_certified["gate_sha256"] = "gate-sha"
        still = evaluate(rows, self_certified, "r", "gate-sha", **_admitted())
        self.assertEqual(still["net_block_reason"], "GATE_SHA_NOT_SUPPLIED")
        signed = evaluate(
            rows,
            _ok_gate([_signal("AL-02", "D_YES", 0.40, 0.01)]),
            "r",
            "gate-sha",
            "gate-sha",
            **_admitted(),
        )
        self.assertEqual(signed["net_block_reason"], "FEE_SOURCE_NOT_SUPPLIED")
        self.assertEqual(signed["rows"][0]["expected_net"], "BLOCKED_FEE_UNVERIFIED")
        self.assertNotIn("expected_net_sensitivity_direct_member", signed["rows"][0])

    def test_pinned_main_raises_without_outcomes(self):
        pinned = load_national_miss()
        doc = {
            "rows": [_row("AL-02", 0.6, 0.4, y=None)],
            "signals": [_signal("AL-02", "D_YES", 0.4, None)],
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "in.json"
            path.write_text(json.dumps(doc))
            with self.assertRaises(KeyError):
                pinned.main(str(path))


class FeeBlockTests(unittest.TestCase):
    def _row(self):
        return _row("AL-02", 0.70, 0.40)

    def test_gate_blocks_and_handmade_nets_stay_blocked(self):
        import json as _json
        from tests.support import sha256_bytes

        row = self._row()
        absent = gate([row])
        self.assertEqual(absent["reason"], "FEE_SOURCE_ABSENT")
        self.assertIsNone(absent["signals"])

        old = adopted_manifest()
        old["entries"]["KXHOUSERACE"]["entry_id"] = "ADDENDUM_02"
        old_bytes = _json.dumps(old).encode()
        sha_miss = gate([row], old_bytes)
        self.assertEqual(sha_miss["reason"], "FEE_SOURCE_NOT_ADMITTED_V1_ATTEST_FAIL")
        schema = gate(
            [row],
            old_bytes,
            expected_sha256=sha256_bytes(old_bytes),
            expected_accept="a" * 64,
        )
        self.assertEqual(schema["reason"], "FEE_SOURCE_NOT_ADMITTED_V1_ATTEST_FAIL")
        self.assertNotIn("FEE_ONLY_CEIL", schema)
        self.assertNotIn("fee_sensitivity_direct_member", schema)
        for result in (absent, sha_miss, schema):
            self.assertEqual(result["status"], "BLOCKED_FEE_UNVERIFIED")
            self.assertIsNone(result["signals"])
            stress = evaluate([row], result, "r", "g")
            self.assertEqual(stress["stress_status"], "BLOCKED_FEE_UNVERIFIED")
            self.assertIsNone(stress["rows"])

        price = 0.42
        handmade = [
            _signal("AL-02", "D_YES", price, 0.01, source=None),
            _signal("AL-02", "D_YES", price, 0.01, source="ADDENDUM_02"),
            _signal("AL-02", "D_YES", price, 0.01, source="DRAFT_NOT_ADOPTED"),
            _signal("AL-02", "D_YES", price, 0.01, source="unknown-entry"),
            _signal("AL-02", "D_YES", price, None, source="FEE_SOURCE_CARD01_v1"),
        ]
        for signal in handmade:
            signal = dict(signal)
            if signal["fee_source"] is None:
                del signal["fee_source"]
            legacy = {
                "status": "OK",
                "n_selected": 1,
                "signals": [signal],
                "fee_source": "FEE_SOURCE_CARD01_v1",
                "fee_source_sha256": "ab" * 32,
                "fee_attest_verdict": "ATTEST_PASS",
                "fee_attest_fee_source_sha256": "ab" * 32,
            }
            out = evaluate([row], legacy, "r", "g", "g")
            self.assertEqual(out["stress_status"], "BLOCKED_FEE_UNVERIFIED", signal)
            self.assertIsNone(out["rows"])
            self.assertEqual(out["fee_block_reason"], "FEE_SOURCE_NOT_ADMITTED_V1_ATTEST_FAIL")

    def test_source_has_no_unadopted_coefficient(self):
        for name in ("entry_gate.py", "swing_stress.py", "score.py"):
            text = (LAB / "card01_amc" / name).read_text()
            self.assertNotIn("0.07", text)


class JoinTests(unittest.TestCase):
    def test_sets_y_without_reordering(self):
        rows = [
            _row("AL-02", 0.5, 0.4),
            _row("OH-01", 0.5, 0.4),
            _row("NY-02", 0.5, 0.4),
        ]
        original = copy.deepcopy(rows)
        joined = join(rows, {"results": [
            {"ticker": "T-OH-01", "result": "no"},
            {"ticker": "T-AL-02", "result": "yes"},
            {"ticker": "T-NY-02", "result": "maybe"},
        ]})
        self.assertEqual([r["race_id"] for r in joined["rows"]], ["AL-02", "OH-01", "NY-02"])
        self.assertEqual(joined["rows"][0]["y"], 1)
        self.assertEqual(joined["rows"][1]["y"], 0)
        self.assertIsNone(joined["rows"][2]["y"])
        self.assertEqual(joined["rows"][0]["p_model"], original[0]["p_model"])
        self.assertIsNone(rows[0]["y"])
        conflict = join(rows, {"results": [
            {"ticker": "T-AL-02", "result": "yes"},
            {"ticker": "T-AL-02", "result": "no"},
        ]})
        self.assertIsNone(conflict["rows"][0]["y"])
        self.assertEqual(joined["ignored_results"], 0)

    def test_ignores_missing_or_empty_ticker(self):
        rows = [
            _row("AL-02", 0.5, 0.4),
            _row("OH-01", 0.5, 0.4),
        ]
        rows.append(dict(rows[0], race_id="TX-01", ticker=""))
        rows.append(dict(rows[0], race_id="CA-01", ticker=None))
        joined = join(rows, {"results": [
            {"result": "yes"},
            {"ticker": "", "result": "yes"},
            {"ticker": None, "result": "no"},
            {"ticker": "T-OH-01", "result": "no"},
        ]})
        self.assertEqual(joined["ignored_results"], 3)
        self.assertEqual(joined["rows"][0]["y"], None)
        self.assertEqual(joined["rows"][1]["y"], 0)
        self.assertIsNone(joined["rows"][2]["y"])
        self.assertIsNone(joined["rows"][3]["y"])
        self.assertEqual([r["race_id"] for r in joined["rows"]], ["AL-02", "OH-01", "TX-01", "CA-01"])


if __name__ == "__main__":
    unittest.main()
