"""Closed-universe and refusal errors for EXT2-K1."""


class ClosedUniverseRefused(Exception):
    """Ticker or event is outside the pinned cohort universe."""


class SourcePinMismatch(Exception):
    """A closed-manifest pin is missing or its bytes do not match."""


class Admit1WindowRejected(Exception):
    """Timestamp falls inside the half-open ADMIT-1 window."""


class HoldoutRefused(Exception):
    """Holdout game, measurement-development event, or refused series."""


class BeckerRefused(Exception):
    """Named extract or parquet path is outside this freeze."""


class OutcomeFieldRefused(Exception):
    """Settlement or result field is not on the R18 allowlist."""


class FloatDecimalRefused(Exception):
    """Decimal(float) is refused. Fee inputs must be str or Decimal."""


class LeeReadyRefused(Exception):
    """Trade-sign inference from quotes is refused. Mids come from quotes."""
