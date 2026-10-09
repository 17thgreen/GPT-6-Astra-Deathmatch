"""Closed manifest. Repo root is the parent of this lab. Paths come only from SOURCE_PINS.json."""

import hashlib
import json
from pathlib import Path

from .errors import SourcePinMismatch
from .refusals import assert_source_path

LAB_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = LAB_DIR.parent
SOURCE_PINS_PATH = LAB_DIR / "SOURCE_PINS.json"
PACKAGE_DIR = Path(__file__).resolve().parent


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_source_pins(path=None):
    pin_path = Path(path) if path is not None else SOURCE_PINS_PATH
    try:
        text = pin_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SourcePinMismatch(str(pin_path)) from exc
    data = json.loads(text)
    pins = data.get("pins")
    if not isinstance(pins, list) or not pins:
        raise SourcePinMismatch("pins")
    return data


def verify_entries(root, entries):
    """Hash each pin. Mismatch raises SourcePinMismatch and returns nothing."""
    checked = []
    for entry in entries:
        rel = entry["path"]
        assert_source_path(rel)
        full = Path(root) / rel
        if not full.is_file():
            raise SourcePinMismatch(rel)
        size = full.stat().st_size
        digest = sha256_file(full)
        if size != entry["bytes"] or digest != entry["sha256"]:
            raise SourcePinMismatch(rel)
        checked.append(
            {
                "role": entry["role"],
                "path": rel,
                "bytes": size,
                "sha256": digest,
            }
        )
    return checked


def verify_production(root=None, pins_path=None):
    root = REPO_ROOT if root is None else Path(root)
    document = read_source_pins(pins_path)
    return verify_entries(root, document["pins"])


def entry_by_role(entries, role):
    for entry in entries:
        if entry["role"] == role:
            return entry
    raise SourcePinMismatch(role)


def verified_role_bytes(role, root=None):
    """Hash-check one production pin, then return its raw bytes."""
    root = REPO_ROOT if root is None else Path(root)
    document = read_source_pins()
    entry = entry_by_role(document["pins"], role)
    verify_entries(root, [entry])
    return (root / entry["path"]).read_bytes()


def load_verified_json(role, root=None):
    return json.loads(verified_role_bytes(role, root=root).decode("utf-8"))


def read_git_commit(repo_root=None):
    """Read HEAD as text. No subprocess. Unresolvable refs return None."""
    root = REPO_ROOT if repo_root is None else Path(repo_root)
    git_path = root / ".git"
    if not git_path.exists():
        return None
    if git_path.is_file():
        text = git_path.read_text(encoding="utf-8").strip()
        if not text.startswith("gitdir:"):
            return None
        git_path = Path(text.split(":", 1)[1].strip())
        if not git_path.is_absolute():
            git_path = root / git_path
    head_path = git_path / "HEAD"
    if not head_path.is_file():
        return None
    text = head_path.read_text(encoding="utf-8").strip()
    if text.startswith("ref:"):
        ref = text.split(":", 1)[1].strip()
        ref_path = git_path / ref
        if not ref_path.is_file():
            return None
        return ref_path.read_text(encoding="utf-8").strip() or None
    return text or None


def sweeps_module_sha256():
    return sha256_file(PACKAGE_DIR / "sweeps.py")
