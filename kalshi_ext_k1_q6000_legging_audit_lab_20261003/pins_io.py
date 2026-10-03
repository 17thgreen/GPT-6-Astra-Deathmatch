"""Closed manifest reader. Every pin is hashed before its bytes are returned."""

import hashlib
import json
import tarfile
from pathlib import Path

from constants import BUNDLE_SHA256, MANIFEST_SHA256, REFUSED_PATHS
from errors import ManifestMismatch, SqlitePathRefused

LAB = Path(__file__).resolve().parent
PINS = LAB / "pins"
BUNDLE_NAME = "EXT_K1_authentic_pins_2026-10-03.tgz"
TREE_NAME = "EXT_K1_authentic_pins_2026-10-03"
_MANIFEST = None


def bundle_path():
    return PINS / BUNDLE_NAME


def tree_root():
    return PINS / TREE_NAME


def assert_path_allowed(path):
    norm = str(path).replace("\\", "/")
    for refused in REFUSED_PATHS:
        if norm == refused or norm.endswith("/" + refused) or norm.endswith(refused):
            raise SqlitePathRefused(norm)
    base = Path(norm).name
    if base in {"capture.sqlite", "archive.sqlite"}:
        raise SqlitePathRefused(norm)


def _sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ensure_tree():
    """Extract the vendored tarball when the tree is absent. Bytes stay inside pins/."""
    root = tree_root()
    manifest = root / "MANIFEST.sha256"
    tgz = bundle_path()
    if not tgz.is_file():
        raise ManifestMismatch("pin bundle tarball is absent")
    if _sha256(tgz) != BUNDLE_SHA256:
        raise ManifestMismatch("pin bundle tarball sha256")
    if not manifest.is_file():
        with tarfile.open(tgz, "r:gz") as archive:
            _safe_extract(archive, PINS)
    if not manifest.is_file():
        raise ManifestMismatch("inner MANIFEST.sha256 missing after extract")
    if _sha256(manifest) != MANIFEST_SHA256:
        raise ManifestMismatch("inner MANIFEST.sha256")
    return root


def _safe_extract(archive, destination):
    dest = destination.resolve()
    for member in archive.getmembers():
        target = (dest / member.name).resolve()
        if dest != target and dest not in target.parents:
            raise ManifestMismatch("tarball path escapes pins/")
        assert_path_allowed(member.name)
    archive.extractall(dest)


def manifest_entries():
    global _MANIFEST
    if _MANIFEST is None:
        text = (ensure_tree() / "MANIFEST.sha256").read_text(encoding="utf-8")
        entries = []
        for line in text.splitlines():
            if not line.strip():
                continue
            digest, rel = line.split()
            entries.append((digest, rel))
        if len(entries) != 37:
            raise ManifestMismatch(f"manifest count {len(entries)}")
        _MANIFEST = entries
    return _MANIFEST


def manifest_map():
    return {rel: digest for digest, rel in manifest_entries()}


def verified_bytes(rel_path):
    """Hash the pin and only then return bytes. A mismatch raises first."""
    assert_path_allowed(rel_path)
    expected = manifest_map().get(rel_path)
    if expected is None:
        raise ManifestMismatch(f"path not in MANIFEST: {rel_path}")
    path = ensure_tree() / rel_path
    if not path.is_file():
        # A gitignored ledger may be absent until the tarball is expanded again.
        with tarfile.open(bundle_path(), "r:gz") as archive:
            _safe_extract(archive, PINS)
    data = path.read_bytes()
    got = hashlib.sha256(data).hexdigest()
    if got != expected:
        raise ManifestMismatch(rel_path)
    return data


def open_verified(rel_path, parser):
    """Parse only after the hash matches. parser is not called on mismatch."""
    data = verified_bytes(rel_path)
    return parser(data)


def verify_all():
    """Hash every manifest path before any measurement parse."""
    checked = {}
    for digest, rel in manifest_entries():
        data = verified_bytes(rel)
        if hashlib.sha256(data).hexdigest() != digest:
            raise ManifestMismatch(rel)
        checked[rel] = digest
    return checked


def read_json(rel_path):
    return open_verified(rel_path, lambda data: json.loads(data.decode("utf-8")))


def parse_after_hash(path, expected_sha, parser):
    """Return parser(bytes) only after the hash matches. A mismatch does not parse."""
    path = Path(path)
    assert_path_allowed(path)
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != expected_sha:
        raise ManifestMismatch(str(path))
    return parser(data)


def reset_cache():
    global _MANIFEST
    _MANIFEST = None
