"""Price bands from registry 0860cbe2, read verbatim. Never rebinned."""

import json
from pathlib import Path

from shared.canonical import sha256_file
from shared.exceptions import RebinRefused

REGISTRY_SHA256 = "0860cbe28d28ecc6142ddf6f1ebb67792084264ed82e0b4d868c3b3138ea5312"


def load_registry(path):
    digest = sha256_file(path)
    if digest != REGISTRY_SHA256:
        raise RebinRefused("band registry sha mismatch: " + digest)
    doc = json.loads(Path(path).read_text(encoding="utf-8"))
    bands = doc["bands"]
    if len(bands) != 10:
        raise RebinRefused("registry does not have 10 bands")
    return doc


def band_id_for_yes_price(yes_cents, registry):
    """Map integer cents 1..99 through the registry edges. No custom edges."""
    if isinstance(yes_cents, bool) or not isinstance(yes_cents, int):
        raise RebinRefused("yes price must be integer cents")
    if yes_cents < 1 or yes_cents > 99:
        raise RebinRefused("yes price outside 1..99")
    price = yes_cents / 100.0
    matched = []
    for band in registry["bands"]:
        lo = band["price_lo"]
        hi = band["price_hi"]
        lo_ok = price >= lo if band["lo_inclusive"] else price > lo
        hi_ok = price <= hi if band["hi_inclusive"] else price < hi
        if lo_ok and hi_ok:
            matched.append(band["band_id"])
    if len(matched) != 1:
        raise RebinRefused("band assignment is not unique")
    return matched[0]


def refuse_custom_edges(edges):
    """Any caller-supplied edge list is a rebin."""
    raise RebinRefused("custom edges are a rebin of 0860cbe2: " + repr(edges))
