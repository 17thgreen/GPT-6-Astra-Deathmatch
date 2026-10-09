import tempfile
import unittest
from pathlib import Path

import support
from ext2k1.constants import (
    B2_SHA256,
    BUILDER_SHA256,
    COHORT_SHA256,
    HOLDOUT_SHA256,
    MARKETS_SHA256,
    TAPE_SHA256,
)
from ext2k1.errors import SourcePinMismatch
from ext2k1.pins_io import read_source_pins, verify_entries, verify_production

_TABLE_B = {
    "B1 dev tape": TAPE_SHA256,
    "B1 markets": MARKETS_SHA256,
    "B1 cohort": COHORT_SHA256,
    "RESERVED_HOLDOUT": HOLDOUT_SHA256,
    "B2 000 fills": B2_SHA256,
    "B1 quote builder": BUILDER_SHA256,
}


class T10Manifest(unittest.TestCase):
    def test_production_pins_match_table_b_and_hash(self):
        document = read_source_pins()
        self.assertEqual(document["schema"], "astra.ext2k1.source_pins.v1")
        by_role = {entry["role"]: entry for entry in document["pins"]}
        self.assertEqual(set(by_role), set(_TABLE_B))
        for role, digest in _TABLE_B.items():
            self.assertEqual(by_role[role]["sha256"], digest, role)
        checked = verify_production()
        self.assertEqual(
            [(entry["role"], entry["sha256"]) for entry in checked],
            [(entry["role"], entry["sha256"]) for entry in document["pins"]],
        )

    def test_tampered_synthetic_source_writes_nothing(self):
        original = (support.LAB / "tests" / "fixtures" / "SYNTH_EXT2K1_FIXTURES.json").read_bytes()
        payload = bytearray(original)
        payload[0] ^= 0xFF
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "fixture.json").write_bytes(payload)
            entry = {
                "role": "synthetic tape fixture",
                "path": "fixture.json",
                "bytes": len(original),
                "sha256": "4f6791ee4cce5baa3f67acb29c563c0823b36f6ecea420a03cabe95e8efca430",
            }
            with self.assertRaises(SourcePinMismatch):
                verify_entries(root, [entry])
            self.assertFalse((root / "RESULTS.json").exists())
            self.assertFalse((root / "RECEIPT.json").exists())
            self.assertFalse((root / "SWEEPS.json").exists())


if __name__ == "__main__":
    unittest.main()
