"""Holdout, ADMIT-1, path, and Lee-Ready refusals. Both pipelines call these."""

import datetime as dt

from shared.exceptions import (
    Admit1WindowRejected,
    HoldoutRefused,
    LeeReadyRefused,
    SqlitePathRefused,
)

# Half-open window [2026-09-27T00:00:00Z, 2026-09-30T04:00:00Z).
ADMIT1_LO = dt.datetime(2026, 9, 27, 0, 0, tzinfo=dt.timezone.utc)
ADMIT1_HI = dt.datetime(2026, 9, 30, 4, 0, tzinfo=dt.timezone.utc)

MEASUREMENT_DEVELOPMENT_EVENTS = frozenset({
    "KXNFLGAME-26SEP21NYGLAR",
    "KXNFLGAME-26SEP24ATLGB",
})

LEE_READY_KEYS = frozenset({
    "lee_ready", "lee-ready", "leerready", "tick_rule", "tickrule",
    "print_mid", "inferred_side", "quote_rule",
})


def parse_timestamp(value):
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return dt.datetime.fromtimestamp(float(value), tz=dt.timezone.utc)
    text = str(value).strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    parsed = dt.datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def assert_timestamp_allowed(value):
    stamp = parse_timestamp(value)
    if ADMIT1_LO <= stamp < ADMIT1_HI:
        raise Admit1WindowRejected(stamp.isoformat())
    return stamp


def assert_not_holdout(event=None, game_id=None, ticker=None, holdout_events=(), holdout_game_ids=()):
    if ticker is not None and "KXMLBSPREAD" in str(ticker):
        raise HoldoutRefused(ticker)
    if event is not None and event in MEASUREMENT_DEVELOPMENT_EVENTS:
        raise HoldoutRefused(event)
    if event is not None and event in holdout_events:
        raise HoldoutRefused(event)
    if game_id is not None and game_id in holdout_game_ids:
        raise HoldoutRefused(game_id)


def assert_sqlite_path_refused(path):
    text = str(path).replace("\\", "/")
    base = text.rsplit("/", 1)[-1]
    if base in ("capture.sqlite", "archive.sqlite"):
        raise SqlitePathRefused(text)


def assert_no_lee_ready(mapping):
    if mapping is None:
        return
    if isinstance(mapping, str):
        lowered = mapping.lower().replace("-", "_")
        if "lee_ready" in lowered or "tick_rule" in lowered:
            raise LeeReadyRefused(mapping)
        return
    keys = set(mapping.keys()) if hasattr(mapping, "keys") else set()
    for key in keys:
        token = str(key).lower().replace("-", "_")
        if token in LEE_READY_KEYS or "lee_ready" in token or "tick_rule" in token:
            raise LeeReadyRefused(key)
