"""Runtime loader for an astra.fee_source.v1 document.

The adopted file is read from a path. It is not vendored. The taker formula
lives only in pinned_taker_fee. A series that is not PINNED is blocked, with
no default multiplier.
"""
from __future__ import annotations

import json
import re
from decimal import Decimal, ROUND_CEILING

from card01_amc.pinload import sha256_bytes

FEE_SOURCE_ID = "FEE_SOURCE_CARD01_v1"
FEE_SOURCE_SHA256 = "d4dc8e72ae2b2a72824487eb386d6684c451a5e3b2e9dce58c1a68aaea9436cd"
CONDUCTOR_ACCEPT_SHA256 = "5b2eb82613d74bbfb2dd937efa43e239083367f832430a46d011759ccf451b59"
SERIES_C6 = (
    "KXHOUSERACE",
    "HOUSEAZ1",
    "HOUSEAZ2",
    "HOUSEAZ6",
    "HOUSECA22",
    "HOUSECO3",
    "HOUSECO8",
    "HOUSEFL13",
    "HOUSEIA3",
    "HOUSEME2",
    "HOUSEMI4",
    "HOUSEMI7",
    "HOUSEPARTY-MI07",
    "HOUSEMI10",
    "HOUSEMT1",
    "HOUSENC1",
    "KXHOUSENC11",
    "HOUSENE2",
    "HOUSENH1",
    "HOUSENJ7",
    "HOUSENY17",
    "HOUSEOH9",
    "HOUSEPA1",
    "HOUSEPA7",
    "HOUSEPA8",
    "HOUSEPA10",
    "KXHOUSETX9",
    "HOUSETX15",
    "KXHOUSETX32",
    "HOUSETX34",
    "KXHOUSETX35",
    "HOUSEVA1",
    "HOUSEVA2",
    "HOUSEWA3",
    "HOUSEWI1",
    "HOUSEWI3",
)
_ADMISSION = re.compile(r"^ADMITTED_BY_RULING [0-9a-f]{64}$")


class FeeBlocked(Exception):
    def __init__(self, reason, blocked_series=None):
        super().__init__(reason)
        self.reason = reason
        self.blocked_series = list(blocked_series or [])


class FeeSource:
    def __init__(self, doc, digest):
        self.doc = doc
        self.sha256 = digest
        self.manifest_id = doc["manifest_id"]
        self.conductor_accept_sha256 = doc["conductor_accept_sha256"]


class PinnedEntry:
    __slots__ = (
        "series",
        "fee_type",
        "fee_multiplier",
        "fee_multiplier_str",
        "fee_source",
        "fee_source_sha256",
        "taker_rate",
    )

    def __init__(self, series, fee_type, fee_multiplier, fee_multiplier_str, fee_source, fee_source_sha256, taker_rate):
        self.series = series
        self.fee_type = fee_type
        self.fee_multiplier = fee_multiplier
        self.fee_multiplier_str = fee_multiplier_str
        self.fee_source = fee_source
        self.fee_source_sha256 = fee_source_sha256
        self.taker_rate = taker_rate


def load_fee_source(
    path_bytes,
    *,
    expected_sha256=FEE_SOURCE_SHA256,
    expected_id=FEE_SOURCE_ID,
    expected_accept=CONDUCTOR_ACCEPT_SHA256,
):
    """Validate file bytes. Tests may override the three expectations. The CLI does not."""
    if not isinstance(path_bytes, (bytes, bytearray)):
        raise FeeBlocked("FEE_SOURCE_SCHEMA_INVALID")
    digest = sha256_bytes(bytes(path_bytes))
    if digest != expected_sha256:
        raise FeeBlocked("FEE_SOURCE_SHA_MISMATCH")
    try:
        doc = json.loads(bytes(path_bytes))
    except json.JSONDecodeError:
        raise FeeBlocked("FEE_SOURCE_SCHEMA_INVALID") from None
    if not isinstance(doc, dict):
        raise FeeBlocked("FEE_SOURCE_SCHEMA_INVALID")
    template = doc.get("template")
    if isinstance(template, dict) and template.get("is_template") is True:
        raise FeeBlocked("FEE_SOURCE_IS_TEMPLATE")
    series = doc.get("series")
    if (
        doc.get("schema") != "astra.fee_source.v1"
        or not isinstance(template, dict)
        or template.get("is_template") is not False
        or not isinstance(series, dict)
    ):
        raise FeeBlocked("FEE_SOURCE_SCHEMA_INVALID")
    if doc.get("manifest_id") != expected_id:
        raise FeeBlocked("FEE_SOURCE_ID_MISMATCH")
    if doc.get("status") != "ADOPTED":
        raise FeeBlocked("FEE_SOURCE_NOT_ADOPTED")
    if doc.get("conductor_accept_sha256") != expected_accept:
        raise FeeBlocked("CONDUCTOR_ACCEPT_MISMATCH")
    if doc.get("archivist_anchor_sha256") is not None:
        raise FeeBlocked("ARCHIVIST_ANCHOR_IN_FILE")
    if set(series) != set(SERIES_C6):
        raise FeeBlocked("SERIES_SET_MISMATCH")
    return FeeSource(doc, digest)


def _multiplier(value):
    if not isinstance(value, str) or value == "":
        raise FeeBlocked("FEE_TERMS_INVALID")
    try:
        parsed = Decimal(value)
    except Exception:
        raise FeeBlocked("FEE_TERMS_INVALID") from None
    if not parsed.is_finite() or parsed <= 0:
        raise FeeBlocked("FEE_TERMS_INVALID")
    return parsed


def pinned_entry(doc_info, series):
    """Return a PinnedEntry or raise FeeBlocked. No sibling series is consulted."""
    if not isinstance(doc_info, FeeSource):
        raise FeeBlocked("FEE_SOURCE_SCHEMA_INVALID")
    table = doc_info.doc.get("series")
    entry = table.get(series) if isinstance(table, dict) else None
    if not isinstance(entry, dict) or entry.get("ticker") != series:
        raise FeeBlocked("SERIES_ENTRY_MISSING", [series])
    if entry.get("series_status") != "PINNED" or entry.get("blocked_reason") is not None:
        raise FeeBlocked("SERIES_NOT_PINNED", [series])
    endpoint = entry.get("series_endpoint_source")
    if not isinstance(endpoint, dict):
        raise FeeBlocked("SERIES_ENDPOINT_NOT_ADMITTED", [series])
    admission = endpoint.get("admission")
    if not isinstance(admission, str) or _ADMISSION.fullmatch(admission) is None:
        raise FeeBlocked("SERIES_ENDPOINT_NOT_ADMITTED", [series])
    schedule = entry.get("schedule_source")
    if not isinstance(schedule, dict) or schedule.get("evidence_tag") != "[V]" or endpoint.get("evidence_tag") != "[V]":
        raise FeeBlocked("EVIDENCE_NOT_V", [series])
    if endpoint.get("fee_type") != entry.get("fee_type") or endpoint.get("fee_multiplier") != entry.get("fee_multiplier"):
        raise FeeBlocked("FEE_SOURCE_CONFLICT", [series])
    if entry.get("maker_taker_class") not in ("TAKER", "BOTH"):
        raise FeeBlocked("TAKER_NOT_COVERED", [series])
    if entry.get("rounding_rule") != "PER_ORDER_CEIL_CENT":
        raise FeeBlocked("ROUNDING_RULE_UNSUPPORTED", [series])
    if entry.get("fee_type") != "quadratic":
        raise FeeBlocked("FEE_TYPE_UNSUPPORTED", [series])
    multiplier = _multiplier(entry.get("fee_multiplier"))
    taker_rate = entry.get("taker_rate")
    if not isinstance(taker_rate, str):
        raise FeeBlocked("TAKER_RATE_MISMATCH", [series])
    pinned = PinnedEntry(
        series=series,
        fee_type=entry["fee_type"],
        fee_multiplier=multiplier,
        fee_multiplier_str=entry["fee_multiplier"],
        fee_source=doc_info.manifest_id,
        fee_source_sha256=doc_info.sha256,
        taker_rate=taker_rate,
    )
    try:
        pinned_taker_fee(pinned, Decimal("0.50"))
    except FeeBlocked as exc:
        if exc.reason == "TAKER_RATE_MISMATCH":
            raise FeeBlocked("TAKER_RATE_MISMATCH", [series]) from None
        raise
    return pinned


def pinned_taker_fee(entry, price, contracts=1):
    """Headline non-direct cent fee, plus sensitivity rows.

    Headline is ceil_cent(P*C + fee_raw) - P*C. FEE_ONLY_CEIL is
    ceil_cent(fee_raw) and is not the headline. The rate literal is
    intentionally confined to this function.
    """
    if type(entry) is not PinnedEntry:
        raise TypeError("pinned_taker_fee requires a PinnedEntry")
    rate = Decimal("0.07")
    try:
        quoted = Decimal(entry.taker_rate)
    except Exception:
        raise FeeBlocked("TAKER_RATE_MISMATCH") from None
    if quoted != rate:
        raise FeeBlocked("TAKER_RATE_MISMATCH")

    def ceil_to(value, quantum):
        return (value / quantum).to_integral_value(ROUND_CEILING) * quantum

    try:
        observed = Decimal(str(price))
    except Exception:
        raise FeeBlocked("PRICE_NOT_ON_GRID") from None
    if not observed.is_finite():
        raise FeeBlocked("PRICE_NOT_ON_GRID")
    grid = observed.quantize(Decimal("0.0001"))
    if abs(grid - observed) > Decimal("1e-9"):
        raise FeeBlocked("PRICE_NOT_ON_GRID")
    if not (Decimal(0) < grid < Decimal(1)):
        raise FeeBlocked("PRICE_NOT_ON_GRID")
    try:
        count = Decimal(contracts)
    except Exception:
        raise FeeBlocked("FEE_TERMS_INVALID") from None
    if count != 1:
        raise FeeBlocked("FEE_TERMS_INVALID")
    def trim(value):
        text = format(value, "f")
        if "." in text:
            text = text.rstrip("0").rstrip(".")
        return Decimal(text or "0")

    raw = ceil_to(entry.fee_multiplier * rate * count * grid * (1 - grid), Decimal("0.000001"))
    headline = trim(ceil_to(grid * count + raw, Decimal("0.01")) - grid * count)
    fee_only_ceil = trim(ceil_to(raw, Decimal("0.01")))
    sensitivity_direct = trim(ceil_to(grid * count + raw, Decimal("0.0001")) - grid * count)
    raw = trim(raw)
    return {
        "headline": headline,
        "FEE_ONLY_CEIL": fee_only_ceil,
        "sensitivity_direct_member": sensitivity_direct,
        "raw": raw,
    }
