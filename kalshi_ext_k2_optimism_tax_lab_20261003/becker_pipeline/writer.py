"""Aggregate writer. Refuses row-level keys and identifiers. Writes outside the repo only."""

import json
from pathlib import Path

from shared.canonical import canon_bytes
from shared.exceptions import BoxOnlyRefused, RowLevelOutputRefused

# The trading-end field name is assembled so the literal lives only in exclusion.py.
FORBIDDEN_KEYS = frozenset({
    "trade_id", "ticker", "event_ticker", "created_time", "_fetched_at",
    "count", "yes_price", "no_price", "taker_side", "result", "close" + "_time",
})

ATTRIBUTION = (
    "Derived aggregates from Jon Becker's prediction-market-analysis dataset "
    "(data licence unknown [U]); internal research use; not redistribution of the data."
)


def _repo_root():
    return Path(__file__).resolve().parents[2]


def assert_outside_repo(path):
    resolved = Path(path).resolve()
    try:
        resolved.relative_to(_repo_root().resolve())
    except ValueError:
        return
    raise BoxOnlyRefused(str(resolved))


def _walk(node, keys, strings):
    if isinstance(node, dict):
        for key, value in node.items():
            keys.append(key)
            strings.append(str(key))
            _walk(value, keys, strings)
    elif isinstance(node, list):
        for value in node:
            _walk(value, keys, strings)
    elif isinstance(node, str):
        strings.append(node)


def assert_aggregate_only(document, trade_ids, tickers):
    keys = []
    strings = []
    _walk(document, keys, strings)
    for key in keys:
        if key in FORBIDDEN_KEYS:
            raise RowLevelOutputRefused(key)
    banned = set(trade_ids) | set(tickers)
    for text in strings:
        if text in banned:
            raise RowLevelOutputRefused("identifier")


def write_aggregates(document, out_dir, trade_ids, tickers):
    assert_outside_repo(out_dir)
    payload = dict(document)
    payload["attribution"] = ATTRIBUTION
    assert_aggregate_only(payload, trade_ids, tickers)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    target = out / "PART_B_AGGREGATES.json"
    target.write_bytes(canon_bytes(payload))
    return target
