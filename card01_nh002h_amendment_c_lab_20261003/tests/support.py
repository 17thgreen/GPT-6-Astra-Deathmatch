"""Shared paths and synthetic fixture builders. No real prices or outcomes."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
REPO = LAB.parent
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

BASE = "813025a0d02a271208f1607c001a10519bb7cc8c"
PIN_SHA = "049368f942741ff4a63acad328a49ff256252587d6c65f1e7e6d65d6101781f2"
INPUT_SHA = "b16ba92bde540a9623f815654bd33b531536aad8b986c4614a08f36dd27cf65e"
OUTPUT_SHA = "0e93e153b7fc03cb996f3200dc576dd770ad638b00a1a0e3ed1e28632b682f23"
UNIVERSE_SHA = "d8af74515e449b151016105f956c5e54a4fb4eac3ec570364da58f8fe47d8ca6"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def universe():
    raw = (LAB / "pins" / "UNIVERSE_2026_HOUSE_FROZEN.json").read_bytes()
    return json.loads(raw), raw


def full_books(codes):
    forecast = {
        "card": "card01-synthetic",
        "capture_date_utc": "2026-10-30T12:00:00Z",
        "source_sha256": "synthetic",
        "source_fetched_at_utc": "2026-10-30T18:00:00Z",
        "dem_prob_units": "percent",
        "rows": [{"race_code": code, "dem_prob": 55.0} for code in codes],
    }
    mapping = {
        "races": [
            {
                "race": code,
                "status": "mapped",
                "series": "KXHOUSERACE",
                "chosen_ticker": "T-" + code,
            }
            for code in codes
        ]
    }
    book = {
        "snapshots": [
            {
                "ticker": "T-" + code,
                "received_at_utc": "2026-11-02T22:00:00Z",
                "yes_bid": 0.40,
                "yes_ask": 0.60,
                "yes_bid_qty": 10,
                "yes_ask_qty": 12,
                "market_status": "active",
            }
            for code in codes
        ]
    }
    return forecast, mapping, book


def build_from(universe_doc, universe_raw, forecast, mapping, book):
    from card01_amc.build_rows import build
    from card01_amc.dem_name_step import ADD_DEM_NAME_SHA256

    codes = universe_doc["universe_2026_house"]
    blobs = {
        "forecast": json.dumps(forecast).encode(),
        "mapping": json.dumps(mapping).encode(),
        "book": json.dumps(book).encode(),
    }
    forecast_sha = sha256_bytes(blobs["forecast"])
    selection = {"status": "SELECTED", "selected_derived_sha256": forecast_sha}
    selection_raw = json.dumps(selection, sort_keys=True).encode()
    by_code = {row["race_code"]: row for row in forecast["rows"] if isinstance(row, dict)}
    v1_rows = []
    for code in codes:
        fc = by_code.get(code, {})
        v1_rows.append({
            "race_code": code,
            "dem_prob": fc.get("dem_prob"),
            "dem_name": "Synthetic Placeholder",
            "dem_name_status": "RESOLVED",
            "same_party_excluded_s5": False,
        })
    step = {
        "status": "DEM_NAME_ACCEPTED",
        "reason": None,
        "expected_script_sha256": ADD_DEM_NAME_SHA256,
        "observed_script_sha256": ADD_DEM_NAME_SHA256,
        "original_sha256": forecast_sha,
        "v1_sha256": None,
        "check": None,
        "v1": {"version": "dem_name_v1", "rows": v1_rows},
    }
    shas = {
        "universe": sha256_bytes(universe_raw),
        "forecast": forecast_sha,
        "mapping": sha256_bytes(blobs["mapping"]),
        "book": sha256_bytes(blobs["book"]),
        "selection": sha256_bytes(selection_raw),
    }
    return build(universe_doc, forecast, mapping, book, shas, selection=selection, dem_name_step=step)


def adopted_manifest(entries=None):
    if entries is None:
        entries = {
            "KXHOUSERACE": {
                "entry_id": "entry-KXHOUSERACE",
                "status": "ADOPTED",
                "fee_type": "quadratic",
                "fee_multiplier": "1",
                "source": "series_endpoint",
            }
        }
    return {"manifest_id": "synthetic-adopted", "status": "ADOPTED", "entries": entries}
