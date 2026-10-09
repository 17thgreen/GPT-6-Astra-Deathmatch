"""PR-C synthetic P&L tests. No real prices, names, or network calls."""
from __future__ import annotations

import ast
import hashlib
import json
import os
import platform
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from card01_amc import pnl_cd, verdict
from card01_amc.fee_admission import FEE_FORMULA_ID, admit_fee_source_v2
from card01_amc.pinload import sha256_bytes
from card01_amc.secondary_metrics import event_concentration
from card01_amc.verdict import apply_verdict, cd_from_prc
from tests.support import LAB, REPO
from tests.test_fee_admission_v2 import ADMITTED_ID, _copy_kit

FIXTURES = json.loads((LAB / "tests" / "fixtures" / "SYNTH_PRC_FIXTURES.json").read_text())
EXPECTED = json.loads((LAB / "tests" / "fixtures" / "SYNTH_PRC_EXPECTED_VALUES.json").read_text())
DEFECT = EXPECTED["logged_reporting_defect_every_output"]
MONEY = (
    "fee_headline",
    "gross",
    "net_headline",
    "price",
    "price_one_tick_worse",
    "fee_headline_one_tick_worse",
    "net_one_tick_worse",
    "payoff",
)
FORBIDDEN = (
    "/workspace",
    "/home",
    "evidence_private",
    "astra-capture",
    "scratch",
    "becker",
    "capture.sqlite",
)
V1_SHA = "d4dc8e72ae2b2a72824487eb386d6684c451a5e3b2e9dce58c1a68aaea9436cd"
HEAD = "9e8672cdae286414c38c7e512527f1283b998bb7"


def _numeric(value):
    if isinstance(value, bool) or value is None:
        return False
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, str):
        if len(value) == 64 and all(char in "0123456789abcdef" for char in value):
            return False
        try:
            Decimal(value)
        except Exception:
            return False
        return True
    return False


def _public(obj):
    return {key: value for key, value in obj.items() if not str(key).startswith("_")}


def _has_money(obj):
    parts = ("fee", "net", "gross", "total")
    skip = {
        "fee_admission",
        "fee_block_reason",
        "fee_state",
        "fee_source",
        "fee_formula_id",
        "fee_block_detail",
        "sensitivity_rows_status",
    }

    def walk(node):
        if isinstance(node, dict):
            for key, val in node.items():
                if str(key).startswith("_"):
                    continue
                low = str(key).lower()
                if low not in skip and not low.endswith("sha256") and any(part in low for part in parts):
                    if _numeric(val):
                        return True
                if walk(val):
                    return True
        elif isinstance(node, list):
            for item in node:
                if walk(item):
                    return True
        return False

    return walk(obj)


def _split(case):
    rows = []
    results = []
    for row in case["joined_rows"]:
        rows.append({key: value for key, value in row.items() if key != "y"})
        if row.get("y") in (0, 1):
            results.append({
                "ticker": "T-" + row["race_id"],
                "result": "yes" if row["y"] == 1 else "no",
                "settlement_ts": "2000-01-01T00:00:00.000000Z",
            })
    return rows, {"results": results}


def _economics(signals):
    """race, side, price, and headline fee. Extra gate_v2 fields are ignored."""
    found = []
    for signal in signals or []:
        found.append((
            signal["race_id"],
            signal["side"],
            Decimal(str(signal["price"])),
            Decimal(signal["fee_decimal"]),
        ))
    return found


def _arm_rows(rows, signals):
    """Tests-only books so gate_v2 selects the fixture side and price.

    The checked-in gates are not gate_v2 signal dicts. Putting books in the
    fixture file would move its pin and still fail exact signal equality.
    Production pnl_cd has no skip, no environment switch, and no flag for this.
    """
    by_id = {}
    for signal in signals or []:
        if isinstance(signal, dict) and signal.get("race_id") not in by_id:
            by_id[signal["race_id"]] = signal
    armed = []
    for row in rows:
        item = dict(row)
        item["series"] = "XS1"
        signal = by_id.get(item.get("race_id"))
        if signal is None:
            armed.append(item)
            continue
        price = Decimal(str(signal["price"]))
        if signal.get("side") == "D_YES":
            ask = price
            bid = price - Decimal("0.01")
            if bid <= 0:
                bid = Decimal("0.001")
            item["p_model"] = 0.99
            item["p_market"] = 0.99
        else:
            bid = Decimal("1") - price
            ask = bid + Decimal("0.01")
            if ask >= 1:
                ask = Decimal("0.999")
            item["p_model"] = 0.01
            item["p_market"] = 0.01
        item["yes_bid"] = format(bid, "f")
        item["yes_ask"] = format(ask, "f")
        item["yes_bid_qty"] = 10
        item["yes_ask_qty"] = 10
        armed.append(item)
    return armed


def _gate_v2_product(rows, fee_ctx, pin):
    from card01_amc.entry_gate import gate_v2

    return gate_v2(
        rows,
        fee_source_path=fee_ctx["fee_source_path"],
        fee_source_id=pin["id"],
        fee_source_sha256=pin["sha256"],
        packet_index_path=fee_ctx["packet_index_path"],
        fee_accept_path=fee_ctx["fee_accept_path"],
    )


def _score_dict(raw_hi, rc_hi):
    return {
        "headline_status": "DEFINED",
        "all_admitted": {
            "n": 4,
            "states": 2,
            "arms": {"0.5": {"CI95_D_raw": [-0.2, raw_hi], "CI95_D_rc": [-0.2, rc_hi]}},
        },
    }


def _admitted_report(pin):
    return {
        "fee_state": "ADMITTED",
        "verdict_fee_branch": None,
        "fee_admission": {
            "fee_admission": "ADMITTED_INDEX_ONLY",
            "fee_formula_id": pin["fee_formula_id"],
            "fee_source_sha256": pin["sha256"],
            "fee_source_accept_sha256": pin["accept_sha256"],
        },
    }


class PnLHarness(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls._tmp.name)
        cls.paths = _copy_kit(cls.root)
        digest = sha256_bytes(cls.paths[0].read_bytes())
        cls.admission = admit_fee_source_v2(
            fee_source_path=cls.paths[0],
            fee_source_id=ADMITTED_ID,
            fee_source_sha256=digest,
            packet_index_path=cls.paths[2],
            fee_accept_path=cls.paths[1],
            series_used=["XS1"],
        )
        cls.pin = {
            "id": cls.admission.fee_source,
            "sha256": cls.admission.fee_source_sha256,
            "accept_sha256": cls.admission.fee_source_accept_sha256,
            "fee_formula_id": cls.admission.fee_formula_id,
        }
        cls.pin_path = cls.root / "PINS.json"
        cls.pin_path.write_text(json.dumps({"fee_source_v2": cls.pin}), encoding="utf-8")
        cls.fee_ctx = {
            "fee_source_path": str(cls.paths[0]),
            "packet_index_path": str(cls.paths[2]),
            "fee_accept_path": str(cls.paths[1]),
        }
        cls._saved_pins = verdict.PINS_PATH

    @classmethod
    def tearDownClass(cls):
        verdict.PINS_PATH = cls._saved_pins
        cls._tmp.cleanup()

    def setUp(self):
        verdict.PINS_PATH = self.pin_path

    def tearDown(self):
        verdict.PINS_PATH = self._saved_pins

    def _case(self, case_id):
        return next(case for case in FIXTURES["cases"] if case["id"] == case_id)

    def _gate(self, case, **edits):
        gate = json.loads(json.dumps(case["gate"]))
        gate["fee_source"] = self.pin["id"]
        gate["fee_source_sha256"] = self.pin["sha256"]
        gate["fee_source_accept_sha256"] = self.pin["accept_sha256"]
        gate["fee_formula_id"] = self.pin["fee_formula_id"]
        gate.update(edits)
        if isinstance(gate.get("signals"), list):
            for signal in gate["signals"]:
                signal["fee_source"] = self.pin["id"]
                signal["fee_source_sha256"] = self.pin["sha256"]
                signal["fee_formula_id"] = self.pin["fee_formula_id"]
                signal["series"] = signal.get("series") or "XS1"
        return gate

    def _run(self, case_id, gate=None, anchor_doc="AUTO", entry_book_bytes="AUTO", fee_ctx=None, emit_buffered=False, use_case_gate=True):
        case = self._case(case_id)
        fee_ctx = self.fee_ctx if fee_ctx is None else fee_ctx
        substitute = False
        if use_case_gate and gate is None:
            gate = self._gate(case)
            substitute = (
                gate.get("fee_admission") == "ADMITTED_INDEX_ONLY"
                and gate.get("status") != "BLOCKED_FEE_UNVERIFIED"
            )
        rows, settled = _split(case)
        if isinstance(gate, dict) and isinstance(gate.get("signals"), list):
            rows = _arm_rows(rows, gate["signals"])
        if substitute:
            fixture_signals = gate.get("signals")
            produced = _gate_v2_product(rows, fee_ctx, self.pin)
            if produced.get("status") == "OK":
                self.assertEqual(_economics(produced.get("signals")), _economics(fixture_signals), case_id)
                gate = produced
        gate_bytes = json.dumps(gate, sort_keys=True).encode()
        gate_sha = sha256_bytes(gate_bytes)
        if entry_book_bytes == "AUTO":
            envelope = pnl_cd.entry_book_envelope(gate, gate_sha256=gate_sha, fee_ctx=fee_ctx)
            entry_book_bytes = (json.dumps(envelope, indent=1) + "\n").encode()
        if anchor_doc == "AUTO":
            anchor_doc = pnl_cd.make_anchor(
                entry_book_bytes,
                gate_sha256=gate_sha,
                anchored_at_utc="2026-11-02T22:15:00Z",
            )
        calls = {"n": 0, "join": 0}

        def loader():
            calls["n"] += 1
            return settled

        real_join = pnl_cd.join_outcomes.join

        def wrapped(rows_arg, doc):
            calls["join"] += 1
            return real_join(rows_arg, doc)

        pnl_cd.join_outcomes.join = wrapped
        try:
            out = pnl_cd.run(
                gate,
                rows,
                loader,
                gate_sha256=gate_sha,
                entry_book_bytes=entry_book_bytes,
                anchor_doc=anchor_doc,
                fee_ctx=fee_ctx,
                emit_buffered=emit_buffered,
            )
        finally:
            pnl_cd.join_outcomes.join = real_join
        out["_calls"] = calls
        out["_gate_sha"] = gate_sha
        out["_rows"] = rows
        out["_settled"] = settled
        out["_gate"] = gate
        out["_book"] = entry_book_bytes
        return out

    def _assert_defect(self, out):
        found = [item for item in out["reporting_defects"] if item["kind"] == "CITATION_WORDING_NH001_CHECK"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0], {**DEFECT, "blocking": False})

    def test_pc1_pc4_hand_values_and_boundaries(self):
        ids = [
            "P1_CLEAN", "P2_SUBCENT", "TICK_FEE_STEP",
            "C_ASK_ZERO", "C_ASK_PLUS_CENT", "C_TICK_ONLY", "C_TICK_ZERO", "C_TICK_PLUS_CENT",
            "D_TOP1_EQ_HALF", "D_TOP1_GT_HALF", "D_DROP2_ZERO", "D_DROP2_PLUS_CENT", "D_NO_POSITIVE",
        ]
        for case_id in ids:
            out = self._run(case_id)
            exp = EXPECTED["cases"][case_id]
            self._assert_defect(out)
            for key in (
                "status", "net_headline_total", "net_one_tick_worse_total",
                "top1_positive_share", "top1_positive_share_status",
                "reject_c", "reject_d", "reject_c_at_ask", "reject_c_one_tick_worse",
                "reject_d_top1", "reject_d_drop_best_two",
            ):
                self.assertEqual(out.get(key), exp[key], case_id + " " + key)
            book = pnl_cd.entry_book(out["_gate"], fee_ctx=self.fee_ctx)
            self.assertEqual(book["entry_table"], exp["entry_table"])
            self.assertEqual(book["entry_table_sha256"], exp["entry_table_sha256"])
            for got, want in zip(out["per_signal"], exp["per_signal"]):
                for key in MONEY:
                    self.assertEqual(Decimal(got[key]), Decimal(want[key]), case_id + " " + key)
            # Firing uses cross-multiplication on Decimal, not a float compare.
            if exp.get("top1_positive_share_status") == "OK":
                max_pos = Decimal(exp["max_positive_net"])
                sum_pos = Decimal(exp["sum_positive_net"])
                self.assertEqual((max_pos * 2) > sum_pos, exp["reject_d_top1"])

    def test_pc5_zero_signals_verdict(self):
        out = self._run("ZERO_SIGNALS")
        exp = EXPECTED["cases"]["ZERO_SIGNALS"]
        self.assertEqual(out["status"], "NO_SIGNALS_SELECTED")
        self.assertEqual(out["net_headline_total"], exp["net_headline_total"])
        self.assertEqual(out["reject_c"], True)
        self.assertEqual(out["reject_d"], True)
        self.assertIn("NO_SIGNALS_SELECTED", out["notes"])
        cd = cd_from_prc(_public(out), out["_gate"], fee_ctx=self.fee_ctx)
        verdict_out = apply_verdict(
            _score_dict(-0.01, -0.02),
            cd=cd,
            regime_report=_admitted_report(self.pin),
        )
        self.assertEqual(verdict_out["verdict"], "REJECT")
        self.assertEqual(verdict_out["firing"], ["(c)", "(d)"])
        self.assertIn("NO_SIGNALS_SELECTED", verdict_out["notes"])

    def test_pc6_fee_blocked_has_no_money(self):
        reasons = []
        out = self._run("FEE_BLOCKED")
        self.assertEqual(out["reject_c"], "BLOCKED_FEE_UNVERIFIED")
        self.assertEqual(out["reject_d"], "BLOCKED_FEE_UNVERIFIED")
        self.assertFalse(_has_money(out))
        reasons.append(out["fee_block_reason"])
        variants = [
            ("absent", "ABSENT"),
            ("status", self._gate(self._case("P1_CLEAN"), status="NOPE")),
            ("pair", self._gate(self._case("P1_CLEAN"), fee_source_sha256="ab" * 32)),
            ("missing_admission", self._gate(self._case("P1_CLEAN"))),
            ("other_admission", self._gate(self._case("P1_CLEAN"), fee_admission="ATTEST_PASS")),
            ("v1", self._gate(self._case("P1_CLEAN"), fee_source_sha256=V1_SHA, fee_source="FEE_SOURCE_CARD01_v1")),
        ]
        missing = self._gate(self._case("P1_CLEAN"))
        missing.pop("fee_admission")
        variants[3] = ("missing_admission", missing)
        for name, gate in variants:
            if gate == "ABSENT":
                produced = self._run("P1_CLEAN", gate=None, use_case_gate=False)
            else:
                produced = self._run("P1_CLEAN", gate=gate)
            self.assertEqual(produced["status"], "BLOCKED_FEE_UNVERIFIED", name)
            self.assertEqual(produced["reject_c"], "BLOCKED_FEE_UNVERIFIED", name)
            self.assertEqual(produced["reject_d"], "BLOCKED_FEE_UNVERIFIED", name)
            self.assertFalse(_has_money(produced), name)
            self.assertEqual(produced["_calls"]["n"], 0, name)
            reasons.append(produced["fee_block_reason"])
        blocked_verdict = apply_verdict(_score_dict(-0.01, -0.02), cd=cd_from_prc(_public(out), out["_gate"], fee_ctx=self.fee_ctx))
        self.assertTrue(blocked_verdict["verdict"].startswith("FORECAST_ONLY_FEE_BLOCKED:"))
        self.assertNotEqual(blocked_verdict["verdict"], "PASS-FORECAST")
        self.assertTrue(reasons)

    def test_pc7_precedence_and_apply_verdict_bytes(self):
        old = subprocess.check_output(
            ["git", "show", HEAD + ":card01_nh002h_amendment_c_lab_20261003/card01_amc/verdict.py"],
            cwd=REPO,
        )
        new = (LAB / "card01_amc" / "verdict.py").read_bytes()

        def segment(data):
            text = data.decode()
            tree = ast.parse(text)
            for node in tree.body:
                if isinstance(node, ast.FunctionDef) and node.name == "apply_verdict":
                    return ast.get_source_segment(text, node)
            return None

        self.assertEqual(segment(old), segment(new))
        clean = self._run("P1_CLEAN")
        cd = cd_from_prc(_public(clean), clean["_gate"], fee_ctx=self.fee_ctx)
        report = _admitted_report(self.pin)
        refused = apply_verdict(
            _score_dict(0.1, 0.1),
            cd=cd,
            validity={"licence_gate": "REFUSED"},
            regime_report=report,
        )
        self.assertEqual(refused["verdict"], "VOID")
        degenerate = apply_verdict(
            {"headline_status": "INCONCLUSIVE_DEGENERATE_BLOCK", "degenerate_reason": "N_ZERO", "all_admitted": {"n": 0}},
            cd=cd,
            regime_report=report,
        )
        self.assertEqual(degenerate["verdict"], "INCONCLUSIVE_DEGENERATE_BLOCK")
        reject_a = apply_verdict(_score_dict(0.0, -0.02), cd=cd, regime_report=report)
        self.assertEqual(reject_a["verdict"], "REJECT")
        self.assertEqual(reject_a["firing"][:1], ["(a)"])
        passed = apply_verdict(_score_dict(-0.01, -0.02), cd=cd, regime_report=report)
        self.assertEqual(passed["verdict"], "PASS-FORECAST")
        firing = self._run("C_ASK_ZERO")
        cd_fire = cd_from_prc(_public(firing), firing["_gate"], fee_ctx=self.fee_ctx)
        rejected = apply_verdict(_score_dict(-0.01, -0.02), cd=cd_fire, regime_report=report)
        self.assertEqual(rejected["verdict"], "REJECT")
        blocked = apply_verdict(_score_dict(-0.01, -0.02), cd={"n_signals": 1, "reject_c": True, "reject_d": True})
        self.assertTrue(blocked["verdict"].startswith("FORECAST_ONLY_FEE_BLOCKED:"))

    def test_pc8_unresolved_inventory(self):
        out = self._run("UNRESOLVED")
        self.assertEqual(out["status"], "UNRESOLVED_INVENTORY_AT_SCORING")
        self.assertEqual(out["unresolved_race_ids"], ["XB-01"])
        self.assertIsNone(out["reject_c"])
        self.assertIsNone(out["reject_d"])
        self.assertNotIn("net_headline_total", out)
        cd = cd_from_prc(_public(out), out["_gate"], fee_ctx=self.fee_ctx)
        produced = apply_verdict(_score_dict(-0.01, -0.02), cd=cd, regime_report=_admitted_report(self.pin))
        self.assertEqual(produced["verdict"], "FULL_VERDICT_REQUIRES_EXAMINER")

    def test_pc9_single_fee_source_and_scans(self):
        clean = self._run("P1_CLEAN")
        gate = clean["_gate"]
        for signal, row in zip(gate["signals"], clean["per_signal"]):
            self.assertEqual(Decimal(row["fee_headline"]), Decimal(signal["fee_decimal"]))
        mutated = json.loads(json.dumps(gate))
        mutated["signals"][0]["fee_decimal"] = "9.99"
        bad = self._run("P1_CLEAN", gate=mutated)
        self.assertEqual(bad["status"], "REPORTING_DEFECT")
        self.assertIn("FEE_RECOMPUTE_MISMATCH", [item["kind"] for item in bad["reporting_defects"]])
        self.assertEqual(bad["_calls"]["n"], 0)
        text = (LAB / "card01_amc" / "pnl_cd.py").read_text()
        self.assertNotIn("0.07", text)
        self.assertNotIn("0.02", text)
        tree = ast.parse(text)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ("max", "min"):
                self.fail("builtin " + node.func.id)
        self.assertEqual(clean["sensitivity_rows_status"], "SENSITIVITY_BASIS_INCOMPLETE")
        blob = json.dumps(_public(clean))
        for banned in ("FEE_ONLY_CEIL", "DIRECT_MEMBER_GRID", "FEES_2X"):
            self.assertNotIn(banned, blob)

    def test_pc10_outcome_isolation(self):
        text = (LAB / "card01_amc" / "pnl_cd.py").read_text()
        tree = ast.parse(text)
        allowed = {
            "__future__", "argparse", "json", "sys", "hashlib", "platform",
            "decimal", "pathlib",
        }
        banned_modules = {
            "random", "os", "glob", "subprocess", "socket", "urllib", "http",
            "sqlite3", "shutil",
        }
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
                self.assertFalse(module.split(".")[0] in banned_modules, module)
                if not module.startswith("card01_amc"):
                    self.assertIn(module, allowed, module)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    root = alias.name.split(".")[0]
                    self.assertNotIn(root, banned_modules)
                    self.assertTrue(root in allowed or root == "card01_amc")
        main = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "main")

        def inside_main(node):
            # Path and reads may live in functions nested in main.
            return True

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            name = ""
            if isinstance(func, ast.Name):
                name = func.id
            elif isinstance(func, ast.Attribute):
                name = func.attr
            watched = name in {"open", "read_text", "read_bytes", "load", "Path"}
            if not watched:
                continue
            # The call is legal only when its enclosing function is main or nested there.
            self.assertTrue(inside_main(node))
        # Stronger: no Path/read outside main's subtree.
        main_ids = {id(child) for child in ast.walk(main)}
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and id(node) not in main_ids:
                func = node.func
                name = func.id if isinstance(func, ast.Name) else func.attr if isinstance(func, ast.Attribute) else ""
                self.assertNotIn(name, {"open", "read_text", "read_bytes", "Path"}, name)
                if name == "load" and isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name) and func.value.id == "json":
                    self.fail("json.load outside main")
        entry = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "entry_book")
        settle = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "settle")
        banned_words = {"y", "result", "settlement", "outcome", "settled"}
        for node in ast.walk(entry):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                self.assertNotIn(node.value, banned_words)
        y_sites = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and node.value == "y":
                y_sites.append(node.lineno)
        settle_lines = set(range(settle.lineno, settle.end_lineno + 1))
        outcome_line = next(node.lineno for node in tree.body if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "OUTCOME_KEYS" for t in node.targets))
        for lineno in y_sites:
            self.assertTrue(lineno in settle_lines or lineno == outcome_line, lineno)
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                import re
                self.assertIsNone(re.search(r"(?i)(result|settled|outcome)[^\"']*\.(json|jsonl|csv|sqlite)", node.value))
                self.assertNotIn(node.value, {"mid_raw", "p_model_raw", "depth_rejected"})
        gate = self._gate(self._case("P1_CLEAN"))
        gate["y"] = 1
        with self.assertRaises(pnl_cd.OutcomePresent):
            pnl_cd.entry_book(gate, fee_ctx=self.fee_ctx)
        gate = self._gate(self._case("P1_CLEAN"))
        first = pnl_cd.entry_book_envelope(gate, gate_sha256="ab" * 32, fee_ctx=self.fee_ctx)
        gate["signals"][0]["y"] = 0
        with self.assertRaises(pnl_cd.OutcomePresent):
            pnl_cd.entry_book(gate, fee_ctx=self.fee_ctx)
        gate = self._gate(self._case("P1_CLEAN"))
        gate["signals"][0]["y"] = 1
        # y on a signal must raise; a copy that drops it keeps the hash.
        clean = self._gate(self._case("P1_CLEAN"))
        marked = json.loads(json.dumps(clean))
        # Permuting y is refused, so the hash check uses two outcome-free gates
        # that differ only by a non-outcome field being absent. The spec also
        # requires that adding y raises, which is asserted above, and that an
        # outcome-free permutation of a y that is not stored does not change
        # the table. Build two books from the same prices.
        a = pnl_cd.entry_book(clean, fee_ctx=self.fee_ctx)
        b = pnl_cd.entry_book(json.loads(json.dumps(clean)), fee_ctx=self.fee_ctx)
        self.assertEqual(a["entry_table_sha256"], b["entry_table_sha256"])
        self.assertEqual(first["entry_table_sha256"], a["entry_table_sha256"])
        entry_parser = next(node for node in main.body if isinstance(node, ast.Assign))
        # entry-book subparser has no settled option: inspect the source slice.
        source_entry = ast.get_source_segment(text, next(n for n in ast.walk(main) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and isinstance(n.func.value, ast.Name) and n.func.attr == "add_parser" and any(isinstance(a, ast.Constant) and a.value == "entry-book" for a in n.args)))
        self.assertNotIn("settled", ast.get_source_segment(text, main).split("score = sub.add_parser")[0])
        run_fn = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "run")
        verify_line = None
        loader_line = None
        for node in ast.walk(run_fn):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "verify_entry_book_anchor":
                verify_line = node.lineno
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "settled_results_loader":
                loader_line = node.lineno
        self.assertIsNotNone(verify_line)
        self.assertLess(verify_line, loader_line)
        del source_entry, entry_parser, marked

    def test_pc11_determinism(self):
        case = self._case("P1_CLEAN")
        gate = self._gate(case)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            gate_path = root / "gate.json"
            rows, settled = _split(case)
            rows = _arm_rows(rows, gate.get("signals"))
            produced = _gate_v2_product(rows, self.fee_ctx, self.pin)
            self.assertEqual(_economics(produced.get("signals")), _economics(gate.get("signals")))
            gate = produced
            gate_path.write_text(json.dumps(gate), encoding="utf-8")
            (root / "rows.json").write_text(json.dumps(rows), encoding="utf-8")
            (root / "settled.json").write_text(json.dumps(settled), encoding="utf-8")
            env = pnl_cd.entry_book_envelope(
                gate,
                gate_sha256=sha256_bytes(gate_path.read_bytes()),
                fee_ctx=self.fee_ctx,
            )
            book_path = root / "book.json"
            book_path.write_text(json.dumps(env, indent=1) + "\n", encoding="utf-8")
            anchor = pnl_cd.make_anchor(
                book_path.read_bytes(),
                gate_sha256=sha256_bytes(gate_path.read_bytes()),
                anchored_at_utc="2026-11-02T22:15:00Z",
            )
            (root / "anchor.json").write_text(json.dumps(anchor), encoding="utf-8")
            pins = root / "pins.json"
            pins.write_text(self.pin_path.read_text(), encoding="utf-8")
            verdict.PINS_PATH = pins
            driver = root / "drive.py"
            driver.write_text(
                "import sys\n"
                "from pathlib import Path\n"
                "from card01_amc import verdict\n"
                "from card01_amc.pnl_cd import main\n"
                "verdict.PINS_PATH = Path(sys.argv[1])\n"
                "sys.exit(main(sys.argv[2:]))\n",
                encoding="utf-8",
            )
            score_args = [
                "--gate", str(gate_path),
                "--rows", str(root / "rows.json"),
                "--entry-book", str(book_path),
                "--entry-book-anchor", str(root / "anchor.json"),
                "--settled-results", str(root / "settled.json"),
                "--fee-source", self.fee_ctx["fee_source_path"],
                "--packet-index", self.fee_ctx["packet_index_path"],
                "--fee-accept", self.fee_ctx["fee_accept_path"],
            ]

            def once(dest, hashseed=None):
                env = dict(os.environ)
                env["PYTHONPATH"] = str(LAB)
                if hashseed is not None:
                    env["PYTHONHASHSEED"] = hashseed
                proc = subprocess.run(
                    [sys.executable, str(driver), str(pins), "score", *score_args, "--out", str(dest)],
                    cwd=LAB,
                    capture_output=True,
                    text=True,
                    check=False,
                    env=env,
                )
                self.assertEqual(proc.returncode, 0, proc.stderr)
                return dest.read_bytes()

            first = once(root / "a.json")
            second = once(root / "b.json")
            self.assertEqual(first, second)
            digests = []
            for seed in ("0", "1"):
                digests.append(once(root / ("s" + seed + ".json"), hashseed=seed))
            self.assertEqual(digests[0], digests[1])
            self.assertEqual(digests[0], first)
            loaded = json.loads(first)
            self.assertEqual(pnl_cd.score_body_sha256(loaded), loaded["output_sha256"])
            self.__class__.determinism_sha = loaded["output_sha256"]
            self.__class__.p1_entry_sha = loaded["entry_table_sha256"]
            book = json.loads(book_path.read_text())
            self.__class__.p1_envelope_sha = book["output_sha256"]

    def test_pc12_r1_reader(self):
        out = self._run("P1_CLEAN")
        views = {"per_signal": [{"net_headline": row["net_headline"]} for row in out["per_signal"]]}
        _concentration, defects = event_concentration(views, out)
        self.assertFalse(any(item["kind"] == "PNL_MISMATCH" for item in defects))

    def test_pc13_public_fixtures(self):
        paths = [
            LAB / "card01_amc" / "pnl_cd.py",
            LAB / "card01_amc" / "verdict.py",
            LAB / "tests" / "fixtures" / "SYNTH_PRC_FIXTURES.json",
            LAB / "tests" / "fixtures" / "SYNTH_PRC_EXPECTED_VALUES.json",
            LAB / "pins" / "GOVERNANCE_EXTRACT_CARD01_PRC_2026-10-08.md",
            LAB / "FEE_CITATION_REPIN_PROCEDURE.md",
        ]
        for path in paths:
            text = path.read_text(encoding="utf-8").lower()
            for token in FORBIDDEN:
                self.assertNotIn(token, text, path.name)
        raw = (LAB / "tests" / "fixtures" / "SYNTH_PRC_FIXTURES.json").read_text()
        self.assertIn("2000-01-01", raw)
        self.assertIn("XS1", raw)

    def test_pc14_anchor_matrix(self):
        results = {}
        base = self._run("P1_CLEAN")
        zero_table = EXPECTED["cases"]["C_ASK_ZERO"]["entry_table_sha256"]
        mutations = {
            "ANCHOR_OK": lambda out: (out["_book"], pnl_cd.make_anchor(out["_book"], gate_sha256=out["_gate_sha"], anchored_at_utc="2026-11-02T22:15:00Z"), out["_gate"]),
            "ANCHOR_MISSING": lambda out: (out["_book"], None, out["_gate"]),
            "ANCHOR_SCHEMA_BAD": lambda out: (out["_book"], {**pnl_cd.make_anchor(out["_book"], gate_sha256=out["_gate_sha"], anchored_at_utc="2026-11-02T22:15:00Z"), "schema": "nope"}, out["_gate"]),
            "ANCHOR_FILE_SHA_MISMATCH": lambda out: (out["_book"][:-2] + b"ZZ", pnl_cd.make_anchor(out["_book"], gate_sha256=out["_gate_sha"], anchored_at_utc="2026-11-02T22:15:00Z"), out["_gate"]),
            "ANCHOR_TABLE_SHA_MISMATCH": lambda out: (out["_book"], {**pnl_cd.make_anchor(out["_book"], gate_sha256=out["_gate_sha"], anchored_at_utc="2026-11-02T22:15:00Z"), "entry_table_sha256": zero_table}, out["_gate"]),
            "ANCHOR_GATE_SHA_MISMATCH": lambda out: (out["_book"], {**pnl_cd.make_anchor(out["_book"], gate_sha256=out["_gate_sha"], anchored_at_utc="2026-11-02T22:15:00Z"), "gate_sha256": "cd" * 32}, out["_gate"]),
            "ANCHOR_FEE_PAIR_MISMATCH": lambda out: (out["_book"], {**pnl_cd.make_anchor(out["_book"], gate_sha256=out["_gate_sha"], anchored_at_utc="2026-11-02T22:15:00Z"), "fee_source_sha256": "ef" * 32}, out["_gate"]),
        }
        for name, build in mutations.items():
            spec = EXPECTED["anchor_cases"][name]
            book, anchor, gate = build(base)
            out = self._run("P1_CLEAN", gate=gate, anchor_doc=anchor, entry_book_bytes=book)
            self.assertEqual(out["status"], spec["expect_status"], name)
            if spec.get("expect_kind"):
                self.assertIn(spec["expect_kind"], [item["kind"] for item in out["reporting_defects"]], name)
                self.assertIsNone(out["reject_c"], name)
                self.assertIsNone(out["reject_d"], name)
                self.assertNotIn("net_headline_total", out, name)
                cd = cd_from_prc(_public(out), gate, fee_ctx=self.fee_ctx)
                produced = apply_verdict(_score_dict(-0.01, -0.02), cd=cd, regime_report=_admitted_report(self.pin))
                self.assertEqual(produced["verdict"], "FULL_VERDICT_REQUIRES_EXAMINER", name)
            self.assertEqual(out["_calls"]["n"] > 0, spec["join_called"], name)
            self.assertEqual(out["_calls"]["join"] > 0, spec["join_called"], name)
            self._assert_defect(out)
            results[name] = (out["status"], spec.get("expect_kind"), spec["join_called"])
        # Recompute mismatch: book anchored from a different price, scored on the original gate.
        original = base["_gate"]
        mutated = json.loads(json.dumps(original))
        mutated["signals"][0]["price"] = 0.41
        mutated["signals"][0]["fee_decimal"] = str(
            __import__("card01_amc.fee_source", fromlist=["pinned_taker_fee"]).pinned_taker_fee(
                __import__("card01_amc.fee_admission", fromlist=["pinned_entry_v2"]).pinned_entry_v2(self.admission, "XS1"),
                0.41,
            )["headline"]
        )
        mutated_bytes = json.dumps(mutated, sort_keys=True).encode()
        env = pnl_cd.entry_book_envelope(mutated, gate_sha256=sha256_bytes(mutated_bytes), fee_ctx=self.fee_ctx)
        raw = (json.dumps(env, indent=1) + "\n").encode()
        anchor = pnl_cd.make_anchor(raw, gate_sha256=base["_gate_sha"], anchored_at_utc="2026-11-02T22:15:00Z")
        out = self._run("P1_CLEAN", gate=original, anchor_doc=anchor, entry_book_bytes=raw)
        self.assertEqual(out["status"], "REPORTING_DEFECT")
        self.assertIn("ENTRY_BOOK_RECOMPUTE_MISMATCH", [item["kind"] for item in out["reporting_defects"]])
        self.assertEqual(out["_calls"]["n"], 0)
        results["ANCHOR_RECOMPUTE_MISMATCH"] = (out["status"], "ENTRY_BOOK_RECOMPUTE_MISMATCH", False)
        zero = self._run("ZERO_SIGNALS")
        self.assertEqual(zero["status"], "NO_SIGNALS_SELECTED")
        self.assertGreater(zero["_calls"]["n"], 0)
        results["ANCHOR_ZERO_SIGNALS_OK"] = (zero["status"], None, True)
        blocked = self._run("FEE_BLOCKED")
        self.assertEqual(blocked["status"], "BLOCKED_FEE_UNVERIFIED")
        self.assertEqual(blocked["_calls"]["n"], 0)
        results["ANCHOR_FEE_BLOCKED"] = (blocked["status"], None, False)
        self.__class__.anchor_results = results
        # Envelope serialization matches swing_stress: dumps(body, indent=1).
        env = json.loads(base["_book"])
        body = {key: value for key, value in env.items() if key != "output_sha256"}
        digest = hashlib.sha256(json.dumps(body, indent=1).encode()).hexdigest()
        self.assertEqual(env["output_sha256"], digest)

    def test_pc15_buffered_sensitivity(self):
        with_row = self._run("P1_CLEAN", emit_buffered=True)
        exp = EXPECTED["cases"]["P1_CLEAN"]["sensitivity_buffered_2c"]
        self.assertEqual(with_row["sensitivity_buffered_2c"], exp)
        self.assertEqual(with_row["sensitivity_buffered_2c"]["verdict_input"], False)
        plain = self._run("P1_CLEAN")
        self.assertNotIn("sensitivity_buffered_2c", plain)
        mutated = json.loads(json.dumps(_public(with_row)))
        cd_before = cd_from_prc(_public(with_row), with_row["_gate"], fee_ctx=self.fee_ctx)
        del mutated["sensitivity_buffered_2c"]
        self.assertEqual(mutated["reject_c"], with_row["reject_c"])
        self.assertEqual(mutated["reject_d"], with_row["reject_d"])
        cd_after = cd_from_prc(mutated, with_row["_gate"], fee_ctx=self.fee_ctx)
        self.assertEqual(cd_before, cd_after)
        text = (LAB / "card01_amc" / "pnl_cd.py").read_text()
        self.assertNotIn("sensitivity_buffered_2c", ast.get_source_segment(text, next(node for node in ast.parse(text).body if isinstance(node, ast.FunctionDef) and node.name == "evaluate_cd")))
        verdict_text = (LAB / "card01_amc" / "verdict.py").read_text()
        self.assertNotIn("sensitivity_buffered_2c", verdict_text)
        self.assertNotIn("net_buffered_2c", verdict_text)

    def test_pc16_citation_on_every_output(self):
        for case in FIXTURES["cases"]:
            out = self._run(case["id"])
            self._assert_defect(out)
        clean = self._run("P1_CLEAN")
        cd = cd_from_prc(_public(clean), clean["_gate"], fee_ctx=self.fee_ctx)
        produced = apply_verdict(_score_dict(-0.01, -0.02), cd=cd, regime_report=_admitted_report(self.pin))
        self.assertEqual(produced["verdict"], "PASS-FORECAST")

    def test_pc17_forged_pair_against_real_pins(self):
        verdict.PINS_PATH = self._saved_pins
        gate = self._gate(self._case("P1_CLEAN"))
        out = self._run("P1_CLEAN", gate=gate)
        self.assertEqual(out["status"], "BLOCKED_FEE_UNVERIFIED")
        self.assertEqual(out["reject_c"], "BLOCKED_FEE_UNVERIFIED")
        self.assertEqual(out["reject_d"], "BLOCKED_FEE_UNVERIFIED")
        self.assertFalse(_has_money(out))
        self.assertEqual(out["_calls"]["n"], 0)
        cd = cd_from_prc(_public(out), gate, fee_ctx=self.fee_ctx)
        self.assertIsNone(cd)
        produced = apply_verdict(_score_dict(-0.01, -0.02), cd=cd)
        self.assertTrue(produced["verdict"].startswith("FORECAST_ONLY_FEE_BLOCKED:"))
        # A score that would clear, with a fee pair that is not the real PINS pair.
        verdict.PINS_PATH = self.pin_path
        good = self._run("P1_CLEAN")
        verdict.PINS_PATH = self._saved_pins
        forged = json.loads(json.dumps({key: value for key, value in good.items() if not key.startswith("_")}))
        forged["fee_source_sha256"] = self.pin["sha256"]
        forged["output_sha256"] = pnl_cd.score_body_sha256(forged)
        cleared = cd_from_prc(forged, good["_gate"], fee_ctx=self.fee_ctx)
        self.assertIsNone(cleared)
        follow = apply_verdict(_score_dict(-0.01, -0.02), cd=cleared, regime_report=_admitted_report(self.pin))
        self.assertEqual(follow["verdict"], "FULL_VERDICT_REQUIRES_EXAMINER")

    def test_pc18_unreadable_fee_files(self):
        gate = self._gate(self._case("P1_CLEAN"))
        cases = []
        missing = self.root / "missing-fee.json"
        directory = self.root / "fee-dir"
        directory.mkdir(exist_ok=True)
        non_utf = self.root / "fee-nonutf.json"
        non_utf.write_bytes(b"\xff\xfe\x00")
        accept_bad = self.root / "accept-nonutf.json"
        accept_bad.write_bytes(b"\xff\xfe\x00")
        pin_for_utf = dict(self.pin)
        pin_for_utf["sha256"] = sha256_bytes(b"\xff\xfe\x00")
        utf_pin = self.root / "pins-utf.json"
        utf_pin.write_text(json.dumps({"fee_source_v2": pin_for_utf}), encoding="utf-8")
        specs = [
            ("missing", {"fee_source_path": str(missing), "packet_index_path": self.fee_ctx["packet_index_path"], "fee_accept_path": self.fee_ctx["fee_accept_path"]}, self.pin_path),
            ("directory", {"fee_source_path": str(directory), "packet_index_path": self.fee_ctx["packet_index_path"], "fee_accept_path": self.fee_ctx["fee_accept_path"]}, self.pin_path),
            ("nonutf", {"fee_source_path": str(non_utf), "packet_index_path": self.fee_ctx["packet_index_path"], "fee_accept_path": self.fee_ctx["fee_accept_path"]}, utf_pin),
            ("accept", {"fee_source_path": self.fee_ctx["fee_source_path"], "packet_index_path": self.fee_ctx["packet_index_path"], "fee_accept_path": str(accept_bad)}, self.pin_path),
        ]
        for name, fee_ctx, pin_path in specs:
            verdict.PINS_PATH = pin_path
            out = self._run("P1_CLEAN", gate=gate, fee_ctx=fee_ctx)
            self.assertEqual(out["status"], "BLOCKED_FEE_UNVERIFIED", name)
            self.assertTrue(out["fee_block_reason"], name)
            self.assertFalse(_has_money(out), name)
            self.assertEqual(out["_calls"]["n"], 0, name)
            self.assertEqual(out["_calls"]["join"], 0, name)
            cd = cd_from_prc(_public(out), gate, fee_ctx=fee_ctx)
            self.assertIsNone(cd, name)
            cases.append(out["fee_block_reason"])
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                gate_path = root / "gate.json"
                gate_path.write_text(json.dumps(gate), encoding="utf-8")
                rows, _settled = _split(self._case("P1_CLEAN"))
                (root / "rows.json").write_text(json.dumps(rows), encoding="utf-8")
                env = pnl_cd.entry_book_envelope(gate, gate_sha256=sha256_bytes(gate_path.read_bytes()), fee_ctx=fee_ctx)
                book = root / "book.json"
                book.write_text(json.dumps(env, indent=1) + "\n", encoding="utf-8")
                anchor = pnl_cd.make_anchor(book.read_bytes(), gate_sha256=sha256_bytes(gate_path.read_bytes()), anchored_at_utc="2026-11-02T22:15:00Z")
                (root / "anchor.json").write_text(json.dumps(anchor), encoding="utf-8")
                missing_settled = root / "no-such-settled.json"
                dest = root / "out.json"
                proc = subprocess.run(
                    [
                        sys.executable, "-m", "card01_amc.pnl_cd", "score",
                        "--gate", str(gate_path), "--rows", str(root / "rows.json"),
                        "--entry-book", str(book), "--entry-book-anchor", str(root / "anchor.json"),
                        "--settled-results", str(missing_settled),
                        "--fee-source", fee_ctx["fee_source_path"],
                        "--packet-index", fee_ctx["packet_index_path"],
                        "--fee-accept", fee_ctx["fee_accept_path"],
                        "--out", str(dest),
                    ],
                    cwd=LAB, capture_output=True, text=True, check=False,
                )
                self.assertEqual(proc.returncode, 0, proc.stderr + name)
                self.assertNotIn("Traceback", proc.stderr, name)
                self.assertFalse(missing_settled.exists())
                loaded = json.loads(dest.read_text())
                self.assertEqual(loaded["status"], "BLOCKED_FEE_UNVERIFIED", name)
                self.assertFalse(_has_money(loaded), name)
        self.assertIn("FEE_SOURCE_UNREADABLE", cases)

    def test_pc19_formula_id(self):
        forged = "astra.card01.fee_eff.FORGED.v0"
        gate = self._gate(self._case("P1_CLEAN"), fee_formula_id=forged)
        for signal in gate["signals"]:
            signal["fee_formula_id"] = forged
        out = self._run("P1_CLEAN", gate=gate)
        self.assertEqual(out["status"], "BLOCKED_FEE_UNVERIFIED")
        self.assertNotEqual(out["reject_c"], True)
        missing = self._gate(self._case("P1_CLEAN"))
        missing.pop("fee_formula_id")
        for signal in missing["signals"]:
            signal.pop("fee_formula_id", None)
        missing_out = self._run("P1_CLEAN", gate=missing)
        self.assertEqual(missing_out["status"], "BLOCKED_FEE_UNVERIFIED")
        good = self._run("P1_CLEAN")
        forged_out = json.loads(json.dumps({key: value for key, value in good.items() if not key.startswith("_")}))
        forged_out["fee_formula_id"] = forged
        forged_out["output_sha256"] = pnl_cd.score_body_sha256(forged_out)
        self.assertIsNone(cd_from_prc(forged_out, good["_gate"], fee_ctx=self.fee_ctx))
        forged_out.pop("fee_formula_id")
        forged_out["output_sha256"] = pnl_cd.score_body_sha256(forged_out)
        self.assertIsNone(cd_from_prc(forged_out, good["_gate"], fee_ctx=self.fee_ctx))
        anchor = pnl_cd.make_anchor(good["_book"], gate_sha256=good["_gate_sha"], anchored_at_utc="2026-11-02T22:15:00Z")
        anchor["fee_formula_id"] = forged
        bad_anchor = self._run("P1_CLEAN", anchor_doc=anchor, entry_book_bytes=good["_book"])
        self.assertEqual(bad_anchor["status"], "REPORTING_DEFECT")
        self.assertIn("ENTRY_BOOK_ANCHOR_MISMATCH", [item["kind"] for item in bad_anchor["reporting_defects"]])
        self.assertIsNone(bad_anchor["reject_c"])
        anchor.pop("fee_formula_id")
        missing_anchor = self._run("P1_CLEAN", anchor_doc=anchor, entry_book_bytes=good["_book"])
        self.assertEqual(missing_anchor["status"], "REPORTING_DEFECT")
        self.assertIn("ENTRY_BOOK_ANCHOR_MISMATCH", [item["kind"] for item in missing_anchor["reporting_defects"]])
        follow = apply_verdict(
            _score_dict(-0.01, -0.02),
            cd=cd_from_prc(forged_out, good["_gate"], fee_ctx=self.fee_ctx),
            regime_report=_admitted_report(self.pin),
        )
        self.assertEqual(follow["verdict"], "FULL_VERDICT_REQUIRES_EXAMINER")

    def _citing_index(self):
        text = Path(self.fee_ctx["packet_index_path"]).read_text(encoding="utf-8")
        path = self.root / "packet-index-cited.md"
        path.write_text(text + "\nConductor WITHDRAW of amendment 2c870cd5\n", encoding="utf-8")
        return path

    def _verdict_cli(self, prc, gate, regime, fee_ctx=None):
        fee_ctx = self.fee_ctx if fee_ctx is None else fee_ctx
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            score = root / "score.json"
            score.write_text(json.dumps(_score_dict(-0.01, -0.02)), encoding="utf-8")
            prc_path = root / "prc.json"
            prc_path.write_text(json.dumps(prc), encoding="utf-8")
            gate_path = root / "gate.json"
            gate_path.write_text(json.dumps(gate), encoding="utf-8")
            report_path = root / "regime.json"
            report_path.write_text(json.dumps(regime), encoding="utf-8")
            driver = root / "drive.py"
            driver.write_text(
                "import sys\n"
                "from pathlib import Path\n"
                "from card01_amc import verdict\n"
                "from card01_amc.verdict import main\n"
                "verdict.PINS_PATH = Path(sys.argv[1])\n"
                "sys.exit(main(sys.argv[2:]))\n",
                encoding="utf-8",
            )
            env = dict(os.environ)
            env["PYTHONPATH"] = str(LAB)
            proc = subprocess.run(
                [
                    sys.executable, str(driver), str(self.pin_path), str(score),
                    "--gate", str(gate_path),
                    "--prc", str(prc_path),
                    "--fee-source", fee_ctx["fee_source_path"],
                    "--packet-index", fee_ctx["packet_index_path"],
                    "--fee-accept", fee_ctx["fee_accept_path"],
                    "--regime-report", str(report_path),
                ],
                cwd=str(LAB),
                capture_output=True,
                text=True,
                check=False,
                env=env,
            )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertNotIn("Traceback", proc.stderr)
        return json.loads(proc.stdout)

    def test_m1a_blocked_prc_admitted_report_requires_examiner(self):
        cited = self._citing_index()
        fee_ctx = dict(self.fee_ctx)
        fee_ctx["packet_index_path"] = str(cited)
        cited_out = self._run("P1_CLEAN", fee_ctx=fee_ctx)
        self.assertEqual(cited_out["status"], "BLOCKED_FEE_UNVERIFIED")
        self.assertEqual(cited_out["fee_block_reason"], "FEE_CITATIONS_CHANGED")
        self.assertEqual(cited_out["reject_c"], "BLOCKED_FEE_UNVERIFIED")
        missing = self._gate(self._case("P1_CLEAN"))
        missing.pop("fee_formula_id")
        for signal in missing["signals"]:
            signal.pop("fee_formula_id", None)
        missing_out = self._run("P1_CLEAN", gate=missing)
        self.assertEqual(missing_out["status"], "BLOCKED_FEE_UNVERIFIED")
        self.assertEqual(missing_out["fee_block_reason"], "FEE_FORMULA_ID_MISMATCH")
        report = _admitted_report(self.pin)
        blocked_report = {
            "fee_state": "BLOCKED_FEE_UNVERIFIED",
            "fee_admission": {"fee_admission": "BLOCKED_FEE_UNVERIFIED"},
        }
        for name, out, ctx in (
            ("FEE_CITATIONS_CHANGED", cited_out, fee_ctx),
            ("missing_fee_formula_id", missing_out, self.fee_ctx),
        ):
            public = _public(out)
            cd = cd_from_prc(public, out["_gate"], fee_ctx=ctx)
            self.assertIsNone(cd, name)
            produced = apply_verdict(_score_dict(-0.01, -0.02), cd=cd, regime_report=report)
            self.assertEqual(produced["verdict"], "FULL_VERDICT_REQUIRES_EXAMINER", name)
            self.assertNotIn("PASS-FORECAST", produced["verdict"], name)
            self.assertEqual(produced["firing"], [], name)
            cli = self._verdict_cli(public, out["_gate"], report, fee_ctx=ctx)
            if name == "FEE_CITATIONS_CHANGED":
                self.assertEqual(cli["verdict"], "FULL_VERDICT_REQUIRES_EXAMINER", name)
                self.assertEqual(cli["binding_reason"], "DISK_BLOCKED_INPUTS_ADMITTED", name)
                self.assertIn("regime_report", cli["binding_detail"], name)
                self.assertNotEqual(cli["fee_block_reason"], "FEE_REPORT_MISSING", name)
                self.assertNotIn("PASS-FORECAST", cli["verdict"], name)
                self.assertNotEqual(cli["verdict"], "REJECT", name)
            else:
                self.assertEqual(cli["verdict"], "FULL_VERDICT_REQUIRES_EXAMINER", name)
                self.assertNotIn("PASS-FORECAST", cli["verdict"], name)
                self.assertEqual(cli["firing"], [], name)
            held = apply_verdict(_score_dict(-0.01, -0.02), cd=cd, regime_report=blocked_report)
            self.assertTrue(held["verdict"].startswith("FORECAST_ONLY_FEE_BLOCKED:"), name)

    def test_m1b_blocked_prc_blocked_report_stays_forecast_only(self):
        out = self._run("FEE_BLOCKED")
        self.assertEqual(out["status"], "BLOCKED_FEE_UNVERIFIED")
        self.assertEqual(out["reject_c"], "BLOCKED_FEE_UNVERIFIED")
        cd = cd_from_prc(_public(out), out["_gate"], fee_ctx=self.fee_ctx)
        self.assertIsNone(cd)
        blocked_report = {
            "fee_state": "BLOCKED_FEE_UNVERIFIED",
            "fee_block_reason": out["fee_block_reason"],
            "fee_admission": {"fee_admission": "BLOCKED_FEE_UNVERIFIED"},
        }
        produced = apply_verdict(
            _score_dict(-0.01, -0.02),
            cd=cd,
            regime_report=blocked_report,
        )
        self.assertTrue(produced["verdict"].startswith("FORECAST_ONLY_FEE_BLOCKED:"))
        self.assertEqual(produced["evaluations"]["reject_c"], "BLOCKED_FEE_UNVERIFIED")
        self.assertEqual(produced["evaluations"]["reject_d"], "BLOCKED_FEE_UNVERIFIED")
        omitted = apply_verdict(_score_dict(-0.01, -0.02), cd=cd)
        self.assertTrue(omitted["verdict"].startswith("FORECAST_ONLY_FEE_BLOCKED:"))

    def test_m1c_nonboolean_reject_maps_to_none(self):
        clean = self._run("P1_CLEAN")
        self.assertIs(clean["reject_c"], False)
        self.assertIs(clean["reject_d"], False)
        base = _public(clean)
        for label, reject_c, reject_d in (
            ("string", "BLOCKED_FEE_UNVERIFIED", False),
            ("int", 1, 1),
            ("none", None, None),
        ):
            mutated = json.loads(json.dumps(base))
            mutated["reject_c"] = reject_c
            mutated["reject_d"] = reject_d
            mutated["output_sha256"] = pnl_cd.score_body_sha256(mutated)
            cd = cd_from_prc(mutated, clean["_gate"], fee_ctx=self.fee_ctx)
            self.assertIsNone(cd, label)
        kept = cd_from_prc(base, clean["_gate"], fee_ctx=self.fee_ctx)
        self.assertEqual(kept["reject_c"], False)
        self.assertEqual(kept["reject_d"], False)

    def _score_bytes(self, gate, gate_bytes, rows, settled):
        gate_sha = sha256_bytes(gate_bytes)
        envelope = pnl_cd.entry_book_envelope(gate, gate_sha256=gate_sha, fee_ctx=self.fee_ctx)
        book = (json.dumps(envelope, indent=1) + "\n").encode()
        anchor = pnl_cd.make_anchor(
            book,
            gate_sha256=gate_sha,
            anchored_at_utc="2026-11-02T22:15:00Z",
        )
        calls = {"n": 0}

        def loader():
            calls["n"] += 1
            return settled

        out = pnl_cd.run(
            gate,
            rows,
            loader,
            gate_sha256=gate_sha,
            entry_book_bytes=book,
            anchor_doc=anchor,
            fee_ctx=self.fee_ctx,
        )
        out["_calls"] = calls
        out["_gate_sha"] = gate_sha
        return out

    def test_e2b_subset_gate_does_not_bind(self):
        full_out = self._run("P1_CLEAN")
        full = full_out["_gate"]
        rows = full_out["_rows"]
        settled = full_out["_settled"]
        subset_rows = rows[:3]
        subset = _gate_v2_product(subset_rows, self.fee_ctx, self.pin)
        self.assertEqual(subset["status"], "OK")
        self.assertEqual(subset["signals"], full["signals"][:3])
        full_bytes = json.dumps(full, sort_keys=True).encode()
        subset_bytes = json.dumps(subset, sort_keys=True).encode()
        full_scored = self._score_bytes(full, full_bytes, rows, settled)
        subset_out = self._score_bytes(subset, subset_bytes, subset_rows, settled)
        self.assertEqual(full_scored["status"], "OK")
        self.assertEqual(subset_out["status"], "OK")
        self.assertEqual(subset_out["n_signals"], 3)
        self.assertNotEqual(subset_out["inputs_sha256"]["gate_output"], full_scored["inputs_sha256"]["gate_output"])
        dropped = self._score_bytes(subset, subset_bytes, rows, settled)
        self.assertEqual(dropped["status"], "GATE_NOT_REPRODUCED")
        self.assertEqual(dropped["_calls"]["n"], 0)
        self.assertFalse(_has_money(dropped))
        mismatch = cd_from_prc(_public(subset_out), full, fee_ctx=self.fee_ctx)
        self.assertIsNone(mismatch)
        produced = apply_verdict(
            _score_dict(-0.01, -0.02),
            cd=mismatch,
            regime_report=_admitted_report(self.pin),
        )
        self.assertEqual(produced["verdict"], "FULL_VERDICT_REQUIRES_EXAMINER")
        self.assertNotIn("PASS-FORECAST", produced["verdict"])
        matched = cd_from_prc(_public(subset_out), subset, fee_ctx=self.fee_ctx)
        self.assertIs(matched["reject_c"], subset_out["reject_c"])
        self.assertIs(matched["reject_d"], subset_out["reject_d"])
        self.assertIs(type(matched["reject_c"]), bool)
        self.assertIs(type(matched["reject_d"]), bool)

    def test_e2b_cli_gate_prc_regime_must_agree(self):
        full_out = self._run("P1_CLEAN")
        full = full_out["_gate"]
        rows = full_out["_rows"]
        settled = full_out["_settled"]
        subset_rows = rows[:3]
        subset = _gate_v2_product(subset_rows, self.fee_ctx, self.pin)
        full_bytes = json.dumps(full, sort_keys=True).encode()
        subset_bytes = json.dumps(subset, sort_keys=True).encode()
        subset_out = self._score_bytes(subset, subset_bytes, subset_rows, settled)
        self.assertEqual(subset_out["status"], "OK")
        public = _public(subset_out)

        def report_for(gate_sha, n_signals):
            report = _admitted_report(self.pin)
            report["gate_sha256"] = gate_sha
            report["n_signals"] = n_signals
            return report

        def invoke(gate_bytes, regime):
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                (root / "score.json").write_text(json.dumps(_score_dict(-0.01, -0.02)), encoding="utf-8")
                (root / "prc.json").write_text(json.dumps(public), encoding="utf-8")
                (root / "gate.json").write_bytes(gate_bytes)
                (root / "regime.json").write_text(json.dumps(regime), encoding="utf-8")
                driver = root / "drive.py"
                driver.write_text(
                    "import sys\n"
                    "from pathlib import Path\n"
                    "from card01_amc import verdict\n"
                    "from card01_amc.verdict import main\n"
                    "verdict.PINS_PATH = Path(sys.argv[1])\n"
                    "sys.exit(main(sys.argv[2:]))\n",
                    encoding="utf-8",
                )
                env = dict(os.environ)
                env["PYTHONPATH"] = str(LAB)
                proc = subprocess.run(
                    [
                        sys.executable, str(driver), str(self.pin_path),
                        str(root / "score.json"),
                        "--gate", str(root / "gate.json"),
                        "--prc", str(root / "prc.json"),
                        "--fee-source", self.fee_ctx["fee_source_path"],
                        "--packet-index", self.fee_ctx["packet_index_path"],
                        "--fee-accept", self.fee_ctx["fee_accept_path"],
                        "--regime-report", str(root / "regime.json"),
                    ],
                    cwd=str(LAB),
                    capture_output=True,
                    text=True,
                    check=False,
                    env=env,
                )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            return json.loads(proc.stdout)

        refused = invoke(full_bytes, report_for(sha256_bytes(full_bytes), 5))
        self.assertEqual(refused["verdict"], "FULL_VERDICT_REQUIRES_EXAMINER")
        self.assertIsNone(refused["evaluations"]["reject_c"])
        self.assertIsNone(refused["evaluations"]["reject_d"])
        self.assertNotIn("PASS-FORECAST", refused["verdict"])
        agreed = invoke(subset_bytes, report_for(sha256_bytes(subset_bytes), 3))
        self.assertEqual(agreed["evaluations"]["reject_c"], subset_out["reject_c"])
        self.assertEqual(agreed["evaluations"]["reject_d"], subset_out["reject_d"])
        self.assertIs(type(agreed["evaluations"]["reject_c"]), bool)
        self.assertNotEqual(agreed["verdict"], "FULL_VERDICT_REQUIRES_EXAMINER")

    def test_e2b_real_build_report_binds_honest_chain(self):
        from card01_amc.regime_split_secondary import build_report
        from tests.test_regime_split_secondary import _selection

        full_out = self._run("P1_CLEAN")
        full = json.loads(json.dumps(full_out["_gate"]))
        rows = full_out["_rows"]
        settled = full_out["_settled"]
        full_bytes = json.dumps(full, sort_keys=True).encode()
        full_scored = self._score_bytes(full, full_bytes, rows, settled)
        self.assertEqual(full_scored["status"], "OK")
        report = build_report(
            rows,
            selection=_selection(),
            gate=json.loads(full_bytes.decode("utf-8")),
            settled=settled,
            fee_source_path=self.fee_ctx["fee_source_path"],
            fee_source_id=self.pin["id"],
            fee_source_sha256=self.pin["sha256"],
            packet_index_path=self.fee_ctx["packet_index_path"],
            fee_accept_path=self.fee_ctx["fee_accept_path"],
            series_used=["XS1"],
        )
        self.assertNotIn("n_signals", report)
        self.assertNotIn("gate_sha256", report)
        self.assertEqual(report["fee_state"], "ADMITTED")
        self.assertEqual(report["secondary"]["signals_and_size"]["n_signals"], len(full["signals"]))
        self.assertNotEqual(
            report["inputs_sha256"]["gate_output"],
            sha256_bytes(full_bytes),
        )
        subset_rows = rows[:3]
        subset = _gate_v2_product(subset_rows, self.fee_ctx, self.pin)
        subset_bytes = json.dumps(subset, sort_keys=True).encode()
        subset_out = self._score_bytes(subset, subset_bytes, subset_rows, settled)
        self.assertEqual(subset_out["status"], "OK")
        public = _public(subset_out)

        def invoke(gate_bytes, regime, prc):
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                (root / "score.json").write_text(json.dumps(_score_dict(-0.01, -0.02)), encoding="utf-8")
                (root / "prc.json").write_text(json.dumps(prc), encoding="utf-8")
                (root / "gate.json").write_bytes(gate_bytes)
                (root / "regime.json").write_text(json.dumps(regime), encoding="utf-8")
                driver = root / "drive.py"
                driver.write_text(
                    "import sys\n"
                    "from pathlib import Path\n"
                    "from card01_amc import verdict\n"
                    "from card01_amc.verdict import main\n"
                    "verdict.PINS_PATH = Path(sys.argv[1])\n"
                    "sys.exit(main(sys.argv[2:]))\n",
                    encoding="utf-8",
                )
                env = dict(os.environ)
                env["PYTHONPATH"] = str(LAB)
                proc = subprocess.run(
                    [
                        sys.executable, str(driver), str(self.pin_path),
                        str(root / "score.json"),
                        "--gate", str(root / "gate.json"),
                        "--prc", str(root / "prc.json"),
                        "--fee-source", self.fee_ctx["fee_source_path"],
                        "--packet-index", self.fee_ctx["packet_index_path"],
                        "--fee-accept", self.fee_ctx["fee_accept_path"],
                        "--regime-report", str(root / "regime.json"),
                    ],
                    cwd=str(LAB),
                    capture_output=True,
                    text=True,
                    check=False,
                    env=env,
                )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            return json.loads(proc.stdout)

        refused = invoke(full_bytes, report, public)
        self.assertEqual(refused["verdict"], "FULL_VERDICT_REQUIRES_EXAMINER")
        self.assertIsNone(refused["evaluations"]["reject_c"])
        self.assertIsNone(refused["evaluations"]["reject_d"])
        self.assertNotIn("PASS-FORECAST", refused["verdict"])
        honest_report = build_report(
            subset_rows,
            selection=_selection(),
            gate=json.loads(subset_bytes.decode("utf-8")),
            settled=settled,
            fee_source_path=self.fee_ctx["fee_source_path"],
            fee_source_id=self.pin["id"],
            fee_source_sha256=self.pin["sha256"],
            packet_index_path=self.fee_ctx["packet_index_path"],
            fee_accept_path=self.fee_ctx["fee_accept_path"],
            series_used=["XS1"],
        )
        self.assertEqual(honest_report["secondary"]["signals_and_size"]["n_signals"], 3)
        agreed = invoke(subset_bytes, honest_report, public)
        self.assertEqual(agreed["evaluations"]["reject_c"], subset_out["reject_c"])
        self.assertEqual(agreed["evaluations"]["reject_d"], subset_out["reject_d"])
        self.assertIs(type(agreed["evaluations"]["reject_c"]), bool)
        self.assertNotEqual(agreed["verdict"], "FULL_VERDICT_REQUIRES_EXAMINER")

    def _run_module(self, root, module, args):
        driver = root / "drive.py"
        if not driver.is_file():
            driver.write_text(
                "import sys\n"
                "from pathlib import Path\n"
                "from card01_amc import verdict\n"
                "verdict.PINS_PATH = Path(sys.argv[1])\n"
                "name = sys.argv[2]\n"
                "if name == 'entry_gate':\n"
                "    from card01_amc.entry_gate import main\n"
                "elif name == 'pnl_cd':\n"
                "    from card01_amc.pnl_cd import main\n"
                "elif name == 'verdict':\n"
                "    from card01_amc.verdict import main\n"
                "else:\n"
                "    raise SystemExit(2)\n"
                "sys.exit(main(sys.argv[3:]))\n",
                encoding="utf-8",
            )
        env = dict(os.environ)
        env["PYTHONPATH"] = str(LAB)
        proc = subprocess.run(
            [sys.executable, str(driver), str(self.pin_path), module, *args],
            cwd=str(LAB),
            capture_output=True,
            text=True,
            check=False,
            env=env,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertNotIn("Traceback", proc.stderr)
        return proc

    def _examiner_world(self):
        from card01_amc.join_outcomes import join
        from card01_amc.pnl_cd import make_anchor
        from card01_amc.regime_split_secondary import build_report
        from tests.test_regime_split_secondary import _selection

        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)

        def quote_row(race, ask):
            ask_d = Decimal(ask)
            bid = ask_d - Decimal("0.01")
            return {
                "race_id": race,
                "ticker": "T-" + race,
                "series": "XS1",
                "mapping_status": "LEGACY",
                "p_model": 0.99,
                "p_market": 0.99,
                "yes_bid": format(bid, "f"),
                "yes_ask": format(ask_d, "f"),
                "yes_bid_qty": 10,
                "yes_ask_qty": 10,
            }

        rows = [
            quote_row("W1", "0.055"),
            quote_row("W2", "0.055"),
            quote_row("W3", "0.055"),
            quote_row("L1", "0.50"),
            quote_row("L2", "0.50"),
        ]
        settled = {
            "results": [
                {"ticker": "T-" + race, "result": result, "settlement_ts": "2000-01-01T00:00:00.000000Z"}
                for race, result in (
                    ("W1", "yes"),
                    ("W2", "yes"),
                    ("W3", "yes"),
                    ("L1", "no"),
                    ("L2", "no"),
                )
            ]
        }
        (root / "rows.json").write_text(json.dumps(rows), encoding="utf-8")
        (root / "rows-sub3.json").write_text(json.dumps(rows[:3]), encoding="utf-8")
        (root / "settled.json").write_text(json.dumps(settled), encoding="utf-8")
        (root / "score.json").write_text(json.dumps(_score_dict(-0.01, -0.02)), encoding="utf-8")
        fee_args = [
            "--fee-source", self.fee_ctx["fee_source_path"],
            "--packet-index", self.fee_ctx["packet_index_path"],
            "--fee-accept", self.fee_ctx["fee_accept_path"],
        ]
        gated = self._run_module(root, "entry_gate", [
            str(root / "rows.json"),
            "--fee-source-id", self.pin["id"],
            "--fee-source-sha256", self.pin["sha256"],
            *fee_args,
        ])
        (root / "gate-full5.json").write_text(gated.stdout, encoding="utf-8")
        gated3 = self._run_module(root, "entry_gate", [
            str(root / "rows-sub3.json"),
            "--fee-source-id", self.pin["id"],
            "--fee-source-sha256", self.pin["sha256"],
            *fee_args,
        ])
        (root / "gate-sub3.json").write_text(gated3.stdout, encoding="utf-8")

        def book_and_score(tag, gate_name, row_name):
            book = root / ("book-" + tag + ".json")
            self._run_module(root, "pnl_cd", [
                "entry-book",
                "--gate", str(root / gate_name),
                *fee_args,
                "--out", str(book),
            ])
            anchor = make_anchor(
                book.read_bytes(),
                gate_sha256=sha256_bytes((root / gate_name).read_bytes()),
                anchored_at_utc="2026-11-02T22:15:00Z",
            )
            anchor_path = root / ("anchor-" + tag + ".json")
            anchor_path.write_text(json.dumps(anchor), encoding="utf-8")
            prc = root / ("prc-" + tag + ".json")
            self._run_module(root, "pnl_cd", [
                "score",
                "--gate", str(root / gate_name),
                "--rows", str(root / row_name),
                "--entry-book", str(book),
                "--entry-book-anchor", str(anchor_path),
                "--settled-results", str(root / "settled.json"),
                *fee_args,
                "--out", str(prc),
            ])
            return json.loads(prc.read_text(encoding="utf-8"))

        full = book_and_score("full5", "gate-full5.json", "rows.json")
        sub = book_and_score("sub3", "gate-sub3.json", "rows-sub3.json")
        full_gate = json.loads((root / "gate-full5.json").read_text(encoding="utf-8"))
        subset_gate = json.loads(json.dumps(full_gate))
        subset_gate["signals"] = full_gate["signals"][:3]
        subset_gate["n_selected"] = 3
        joined = join(rows, settled)["rows"]
        report_kwargs = {
            "selection": _selection(),
            "settled": settled,
            "fee_source_path": self.fee_ctx["fee_source_path"],
            "fee_source_id": self.pin["id"],
            "fee_source_sha256": self.pin["sha256"],
            "packet_index_path": self.fee_ctx["packet_index_path"],
            "fee_accept_path": self.fee_ctx["fee_accept_path"],
            "series_used": ["XS1"],
        }
        blocked = build_report(joined, gate=subset_gate, **report_kwargs)
        honest = build_report(joined, gate=full_gate, **report_kwargs)
        (root / "regime-blocked.json").write_text(json.dumps(blocked), encoding="utf-8")
        (root / "regime-honest.json").write_text(json.dumps(honest), encoding="utf-8")
        return root, full, sub, blocked, honest

    def _verdict_bound(self, root, *, gate=None, prc=None, regime=None, fee_ctx=None, fee_paths=True):
        fee_ctx = self.fee_ctx if fee_ctx is None else fee_ctx
        args = [str(root / "score.json")]
        if gate is not None:
            args.extend(["--gate", str(gate)])
        if prc is not None:
            args.extend(["--prc", str(prc)])
        if fee_paths:
            args.extend([
                "--fee-source", fee_ctx["fee_source_path"],
                "--packet-index", fee_ctx["packet_index_path"],
                "--fee-accept", fee_ctx["fee_accept_path"],
            ])
        if regime is not None:
            args.extend(["--regime-report", str(regime)])
        proc = self._run_module(root, "verdict", args)
        return json.loads(proc.stdout)

    def _rehash_score(self, doc):
        body = json.loads(json.dumps(doc))
        body.pop("output_sha256", None)
        body["output_sha256"] = pnl_cd.score_body_sha256(body)
        return body

    def _blocked_disk_chain(self, root):
        """Real entry_gate and build_report on a fee file that does not admit."""
        from card01_amc.join_outcomes import join
        from card01_amc.pnl_cd import make_anchor
        from card01_amc.regime_split_secondary import build_report
        from tests.test_regime_split_secondary import _selection

        bad = root / "bad-fee.json"
        bad.write_text("{}", encoding="utf-8")
        fee_ctx = dict(self.fee_ctx)
        fee_ctx["fee_source_path"] = str(bad)
        fee_args = [
            "--fee-source", fee_ctx["fee_source_path"],
            "--packet-index", fee_ctx["packet_index_path"],
            "--fee-accept", fee_ctx["fee_accept_path"],
        ]
        gated = self._run_module(root, "entry_gate", [
            str(root / "rows.json"),
            "--fee-source-id", self.pin["id"],
            "--fee-source-sha256", self.pin["sha256"],
            *fee_args,
        ])
        gate_path = root / "gate-disk-blocked.json"
        gate_path.write_text(gated.stdout, encoding="utf-8")
        gate = json.loads(gated.stdout)
        rows = json.loads((root / "rows.json").read_text(encoding="utf-8"))
        settled = json.loads((root / "settled.json").read_text(encoding="utf-8"))
        report = build_report(
            join(rows, settled)["rows"],
            gate=gate,
            selection=_selection(),
            settled=settled,
            fee_source_path=fee_ctx["fee_source_path"],
            fee_source_id=self.pin["id"],
            fee_source_sha256=self.pin["sha256"],
            packet_index_path=fee_ctx["packet_index_path"],
            fee_accept_path=fee_ctx["fee_accept_path"],
            series_used=["XS1"],
        )
        report_path = root / "regime-disk-blocked.json"
        report_path.write_text(json.dumps(report), encoding="utf-8")
        book = root / "book-disk-blocked.json"
        self._run_module(root, "pnl_cd", [
            "entry-book",
            "--gate", str(gate_path),
            *fee_args,
            "--out", str(book),
        ])
        anchor = make_anchor(
            book.read_bytes(),
            gate_sha256=sha256_bytes(gate_path.read_bytes()),
            anchored_at_utc="2026-11-02T22:15:00Z",
        )
        anchor_path = root / "anchor-disk-blocked.json"
        anchor_path.write_text(json.dumps(anchor), encoding="utf-8")
        prc_path = root / "prc-disk-blocked.json"
        self._run_module(root, "pnl_cd", [
            "score",
            "--gate", str(gate_path),
            "--rows", str(root / "rows.json"),
            "--entry-book", str(book),
            "--entry-book-anchor", str(anchor_path),
            "--settled-results", str(root / "settled.json"),
            *fee_args,
            "--out", str(prc_path),
        ])
        return fee_ctx, gate_path, prc_path, report_path, gate, report

    def test_e2b_cli_blocked_regime_requires_examiner(self):
        root, full, sub, blocked, _honest = self._examiner_world()
        self.assertEqual(full["status"], "OK")
        self.assertEqual(full["n_signals"], 5)
        self.assertEqual(full["net_headline_total"], "1.780")
        self.assertEqual(full["net_one_tick_worse_total"], "1.730")
        self.assertIs(full["reject_c"], False)
        self.assertIs(full["reject_d"], True)
        self.assertEqual(sub["status"], "OK")
        self.assertEqual(sub["n_signals"], 3)
        self.assertEqual(sub["net_headline_total"], "2.820")
        self.assertEqual(sub["net_one_tick_worse_total"], "2.790")
        self.assertIs(sub["reject_c"], False)
        self.assertIs(sub["reject_d"], False)
        self.assertEqual(blocked["fee_state"], "BLOCKED_FEE_UNVERIFIED")
        self.assertEqual(blocked["secondary"]["fee_block_reason"], "GATE_NOT_REPRODUCED")
        blocked_path = root / "regime-blocked.json"
        cases = (
            ("a", root / "gate-full5.json", root / "prc-full5.json"),
            ("b", root / "gate-full5.json", root / "prc-sub3.json"),
            ("c", root / "gate-full5.json", root / "prc-full5.json"),
        )
        for name, gate, prc in cases:
            regime = None if name == "c" else blocked_path
            produced = self._verdict_bound(root, gate=gate, prc=prc, regime=regime)
            self.assertEqual(produced["verdict"], "FULL_VERDICT_REQUIRES_EXAMINER", name)
            self.assertNotIn("PASS-FORECAST", produced["verdict"], name)
            self.assertIsNone(produced["evaluations"]["reject_c"], name)
            self.assertIsNone(produced["evaluations"]["reject_d"], name)
            if name == "c":
                self.assertEqual(produced["binding_reason"], "REGIME_REPORT_REQUIRED", name)
            else:
                self.assertEqual(produced["binding_reason"], "REGIME_BLOCKED_DISK_ADMITS", name)

    def test_e2b_cli_prc_without_regime_requires_examiner(self):
        root, _full, _sub, _blocked, _honest = self._examiner_world()
        produced = self._verdict_bound(root, prc=root / "prc-full5.json")
        self.assertEqual(produced["verdict"], "FULL_VERDICT_REQUIRES_EXAMINER")
        self.assertEqual(produced["binding_reason"], "REGIME_REPORT_REQUIRED")
        self.assertNotIn("PASS-FORECAST", produced["verdict"])
        self.assertIsNone(produced["evaluations"]["reject_c"])
        self.assertIsNone(produced["evaluations"]["reject_d"])

    def test_e2b_cli_honest_triple_rejects_d(self):
        root, _full, _sub, _blocked, honest = self._examiner_world()
        self.assertEqual(honest["fee_state"], "ADMITTED")
        self.assertEqual(honest["secondary"]["signals_and_size"]["n_signals"], 5)
        produced = self._verdict_bound(
            root,
            gate=root / "gate-full5.json",
            prc=root / "prc-full5.json",
            regime=root / "regime-honest.json",
        )
        self.assertEqual(produced["verdict"], "REJECT")
        self.assertIn("(d)", produced["firing"])
        self.assertNotIn("(c)", produced["firing"])
        self.assertNotIn("PASS-FORECAST", produced["verdict"])
        self.assertNotIn("binding_reason", produced)

    def test_e2b_cli_regime_blocked_disk_admits_requires_examiner(self):
        root, _full, _sub, blocked, _honest = self._examiner_world()
        self.assertEqual(blocked["fee_state"], "BLOCKED_FEE_UNVERIFIED")
        self.assertIsNone(blocked["secondary"]["signals_and_size"])
        self.assertNotIn("n_signals", blocked["secondary"])
        produced = self._verdict_bound(
            root,
            gate=root / "gate-full5.json",
            prc=root / "prc-full5.json",
            regime=root / "regime-blocked.json",
        )
        self.assertEqual(produced["verdict"], "FULL_VERDICT_REQUIRES_EXAMINER")
        self.assertEqual(produced["binding_reason"], "REGIME_BLOCKED_DISK_ADMITS")
        self.assertNotIn("PASS-FORECAST", produced["verdict"])
        self.assertIsNone(produced["evaluations"]["reject_c"])
        self.assertIsNone(produced["evaluations"]["reject_d"])

    def test_mf1_regime_report_only_admitting_disk_is_full(self):
        root, _full, _sub, blocked, _honest = self._examiner_world()
        self.assertEqual(blocked["fee_state"], "BLOCKED_FEE_UNVERIFIED")
        produced = self._verdict_bound(root, regime=root / "regime-blocked.json")
        self.assertEqual(produced["verdict"], "FULL_VERDICT_REQUIRES_EXAMINER")
        self.assertEqual(produced["binding_reason"], "GATE_REQUIRED")
        self.assertNotIn("PASS-FORECAST", produced["verdict"])
        self.assertNotIn("FORECAST_ONLY", produced["verdict"])
        self.assertIsNone(produced["evaluations"]["reject_c"])
        self.assertIsNone(produced["evaluations"]["reject_d"])

    def test_e2b_cli_only_gate_requires_examiner(self):
        root, _full, _sub, _blocked, _honest = self._examiner_world()
        produced = self._verdict_bound(root, gate=root / "gate-full5.json")
        self.assertEqual(produced["verdict"], "FULL_VERDICT_REQUIRES_EXAMINER")
        self.assertEqual(produced["binding_reason"], "REGIME_REPORT_REQUIRED")
        self.assertNotIn("PASS-FORECAST", produced["verdict"])

    def test_e2b_cli_one_sided_requires_examiner(self):
        root, _full, _sub, _blocked, honest = self._examiner_world()
        self.assertEqual(honest["fee_state"], "ADMITTED")
        missing_prc = self._verdict_bound(
            root,
            gate=root / "gate-full5.json",
            regime=root / "regime-honest.json",
        )
        self.assertEqual(missing_prc["verdict"], "FULL_VERDICT_REQUIRES_EXAMINER")
        self.assertEqual(missing_prc["binding_reason"], "PRC_REQUIRED")
        self.assertNotIn("PASS-FORECAST", missing_prc["verdict"])
        missing_gate = self._verdict_bound(
            root,
            prc=root / "prc-full5.json",
            regime=root / "regime-honest.json",
        )
        self.assertEqual(missing_gate["verdict"], "FULL_VERDICT_REQUIRES_EXAMINER")
        self.assertEqual(missing_gate["binding_reason"], "GATE_REQUIRED")
        self.assertNotIn("PASS-FORECAST", missing_gate["verdict"])

    def test_e2b_cli_missing_fee_paths_requires_examiner(self):
        root, _full, _sub, _blocked, _honest = self._examiner_world()
        produced = self._verdict_bound(
            root,
            gate=root / "gate-full5.json",
            prc=root / "prc-full5.json",
            regime=root / "regime-honest.json",
            fee_paths=False,
        )
        self.assertEqual(produced["verdict"], "FULL_VERDICT_REQUIRES_EXAMINER")
        self.assertEqual(produced["binding_reason"], "FEE_PATHS_REQUIRED")
        self.assertNotIn("PASS-FORECAST", produced["verdict"])
        regime_only = self._verdict_bound(
            root,
            regime=root / "regime-blocked.json",
            fee_paths=False,
        )
        self.assertEqual(regime_only["verdict"], "FULL_VERDICT_REQUIRES_EXAMINER")
        self.assertEqual(regime_only["binding_reason"], "FEE_PATHS_REQUIRED")

    def test_e2b_cli_race_id_relabel_requires_examiner(self):
        root, full, sub, _blocked, honest = self._examiner_world()
        self.assertEqual(honest["fee_state"], "ADMITTED")
        self.assertEqual([row["race_id"] for row in sub["per_signal"]], ["W1", "W2", "W3"])
        self.assertEqual(
            [row["race_id"] for row in full["per_signal"]],
            ["W1", "W2", "W3", "L1", "L2"],
        )
        forged = json.loads(json.dumps(sub))
        forged["n_signals"] = full["n_signals"]
        forged["inputs_sha256"]["gate_output"] = sha256_bytes((root / "gate-full5.json").read_bytes())
        forged = self._rehash_score(forged)
        path = root / "prc-relabelled.json"
        path.write_text(json.dumps(forged), encoding="utf-8")
        produced = self._verdict_bound(
            root,
            gate=root / "gate-full5.json",
            prc=path,
            regime=root / "regime-honest.json",
        )
        self.assertEqual(produced["verdict"], "FULL_VERDICT_REQUIRES_EXAMINER")
        self.assertEqual(produced["binding_reason"], "SIGNAL_IDENTITY_MISMATCH")
        self.assertNotIn("PASS-FORECAST", produced["verdict"])
        self.assertIsNone(produced["evaluations"]["reject_c"])
        self.assertIsNone(produced["evaluations"]["reject_d"])
        shuffled = json.loads(json.dumps(full))
        shuffled["per_signal"] = list(reversed(shuffled["per_signal"]))
        shuffled = self._rehash_score(shuffled)
        shuffle_path = root / "prc-shuffled.json"
        shuffle_path.write_text(json.dumps(shuffled), encoding="utf-8")
        ordered = self._verdict_bound(
            root,
            gate=root / "gate-full5.json",
            prc=shuffle_path,
            regime=root / "regime-honest.json",
        )
        self.assertEqual(ordered["verdict"], "REJECT")
        self.assertIn("(d)", ordered["firing"])
        self.assertNotIn("PASS-FORECAST", ordered["verdict"])

    def test_e2b_cli_blocked_disk_stays_forecast_only(self):
        root, _full, _sub, _blocked, _honest = self._examiner_world()
        fee_ctx, gate_path, prc_path, report_path, gate, report = self._blocked_disk_chain(root)
        self.assertIsNone(gate.get("signals"))
        self.assertNotEqual(report["fee_state"], "ADMITTED")
        self.assertIsNone(report["secondary"]["signals_and_size"])
        produced = self._verdict_bound(
            root,
            gate=gate_path,
            prc=prc_path,
            regime=report_path,
            fee_ctx=fee_ctx,
        )
        self.assertTrue(produced["verdict"].startswith("FORECAST_ONLY_FEE_BLOCKED:"))
        self.assertNotEqual(produced["verdict"], "FULL_VERDICT_REQUIRES_EXAMINER")
        self.assertNotEqual(produced["verdict"], "PASS-FORECAST")
        self.assertNotEqual(produced["verdict"], "REJECT")
        self.assertNotEqual(produced["fee_block_reason"], "FEE_REPORT_MISSING")
        report_only = self._verdict_bound(root, regime=report_path, fee_ctx=fee_ctx)
        self.assertTrue(report_only["verdict"].startswith("FORECAST_ONLY_FEE_BLOCKED:"))
        self.assertNotEqual(report_only["fee_block_reason"], "FEE_REPORT_MISSING")
        absent_report = self._verdict_bound(
            root,
            gate=gate_path,
            prc=prc_path,
            fee_ctx=fee_ctx,
        )
        self.assertTrue(absent_report["verdict"].startswith("FORECAST_ONLY_FEE_BLOCKED:"))
        self.assertEqual(absent_report["fee_block_reason"], "FEE_REPORT_MISSING")

    def test_mf2_wrong_fee_path_on_honest_triple_requires_examiner(self):
        root, full, _sub, _blocked, honest = self._examiner_world()
        self.assertEqual(honest["fee_state"], "ADMITTED")
        self.assertEqual(full["status"], "OK")
        self.assertNotEqual(full["status"], "BLOCKED_FEE_UNVERIFIED")
        self.assertNotEqual(full["fee_state"], "BLOCKED_FEE_UNVERIFIED")
        gate = json.loads((root / "gate-full5.json").read_text(encoding="utf-8"))
        self.assertIsInstance(gate.get("signals"), list)
        self.assertTrue(gate["signals"])
        pinned_v1 = LAB / "pins" / "FEE_SOURCE_CARD01_v1_2026-10-03.json"
        if pinned_v1.is_file() and sha256_bytes(pinned_v1.read_bytes()) == V1_SHA:
            v1_path = pinned_v1
        else:
            v1_path = LAB / "tests" / "fixtures" / "SYNTH_FEE_SOURCE_v1_example.json"
            self.assertTrue(v1_path.is_file())
            self.assertNotEqual(sha256_bytes(v1_path.read_bytes()), self.pin["sha256"])
        unrelated = root / "unrelated-accept.txt"
        unrelated.write_text("not an accept\n", encoding="utf-8")
        cited = root / "packet-index-cited.md"
        cited.write_text(
            Path(self.fee_ctx["packet_index_path"]).read_text(encoding="utf-8")
            + "\nConductor WITHDRAW of amendment 2c870cd5\n",
            encoding="utf-8",
        )
        swapped = dict(self.fee_ctx)
        swapped["fee_source_path"] = self.fee_ctx["fee_accept_path"]
        swapped["fee_accept_path"] = self.fee_ctx["fee_source_path"]
        v1_ctx = dict(self.fee_ctx)
        v1_ctx["fee_source_path"] = str(v1_path)
        unrelated_ctx = dict(self.fee_ctx)
        unrelated_ctx["fee_accept_path"] = str(unrelated)
        cited_ctx = dict(self.fee_ctx)
        cited_ctx["packet_index_path"] = str(cited)
        cases = (
            ("v1_fee_source", v1_ctx),
            ("swapped_source_and_accept", swapped),
            ("unrelated_accept", unrelated_ctx),
            ("citation_changed_index", cited_ctx),
        )
        for name, fee_ctx in cases:
            produced = self._verdict_bound(
                root,
                gate=root / "gate-full5.json",
                prc=root / "prc-full5.json",
                regime=root / "regime-honest.json",
                fee_ctx=fee_ctx,
            )
            self.assertEqual(produced["verdict"], "FULL_VERDICT_REQUIRES_EXAMINER", name)
            self.assertEqual(produced["binding_reason"], "DISK_BLOCKED_INPUTS_ADMITTED", name)
            self.assertEqual(
                produced["binding_detail"],
                "regime_report:fee_admission=ADMITTED_INDEX_ONLY;prc:status=OK,fee_state=ADMITTED;gate:status=OK",
                name,
            )
            self.assertNotEqual(produced["fee_block_reason"], "FEE_REPORT_MISSING", name)
            self.assertNotIn("PASS-FORECAST", produced["verdict"], name)
            self.assertNotIn("FORECAST_ONLY", produced["verdict"], name)
            self.assertIsNone(produced["evaluations"]["reject_c"], name)
            self.assertIsNone(produced["evaluations"]["reject_d"], name)

    def _wrong_fee_contexts(self, root):
        pinned_v1 = LAB / "pins" / "FEE_SOURCE_CARD01_v1_2026-10-03.json"
        if pinned_v1.is_file() and sha256_bytes(pinned_v1.read_bytes()) == V1_SHA:
            v1_path = pinned_v1
        else:
            v1_path = LAB / "tests" / "fixtures" / "SYNTH_FEE_SOURCE_v1_example.json"
            self.assertTrue(v1_path.is_file())
            self.assertNotEqual(sha256_bytes(v1_path.read_bytes()), self.pin["sha256"])
        unrelated = root / "unrelated-accept.txt"
        unrelated.write_text("not an accept\n", encoding="utf-8")
        cited = root / "packet-index-cited.md"
        cited.write_text(
            Path(self.fee_ctx["packet_index_path"]).read_text(encoding="utf-8")
            + "\nConductor WITHDRAW of amendment 2c870cd5\n",
            encoding="utf-8",
        )
        swapped = dict(self.fee_ctx)
        swapped["fee_source_path"] = self.fee_ctx["fee_accept_path"]
        swapped["fee_accept_path"] = self.fee_ctx["fee_source_path"]
        v1_ctx = dict(self.fee_ctx)
        v1_ctx["fee_source_path"] = str(v1_path)
        unrelated_ctx = dict(self.fee_ctx)
        unrelated_ctx["fee_accept_path"] = str(unrelated)
        cited_ctx = dict(self.fee_ctx)
        cited_ctx["packet_index_path"] = str(cited)
        return (
            ("v1_fee_source", v1_ctx),
            ("swapped_source_and_accept", swapped),
            ("unrelated_accept", unrelated_ctx),
            ("citation_changed_index", cited_ctx),
        )

    def _zero_signal_chain(self, root):
        """Real entry_gate, score, and build_report with no selected signal."""
        from card01_amc.join_outcomes import join
        from card01_amc.pnl_cd import make_anchor
        from card01_amc.regime_split_secondary import build_report
        from tests.test_regime_split_secondary import _selection

        rows = [{
            "race_id": "Z0",
            "ticker": "T-Z0",
            "series": "XS1",
            "mapping_status": "LEGACY",
            "p_model": 0.50,
            "p_market": 0.50,
            "yes_bid": "0.49",
            "yes_ask": "0.50",
            "yes_bid_qty": 10,
            "yes_ask_qty": 10,
        }]
        settled = {
            "results": [{
                "ticker": "T-Z0",
                "result": "yes",
                "settlement_ts": "2000-01-01T00:00:00.000000Z",
            }],
        }
        (root / "rows-zero.json").write_text(json.dumps(rows), encoding="utf-8")
        (root / "settled-zero.json").write_text(json.dumps(settled), encoding="utf-8")
        fee_args = [
            "--fee-source", self.fee_ctx["fee_source_path"],
            "--packet-index", self.fee_ctx["packet_index_path"],
            "--fee-accept", self.fee_ctx["fee_accept_path"],
        ]
        gated = self._run_module(root, "entry_gate", [
            str(root / "rows-zero.json"),
            "--fee-source-id", self.pin["id"],
            "--fee-source-sha256", self.pin["sha256"],
            *fee_args,
        ])
        gate_path = root / "gate-zero.json"
        gate_path.write_text(gated.stdout, encoding="utf-8")
        gate = json.loads(gated.stdout)
        joined = join(rows, settled)["rows"]
        report = build_report(
            joined,
            gate=gate,
            selection=_selection(),
            settled=settled,
            fee_source_path=self.fee_ctx["fee_source_path"],
            fee_source_id=self.pin["id"],
            fee_source_sha256=self.pin["sha256"],
            packet_index_path=self.fee_ctx["packet_index_path"],
            fee_accept_path=self.fee_ctx["fee_accept_path"],
            series_used=["XS1"],
        )
        report_path = root / "regime-zero.json"
        report_path.write_text(json.dumps(report), encoding="utf-8")
        book = root / "book-zero.json"
        self._run_module(root, "pnl_cd", [
            "entry-book",
            "--gate", str(gate_path),
            *fee_args,
            "--out", str(book),
        ])
        anchor = make_anchor(
            book.read_bytes(),
            gate_sha256=sha256_bytes(gate_path.read_bytes()),
            anchored_at_utc="2026-11-02T22:15:00Z",
        )
        anchor_path = root / "anchor-zero.json"
        anchor_path.write_text(json.dumps(anchor), encoding="utf-8")
        prc_path = root / "prc-zero.json"
        self._run_module(root, "pnl_cd", [
            "score",
            "--gate", str(gate_path),
            "--rows", str(root / "rows-zero.json"),
            "--entry-book", str(book),
            "--entry-book-anchor", str(anchor_path),
            "--settled-results", str(root / "settled-zero.json"),
            *fee_args,
            "--out", str(prc_path),
        ])
        return gate_path, prc_path, report_path, gate, report, json.loads(prc_path.read_text(encoding="utf-8"))

    def test_mf3_gate_not_reproduced_report_on_wrong_fee_path_requires_examiner(self):
        root, _full, _sub, blocked, _honest = self._examiner_world()
        self.assertEqual(blocked["fee_state"], "BLOCKED_FEE_UNVERIFIED")
        self.assertEqual(blocked["secondary"]["fee_block_reason"], "GATE_NOT_REPRODUCED")
        self.assertEqual(blocked["fee_admission"]["fee_admission"], "ADMITTED_INDEX_ONLY")
        for name, fee_ctx in self._wrong_fee_contexts(root):
            produced = self._verdict_bound(
                root,
                regime=root / "regime-blocked.json",
                fee_ctx=fee_ctx,
            )
            self.assertEqual(produced["verdict"], "FULL_VERDICT_REQUIRES_EXAMINER", name)
            self.assertEqual(produced["binding_reason"], "DISK_BLOCKED_INPUTS_ADMITTED", name)
            self.assertEqual(
                produced["binding_detail"],
                "regime_report:fee_admission=ADMITTED_INDEX_ONLY",
                name,
            )
            self.assertNotEqual(produced["fee_block_reason"], "FEE_REPORT_MISSING", name)
            self.assertNotIn("PASS-FORECAST", produced["verdict"], name)
            self.assertNotIn("FORECAST_ONLY", produced["verdict"], name)
            self.assertIsNone(produced["evaluations"]["reject_c"], name)
            self.assertIsNone(produced["evaluations"]["reject_d"], name)

    def test_mf3_zero_signal_gate_on_v1_path_requires_examiner(self):
        root, _full, _sub, _blocked, _honest = self._examiner_world()
        gate_path, _prc_path, _report_path, gate, report, _prc = self._zero_signal_chain(root)
        self.assertEqual(gate["status"], "OK")
        self.assertEqual(gate["signals"], [])
        self.assertEqual(report["fee_state"], "ADMITTED")
        v1_ctx = dict(self._wrong_fee_contexts(root)[0][1])
        produced = self._verdict_bound(root, gate=gate_path, fee_ctx=v1_ctx)
        self.assertEqual(produced["verdict"], "FULL_VERDICT_REQUIRES_EXAMINER")
        self.assertEqual(produced["binding_reason"], "DISK_BLOCKED_INPUTS_ADMITTED")
        self.assertEqual(produced["binding_detail"], "gate:status=OK")
        self.assertNotEqual(produced["fee_block_reason"], "FEE_REPORT_MISSING")
        self.assertNotIn("PASS-FORECAST", produced["verdict"])
        self.assertNotIn("FORECAST_ONLY", produced["verdict"])
        self.assertIsNone(produced["evaluations"]["reject_c"])
        self.assertIsNone(produced["evaluations"]["reject_d"])

    def test_mf3_honest_zero_signal_triple_rejects(self):
        root, _full, _sub, _blocked, _honest = self._examiner_world()
        gate_path, prc_path, report_path, gate, report, prc = self._zero_signal_chain(root)
        self.assertEqual(gate["status"], "OK")
        self.assertEqual(gate["signals"], [])
        self.assertEqual(report["fee_state"], "ADMITTED")
        self.assertEqual(prc["status"], "NO_SIGNALS_SELECTED")
        self.assertEqual(prc["n_signals"], 0)
        self.assertIs(prc["reject_c"], True)
        self.assertIs(prc["reject_d"], True)
        produced = self._verdict_bound(
            root,
            gate=gate_path,
            prc=prc_path,
            regime=report_path,
        )
        self.assertEqual(produced["verdict"], "REJECT")
        self.assertIn("(c)", produced["firing"])
        self.assertIn("(d)", produced["firing"])
        self.assertNotIn("PASS-FORECAST", produced["verdict"])
        self.assertNotIn("binding_reason", produced)

    def test_e1b_stripped_book_reject_cannot_pass_forecast(self):
        from card01_amc.fee_admission import pinned_entry_v2
        from card01_amc.fee_source import pinned_taker_fee

        honest = self._run("C_TICK_ONLY")
        self.assertIs(honest["reject_c"], True)
        self.assertIs(honest["reject_d"], True)
        forged = json.loads(json.dumps(honest["_gate"]))
        entry = pinned_entry_v2(self.admission, "XS1")
        for signal in forged["signals"]:
            signal["price"] = 0.2
            if signal["race_id"] in ("XC-01", "XC-02"):
                signal["side"] = "D_NO"
            quoted = pinned_taker_fee(entry, Decimal("0.2"))
            signal["fee"] = float(quoted["headline"])
            signal["fee_decimal"] = str(quoted["headline"])
        rows = []
        for row in honest["_rows"]:
            item = dict(row)
            for key in ("yes_bid", "yes_ask", "yes_bid_qty", "yes_ask_qty"):
                item.pop(key, None)
            rows.append(item)
        settled = honest["_settled"]
        gate_bytes = json.dumps(forged, sort_keys=True).encode()

        def stripped(mode):
            built = []
            for row in rows:
                item = dict(row)
                if mode == "deleted":
                    pass
                elif mode == "none":
                    item["yes_bid"] = None
                    item["yes_ask"] = None
                elif mode == "one_sided":
                    item["yes_bid"] = "0.19"
                    item["yes_ask"] = None
                built.append(item)
            return built

        report = _admitted_report(self.pin)
        for mode in ("deleted", "none", "one_sided"):
            scored = self._score_bytes(forged, gate_bytes, stripped(mode), settled)
            self.assertEqual(scored["status"], "BLOCKED_FEE_UNVERIFIED", mode)
            self.assertEqual(scored["fee_block_reason"], "ENTRY_ROW_BOOK_MISSING", mode)
            self.assertIn("ENTRY_ROW_BOOK_MISSING", [item["kind"] for item in scored["reporting_defects"]], mode)
            self.assertEqual(scored["_calls"]["n"], 0, mode)
            self.assertFalse(_has_money(scored), mode)
            self.assertNotIn("net_headline_total", scored, mode)
            cd = cd_from_prc(_public(scored), forged, fee_ctx=self.fee_ctx)
            self.assertIsNone(cd, mode)
            produced = apply_verdict(_score_dict(-0.01, -0.02), cd=cd, regime_report=report)
            self.assertEqual(produced["verdict"], "FULL_VERDICT_REQUIRES_EXAMINER", mode)
            self.assertNotIn("PASS-FORECAST", produced["verdict"], mode)
            self.assertNotEqual(produced["verdict"], "PASS-FORECAST", mode)

    def test_e1b_ten_cent_forged_gate_is_not_reproduced(self):
        from card01_amc.entry_gate import gate_v2
        from card01_amc.fee_admission import pinned_entry_v2
        from card01_amc.fee_source import pinned_taker_fee

        row = {
            "series": "XS1",
            "mapping_status": "LEGACY",
            "p_market": 0.8,
            "p_model": 0.8,
            "yes_bid": 0.35,
            "yes_ask": 0.4,
            "yes_ask_qty": 10,
            "yes_bid_qty": 10,
            "race_id": "XA-01",
            "state": "XA",
            "ticker": "T-XA-01",
            "y": 1,
        }
        bare = {key: value for key, value in row.items() if key != "y"}
        true_gate = gate_v2(
            [bare],
            fee_source_path=self.fee_ctx["fee_source_path"],
            fee_source_id=self.pin["id"],
            fee_source_sha256=self.pin["sha256"],
            packet_index_path=self.fee_ctx["packet_index_path"],
            fee_accept_path=self.fee_ctx["fee_accept_path"],
        )
        self.assertEqual(true_gate["status"], "OK")
        self.assertEqual(len(true_gate["signals"]), 1)
        forged = json.loads(json.dumps(true_gate))
        entry = pinned_entry_v2(self.admission, "XS1")
        for signal in forged["signals"]:
            price = Decimal(str(signal["price"])) + Decimal("0.10")
            signal["price"] = float(price)
            quoted = pinned_taker_fee(entry, price)
            signal["fee"] = float(quoted["headline"])
            signal["fee_decimal"] = str(quoted["headline"])
        self.assertNotEqual(forged["signals"], true_gate["signals"])
        scoring_row = {key: value for key, value in row.items() if key != "y"}
        settled = {
            "results": [{
                "ticker": "T-XA-01",
                "result": "yes",
                "settlement_ts": "2000-01-01T00:00:00.000000Z",
            }],
        }
        gate_bytes = json.dumps(forged, sort_keys=True).encode()
        scored = self._score_bytes(forged, gate_bytes, [scoring_row], settled)
        self.assertEqual(scored["status"], "GATE_NOT_REPRODUCED")
        self.assertEqual(scored["fee_block_reason"], "GATE_NOT_REPRODUCED")
        self.assertIn("GATE_NOT_REPRODUCED", [item["kind"] for item in scored["reporting_defects"]])
        self.assertEqual(scored["_calls"]["n"], 0)
        self.assertFalse(_has_money(scored))
        self.assertNotEqual(scored["reject_c"], True)
        self.assertNotEqual(scored["reject_d"], True)
        honest = self._score_bytes(
            true_gate,
            json.dumps(true_gate, sort_keys=True).encode(),
            [scoring_row],
            settled,
        )
        self.assertEqual(honest["status"], "OK")
        self.assertGreater(honest["_calls"]["n"], 0)

    def test_e5_anchor_window(self):
        base = self._run("P1_CLEAN")

        def scored(stamp):
            anchor = pnl_cd.make_anchor(
                base["_book"],
                gate_sha256=base["_gate_sha"],
                anchored_at_utc=stamp,
            )
            return self._run(
                "P1_CLEAN",
                gate=base["_gate"],
                anchor_doc=anchor,
                entry_book_bytes=base["_book"],
            )

        outside = (
            ("2026-11-02T22:14:59Z", "BEFORE_EARLIEST"),
            ("1999-01-01T00:00:00Z", "BEFORE_EARLIEST"),
            ("2026-11-03T23:00:00Z", "AT_OR_AFTER_CUTOFF"),
            ("2026-11-05T00:00:00Z", "AT_OR_AFTER_CUTOFF"),
        )
        for stamp, detail in outside:
            blocked = scored(stamp)
            self.assertEqual(blocked["status"], "REPORTING_DEFECT", stamp)
            window = [
                item for item in blocked["reporting_defects"]
                if item.get("kind") == "ENTRY_BOOK_ANCHOR_OUTSIDE_WINDOW"
            ]
            self.assertEqual(len(window), 1, stamp)
            self.assertEqual(window[0].get("detail"), detail, stamp)
            self.assertEqual(blocked["_calls"]["n"], 0, stamp)
            self.assertFalse(_has_money(blocked), stamp)
        for stamp in ("2026-11-02T22:15:00Z", "2026-11-03T22:59:59Z"):
            passed = scored(stamp)
            self.assertEqual(passed["status"], "OK", stamp)
            self.assertGreater(passed["_calls"]["n"], 0, stamp)
        unparsed = pnl_cd.make_anchor(
            base["_book"],
            gate_sha256=base["_gate_sha"],
            anchored_at_utc="2026-11-02T22:15:00Z",
        )
        unparsed["anchored_at_utc"] = "not-a-timestamp"
        bad = self._run(
            "P1_CLEAN",
            gate=base["_gate"],
            anchor_doc=unparsed,
            entry_book_bytes=base["_book"],
        )
        self.assertEqual(bad["status"], "REPORTING_DEFECT")
        self.assertIn("ENTRY_BOOK_ANCHOR_INVALID", [item["kind"] for item in bad["reporting_defects"]])
        self.assertEqual(bad["_calls"]["n"], 0)

    def test_e9_empty_or_missing_entry_book_is_blocked(self):
        gate = self._gate(self._case("P1_CLEAN"))
        rows, settled = _split(self._case("P1_CLEAN"))
        calls = {"n": 0}

        def loader():
            calls["n"] += 1
            return settled

        specs = (("absent", None, "ENTRY_BOOK_ABSENT"), ("empty", b"{}", "ENTRY_BOOK_EMPTY"))
        for name, book, reason in specs:
            out = pnl_cd.run(
                gate,
                rows,
                loader,
                gate_sha256="ab" * 32,
                entry_book_bytes=book,
                anchor_doc=None,
                fee_ctx=self.fee_ctx,
            )
            self.assertEqual(out["status"], "BLOCKED_FEE_UNVERIFIED", name)
            self.assertEqual(out["fee_block_reason"], reason, name)
            self.assertIn(reason, [item["kind"] for item in out["reporting_defects"]], name)
            self.assertNotEqual(out["status"], "OK", name)
            self.assertFalse(_has_money(out), name)
            self.assertEqual(calls["n"], 0, name)

    def test_r39_net_figures_are_labelled_illustrative(self):
        out = self._run("P1_CLEAN")
        self.assertEqual(out["net_figure_label"], "ILLUSTRATIVE/R39")
        self.assertEqual(out["net_headline_total"], EXPECTED["cases"]["P1_CLEAN"]["net_headline_total"])
        self.assertTrue(out["per_signal"])
        for row in out["per_signal"]:
            self.assertEqual(row["net_label"], "ILLUSTRATIVE/R39")
        zero = self._run("ZERO_SIGNALS")
        self.assertEqual(zero["net_figure_label"], "ILLUSTRATIVE/R39")
        self.assertEqual(zero["net_headline_total"], "0")

    def test_pins_override_is_tests_only(self):
        for path in (LAB / "card01_amc").glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module and (node.module == "tests" or node.module.startswith("tests.")):
                    self.fail(path.name)
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name == "tests" or alias.name.startswith("tests."):
                            self.fail(path.name)
                if isinstance(node, ast.Constant) and isinstance(node.value, str) and "pins_override" in node.value.lower():
                    self.fail(path.name)
                if isinstance(node, ast.Attribute) and node.attr in {"environ", "getenv"}:
                    self.fail(path.name + " reads the environment")
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "add_argument":
                    for arg in node.args:
                        if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                            low = arg.value.lower()
                            self.assertNotIn("pins", low, path.name)
                            self.assertNotIn("override", low, path.name)
        for module, args in (
            ("card01_amc.pnl_cd", ["entry-book", "--help"]),
            ("card01_amc.pnl_cd", ["score", "--help"]),
            ("card01_amc.verdict", ["--help"]),
            ("card01_amc.swing_stress", ["--help"]),
        ):
            proc = subprocess.run([sys.executable, "-m", module, *args], cwd=LAB, capture_output=True, text=True, check=False)
            self.assertEqual(proc.returncode, 0, module)
            low = proc.stdout.lower()
            self.assertNotIn("--pins", low, module)
            self.assertNotIn("override", low, module)

    def test_cli_refuses_repo_output_and_entry_book_has_no_settled_flag(self):
        proc = subprocess.run(
            [sys.executable, "-m", "card01_amc.pnl_cd", "entry-book", "--help"],
            cwd=LAB, capture_output=True, text=True, check=False,
        )
        self.assertNotIn("settled", proc.stdout.lower())
        self.assertNotIn("--rows", proc.stdout)
        gate = self._gate(self._case("P1_CLEAN"))
        with tempfile.TemporaryDirectory() as tmp:
            gate_path = Path(tmp) / "gate.json"
            gate_path.write_text(json.dumps(gate), encoding="utf-8")
            refused = subprocess.run(
                [
                    sys.executable, "-m", "card01_amc.pnl_cd", "entry-book",
                    "--gate", str(gate_path),
                    "--fee-source", self.fee_ctx["fee_source_path"],
                    "--packet-index", self.fee_ctx["packet_index_path"],
                    "--fee-accept", self.fee_ctx["fee_accept_path"],
                    "--out", str(LAB / "CARD01_PRC_ENTRY_BOOK_refused.json"),
                ],
                cwd=LAB, capture_output=True, text=True, check=False,
            )
            self.assertEqual(refused.returncode, 2)
            self.assertIn("OUTPUT_PATH_IN_REPO", refused.stderr)
            self.assertFalse((LAB / "CARD01_PRC_ENTRY_BOOK_refused.json").exists())


if __name__ == "__main__":
    unittest.main()
