"""Q6 strict selector. Every fixture here is synthetic."""
from __future__ import annotations

import json
import unittest

from card01_amc.select_forecast import (
    CARD,
    CSV_URL,
    DECISION,
    R0,
    UNIVERSE_SHA,
    WINDOW_END,
    OutcomeKeyRefused,
    SelectorError,
    dumps,
    select_forecast,
)
from tests.support import sha256_bytes

RUN_AT = "2026-11-02T12:00:00Z"
OTHER = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
OTHER_2 = "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"


def _derived(raw, fetched):
    doc = {
        "card": CARD,
        "source_url": CSV_URL,
        "source_sha256": sha256_bytes(raw),
        "source_fetched_at_utc": fetched,
        "universe_ref": {"sha256": UNIVERSE_SHA},
        "n_rows": 1,
        "rows": [{"race_code": "AL-02", "dem_prob": 50.0}],
    }
    return json.dumps(doc, sort_keys=True).encode()


def _capture(**overrides):
    row = {
        "record_type": "capture",
        "source": "races_summary",
        "url": CSV_URL,
        "status": 200,
        "attempt": 1,
        "run_id": "run-1",
        "capture_date_utc": "2026-10-31",
        "fetched_at_utc": "2026-10-31T18:00:00Z",
    }
    row.update(overrides)
    return row


def _asset(run_id, digest, fetched, capture_date="2026-10-31"):
    return {
        "record_type": "capture",
        "source": "methodology_asset",
        "status": 200,
        "run_id": run_id,
        "capture_date_utc": capture_date,
        "fetched_at_utc": fetched,
        "methodology_asset_sha256": digest,
        "methodology_text_sha256": "dd" * 32,
    }


def _pack(raw, derived, raw_rel, derived_rel, **overrides):
    row = _capture(
        sha256=sha256_bytes(raw),
        bytes=len(raw),
        raw_path_private=raw_rel,
        derived_path=derived_rel,
        derived_sha256=sha256_bytes(derived),
        derived_n_rows=1,
        **overrides,
    )
    return row, {raw_rel: raw, derived_rel: derived}


def _select(records, files, daily=None, hook=None):
    if daily is None:
        daily = json.dumps({"run_id": "run-1", "runner_sha256": "aa" * 32}) + "\n"
        daily += json.dumps({"run_id": "run-0", "runner_sha256": "ee" * 32}) + "\n"
    log = "".join(json.dumps(row) + "\n" for row in records).encode()
    return select_forecast(log, daily.encode() if isinstance(daily, str) else daily, ".", RUN_AT, rebuild_derived=hook, files=files)


class SelectorTests(unittest.TestCase):
    def test_empty_late_and_stale_windows_are_missing(self):
        self.assertEqual(_select([], {})["status"], "FORECAST_FILE_MISSING")
        late_raw = b"late"
        stale_raw = b"stale"
        late_der = _derived(late_raw, "2026-11-02T00:00:00Z")
        stale_der = _derived(stale_raw, "2026-10-01T00:00:00Z")
        late, late_files = _pack(late_raw, late_der, "raw/late.csv", "derived/late.json", fetched_at_utc="2026-11-02T00:00:00Z")
        stale, stale_files = _pack(stale_raw, stale_der, "raw/stale.csv", "derived/stale.json", fetched_at_utc="2026-10-01T00:00:00Z")
        files = {**late_files, **stale_files}
        got = _select([late, stale], files)
        self.assertEqual(got["status"], "FORECAST_FILE_MISSING")
        self.assertEqual(got["n_late"], 1)
        self.assertEqual(got["n_stale"], 1)
        self.assertEqual(got["n_in_window"], 0)

    def test_non_200_latest_day_keeps_the_prior_in_window_file(self):
        raw = b"good-raw"
        derived = _derived(raw, "2026-10-30T18:00:00Z")
        good, files = _pack(
            raw, derived, "raw/good.csv", "derived/good.json",
            fetched_at_utc="2026-10-30T18:00:00Z",
            run_id="run-1",
            capture_date_utc="2026-10-30",
        )
        missed = _capture(
            status=404,
            fetched_at_utc="2026-11-01T18:00:00Z",
            sha256="ff" * 32,
            bytes=1,
            raw_path_private="raw/miss.csv",
            derived_path="derived/miss.json",
            derived_sha256="ff" * 32,
            run_id="run-miss",
            capture_date_utc="2026-11-01",
        )
        asset = _asset("run-1", R0, "2026-10-30T18:00:00Z", "2026-10-30")
        got = _select([good, missed, asset], files)
        self.assertEqual(got["status"], "SELECTED")
        self.assertEqual(got["selected"]["fetched_at_utc"], "2026-10-30T18:00:00Z")
        self.assertEqual(got["n_non_200"], 1)
        self.assertEqual(got["regime"]["label"], "R0")
        self.assertEqual(got["sensitivity_pre_change"], "NOT_APPLICABLE")

    def test_ties_and_corrupt_latest_does_not_step_back(self):
        raw = b"same-raw"
        derived = _derived(raw, "2026-10-31T18:00:00Z")
        first, files = _pack(raw, derived, "raw/a.csv", "derived/a.json", fetched_at_utc="2026-10-31T18:00:00Z")
        second, _files2 = _pack(raw, derived, "raw/a.csv", "derived/a.json", fetched_at_utc="2026-10-31T18:00:00Z")
        tied = _select([first, second, _asset("run-1", R0, "2026-10-31T18:00:00Z")], files)
        self.assertEqual(tied["status"], "SELECTED")
        self.assertEqual(tied["selected"]["line_no"], 1)
        self.assertIn("TIE_IDENTICAL_SHA", tied["flags"])

        other = b"other-raw"
        other_der = _derived(other, "2026-10-31T18:00:00Z")
        left, left_files = _pack(raw, derived, "raw/a.csv", "derived/a.json")
        right, right_files = _pack(other, other_der, "raw/b.csv", "derived/b.json")
        ambiguous = _select([left, right], {**left_files, **right_files})
        self.assertEqual(ambiguous["status"], "FORECAST_FILE_AMBIGUOUS")
        self.assertIsNone(ambiguous["selected"])

        early_raw = b"early"
        early_der = _derived(early_raw, "2026-10-28T18:00:00Z")
        early, early_files = _pack(
            early_raw, early_der, "raw/early.csv", "derived/early.json",
            fetched_at_utc="2026-10-28T18:00:00Z", run_id="run-0", capture_date_utc="2026-10-28",
        )
        late_raw = b"late-good"
        late_der = _derived(late_raw, "2026-10-31T18:00:00Z")
        late, late_files = _pack(late_raw, late_der, "raw/late.csv", "derived/late.json")
        late_files["raw/late.csv"] = b"not-the-bytes"
        corrupt = _select([early, late], {**early_files, **late_files})
        self.assertEqual(corrupt["status"], "FORECAST_FILE_CORRUPT")
        self.assertEqual(corrupt["status_reason"], "RAW_SHA_MISMATCH")
        self.assertIsNone(corrupt["selected"])

    def test_rebuild_hook_and_fail_closed_without_it(self):
        raw = b"rebuild-raw"
        derived = _derived(raw, "2026-10-31T18:00:00Z")
        record, files = _pack(raw, derived, "raw/a.csv", "derived/a.json")
        files["derived/a.json"] = b"stale-derived"
        asset = _asset("run-1", R0, "2026-10-31T18:00:00Z")

        def hook(raw_bytes, rec):
            self.assertEqual(raw_bytes, raw)
            return derived

        rebuilt = _select([record, asset], files, hook=hook)
        self.assertEqual(rebuilt["status"], "SELECTED")
        self.assertIn("DERIVED_REBUILT_MATCH", rebuilt["flags"])
        self.assertTrue(rebuilt["selected"]["derived_rebuilt"])

        closed = _select([record, asset], files, hook=None)
        self.assertEqual(closed["status"], "FORECAST_FILE_CORRUPT")
        self.assertEqual(closed["status_reason"], "DERIVED_SHA_MISMATCH")
        self.assertIn("DERIVED_REBUILD_UNAVAILABLE", closed["flags"])

        def mismatch(raw_bytes, rec):
            return b"still-wrong"

        still = _select([record, asset], files, hook=mismatch)
        self.assertEqual(still["status"], "FORECAST_FILE_CORRUPT")
        self.assertEqual(still["status_reason"], "DERIVED_SHA_MISMATCH")
        self.assertNotIn("DERIVED_REBUILT_MATCH", still["flags"])

    def test_null_derived_corrupt_log_and_regimes(self):
        raw = b"null-derived"
        record = _capture(
            sha256=sha256_bytes(raw),
            bytes=len(raw),
            raw_path_private="raw/a.csv",
            derived_path=None,
            derived_sha256=None,
        )
        got = _select([record], {"raw/a.csv": raw})
        self.assertEqual(got["status"], "FORECAST_FILE_UNPARSABLE")
        self.assertEqual(got["status_reason"], "DERIVED_PATH_NULL")

        corrupt_log = select_forecast(b"{not json}\n", b"", ".", RUN_AT, files={})
        self.assertEqual(corrupt_log["status"], "FORECAST_LOG_CORRUPT")

        r0_raw = b"r0"
        r0_der = _derived(r0_raw, "2026-10-26T18:00:00Z")
        r0, r0_files = _pack(
            r0_raw, r0_der, "raw/r0.csv", "derived/r0.json",
            fetched_at_utc="2026-10-26T18:00:00Z", run_id="run-0", capture_date_utc="2026-10-26",
        )
        r1_raw = b"r1"
        r1_der = _derived(r1_raw, "2026-10-30T18:00:00Z")
        r1, r1_files = _pack(
            r1_raw, r1_der, "raw/r1.csv", "derived/r1.json",
            fetched_at_utc="2026-10-30T18:00:00Z", run_id="run-1", capture_date_utc="2026-10-30",
        )
        files = {**r0_files, **r1_files}
        changed = _select([
            r0,
            _asset("run-0", R0, "2026-10-26T18:00:00Z", "2026-10-26"),
            r1,
            _asset("run-1", OTHER, "2026-10-30T18:00:00Z", "2026-10-30"),
        ], files)
        self.assertEqual(changed["status"], "SELECTED")
        self.assertEqual(changed["regime"]["label"], "R1")
        self.assertTrue(changed["regime"]["regime_changed_since_freeze"])
        self.assertEqual(changed["sensitivity_pre_change"]["status"], "SELECTED")
        self.assertEqual(changed["sensitivity_pre_change"]["selected"]["run_id"], "run-0")

        r2_raw = b"r2"
        r2_der = _derived(r2_raw, "2026-10-31T18:00:00Z")
        r2, r2_files = _pack(
            r2_raw, r2_der, "raw/r2.csv", "derived/r2.json",
            fetched_at_utc="2026-10-31T18:00:00Z", run_id="run-2", capture_date_utc="2026-10-31",
        )
        ranked = _select([
            r1,
            _asset("run-1", OTHER, "2026-10-30T18:00:00Z", "2026-10-30"),
            r2,
            _asset("run-2", OTHER_2, "2026-10-31T18:00:00Z", "2026-10-31"),
        ], {**r1_files, **r2_files})
        self.assertEqual(ranked["regime"]["label"], "R2")
        self.assertEqual(ranked["sensitivity_pre_change"], "UNAVAILABLE_NO_PRECHANGE_FILE")

        bare_raw = b"bare"
        bare_der = _derived(bare_raw, "2026-10-31T18:00:00Z")
        bare, bare_files = _pack(bare_raw, bare_der, "raw/bare.csv", "derived/bare.json")
        unmonitored = _select([bare], bare_files)
        self.assertEqual(unmonitored["regime"]["label"], "UNMONITORED")
        self.assertEqual(unmonitored["sensitivity_pre_change"], "UNAVAILABLE_NO_PRECHANGE_FILE")

    def test_outcome_key_rerun_and_run_at(self):
        raw = b"clean"
        derived = _derived(raw, "2026-10-31T18:00:00Z")
        record, files = _pack(raw, derived, "raw/a.csv", "derived/a.json")
        asset = _asset("run-1", R0, "2026-10-31T18:00:00Z")
        first = _select([record, asset], files)
        second = _select([record, asset], files)
        self.assertEqual(dumps(first), dumps(second))
        self.assertNotIn("dem_prob", dumps(first))
        self.assertNotIn(WINDOW_END, first["selected"]["raw_relpath"])
        self.assertFalse(first["selected"]["raw_relpath"].startswith("/"))
        leaked = dict(record)
        leaked["y"] = None
        with self.assertRaises(OutcomeKeyRefused):
            _select([leaked], files)
        with self.assertRaises(SelectorError):
            select_forecast(b"", b"", ".", DECISION, files={})
        with self.assertRaises(SelectorError):
            select_forecast(b"", b"", ".", WINDOW_END, files={})
        absent = select_forecast(None, b"", ".", RUN_AT, files={})
        self.assertEqual(absent["status"], "FORECAST_LOG_MISSING")


if __name__ == "__main__":
    unittest.main()
