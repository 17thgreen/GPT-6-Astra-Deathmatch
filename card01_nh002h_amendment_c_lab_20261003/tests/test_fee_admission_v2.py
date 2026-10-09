"""v2 index-only fee admission and the headline gate. Synthetic fixtures only."""
from __future__ import annotations

import ast
import copy
import json
import os
import unittest
from decimal import Decimal
from pathlib import Path

from card01_amc.entry_gate import gate, gate_v2
from card01_amc.fee_admission import (
    FEE_FORMULA_ID,
    admit_fee_source_v2,
    pinned_entry_v2,
)
from card01_amc.fee_source import FeeBlocked, PinnedEntry, pinned_taker_fee
from card01_amc.pinload import sha256_bytes
from tests.support import LAB

FIXTURES = LAB / "tests" / "fixtures"
FEE_NAME = "SYNTH_FEE_SOURCE_v2_example.json"
ACCEPT_NAME = "SYNTH_CONDUCTOR_ACCEPT_FEE_FILL.json"
INDEX_NAME = "SYNTH_PACKET_INDEX_excerpt.md"
EXPECTED = json.loads((FIXTURES / "SYNTH_R1_EXPECTED_VALUES.json").read_text())
RETIRED = (
    "PENDING_ADOPTION_RULE_AMENDMENT",
    "FEE_ATTESTATION_MISSING",
    "FEE_REATTEST_NOT_PASS",
)
FORMULA_MISMATCH = "FEE_FORMULA_ID_MISMATCH"
ADMITTED_ID = "FEE_SOURCE_SYNTH_v2"


def _no_fee_numbers(obj):
    """True when no headline, net, or gross number is present."""
    banned = {
        "fee_headline",
        "fee_decimal",
        "fee_only_ceil",
        "fee_direct_0001",
        "net_headline",
        "net_fees_2x",
        "net_fee_only_ceil",
        "net_direct_0001",
        "gross",
        "expected_net",
        "expected_net_gate",
    }

    def walk(node):
        if isinstance(node, dict):
            for key, val in node.items():
                if key in banned and isinstance(val, (int, float)):
                    return False
                if key in banned and isinstance(val, str):
                    try:
                        Decimal(val)
                    except Exception:
                        pass
                    else:
                        if val not in ("BLOCKED_FEE_UNVERIFIED",):
                            return False
                if not walk(val):
                    return False
        elif isinstance(node, list):
            for item in node:
                if not walk(item):
                    return False
        return True

    return obj.get("signals") is None and walk(obj)


def _copy_kit(tmp: Path):
    fee = (FIXTURES / FEE_NAME).read_bytes()
    accept = (FIXTURES / ACCEPT_NAME).read_bytes()
    index = (FIXTURES / INDEX_NAME).read_bytes()
    fee_path = tmp / "fee.json"
    accept_path = tmp / "accept.json"
    index_path = tmp / "index.md"
    fee_path.write_bytes(fee)
    accept_path.write_bytes(accept)
    index_path.write_bytes(index)
    return fee_path, accept_path, index_path


def _repin(tmp: Path, doc, accept_fill_sha=None, adopted_phrase=None):
    fee_path = tmp / "fee.json"
    accept_path = tmp / "accept.json"
    index_path = tmp / "index.md"
    fee_bytes = json.dumps(doc).encode()
    fee_path.write_bytes(fee_bytes)
    fee_sha = sha256_bytes(fee_bytes)
    accept = json.loads(accept_path.read_bytes()) if accept_path.is_file() else {}
    if not isinstance(accept, dict):
        accept = {}
    accept.setdefault("accepted", {})
    accept["accepted"]["fill_sha256"] = fee_sha if accept_fill_sha is None else accept_fill_sha
    accept_bytes = json.dumps(accept).encode()
    accept_path.write_bytes(accept_bytes)
    accept_sha = sha256_bytes(accept_bytes)
    phrase = adopted_phrase
    if phrase is None:
        phrase = "**ADOPTED (anchor) by Conductor ACCEPT " + accept_sha + "**"
    text = (
        "# SYNTHETIC PACKET_INDEX excerpt\n\n"
        "| File | sha256 |\n"
        "|---|---|\n"
        "| `registry/SYNTH_FEE_SOURCE_v2_example.json` (SYNTHETIC v2 fill; "
        + phrase
        + ") | `"
        + fee_sha
        + "` |\n"
        "| `packets/SYNTH_CONDUCTOR_ACCEPT_FEE_FILL.json` "
        "(SYNTHETIC Conductor fill ACCEPT) | `"
        + accept_sha
        + "` |\n"
        "| `registry/SYNTH_FEE_SOURCE_v1_historical.json` "
        "(SYNTHETIC v1, HISTORICAL; deny-listed) | "
        "`d4dc8e72ae2b2a72824487eb386d6684c451a5e3b2e9dce58c1a68aaea9436cd` |\n"
    )
    index_path.write_text(text)
    return fee_path, accept_path, index_path, fee_sha


def _admit(paths, series=("XS1",), **kwargs):
    fee_path, accept_path, index_path = paths[:3]
    fee_sha = kwargs.pop("fee_sha", None)
    if fee_sha is None:
        fee_sha = sha256_bytes(fee_path.read_bytes())
    fee_id = kwargs.pop("fee_id", ADMITTED_ID)
    return admit_fee_source_v2(
        fee_source_path=kwargs.pop("fee_source_path", fee_path),
        fee_source_id=fee_id,
        fee_source_sha256=fee_sha,
        packet_index_path=kwargs.pop("packet_index_path", index_path),
        fee_accept_path=kwargs.pop("fee_accept_path", accept_path),
        series_used=list(series),
        **kwargs,
    )


def _row(race_id="G1-01", **kwargs):
    row = {
        "race_id": race_id,
        "state": "XA",
        "mapping_status": "KXHOUSERACE",
        "series": "XS1",
        "p_model": 0.176,
        "p_market": 0.05,
        "y": None,
        "yes_bid": 0.05,
        "yes_ask": 0.055,
        "yes_bid_qty": 5,
        "yes_ask_qty": 5,
    }
    row.update(kwargs)
    return row


class AdmissionTests(unittest.TestCase):
    def test_t20_admitted_index_only(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            paths = _copy_kit(Path(tmp))
            admission = _admit(paths)
            self.assertEqual(admission.fee_admission, "ADMITTED_INDEX_ONLY")
            self.assertEqual(admission.adoption_mode, "INDEX_ONLY")
            self.assertEqual(admission.fee_formula_id, FEE_FORMULA_ID)
            self.assertEqual(admission.sensitivity_rows_status, "SENSITIVITY_BASIS_INCOMPLETE")
            record = admission.public_dict()
            for key in (
                "fee_source_accept_sha256",
                "packet_index_sha256_at_run",
                "fee_admission_rule_sha256",
                "fee_attestation_sha256",
                "fee_attestation_result",
                "fee_attestation_scope",
                "series_used",
                "fee_source_attestation",
            ):
                self.assertIn(key, record)
                self.assertIsNotNone(record[key], key)
            self.assertEqual(record["fee_attestation_result"], "ATTEST_PASS")
            self.assertEqual(record["fee_attestation_scope"], "HEADLINE_FEE_SOURCE_ONLY")
            entry = pinned_entry_v2(admission, "XS1")
            for price, headline in (
                (Decimal("0.055"), Decimal("0.005")),
                (Decimal("0.072"), Decimal("0.008")),
                (Decimal("0.077"), Decimal("0.013")),
            ):
                self.assertEqual(pinned_taker_fee(entry, price)["headline"], headline)
            gated = gate_v2(
                [_row()],
                fee_source_path=paths[0],
                fee_source_id=ADMITTED_ID,
                fee_source_sha256=sha256_bytes(paths[0].read_bytes()),
                packet_index_path=paths[2],
                fee_accept_path=paths[1],
            )
            self.assertEqual(gated["status"], "OK")
            self.assertEqual(gated["fee_admission"], "ADMITTED_INDEX_ONLY")
            self.assertEqual(gated["signals"][0]["fee_decimal"], "0.005")
            self.assertEqual(gated["sensitivity_rows_status"], "SENSITIVITY_BASIS_INCOMPLETE")

    def test_t15_v1_refused_and_no_admitted_constant(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            paths = _copy_kit(Path(tmp))
            doc = json.loads(paths[0].read_bytes())
            doc["status"] = "ADOPTED"
            fee_path, accept_path, index_path, fee_sha = _repin(Path(tmp), doc)
            by_sha = _admit((fee_path, accept_path, index_path), fee_sha="d4dc8e72ae2b2a72824487eb386d6684c451a5e3b2e9dce58c1a68aaea9436cd")
            self.assertEqual(by_sha.fee_admission, "BLOCKED_FEE_UNVERIFIED")
            self.assertEqual(by_sha.fee_block_reason, "FEE_SOURCE_NOT_ADMITTED_V1_ATTEST_FAIL")
            self.assertIsNone(by_sha.amendment_check_failed)
            by_id = _admit((fee_path, accept_path, index_path), fee_id="FEE_SOURCE_CARD01_v1", fee_sha=fee_sha)
            self.assertEqual(by_id.fee_block_reason, "FEE_SOURCE_NOT_ADMITTED_V1_ATTEST_FAIL")
        banned_prefix = "6edc3eff"
        banned_id = "FEE_SOURCE_CARD01_v2"
        for path in (LAB / "card01_amc").glob("*.py"):
            text = path.read_text()
            self.assertNotIn(banned_prefix, text, path.name)
            self.assertNotIn(banned_id, text, path.name)

    def test_t19_draft_in_file_is_admitted_and_formula_scope_anchor(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = _copy_kit(root)
            doc = json.loads(paths[0].read_bytes())
            self.assertEqual(doc["status"], "DRAFT_NOT_ADOPTED")
            self.assertIsNone(doc["conductor_accept_sha256"])
            admitted = _admit(paths)
            self.assertEqual(admitted.fee_admission, "ADMITTED_INDEX_ONLY")

            bad_formula = copy.deepcopy(doc)
            bad_formula["fee_computation"]["headline"]["formula_id"] = (
                "astra.r1p1.feebook.claude_order_level_ceil.v1"
            )
            fee_path, accept_path, index_path, fee_sha = _repin(root, bad_formula)
            mismatch = _admit((fee_path, accept_path, index_path), fee_sha=fee_sha)
            self.assertEqual(mismatch.fee_block_reason, FORMULA_MISMATCH)
            self.assertEqual(mismatch.fee_admission, "BLOCKED_FEE_UNVERIFIED")

            sell = copy.deepcopy(doc)
            sell["fee_computation"]["headline"]["applies_to"] = dict(
                sell["fee_computation"]["headline"]["applies_to"]
            )
            sell["fee_computation"]["headline"]["applies_to"]["side"] = "SELL"
            fee_path, accept_path, index_path, fee_sha = _repin(root, sell)
            scope = _admit((fee_path, accept_path, index_path), fee_sha=fee_sha)
            self.assertEqual(scope.fee_block_reason, "HEADLINE_SCOPE_MISMATCH")

            paths = _copy_kit(root)
            index = paths[2].read_text().replace(
                "9d9da1c4e2c593cfa762701eef973c2a3538bd74410097fbcff20673b884c5b8",
                "ab" * 32,
                1,
            )
            paths[2].write_text(index)
            orphan = _admit(paths)
            self.assertEqual(orphan.fee_block_reason, "FEE_SOURCE_NOT_ANCHORED")
            self.assertEqual(orphan.amendment_check_failed, "a")

    def test_t21a_check_a_alone(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = _copy_kit(root)
            original = paths[0].read_bytes()
            paths[0].write_bytes(original[:-1] + bytes([original[-1] ^ 0x01]))
            rehash = _admit(paths, fee_sha=sha256_bytes(original))
            self.assertEqual(rehash.fee_block_reason, "FEE_SOURCE_REHASH_MISMATCH")
            self.assertEqual(rehash.amendment_check_failed, "a")
            self.assertTrue(_no_fee_numbers(rehash.public_dict()))

            paths = _copy_kit(root)
            text = paths[2].read_text().replace(sha256_bytes(paths[0].read_bytes()), "cd" * 32)
            paths[2].write_text(text)
            anchor = _admit(paths)
            self.assertEqual(anchor.fee_block_reason, "FEE_SOURCE_NOT_ANCHORED")
            self.assertEqual(anchor.amendment_check_failed, "a")

            missing = _admit(paths, fee_source_path=root / "missing.json")
            self.assertEqual(missing.fee_block_reason, "FEE_SOURCE_PAIR_MISSING")
            self.assertEqual(missing.amendment_check_failed, "a")
            self.assertEqual(missing.fee_block_detail, "fee_source_path")

    def test_t21b_check_b_alone(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = json.loads((FIXTURES / FEE_NAME).read_bytes())
            fee_path, accept_path, index_path, fee_sha = _repin(
                root, doc, adopted_phrase="not an adoption row"
            )
            plain = _admit((fee_path, accept_path, index_path), fee_sha=fee_sha)
            self.assertEqual(plain.fee_block_reason, "FEE_SOURCE_STATUS_NOT_ADOPTED")
            self.assertEqual(plain.amendment_check_failed, "b")

            fee_path, accept_path, index_path, fee_sha = _repin(
                root, doc, adopted_phrase="**ADOPTED (anchor)** with no citation"
            )
            bare = _admit((fee_path, accept_path, index_path), fee_sha=fee_sha)
            self.assertEqual(bare.fee_block_reason, "FEE_SOURCE_STATUS_NOT_ADOPTED")

            fee_path, accept_path, index_path, fee_sha = _repin(root, doc)
            accept_path.unlink()
            absent = _admit((fee_path, accept_path, index_path), fee_sha=fee_sha)
            self.assertEqual(absent.fee_block_reason, "FEE_ACCEPT_MISSING")
            self.assertEqual(absent.amendment_check_failed, "b")

            fee_path, accept_path, index_path, fee_sha = _repin(root, doc)
            accept_path.write_bytes(accept_path.read_bytes() + b" ")
            bad_bytes = _admit((fee_path, accept_path, index_path), fee_sha=fee_sha)
            self.assertEqual(bad_bytes.fee_block_reason, "FEE_ACCEPT_REHASH_MISMATCH")

            fee_path, accept_path, index_path, fee_sha = _repin(root, doc, accept_fill_sha="ab" * 32)
            # _repin wrote the wrong fill sha, then hashed that accept. The index
            # cites that accept sha, so (b) reaches the fill_sha256 compare.
            wrong_fill = _admit((fee_path, accept_path, index_path), fee_sha=fee_sha)
            self.assertEqual(wrong_fill.fee_block_reason, "FEE_ACCEPT_REHASH_MISMATCH")
            self.assertEqual(wrong_fill.amendment_check_failed, "b")
            self.assertTrue(_no_fee_numbers(wrong_fill.public_dict()))

    def test_t21c_check_c_alone(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = json.loads((FIXTURES / FEE_NAME).read_bytes())
            adopted = copy.deepcopy(doc)
            adopted["status"] = "ADOPTED"
            fee_path, accept_path, index_path, fee_sha = _repin(root, adopted)
            status = _admit((fee_path, accept_path, index_path), fee_sha=fee_sha)
            self.assertEqual(status.fee_block_reason, "FEE_SOURCE_IN_FILE_UNEXPECTED")
            self.assertEqual(status.amendment_check_failed, "c")

            cited = copy.deepcopy(doc)
            cited["conductor_accept_sha256"] = "ab" * 32
            fee_path, accept_path, index_path, fee_sha = _repin(root, cited)
            accept_field = _admit((fee_path, accept_path, index_path), fee_sha=fee_sha)
            self.assertEqual(accept_field.fee_block_reason, "FEE_SOURCE_IN_FILE_UNEXPECTED")

            anchored = copy.deepcopy(doc)
            anchored["archivist_anchor_sha256"] = "cd" * 32
            fee_path, accept_path, index_path, fee_sha = _repin(root, anchored)
            anchor_field = _admit((fee_path, accept_path, index_path), fee_sha=fee_sha)
            self.assertEqual(anchor_field.fee_block_reason, "FEE_SOURCE_IN_FILE_UNEXPECTED")
            self.assertEqual(anchor_field.amendment_check_failed, "c")

            original_sha = sha256_bytes((FIXTURES / FEE_NAME).read_bytes())
            fee_path.write_bytes(json.dumps(adopted).encode())
            stale = _admit((fee_path, accept_path, index_path), fee_sha=original_sha)
            self.assertEqual(stale.fee_block_reason, "FEE_SOURCE_REHASH_MISMATCH")
            self.assertEqual(stale.amendment_check_failed, "a")

    def test_t21d_check_d_alone(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = _copy_kit(root)
            blocked = _admit(paths, series=("XS3",))
            self.assertEqual(blocked.fee_block_reason, "SERIES_NOT_PINNED")
            self.assertEqual(list(blocked.blocked_series), ["XS3"])
            self.assertEqual(blocked.amendment_check_failed, "d")
            self.assertTrue(_no_fee_numbers(blocked.public_dict()))

            both = _admit(paths, series=("XS1", "XS3"))
            self.assertEqual(both.fee_block_reason, "SERIES_NOT_PINNED")
            self.assertEqual(list(both.blocked_series), ["XS3"])

            for kwargs in (
                {"side": "SELL"},
                {"taker_maker_role": "MAKER"},
                {"fill_model": "MULTI_FILL_ACCUMULATOR"},
            ):
                trade = _admit(paths, **kwargs)
                self.assertEqual(trade.fee_block_reason, "HEADLINE_SCOPE_MISMATCH", kwargs)
                self.assertEqual(trade.amendment_check_failed, "d")

            doc = json.loads(paths[0].read_bytes())
            doc["series"]["XS1"]["fee_type"] = "flat"
            doc["series"]["XS1"]["series_endpoint_source"]["fee_type"] = "flat"
            fee_path, accept_path, index_path, fee_sha = _repin(root, doc)
            flat = _admit((fee_path, accept_path, index_path), fee_sha=fee_sha)
            self.assertEqual(flat.fee_block_reason, "HEADLINE_SCOPE_MISMATCH")
            self.assertEqual(flat.amendment_check_failed, "d")

    def test_t22_multiplier_not_one(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = json.loads((FIXTURES / FEE_NAME).read_bytes())
            doc["series"]["XS1"]["fee_multiplier"] = "1.5"
            doc["series"]["XS1"]["series_endpoint_source"]["fee_multiplier"] = "1.5"
            fee_path, accept_path, index_path, fee_sha = _repin(root, doc)
            admission = _admit((fee_path, accept_path, index_path), fee_sha=fee_sha)
            self.assertEqual(admission.fee_admission, "BLOCKED_FEE_UNVERIFIED")
            self.assertEqual(admission.fee_block_reason, "HEADLINE_SCOPE_MISMATCH")
            self.assertEqual(admission.fee_block_detail, "FEE_MULTIPLIER_NOT_1")
            self.assertTrue(_no_fee_numbers(admission.public_dict()))

    def test_t23_retired_strings_absent_from_gate_cases(self):
        import tempfile
        texts = []
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = _copy_kit(root)
            cases = [_admit(paths)]
            doc = json.loads(paths[0].read_bytes())
            doc["series"]["XS1"]["fee_multiplier"] = "1.5"
            doc["series"]["XS1"]["series_endpoint_source"]["fee_multiplier"] = "1.5"
            fee_path, accept_path, index_path, fee_sha = _repin(root, doc)
            cases.append(_admit((fee_path, accept_path, index_path), fee_sha=fee_sha))
            paths = _copy_kit(root)
            cases.append(_admit(paths, series=("XS3",)))
            for admission in cases:
                blob = json.dumps(admission.public_dict())
                texts.append(blob)
                for retired in RETIRED + (FORMULA_MISMATCH,):
                    self.assertNotIn(retired, blob)
        source = (LAB / "card01_amc" / "fee_admission.py").read_text()
        for retired in RETIRED:
            self.assertNotIn(retired, source)

    def test_t24_gate_omits_sensitivity_rows(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = _copy_kit(root)
            first = gate_v2(
                [_row()],
                fee_source_path=paths[0],
                fee_source_id=ADMITTED_ID,
                fee_source_sha256=sha256_bytes(paths[0].read_bytes()),
                packet_index_path=paths[2],
                fee_accept_path=paths[1],
            )
            self.assertEqual(first["sensitivity_rows_status"], "SENSITIVITY_BASIS_INCOMPLETE")
            blob = json.dumps(first)
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
            doc = json.loads(paths[0].read_bytes())
            doc["fee_computation"]["sensitivity_rows"][0]["expression"] = "ceil_cent(fee_raw)+1"
            fee_path, accept_path, index_path, fee_sha = _repin(root, doc)
            second = gate_v2(
                [_row()],
                fee_source_path=fee_path,
                fee_source_id=ADMITTED_ID,
                fee_source_sha256=fee_sha,
                packet_index_path=index_path,
                fee_accept_path=accept_path,
            )
            def scrub(obj):
                if isinstance(obj, dict):
                    return {
                        key: scrub(val)
                        for key, val in obj.items()
                        if "sha256" not in key
                    }
                if isinstance(obj, list):
                    return [scrub(item) for item in obj]
                return obj
            self.assertEqual(scrub(first), scrub(second))

    def test_blocked_gate_carries_fee_identity(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            paths = _copy_kit(Path(tmp))
            claimed = "ab" * 32
            blocked = gate_v2(
                [_row()],
                fee_source_path=paths[0],
                fee_source_id=ADMITTED_ID,
                fee_source_sha256=claimed,
                packet_index_path=paths[2],
                fee_accept_path=paths[1],
            )
            self.assertEqual(blocked["status"], "BLOCKED_FEE_UNVERIFIED")
            self.assertEqual(blocked["fee_source"], ADMITTED_ID)
            self.assertEqual(blocked["fee_source_sha256"], claimed)
            self.assertIsNone(blocked["signals"])
        absent = gate([_row()])
        self.assertIn("fee_source", absent)
        self.assertIn("fee_source_sha256", absent)
        self.assertIsNone(absent["fee_source"])
        self.assertIsNone(absent["fee_source_sha256"])

    def test_t1e_pinned_function(self):
        def entry(multiplier="1"):
            return PinnedEntry("XS", "quadratic", Decimal(multiplier), multiplier, "synth", "ab" * 32, "0.07")

        cases = {
            "P.055": (Decimal("0.055"), "1", 1),
            "P.072": (Decimal("0.072"), "1", 1),
            "P.077": (Decimal("0.077"), "1", 1),
            "P.50": (Decimal("0.50"), "1", 1),
            "P.85": (Decimal("0.85"), "1", 1),
            "M1.5_P.50": (Decimal("0.50"), "1.5", 1),
            "P.37_C10": (Decimal("0.37"), "1", 10),
        }
        for key, (price, multiplier, contracts) in cases.items():
            quoted = pinned_taker_fee(entry(multiplier), price, contracts)
            expected = EXPECTED["T1e"][key]
            self.assertEqual(quoted["raw"], Decimal(expected["raw"]), key)
            self.assertEqual(quoted["headline"], Decimal(expected["HEADLINE"]), key)
            raw = quoted["raw"]
            fee_only = (raw / Decimal("0.01")).to_integral_value(rounding="ROUND_CEILING") * Decimal("0.01")
            direct_base = price * Decimal(contracts) + raw
            direct = (direct_base / Decimal("0.0001")).to_integral_value(rounding="ROUND_CEILING") * Decimal("0.0001")
            direct -= price * Decimal(contracts)
            self.assertEqual(fee_only, Decimal(expected["FEE_ONLY_CEIL"]), key)
            self.assertEqual(direct, Decimal(expected["DIRECT_0001"]), key)

    def test_t9_gate_views_and_ast_ban(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            paths = _copy_kit(Path(tmp))
            digest = sha256_bytes(paths[0].read_bytes())
            common = dict(
                fee_source_path=paths[0],
                fee_source_id=ADMITTED_ID,
                fee_source_sha256=digest,
                packet_index_path=paths[2],
                fee_accept_path=paths[1],
            )
            g1 = gate_v2([_row()], **common)
            self.assertEqual(g1["n_selected"], 1)
            self.assertEqual(g1["signals"][0]["fee_decimal"], "0.005")
            q = 0.5 * 0.176 + 0.5 * 0.05
            binary = q - (0.055 + 0.005 + 0.02)
            self.assertEqual(binary, 0.03299999999999999)
            self.assertGreater(binary, 0.03 + 1e-12)
            self.assertGreater(g1["signals"][0]["expected_net_gate"], 0.03 + 1e-12)
            g2 = gate_v2([_row(
                race_id="G2-01",
                yes_ask=0.077,
                p_model=0.195,
                p_market=0.077,
            )], **common)
            self.assertEqual(g2["n_selected"], 0)
            self.assertEqual(g2["signals"], [])
            thin = gate_v2([_row(yes_ask_qty=0)], **common)
            self.assertEqual(thin["n_selected"], 0)
            self.assertEqual(len(thin["depth_rejected"]), 1)
            self.assertEqual(thin["depth_rejected"][0]["visible_qty"], 0)

        banned = []
        covered = (
            "fee_admission.py",
            "secondary_metrics.py",
            "book_1103.py",
            "regime_split_secondary.py",
            "fee_source.py",
        )
        for name in covered:
            tree = ast.parse((LAB / "card01_amc" / name).read_text())
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                func = node.func
                if isinstance(func, ast.Name) and func.id in ("max", "min"):
                    banned.append((name, func.id, node.lineno))
                if (
                    isinstance(func, ast.Attribute)
                    and func.attr in ("max", "min")
                    and isinstance(func.value, ast.Name)
                    and func.value.id == "builtins"
                ):
                    banned.append((name, func.attr, node.lineno))
        self.assertEqual(banned, [])

    def test_same_accept_sha_on_two_rows_admits(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            paths = _copy_kit(Path(tmp))
            text = paths[2].read_text()
            accept_lines = [line for line in text.splitlines() if "CONDUCTOR_ACCEPT" in line]
            self.assertEqual(len(accept_lines), 1)
            paths[2].write_text(text + accept_lines[0] + "\n")
            admission = _admit(paths)
            self.assertEqual(admission.fee_admission, "ADMITTED_INDEX_ONLY")
            self.assertEqual(len(admission.fee_source_accept_sha256), 64)

    def test_conflicting_accept_shas_block_as_rehash_mismatch(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            paths = _copy_kit(Path(tmp))
            other = "76233683" + ("ab" * 28)
            self.assertEqual(len(other), 64)
            extra = (
                "| `packets/OTHER_CONDUCTOR_ACCEPT.json` (second fill ACCEPT) | `"
                + other
                + "` |\n"
            )
            paths[2].write_text(paths[2].read_text() + extra)
            admission = _admit(paths)
            self.assertEqual(admission.fee_admission, "BLOCKED_FEE_UNVERIFIED")
            self.assertEqual(admission.fee_block_reason, "FEE_ACCEPT_REHASH_MISMATCH")
            self.assertNotEqual(admission.fee_block_reason, "FEE_ACCEPT_MISSING")
            self.assertEqual(admission.amendment_check_failed, "b")

    def test_missing_taker_rate_blocks_without_keyerror(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = json.loads((FIXTURES / FEE_NAME).read_bytes())
            del doc["series"]["XS1"]["taker_rate"]
            fee_path, accept_path, index_path, fee_sha = _repin(root, doc)
            admission = _admit((fee_path, accept_path, index_path), fee_sha=fee_sha)
            self.assertTrue(admission.admitted)
            with self.assertRaises(FeeBlocked) as caught:
                pinned_entry_v2(admission, "XS1")
            self.assertEqual(caught.exception.reason, "TAKER_RATE_MISMATCH")
            gated = gate_v2(
                [_row()],
                fee_source_path=fee_path,
                fee_source_id=ADMITTED_ID,
                fee_source_sha256=fee_sha,
                packet_index_path=index_path,
                fee_accept_path=accept_path,
            )
            self.assertEqual(gated["status"], "BLOCKED_FEE_UNVERIFIED")
            self.assertEqual(gated["fee_block_reason"], "TAKER_RATE_MISMATCH")
            self.assertIsNone(gated["signals"])

    def test_t20_real_when_env_set(self):
        real = os.environ.get("CARD01_R1_REAL_FEE_DIR")
        if not real:
            self.skipTest("CARD01_R1_REAL_FEE_DIR is unset")
        root = Path(real)
        pins = json.loads((LAB / "PINS.json").read_text())["fee_source_v2"]
        fee_path = root / "fee.json"
        accept_path = root / "accept.json"
        index_path = root / "PACKET_INDEX.md"
        admission = admit_fee_source_v2(
            fee_source_path=fee_path,
            fee_source_id=pins["id"],
            fee_source_sha256=pins["sha256"],
            packet_index_path=index_path,
            fee_accept_path=accept_path,
            series_used=["KXHOUSERACE"],
        )
        self.assertEqual(admission.fee_admission, "ADMITTED_INDEX_ONLY")
        self.assertEqual(admission.fee_source_accept_sha256, pins["accept_sha256"])
        entry = pinned_entry_v2(admission, "KXHOUSERACE")
        for price, headline in (
            (Decimal("0.055"), Decimal("0.005")),
            (Decimal("0.072"), Decimal("0.008")),
            (Decimal("0.077"), Decimal("0.013")),
        ):
            self.assertEqual(pinned_taker_fee(entry, price)["headline"], headline)

    def test_t20_real_index_sha_before_use(self):
        real = os.environ.get("CARD01_R1_REAL_FEE_DIR")
        if not real:
            self.skipTest("CARD01_R1_REAL_FEE_DIR is unset")
        root = Path(real)
        index_path = root / "PACKET_INDEX.md"
        fee_path = root / "fee.json"
        accept_path = root / "accept.json"
        if not index_path.is_file() or not fee_path.is_file() or not accept_path.is_file():
            self.skipTest("runtime fee index is absent")
        digest = sha256_bytes(index_path.read_bytes())
        self.assertEqual(
            digest,
            "4a1ceb4b036b45914d5c0a0b7f6eeac9efb208f7792f99423acbeaf852587dfe",
        )
        pins = json.loads((LAB / "PINS.json").read_text())["fee_source_v2"]
        admission = admit_fee_source_v2(
            fee_source_path=fee_path,
            fee_source_id=pins["id"],
            fee_source_sha256=pins["sha256"],
            packet_index_path=index_path,
            fee_accept_path=accept_path,
            series_used=["KXHOUSERACE"],
        )
        self.assertEqual(admission.fee_admission, "ADMITTED_INDEX_ONLY")
        self.assertEqual(admission.packet_index_sha256_at_run, digest)


if __name__ == "__main__":
    unittest.main()
