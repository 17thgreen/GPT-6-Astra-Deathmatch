"""Closed-failure exceptions for the EXT-K1 measurement lab."""


class ClosedUniverseRefused(Exception):
    """Ticker or event is outside the 31-event cohort."""


class JoinRefused(Exception):
    """nflverse join is not exactly one candidate for every cohort event."""


class Admit1WindowRejected(Exception):
    """Timestamp falls inside the half-open ADMIT-1 window."""


class HoldoutRefused(Exception):
    """Row identifies a reserved holdout, measurement-development event, or KXMLBSPREAD ticker."""


class SqlitePathRefused(Exception):
    """capture.sqlite and the weather archive.sqlite are never opened."""


class LookaheadRefused(Exception):
    """The refusal gate accepts no tape, score, or markout argument."""


class LeeReadyRefused(Exception):
    """Lee-Ready classification is refused. taker_side is native."""


class ManifestMismatch(Exception):
    """A vendored pin does not match MANIFEST.sha256."""


class StructureDrift(Exception):
    """Ledger structure does not match the frozen replay accounting."""


class FeeScheduleError(Exception):
    """KXNFLGAME maker multiplier could not be read as 1 from the cached schedule."""
