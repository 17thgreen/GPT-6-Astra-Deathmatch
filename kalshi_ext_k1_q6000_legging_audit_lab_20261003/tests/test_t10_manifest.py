import hashlib
import tempfile
import unittest
from pathlib import Path

import support  # noqa: F401
from errors import ManifestMismatch
from pins_io import manifest_entries, parse_after_hash, verified_bytes
from constants import PINS_REL


class T10Manifest(unittest.TestCase):
    def test_one_byte_tamper_fails_before_parse(self):
        original = verified_bytes(PINS_REL["weeks"])
        expected = hashlib.sha256(original).hexdigest()
        parsed = {"called": False}

        def parser(data):
            parsed["called"] = True
            return data

        self.assertEqual(manifest_entries()[0][0], manifest_entries()[0][0])
        self.assertEqual(len(manifest_entries()), 37)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "weeks.json"
            flipped = bytearray(original)
            flipped[-1] ^= 0x01
            path.write_bytes(flipped)
            with self.assertRaises(ManifestMismatch):
                parse_after_hash(path, expected, parser)
        self.assertFalse(parsed["called"])
        self.assertIs(parse_after_hash_bytes(original, expected, parser), original)
        self.assertTrue(parsed["called"])


def parse_after_hash_bytes(data, expected, parser):
    digest = hashlib.sha256(data).hexdigest()
    if digest != expected:
        raise ManifestMismatch("memory")
    return parser(data)


if __name__ == "__main__":
    unittest.main()
