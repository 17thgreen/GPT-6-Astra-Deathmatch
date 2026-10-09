"""Regime-split and secondary-metric tests. Synthetic fixtures only."""
from __future__ import annotations

import ast
import json
import os
import random
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from card01_amc.book_1103 import LABELS, adverse_selection, quote_for_ticker
from card01_amc.fee_source import PinnedEntry, pinned_taker_fee
from card01_amc.pinload import load_national_miss
from card01_amc.regime_split import (
    FROZEN_13,
    build_regime_split,
    pre_change_snapshot,
    regime_labels,
    safe_block,
)
from card01_amc.regime_split_secondary import (
    build_report,
    main,
    output_inside_repo,
    render,
)
from card01_amc.score import score_document
from card01_amc.secondary_metrics import (
    capital_hours,
    drawdown,
    event_concentration,
    executable_usd_per_day,
    fee_views,
    holding_hours,
    log_loss_and_calibration,
    m3_mids_gaps,
    signals_and_size,
)
from tests.support import LAB, universe
from tests.test_fee_admission_v2 import ADMITTED_ID, _copy_kit, _no_fee_numbers, _repin

EXPECTED = json.loads((LAB / "tests" / "fixtures" / "SYNTH_R1_EXPECTED_VALUES.json").read_text())
RETIRED = (
    "PENDING_ADOPTION_RULE_AMENDMENT",
    "FEE_ATTESTATION_MISSING",
    "FEE_REATTEST_NOT_PASS",
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


def _entry():
    return PinnedEntry("XS1", "quadratic", Decimal("1"), "1", "synth", "ab" * 32, "0.07")


def _scored_spec():
    return [
        ("XA-01", 0.40, 0.60, 1, "KXHOUSERACE"),
        ("XA-02", 0.70, 0.50, 0, "KXHOUSERACE"),
        ("XB-01", 0.30, 0.20, 0, "LEGACY"),
        ("XB-02", 0.55, 0.75, 1, "KXHOUSERACE"),
        ("XC-01", 0.10, 0.30, 0, "LEGACY"),
        ("XC-02", 0.92, 0.88, 1, "KXHOUSERACE"),
    ]


def _row(race, market, model, y, mapping, **extra):
    item = {
        "race_id": race,
        "state": race[:2],
        "mapping_status": mapping,
        "y": y,
        "p_market": market,
        "p_model": model,
        "series": "XS1",
        "ticker": "T-" + race,
        "mid_raw": market,
        "mid_raw_status": "OK" if market is not None else "no_two_sided_book",
        "p_model_raw": model,
        "p_model_raw_status": "OK" if model is not None else "no_admissible_forecast",
        "exclusion_reasons": [],
    }
    item.update(extra)
    return item


def fixture_a(extra=0):
    rows = [_row(*spec) for spec in _scored_spec()]
    rows.append(_row(
        "XA-03", None, 0.40, None, "KXHOUSERACE",
        mid_raw=None, mid_raw_status="no_two_sided_book",
        p_model_raw=0.40, exclusion_reasons=["no_two_sided_book"],
    ))
    rows.append(_row(
        "XC-03", None, None, None, "UNRESOLVED",
        mid_raw=None, mid_raw_status="mapping_unresolved",
        p_model_raw=None, exclusion_reasons=["mapping_unresolved"],
    ))
    for index in range(1, extra + 1):
        rows.append(_row(
            f"XD-{index:02d}", None, None, None, "UNRESOLVED",
            mid_raw=None, mid_raw_status="mapping_unresolved",
            exclusion_reasons=["mapping_unresolved"],
        ))
    return rows


def _selection(label="R1", pre="UNAVAILABLE_NO_PRECHANGE_FILE"):
    return {
        "status": "SELECTED",
        "selected_derived_sha256": "cc" * 32,
        "regime": {
            "label": label,
            "methodology_asset_sha256": "bb" * 32,
            "regime_changed_since_freeze": label != "R0",
        },
        "regime_table": [
            {
                "label": "R0",
                "methodology_asset_sha256": "aa" * 32,
                "first_seen_fetched_at_utc": "2026-09-01T00:00:00Z",
            },
            {
                "label": "R1",
                "methodology_asset_sha256": "bb" * 32,
                "first_seen_fetched_at_utc": "2026-10-03T21:13:06Z",
            },
        ],
        "sensitivity_pre_change": pre,
    }


def _views_for(signals, rows):
    by_id = {row["race_id"]: row for row in rows}
    entries = {}
    for signal in signals:
        series = signal.get("series")
        entries.setdefault(series, _entry())
    return fee_views(signals, by_id, entries), by_id


def fixture_b():
    rows = [
        _row("S1", 0.30, 0.30, 1, "KXHOUSERACE", ticker="TS1"),
        _row("S2", 0.40, 0.40, 1, "KXHOUSERACE", ticker="TS2"),
        _row("S3", 0.05, 0.05, 0, "LEGACY", ticker="TS3"),
    ]
    signals = [
        {"race_id": "S1", "side": "D_YES", "price": Decimal("0.077"), "series": "XS1", "fee_decimal": "0.013"},
        {"race_id": "S2", "side": "D_NO", "price": Decimal("0.50"), "series": "XS1", "fee_decimal": "0.02"},
        {"race_id": "S3", "side": "D_NO", "price": Decimal("0.85"), "series": "XS1", "fee_decimal": "0.01"},
    ]
    book = {
        "capture_status": "OK",
        "snapshots": [
            {"ticker": "TS1", "received_at_utc": "2026-11-03T22:00:00Z", "yes_bid": "0.05", "yes_ask": "0.07", "market_status": "active"},
            {"ticker": "TS2", "received_at_utc": "2026-11-03T22:00:00Z", "yes_bid": "0.56", "yes_ask": "0.60", "market_status": "open"},
            {"ticker": "TS3", "received_at_utc": "2026-11-03T22:00:00Z", "yes_bid": "0.10", "yes_ask": "0.14", "market_status": "active"},
        ],
    }
    settled = {
        "results": [
            {"ticker": "TS1", "result": "yes", "settlement_ts": "2026-11-05T22:00:00.000000Z"},
            {"ticker": "TS2", "result": "yes", "settlement_ts": "2026-11-04T22:00:00.000000Z"},
            {"ticker": "TS3", "result": "no", "settlement_ts": "2026-11-06T22:00:00.000000Z"},
        ]
    }
    return rows, signals, book, settled


def fixture_c():
    rows = [
        _row("C1", 0.40, 0.40, 0, "KXHOUSERACE"),
        _row("C2", 0.40, 0.40, 1, "KXHOUSERACE"),
    ]
    signals = [
        {"race_id": "C1", "side": "D_YES", "price": Decimal("0.055"), "series": "XS1", "fee_decimal": "0.005"},
        {"race_id": "C2", "side": "D_YES", "price": Decimal("0.077"), "series": "XS1", "fee_decimal": "0.013"},
    ]
    return rows, signals


class MetricTests(unittest.TestCase):
    def test_t1a_t1d_brier_log_loss_and_bins(self):
        metrics = log_loss_and_calibration(fixture_a())
        for key, value in EXPECTED["T1a_brier"].items():
            self.assertEqual(metrics["calibration"][key]["brier"], value, key)
            self.assertEqual(metrics["log_loss"][key], EXPECTED["T1b_logloss"][key], key)
            self.assertEqual(metrics["delta_log_loss"][key], EXPECTED["T1b_delta"][key], key)
        arm = metrics["calibration"]["0.5"]
        by_bin = {item["bin"]: item for item in arm["bins"]}
        self.assertEqual(sum(item["count"] for item in arm["bins"]), 6)
        self.assertEqual(by_bin[3]["count"], 2)
        self.assertEqual(by_bin[3]["mean_forecast"], 0.225)
        self.assertEqual(by_bin[3]["observed_freq"], 0.0)
        self.assertEqual(by_bin[6]["count"], 1)
        self.assertEqual(by_bin[6]["mean_forecast"], 0.5)
        self.assertEqual(by_bin[6]["observed_freq"], 1.0)
        self.assertEqual(by_bin[7]["count"], 2)
        self.assertEqual(by_bin[7]["mean_forecast"], 0.625)
        self.assertEqual(by_bin[7]["observed_freq"], 0.5)
        self.assertEqual(by_bin[10]["count"], 1)
        self.assertEqual(by_bin[10]["mean_forecast"], 0.9)
        self.assertEqual(by_bin[10]["observed_freq"], 1.0)
        self.assertTrue(all(item["thin"] for item in arm["bins"]))
        pinned = load_national_miss()
        from card01_amc.secondary_metrics import _bin_index

        scored = [row for row in fixture_a() if row["y"] is not None]
        for weight, spec in EXPECTED["T1c_T1d_bins"].items():
            arm_w = 0.0 if weight == "0" else float(weight)
            probabilities = [pinned.arm_p(row, arm_w) for row in scored]
            self.assertEqual([_bin_index(p) for p in probabilities], spec["bins"], weight)

    def test_t1f_t1g_views_and_concentration(self):
        rows, signals, _book, _settled = fixture_b()
        views, _by = _views_for(signals, rows)
        expected = EXPECTED["T1f_B"]
        for item, spec in zip(views["per_signal"], expected["per_signal"]):
            self.assertEqual(Decimal(item["gross"]), Decimal(spec["gross"]), spec["id"])
            self.assertEqual(Decimal(item["net_headline"]), Decimal(spec["net_HEADLINE"]), spec["id"])
            self.assertEqual(Decimal(item["net_fees_2x"]), Decimal(spec["net_FEES_2X"]), spec["id"])
            self.assertEqual(Decimal(item["gross"]) - Decimal(item["fee_headline"]), Decimal(item["net_headline"]))
            self.assertEqual(Decimal(item["gross"]) - Decimal(item["fee_fees_2x"]), Decimal(item["net_fees_2x"]))
        self.assertEqual(Decimal(views["totals"]["gross"]), Decimal(expected["totals"]["gross"]))
        self.assertEqual(Decimal(views["totals"]["net_headline"]), Decimal(expected["totals"]["net_HEADLINE"]))
        self.assertEqual(Decimal(views["totals"]["net_fees_2x"]), Decimal(expected["totals"]["net_FEES_2X"]))
        blob = json.dumps(views)
        for banned in ("FEE_ONLY_CEIL", "DIRECT_MEMBER_GRID", "fee_only_ceil", "fee_direct_0001", "net_direct_0001"):
            self.assertNotIn(banned, blob)
        concentration, defects = event_concentration(views, None)
        self.assertEqual(defects, [])
        self.assertEqual(concentration["pr_c_match_status"], "PR_C_OUTPUT_ABSENT")
        self.assertEqual(Decimal(concentration["hhi"]), Decimal(EXPECTED["T1g"]["hhi"]))
        self.assertEqual(Decimal(concentration["top1_positive_share"]), Decimal(EXPECTED["T1g"]["top1_positive_share"]))
        self.assertIs(concentration["top1_flag"], True)
        matched, no_defect = event_concentration(views, {
            "net_headline_total": concentration["net_headline_total"],
            "top1_positive_share": concentration["top1_positive_share"],
        })
        self.assertEqual(no_defect, [])
        self.assertIs(matched["pr_c_match"], True)
        mismatched, defects = event_concentration(views, {"net_headline_total": "0", "top1_positive_share": "0.1"})
        self.assertEqual(defects[0]["kind"], "PNL_MISMATCH")
        self.assertEqual(mismatched["pr_c_match_status"], "REPORTING_DEFECT")

        c_rows, c_signals = fixture_c()
        c_views, _by = _views_for(c_signals, c_rows)
        c_expected = EXPECTED["T1f2_C"]
        for item, spec in zip(c_views["per_signal"], c_expected["per_signal"]):
            self.assertEqual(Decimal(item["net_headline"]), Decimal(spec["net_HEADLINE"]), spec["id"])
        self.assertEqual(Decimal(c_views["totals"]["net_headline"]), Decimal(c_expected["totals"]["net_HEADLINE"]))
        self.assertEqual(Decimal(c_views["totals"]["gross"]), Decimal(c_expected["totals"]["gross"]))
        self.assertEqual(Decimal(c_views["totals"]["net_fees_2x"]), Decimal(c_expected["totals"]["net_FEES_2X"]))

    def test_t1h_t1i_adverse_selection_hours_and_edges(self):
        rows, signals, book, settled = fixture_b()
        by_id = {row["race_id"]: row for row in rows}
        block = adverse_selection(signals, by_id, book)
        plus = [item["value"] for item in block["plus_24h"]["per_signal"]]
        settle = [item["value"] for item in block["settlement"]["per_signal"]]
        self.assertEqual([Decimal(item) for item in plus], [Decimal(item) for item in EXPECTED["T1h"]["plus_24h"]])
        self.assertEqual(Decimal(block["plus_24h"]["mean_cents"]), Decimal(EXPECTED["T1h"]["plus_24h_mean"]))
        self.assertEqual(Decimal(block["plus_24h"]["sum_cents"]), Decimal(EXPECTED["T1h"]["plus_24h_sum"]))
        self.assertEqual([Decimal(item) for item in settle], [Decimal(item) for item in EXPECTED["T1h"]["settlement"]])
        self.assertEqual(Decimal(block["settlement"]["mean_cents"]), Decimal(EXPECTED["T1h"]["settlement_mean"]))
        self.assertEqual(block["plus_60s_status"], "NOT_CAPTURED")
        self.assertEqual(block["plus_300s_status"], "NOT_CAPTURED")
        self.assertIsNone(block["plus_60s"])
        views, _by = _views_for(signals, rows)
        settled_by = {item["ticker"]: item for item in settled["results"]}
        hours = capital_hours(signals, by_id, views, settled_by)
        expected_hours = EXPECTED["T1i"]["capital_hours"]
        for item, spec in zip(hours["per_signal"], expected_hours):
            self.assertEqual(item["settlement_ts"], item["settled_at_utc"])
            self.assertEqual(Decimal(item["usd_hours"]), Decimal(spec["usd_hours"]), spec["id"])
        self.assertEqual(Decimal(hours["total_usd_hours"]), Decimal(EXPECTED["T1i"]["capital_hours_total"]))
        down = drawdown(signals, views, settled_by, by_id)
        self.assertEqual(Decimal(down["drawdown_usd"]), Decimal(EXPECTED["T1i"]["drawdown"]))
        executed = executable_usd_per_day(signals, by_id, views)
        self.assertEqual(
            [Decimal(item["edge"]) for item in executed["per_signal"]],
            [Decimal(item) for item in EXPECTED["T1i"]["edges"]],
        )
        self.assertEqual(Decimal(executed["day_sum"]), Decimal(EXPECTED["T1i"]["day_sum"]))
        self.assertEqual(Decimal(executed["median_day"]), Decimal(EXPECTED["T1i"]["day_sum"]))
        self.assertEqual(Decimal(executed["p10_day"]), Decimal(EXPECTED["T1i"]["day_sum"]))
        self.assertEqual(executed["n_days"], 1)

    def test_t4_identity_and_both_orderings(self):
        rows, signals, _book, _settled = fixture_b()
        views, _by = _views_for(signals, rows)
        gross = Decimal(0)
        net_h = Decimal(0)
        net_2 = Decimal(0)
        for item in views["per_signal"]:
            self.assertEqual(Decimal(item["gross"]) - Decimal(item["fee_headline"]), Decimal(item["net_headline"]))
            self.assertEqual(Decimal(item["gross"]) - Decimal(item["fee_fees_2x"]), Decimal(item["net_fees_2x"]))
            gross += Decimal(item["gross"])
            net_h += Decimal(item["net_headline"])
            net_2 += Decimal(item["net_fees_2x"])
        self.assertEqual(gross, Decimal(views["totals"]["gross"]))
        self.assertEqual(net_h, Decimal(views["totals"]["net_headline"]))
        self.assertEqual(net_2, Decimal(views["totals"]["net_fees_2x"]))
        entry = _entry()
        for price, direction in (
            (Decimal("0.055"), "below"),
            (Decimal("0.072"), "below"),
            (Decimal("0.077"), "above"),
        ):
            quoted = pinned_taker_fee(entry, price)
            if direction == "below":
                self.assertLess(quoted["headline"], quoted["FEE_ONLY_CEIL"])
            else:
                self.assertGreater(quoted["headline"], quoted["FEE_ONLY_CEIL"])
        below = above = equal = 0
        price = Decimal("0.0001")
        step = Decimal("0.0001")
        while price < 1:
            quoted = pinned_taker_fee(entry, price)
            headline = quoted["headline"]
            other = quoted["FEE_ONLY_CEIL"]
            if headline < other:
                below += 1
            elif headline > other:
                above += 1
            else:
                equal += 1
            price += step
        self.assertEqual(below, EXPECTED["T4_grid"]["H_lt_FO"])
        self.assertEqual(above, EXPECTED["T4_grid"]["H_gt_FO"])
        self.assertEqual(equal, EXPECTED["T4_grid"]["H_eq_FO"])

    def test_t8_permuting_y_leaves_forecast_free_fields(self):
        rows = fixture_a(84)
        selection = _selection()
        labels = regime_labels(rows, selection)
        gaps = m3_mids_gaps(rows)
        gate = {"signals": [{"race_id": "XA-01", "side": "D_YES"}], "depth_rejected": []}
        size = signals_and_size(gate)
        permuted = []
        for row in rows:
            clone = dict(row)
            if clone.get("y") in (0, 1):
                clone["y"] = 1 - clone["y"]
            permuted.append(clone)
        self.assertEqual(regime_labels(permuted, selection), labels)
        self.assertEqual(m3_mids_gaps(permuted), gaps)
        self.assertEqual(signals_and_size(gate), size)
        signals = [{"race_id": "XA-01", "side": "D_YES", "price": Decimal("0.40"), "series": "XS1", "fee_decimal": "0.02"}]
        # Executable uses the arm probability, not y. Give the row a fee view from the original y.
        views, by_id = _views_for(signals, rows)
        first = executable_usd_per_day(signals, by_id, views)
        views2, by_id2 = _views_for(signals, permuted)
        # Fee and price do not depend on y, so the edge is unchanged even though gross changes.
        self.assertEqual(
            executable_usd_per_day(signals, by_id2, views2)["per_signal"],
            first["per_signal"],
        )

    def test_t17_settlement_hours(self):
        spec = EXPECTED["T17"]
        hours, status = holding_hours("2026-11-05T22:00:00.900000Z")
        self.assertEqual(status, "OK")
        self.assertEqual(hours, Decimal(spec["hours"]))
        usd = Decimal("0.077") * hours
        self.assertEqual(usd, Decimal(spec["usd_hours_P.077"]))
        short, status = holding_hours("2026-11-02T22:00:00.001800Z")
        self.assertEqual(short, Decimal(spec["h_1800us"]))
        longer, status = holding_hours("2026-11-02T22:00:00.005400Z")
        self.assertEqual(longer, Decimal(spec["h_5400us"]))
        missing, status = holding_hours(None)
        self.assertIsNone(missing)
        self.assertEqual(status, "INPUT_MISSING:settlement_ts")
        empty, status = holding_hours("")
        self.assertEqual(status, "INPUT_MISSING:settlement_ts")
        kept, status = holding_hours("2026-11-05T22:00:00Z")
        self.assertIsNone(kept)
        self.assertEqual(status, "INPUT_MISSING:settlement_ts_unparseable")

    def test_t18_eleven_three_labels(self):
        ticker = "T-OPEN"
        early = {
            "ticker": ticker,
            "received_at_utc": "2026-11-02T22:00:00Z",
            "yes_bid": "0.40",
            "yes_ask": "0.42",
            "market_status": "active",
        }
        def snaps(quotes, status="active"):
            base = datetime_offsets()
            out = [early]
            for index, (bid, ask) in enumerate(quotes):
                out.append({
                    "ticker": ticker,
                    "received_at_utc": base[index],
                    "yes_bid": bid,
                    "yes_ask": ask,
                    "market_status": status,
                })
            return {"capture_status": "OK", "snapshots": out}

        closed = quote_for_ticker(snaps([("0.40", "0.42")], status="settled"), ticker)
        self.assertEqual(closed["status"], "MARKET_NOT_OPEN_AT_T")
        self.assertEqual(closed["market_status_verbatim"], "settled")
        self.assertIsNone(closed["yes_mid"])
        absent = quote_for_ticker({"capture_status": "OK", "snapshots": [early]}, ticker)
        self.assertEqual(absent["status"], "NOT_CAPTURED")
        egress = quote_for_ticker(None, ticker)
        self.assertEqual(egress["status"], "NOT_CAPTURED_EGRESS_CLOSED")
        named = quote_for_ticker({"capture_status": "NOT_CAPTURED_EGRESS_CLOSED", "snapshots": []}, ticker)
        self.assertEqual(named["status"], "NOT_CAPTURED_EGRESS_CLOSED")
        ask = quote_for_ticker(snaps([( "0.40", None)] * 3), ticker)
        self.assertEqual(ask["status"], "NO_TWO_SIDED_BOOK_IN_WINDOW")
        self.assertEqual(ask["no_two_sided_detail"], {"missing_side": "ask", "n_captures": 3})
        self.assertIsNone(ask["yes_mid"])
        bid = quote_for_ticker(snaps([(None, "0.42")] * 3), ticker)
        self.assertEqual(bid["no_two_sided_detail"]["missing_side"], "bid")
        both = quote_for_ticker(snaps([(None, None)] * 3), ticker)
        self.assertEqual(both["no_two_sided_detail"]["missing_side"], "both")
        crossed = quote_for_ticker(snaps([("0.70", "0.40")] * 3), ticker)
        self.assertEqual(crossed["no_two_sided_detail"]["missing_side"], "crossed_or_out_of_range")
        valued = quote_for_ticker(snaps([("0.40", "0.42")]), ticker)
        self.assertEqual(valued["status"], "OK")
        self.assertEqual(valued["yes_mid"], Decimal("0.41"))
        rows, signals, _book, _settled = fixture_b()
        block = adverse_selection(signals, {row["race_id"]: row for row in rows}, {"capture_status": "OK", "snapshots": []})
        statuses = {item["status"] for item in block["plus_24h"]["per_signal"]}
        self.assertTrue(statuses <= set(LABELS))
        self.assertEqual(block["plus_60s_status"], "NOT_CAPTURED")
        self.assertEqual(block["plus_300s_status"], "NOT_CAPTURED")


def datetime_offsets():
    return [
        "2026-11-03T21:50:00Z",
        "2026-11-03T22:00:00Z",
        "2026-11-03T22:10:00Z",
    ]


class PartitionTests(unittest.TestCase):
    def test_t2_partition_and_unclassified_share(self):
        rows = fixture_a(84)
        self.assertEqual(len(rows), 92)
        report = build_regime_split(rows, _selection())
        self.assertEqual(report["n_universe"], 92)
        self.assertEqual(report["n_scored"] + report["n_not_scored"], 92)
        self.assertEqual(sum(item["n"] for item in report["rows"]), report["n_scored"])
        labels = [item["regime_label"] for item in report["rows"]]
        self.assertEqual(labels, ["R0", "R1", "UNMONITORED", "UNCLASSIFIED"])
        nonempty = [item for item in report["rows"] if item["n"]]
        self.assertEqual(len(nonempty), 1)
        self.assertEqual(nonempty[0]["regime_label"], "R1")
        self.assertEqual(nonempty[0]["n"], 6)
        self.assertEqual(report["structural_label"], "ROWS_NONEMPTY=1")
        self.assertEqual(report["unclassified_share_of_scored"], "0.000000")
        assigned = []
        for item in report["rows"]:
            assigned.extend(item["race_ids"])
        self.assertEqual(sorted(assigned), ["XA-01", "XA-02", "XB-01", "XB-02", "XC-01", "XC-02"])

        missing = _selection()
        missing["regime"]["label"] = None
        missing_report = build_regime_split(rows, missing)
        self.assertEqual(missing_report["n_unclassified"], 6)
        self.assertEqual(missing_report["unclassified_share_of_scored"], "1.000000")
        bad = _selection()
        bad["regime"]["label"] = "RX"
        self.assertEqual(build_regime_split(rows, bad)["n_unclassified"], 6)
        mismatched = fixture_a(84)
        mismatched[0]["forecast_input_sha256"] = "dd" * 32
        mixed = build_regime_split(mismatched, _selection())
        self.assertEqual(mixed["n_unclassified"], 1)
        self.assertEqual(mixed["unclassified_share_of_scored"], "0.166667")

        two = fixture_a(84)
        r0 = {"XA-01", "XA-02", "XB-01"}
        for row in two:
            if row["race_id"] in r0:
                row["regime_label"] = "R0"
            elif row["y"] is not None:
                row["regime_label"] = "R1"
        split = build_regime_split(two, _selection())
        by_label = {item["regime_label"]: item for item in split["rows"]}
        self.assertEqual(by_label["R0"]["n"], 3)
        self.assertEqual(by_label["R1"]["n"], 3)
        self.assertEqual(by_label["R0"]["states"], 2)
        self.assertEqual(by_label["R1"]["states"], 2)
        self.assertEqual(split["rows_nonempty"], 2)
        self.assertEqual(split["structural_label"], "ROWS_NONEMPTY=2")

    def test_t3_single_regime_block_matches_score(self):
        rows = fixture_a()
        report = build_regime_split(rows, _selection())
        r1 = [item for item in report["rows"] if item["regime_label"] == "R1"][0]
        scored = score_document({"rows": rows})
        self.assertEqual(
            json.dumps(r1["block"], sort_keys=True),
            json.dumps(scored["all_admitted"], sort_keys=True),
        )
        self.assertEqual(report["structural_label"], "ROWS_NONEMPTY=1")

    def test_t6_draw_pin_and_random_call_count(self):
        pinned = load_national_miss()
        rng = random.Random(pinned.SEED)
        states = ["XA", "XB", "XC"]
        draws = [rng.choices(states, k=len(states)) for _ in range(3)]
        self.assertEqual(draws, EXPECTED["T6_first3"])
        calls = {"n": 0}
        real = random.Random.random

        def wrapped(self, *args, **kwargs):
            calls["n"] += 1
            return real(self, *args, **kwargs)

        random.Random.random = wrapped
        try:
            safe_block([row for row in fixture_a() if row["y"] is not None], pinned)
        finally:
            random.Random.random = real
        self.assertEqual(calls["n"], 3 * 10000)

    def test_t11_pre_change_statuses(self):
        rows = fixture_a()
        ids = [row["race_id"] for row in rows if row["y"] is not None]
        not_applicable = _selection("R0", "NOT_APPLICABLE")
        result = pre_change_snapshot(not_applicable, rows, ids, "ee" * 32)
        self.assertEqual(result["status"], "NOT_APPLICABLE")
        self.assertIsNone(result["counts"])
        self.assertIsNone(result["all_admitted"])
        unavailable = pre_change_snapshot(_selection(), None, ids, None)
        self.assertEqual(unavailable["status"], "UNAVAILABLE_NO_PRECHANGE_FILE")
        selected = _selection()
        selected["sensitivity_pre_change"] = {
            "status": "SELECTED",
            "selected": {"derived_sha256": "ee" * 32},
        }
        refused = pre_change_snapshot(selected, rows, ids, "ff" * 32)
        self.assertEqual(refused["status"], "INPUT_MISSING:pre_change_linkage")
        self.assertIsNone(refused["all_admitted"])
        pre_rows = fixture_a()
        pre_rows[0]["y"] = None
        accepted = pre_change_snapshot(selected, pre_rows, ids, "ee" * 32)
        self.assertEqual(accepted["status"], "SELECTED")
        self.assertEqual(set(accepted.keys()), {"status", "counts", "all_admitted", "class"})
        self.assertEqual(accepted["counts"]["n_scored"], 5)
        self.assertEqual(accepted["counts"]["n_admission_differs"], 1)
        self.assertIn("arms", accepted["all_admitted"])

    def test_t12_frozen_thirteen_are_universe_codes(self):
        codes = universe()[0]["universe_2026_house"]
        self.assertEqual(len(FROZEN_13), 13)
        self.assertTrue(FROZEN_13 <= set(codes))
        self.assertEqual(len(set(codes) - FROZEN_13), 79)
        kept = [row for row in (_row(code, 0.4, 0.4, 1, "KXHOUSERACE") for code in codes) if row["race_id"] not in FROZEN_13]
        self.assertEqual(len(kept), 79)


class SafetyAndGuardTests(unittest.TestCase):
    def test_t13_new_modules_and_fixtures_omit_forbidden_substrings(self):
        roots = [
            LAB / "card01_amc" / "regime_split.py",
            LAB / "card01_amc" / "secondary_metrics.py",
            LAB / "card01_amc" / "book_1103.py",
            LAB / "card01_amc" / "regime_split_secondary.py",
            LAB / "card01_amc" / "fee_admission.py",
        ]
        roots.extend((LAB / "tests" / "fixtures").glob("SYNTH_*"))
        for path in roots:
            text = path.read_text().lower()
            for token in FORBIDDEN:
                self.assertNotIn(token, text, path.name)

    def test_t16_path_guard_and_universe_count(self):
        self.assertTrue(output_inside_repo(LAB / "CARD01_REGIME_SPLIT_SECONDARY_x.json"))
        self.assertFalse(output_inside_repo(Path(tempfile.gettempdir()) / "CARD01_REGIME_SPLIT_SECONDARY_x.json"))
        rc = main([
            "--joined-rows", "unused.json",
            "--score", "unused.json",
            "--selection", "unused.json",
            "--gate", "unused.json",
            "--settled", "unused.json",
            "--book-1103", "unused.json",
            "--fee-source", "unused.json",
            "--fee-source-id", "ID",
            "--fee-source-sha256", "ab" * 32,
            "--packet-index", "unused.md",
            "--fee-accept", "unused.json",
            "--out", str(LAB / "CARD01_REGIME_SPLIT_SECONDARY_refused.json"),
        ])
        self.assertEqual(rc, 2)
        self.assertFalse((LAB / "CARD01_REGIME_SPLIT_SECONDARY_refused.json").exists())
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rows = root / "rows.json"
            rows.write_text(json.dumps(fixture_a()))
            code = main([
                "--joined-rows", str(rows),
                "--score", "unused.json",
                "--selection", "unused.json",
                "--gate", "unused.json",
                "--settled", "unused.json",
                "--book-1103", "unused.json",
                "--fee-source", "unused.json",
                "--fee-source-id", "ID",
                "--fee-source-sha256", "ab" * 32,
                "--packet-index", "unused.md",
                "--fee-accept", "unused.json",
                "--out", str(root / "CARD01_REGIME_SPLIT_SECONDARY_short.json"),
            ])
            self.assertEqual(code, 2)

    def test_fewer_than_two_states_nulls_intervals(self):
        rows = [_row("XA-01", 0.4, 0.6, 1, "KXHOUSERACE"), _row("XA-02", 0.5, 0.5, 0, "KXHOUSERACE")]
        block, status = safe_block(rows)
        self.assertEqual(status, "UNDEFINED_FEWER_THAN_2_STATES")
        self.assertIsNone(block["arms"]["0.5"]["CI95_D_raw"])
        self.assertIsNone(block["arms"]["0.5"]["CI95_D_rc"])
        self.assertEqual(block["ci_status"], "UNDEFINED_FEWER_THAN_2_STATES")

    def test_block_error_nulls_intervals(self):
        import card01_amc.regime_split as module

        def boom(rows, pinned):
            raise RuntimeError("synthetic")

        original = module.block_with_boundary_count
        module.block_with_boundary_count = boom
        try:
            block, status = safe_block([_row("XA-01", 0.4, 0.6, 1, "KXHOUSERACE")])
        finally:
            module.block_with_boundary_count = original
        self.assertEqual(status, "ERROR")
        self.assertIsNone(block["arms"])
        self.assertEqual(block["ci_status"], "ERROR")


class ReportTests(unittest.TestCase):
    def _fee(self, root):
        return _copy_kit(root)

    def test_t7_blocked_fee_emits_no_fee_number_and_keeps_forecast(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = self._fee(Path(tmp))
            report = build_report(
                fixture_a(),
                selection=_selection(),
                gate={"status": "OK", "signals": None, "fee_formula_id": "other"},
                fee_source_path=paths[0],
                fee_source_id="FEE_SOURCE_CARD01_v1",
                fee_source_sha256="d4dc8e72ae2b2a72824487eb386d6684c451a5e3b2e9dce58c1a68aaea9436cd",
                packet_index_path=paths[2],
                fee_accept_path=paths[1],
            )
        self.assertEqual(report["verdict_fee_branch"], "FORECAST_ONLY_FEE_BLOCKED")
        self.assertEqual(report["fee_views_status"], "BLOCKED_FEE_UNVERIFIED")
        self.assertIsNone(report["fee_views"])
        self.assertEqual(report["secondary"]["event_concentration_status"], "BLOCKED_FEE_UNVERIFIED")
        self.assertIsNotNone(report["secondary"]["log_loss"])
        self.assertTrue(_no_fee_numbers(report))
        blob = json.dumps(report)
        for token in RETIRED:
            self.assertNotIn(token, blob)

    def test_t5_determinism(self):
        rows = fixture_a(84)
        selection = _selection()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = self._fee(root)
            from card01_amc.pinload import sha256_bytes

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
            kwargs = dict(
                rows=rows,
                selection=selection,
                gate=gate,
                book={"capture_status": "NOT_CAPTURED_EGRESS_CLOSED", "snapshots": []},
                settled={"results": []},
                fee_source_path=paths[0],
                fee_source_id=ADMITTED_ID,
                fee_source_sha256=fee_sha,
                packet_index_path=paths[2],
                fee_accept_path=paths[1],
            )
            first, digest = render(build_report(**kwargs))
            second, digest2 = render(build_report(**kwargs))
            self.assertEqual(first, second)
            self.assertEqual(digest, digest2)
            payload = json.loads(first)
            self.assertEqual(payload["output_sha256"], digest)
            body = {key: value for key, value in payload.items() if key != "output_sha256"}
            recomputed = __import__("hashlib").sha256(
                (json.dumps(body, indent=1, sort_keys=True, ensure_ascii=True) + "\n").encode("ascii")
            ).hexdigest()
            self.assertEqual(recomputed, digest)
            bundle = root / "bundle.json"
            bundle.write_text(json.dumps({
                "rows": rows,
                "selection": selection,
                "gate": gate,
                "book": kwargs["book"],
                "settled": kwargs["settled"],
                "fee_source_path": str(paths[0]),
                "fee_source_id": ADMITTED_ID,
                "fee_source_sha256": kwargs["fee_source_sha256"],
                "packet_index_path": str(paths[2]),
                "fee_accept_path": str(paths[1]),
            }))
            script = (
                "import json,sys\n"
                "from pathlib import Path\n"
                "from card01_amc.regime_split_secondary import build_report, render\n"
                "doc=json.loads(Path(sys.argv[1]).read_text())\n"
                "text,digest=render(build_report(doc['rows'], selection=doc['selection'], gate=doc['gate'], book=doc['book'], settled=doc['settled'], fee_source_path=doc['fee_source_path'], fee_source_id=doc['fee_source_id'], fee_source_sha256=doc['fee_source_sha256'], packet_index_path=doc['packet_index_path'], fee_accept_path=doc['fee_accept_path']))\n"
                "Path(sys.argv[2]).write_text(text)\n"
                "print(digest)\n"
            )
            digests = []
            for seed in ("0", "1"):
                out = root / f"out-{seed}.json"
                env = os.environ.copy()
                env["PYTHONHASHSEED"] = seed
                proc = subprocess.run(
                    [sys.executable, "-c", script, str(bundle), str(out)],
                    cwd=str(LAB),
                    env=env,
                    check=True,
                    capture_output=True,
                    text=True,
                )
                digests.append(proc.stdout.strip())
                self.assertEqual(out.read_text(), first)
            self.assertEqual(digests, [digest, digest])
            (root / "determinism_sha.txt").write_text(digest + "\n")
            print("T5_OUTPUT_SHA256", digest)

    def test_t23_regime_outputs_omit_retired_strings(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = self._fee(root)
            cases = []
            cases.append(build_report(
                [],
                selection=_selection(),
                gate={"status": "OK", "signals": []},
                fee_source_path=paths[0],
                fee_source_id=ADMITTED_ID,
                fee_source_sha256=__import__("card01_amc.pinload", fromlist=["sha256_bytes"]).sha256_bytes(paths[0].read_bytes()),
                packet_index_path=paths[2],
                fee_accept_path=paths[1],
            ))
            doc = json.loads(paths[0].read_bytes())
            doc["series"]["XS1"]["fee_multiplier"] = "1.5"
            doc["series"]["XS1"]["series_endpoint_source"]["fee_multiplier"] = "1.5"
            fee_path, accept_path, index_path, fee_sha = _repin(root, doc)
            cases.append(build_report(
                [],
                selection=_selection(),
                gate={"status": "OK", "signals": [], "series": "XS1"},
                fee_source_path=fee_path,
                fee_source_id=ADMITTED_ID,
                fee_source_sha256=fee_sha,
                packet_index_path=index_path,
                fee_accept_path=accept_path,
                series_used=["XS1"],
            ))
            for report in cases:
                blob = json.dumps(report)
                for token in RETIRED + ("FEE_FORMULA_ID_MISMATCH",):
                    self.assertNotIn(token, blob)
                self.assertTrue(_no_fee_numbers(report) or report["fee_admission"]["fee_admission"] == "ADMITTED_INDEX_ONLY")
        for name in (
            "regime_split.py",
            "secondary_metrics.py",
            "book_1103.py",
            "regime_split_secondary.py",
            "fee_admission.py",
        ):
            text = (LAB / "card01_amc" / name).read_text()
            for token in RETIRED:
                self.assertNotIn(token, text, name)

    def test_t24_admitted_output_omits_sensitivity_rows(self):
        from card01_amc.entry_gate import gate_v2
        from card01_amc.pinload import sha256_bytes

        rows = [
            _row(
                "S1", 0.077, 0.90, 1, "KXHOUSERACE", ticker="TS1",
                yes_bid=0.05, yes_ask=0.077, yes_bid_qty=5, yes_ask_qty=5,
            ),
            _row(
                "S2", 0.50, 0.90, 1, "LEGACY", ticker="TS2",
                yes_bid=0.40, yes_ask=0.50, yes_bid_qty=5, yes_ask_qty=5,
            ),
        ]
        bare = [
            {key: value for key, value in row.items() if key not in ("y", "result", "settlement", "outcome", "settled")}
            for row in rows
        ]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = self._fee(root)

            def once(fee_sha, fee_path, accept_path, index_path):
                gate = gate_v2(
                    bare,
                    fee_source_path=fee_path,
                    fee_source_id=ADMITTED_ID,
                    fee_source_sha256=fee_sha,
                    packet_index_path=index_path,
                    fee_accept_path=accept_path,
                )
                self.assertEqual(gate["status"], "OK")
                self.assertGreaterEqual(len(gate["signals"]), 1)
                return build_report(
                    rows,
                    selection=_selection(),
                    gate=gate,
                    book={"capture_status": "NOT_CAPTURED_EGRESS_CLOSED"},
                    settled={"results": []},
                    fee_source_path=fee_path,
                    fee_source_id=ADMITTED_ID,
                    fee_source_sha256=fee_sha,
                    packet_index_path=index_path,
                    fee_accept_path=accept_path,
                    series_used=["XS1"],
                )

            first = once(sha256_bytes(paths[0].read_bytes()), *paths)
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
            self.assertEqual(first["sensitivity_rows_status"], "SENSITIVITY_BASIS_INCOMPLETE")
            self.assertEqual(first["fee_views"]["per_signal"][0]["fee_headline"], "0.013")
            self.assertEqual(first["fee_state"], "ADMITTED")
            doc = json.loads(paths[0].read_bytes())
            doc["fee_computation"]["sensitivity_rows"][0]["expression"] = "ceil_cent(fee_raw)+1"
            fee_path, accept_path, index_path, fee_sha = _repin(root, doc)
            second = once(fee_sha, fee_path, accept_path, index_path)

            def scrub(obj):
                if isinstance(obj, dict):
                    return {key: scrub(val) for key, val in obj.items() if "sha256" not in key}
                if isinstance(obj, list):
                    return [scrub(item) for item in obj]
                return obj

            self.assertEqual(scrub(first), scrub(second))

    def test_blocked_gate_does_not_emit_zero_totals_when_file_admits(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = self._fee(Path(tmp))
            from card01_amc.pinload import sha256_bytes

            fee_sha = sha256_bytes(paths[0].read_bytes())
            report = build_report(
                fixture_a(),
                selection=_selection(),
                gate={"status": "OK", "signals": [], "fee_attest_verdict": "ATTEST_PASS"},
                fee_source_path=paths[0],
                fee_source_id=ADMITTED_ID,
                fee_source_sha256=fee_sha,
                packet_index_path=paths[2],
                fee_accept_path=paths[1],
            )
        self.assertEqual(report["fee_admission"]["fee_admission"], "ADMITTED_INDEX_ONLY")
        self.assertEqual(report["verdict_fee_branch"], "FORECAST_ONLY_FEE_BLOCKED")
        self.assertEqual(report["fee_state"], "BLOCKED_FEE_UNVERIFIED")
        self.assertEqual(report["secondary"]["fee_block_reason"], "FEE_ADMISSION_MISSING")
        self.assertIsNone(report["fee_views"])
        self.assertNotIn('"fee_headline": "0"', json.dumps(report))

    def test_each_signal_uses_its_own_series_entry(self):
        from decimal import Decimal

        from card01_amc.entry_gate import gate_v2
        from card01_amc.fee_source import PinnedEntry
        from card01_amc.pinload import sha256_bytes
        from card01_amc.secondary_metrics import fee_views

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = self._fee(root)
            fee_sha = sha256_bytes(paths[0].read_bytes())
            rows = [
                _row(
                    "S1", 0.055, 0.90, 1, "KXHOUSERACE", series="XS1",
                    yes_bid=0.04, yes_ask=0.055, yes_bid_qty=5, yes_ask_qty=5,
                ),
                _row(
                    "S2", 0.055, 0.90, 1, "LEGACY", series="XS2",
                    yes_bid=0.04, yes_ask=0.055, yes_bid_qty=5, yes_ask_qty=5,
                ),
            ]
            bare = [
                {key: value for key, value in row.items() if key not in ("y", "result", "settlement", "outcome", "settled")}
                for row in rows
            ]
            gate = gate_v2(
                bare,
                fee_source_path=paths[0],
                fee_source_id=ADMITTED_ID,
                fee_source_sha256=fee_sha,
                packet_index_path=paths[2],
                fee_accept_path=paths[1],
            )
            self.assertEqual([signal["series"] for signal in gate["signals"]], ["XS1", "XS2"])
            report = build_report(
                rows,
                selection=_selection(),
                gate=gate,
                fee_source_path=paths[0],
                fee_source_id=ADMITTED_ID,
                fee_source_sha256=fee_sha,
                packet_index_path=paths[2],
                fee_accept_path=paths[1],
                series_used=["XS1", "XS2"],
            )
        self.assertEqual(report["fee_state"], "ADMITTED")
        self.assertIsNone(report["verdict_fee_branch"])
        self.assertEqual(
            [item["fee_headline"] for item in report["fee_views"]["per_signal"]],
            ["0.005", "0.005"],
        )
        low = PinnedEntry("XS1", "quadratic", Decimal("1"), "1", "synth", "ab" * 32, "0.07")
        high = PinnedEntry("XS2", "quadratic", Decimal("1.5"), "1.5", "synth", "ab" * 32, "0.07")
        views = fee_views(
            [
                {"race_id": "A", "series": "XS1", "side": "D_YES", "price": "0.50", "fee_decimal": "0.02"},
                {"race_id": "B", "series": "XS2", "side": "D_YES", "price": "0.50", "fee_decimal": "0.03"},
            ],
            {},
            {"XS1": low, "XS2": high},
        )
        self.assertNotEqual(views["per_signal"][0]["fee_headline"], views["per_signal"][1]["fee_headline"])
        self.assertEqual(views["per_signal"][1]["fee_headline"], "0.03")


if __name__ == "__main__":
    unittest.main()
