"""Canonical JSON (K1 R37 / K2 R49)."""

import hashlib
import json
from decimal import Decimal


def canon_bytes(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def canon_sha256(obj):
    return hashlib.sha256(canon_bytes(obj)).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def q6(value):
    """Report $/contract and shares at 6 decimal places. None stays None."""
    if value is None:
        return None
    return float(Decimal(str(value)).quantize(Decimal("0.000001")))


def q4(value):
    """Report contract-hours at 4 decimal places."""
    if value is None:
        return None
    return float(Decimal(str(value)).quantize(Decimal("0.0001")))
