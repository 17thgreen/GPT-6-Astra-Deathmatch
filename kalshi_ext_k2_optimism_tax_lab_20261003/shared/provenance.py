"""Provenance container. The only cross-provenance operation is a trade_id count."""

from shared.exceptions import BeckerMixRefused, CrossCheckKeyRefused

PROVENANCES = ("DEV_B1B2", "BECKER_A", "SYNTHETIC_NOT_BECKER")


class Provenanced:
    def __init__(self, rows, provenance):
        if provenance not in PROVENANCES:
            raise BeckerMixRefused("unknown provenance " + str(provenance))
        self.rows = list(rows)
        self.provenance = provenance

    def _require_same(self, other, op):
        if not isinstance(other, Provenanced) or other.provenance != self.provenance:
            raise BeckerMixRefused(op)
        return other

    def concat(self, other):
        other = self._require_same(other, "concat")
        return Provenanced(self.rows + other.rows, self.provenance)

    def merge(self, other):
        other = self._require_same(other, "merge")
        return Provenanced(self.rows + other.rows, self.provenance)

    def join(self, other):
        other = self._require_same(other, "join")
        return Provenanced(self.rows + other.rows, self.provenance)

    def zip_with(self, other):
        other = self._require_same(other, "zip")
        return Provenanced(list(zip(self.rows, other.rows)), self.provenance)

    def compare(self, other):
        other = self._require_same(other, "compare")
        return self.rows == other.rows


def cross_check(key, left, right):
    """The only legal cross-provenance key is trade_id. Anything else is refused."""
    if key != "trade_id":
        raise CrossCheckKeyRefused(key)
    return trade_id_overlap_count(left, right)


def trade_id_overlap_count(dev_ids, becker_ids):
    """Return an int. Sets of trade_id strings only."""
    if not isinstance(dev_ids, (set, frozenset)) or not isinstance(becker_ids, (set, frozenset)):
        raise CrossCheckKeyRefused("overlap accepts sets of trade_id strings")
    for group in (dev_ids, becker_ids):
        for item in group:
            if not isinstance(item, str):
                raise CrossCheckKeyRefused("overlap key must be a trade_id string")
    return len(dev_ids & becker_ids)
