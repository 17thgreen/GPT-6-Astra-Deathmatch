import gzip
import json
import tempfile
import unittest
from pathlib import Path

import support
from ext2k1.canonical import canonical_sha256
from ext2k1.sweeps import build
from ext2k1.tape import load_jsonl_gz


class T01Sweeps(unittest.TestCase):
    def test_hand_vectors_group_by_key(self):
        markets = {"T-X": {"event": "XH-1"}}
        rows = [
            {"ticker": "T-X", "at": 10.0, "taker_side": "yes", "size": 999.99},
            {"ticker": "T-X", "at": 11.0, "taker_side": "no", "size": 600.0},
            {"ticker": "T-X", "at": 11.0, "taker_side": "no", "size": 400.0},
            {"ticker": "T-X", "at": 12.5, "taker_side": "yes", "size": 700.0},
            {"ticker": "T-X", "at": 12.5, "taker_side": "no", "size": 1000.0, "kind": "trade"},
            {"ticker": "T-X", "at": 12.5, "taker_side": "no", "size": 500.0},
            {"kind": "quote", "ticker": "T-X", "at": 12.5, "size": 99999.0},
        ]
        document = build(rows, markets)
        self.assertEqual(len(document["sweeps"]), 2)
        by_side = {sweep["taker_side"]: sweep for sweep in document["sweeps"]}
        self.assertNotIn("yes", {sweep["taker_side"] for sweep in document["sweeps"] if sweep["t_s"] == 10.0})
        self.assertEqual(by_side["no"]["S"] if False else document["sweeps"][0]["S"], 1000.0)
        multi = [sweep for sweep in document["sweeps"] if sweep["t_s"] == 11.0][0]
        headline = [sweep for sweep in document["sweeps"] if sweep["t_s"] == 12.5][0]
        self.assertEqual(multi["n_prints"], 2)
        self.assertEqual(multi["S"], 1000.0)
        self.assertEqual(multi["taker_side"], "no")
        self.assertEqual(headline["taker_side"], "no")
        self.assertEqual(headline["S"], 1500.0)
        self.assertEqual(headline["n_prints"], 2)
        self.assertNotEqual(multi["sweep_id"], headline["sweep_id"])

    def test_tape_document_and_named_edges(self):
        tape = support.FIXTURES["tape"]
        expected = support.EXPECTED
        document = build(tape["rows"], tape["markets"])
        self.assertEqual(document, expected["sweeps_doc"])
        self.assertEqual(canonical_sha256(document), expected["sweeps_sha256"])
        edges = expected["edge_cases"]

        def hits(tag):
            edge = edges[tag]
            return [
                sweep
                for sweep in document["sweeps"]
                if sweep["ticker"] == edge["ticker"]
                and sweep["t_s"] == edge["t_s"]
                and sweep["taker_side"] == edge["taker_side"]
            ]

        self.assertEqual(hits("E6a_999.99_out"), [])
        multi = hits("E6b_exactly_1000_in_multi_print")
        self.assertEqual(len(multi), 1)
        self.assertEqual(multi[0]["S"], 1000.0)
        self.assertEqual(multi[0]["n_prints"], 2)
        self.assertEqual(hits("E8a_same_at_yes_sub"), [])
        opposite = hits("E8b_same_at_no_headline")
        self.assertEqual(len(opposite), 1)
        self.assertEqual(opposite[0]["S"], 1500.0)
        self.assertNotEqual(edges["E8a_same_at_yes_sub"]["taker_side"], opposite[0]["taker_side"])
        self.assertEqual(edges["E8a_same_at_yes_sub"]["t_s"], opposite[0]["t_s"])

    def test_tape_round_trip_through_gzip(self):
        tape = support.FIXTURES["tape"]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "events.jsonl.gz"
            with path.open("wb") as raw:
                with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as handle:
                    for row in tape["rows"]:
                        handle.write((json.dumps(row, sort_keys=True) + "\n").encode("utf-8"))
            loaded = load_jsonl_gz(path)
        self.assertEqual(loaded, tape["rows"])
        document = build(loaded, tape["markets"])
        self.assertEqual(canonical_sha256(document), support.EXPECTED["sweeps_sha256"])


if __name__ == "__main__":
    unittest.main()
