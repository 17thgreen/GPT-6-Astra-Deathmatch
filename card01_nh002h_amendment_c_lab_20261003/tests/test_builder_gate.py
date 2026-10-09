"""AF-8 builder and the NH-001 gate transcription, with a test-only fee function."""
from __future__ import annotations

import copy
import re
import unittest

from card01_amc.build_rows import (
    BOOK_WINDOW_END_UTC,
    BOOK_WINDOW_START_UTC,
    DECISION_SNAPSHOT_UTC,
    FORECAST_EARLIEST_UTC,
    FORECAST_LATEST_UTC,
    OutcomeKeyRefused,
    dumps,
)
from card01_amc.entry_gate import RESERVE, SELECT_EPS, OutcomePresent, gate
from tests.support import build_from, universe


def _built(forecast, mapping, book):
    doc, raw = universe()
    return build_from(doc, raw, forecast, mapping, book)


def _inputs():
    doc, _raw = universe()
    codes = doc["universe_2026_house"]
    from tests.support import full_books

    forecast, mapping, book = full_books(codes)
    return codes, forecast, mapping, book


def _snap(book, code):
    ticker = "T-" + code
    for snap in book["snapshots"]:
        if snap["ticker"] == ticker:
            return snap
    raise KeyError(code)


def _map(mapping, code):
    for row in mapping["races"]:
        if row["race"] == code:
            return row
    raise KeyError(code)


def _fc(forecast, code):
    for row in forecast["rows"]:
        if row["race_code"] == code:
            return row
    raise KeyError(code)


class BuilderTests(unittest.TestCase):
    def test_constants_are_the_frozen_window(self):
        self.assertEqual(DECISION_SNAPSHOT_UTC, "2026-11-02T22:00:00Z")
        self.assertEqual(BOOK_WINDOW_START_UTC, "2026-11-02T21:45:00Z")
        self.assertEqual(BOOK_WINDOW_END_UTC, "2026-11-02T22:15:00Z")
        self.assertEqual(FORECAST_EARLIEST_UTC, "2026-10-25T22:00:00Z")
        self.assertEqual(FORECAST_LATEST_UTC, "2026-11-01T22:00:00Z")

    def test_universe_order_state_and_determinism(self):
        codes, forecast, mapping, book = _inputs()
        first = _built(forecast, mapping, book)
        second = _built(forecast, mapping, book)
        self.assertEqual(dumps(first), dumps(second))
        self.assertEqual([row["race_id"] for row in first["rows"]], codes)
        self.assertEqual(len(first["rows"]), 92)
        states = {row["state"] for row in first["rows"]}
        self.assertEqual(len(states), 28)
        for row in first["rows"]:
            self.assertEqual(row["state"], row["race_id"][:2])
            self.assertIsNotNone(re.fullmatch(r"[A-Z]{2}", row["state"]))
            self.assertIsNone(row["y"])
            self.assertIsNone(row["exclusion_reason"])
            self.assertEqual(row["mapping_status"], "KXHOUSERACE")
            self.assertEqual(row["p_model"], 0.55)
            self.assertEqual(row["p_market"], 0.5)
        self.assertEqual(first["exclusions"], [])

    def test_legacy_series(self):
        codes, forecast, mapping, book = _inputs()
        _map(mapping, "AZ-01")["series"] = "HOUSEAZ1"
        built = _built(forecast, mapping, book)
        row = built["rows"][codes.index("AZ-01")]
        self.assertEqual(row["mapping_status"], "LEGACY")
        self.assertEqual(row["series"], "HOUSEAZ1")
        self.assertIsNone(row["exclusion_reason"])

    def test_each_exclusion_keeps_the_row(self):
        cases = {
            "mapping_unresolved": lambda f, m, b: _map(m, "AL-02").update({"status": "unresolved_rate_limited"}),
            "no_admissible_forecast": lambda f, m, b: _fc(f, "AL-02").update({"dem_prob": "55"}),
            "snapshot_outside_window": lambda f, m, b: _snap(b, "AL-02").update({"received_at_utc": "2026-11-02T21:44:59Z"}),
            "market_closed_or_settled": lambda f, m, b: _snap(b, "AL-02").update({"market_status": "settled"}),
            "no_two_sided_book": lambda f, m, b: _snap(b, "AL-02").update({"yes_bid": 0.0}),
        }
        codes, forecast0, mapping0, book0 = _inputs()
        index = codes.index("AL-02")
        for reason, mutate in cases.items():
            forecast, mapping, book = copy.deepcopy(forecast0), copy.deepcopy(mapping0), copy.deepcopy(book0)
            mutate(forecast, mapping, book)
            built = _built(forecast, mapping, book)
            self.assertEqual([row["race_id"] for row in built["rows"]], codes, reason)
            row = built["rows"][index]
            self.assertEqual(row["exclusion_reason"], reason, reason)
            self.assertIsNone(row["p_market"], reason)
            self.assertIsNone(row["p_model"], reason)
            self.assertIsNone(row["y"], reason)
            self.assertEqual(built["exclusions"][0]["race_id"], "AL-02")

    def test_book_shapes_and_window_edges(self):
        codes, forecast, mapping, book = _inputs()
        index = codes.index("AL-02")
        shapes = (
            {"yes_ask": None},
            {"yes_bid": 0.70, "yes_ask": 0.40},
            {"yes_ask": 1.0},
        )
        for update in shapes:
            book2 = copy.deepcopy(book)
            _snap(book2, "AL-02").update(update)
            row = _built(forecast, mapping, book2)["rows"][index]
            self.assertEqual(row["exclusion_reason"], "no_two_sided_book")

        early = copy.deepcopy(book)
        _snap(early, "AL-02")["received_at_utc"] = "2026-11-02T21:45:00Z"
        self.assertIsNone(_built(forecast, mapping, early)["rows"][index]["exclusion_reason"])
        late = copy.deepcopy(book)
        _snap(late, "AL-02")["received_at_utc"] = "2026-11-02T22:15:01Z"
        self.assertEqual(
            _built(forecast, mapping, late)["rows"][index]["exclusion_reason"],
            "snapshot_outside_window",
        )
        tied = copy.deepcopy(book)
        _snap(tied, "AL-02").update({"received_at_utc": "2026-11-02T22:10:00Z", "yes_bid": 0.50, "yes_ask": 0.70})
        tied["snapshots"].append({
            "ticker": "T-AL-02",
            "received_at_utc": "2026-11-02T21:50:00Z",
            "yes_bid": 0.30,
            "yes_ask": 0.40,
            "yes_bid_qty": 3,
            "yes_ask_qty": 4,
            "market_status": "active",
        })
        chosen = _built(forecast, mapping, tied)["rows"][index]
        self.assertEqual(chosen["yes_bid"], 0.30)
        self.assertEqual(chosen["p_market"], 0.35)

        for stamp in ("2026-11-01T22:00:00Z", "2026-10-25T22:00:00Z"):
            forecast2 = copy.deepcopy(forecast)
            forecast2["source_fetched_at_utc"] = stamp
            self.assertEqual(_built(forecast2, mapping, book)["exclusions"], [])
        late_fc = copy.deepcopy(forecast)
        late_fc["source_fetched_at_utc"] = "2026-11-01T22:00:01Z"
        self.assertEqual(_built(late_fc, mapping, book)["rows"][0]["exclusion_reason"], "no_admissible_forecast")

    def test_refuses_outcome_keys(self):
        _codes, forecast, mapping, book = _inputs()
        leaked = copy.deepcopy(forecast)
        leaked["y"] = None
        with self.assertRaises(OutcomeKeyRefused):
            _built(leaked, mapping, book)
        settled = copy.deepcopy(book)
        settled["snapshots"][0]["settlement"] = "yes"
        with self.assertRaises(OutcomeKeyRefused):
            _built(forecast, mapping, settled)

    def test_mapped_without_ticker_is_not_a_window_miss(self):
        codes, forecast, mapping, book = _inputs()
        index = codes.index("AL-02")
        for blank in (None, ""):
            mapping2 = copy.deepcopy(mapping)
            _map(mapping2, "AL-02")["chosen_ticker"] = blank
            row = _built(forecast, mapping2, book)["rows"][index]
            self.assertEqual(row["exclusion_reason"], "no_ticker_for_mapped_race")
            self.assertNotEqual(row["exclusion_reason"], "snapshot_outside_window")
            self.assertIsNone(row["p_market"])
            self.assertIsNone(row["p_model"])
            self.assertEqual(row["mapping_status"], "KXHOUSERACE")

    def test_same_party_only_from_explicit_fields(self):
        codes, forecast, mapping, book = _inputs()
        index = codes.index("AL-02")
        flagged = copy.deepcopy(forecast)
        _fc(flagged, "AL-02")["same_party"] = True
        _fc(flagged, "AL-02")["rep_name"] = "(No Republican)"
        _fc(flagged, "AL-02")["dem_name"] = "(No Democrat)"
        row = _built(flagged, mapping, book)["rows"][index]
        self.assertIsNone(row["exclusion_reason"])
        self.assertNotIn("same_party_race", row["exclusion_reasons"])
        self.assertEqual(row["p_model"], 0.55)
        self.assertEqual(row["yes_bid"], 0.40)

    def test_p1_spelling_changes_sort_order(self):
        usps = sorted(["NE", "NH", "NV"])
        names = sorted(["Nebraska", "New Hampshire", "Nevada"])
        self.assertEqual(usps, ["NE", "NH", "NV"])
        self.assertEqual(names, ["Nebraska", "Nevada", "New Hampshire"])
        self.assertNotEqual(usps, names)


class GateSelectionTests(unittest.TestCase):
    def _open(self):
        from tests.test_fee_source import attest_pass, synth_bytes, synth_overrides
        raw = synth_bytes()
        return raw, synth_overrides(raw), attest_pass(raw)

    def _row(self, **kwargs):
        row = {
            "race_id": "AL-02",
            "state": "AL",
            "mapping_status": "KXHOUSERACE",
            "series": "KXHOUSERACE",
            "p_market": 0.25,
            "p_model": 0.90,
            "y": None,
            "ticker": "T-AL-02",
            "yes_bid": 0.20,
            "yes_ask": 0.30,
            "yes_bid_qty": 5,
            "yes_ask_qty": 5,
            "exclusion_reason": None,
        }
        row.update(kwargs)
        return row

    def _gate(self, rows):
        raw, overrides, attest = self._open()
        return gate(rows, raw, fee_attest=attest, **overrides)

    def test_yes_no_tie_boundary_and_qty(self):
        yes = self._gate([self._row()])
        self.assertEqual(yes["status"], "OK")
        self.assertEqual(yes["signals"][0]["side"], "D_YES")
        self.assertEqual(yes["signals"][0]["price"], 0.30)
        self.assertEqual(yes["signals"][0]["fee_decimal"], "0.03")
        self.assertEqual(yes["signals"][0]["fee_rounding"], "NON_DIRECT_CEIL_CENT")
        self.assertGreater(yes["signals"][0]["expected_net_gate"], float(RESERVE + SELECT_EPS))

        no = self._gate([self._row(p_market=0.85, p_model=0.10, yes_bid=0.80, yes_ask=0.90)])
        self.assertEqual(no["signals"][0]["side"], "D_NO")
        self.assertEqual(no["signals"][0]["price"], 0.20)
        self.assertEqual(no["signals"][0]["fee_decimal"], "0.02")

        tie = self._gate([self._row(p_market=0.50, p_model=0.50, yes_bid=0.95, yes_ask=0.05)])
        self.assertEqual(tie["n_selected"], 1)
        self.assertEqual(tie["signals"][0]["side"], "D_YES")
        self.assertEqual(tie["signals"][0]["price"], 0.05)
        self.assertEqual(tie["signals"][0]["fee_decimal"], "0.01")

        # Headline net is exactly the reserve. The direct-member fee would clear it.
        edge = self._gate([self._row(p_market=0.58, p_model=0.58, yes_bid=0.40, yes_ask=0.50)])
        self.assertEqual(edge["status"], "OK")
        self.assertEqual(edge["n_selected"], 0)
        self.assertEqual(edge["signals"], [])

        thin = self._gate([self._row(yes_ask_qty=0)])
        self.assertEqual(thin["n_selected"], 0)

    def test_refuses_non_null_y(self):
        with self.assertRaises(OutcomePresent):
            self._gate([self._row(y=1)])

    def test_absent_fee_source_blocks(self):
        result = gate([self._row()])
        self.assertEqual(result["status"], "BLOCKED_FEE_UNVERIFIED")
        self.assertIsNone(result["signals"])
        self.assertEqual(result["reason"], "FEE_SOURCE_ABSENT")
        self.assertEqual(result["blocked_series"], [])


if __name__ == "__main__":
    unittest.main()
