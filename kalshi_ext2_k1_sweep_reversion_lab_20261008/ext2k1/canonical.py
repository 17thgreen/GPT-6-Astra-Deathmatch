"""KD-1 canonical JSON. Same rule as the K1 lab, reimplemented here."""

import hashlib
import json


def canonical_bytes(obj):
    payload = json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )
    return payload.encode("utf-8")


def canonical_sha256(obj):
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()
