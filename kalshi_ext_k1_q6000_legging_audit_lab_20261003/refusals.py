"""ADMIT-1 and holdout refusals. Both paths raise."""

import json
from datetime import datetime, timezone

from constants import HOLDOUT_SHA256, PINS_REL
from errors import Admit1WindowRejected, HoldoutRefused
from pins_io import verified_bytes

ADMIT1_START = datetime(2026, 9, 27, 0, 0, 0, tzinfo=timezone.utc).timestamp()
ADMIT1_END = datetime(2026, 9, 30, 4, 0, 0, tzinfo=timezone.utc).timestamp()

_HOLDOUT = None


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
    """Load the reserved-holdout pin. Development events stay eligible."""
    global _HOLDOUT
    if _HOLDOUT is not None:
        return _HOLDOUT
    raw = verified_bytes(PINS_REL["holdout"])
    # verified_bytes already enforced the manifest hash; keep the prefix visible.
    import hashlib
    digest = hashlib.sha256(raw).hexdigest()
    if digest != HOLDOUT_SHA256:
        raise HoldoutRefused("RESERVED_HOLDOUT hash")
    data = json.loads(raw.decode("utf-8"))
    events = set(data["measurement_development_events"])
    game_ids = set()
    for game in data["holdout_games"]:
        if game.get("event"):
            events.add(game["event"])
        if game.get("game_id"):
            game_ids.add(game["game_id"])
    _HOLDOUT = (events, game_ids, set(data["development_events"]))
    return _HOLDOUT


def assert_not_holdout(event=None, game_id=None, ticker=None):
    if ticker and "KXMLBSPREAD" in str(ticker):
        raise HoldoutRefused(ticker)
    events, game_ids, _development = holdout_sets()
    if event and event in events:
        raise HoldoutRefused(event)
    if game_id and game_id in game_ids:
        raise HoldoutRefused(game_id)
    if ticker:
        parts = str(ticker).split("-")
        if len(parts) >= 2:
            inferred = "-".join(parts[:2])
            if inferred in events:
                raise HoldoutRefused(ticker)
    return True


def screen_clock_row(row):
    """Raise on a holdout identity or an ADMIT-1 timestamp. Does not drop the row."""
    assert_not_holdout(
        event=row.get("event"),
        game_id=row.get("game_id"),
        ticker=row.get("ticker"),
    )
    if "at" in row and row["at"] is not None:
        assert_timestamp_allowed(row["at"])
    if "asof" in row and row["asof"] is not None:
        assert_timestamp_allowed(row["asof"])
    return row
