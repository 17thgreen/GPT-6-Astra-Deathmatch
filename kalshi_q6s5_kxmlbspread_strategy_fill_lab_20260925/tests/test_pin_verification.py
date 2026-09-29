"""Sha256 checks for vendored Q6S5 strategy-fill pins.

Reads committed bytes only. A mismatch or a missing file fails the test.
This module does not run a fill or PnL computation.
"""
import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PIN_DIR = ROOT / 'Q6S5_KXMLBSPREAD_STRATEGY_FILL'
REPO = ROOT.parent

EXPECTED = {
    'CONDUCTOR_ACCEPT_VARIANTS_Q6S5_STRATEGY_FILL_FREEZE_2026-09-29.json':
        'c6f95b32a9224a6beede1a8c0e3d7f0a5a4530cc8b3d0b9d997995f65d64f8f3',
    'CONDUCTOR_ACCEPT_Q6S5_KXMLBSPREAD_STRATEGY_FILL_FREEZE_2026-09-29.json':
        'a5398129aa45c5dee5fdd15656a252bb6c460d00e4f5b06360ce522de0f968b4',
    'CONDUCTOR_RECONCILE_Q6S5_STRATEGY_FILL_DUAL_ACCEPT_SOLE_CLOUD_2026-09-29.json':
        '0f33a94c970eec6a9863041396071c78ce64b58abc8a7ab91f48062fbfc052b0',
    'Q6S5_KXMLBSPREAD_STRATEGY_FILL_FREEZE_2026-09-25.md':
        '9f50ba19694083c774bbe2a6cff491d1a2f81ed3a6f9cc21a3641a938c84955d',
    'CONDUCTOR_KICK_VARIANTS_Q6S5_STRATEGY_FILL_FREEZE_2026-09-25.json':
        'dc19794bdb8e26c3a3f4fe86eadc9bec1b02db97d508fca9426e3c3eddfb6bc8',
    'CONDUCTOR_RULING_ADMIT1_OUTAGE_GAP_WEATHER_CARD03_RELAUNCH_2026-09-29.json':
        'ac7cfe63623ca342ab5b4285ff58382a8138b58fb6cd8e95310a5d30d90304f2',
    'CONDUCTOR_QUEUE_Q6S5_STRATEGY_FILL_FREEZE_AFTER_Q6S1_2026-09-25.json':
        '7472b8ac01fd906577c49eb4d96b8fd5dbb2d7766c5a87fa86e47b3bffad2c61',
    'FROZEN_EXPERIMENT.json':
        '7383b4836a378b1da8afe889d82a13997b9b3a4584bdc454ae1c67785eab5fff',
    'SOURCE_PINS.json':
        '1846a9710375dd418983e1a03e05ac15386138ada7c405923b7fd0514cf116a1',
    'EMPTY_RESULTS.json':
        '9b5752893c714ff8fc8e2e1867f902eb5c06c5d6aab35e46e1c786b925bd97bc',
    'Q6S5_KXMLBSPREAD_STRATEGY_FILL_FREEZE_DIGEST_2026-09-25.json':
        'da84339141cef2cb52bfbd33629eb4896b98c3581a55ef8a3f286a3f631d87ed',
    'QUEUE_LINEAGE.md':
        '86fad73cc18a2edc374279d6c9ff3e2c393f3e4dc2ad32e2de94180c2fd378b4',
    'Q6S5_KXMLBSPREAD_STRATEGY_FILL_authentic_pins_2026-09-25.tgz':
        '6602e07ef9b444b8b242086d0cb338025507d117aa0874f24e99390cd9d01993',
    'Q6S5_KXMLBSPREAD_STRATEGY_FILL_authentic_pins_v2_2026-09-25.tgz':
        '739d81d6ab29d1b3964d3c4d1d72c02e0db202e8646777f8c484152d4816e02a',
}


class PinVerificationError(Exception):
    """One or more vendored pin files are missing or do not match."""

    def __init__(self, failures):
        self.failures = list(failures)
        super().__init__('\n'.join(self.failures))


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b''):
            digest.update(chunk)
    return digest.hexdigest()


def check_manifest(pin_dir, manifest_name):
    """Check a sha256sum manifest. Raises PinVerificationError on any failure."""
    failures = []
    manifest = Path(pin_dir) / manifest_name
    if not manifest.is_file():
        raise PinVerificationError(['missing manifest %s' % manifest_name])
    for lineno, line in enumerate(manifest.read_text(encoding='utf-8').splitlines(), 1):
        if line == '':
            continue
        parts = line.split('  ', 1)
        if len(parts) != 2 or len(parts[0]) != 64:
            failures.append('%s:%s unreadable' % (manifest_name, lineno))
            continue
        digest, name = parts
        target = Path(pin_dir) / name
        if not target.is_file():
            failures.append('%s:%s missing %s' % (manifest_name, lineno, name))
            continue
        got = sha256_file(target)
        if got != digest:
            failures.append(
                '%s:%s mismatch %s got %s expected %s' % (
                    manifest_name, lineno, name, got, digest,
                )
            )
    if failures:
        raise PinVerificationError(failures)


def verify_pins(pin_dir, expected):
    """Hash expected files and require MANIFEST.sha256 to check clean."""
    pin_dir = Path(pin_dir)
    failures = []
    if not pin_dir.is_dir():
        raise PinVerificationError(['missing pin dir %s' % pin_dir])
    for name, digest in expected.items():
        path = pin_dir / name
        if not path.is_file():
            failures.append('missing %s' % name)
            continue
        got = sha256_file(path)
        if got != digest:
            failures.append('mismatch %s got %s expected %s' % (name, got, digest))
    if failures:
        raise PinVerificationError(failures)
    check_manifest(pin_dir, 'MANIFEST.sha256')
    return True


class PinVerificationTests(unittest.TestCase):
    def test_committed_pins_match_hardcoded_sha256_and_manifest(self):
        self.assertEqual(len(EXPECTED), 14)
        verify_pins(PIN_DIR, EXPECTED)
        check_manifest(PIN_DIR, 'MANIFEST_V2.sha256')
        v2_line = (PIN_DIR / 'MANIFEST_V2.sha256').read_text(encoding='utf-8').strip()
        self.assertEqual(
            v2_line,
            EXPECTED['Q6S5_KXMLBSPREAD_STRATEGY_FILL_authentic_pins_v2_2026-09-25.tgz']
            + '  Q6S5_KXMLBSPREAD_STRATEGY_FILL_authentic_pins_v2_2026-09-25.tgz',
        )
        authority = json.loads((ROOT / 'AUTHORITY_VERIFICATION.json').read_text())
        source = json.loads((ROOT / 'SOURCE_PINS.json').read_text())
        self.assertIs(authority['digest_all_match_claimed'], True)
        self.assertIs(source['digest_all_match_claimed'], True)
        self.assertEqual(authority['primary_authentic_bundle']['version'], 'v2')
        self.assertEqual(
            authority['primary_authentic_bundle']['sha256'],
            EXPECTED['Q6S5_KXMLBSPREAD_STRATEGY_FILL_authentic_pins_v2_2026-09-25.tgz'],
        )
        self.assertEqual(authority['v1_subset_bundle']['role'], 'subset')
        self.assertEqual(
            authority['v1_subset_bundle']['sha256'],
            EXPECTED['Q6S5_KXMLBSPREAD_STRATEGY_FILL_authentic_pins_2026-09-25.tgz'],
        )
        self.assertEqual(len(authority['pins']), 14)
        seen = {}
        for pin in authority['pins']:
            seen[pin['key']] = pin
            path = REPO / pin['path']
            self.assertTrue(path.is_file(), pin['path'])
            self.assertEqual(sha256_file(path), pin['claimed_sha256'])
            self.assertIn(path.name, EXPECTED)
            self.assertEqual(pin['claimed_sha256'], EXPECTED[path.name])
        self.assertEqual(
            seen['conductor_accept']['role'],
            'implementation ACCEPT',
        )
        self.assertEqual(
            seen['conductor_accept_companion']['role'],
            'companion rulings',
        )
        self.assertEqual(
            seen['reconcile_dual_accept']['claimed_sha256'],
            '0f33a94c970eec6a9863041396071c78ce64b58abc8a7ab91f48062fbfc052b0',
        )
        absent = {item['key'] for item in authority['measurement_absent']}
        self.assertEqual(
            absent,
            {
                'mechanic_demo_artifact',
                'examiner_formula_id',
                'sep25_settlements_6_of_12',
                'untouched_evaluation_period',
                'admit1_window_data',
            },
        )
        self.assertIs(authority['superseded_not_recreated']['recreated'], False)
        self.assertIsNone(authority['results'])
        self.assertIsNone(authority['pnl'])
        self.assertIsNone(authority['roi'])
        self.assertIsNone(source['results'])
        self.assertIsNone(source['pnl'])
        self.assertIsNone(source['roi'])
        governance = (
            REPO / 'lab' / 'governance' / 'astra' / 'packets'
            / 'Q6S5_KXMLBSPREAD_STRATEGY_FILL'
        )
        self.assertFalse(governance.exists())

    def test_tampered_byte_reports_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / 'pins'
            shutil.copytree(PIN_DIR, dest)
            target = dest / 'EMPTY_RESULTS.json'
            data = bytearray(target.read_bytes())
            self.assertGreater(len(data), 0)
            data[0] ^= 0xFF
            target.write_bytes(data)
            with self.assertRaises(PinVerificationError) as ctx:
                verify_pins(dest, EXPECTED)
        self.assertTrue(ctx.exception.failures)
        self.assertTrue(
            any(
                'mismatch' in item and 'EMPTY_RESULTS.json' in item
                for item in ctx.exception.failures
            )
        )

    def test_missing_file_reports_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / 'pins'
            shutil.copytree(PIN_DIR, dest)
            (dest / 'QUEUE_LINEAGE.md').unlink()
            with self.assertRaises(PinVerificationError) as ctx:
                verify_pins(dest, EXPECTED)
        self.assertTrue(
            any('missing QUEUE_LINEAGE.md' == item for item in ctx.exception.failures)
        )


if __name__ == '__main__':
    unittest.main()
