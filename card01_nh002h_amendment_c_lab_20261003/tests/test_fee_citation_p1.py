"""P1 citation pin: amendment 2c870cd5, file-name folding, runtime pin sha.

Synthetic indexes only, except the real-data cases, which skip unless
CARD01_R1_REAL_FEE_DIR is set. Existing admission tests are not edited.
"""
from __future__ import annotations

import json
import os
import unittest
from pathlib import Path

from card01_amc import fee_admission
from card01_amc.fee_admission import admit_fee_source_v2
from card01_amc.pinload import sha256_bytes
from tests.support import LAB
from tests.test_fee_admission_v2 import _copy_kit, _no_fee_numbers, _repin

WATCHED_FILES = [
    "FEE_SOURCE_CARD01_v2_2026-10-08_r1fill.json",
    "CONDUCTOR_ACCEPT_FEE_SOURCE_CARD01_V2_FILL_2026-10-08.json",
    "EXAMINER_ATTEST_FEE_SOURCE_CARD01_V2_2026-10-08_r2.json",
]
SYNTH_PREFIX = "aa11bb22"


def _pin_bytes(doc):
    return (json.dumps(doc, indent=1) + "\n").encode("utf-8")


def _install_pin(testcase, path):
    raw = path.read_bytes()
    testcase._pin_path = fee_admission._CITATION_PATH
    testcase._pin_sha = fee_admission.FEE_CITATION_SET_SHA256
    fee_admission._CITATION_PATH = path
    fee_admission.FEE_CITATION_SET_SHA256 = sha256_bytes(raw)

    def restore():
        fee_admission._CITATION_PATH = testcase._pin_path
        fee_admission.FEE_CITATION_SET_SHA256 = testcase._pin_sha

    testcase.addCleanup(restore)


def _citing_hashes(text, watched_sha8, watched_files):
    found = []
    for line in text.splitlines():
        stripped = line.rstrip()
        if fee_admission._line_cites(
            fee_admission._citation_fold(stripped),
            watched_sha8,
            watched_files,
        ):
            found.append(sha256_bytes(stripped.encode("utf-8")))
    found.sort()
    return found


class CitationPinTests(unittest.TestCase):
    def test_production_pin_shape_and_line_list_sha(self):
        raw = (LAB / "card01_amc" / "fee_citation_set.json").read_bytes()
        self.assertEqual(sha256_bytes(raw), fee_admission.FEE_CITATION_SET_SHA256)
        doc = json.loads(raw.decode("utf-8"))
        self.assertEqual(
            doc["watched_sha8"],
            ["6edc3eff", "cb5e88a6", "b59e4168", "2c870cd5"],
        )
        self.assertEqual(doc["watched_files"], WATCHED_FILES)
        self.assertEqual(doc["ruling_allowlist"], ["ACCEPT_FEE_SOURCE_CARD01_v2_FILL"])
        self.assertEqual(
            doc["packet_index_sha256"],
            "4a1ceb4b036b45914d5c0a0b7f6eeac9efb208f7792f99423acbeaf852587dfe",
        )
        self.assertEqual(len(doc["line_sha256"]), 26)
        self.assertEqual(doc["line_sha256"], sorted(doc["line_sha256"]))
        blob = "\n".join(doc["line_sha256"]) + "\n"
        self.assertEqual(
            sha256_bytes(blob.encode("utf-8")),
            "87b9626e3f82143c04d17a6f3181112b6e9c3967c209cd0376f12340ece24bd8",
        )
        self.assertIn(
            "14fe3f3d86f6359f9ad77f6acfb5d156bd6d32608028ba4d41cad19c80432dc6",
            doc["line_sha256"],
        )

    def test_synthetic_withdraw_of_watched_amendment_blocks(self):
        """A later WITHDRAW row that cites only the watched amendment blocks."""
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = _copy_kit(root)
            _paths = _repin(
                root,
                json.loads(paths[0].read_bytes()),
            )
            fee_path, accept_path, index_path, fee_sha = _paths
            base = index_path.read_text(encoding="utf-8")
            cite = (
                "| `notes/SYNTH_AMENDMENT_"
                + SYNTH_PREFIX
                + ".md` (synthetic amendment "
                + SYNTH_PREFIX
                + ") | `"
                + ("ab" * 32)
                + "` |\n"
            )
            armed = base + cite
            watched = [SYNTH_PREFIX]
            doc = {
                "packet_index_sha256": "ab" * 32,
                "ruling_allowlist": ["ACCEPT_FEE_SOURCE_CARD01_v2_FILL"],
                "watched_sha8": watched,
                "watched_files": list(WATCHED_FILES),
                "line_sha256": _citing_hashes(armed, watched, WATCHED_FILES),
            }
            pin_path = root / "fee_citation_set.json"
            pin_path.write_bytes(_pin_bytes(doc))
            _install_pin(self, pin_path)
            index_path.write_text(armed, encoding="utf-8")
            admitted = admit_fee_source_v2(
                fee_source_path=fee_path,
                fee_source_id="FEE_SOURCE_SYNTH_v2",
                fee_source_sha256=fee_sha,
                packet_index_path=index_path,
                fee_accept_path=accept_path,
                series_used=["XS1"],
            )
            self.assertEqual(admitted.fee_admission, "ADMITTED_INDEX_ONLY")
            withdrawn = armed + (
                "Conductor WITHDRAW of amendment " + SYNTH_PREFIX + "\n"
            )
            index_path.write_text(withdrawn, encoding="utf-8")
            blocked = admit_fee_source_v2(
                fee_source_path=fee_path,
                fee_source_id="FEE_SOURCE_SYNTH_v2",
                fee_source_sha256=fee_sha,
                packet_index_path=index_path,
                fee_accept_path=accept_path,
                series_used=["XS1"],
            )
            self.assertEqual(blocked.fee_admission, "BLOCKED_FEE_UNVERIFIED")
            self.assertEqual(blocked.fee_block_reason, "FEE_CITATIONS_CHANGED")
            self.assertTrue(_no_fee_numbers(blocked.public_dict()))

    def test_folded_citations_change_the_multiset(self):
        """Uppercase, zero-width, 7-hex, and file-name citations each block."""
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = _copy_kit(root)
            fee_path, accept_path, index_path, fee_sha = _repin(
                root,
                json.loads(paths[0].read_bytes()),
            )
            base = index_path.read_text(encoding="utf-8")
            watched = [SYNTH_PREFIX]
            # The admitting pin watches the prefix but the base index cites none.
            empty = {
                "packet_index_sha256": "ab" * 32,
                "ruling_allowlist": ["ACCEPT_FEE_SOURCE_CARD01_v2_FILL"],
                "watched_sha8": watched,
                "watched_files": list(WATCHED_FILES),
                "line_sha256": ["ab" * 32],
            }
            # line_sha256 must be sorted 64-hex. An unused placeholder would
            # make a citing index fail closed, which is what these cases need.
            # The base index cites none, so admission does not compare the list.
            pin_path = root / "fee_citation_set.json"
            pin_path.write_bytes(_pin_bytes(empty))
            _install_pin(self, pin_path)
            index_path.write_text(base, encoding="utf-8")
            clear = admit_fee_source_v2(
                fee_source_path=fee_path,
                fee_source_id="FEE_SOURCE_SYNTH_v2",
                fee_source_sha256=fee_sha,
                packet_index_path=index_path,
                fee_accept_path=accept_path,
                series_used=["XS1"],
            )
            self.assertEqual(clear.fee_admission, "ADMITTED_INDEX_ONLY")
            extras = [
                "note " + SYNTH_PREFIX.upper() + "\n",
                "note " + SYNTH_PREFIX[:4] + "\u200b" + SYNTH_PREFIX[4:] + "\n",
                "note " + SYNTH_PREFIX[:7] + "\n",
                "see " + WATCHED_FILES[0] + "\n",
            ]
            for extra in extras:
                index_path.write_text(base + extra, encoding="utf-8")
                blocked = admit_fee_source_v2(
                    fee_source_path=fee_path,
                    fee_source_id="FEE_SOURCE_SYNTH_v2",
                    fee_source_sha256=fee_sha,
                    packet_index_path=index_path,
                    fee_accept_path=accept_path,
                    series_used=["XS1"],
                )
                self.assertEqual(blocked.fee_block_reason, "FEE_CITATIONS_CHANGED", extra)
                self.assertTrue(_no_fee_numbers(blocked.public_dict()))

    def test_tampered_pin_bytes_fail_closed(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = _copy_kit(root)
            fee_path, accept_path, index_path, fee_sha = _repin(
                root,
                json.loads(paths[0].read_bytes()),
            )
            original = (LAB / "card01_amc" / "fee_citation_set.json").read_bytes()
            flipped = bytearray(original)
            flipped[0] ^= 0x01
            pin_path = root / "fee_citation_set.json"
            pin_path.write_bytes(bytes(flipped))
            saved = fee_admission._CITATION_PATH
            fee_admission._CITATION_PATH = pin_path
            self.addCleanup(lambda: setattr(fee_admission, "_CITATION_PATH", saved))
            self.assertEqual(
                fee_admission.FEE_CITATION_SET_SHA256,
                sha256_bytes(original),
            )
            blocked = admit_fee_source_v2(
                fee_source_path=fee_path,
                fee_source_id="FEE_SOURCE_SYNTH_v2",
                fee_source_sha256=fee_sha,
                packet_index_path=index_path,
                fee_accept_path=accept_path,
                series_used=["XS1"],
            )
            self.assertEqual(blocked.fee_block_reason, "FEE_CITATIONS_CHANGED")
            self.assertTrue(_no_fee_numbers(blocked.public_dict()))

    def _admit_synth_index(self, extra):
        import tempfile

        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        paths = _copy_kit(root)
        index_path = paths[2]
        index_path.write_text(index_path.read_text(encoding="utf-8") + extra, encoding="utf-8")
        digest = sha256_bytes(paths[0].read_bytes())
        return admit_fee_source_v2(
            fee_source_path=paths[0],
            fee_source_id="FEE_SOURCE_SYNTH_v2",
            fee_source_sha256=digest,
            packet_index_path=index_path,
            fee_accept_path=paths[1],
            series_used=["XS1"],
        )

    def test_r1_withdraw_citing_69b98b2f_blocks(self):
        calm = self._admit_synth_index(
            "| `notes/r1-context.md` (background on 69b98b2f only) | `" + ("ab" * 32) + "` |\n"
        )
        self.assertEqual(calm.fee_admission, "ADMITTED_INDEX_ONLY")
        narrative = self._admit_synth_index(
            "| `notes/r1-context.md` (superseded by 0123abcd under 69b98b2f) | `" + ("cd" * 32) + "` |\n"
        )
        self.assertEqual(narrative.fee_admission, "ADMITTED_INDEX_ONLY")
        blocked = self._admit_synth_index(
            "| `notes/r1-status.md` (WITHDRAWN 69b98b2f) | `" + ("ef" * 32) + "` |\n"
        )
        self.assertEqual(blocked.fee_admission, "BLOCKED_FEE_UNVERIFIED")
        self.assertEqual(blocked.fee_block_reason, "ACCEPT_69B98B2F_WITHDRAWN")
        self.assertTrue(_no_fee_numbers(blocked.public_dict()))

    def test_r1_revoke_citing_69b98b2f_blocks(self):
        blocked = self._admit_synth_index(
            "| `notes/r1-status.md` (**REVOKED** 69b98b2f) | `" + ("11" * 32) + "` |\n"
        )
        self.assertEqual(blocked.fee_admission, "BLOCKED_FEE_UNVERIFIED")
        self.assertEqual(blocked.fee_block_reason, "ACCEPT_69B98B2F_WITHDRAWN")
        self.assertTrue(_no_fee_numbers(blocked.public_dict()))

    def test_r1_supersede_packet_citing_69b98b2f_blocks(self):
        blocked = self._admit_synth_index(
            "| `packets/SUPERSEDE_note.md` (cites 69b98b2f) | `" + ("22" * 32) + "` |\n"
        )
        self.assertEqual(blocked.fee_admission, "BLOCKED_FEE_UNVERIFIED")
        self.assertEqual(blocked.fee_block_reason, "ACCEPT_69B98B2F_WITHDRAWN")
        self.assertTrue(_no_fee_numbers(blocked.public_dict()))


class RealCitationTests(unittest.TestCase):
    def _root(self):
        real = os.environ.get("CARD01_R1_REAL_FEE_DIR")
        if not real:
            self.skipTest("CARD01_R1_REAL_FEE_DIR is unset")
        root = Path(real)
        needed = ("fee.json", "accept.json", "PACKET_INDEX.md")
        if any(not (root / name).is_file() for name in needed):
            self.skipTest("runtime fee index is absent")
        return root

    def _admit(self, root, index_path):
        pins = json.loads((LAB / "PINS.json").read_text())["fee_source_v2"]
        return admit_fee_source_v2(
            fee_source_path=root / "fee.json",
            fee_source_id=pins["id"],
            fee_source_sha256=pins["sha256"],
            packet_index_path=index_path,
            fee_accept_path=root / "accept.json",
            series_used=["KXHOUSERACE"],
        )

    def test_real_withdraw_and_checklist_rows_block(self):
        import tempfile

        root = self._root()
        index_path = root / "PACKET_INDEX.md"
        text = index_path.read_text(encoding="utf-8")
        self.assertEqual(
            sha256_bytes(text.encode("utf-8")),
            "4a1ceb4b036b45914d5c0a0b7f6eeac9efb208f7792f99423acbeaf852587dfe",
        )
        admitted = self._admit(root, index_path)
        self.assertEqual(admitted.fee_admission, "ADMITTED_INDEX_ONLY")
        lines = text.splitlines()
        newline = "\n" if text.endswith("\n") else ""
        swapped = list(lines)
        pin = json.loads((LAB / "card01_amc" / "fee_citation_set.json").read_text())
        citing = [
            i
            for i, line in enumerate(lines)
            if fee_admission._line_cites(
                fee_admission._citation_fold(line.rstrip()),
                pin["watched_sha8"],
                pin["watched_files"],
            )
        ]
        self.assertEqual(len(citing), 26)
        swapped[citing[0]], swapped[citing[-1]] = swapped[citing[-1]], swapped[citing[0]]
        with tempfile.TemporaryDirectory() as tmp:
            tmp_index = Path(tmp) / "PACKET_INDEX.md"
            tmp_index.write_text("\n".join(swapped) + newline, encoding="utf-8")
            reordered = self._admit(root, tmp_index)
            self.assertEqual(reordered.fee_admission, "ADMITTED_INDEX_ONLY")
            withdraw = (
                text
                + "| `packets/CONDUCTOR_WITHDRAW_X.json` "
                + "(Conductor WITHDRAW of amendment 2c870cd5) | `"
                + ("cd" * 32)
                + "` |\n"
            )
            tmp_index.write_text(withdraw, encoding="utf-8")
            blocked = self._admit(root, tmp_index)
            self.assertEqual(blocked.fee_admission, "BLOCKED_FEE_UNVERIFIED")
            self.assertEqual(blocked.fee_block_reason, "FEE_CITATIONS_CHANGED")
            edited = list(lines)
            edited[1263] = edited[1263] + " — WITHDRAWN"
            tmp_index.write_text("\n".join(edited) + newline, encoding="utf-8")
            edited_block = self._admit(root, tmp_index)
            self.assertEqual(edited_block.fee_block_reason, "FEE_CITATIONS_CHANGED")
            appended = text + (
                "Conductor WITHDRAW of 69b98b2f §2: BINDING under 2c870cd5 (a)–(d)\n"
            )
            tmp_index.write_text(appended, encoding="utf-8")
            text_block = self._admit(root, tmp_index)
            self.assertEqual(text_block.fee_block_reason, "FEE_CITATIONS_CHANGED")


if __name__ == "__main__":
    unittest.main()
