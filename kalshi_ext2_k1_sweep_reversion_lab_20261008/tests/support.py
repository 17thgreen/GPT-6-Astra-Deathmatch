"""Shared synthetic fixtures. Inserts the lab on sys.path for unittest discover."""

import json
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
if str(LAB) not in sys.path:
    sys.path.insert(0, str(LAB))

from ext2k1.canonical import canonical_bytes, canonical_sha256  # noqa: E402
from ext2k1.constants import BUILDER_SHA256, Pins  # noqa: E402
from ext2k1.pins_io import sweeps_module_sha256  # noqa: E402
from ext2k1.report import build_results, published_results  # noqa: E402

FIXTURES = json.loads((LAB / "tests" / "fixtures" / "SYNTH_EXT2K1_FIXTURES.json").read_text(encoding="utf-8"))
EXPECTED = json.loads((LAB / "tests" / "fixtures" / "SYNTH_EXT2K1_EXPECTED.json").read_text(encoding="utf-8"))

SOURCE_PINS = [
    {
        "role": "synthetic tape fixture",
        "path": "tests/fixtures/SYNTH_EXT2K1_FIXTURES.json",
        "bytes": 521486,
        "sha256": "4f6791ee4cce5baa3f67acb29c563c0823b36f6ecea420a03cabe95e8efca430",
    }
]


def synthetic_pins():
    counts = dict(EXPECTED["structural_counts_synth"])
    counts["events"] = len(EXPECTED["EVENTS"])
    return Pins(counts, BUILDER_SHA256)


def near(left, right, tol=1e-12):
    if isinstance(left, bool) or isinstance(right, bool):
        return left == right
    if isinstance(left, float) or isinstance(right, float):
        if left is None or right is None:
            return left is None and right is None
        return abs(left - right) <= tol
    if isinstance(left, dict) and isinstance(right, dict):
        return left.keys() == right.keys() and all(near(left[key], right[key], tol) for key in left)
    if isinstance(left, list) and isinstance(right, list):
        return len(left) == len(right) and all(near(a, b, tol) for a, b in zip(left, right))
    return left == right


_RUN = None


def full_run():
    """One synthetic score. Read-only for callers; determinism tests call build_results themselves."""
    global _RUN
    if _RUN is None:
        tape = FIXTURES["tape"]
        _RUN = build_results(
            tape["rows"],
            tape["markets"],
            tape["week_membership"],
            synthetic_pins(),
            builder_sha256=BUILDER_SHA256,
            source_pins=SOURCE_PINS,
            sweeps_module_sha256=sweeps_module_sha256(),
            b2_rows=tape["b2_fills"],
        )
    return _RUN


def published():
    _receipt, _document, body = full_run()
    return published_results(body)
