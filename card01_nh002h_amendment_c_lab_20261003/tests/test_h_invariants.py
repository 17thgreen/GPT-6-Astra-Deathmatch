"""Hardening invariants: frozen verdict AST, module-sha substitution, T5."""
from __future__ import annotations

import ast
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from card01_amc import pnl_cd, verdict
from card01_amc.fee_admission import admit_fee_source_v2
from card01_amc.pinload import sha256_bytes
from card01_amc.regime_split_secondary import build_report, render
from tests.support import LAB
from tests.test_fee_admission_v2 import ADMITTED_ID, _copy_kit
from tests.test_pnl_cd import EXPECTED, FIXTURES, _arm_rows, _economics, _gate_v2_product, _split
from tests.test_regime_split_secondary import _selection, fixture_a

OLD_MODULE_SHA256 = "fd4473b10625e619b545f421aa09edd7341ac5567925ad35c63a95c5602f485f"
OLD_DETERMINISM = "91ddfa5546a63b175e440bce841baa71ffa7bb461c62b9fc9b7ad5de3a5af142"
OLD_ENVELOPE = "99cd8259686a3e59098f5b8fae7a6617f7ebdc181f9eec181fb04f67e48f38c5"
NATURAL_DETERMINISM = "305c351c7a449e3d9f0cc097fad17d8940d0d8509bd0306d7b16e98b93ac6344"
NATURAL_ENVELOPE = "ded715f5d9f58aec88577fc76e6fdc5885ec6846e4c3a147770bb3815d0007e7"
PY_VERSION = "3.12.3 (main, Mar 23 2026, 19:04:32) [GCC 13.3.0]"
PLATFORM_NAME = "Linux-6.12.94+-x86_64-with-glibc2.39"
T5_DIGEST = "5113b8cd01950a13a1547ed44b8726c9a40afde312526b42774dc7f6e7c1d7b6"
FROZEN_AST = {
    "_hi": "4f4911ce06ecd0f4339b25bd9c8693c236f3eb18a991484b1e9ff729d7d3ac4b",
    "_degenerate_from": "e32d9b6e01ba89cfa3ebfa75b96bb0e0196e6a84dde7cfc73aa3471dde9ff26c",
    "_blocked": "2f0aef3a4cc435cf44dc6297eb498586f433fe24b1155dd4865e3e76797fbe9c",
    "_report_reason": "ffd6658ba950eb95445b2fa92095c969fa6d54c8c5f52152e823924f2e72cb04",
    "_fee_state": "905bf80c08508c74cf13fc618d1467eaf847c1c0ce452d9cecb756353233eb2a",
    "_evaluations": "3b4b1b4188896b35a290e24e65d4ef112bba0c4d94163750c0b40ab01f9777b6",
    "_cd_firing": "8af21d02c383c0fc0111994b098679bc2bb39fee7f96c74c6597f5be807f7525",
    "apply_verdict": "25ffb1858d51733478dcf40378353f6a7cefdb63a67d4205a93ff4a2a77c0fec",
    "_binding_reason": "2951c7ac1766cd206fb84255536427e474f40b6ce744b27eca68338f0731ca95",
    "cd_from_prc": "4c80f9c6505fa4e4d4f01eed8aed7ec679b4327bffaf7581681e0156195ae124",
    "_signal_identity_reason": "e0706e5294dddf14ef3219510c96c01abe5187b335ce667074c925f86571155a",
    "_unproven_fee_blocks": "12c72f956388259ce5963971ae3298ddc232762f657a49759be02699e2ab27bb",
    "_forecast_only": "0974b8a2416ed9645ef58fdc787048d6ac64996476f3ddb30de823104f0d9bdb",
}


def _sha_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class FrozenVerdictTests(unittest.TestCase):
    def test_h_invariant_frozen_verdict_ast(self):
        text = (LAB / "card01_amc" / "verdict.py").read_text(encoding="utf-8")
        tree = ast.parse(text)
        found = {}
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name in FROZEN_AST:
                found[node.name] = hashlib.sha256(ast.dump(node).encode()).hexdigest()
        self.assertEqual(found, FROZEN_AST)

    def test_h_invariant_frozen_modules_and_citation_sets(self):
        expected = {
            "card01_amc/fee_admission.py": "c4a5d3b2fe8edb50a3782ed6a15fd0b3a3d2071597e657a0fbb10ab9aae60805",
            "card01_amc/entry_gate.py": "24c9e06ab392b463613a7f1d7ca29eb3f7c88e7d24de299d59c11fa5014b9d73",
            "card01_amc/regime_split_secondary.py": "c498f72b7a0b559b47342183e09bc62f4e14bd5a9174fe89efa96796efd1a151",
            "card01_amc/fee_citation_set.json": "3a56ead8151967f704ce6e344f3c61f18bc660e3f37e45dbb269dd3123905149",
            "card01_amc/r1_accept_citation_set.json": "8e26ac4e5db007ab671119379acdf0251f18b08f56ab00813cdd4e89401d4da3",
        }
        for rel, digest in expected.items():
            self.assertEqual(_sha_file(LAB / rel), digest, rel)


class SubstitutionTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        root = Path(self._tmp.name)
        paths = _copy_kit(root)
        digest = sha256_bytes(paths[0].read_bytes())
        admission = admit_fee_source_v2(
            fee_source_path=paths[0],
            fee_source_id=ADMITTED_ID,
            fee_source_sha256=digest,
            packet_index_path=paths[2],
            fee_accept_path=paths[1],
            series_used=["XS1"],
        )
        self.pin = {
            "id": admission.fee_source,
            "sha256": admission.fee_source_sha256,
            "accept_sha256": admission.fee_source_accept_sha256,
            "fee_formula_id": admission.fee_formula_id,
            "series_pinned": ["XS1"],
        }
        self.pin_path = root / "PINS.json"
        self.pin_path.write_text(json.dumps({"fee_source_v2": self.pin}), encoding="utf-8")
        self.fee_ctx = {
            "fee_source_path": str(paths[0]),
            "packet_index_path": str(paths[2]),
            "fee_accept_path": str(paths[1]),
        }
        self._saved = verdict.PINS_PATH
        verdict.PINS_PATH = self.pin_path
        self.addCleanup(self._restore_pins)

    def _restore_pins(self):
        verdict.PINS_PATH = self._saved

    def _digests(self):
        case = next(item for item in FIXTURES["cases"] if item["id"] == "P1_CLEAN")
        gate = json.loads(json.dumps(case["gate"]))
        gate["fee_source"] = self.pin["id"]
        gate["fee_source_sha256"] = self.pin["sha256"]
        gate["fee_source_accept_sha256"] = self.pin["accept_sha256"]
        gate["fee_formula_id"] = self.pin["fee_formula_id"]
        for signal in gate["signals"]:
            signal["fee_source"] = self.pin["id"]
            signal["fee_source_sha256"] = self.pin["sha256"]
            signal["fee_formula_id"] = self.pin["fee_formula_id"]
            signal["series"] = signal.get("series") or "XS1"
        rows, settled = _split(case)
        rows = _arm_rows(rows, gate.get("signals"))
        produced = _gate_v2_product(rows, self.fee_ctx, self.pin)
        self.assertEqual(_economics(produced.get("signals")), _economics(gate.get("signals")))
        gate = produced
        raw = json.dumps(gate).encode()
        gate_sha = sha256_bytes(raw)
        envelope = pnl_cd.entry_book_envelope(gate, gate_sha256=gate_sha, fee_ctx=self.fee_ctx)
        book = (json.dumps(envelope, indent=1) + "\n").encode()
        anchor = pnl_cd.make_anchor(
            book,
            gate_sha256=gate_sha,
            anchored_at_utc="2026-11-02T22:15:00Z",
        )
        scored = pnl_cd.run(
            gate,
            rows,
            lambda: settled,
            gate_sha256=gate_sha,
            entry_book_bytes=book,
            anchor_doc=anchor,
            fee_ctx=self.fee_ctx,
        )
        return scored["output_sha256"], envelope["output_sha256"]

    def _under_interpreter(self, module_sha):
        with mock.patch.object(pnl_cd, "module_sha256", return_value=module_sha):
            with mock.patch.object(pnl_cd.platform, "platform", return_value=PLATFORM_NAME):
                with mock.patch.object(pnl_cd.sys, "version", PY_VERSION):
                    return self._digests()

    def test_h_invariant_module_sha_substitution(self):
        determinism, envelope = self._under_interpreter(OLD_MODULE_SHA256)
        self.assertEqual(determinism, OLD_DETERMINISM)
        self.assertEqual(envelope, OLD_ENVELOPE)
        natural_d, natural_e = self._under_interpreter(pnl_cd.module_sha256())
        self.assertEqual(natural_d, NATURAL_DETERMINISM)
        self.assertEqual(natural_e, NATURAL_ENVELOPE)
        self.assertEqual(
            EXPECTED["cases"]["P1_CLEAN"]["entry_table_sha256"],
            "ce2d2c694cee99dd6fce14d0a990cb20529e3ec1b046e28e826767c13887174f",
        )


class T5InvariantTests(unittest.TestCase):
    def test_h_invariant_t5_digest(self):
        rows = fixture_a(84)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = _copy_kit(root)
            fee_sha = sha256_bytes(paths[0].read_bytes())
            accept_sha = sha256_bytes(paths[1].read_bytes())
            gate = {
                "status": "OK",
                "signals": [],
                "depth_rejected": [],
                "gate_sha256": "ab" * 32,
                "fee_admission": "ADMITTED_INDEX_ONLY",
                "fee_formula_id": "astra.card01.fee_eff.non_direct_buy_ceil_cent.v1",
                "fee_source": ADMITTED_ID,
                "fee_source_sha256": fee_sha,
                "fee_source_accept_sha256": accept_sha,
            }
            with mock.patch.object(sys, "version", PY_VERSION):
                _text, digest = render(build_report(
                    rows,
                    selection=_selection(),
                    gate=gate,
                    book={"capture_status": "NOT_CAPTURED_EGRESS_CLOSED", "snapshots": []},
                    settled={"results": []},
                    fee_source_path=paths[0],
                    fee_source_id=ADMITTED_ID,
                    fee_source_sha256=fee_sha,
                    packet_index_path=paths[2],
                    fee_accept_path=paths[1],
                ))
        self.assertEqual(digest, T5_DIGEST)
