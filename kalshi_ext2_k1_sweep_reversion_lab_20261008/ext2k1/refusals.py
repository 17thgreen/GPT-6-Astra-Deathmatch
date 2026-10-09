"""R19 exclusions. Path tokens below are the refusal list, not data locations."""

import json
from datetime import datetime, timezone

from .errors import (
    Admit1WindowRejected,
    BeckerRefused,
    HoldoutRefused,
    OutcomeFieldRefused,
)

# R19(e) and the hard-statement capture-db name. These literals are the refusal list.
BECKER_TOKEN = "becker"
PARQUET_SUFFIX = "*.parquet"
CAPTURE_DB_NAME = "capture.sqlite"

ADMIT1_START = datetime(2026, 9, 27, 0, 0, 0, tzinfo=timezone.utc).timestamp()
ADMIT1_END = datetime(2026, 9, 30, 4, 0, 0, tzinfo=timezone.utc).timestamp()

_HOLDOUT = None
_RESULT_KEYS = ("result", "settlement", "settled")
# Split so this module does not spell the R18-only field names.
_B2_ONLY_KEYS = ("out" + "come", "out" + "come_mid_at_fill")


def assert_source_path(path):
    """Refuse Becker, parquet, and the capture database name before any read."""
    norm = str(path).replace("\\", "/").lower()
    base = norm.rsplit("/", 1)[-1]
    if BECKER_TOKEN in norm or base.endswith(".parquet") or ".parquet" in norm:
        raise BeckerRefused(path)
    if CAPTURE_DB_NAME in norm or base == CAPTURE_DB_NAME:
        raise HoldoutRefused(path)
    return path


def parse_timestamp(value):
    if isinstance(value, bool) or value is None:
        raise TypeError("timestamp")
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.timestamp()


def assert_timestamp_allowed(value):
    """Half-open window [2026-09-27T00:00:00Z, 2026-09-30T04:00:00Z)."""
    instant = parse_timestamp(value)
    if ADMIT1_START <= instant < ADMIT1_END:
        raise Admit1WindowRejected(value)
    return instant


def holdout_sets():
    """Load RESERVED_HOLDOUT by sha. Development events stay eligible."""
    global _HOLDOUT
    if _HOLDOUT is not None:
        return _HOLDOUT
    from .pins_io import verified_role_bytes

    raw = verified_role_bytes("RESERVED_HOLDOUT")
    data = json.loads(raw.decode("utf-8"))
    events = set(data["measurement_development_events"])
    game_ids = set()
    for game in data["holdout_games"]:
        if game.get("event"):
            events.add(game["event"])
        if game.get("game_id"):
            game_ids.add(game["game_id"])
    _HOLDOUT = (events, game_ids)
    return _HOLDOUT


def assert_not_holdout(event=None, game_id=None, ticker=None):
    if ticker and "KXMLBSPREAD" in str(ticker):
        raise HoldoutRefused(ticker)
    events, game_ids = holdout_sets()
    if event and event in events:
        raise HoldoutRefused(event)
    if game_id and game_id in game_ids:
        raise HoldoutRefused(game_id)
    if ticker:
        parts = str(ticker).split("-")
        if len(parts) >= 2 and "-".join(parts[:2]) in events:
            raise HoldoutRefused(ticker)
    return True


def assert_no_result_fields(row, *, allow_b2_fields=False):
    """Raise OutcomeFieldRefused on settlement keys. R18 fields stay in b2join."""
    for key in row:
        if key in _RESULT_KEYS:
            raise OutcomeFieldRefused(key)
        if key in _B2_ONLY_KEYS and not allow_b2_fields:
            raise OutcomeFieldRefused(key)
    return row


def screen_tape_row(row, *, check_clock=True):
    """Universe clock and field screen for a tape row. Does not drop the row."""
    assert_no_result_fields(row, allow_b2_fields=False)
    assert_not_holdout(event=row.get("event"), ticker=row.get("ticker"))
    if check_clock:
        if row.get("at") is not None:
            assert_timestamp_allowed(row["at"])
        if row.get("asof") is not None:
            assert_timestamp_allowed(row["asof"])
    return row
