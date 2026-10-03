"""T01–T04 and the dev-tape half of T16. Label-free part (a)."""

import ast
import os
import random
import unittest
from pathlib import Path

from tests.support import dev_state, lab_root, repo_root


class TestT01LabelPermutation(unittest.TestCase):
    def test_synthetic_label_swap_keeps_canonical_bytes(self):
        from dev_pipeline.terciles import bucket_document, flow_terciles, portion_labels
        from shared.canonical import canon_bytes
        from shared.exceptions import LabelInputRefused

        rows = []
        for ticker, side, size in (
            ("KXNFLGAME-25SEP07AAAA-AA", "yes", 8.0),
            ("KXNFLGAME-25SEP07AAAA-AA", "no", 2.0),
            ("KXNFLGAME-25SEP07AAAA-BB", "yes", 3.0),
            ("KXNFLGAME-25SEP07AAAA-BB", "yes", 1.0),
            ("KXNFLGAME-25SEP07BBBB-CC", "no", 5.0),
            ("KXNFLGAME-25SEP07BBBB-CC", "no", 4.0),
            ("KXNFLGAME-25SEP07BBBB-DD", "yes", 9.0),
            ("KXNFLGAME-25SEP07BBBB-DD", "no", 1.0),
        ):
            for k in range(5):
                rows.append((ticker, 1_000_000.0 + k, side, size))
        built = flow_terciles(rows)
        portions = [
            {"ticker": "KXNFLGAME-25SEP07AAAA-AA", "t_open": 1_000_002.0,
             "event": "KXNFLGAME-25SEP07AAAA", "row_index": 0},
            {"ticker": "KXNFLGAME-25SEP07BBBB-CC", "t_open": 1_000_003.0,
             "event": "KXNFLGAME-25SEP07BBBB", "row_index": 1},
        ]
        from dev_pipeline.terciles import index_trades
        labels = portion_labels(portions, built, index_trades(rows))
        cuts = {"c1": built["c1"], "c2": built["c2"], "e1": built["e1"], "e2": built["e2"]}
        before = (
            canon_bytes(cuts),
            canon_bytes(bucket_document(built, tape_sha="synthetic")),
            canon_bytes(labels),
        )
        swapped = {"KXNFLGAME-25SEP07AAAA": "yes", "KXNFLGAME-25SEP07BBBB": "no"}
        swapped = {key: ("no" if value == "yes" else "yes") for key, value in swapped.items()}
        with self.assertRaises(LabelInputRefused):
            flow_terciles(rows, result=swapped)
        rebuilt = flow_terciles(rows)
        labels_b = portion_labels(portions, rebuilt, index_trades(rows))
        cuts_b = {"c1": rebuilt["c1"], "c2": rebuilt["c2"], "e1": rebuilt["e1"], "e2": rebuilt["e2"]}
        after = (
            canon_bytes(cuts_b),
            canon_bytes(bucket_document(rebuilt, tape_sha="synthetic")),
            canon_bytes(labels_b),
        )
        self.assertEqual(before, after)

    def test_pinned_permutations_leave_shas_constant(self):
        from dev_pipeline import load as load_mod
        from dev_pipeline.load import load_dev
        from dev_pipeline.lots import reconstruct
        from dev_pipeline.terciles import bucket_document, flow_terciles, index_trades, portion_labels
        from shared.canonical import canon_sha256
        from shared.exceptions import LabelInputRefused
        from tests import support

        support._STATE.clear()
        load_mod._CACHE.clear()
        dev = load_dev()
        rng = random.Random(20261003)
        games = list(dev["games"])
        attached = {}
        for _ in range(1000):
            permuted = list(games)
            rng.shuffle(permuted)
            attached = {game: permuted[i] for i, game in enumerate(games)}
            with self.assertRaises(LabelInputRefused):
                flow_terciles(dev["flow"], result=attached)
        rotated = {game: games[(i + 1) % len(games)] for i, game in enumerate(games)}
        with self.assertRaises(LabelInputRefused):
            flow_terciles(dev["flow"], result=rotated)
        quotes = []
        for ticker, rows in dev["quotes"].items():
            for at, asof, bid, ask in rows:
                quotes.append((ticker, at, asof, bid, ask))
        rng.shuffle(quotes)
        with self.assertRaises(LabelInputRefused):
            flow_terciles(dev["flow"], quote=quotes)
        fills = [dict(row) for row in dev["fills"]]
        mids = [row.get("outcome_mid_at_fill") for row in fills]
        rng.shuffle(mids)
        for row, mid in zip(fills, mids):
            row["outcome_mid_at_fill"] = mid
        with self.assertRaises(LabelInputRefused):
            flow_terciles(dev["flow"], fill=mids)
        with self.assertRaises(LabelInputRefused):
            flow_terciles(dev["flow"], score={"home": 1})
        # Labels, quotes, and mids are not inputs. The rebuild uses the flow projection only.
        flow = []
        for ticker, at, side, size in dev["flow"]:
            _ = (attached, quotes, mids)
            flow.append((ticker, at, side, size))
        self.assertEqual(flow, list(dev["flow"]))
        built = flow_terciles(flow)
        document = bucket_document(built)
        lots = reconstruct(fills, dev["markets"])
        labels = portion_labels(lots["portions"], built, index_trades(flow))
        shas = {
            "tercile_cuts": canon_sha256({
                "c1": built["c1"], "c2": built["c2"], "e1": built["e1"], "e2": built["e2"],
            }),
            "bucket_terciles": canon_sha256(document),
            "portion_terciles": canon_sha256(labels),
        }
        constancy = canon_sha256({
            "bucket_terciles_sha256": shas["bucket_terciles"],
            "portion_terciles_sha256": shas["portion_terciles"],
            "tercile_cuts_sha256": shas["tercile_cuts"],
        })
        print("tercile_cuts", shas["tercile_cuts"])
        print("bucket_terciles", shas["bucket_terciles"])
        print("portion_terciles", shas["portion_terciles"])
        print("constancy", constancy)
        self.assertEqual(
            constancy,
            "523f840babd3e57d8a305ecc458f979d9288e69082210edaf8648e3132101968",
        )
        self.assertAlmostEqual(built["c1"], 0.9271702456462422, delta=1e-12)
        self.assertAlmostEqual(built["c2"], 0.989881659505818, delta=1e-12)


class TestT02TrailingWindow(unittest.TestCase):
    def test_deleting_future_trades_leaves_trailing_regime(self):
        from dev_pipeline.terciles import index_trades, trailing_share

        state = dev_state()
        portions = state["lots"]["portions"]
        index = index_trades(state["dev"]["flow"])
        rng = random.Random(20261003)
        chosen = rng.sample(range(len(portions)), 200)
        for pos in chosen:
            portion = portions[pos]
            trades = index[portion["ticker"]]
            full = trailing_share(trades, portion["t_open"])
            trimmed = [row for row in trades if row[0] < portion["t_open"]]
            self.assertEqual(full, trailing_share(trimmed, portion["t_open"]))


class TestT03TercileFixture(unittest.TestCase):
    def test_cuts_counts_and_bucket_bytes(self):
        state = dev_state()
        built = state["built"]
        self.assertAlmostEqual(built["c1"], 0.9271702456462422, delta=1e-12)
        self.assertAlmostEqual(built["c2"], 0.989881659505818, delta=1e-12)
        self.assertAlmostEqual(built["e1"], 0.9126590461375717, delta=1e-12)
        self.assertAlmostEqual(built["e2"], 0.9359888338062846, delta=1e-12)
        counts = {"T1_LOW": 0, "T2_MID": 0, "T3_HIGH": 0, "UNCLASSIFIED": 0}
        for row in built["rows"]:
            counts[row["tercile"]] += 1
        self.assertEqual(counts, {
            "T1_LOW": 3093, "T2_MID": 3092, "T3_HIGH": 3092, "UNCLASSIFIED": 812,
        })
        events = {"T1_LOW": 0, "T2_MID": 0, "T3_HIGH": 0, "UNCLASSIFIED": 0}
        for label in built["event_tercile"].values():
            events[label] += 1
        self.assertEqual(
            [events["T1_LOW"], events["T2_MID"], events["T3_HIGH"]],
            [11, 10, 10],
        )
        pinned = (
            lab_root()
            / "pins/k2/EXT_K2_authentic_pins_2026-10-03/lab/governance/astra/packets"
            / "EXT_K2_OPTIMISM_TAX/TERCILE_BUCKETS.json"
        )
        self.assertEqual(state["document_bytes"], pinned.read_bytes())
        self.assertEqual(
            state["shas"]["bucket_terciles"],
            "9acb52888a411be801bb701d12f3982e1e2f1c884accc162ca6f1f1d8fef6a14",
        )


class TestT04Structural(unittest.TestCase):
    def test_r36_gate_and_section_3_counts(self):
        from dev_pipeline.orchestrator import structural_gate

        state = dev_state()
        gate = structural_gate(
            state["dev"], state["built"], state["lots"], state["shas"]["bucket_terciles"],
        )
        self.assertTrue(gate["ok"], gate["failures"])
        self.assertAlmostEqual(gate["maker_no_share"], 0.989706, delta=1e-6)
        self.assertAlmostEqual(gate["uch_integral"], 603262.7291176913, delta=0.01)
        self.assertEqual(gate["n_portions"], 6161)
        self.assertAlmostEqual(gate["taker_yes_contract_share"], 0.9168821893496498, delta=1e-12)
        self.assertEqual(gate["trade_rows"], 681732)
        self.assertEqual(gate["quote_rows"], 364988)
        self.assertEqual(gate["tickers"], 62)
        self.assertEqual(gate["events"], 31)
        import json
        import sys
        from collections import defaultdict
        from decimal import Decimal

        from shared.fees import part_a_order_headline

        k1_root = repo_root() / "kalshi_ext_k1_q6000_legging_audit_lab_20261003"
        structural = json.loads((k1_root / "results" / "STRUCTURAL.json").read_text(encoding="utf-8"))
        self.assertEqual(structural["opening_portions"], gate["n_portions"])
        self.assertAlmostEqual(structural["maker_no_share_raw"], gate["maker_no_share"], delta=1e-9)
        self.assertAlmostEqual(structural["ledger_uch_raw"], gate["uch_integral"], delta=1e-6)
        self.assertEqual(structural["fees"]["headline_maker_order_fee_total_raw"], "1286.22")
        groups = defaultdict(list)
        for fill in state["dev"]["fills"]:
            if fill["kind"] != "maker":
                continue
            groups[fill["order_id"]].append((fill["size"], fill["price"]))
        total = sum(
            (part_a_order_headline(pairs, Decimal(1))[0] for pairs in groups.values()),
            Decimal(0),
        )
        self.assertEqual(total, Decimal(structural["fees"]["headline_maker_order_fee_total_raw"]))
        sys.path.insert(0, str(k1_root))
        try:
            import importlib
            k1_fees = importlib.import_module("fees")
            order_fee, _per, _six = k1_fees.headline_order_fee([(Decimal("247.5"), Decimal("0.37"))])
            self.assertEqual(order_fee, Decimal("1.01"))
        finally:
            sys.path.remove(str(k1_root))
            for name in ("fees", "constants", "errors"):
                sys.modules.pop(name, None)

    def test_undefined_contrast_is_inconclusive(self):
        from dev_pipeline.orchestrator import decide_verdict

        def cell(name, opening):
            return {
                "tercile": name,
                "opening_contracts": opening,
                "distinct_games": 10,
                "horizons": {"1800": {"censored_contracts": 0.0}},
            }

        cells = [
            cell("T1_LOW", 100.0), cell("T2_MID", 100.0),
            cell("T3_HIGH", 100.0), cell("UNCLASSIFIED", 1.0),
        ]
        missing = {"dropped_share": 0.0, "delta_gross": None, "ci95_gross": None}
        verdict, reasons = decide_verdict({"ok": True}, cells, missing)
        self.assertEqual(verdict, "INCONCLUSIVE")
        self.assertIn("undefined_contrast", reasons)
        present = {"dropped_share": 0.0, "delta_gross": -0.000301641, "ci95_gross": [-0.001030989, 0.000450135]}
        self.assertEqual(decide_verdict({"ok": True}, cells, present)[0], "DESCRIPTIVE")

    def test_dev_pipeline_has_no_becker_import(self):
        root = lab_root() / "dev_pipeline"
        for path in root.glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                module = ""
                if isinstance(node, ast.Import):
                    module = " ".join(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    module = node.module
                self.assertNotIn("becker_pipeline", module)


class TestT16Untouched(unittest.TestCase):
    def test_000_shas_and_empty_diff_and_lee_ready(self):
        from dev_pipeline.load import SHA
        from shared.canonical import sha256_file
        from shared.exceptions import LeeReadyRefused
        from shared.refusals import assert_no_lee_ready

        vendored = (
            lab_root()
            / "pins/k1/EXT_K1_authentic_pins_2026-10-03/lab/astra-science/nfl_factorial_lab_20260921"
        )
        repo_lab = repo_root() / "nfl_factorial_lab_20260921"
        pairs = {
            "replay_v2.py": SHA["replay"],
            "queue_policies.py": SHA["queue"],
            "run_experiment.py": SHA["run"],
            "results/q3300_d0.25_000.json": SHA["summary"],
            "results/q3300_d0.25_000_fills.jsonl.gz": SHA["fills"],
            "results/q3300_d0.25_000_orders.jsonl.gz": SHA["orders"],
        }
        for rel, digest in pairs.items():
            self.assertEqual(sha256_file(vendored / rel), digest)
        for rel in ("replay_v2.py", "queue_policies.py", "run_experiment.py"):
            self.assertEqual(sha256_file(repo_lab / rel), SHA[
                {"replay_v2.py": "replay", "queue_policies.py": "queue", "run_experiment.py": "run"}[rel]
            ])
        pipe = os.popen("git diff --stat -- nfl_factorial_lab_20260921")
        diff = pipe.read()
        pipe.close()
        self.assertEqual(diff.strip(), "")
        with self.assertRaises(LeeReadyRefused):
            assert_no_lee_ready({"lee_ready": True})
        with self.assertRaises(LeeReadyRefused):
            assert_no_lee_ready("tick-rule")


if __name__ == "__main__":
    unittest.main()
