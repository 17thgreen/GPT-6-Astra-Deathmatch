"""Canonical JSON: sorted keys, compact separators, UTF-8."""

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


def write_json(path, obj):
    path.write_bytes(canonical_bytes(obj))
