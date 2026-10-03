"""Path and column guards for the Becker pipeline."""

import re

from shared.exceptions import (
    BeckerMixRefused,
    BeckerQuoteFieldRefused,
    TierRefused,
)
from shared.refusals import assert_sqlite_path_refused

REFUSED_MARKET_FIELDS = frozenset({
    "yes_bid", "yes_ask", "no_bid", "no_ask", "last_price", "open_interest", "volume_24h",
})

_TIER = re.compile(r"_t[1-4](?:_|\.)")


def refuse_tier_path(path):
    text = str(path).replace("\\", "/")
    if _TIER.search(text):
        raise TierRefused(text)


def read_market_field(row, field):
    if field in REFUSED_MARKET_FIELDS:
        raise BeckerQuoteFieldRefused(field)
    return row[field]


def refuse_becker_input(path, sha=None, cloud_shas=()):
    text = str(path).replace("\\", "/")
    assert_sqlite_path_refused(text)
    refuse_tier_path(text)
    if "astra-science/" in text or "astra-capture/prospective/" in text:
        raise BeckerMixRefused(text)
    if text.endswith("events.jsonl.gz"):
        raise BeckerMixRefused(text)
    if "EXT_K1_authentic_pins" in text or "EXT_K2_authentic_pins" in text:
        raise BeckerMixRefused(text)
    if sha is not None and sha in cloud_shas:
        raise BeckerMixRefused(sha)
    return text
