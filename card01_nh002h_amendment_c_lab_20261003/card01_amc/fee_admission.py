"""Index-only admission for an astra.fee_source.v2 document.

The fee file, the packet index, and the fill ACCEPT are runtime inputs.
This module records rule pins. The only fee-source identity it hard-codes
is the v1 refuse list.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from card01_amc.fee_source import FeeBlocked, PinnedEntry
from card01_amc.pinload import sha256_bytes

FEE_FORMULA_ID = "astra.card01.fee_eff.non_direct_buy_ceil_cent.v1"
HEADLINE_EXPRESSION = "ceil_cent(P*C + fee_raw) - P*C"
HEADLINE_APPLIES_TO = {
    "side": "BUY",
    "taker_maker_role": "TAKER",
    "member_class_assumption": "NON_DIRECT",
    "fill_model": "SINGLE_FILL",
    "fee_type": "quadratic",
}
FEE_ADMISSION_RULE_SHA256 = "2c870cd57fc4acb4290c1273e06876e8380159f2f6614a5519314b43817a8583"
FEE_ATTESTATION_SHA256 = "b59e416873bd00c7c27572eb5eab10bb4d4a078b515465d94ea6e37efb3db84f"
FEE_ATTESTATION_RESULT = "ATTEST_PASS"
FEE_ATTESTATION_SCOPE = "HEADLINE_FEE_SOURCE_ONLY"
SENSITIVITY_ROWS_STATUS = "SENSITIVITY_BASIS_INCOMPLETE"
ATTESTED_AT_UTC = "2026-10-08T23:32:51Z"
EXAMINER_NAME = "Examiner KALSHI"

REFUSED_FEE_SOURCES = frozenset({
    "d4dc8e72ae2b2a72824487eb386d6684c451a5e3b2e9dce58c1a68aaea9436cd",
    "FEE_SOURCE_CARD01_v1",
})

_ROW_RE = re.compile(r"^\|\s*`([^`]+)`\s*(.*)\|\s*`([0-9a-f]{64})`\s*\|\s*$", re.M)
_ADOPTED_RE = re.compile(r"(?<!NOT )ADOPTED \(anchor\) by (?:Conductor )?ACCEPT ([0-9a-f]{8,64})")
_BLOCK_RE = re.compile(r"\b(?:withdrawn|withdraw|revoked|not adopted|not admitted)\b")
_SUPERSEDED_RE = re.compile(r"\bsuperseded\b(?! by\b)")
_BOLD_STATUS_RE = re.compile(
    r"\*\*\s*(?:withdrawn|withdraw|revoked|superseded|not\s+adopted|not\s+admitted)\s*\*\*",
    re.IGNORECASE,
)
_HEX_TOKEN_RE = re.compile(r"[0-9a-f]{8,64}")
_RULING_RE = re.compile(r"accept(?:_[a-z0-9]+)*\Z")
_RULING_STATUS_TOKENS = frozenset({
    "withdrawn",
    "withdraw",
    "revoked",
    "superseded",
    "adopted",
    "admitted",
})
_ADMISSION_RE = re.compile(r"^ADMITTED_BY_RULING [0-9a-f]{64}$")


@dataclass(frozen=True)
class FeeAdmission:
    fee_admission: str
    fee_block_reason: str | None = None
    fee_block_detail: str | None = None
    amendment_check_failed: str | None = None
    adoption_mode: str | None = None
    fee_source: str | None = None
    fee_source_sha256: str | None = None
    fee_formula_id: str | None = None
    fee_source_accept_sha256: str | None = None
    packet_index_sha256_at_run: str | None = None
    fee_admission_rule_sha256: str = FEE_ADMISSION_RULE_SHA256
    fee_attestation_sha256: str = FEE_ATTESTATION_SHA256
    fee_attestation_result: str = FEE_ATTESTATION_RESULT
    fee_attestation_scope: str = FEE_ATTESTATION_SCOPE
    sensitivity_rows_status: str = SENSITIVITY_ROWS_STATUS
    series_used: tuple = ()
    blocked_series: tuple = ()
    fee_source_attestation: dict | None = None
    series_table_json: str | None = None

    @property
    def admitted(self) -> bool:
        return self.fee_admission == "ADMITTED_INDEX_ONLY"

    def public_dict(self) -> dict:
        """Provenance recorded on an admitted or blocked gate. No fee-file body."""
        return {
            "fee_admission": self.fee_admission,
            "adoption_mode": self.adoption_mode,
            "fee_source": self.fee_source,
            "fee_source_sha256": self.fee_source_sha256,
            "fee_formula_id": self.fee_formula_id,
            "fee_block_reason": self.fee_block_reason,
            "fee_block_detail": self.fee_block_detail,
            "amendment_check_failed": self.amendment_check_failed,
            "blocked_series": list(self.blocked_series),
            "fee_source_accept_sha256": self.fee_source_accept_sha256,
            "packet_index_sha256_at_run": self.packet_index_sha256_at_run,
            "fee_admission_rule_sha256": self.fee_admission_rule_sha256,
            "fee_attestation_sha256": self.fee_attestation_sha256,
            "fee_attestation_result": self.fee_attestation_result,
            "fee_attestation_scope": self.fee_attestation_scope,
            "sensitivity_rows_status": self.sensitivity_rows_status,
            "series_used": [dict(item) for item in self.series_used],
            "fee_source_attestation": self.fee_source_attestation,
        }


def _blocked(reason, check, detail=None, **kwargs):
    return FeeAdmission(
        fee_admission="BLOCKED_FEE_UNVERIFIED",
        fee_block_reason=reason,
        fee_block_detail=detail,
        amendment_check_failed=check,
        sensitivity_rows_status=SENSITIVITY_ROWS_STATUS,
        fee_admission_rule_sha256=FEE_ADMISSION_RULE_SHA256,
        fee_attestation_sha256=FEE_ATTESTATION_SHA256,
        fee_attestation_result=FEE_ATTESTATION_RESULT,
        fee_attestation_scope=FEE_ATTESTATION_SCOPE,
        **kwargs,
    )


def _read(path):
    if path is None or path == "":
        return None, "absent"
    try:
        return Path(path).read_bytes(), None
    except OSError:
        return None, "unreadable"


def _index_rows(text):
    rows = []
    for match in _ROW_RE.finditer(text):
        rows.append({
            "path": match.group(1),
            "description": match.group(2),
            "sha256": match.group(3),
        })
    return rows


def _normalize_status(text):
    return re.sub(r"\s+", " ", text).strip().casefold()


def _status_blocks(text):
    """True when a status word is an exact token after case and whitespace folding.

    Underscore stays inside a token, so DRAFT_NOT_ADOPTED and
    SUPERSEDED_CHECKER_BUG do not match. A narrative "superseded by <later
    record>" names a successor and is not a withdrawal of this row. A bold
    status word still blocks, including **SUPERSEDED** by a later sha.
    """
    if not isinstance(text, str) or text == "":
        return False
    if _BOLD_STATUS_RE.search(text):
        return True
    folded = _normalize_status(text)
    if _BLOCK_RE.search(folded):
        return True
    return _SUPERSEDED_RE.search(folded) is not None


def _mentions_sha(row, sha):
    """True when the row is keyed by sha, or its path or text cites sha."""
    if not isinstance(sha, str) or len(sha) != 64:
        return False
    if row["sha256"] == sha:
        return True
    blob = (row["path"] + " " + row["description"]).casefold()
    target = sha.casefold()
    if target in blob:
        return True
    return any(target.startswith(token) for token in _HEX_TOKEN_RE.findall(blob))


def _ruling_is_accept(ruling):
    """True for the exact token ACCEPT, or ACCEPT plus non-status underscore tokens.

    ACCEPT_THEN_WITHDRAWN is refused. A prefix such as ACCEPTED is refused.
    """
    if not isinstance(ruling, str):
        return False
    folded = _normalize_status(ruling)
    if _RULING_RE.fullmatch(folded) is None:
        return False
    tokens = folded.split("_")
    if tokens[0] != "accept":
        return False
    if any(token in _RULING_STATUS_TOKENS for token in tokens):
        return False
    if "not" in tokens:
        return False
    return True


def _series_list(names):
    return tuple({"series": name, "series_status": "PINNED"} for name in names)


def admit_fee_source_v2(
    *,
    fee_source_path,
    fee_source_id,
    fee_source_sha256,
    packet_index_path,
    fee_accept_path,
    series_used,
    side="BUY",
    taker_maker_role="TAKER",
    member_class_assumption="NON_DIRECT",
    fill_model="SINGLE_FILL",
):
    """Admit a v2 fee source under amendment 2c870cd5. First failure wins."""
    identity = {
        "fee_source": fee_source_id if isinstance(fee_source_id, str) else None,
        "fee_source_sha256": fee_source_sha256 if isinstance(fee_source_sha256, str) else None,
    }
    if fee_source_sha256 in REFUSED_FEE_SOURCES or fee_source_id in REFUSED_FEE_SOURCES:
        return _blocked("FEE_SOURCE_NOT_ADMITTED_V1_ATTEST_FAIL", None, **identity)

    fee_bytes, fee_err = _read(fee_source_path)
    if fee_err is not None:
        return _blocked("FEE_SOURCE_UNREADABLE", "a", fee_err, **identity)
    index_bytes, index_err = _read(packet_index_path)
    if index_err is not None:
        return _blocked("FEE_SOURCE_PAIR_MISSING", "a", "packet_index_path", **identity)
    if fee_accept_path is None or fee_accept_path == "":
        return _blocked("FEE_SOURCE_PAIR_MISSING", "b", "fee_accept_path", **identity)
    accept_bytes, accept_err = _read(fee_accept_path)
    if accept_err is not None:
        return _blocked("FEE_ACCEPT_MISSING", "b", "fee_accept_path", **identity)

    digest = sha256_bytes(fee_bytes)
    index_sha = sha256_bytes(index_bytes)
    identity["packet_index_sha256_at_run"] = index_sha
    if digest != fee_source_sha256:
        identity["fee_source_sha256"] = fee_source_sha256
        return _blocked("FEE_SOURCE_REHASH_MISMATCH", "a", **identity)

    try:
        fee_text = fee_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return _blocked("FEE_SOURCE_UNREADABLE", "a", "non_utf8", **identity)
    try:
        doc = json.loads(fee_text)
    except json.JSONDecodeError:
        return _blocked("FEE_SOURCE_IN_FILE_UNEXPECTED", "c", "UNPARSEABLE", **identity)
    if not isinstance(doc, dict):
        return _blocked("FEE_SOURCE_IN_FILE_UNEXPECTED", "c", "UNPARSEABLE", **identity)

    rows = _index_rows(index_bytes.decode("utf-8", "replace"))
    anchored = [row for row in rows if row["sha256"] == fee_source_sha256]
    if not anchored:
        return _blocked("FEE_SOURCE_NOT_ANCHORED", "a", **identity)

    if doc.get("manifest_id") != fee_source_id:
        return _blocked("FEE_SOURCE_REHASH_MISMATCH", "a", "MANIFEST_ID_MISMATCH", **identity)

    if any(_status_blocks(row["description"]) for row in anchored):
        return _blocked("FEE_SOURCE_STATUS_NOT_ADOPTED", "b", "REVOKED_ROW", **identity)

    adopted = []
    for row in anchored:
        match = _ADOPTED_RE.search(row["description"])
        if match is not None:
            adopted.append((row, match.group(1)))
    if not adopted:
        return _blocked("FEE_SOURCE_STATUS_NOT_ADOPTED", "b", **identity)

    prefixes = []
    for _row, prefix in adopted:
        if prefix not in prefixes:
            prefixes.append(prefix)
    cited_shas = set()
    for row in rows:
        if "CONDUCTOR_ACCEPT" not in row["path"]:
            continue
        if any(row["sha256"].startswith(prefix) for prefix in prefixes):
            cited_shas.add(row["sha256"])
    if len(cited_shas) == 0:
        return _blocked("FEE_ACCEPT_MISSING", "b", **identity)
    if len(cited_shas) > 1:
        return _blocked("FEE_ACCEPT_REHASH_MISMATCH", "b", **identity)
    accept_sha = next(iter(cited_shas))
    identity["fee_source_accept_sha256"] = accept_sha
    watched = (accept_sha, FEE_ATTESTATION_SHA256)
    if any(
        _status_blocks(row["description"]) and any(_mentions_sha(row, sha) for sha in watched)
        for row in rows
    ):
        return _blocked("FEE_SOURCE_STATUS_NOT_ADOPTED", "b", "REVOKED_ROW", **identity)
    if sha256_bytes(accept_bytes) != accept_sha:
        return _blocked("FEE_ACCEPT_REHASH_MISMATCH", "b", **identity)
    try:
        accept_doc = json.loads(accept_bytes)
    except json.JSONDecodeError:
        return _blocked("FEE_ACCEPT_REHASH_MISMATCH", "b", **identity)
    ruling = accept_doc.get("ruling") if isinstance(accept_doc, dict) else None
    if not _ruling_is_accept(ruling):
        return _blocked("FEE_ACCEPT_REHASH_MISMATCH", "b", "NOT_AN_ACCEPT", **identity)
    accepted = accept_doc.get("accepted") if isinstance(accept_doc, dict) else None
    fill_sha = accepted.get("fill_sha256") if isinstance(accepted, dict) else None
    if fill_sha != fee_source_sha256:
        return _blocked("FEE_ACCEPT_REHASH_MISMATCH", "b", **identity)

    template = doc.get("template")
    in_file_ok = (
        doc.get("status") == "DRAFT_NOT_ADOPTED"
        and doc.get("conductor_accept_sha256") is None
        and doc.get("archivist_anchor_sha256") is None
        and doc.get("schema") == "astra.fee_source.v2"
        and isinstance(template, dict)
        and template.get("is_template") is False
    )
    if not in_file_ok:
        return _blocked("FEE_SOURCE_IN_FILE_UNEXPECTED", "c", **identity)

    headline = {}
    computation = doc.get("fee_computation")
    if isinstance(computation, dict) and isinstance(computation.get("headline"), dict):
        headline = computation["headline"]
    if (
        headline.get("role") != "HEADLINE_FEE_SOURCE"
        or headline.get("formula_id") != FEE_FORMULA_ID
        or headline.get("expression") != HEADLINE_EXPRESSION
    ):
        return _blocked("FEE_FORMULA_ID_MISMATCH", None, **identity)

    if headline.get("applies_to") != HEADLINE_APPLIES_TO:
        return _blocked("HEADLINE_SCOPE_MISMATCH", "d", **identity)

    table = doc.get("series")
    if not isinstance(table, dict):
        table = {}
    names = list(series_used or [])
    blocked_series = []
    for name in names:
        entry = table.get(name) if isinstance(name, str) else None
        if (
            not isinstance(entry, dict)
            or entry.get("series_status") != "PINNED"
            or entry.get("blocked_reason") is not None
        ):
            blocked_series.append(name)
    if blocked_series:
        detail = json.dumps(blocked_series)
        return _blocked(
            "SERIES_NOT_PINNED",
            "d",
            detail,
            blocked_series=tuple(blocked_series),
            **identity,
        )

    for name in names:
        entry = table[name]
        endpoint = entry.get("series_endpoint_source")
        admission = endpoint.get("admission") if isinstance(endpoint, dict) else None
        scope_ok = (
            entry.get("fee_type") == "quadratic"
            and entry.get("maker_taker_class") in ("TAKER", "BOTH")
            and isinstance(endpoint, dict)
            and isinstance(admission, str)
            and _ADMISSION_RE.fullmatch(admission) is not None
            and endpoint.get("fee_type") == entry.get("fee_type")
            and endpoint.get("fee_multiplier") == entry.get("fee_multiplier")
        )
        if not scope_ok:
            return _blocked("HEADLINE_SCOPE_MISMATCH", "d", **identity)
        raw_mult = entry.get("fee_multiplier")
        try:
            parsed = Decimal(raw_mult) if isinstance(raw_mult, str) else None
        except Exception:
            parsed = None
        if parsed is None or parsed != Decimal("1"):
            return _blocked("HEADLINE_SCOPE_MISMATCH", "d", "FEE_MULTIPLIER_NOT_1", **identity)

    trade_ok = (
        side == "BUY"
        and taker_maker_role == "TAKER"
        and member_class_assumption == "NON_DIRECT"
        and fill_model == "SINGLE_FILL"
    )
    if not trade_ok:
        return _blocked("HEADLINE_SCOPE_MISMATCH", "d", **identity)

    used = _series_list(names)
    attestation = {
        "rehash_ok": True,
        "packet_index_anchor_ok": True,
        "status": "ADOPTED (PACKET_INDEX, index-only); in-file DRAFT_NOT_ADOPTED",
        "conductor_accept_sha256": accept_sha,
        "fee_formula_id": FEE_FORMULA_ID,
        "headline_expression": HEADLINE_EXPRESSION,
        "series": [dict(item) for item in used],
        "examiner": EXAMINER_NAME,
        "attested_at_utc": ATTESTED_AT_UTC,
        "fee_source": fee_source_id,
        "fee_source_sha256": fee_source_sha256,
    }
    return FeeAdmission(
        fee_admission="ADMITTED_INDEX_ONLY",
        adoption_mode="INDEX_ONLY",
        fee_source=fee_source_id,
        fee_source_sha256=fee_source_sha256,
        fee_formula_id=FEE_FORMULA_ID,
        fee_source_accept_sha256=accept_sha,
        packet_index_sha256_at_run=index_sha,
        series_used=used,
        fee_source_attestation=attestation,
        series_table_json=json.dumps({name: table[name] for name in names}, sort_keys=True),
    )


def pinned_entry_v2(admission, series):
    """Build a PinnedEntry only from an admitted headline series."""
    if not isinstance(admission, FeeAdmission) or not admission.admitted:
        raise FeeBlocked("BLOCKED_FEE_UNVERIFIED")
    if not admission.series_table_json:
        raise FeeBlocked("SERIES_NOT_PINNED", [series])
    table = json.loads(admission.series_table_json)
    entry = table.get(series)
    if not isinstance(entry, dict):
        raise FeeBlocked("SERIES_NOT_PINNED", [series])
    multiplier = Decimal(entry["fee_multiplier"])
    taker_rate = entry.get("taker_rate")
    if not isinstance(taker_rate, str):
        raise FeeBlocked("TAKER_RATE_MISMATCH", [series])
    return PinnedEntry(
        series=series,
        fee_type=entry["fee_type"],
        fee_multiplier=multiplier,
        fee_multiplier_str=entry["fee_multiplier"],
        fee_source=admission.fee_source,
        fee_source_sha256=admission.fee_source_sha256,
        taker_rate=taker_rate,
    )
