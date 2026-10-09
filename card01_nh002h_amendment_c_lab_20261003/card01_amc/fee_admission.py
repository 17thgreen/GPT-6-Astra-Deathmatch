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
_ADMISSION_RE = re.compile(r"^ADMITTED_BY_RULING [0-9a-f]{64}$")
_CITATION_PATH = Path(__file__).with_name("fee_citation_set.json")
# sha256 of fee_citation_set.json. A byte change with this constant left
# unchanged makes the pin unusable (ADV-10). There is no override.
FEE_CITATION_SET_SHA256 = "3a56ead8151967f704ce6e344f3c61f18bc660e3f37e45dbb269dd3123905149"
_ZERO_WIDTH = str.maketrans("", "", "\u200b\u200c\u200d\u2060\ufeff")


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


# The fee citation multiset does not include 69b98b2f. That packet has its
# own pinned line set, checked before this word rule. The word rule is
# defence in depth: a status blocks only when 69b98b2f is the subject.
_R1_ACCEPT_PREFIX7 = "69b98b2"
_R1_STATUS = (
    r"(?:withdrawn|withdrawal|withdraws|withdraw|revoked|revocation|revokes|revoke|"
    r"rescinded|rescission|rescinds|rescind|superseded|supersedes|supersede|"
    r"retracted|vacated|void|no longer adopted|not adopted|not admitted)"
)
_R1_STATUS_RE = re.compile(r"\b" + _R1_STATUS + r"\b")
_R1_BY_FORM = r"(?:withdrawn_by|revoked_by|rescinded_by|superseded_by)"
_R1_OBJECT_AFTER_RE = re.compile(
    _R1_ACCEPT_PREFIX7 + r"[0-9a-f]*\b\s+(?:" + _R1_BY_FORM + r"|" + _R1_STATUS + r")\b"
)
_R1_OBJECT_OF_RE = re.compile(r"\b" + _R1_STATUS + r"\s+of\s+" + _R1_ACCEPT_PREFIX7)
_R1_OBJECT_BEFORE_RE = re.compile(r"\b" + _R1_STATUS + r"\s+" + _R1_ACCEPT_PREFIX7)
_R1_NEGATED_RE = re.compile(
    r"\bnot\s+(?:withdrawn|withdrawal|withdraws|withdraw|revoked|revocation|revokes|revoke|"
    r"rescinded|rescission|rescinds|rescind|superseded|supersedes|supersede|"
    r"retracted|vacated|void)\b"
)
_R1_ACTOR_RE = re.compile(
    r"\b(?:accepted(?:\s+as\s+modified)?\s+by\s+" + _R1_ACCEPT_PREFIX7 + r"[0-9a-f]*"
    r"|(?:superseded|withdrawn|revoked|rescinded)_by\s+" + _R1_ACCEPT_PREFIX7 + r"[0-9a-f]*"
    r"|(?:superseded|withdrawn|revoked|rescinded)\s+by\s+" + _R1_ACCEPT_PREFIX7 + r"[0-9a-f]*)\b"
)
_R1_OTHER_LABEL_RE = re.compile(
    r"\br\d+(?:\s*/\s*r\d+)+\s+" + _R1_STATUS + r"\b"
)
_R1_OTHER_HEX_RE = re.compile(
    r"\b([0-9a-f]{8,64})\s+(" + _R1_STATUS + r")\b"
)
_R1_PACKET_ACTIONS = frozenset({
    "withdraw",
    "withdrawal",
    "withdrawn",
    "withdraws",
    "revoke",
    "revocation",
    "revoked",
    "revokes",
    "rescind",
    "rescinded",
    "rescission",
    "rescinds",
    "supersede",
    "superseded",
    "supersedes",
    "retracted",
    "vacated",
})


def _cites_r1_accept(text):
    if not isinstance(text, str) or text == "":
        return False
    return _R1_ACCEPT_PREFIX7 in text.translate(_ZERO_WIDTH).casefold()


def _r1_plain(text):
    """Casefold, drop zero-width characters, and unfold bold markers."""
    if not isinstance(text, str) or text == "":
        return ""
    plain = text.translate(_ZERO_WIDTH).casefold().replace("*", " ")
    return re.sub(r"\s+", " ", plain).strip()


def _r1_scrub_negation(plain):
    """Drop 'not withdrawn' and the same shape. 'not adopted' stays a status."""
    return _R1_NEGATED_RE.sub(" ", plain)


def _r1_object_hit(text):
    """True when a status word takes 69b98b2f as its object.

    'ACCEPTED by 69b98b2f' and 'SUPERSEDED_BY 69b98b2f' name it as the actor
    and do not match. 'r1/r2 superseded' names other documents and does not
    match unless the status sits on the 69b98b2f token itself.
    """
    plain = _r1_scrub_negation(_r1_plain(text))
    if _R1_ACCEPT_PREFIX7 not in plain:
        return False
    if _R1_OBJECT_OF_RE.search(plain) or _R1_OBJECT_BEFORE_RE.search(plain):
        return True
    return _R1_OBJECT_AFTER_RE.search(plain) is not None


def _r1_scrub_other_subjects(plain):
    """Remove status words that are tied to r1/r2 or to some other sha."""
    plain = _R1_ACTOR_RE.sub(" ", plain)
    plain = _R1_OTHER_LABEL_RE.sub(" ", plain)

    def keep_self(match):
        if match.group(1).startswith(_R1_ACCEPT_PREFIX7):
            return match.group(0)
        return " "

    return _R1_OTHER_HEX_RE.sub(keep_self, plain)


def _r1_subject_status(text):
    """A status aimed at this text after actor phrases and other documents are gone."""
    plain = _r1_scrub_other_subjects(_r1_scrub_negation(_r1_plain(text)))
    return _R1_STATUS_RE.search(plain) is not None


def _r1_header_keyed(line):
    """True when the line's own subject is 69b98b2f, not merely its actor."""
    plain = _r1_scrub_other_subjects(_r1_scrub_negation(_r1_plain(line)))
    return _R1_ACCEPT_PREFIX7 in plain


def _r1_status_line(line):
    return re.search(r"\bstatus\b", _r1_plain(line)) is not None


def _r1_subject_row(row):
    sha = row.get("sha256")
    if isinstance(sha, str) and sha.startswith(_R1_ACCEPT_PREFIX7):
        return True
    return _cites_r1_accept(row.get("path"))


def _r1_packet_action(path):
    if not isinstance(path, str) or path == "":
        return False
    parts = re.split(r"[^a-z0-9]+", path.translate(_ZERO_WIDTH).casefold())
    return any(part in _R1_PACKET_ACTIONS for part in parts)


def _r1_entries(text):
    """Heading-led blocks. A blank line or a new heading starts a new entry."""
    entries = []
    current = []
    for line in text.splitlines():
        if line.strip() == "":
            if current:
                entries.append(current)
                current = []
            continue
        if line.lstrip().startswith("#") and current:
            entries.append(current)
            current = [line]
            continue
        current.append(line)
    if current:
        entries.append(current)
    return entries


def _r1_accept_block_reason(text):
    """ACCEPT_69B98B2F_WITHDRAWN, or None.

    Defence in depth after the R1 accept citation set. A packet path named
    WITHDRAW, WITHDRAWAL, REVOKE, REVOCATION, RESCIND, or SUPERSEDE blocks
    when the row cites it. A status word blocks only when 69b98b2f is the
    object ('69b98b2f WITHDRAWN', 'WITHDRAW of 69b98b2f', 'revokes 69b98b2f',
    '69b98b2f superseded by X') or the entry's own subject (its sha or path,
    or a header keyed by it plus a later STATUS line). 'ACCEPTED by 69b98b2f'
    and 'SUPERSEDED_BY 69b98b2f' keep it as the actor and stay open.
    """
    if not isinstance(text, str) or text == "":
        return None
    for row in _index_rows(text):
        blob = row["path"] + " " + row["description"]
        if _cites_r1_accept(blob) and _r1_packet_action(row["path"]):
            return "ACCEPT_69B98B2F_WITHDRAWN"
        if _r1_object_hit(row["description"]) or _r1_object_hit(blob):
            return "ACCEPT_69B98B2F_WITHDRAWN"
        if _r1_subject_row(row) and _r1_subject_status(row["description"]):
            return "ACCEPT_69B98B2F_WITHDRAWN"
    for entry in _r1_entries(text):
        if not entry or not _r1_header_keyed(entry[0]):
            for line in entry:
                if _r1_object_hit(line):
                    return "ACCEPT_69B98B2F_WITHDRAWN"
            continue
        for line in entry[1:]:
            if _r1_status_line(line) and _r1_subject_status(line):
                return "ACCEPT_69B98B2F_WITHDRAWN"
        for line in entry:
            if _r1_object_hit(line):
                return "ACCEPT_69B98B2F_WITHDRAWN"
    for line in text.splitlines():
        if _r1_object_hit(line):
            return "ACCEPT_69B98B2F_WITHDRAWN"
    return None


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


def _load_citation_doc():
    """Return the citation pin, or None when it is missing or unusable.

    The raw bytes must match FEE_CITATION_SET_SHA256. A mismatch is an
    unusable pin. The constant is the reference; PINS.json is not read.
    """
    try:
        raw = _CITATION_PATH.read_bytes()
    except OSError:
        return None
    if sha256_bytes(raw) != FEE_CITATION_SET_SHA256:
        return None
    try:
        doc = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None
    if not isinstance(doc, dict):
        return None
    allow = doc.get("ruling_allowlist")
    watched = doc.get("watched_sha8")
    files = doc.get("watched_files")
    lines = doc.get("line_sha256")
    if (
        not isinstance(allow, list)
        or len(allow) != 1
        or not isinstance(allow[0], str)
        or allow[0] == ""
    ):
        return None
    if (
        not isinstance(watched, list)
        or not watched
        or any(not isinstance(item, str) or len(item) != 8 for item in watched)
    ):
        return None
    if (
        not isinstance(files, list)
        or not files
        or any(not isinstance(item, str) or item == "" for item in files)
    ):
        return None
    if (
        not isinstance(lines, list)
        or not lines
        or any(not isinstance(item, str) or len(item) != 64 for item in lines)
        or lines != sorted(lines)
    ):
        return None
    return doc


def _ruling_is_accept(ruling):
    """True only when ruling equals the single pinned allowlist token."""
    doc = _load_citation_doc()
    if doc is None or not isinstance(ruling, str):
        return False
    return ruling in doc["ruling_allowlist"]


def _citation_fold(line):
    """Drop zero-width characters, then casefold. The line hash stays raw."""
    return line.translate(_ZERO_WIDTH).casefold()


def _line_cites(folded, watched_sha8, watched_files):
    """True when the folded line contains a 7-hex prefix or a watched file name."""
    prefixes = [item[:7].casefold() for item in watched_sha8]
    names = [item.casefold() for item in watched_files]
    if any(prefix in folded for prefix in prefixes):
        return True
    return any(name in folded for name in names)


_R1_CITATION_PATH = Path(__file__).with_name("r1_accept_citation_set.json")
# sha256 of r1_accept_citation_set.json. A byte change with this constant
# left unchanged makes the pin unusable (ADV-10). There is no override.
R1_ACCEPT_CITATION_SET_SHA256 = "8e26ac4e5db007ab671119379acdf0251f18b08f56ab00813cdd4e89401d4da3"


def _load_r1_citation_doc():
    """Return the 69b98b2f citation pin, or None when it is missing or unusable.

    The raw bytes must match R1_ACCEPT_CITATION_SET_SHA256. A mismatch is an
    unusable pin. The constant is the reference; there is no path override.
    """
    try:
        raw = _R1_CITATION_PATH.read_bytes()
    except OSError:
        return None
    if sha256_bytes(raw) != R1_ACCEPT_CITATION_SET_SHA256:
        return None
    try:
        doc = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None
    if not isinstance(doc, dict):
        return None
    watched = doc.get("watched_sha8")
    lines = doc.get("line_sha256")
    if not isinstance(watched, list) or watched != ["69b98b2f"]:
        return None
    if (
        not isinstance(lines, list)
        or not lines
        or any(not isinstance(item, str) or len(item) != 64 for item in lines)
        or lines != sorted(lines)
    ):
        return None
    return doc


def _r1_citation_block_reason(text):
    """ACCEPT_69B98B2F_CITATIONS_CHANGED unless the index matches or cites none.

    Same citing-line rule as the fee set, watching only the 7-hex prefix
    69b98b2. The line hash is sha256 of the original rstrip'd line. An index
    that cites none of them is left to the word rule. An index that cites any
    must reproduce the pinned multiset. A missing or unusable pin fails closed.
    """
    doc = _load_r1_citation_doc()
    if doc is None:
        return "ACCEPT_69B98B2F_CITATIONS_CHANGED"
    found = []
    for line in text.splitlines():
        stripped = line.rstrip()
        if _line_cites(_citation_fold(stripped), doc["watched_sha8"], []):
            found.append(sha256_bytes(stripped.encode("utf-8")))
    found.sort()
    if not found:
        return None
    if found != doc["line_sha256"]:
        return "ACCEPT_69B98B2F_CITATIONS_CHANGED"
    return None


def _citation_block_reason(text):
    """FEE_CITATIONS_CHANGED unless this index matches the pin or cites none.

    A line cites when, after zero-width removal and casefolding, it contains
    the first 7 hex digits of a watched_sha8 entry or a watched file name.
    The line hash is sha256 of the original rstrip'd line. An index that
    cites none of them is left to the other checks. An index that cites any
    must reproduce the pinned multiset. A missing or unusable pin fails
    closed. Status words are not this gate.
    """
    doc = _load_citation_doc()
    if doc is None:
        return "FEE_CITATIONS_CHANGED"
    watched = doc["watched_sha8"]
    files = doc["watched_files"]
    found = []
    for line in text.splitlines():
        stripped = line.rstrip()
        if _line_cites(_citation_fold(stripped), watched, files):
            found.append(sha256_bytes(stripped.encode("utf-8")))
    found.sort()
    if not found:
        return None
    if found != doc["line_sha256"]:
        return "FEE_CITATIONS_CHANGED"
    return None


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

    index_text = index_bytes.decode("utf-8", "replace")
    citation_reason = _citation_block_reason(index_text)
    if citation_reason is not None:
        return _blocked(citation_reason, "b", "CITATION_SET", **identity)
    r1_set_reason = _r1_citation_block_reason(index_text)
    if r1_set_reason is not None:
        return _blocked(r1_set_reason, "b", "R1_ACCEPT_CITATION_SET", **identity)
    r1_reason = _r1_accept_block_reason(index_text)
    if r1_reason is not None:
        return _blocked(r1_reason, "b", "R1_ACCEPT", **identity)
    rows = _index_rows(index_text)
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
