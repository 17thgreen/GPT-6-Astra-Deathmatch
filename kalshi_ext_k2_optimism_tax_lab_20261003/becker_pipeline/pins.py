"""Part (b) pin reads. Does not import dev_pipeline and does not parse Becker rows."""

import json
from pathlib import Path

from shared.canonical import sha256_file
from shared.exceptions import ManifestTamper

LAB = Path(__file__).resolve().parents[1]
K1_ROOT = LAB / "pins" / "k1" / "EXT_K1_authentic_pins_2026-10-03"
K2_ROOT = LAB / "pins" / "k2" / "EXT_K2_authentic_pins_2026-10-03"
HOLDOUT_SHA = "74507e1a4371d69bc79ea2369f9bff030a74f51ee80c8072ba9c0f5345d377ca"
SOURCE_PINS_SHA = "5133c826bde3b8ed73df368f4031de7e445e7408b8bcb4e06a18aa42db074747"
K1_BUNDLE_SHA = "0f8f529733bfd1ccb01b36f312cdc20865cc2811c04dcd3c812d50c67295db38"
K2_BUNDLE_SHA = "963f7663a74527db38479bbf4a253870bd5dc6f99c8f85b70750d3600c65907f"

_HOLDOUT = None
_CLOUD = None


def load_holdout_sets():
    """Sha-check the reserved holdout list, then parse identifiers only."""
    global _HOLDOUT
    if _HOLDOUT is not None:
        return _HOLDOUT
    path = K1_ROOT / "lab/astra-science/nfl_factorial_lab_20260921/RESERVED_HOLDOUT.json"
    digest = sha256_file(path)
    if digest != HOLDOUT_SHA:
        raise ManifestTamper("RESERVED_HOLDOUT")
    doc = json.loads(path.read_text(encoding="utf-8"))
    events = set()
    game_ids = set()
    for row in doc["holdout_games"]:
        if row.get("event"):
            events.add(row["event"])
        if row.get("game_id"):
            game_ids.add(row["game_id"])
    _HOLDOUT = (events, game_ids)
    return _HOLDOUT


def cloud_input_shas():
    """Sha256 values named under SOURCE_PINS cloud_part_a_inputs."""
    global _CLOUD
    if _CLOUD is not None:
        return _CLOUD
    path = K2_ROOT / "lab/governance/astra/packets/EXT_K2_OPTIMISM_TAX/SOURCE_PINS.json"
    digest = sha256_file(path)
    if digest != SOURCE_PINS_SHA:
        raise ManifestTamper("SOURCE_PINS")
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

    walk(doc.get("cloud_part_a_inputs", doc))
    found.add(K1_BUNDLE_SHA)
    found.add(K2_BUNDLE_SHA)
    _CLOUD = frozenset(found)
    return _CLOUD
