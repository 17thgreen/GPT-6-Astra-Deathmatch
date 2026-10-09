"""astra.fee_source.v1 loader, pinned taker formula, and AF-4 block cases."""
from __future__ import annotations

import ast
import copy
import json
import tempfile
import tokenize
import unittest
from decimal import Decimal, ROUND_CEILING, InvalidOperation
from pathlib import Path

from card01_amc.entry_gate import gate
from card01_amc.fee_source import (
    CONDUCTOR_ACCEPT_SHA256,
    FEE_SOURCE_SHA256,
    FeeBlocked,
    PinnedEntry,
    load_fee_source,
    pinned_entry,
    pinned_taker_fee,
)
from card01_amc.swing_stress import evaluate
from tests.support import LAB, sha256_bytes

FIXTURE = LAB / "tests" / "fixtures" / "SYNTH_FEE_SOURCE_v1_example.json"


def synth_bytes() -> bytes:
    return FIXTURE.read_bytes()


def synth_overrides(raw: bytes) -> dict:
    doc = json.loads(raw)
    return {
        "expected_sha256": sha256_bytes(raw),
        "expected_id": doc["manifest_id"],
        "expected_accept": doc["conductor_accept_sha256"],
    }


def attest_pass(raw: bytes) -> dict:
    return {"fee_source_sha256": sha256_bytes(raw), "verdict": "ATTEST_PASS"}


def _row(series="KXHOUSERACE", **kwargs):
    row = {
        "race_id": "AL-02",
        "state": "AL",
        "mapping_status": "KXHOUSERACE" if series == "KXHOUSERACE" else "LEGACY",
        "series": series,
        "p_market": 0.25,
        "p_model": 0.90,
        "y": None,
        "ticker": "T-AL-02",
        "yes_bid": 0.20,
        "yes_ask": 0.30,
        "yes_bid_qty": 5,
        "yes_ask_qty": 5,
    }
    row.update(kwargs)
    return row


def _encode(doc) -> bytes:
    return json.dumps(doc).encode()


class FormulaTests(unittest.TestCase):
    def _entry(self, multiplier):
        return PinnedEntry(
            series="SYNTH",
            fee_type="quadratic",
            fee_multiplier=Decimal(multiplier),
            fee_multiplier_str=str(multiplier),
            fee_source="FEE_SOURCE_CARD01_v1",
            fee_source_sha256="ab" * 32,
            taker_rate="0.07",
        )

    def _fee(self, multiplier, price):
        return pinned_taker_fee(self._entry(multiplier), price)

    def test_documented_decimals(self):
        def ceil_to(value, quantum):
            return (value / quantum).to_integral_value(ROUND_CEILING) * quantum

        half = self._fee("1.5", Decimal("0.50"))
        self.assertEqual(half["raw"], Decimal("0.026250"))
        self.assertEqual(half["headline"], Decimal("0.03"))
        self.assertEqual(half["FEE_ONLY_CEIL"], Decimal("0.03"))
        self.assertEqual(half["sensitivity_direct_member"], Decimal("0.0263"))
        self.assertEqual(half["headline"], ceil_to(half["raw"], Decimal("0.01")))
        self.assertEqual(half["FEE_ONLY_CEIL"], ceil_to(half["raw"], Decimal("0.01")))

        small = self._fee("1", Decimal("0.07"))
        self.assertEqual(small["raw"], Decimal("0.004557"))
        self.assertEqual(small["headline"], Decimal("0.01"))
        self.assertEqual(small["FEE_ONLY_CEIL"], Decimal("0.01"))
        self.assertEqual(small["sensitivity_direct_member"], Decimal("0.0046"))
        self.assertEqual(small["headline"], ceil_to(small["raw"], Decimal("0.01")))

        sub = self._fee("1", Decimal("0.077"))
        self.assertEqual(sub["raw"], Decimal("0.004975"))
        self.assertEqual(sub["headline"], Decimal("0.013"))
        self.assertEqual(sub["FEE_ONLY_CEIL"], Decimal("0.01"))
        self.assertEqual(
            sub["headline"],
            ceil_to(Decimal("0.077") + sub["raw"], Decimal("0.01")) - Decimal("0.077"),
        )
        self.assertNotEqual(sub["headline"], sub["FEE_ONLY_CEIL"])

    def test_synthetic_source_splits_headline_from_fee_only_ceil(self):
        raw = synth_bytes()
        loaded = load_fee_source(raw, **synth_overrides(raw))
        entry = pinned_entry(loaded, "KXHOUSERACE")
        sub = pinned_taker_fee(entry, Decimal("0.077"))
        self.assertEqual(sub["headline"], Decimal("0.013"))
        self.assertEqual(sub["FEE_ONLY_CEIL"], Decimal("0.01"))
        whole = pinned_taker_fee(entry, Decimal("0.50"))
        self.assertEqual(whole["headline"], Decimal("0.03"))
        self.assertEqual(whole["FEE_ONLY_CEIL"], whole["headline"])

        off = _row(yes_bid=0.07, yes_ask=0.077, p_market=0.07, p_model=0.90)
        selected = gate([off], raw, fee_attest=attest_pass(raw), **synth_overrides(raw))
        self.assertEqual(selected["status"], "BLOCKED_FEE_UNVERIFIED")
        self.assertEqual(selected["reason"], "FEE_SOURCE_NOT_ADMITTED_V1_ATTEST_FAIL")
        self.assertIsNone(selected["signals"])
        blob = json.dumps(selected)
        self.assertNotIn("FEE_ONLY_CEIL", blob)
        self.assertNotIn("fee_sensitivity_direct_member", blob)

        from card01_amc import verdict
        self.assertNotIn("FEE_ONLY_CEIL", Path(verdict.__file__).read_text())

    def test_float_complement_matches_grid_price(self):
        floated = 1 - 0.43
        self.assertNotEqual(floated, 0.57)
        left = self._fee("1.5", floated)
        right = self._fee("1.5", Decimal("0.57"))
        self.assertEqual(left, right)

    def test_off_grid_price_is_blocked(self):
        with self.assertRaises(FeeBlocked) as caught:
            self._fee("1.5", Decimal("0.12345"))
        self.assertEqual(caught.exception.reason, "PRICE_NOT_ON_GRID")

    def test_rejects_non_entry(self):
        with self.assertRaises(TypeError):
            pinned_taker_fee({"taker_rate": "0.07"}, Decimal("0.50"))
        with self.assertRaises(TypeError):
            pinned_taker_fee({"series": "KXHOUSERACE"}, 0.5)


class LoadTests(unittest.TestCase):
    def test_real_constant_rejects_the_synthetic_file(self):
        with self.assertRaises(FeeBlocked) as caught:
            load_fee_source(synth_bytes())
        self.assertEqual(caught.exception.reason, "FEE_SOURCE_IDENTITY_MISSING")
        self.assertNotEqual(sha256_bytes(synth_bytes()), FEE_SOURCE_SHA256)
        self.assertEqual(len(CONDUCTOR_ACCEPT_SHA256), 64)
        with self.assertRaises(FeeBlocked) as refused:
            load_fee_source(
                synth_bytes(),
                expected_sha256=FEE_SOURCE_SHA256,
                expected_id="FEE_SOURCE_CARD01_v1",
                expected_accept=CONDUCTOR_ACCEPT_SHA256,
            )
        self.assertEqual(refused.exception.reason, "FEE_SOURCE_NOT_ADMITTED_V1_ATTEST_FAIL")
        self.assertFalse(hasattr(refused.exception, "headline"))

    def test_override_loads_and_pins_house_series(self):
        raw = synth_bytes()
        loaded = load_fee_source(raw, **synth_overrides(raw))
        entry = pinned_entry(loaded, "KXHOUSERACE")
        self.assertEqual(entry.fee_multiplier_str, "1.5")
        self.assertEqual(entry.fee_type, "quadratic")
        with self.assertRaises(FeeBlocked) as caught:
            pinned_entry(loaded, "HOUSEVA2")
        self.assertEqual(caught.exception.reason, "SERIES_NOT_PINNED")
        self.assertEqual(caught.exception.blocked_series, ["HOUSEVA2"])

    def _mutated(self, mutate):
        raw = synth_bytes()
        doc = json.loads(raw)
        mutate(doc)
        body = _encode(doc)
        overrides = {
            "expected_sha256": sha256_bytes(body),
            "expected_id": doc["manifest_id"],
            "expected_accept": doc["conductor_accept_sha256"],
        }
        return body, overrides, doc

    def test_status_anchor_accept_and_shape(self):
        body, overrides, _doc = self._mutated(lambda doc: doc.__setitem__("status", "DRAFT_NOT_ADOPTED"))
        with self.assertRaises(FeeBlocked) as caught:
            load_fee_source(body, **overrides)
        self.assertEqual(caught.exception.reason, "FEE_SOURCE_NOT_ADOPTED")

        body, overrides, _doc = self._mutated(lambda doc: doc.__setitem__("archivist_anchor_sha256", "ab" * 32))
        with self.assertRaises(FeeBlocked) as caught:
            load_fee_source(body, **overrides)
        self.assertEqual(caught.exception.reason, "ARCHIVIST_ANCHOR_IN_FILE")

        raw = synth_bytes()
        with self.assertRaises(FeeBlocked) as caught:
            load_fee_source(raw, expected_sha256=sha256_bytes(raw))
        self.assertEqual(caught.exception.reason, "FEE_SOURCE_IDENTITY_MISSING")

        body, overrides, _doc = self._mutated(lambda doc: doc["template"].__setitem__("is_template", True))
        with self.assertRaises(FeeBlocked) as caught:
            load_fee_source(body, **overrides)
        self.assertEqual(caught.exception.reason, "FEE_SOURCE_IS_TEMPLATE")

        body, overrides, _doc = self._mutated(lambda doc: doc["series"].pop("HOUSEVA2"))
        with self.assertRaises(FeeBlocked) as caught:
            load_fee_source(body, **overrides)
        self.assertEqual(caught.exception.reason, "SERIES_SET_MISMATCH")

    def test_card_blocks_on_any_bad_series(self):
        raw = synth_bytes()
        overrides = synth_overrides(raw)
        rows = [_row("KXHOUSERACE", race_id="AL-02"), _row("HOUSEVA2", race_id="VA-02")]
        loaded = load_fee_source(raw, **overrides)
        with self.assertRaises(FeeBlocked) as caught:
            pinned_entry(loaded, "HOUSEVA2")
        self.assertEqual(caught.exception.reason, "SERIES_NOT_PINNED")
        result = gate(rows, raw, fee_attest=attest_pass(raw), **overrides)
        self.assertEqual(result["status"], "BLOCKED_FEE_UNVERIFIED")
        self.assertIsNone(result["signals"])
        self.assertEqual(result["reason"], "FEE_SOURCE_NOT_ADMITTED_V1_ATTEST_FAIL")

        unknown = gate([_row("NOT-A-SERIES")], raw, fee_attest=attest_pass(raw), **overrides)
        self.assertEqual(unknown["reason"], "FEE_SOURCE_NOT_ADMITTED_V1_ATTEST_FAIL")
        self.assertIsNone(unknown["signals"])

    def test_entry_field_failures(self):
        cases = []

        def not_admitted(doc):
            doc["series"]["KXHOUSERACE"]["series_endpoint_source"]["admission"] = "NOT_ADMITTED"

        def series_list(doc):
            doc["series"]["KXHOUSERACE"]["series_endpoint_source"] = {"source_class": "SERIES_LIST"}

        def conflict(doc):
            doc["series"]["KXHOUSERACE"]["series_endpoint_source"]["fee_multiplier"] = "9"

        def maker(doc):
            doc["series"]["KXHOUSERACE"]["maker_taker_class"] = "MAKER"

        def rounding(doc):
            doc["series"]["KXHOUSERACE"]["rounding_rule"] = "PER_CONTRACT_CEIL_CENT"

        def null_mult(doc):
            doc["series"]["KXHOUSERACE"]["fee_multiplier"] = None
            doc["series"]["KXHOUSERACE"]["series_endpoint_source"]["fee_multiplier"] = None

        def zero_mult(doc):
            doc["series"]["KXHOUSERACE"]["fee_multiplier"] = "0"
            doc["series"]["KXHOUSERACE"]["series_endpoint_source"]["fee_multiplier"] = "0"

        def numeric_mult(doc):
            doc["series"]["KXHOUSERACE"]["fee_multiplier"] = 1.5
            doc["series"]["KXHOUSERACE"]["series_endpoint_source"]["fee_multiplier"] = 1.5

        def unpinned(doc):
            doc["series"]["KXHOUSERACE"]["series_status"] = "BLOCKED_FEE_UNVERIFIED"

        expected = [
            (not_admitted, "SERIES_ENDPOINT_NOT_ADMITTED"),
            (series_list, "SERIES_ENDPOINT_NOT_ADMITTED"),
            (conflict, "FEE_SOURCE_CONFLICT"),
            (maker, "TAKER_NOT_COVERED"),
            (rounding, "ROUNDING_RULE_UNSUPPORTED"),
            (null_mult, "FEE_TERMS_INVALID"),
            (zero_mult, "FEE_TERMS_INVALID"),
            (numeric_mult, "FEE_TERMS_INVALID"),
            (unpinned, "SERIES_NOT_PINNED"),
        ]
        for mutate, reason in expected:
            body, overrides, _doc = self._mutated(mutate)
            with self.assertRaises(FeeBlocked) as caught:
                pinned_entry(load_fee_source(body, **overrides), "KXHOUSERACE")
            self.assertEqual(caught.exception.reason, reason)
            result = gate([_row()], body, fee_attest=attest_pass(body), **overrides)
            self.assertEqual(result["status"], "BLOCKED_FEE_UNVERIFIED", reason)
            self.assertIsNone(result["signals"], reason)
            self.assertEqual(result["reason"], "FEE_SOURCE_NOT_ADMITTED_V1_ATTEST_FAIL")
            cases.append(reason)
        self.assertEqual(len(cases), len(expected))

    def test_positive_synthetic_gate(self):
        raw = synth_bytes()
        result = gate([_row()], raw, fee_attest=attest_pass(raw), **synth_overrides(raw))
        self.assertEqual(result["status"], "BLOCKED_FEE_UNVERIFIED")
        self.assertEqual(result["reason"], "FEE_SOURCE_NOT_ADMITTED_V1_ATTEST_FAIL")
        self.assertEqual(result["fee_source"], "FEE_SOURCE_CARD01_v1")
        self.assertEqual(result["fee_source_sha256"], sha256_bytes(raw))
        self.assertIsNone(result["signals"])
        self.assertNotIn("fee_attest_verdict", result)
        self.assertNotIn("FEE_ONLY_CEIL", result)
        self.assertNotIn("fee_sensitivity_direct_member", result)

    def test_attest_blocks_unless_pass_matches_the_fee_sha(self):
        from card01_amc.verdict import apply_verdict

        raw = synth_bytes()
        overrides = synth_overrides(raw)
        digest = sha256_bytes(raw)
        row = _row()
        missing = gate([row], raw, **overrides)
        mismatched = gate(
            [row],
            raw,
            fee_attest={"fee_source_sha256": "ab" * 32, "verdict": "ATTEST_PASS"},
            **overrides,
        )
        failed = gate(
            [row],
            raw,
            fee_attest={"fee_source_sha256": digest, "verdict": "ATTEST_FAIL"},
            **overrides,
        )
        other = gate(
            [row],
            raw,
            fee_attest={"fee_source_sha256": digest, "verdict": "ATTEST_PENDING"},
            **overrides,
        )
        self.assertEqual(missing["reason"], "FEE_SOURCE_NOT_ADMITTED_V1_ATTEST_FAIL")
        self.assertEqual(mismatched["reason"], "FEE_SOURCE_NOT_ADMITTED_V1_ATTEST_FAIL")
        self.assertEqual(failed["reason"], "FEE_SOURCE_NOT_ADMITTED_V1_ATTEST_FAIL")
        self.assertEqual(other["reason"], "FEE_SOURCE_NOT_ADMITTED_V1_ATTEST_FAIL")
        score = {
            "all_admitted": {
                "n": 2,
                "states": 2,
                "arms": {"0.5": {"CI95_D_raw": [-0.02, -0.01], "CI95_D_rc": [-0.03, -0.01]}},
            }
        }
        for blocked in (missing, mismatched, failed, other):
            self.assertEqual(blocked["status"], "BLOCKED_FEE_UNVERIFIED")
            self.assertIsNone(blocked["signals"])
            stress = evaluate([row], blocked, "r", "g")
            self.assertEqual(stress["stress_status"], "BLOCKED_FEE_UNVERIFIED")
            self.assertIsNone(stress["rows"])
            verdict = apply_verdict(score, gate=blocked)
            self.assertTrue(verdict["verdict"].startswith("FORECAST_ONLY_FEE_BLOCKED"))
            self.assertEqual(verdict["fee_state"], "BLOCKED_FEE_UNVERIFIED")

        admitted = gate([row], raw, fee_attest=attest_pass(raw), **overrides)
        self.assertEqual(admitted["status"], "BLOCKED_FEE_UNVERIFIED")
        self.assertIsNone(admitted["signals"])
        self.assertNotIn("fee_attest_verdict", admitted)

    def test_unknown_schema_version_fails_closed(self):
        body, overrides, _doc = self._mutated(lambda doc: doc.__setitem__("schema", "astra.fee_source.v2"))
        with self.assertRaises(FeeBlocked) as caught:
            load_fee_source(body, **overrides)
        self.assertEqual(caught.exception.reason, "FEE_SOURCE_VERSION_UNSUPPORTED")
        blocked = gate([_row()], body, fee_attest=attest_pass(body), **overrides)
        self.assertEqual(blocked["status"], "BLOCKED_FEE_UNVERIFIED")
        self.assertEqual(blocked["reason"], "FEE_SOURCE_NOT_ADMITTED_V1_ATTEST_FAIL")
        self.assertIsNone(blocked["signals"])

        body, overrides, _doc = self._mutated(lambda doc: doc.__setitem__("version", "v2"))
        with self.assertRaises(FeeBlocked) as caught:
            load_fee_source(body, **overrides)
        self.assertEqual(caught.exception.reason, "FEE_SOURCE_VERSION_UNSUPPORTED")

    def test_m1_headline_can_sit_below_fee_only_ceil(self):
        def set_m1(doc):
            entry = doc["series"]["KXHOUSERACE"]
            entry["fee_multiplier"] = "1"
            entry["series_endpoint_source"]["fee_multiplier"] = "1"

        body, overrides, _doc = self._mutated(set_m1)
        loaded = load_fee_source(body, **overrides)
        entry = pinned_entry(loaded, "KXHOUSERACE")
        self.assertEqual(entry.fee_multiplier, Decimal("1"))
        self.assertEqual(entry.fee_type, "quadratic")
        expected = (
            (Decimal("0.055"), Decimal("0.005"), Decimal("0.01")),
            (Decimal("0.072"), Decimal("0.008"), Decimal("0.01")),
            (Decimal("0.077"), Decimal("0.013"), Decimal("0.01")),
            (Decimal("0.50"), Decimal("0.02"), Decimal("0.02")),
        )
        for price, headline, fee_only in expected:
            quoted = pinned_taker_fee(entry, price)
            self.assertEqual(quoted["headline"], headline, price)
            self.assertEqual(quoted["FEE_ONLY_CEIL"], fee_only, price)
        low = pinned_taker_fee(entry, Decimal("0.055"))
        self.assertLess(low["headline"], low["FEE_ONLY_CEIL"])


class RateScanTests(unittest.TestCase):
    def test_rate_literal_is_only_inside_the_formula(self):
        hits = []
        root = LAB / "card01_amc"
        for path in sorted(root.glob("*.py")):
            span = _formula_span(path)
            with path.open("rb") as handle:
                for tok in tokenize.tokenize(handle.readline):
                    if not _is_rate_token(tok):
                        continue
                    inside = (
                        path.name == "fee_source.py"
                        and span is not None
                        and span[0] <= tok.start[0] <= span[1]
                    )
                    hits.append((path.name, tok.start[0], inside, tok.string))
        self.assertTrue(hits)
        self.assertTrue(all(item[2] for item in hits), hits)
        self.assertEqual({item[0] for item in hits}, {"fee_source.py"})


def _formula_span(path: Path):
    tree = ast.parse(path.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "pinned_taker_fee":
            return node.lineno, node.end_lineno
    return None


def _is_rate_token(tok) -> bool:
    if tok.type == tokenize.NUMBER:
        try:
            return Decimal(tok.string) == Decimal("0.07")
        except InvalidOperation:
            return False
    if tok.type == tokenize.STRING:
        try:
            value = ast.literal_eval(tok.string)
        except (SyntaxError, ValueError):
            return False
        if isinstance(value, str):
            try:
                return Decimal(value) == Decimal("0.07")
            except InvalidOperation:
                return False
    return False


class SwingRecomputeTests(unittest.TestCase):
    def test_forged_fee_and_positive_recompute(self):
        raw = synth_bytes()
        overrides = synth_overrides(raw)
        loaded = load_fee_source(raw, **overrides)
        entry = pinned_entry(loaded, "KXHOUSERACE")
        quoted = pinned_taker_fee(entry, Decimal("0.42"))
        row = _row()
        good = {
            "race_id": "AL-02",
            "side": "D_YES",
            "price": 0.42,
            "fee": float(quoted["headline"]),
            "fee_decimal": str(quoted["headline"]),
            "series": "KXHOUSERACE",
            "fee_source": loaded.manifest_id,
            "fee_source_sha256": loaded.sha256,
        }
        gate_doc = {
            "status": "OK",
            "n_selected": 1,
            "signals": [good],
            "fee_source": loaded.manifest_id,
            "fee_source_sha256": loaded.sha256,
        }
        kwargs = {
            "fee_source_expected_sha256": overrides["expected_sha256"],
            "fee_source_expected_accept": overrides["expected_accept"],
        }
        blocked = evaluate([row], gate_doc, "r", "g", "g", raw, **kwargs)
        self.assertEqual(blocked["stress_status"], "BLOCKED_FEE_UNVERIFIED")
        self.assertIsNone(blocked["rows"])
        self.assertEqual(blocked["fee_block_reason"], "FEE_SOURCE_NOT_ADMITTED_V1_ATTEST_FAIL")
        self.assertEqual(blocked["fee_source"], loaded.manifest_id)
        self.assertEqual(blocked["fee_source_sha256"], loaded.sha256)

        from card01_amc.entry_gate import gate_v2
        from card01_amc.fee_admission import FEE_FORMULA_ID
        from tests.test_fee_admission_v2 import ADMITTED_ID, _copy_kit, _row as fee_row

        with tempfile.TemporaryDirectory() as tmp:
            paths = _copy_kit(Path(tmp))
            digest = sha256_bytes(paths[0].read_bytes())
            accept_sha = sha256_bytes(paths[1].read_bytes())
            book = fee_row()
            admitted_gate = gate_v2(
                [book],
                fee_source_path=paths[0],
                fee_source_id=ADMITTED_ID,
                fee_source_sha256=digest,
                packet_index_path=paths[2],
                fee_accept_path=paths[1],
            )
            self.assertEqual(admitted_gate["status"], "OK")
            headline = Decimal(admitted_gate["signals"][0]["fee_decimal"])
            out = evaluate(
                [book],
                admitted_gate,
                "r",
                "g",
                "g",
                fee_source_path=paths[0],
                packet_index_path=paths[2],
                fee_accept_path=paths[1],
                fee_source_expected_sha256=digest,
                fee_source_expected_accept=accept_sha,
                fee_source_expected_formula=FEE_FORMULA_ID,
            )
            self.assertEqual(out["stress_status"], "OK")
            self.assertNotIn("net_block_reason", out)
            self.assertIsInstance(out["rows"][0]["expected_net"], float)
            gross = out["rows"][0]["expected_gross"]
            self.assertEqual(out["rows"][0]["expected_net"], gross - float(headline))
            forged = copy.deepcopy(admitted_gate)
            forged["signals"][0]["fee_decimal"] = "0.99"
            forged["signals"][0]["fee"] = 0.99
            bad = evaluate(
                [book],
                forged,
                "r",
                "g",
                "g",
                fee_source_path=paths[0],
                packet_index_path=paths[2],
                fee_accept_path=paths[1],
                fee_source_expected_sha256=digest,
                fee_source_expected_accept=accept_sha,
                fee_source_expected_formula=FEE_FORMULA_ID,
            )
        self.assertEqual(bad["stress_status"], "BLOCKED_FEE_UNVERIFIED")
        self.assertEqual(bad["fee_block_reason"], "GATE_NOT_REPRODUCED")
        self.assertIsNone(bad["rows"])
        self.assertEqual(bad["reporting_defects"][0]["kind"], "GATE_NOT_REPRODUCED")

    def test_handmade_ok_gate_without_attestation_is_blocked(self):
        raw = synth_bytes()
        overrides = synth_overrides(raw)
        loaded = load_fee_source(raw, **overrides)
        entry = pinned_entry(loaded, "KXHOUSERACE")
        quoted = pinned_taker_fee(entry, Decimal("0.42"))
        row = _row()
        gate_doc = {
            "status": "OK",
            "n_selected": 1,
            "signals": [{
                "race_id": "AL-02",
                "side": "D_YES",
                "price": 0.42,
                "fee": float(quoted["headline"]),
                "fee_decimal": str(quoted["headline"]),
                "series": "KXHOUSERACE",
                "fee_source": loaded.manifest_id,
                "fee_source_sha256": loaded.sha256,
            }],
            "fee_source": loaded.manifest_id,
            "fee_source_sha256": loaded.sha256,
        }
        self.assertNotIn("fee_attest_verdict", gate_doc)
        self.assertNotIn("fee_attest_fee_source_sha256", gate_doc)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "gate.json"
            path.write_text(json.dumps(gate_doc))
            handmade = json.loads(path.read_text())
        out = evaluate(
            [row],
            handmade,
            "r",
            "g",
            "g",
            raw,
            fee_source_expected_sha256=overrides["expected_sha256"],
            fee_source_expected_accept=overrides["expected_accept"],
        )
        self.assertEqual(out["stress_status"], "BLOCKED_FEE_UNVERIFIED")
        self.assertEqual(out["fragility"], "NOT_EVALUATED_FEE_BLOCKED")
        self.assertIsNone(out["rows"])
        self.assertEqual(out["fee_source"], loaded.manifest_id)
        self.assertEqual(out["fee_source_sha256"], loaded.sha256)


if __name__ == "__main__":
    unittest.main()
