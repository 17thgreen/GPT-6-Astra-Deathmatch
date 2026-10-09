import unittest

import support
from ext2k1.quotes import QuoteBook, classify_sweeps, rv_value, tmo_value
from ext2k1.sweeps import build


def _with_trade(case):
    rows = [dict(row) for row in case["rows"]]
    if "extra_trade_row_at" in case:
        rows.append(
            {
                "at": case["extra_trade_row_at"],
                "ticker": "T-X",
                "taker_side": "yes",
                "size": 1.0,
                "yes_price": 0.4,
                "trade_id": "x",
            }
        )
    return rows


def _one_sweep(case):
    return {
        "sweep_id": "SW-000001",
        "ticker": "T-X",
        "event": "XH-1",
        "t_s": case["t_s"],
        "taker_side": "yes",
        "d": 1,
        "S": 1000.0,
        "n_prints": 1,
        "flags": ["HEADLINE"],
    }


class T02Sign(unittest.TestCase):
    def test_rv_and_tmo_signs(self):
        for vector in support.FIXTURES["t02_vectors"]:
            if "expect_RV" in vector:
                got = rv_value(vector["d"], vector["m_900"], vector["m_E"])
                self.assertAlmostEqual(got, vector["expect_RV"], delta=1e-12)
            else:
                ask = vector.get("ask_E")
                bid = vector.get("bid_E")
                got = tmo_value(vector["d"], vector["m_900"], bid, ask)
                self.assertAlmostEqual(got, vector["expect_TMO"], delta=1e-12)


class T04Mids(unittest.TestCase):
    def test_hand_vectors(self):
        by_id = {case["id"]: case for case in support.FIXTURES["t04_vectors"]}
        entry = by_id["T04_ENTRY"]
        record = classify_sweeps([_one_sweep(entry)], _with_trade(entry))[0]
        self.assertEqual(record["entry_asof"], entry["expect_entry_asof"])
        self.assertEqual(record["entry_asof"], 1860)

        valid = by_id["T04_EXIT60_VALID"]
        record = classify_sweeps([_one_sweep(valid)], _with_trade(valid))[0]
        self.assertEqual(record["entry_asof"], valid["expect_entry_asof"])
        self.assertEqual(record["m"]["60"], valid["expect_m_60"])

        null_exit = by_id["T04_EXIT60_NULL_ORDER"]
        record = classify_sweeps([_one_sweep(null_exit)], _with_trade(null_exit))[0]
        self.assertIsNone(record["m"]["60"])
        self.assertEqual(record["m"]["60"], null_exit["expect_m_60"])
        book = QuoteBook(_with_trade(null_exit))
        _mid, row = book.mid_at("T-X", null_exit["t_s"] + 180)
        self.assertEqual(row[1], null_exit["latest_row_asof_at_exit"])

        missing = by_id["T04_NO_ENTRY_MID"]
        record = classify_sweeps([_one_sweep(missing)], _with_trade(missing))[0]
        self.assertEqual(record["status"], "NO_ENTRY_MID")
        self.assertIsNone(record["m_E"])
        self.assertTrue(all(value is None for value in record["m"].values()))
        self.assertIsNone(missing["expect_entry"])

        boundary = by_id["T04_BOUNDARY_t_s_1800.0"]
        record = classify_sweeps([_one_sweep(boundary)], _with_trade(boundary))[0]
        self.assertEqual(record["entry_asof"], boundary["expect_entry_asof"])
        self.assertNotEqual(record["entry_asof"], boundary["t_s"])

        pre = by_id["T04_PRE_MID_STRICT"]
        book = QuoteBook(pre["rows"])
        self.assertAlmostEqual(book.pre_mid("T-X", pre["t_s"]), pre["expect_m_pre"], delta=1e-12)

    def test_tape_edges_match_expected_per_sweep(self):
        tape = support.FIXTURES["tape"]
        expected = support.EXPECTED
        document = build(tape["rows"], tape["markets"])
        records = {row["sweep_id"]: row for row in classify_sweeps(document["sweeps"], tape["rows"])}
        expected_records = {row["sweep_id"]: row for row in expected["per_sweep"]}
        self.assertEqual(records, expected_records)
        wanted = [
            "E1_NO_PRE_MID",
            "E2_NO_ENTRY_MID_missing_candle",
            "E3_NO_ENTRY_MID_crossed_row",
            "E4_exit_stale_gap_at_900",
            "E5_horizon_past_last_row",
            "E13_integer_t_s_on_boundary",
        ]
        for tag in wanted:
            edge = expected["edge_cases"][tag]
            matches = [
                sweep
                for sweep in document["sweeps"]
                if sweep["ticker"] == edge["ticker"]
                and sweep["t_s"] == edge["t_s"]
                and sweep["taker_side"] == edge["taker_side"]
            ]
            self.assertEqual(len(matches), 1, tag)
            self.assertEqual(records[matches[0]["sweep_id"]], expected_records[matches[0]["sweep_id"]])
        e1 = [
            sweep
            for sweep in document["sweeps"]
            if sweep["t_s"] == expected["edge_cases"]["E1_NO_PRE_MID"]["t_s"]
        ][0]
        self.assertEqual(records[e1["sweep_id"]]["status"], "NO_PRE_MID")
        self.assertIsNotNone(records[e1["sweep_id"]]["m_E"])


if __name__ == "__main__":
    unittest.main()
