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
        from dev_pipeline.terciles import flow_terciles
        from shared.exceptions import LabelInputRefused

        state = dev_state()
        dev = state["dev"]
        shas = state["shas"]
        print("tercile_cuts", shas["tercile_cuts"])
        print("bucket_terciles", shas["bucket_terciles"])
        print("portion_terciles", shas["portion_terciles"])
        print("constancy", shas["constancy"])
        rng = random.Random(20261003)
        games = list(dev["games"])
        for _ in range(1000):
            permuted = list(games)
            rng.shuffle(permuted)
            attached = {game: permuted[i] for i, game in enumerate(games)}
            with self.assertRaises(LabelInputRefused):
                flow_terciles(dev["flow"], result=attached)
        rotated = games[1:] + games[:1]
        with self.assertRaises(LabelInputRefused):
            flow_terciles(dev["flow"], result=rotated)
        quotes = []
        for ticker, rows in dev["quotes"].items():
            for at, asof, bid, ask in rows:
                quotes.append((ticker, at, asof, bid, ask))
        rng.shuffle(quotes)
        with self.assertRaises(LabelInputRefused):
            flow_terciles(dev["flow"], quote=quotes)
        mids = [row.get("outcome_mid_at_fill") for row in dev["fills"]]
        rng.shuffle(mids)
        with self.assertRaises(LabelInputRefused):
            flow_terciles(dev["flow"], fill=mids)
        with self.assertRaises(LabelInputRefused):
            flow_terciles(dev["flow"], score={"home": 1})
        again = dev_state()
        self.assertEqual(again["shas"], shas)
        self.assertEqual(again["cuts_bytes"], state["cuts_bytes"])
        self.assertEqual(again["document_bytes"], state["document_bytes"])
        self.assertEqual(again["portion_bytes"], state["portion_bytes"])
        built = state["built"]
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
        k1_labs = list(repo_root().glob("kalshi_ext_k1*"))
        self.assertEqual(k1_labs, [])

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
