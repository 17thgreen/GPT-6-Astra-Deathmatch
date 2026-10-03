"""Closed manifest for part (a). Sha256 is checked before a file is parsed."""

import json
from pathlib import Path

from shared.canonical import sha256_file
from shared.exceptions import BeckerMixRefused, ClosedUniverseRefused, ManifestTamper
from shared.refusals import assert_not_holdout, assert_sqlite_path_refused, assert_timestamp_allowed

LAB = Path(__file__).resolve().parents[1]
PINS = LAB / "pins"
K1_ROOT = PINS / "k1" / "EXT_K1_authentic_pins_2026-10-03"
K2_ROOT = PINS / "k2" / "EXT_K2_authentic_pins_2026-10-03"

K1_BUNDLE_SHA = "0f8f529733bfd1ccb01b36f312cdc20865cc2811c04dcd3c812d50c67295db38"
K2_BUNDLE_SHA = "963f7663a74527db38479bbf4a253870bd5dc6f99c8f85b70750d3600c65907f"
K1_MANIFEST_SHA = "a041561e130fb97eaa8d7bfab5dd6fa53963fa4fbdb13c00cd4f71089e0e3db5"
K2_MANIFEST_SHA = "2e91d48f87e144031aa18fc4eb0f6d85953a7fa6c817bbfa4e5ba4af567931a3"
K1_PARTS = {
    "EXT_K1_authentic_pins_2026-10-03.tgz.part-00": "3fd70f7ba7c3543877e3608b9d1f3c7532307f8d7869590d8d02e9dc8e9ca027",
    "EXT_K1_authentic_pins_2026-10-03.tgz.part-01": "1f8b2ac11ffe3ff26b784351c9fc7519848d96c605d71aef633abe98d24c914b",
}

# Full Becker box-only shas named in the freeze. The manifest file itself is not in git.
BECKER_BOXONLY_SHA256 = frozenset({
    "a1e1027e8fd1e5bda30c3a4124e990048d5a7700cf2b08df24c1fbc5a0054e99",
    "7238e85874f3e231a9719aaa66847bd166c51c746f92f2e2ccc737ed96e439dd",
    "61a4c993fbea5940e5999177ffb5a0e3161219a8f84812af2d2f44d9f556641b",
    "fd5e10531f488f30baf05e2dd6f17c8f8823603ecbae457170dbbde66126fb95",
    "6f5af9071dd72dc398b0180b779a78da3cb2bfbb88a75217d9c6e65e3fb58819",
    "79be0f4e42e913c341b9186a9b7ee2e02bbb9c4d95d97368176b682e2e5e15ab",
    "ea354f2f4cf75a1a395fed7044c3a05ba0644a93852eb51adce16d8a5f226ef4",
})

FACTORIAL_REL = "lab/astra-science/nfl_factorial_lab_20260921"


def refuse_dev_input(path, sha=None):
    """Part (a) refuses parquet, Becker paths, and box-only shas before any parse."""
    text = str(path).replace("\\", "/")
    assert_sqlite_path_refused(text)
    lowered = text.lower()
    if lowered.endswith(".parquet") or "/becker" in lowered or "becker_" in lowered:
        raise BeckerMixRefused(text)
    if sha is not None and sha in BECKER_BOXONLY_SHA256:
        raise BeckerMixRefused(sha)
    return text


def _parse_manifest(path):
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, rel = line.split(None, 1)
        rows.append((digest, rel.strip()))
    return rows


def verify_manifest(root, manifest_name, expected_manifest_sha):
    """Hash the manifest, then hash each listed file. A mismatch raises before JSON parse."""
    manifest = root / manifest_name
    digest = sha256_file(manifest)
    if digest != expected_manifest_sha:
        raise ManifestTamper(manifest_name)
    checked = []
    for expected, rel in _parse_manifest(manifest):
        target = root / rel
        got = sha256_file(target)
        if got != expected:
            raise ManifestTamper(rel)
        checked.append(rel)
    return checked


def verify_bundles():
    """Check bundle bytes and both inner manifests. Does not parse ledgers."""
    k1 = PINS / "EXT_K1_authentic_pins_2026-10-03.tgz"
    k2 = PINS / "EXT_K2_authentic_pins_2026-10-03.tgz"
    if sha256_file(k1) != K1_BUNDLE_SHA:
        raise ManifestTamper("K1 bundle")
    if sha256_file(k2) != K2_BUNDLE_SHA:
        raise ManifestTamper("K2 bundle")
    for name, digest in K1_PARTS.items():
        if sha256_file(PINS / name) != digest:
            raise ManifestTamper(name)
    k1_files = verify_manifest(K1_ROOT, "MANIFEST.sha256", K1_MANIFEST_SHA)
    k2_files = verify_manifest(K2_ROOT, "MANIFEST.sha256", K2_MANIFEST_SHA)
    return {"k1_files": len(k1_files), "k2_files": len(k2_files)}


def checked_bytes(path, expected_sha):
    """Hash first. Parse only if the caller then decodes these bytes."""
    refuse_dev_input(path)
    digest = sha256_file(path)
    if digest != expected_sha:
        raise ManifestTamper(str(path))
    return path.read_bytes(), digest


def load_holdout_sets():
    path = K1_ROOT / FACTORIAL_REL / "RESERVED_HOLDOUT.json"
    raw, _ = checked_bytes(path, "74507e1a4371d69bc79ea2369f9bff030a74f51ee80c8072ba9c0f5345d377ca")
    doc = json.loads(raw.decode("utf-8"))
    events = set()
    game_ids = set()
    for row in doc["holdout_games"]:
        if row.get("event"):
            events.add(row["event"])
        if row.get("game_id"):
            game_ids.add(row["game_id"])
    return events, game_ids


def assert_dev_row(row, holdout_events, holdout_game_ids, markets, weeks):
    assert_timestamp_allowed(row["at"])
    ticker = row.get("ticker")
    event = row.get("event")
    if event is None and ticker is not None:
        event = ticker.rsplit("-", 1)[0]
    assert_not_holdout(event=event, ticker=ticker, game_id=row.get("game_id"),
                       holdout_events=holdout_events, holdout_game_ids=holdout_game_ids)
    if ticker is not None and ticker not in markets:
        raise ClosedUniverseRefused(ticker)
    if event is not None and event not in weeks:
        raise ClosedUniverseRefused(event)


def cloud_input_shas():
    """Sha256 values of part (a) inputs, so part (b) can refuse them."""
    path = K2_ROOT / "lab/governance/astra/packets/EXT_K2_OPTIMISM_TAX/SOURCE_PINS.json"
    doc = json.loads(path.read_text(encoding="utf-8"))
    found = set()

    def walk(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "sha256" and isinstance(value, str) and len(value) == 64:
                    found.add(value)
                else:
                    walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(doc)
    found.add(K1_BUNDLE_SHA)
    found.add(K2_BUNDLE_SHA)
    return frozenset(found)
