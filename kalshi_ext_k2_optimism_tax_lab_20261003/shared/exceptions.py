"""Named refusals. Both pipelines raise these; neither catches them into a score."""


class LabelInputRefused(Exception):
    """Tercile assignment was given a quote, fill, score, result, or other label."""


class BeckerMixRefused(Exception):
    """A dev table and a Becker table were combined, or a path crossed pipelines."""


class CrossCheckKeyRefused(Exception):
    """A cross-provenance comparison used a key other than trade_id."""


class Admit1WindowRejected(Exception):
    """Timestamp falls in [2026-09-27T00:00:00Z, 2026-09-30T04:00:00Z)."""


class HoldoutRefused(Exception):
    """NFL reserved holdout, measurement-development event, or KXMLBSPREAD ticker."""


class SqlitePathRefused(Exception):
    """capture.sqlite or weather archive.sqlite was named."""


class ClosedUniverseRefused(Exception):
    """Event or ticker outside the 31-event dev universe."""


class StructureDrift(Exception):
    """K1 R36 / FIFO identity failed. The run stops."""


class LeeReadyRefused(Exception):
    """Lee-Ready, a tick rule, or a print-derived mid was requested."""


class ManifestTamper(Exception):
    """A pinned sha256 did not match. Nothing is parsed."""


class OpenTickerRefused(Exception):
    """An excluded open or no-result ticker reached a metric."""


class TierRefused(Exception):
    """A Becker t1–t4 path was named. Only t0 is in scope."""


class BeckerQuoteFieldRefused(Exception):
    """A Becker markets quote, depth, or snapshot column was read."""


class RebinRefused(Exception):
    """Price bands were rebinned, merged, split, or given custom edges."""


class RowLevelOutputRefused(Exception):
    """A Becker output carried a row-level key or identifier."""


class LabelDependentToGateRefused(Exception):
    """A Becker label-dependent value was passed into a dev verdict or gate."""


class BoxOnlyRefused(Exception):
    """Part (b) was started off the box, or an output path is inside the repo."""


class ReceiptMismatchRefused(Exception):
    """Pre-run receipt shas did not match the pins. No aggregate is written."""


class InconclusiveNoOutput(Exception):
    """Part (b) stopped INCONCLUSIVE with no aggregate output."""


class IntegrityRefused(Exception):
    """A Becker integrity invariant failed."""
