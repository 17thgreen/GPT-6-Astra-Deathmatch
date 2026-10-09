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

    def _assert_r1_set_changed(self, extra):
        blocked = self._admit_synth_index(extra)
        self.assertEqual(blocked.fee_admission, "BLOCKED_FEE_UNVERIFIED", extra)
        self.assertEqual(blocked.fee_block_reason, "ACCEPT_69B98B2F_CITATIONS_CHANGED", extra)
        self.assertEqual(blocked.fee_block_detail, "R1_ACCEPT_CITATION_SET", extra)
        self.assertEqual(blocked.amendment_check_failed, "b", extra)
        self.assertTrue(_no_fee_numbers(blocked.public_dict()))

    def _assert_r1_word_blocks(self, text):
        self.assertEqual(
            fee_admission._r1_accept_block_reason(text),
            "ACCEPT_69B98B2F_WITHDRAWN",
            text,
        )

    def _assert_r1_word_open(self, text):
        self.assertIsNone(fee_admission._r1_accept_block_reason(text), text)

    def test_r1_withdraw_citing_69b98b2f_blocks(self):
        calm = "| `notes/r1-context.md` (background on 69b98b2f only) | `" + ("ab" * 32) + "` |\n"
        narrative = (
            "| `notes/r1-context.md` (superseded by 0123abcd under 69b98b2f) | `"
            + ("cd" * 32)
            + "` |\n"
        )
        withdrawn = "| `notes/r1-status.md` (WITHDRAWN 69b98b2f) | `" + ("ef" * 32) + "` |\n"
        self._assert_r1_word_open(calm)
        self._assert_r1_word_open(narrative)
        self._assert_r1_word_blocks(withdrawn)
        for extra in (calm, narrative, withdrawn):
            self._assert_r1_set_changed(extra)

    def test_r1_revoke_citing_69b98b2f_blocks(self):
        extra = "| `notes/r1-status.md` (**REVOKED** 69b98b2f) | `" + ("11" * 32) + "` |\n"
        self._assert_r1_word_blocks(extra)
        self._assert_r1_set_changed(extra)

    def test_r1_supersede_packet_citing_69b98b2f_blocks(self):
        extra = "| `packets/SUPERSEDE_note.md` (cites 69b98b2f) | `" + ("22" * 32) + "` |\n"
        self._assert_r1_word_blocks(extra)
        self._assert_r1_set_changed(extra)

    def test_r1_actor_lines_admit(self):
        """Actor forms stay open at the word rule. Any new citing line changes the set."""
        sha = "ab" * 32
        forms = [
            "| `registry/other.md` (**ACCEPTED by 69b98b2fabcdef**; r1/r2 superseded) | `" + sha + "` |\n",
            "| notes/other.md | **ACCEPTED by 69b98b2fabcdef**; r1/r2 superseded | other |\n",
            "STATUS **ACCEPTED as modified by 69b98b2f** r1/r2 **SUPERSEDED**\n",
            "| `notes/actor.md` (SUPERSEDED_BY 69b98b2fabcdef) | `" + ("cd" * 32) + "` |\n",
            "| `notes/actor.md` (superseded by 69b98b2f) | `" + ("ef" * 32) + "` |\n",
            "| `notes/calm.md` (not withdrawn 69b98b2f) | `" + ("12" * 32) + "` |\n",
            "| `packets/69b98b2f-note.md` (r1/r2 superseded) | `" + ("34" * 32) + "` |\n",
        ]
        for extra in forms:
            self._assert_r1_word_open(extra)
            self._assert_r1_set_changed(extra)

    def test_r1_object_and_subject_forms_block(self):
        forms = [
            "| `notes/status.md` (69b98b2f WITHDRAWN) | `" + ("11" * 32) + "` |\n",
            "| `notes/status.md` (WITHDRAW of 69b98b2f) | `" + ("22" * 32) + "` |\n",
            "| `notes/status.md` (revokes 69b98b2f) | `" + ("33" * 32) + "` |\n",
            "| `notes/status.md` (69b98b2f superseded by abcd1234) | `" + ("44" * 32) + "` |\n",
            "| `notes/status.md` (withdrawal of 69b98b2f) | `" + ("55" * 32) + "` |\n",
            "| `notes/status.md` (revocation of 69b98b2f) | `" + ("66" * 32) + "` |\n",
            "| `notes/status.md` (rescission of 69b98b2f) | `" + ("77" * 32) + "` |\n",
            "| `notes/status.md` (rescinds 69b98b2f) | `" + ("88" * 32) + "` |\n",
            "| `notes/status.md` (supersedes 69b98b2f) | `" + ("99" * 32) + "` |\n",
            "| `notes/status.md` (69b98b2f retracted) | `" + ("a1" * 32) + "` |\n",
            "| `notes/status.md` (69b98b2f vacated) | `" + ("a2" * 32) + "` |\n",
            "| `notes/status.md` (69b98b2f no longer adopted) | `" + ("a3" * 32) + "` |\n",
            "| `notes/status.md` (69b98b2f withdrawn_by abcd1234) | `" + ("a4" * 32) + "` |\n",
            "| `notes/status.md` (69b98b2f REVOKED_BY abcd1234) | `" + ("a5" * 32) + "` |\n",
            "| `notes/status.md` (69b98b2f SUPERSEDED_BY abcd1234) | `" + ("a6" * 32) + "` |\n",
            "| `notes/69b98b2f-note.md` (**RETRACTED**) | `" + ("a7" * 32) + "` |\n",
            "| `packets/WITHDRAWAL_note.md` (cites 69b98b2f) | `" + ("a8" * 32) + "` |\n",
            "| `packets/REVOCATION_note.md` (cites 69b98b2f) | `" + ("a9" * 32) + "` |\n",
            "| `packets/RESCISSION_note.md` (cites 69b98b2f) | `" + ("b1" * 32) + "` |\n",
            "| `packets/69b98b2f.md` (**WITHDRAWN**) | `" + ("69b98b2f" + "ab" * 28) + "` |\n",
            "\n### 69b98b2f accept packet\nSTATUS: **WITHDRAWN**\n",
        ]
        for extra in forms:
            self._assert_r1_word_blocks(extra)
            self._assert_r1_set_changed(extra)

    def test_r1_accept_set_pin_shape_and_line_list_sha(self):
        raw = (LAB / "card01_amc" / "r1_accept_citation_set.json").read_bytes()
        self.assertEqual(sha256_bytes(raw), fee_admission.R1_ACCEPT_CITATION_SET_SHA256)
        self.assertEqual(
            fee_admission.R1_ACCEPT_CITATION_SET_SHA256,
            "8e26ac4e5db007ab671119379acdf0251f18b08f56ab00813cdd4e89401d4da3",
        )
        doc = json.loads(raw.decode("utf-8"))
        self.assertEqual(doc["watched_sha8"], ["69b98b2f"])
        self.assertEqual(len(doc["line_sha256"]), 18)
        self.assertEqual(doc["line_sha256"], sorted(doc["line_sha256"]))
        blob = "\n".join(doc["line_sha256"]) + "\n"
        self.assertEqual(
            sha256_bytes(blob.encode("utf-8")),
            "f0f7efb9f6c81879fcbf2d6ab3ecb77fbca0af58fd141dc7f739bd179d8859fd",
        )
        fee = json.loads((LAB / "card01_amc" / "fee_citation_set.json").read_text())
        self.assertEqual(len(set(doc["line_sha256"]) & set(fee["line_sha256"])), 4)
        self.assertEqual(doc["packet_index_sha256"], fee["packet_index_sha256"])

    def test_r1_accept_set_unmodified_kit_admits(self):
        admitted = self._admit_synth_index("")
        self.assertEqual(admitted.fee_admission, "ADMITTED_INDEX_ONLY")
        self.assertIsNone(fee_admission._r1_citation_block_reason(""))

    def test_r1_accept_set_appended_shapes_changed(self):
        cite = "69b98b2f"
        digest = "ab" * 32
        other = "0123abcd"
        shapes = {
            "a1": "| `notes/x.md` (Conductor withdrawal of ACCEPT " + cite + ") | `" + digest + "` |\n",
            "a2": "| `notes/x.md` (Conductor revokes ACCEPT " + cite + ") | `" + digest + "` |\n",
            "a3": "| `notes/x.md` (ruling " + other + " supersedes ACCEPT " + cite + ") | `" + digest + "` |\n",
            "a4": "| `notes/x.md` (rescission of ACCEPT " + cite + ") | `" + digest + "` |\n",
            "a5": "### Appended 2026-10-10 (Archivist): Conductor WITHDRAWS ACCEPT " + cite + "\n",
            "b": (
                "### Appended 2026-10-10 (Archivist): Conductor WITHDRAW ruling on ACCEPT "
                + cite
                + "\n\n| path | sha256 |\n|---|---|\n| `packets/CONDUCTOR_RULING_X.md` (Conductor ruling) | `"
                + digest
                + "` |\n\nRows and notes:\n- STATUS: R1 ACCEPT **WITHDRAWN**\n"
            ),
            "b2": "- STATUS: R1 ACCEPT `" + cite + "\u2026` **WITHDRAWN** (status only)\n",
            "c1": "- STATUS: " + cite + ": WITHDRAWN\n",
            "c2": "- STATUS: R1 ACCEPT `" + cite + "\u2026` **WITHDRAWN**\n",
            "d1": "| `notes/x.md` (background on " + cite + " only) | `" + digest + "` |\n",
            "d2": "- note: see " + cite + " §3\n",
            "d3": "- note: 69B98B2F\n",
            "d4": "- note: 69b9\u200b8b2f\n",
            "d5_accepted_by": (
                "| `notes/x.md` (**ACCEPTED by " + cite + "**; r1/r2 superseded) | `" + digest + "` |\n"
            ),
            "d5_superseded_by": (
                "| `notes/x.md` (SUPERSEDED_BY " + cite + ") | `" + digest + "` |\n"
            ),
        }
        for name, extra in shapes.items():
            with self.subTest(name=name):
                self._assert_r1_set_changed(extra)

    def test_r1_accept_set_residuals_are_not_cites(self):
        """A status with no hex, a 6-hex cite, and a split-hex cite are not this set."""
        residuals = {
            "r1": "- STATUS: R1 spec ACCEPT **WITHDRAWN**\n",
            "r2": "- STATUS: ACCEPT 69b98b WITHDRAWN\n",
            "r3": "- STATUS: ACCEPT 69b9 8b2f WITHDRAWN\n",
        }
        for name, extra in residuals.items():
            with self.subTest(name=name):
                self.assertIsNone(fee_admission._r1_citation_block_reason(extra))
                admitted = self._admit_synth_index(extra)
                self.assertEqual(admitted.fee_admission, "ADMITTED_INDEX_ONLY")
                self.assertIsNone(admitted.fee_block_reason)

    def _point_r1_pin(self, path):
        saved = fee_admission._R1_CITATION_PATH
        fee_admission._R1_CITATION_PATH = path
        self.addCleanup(lambda: setattr(fee_admission, "_R1_CITATION_PATH", saved))

    def test_r1_accept_set_pin_missing_blocks(self):
        import tempfile

        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self._point_r1_pin(Path(tmp.name) / "absent.json")
        self._assert_r1_set_changed("")

    def test_r1_accept_set_pin_byte_flip_blocks(self):
        import tempfile

        original = (LAB / "card01_amc" / "r1_accept_citation_set.json").read_bytes()
        flipped = bytearray(original)
        flipped[0] ^= 0x01
        with tempfile.TemporaryDirectory() as tmp:
            pin_path = Path(tmp) / "r1_accept_citation_set.json"
            pin_path.write_bytes(bytes(flipped))
            self._point_r1_pin(pin_path)
            self.assertEqual(
                fee_admission.R1_ACCEPT_CITATION_SET_SHA256,
                sha256_bytes(original),
            )
            self._assert_r1_set_changed("")

    def _mutated_r1_pin(self, mutate):
        import tempfile

        doc = json.loads((LAB / "card01_amc" / "r1_accept_citation_set.json").read_text())
        mutate(doc)
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        pin_path = Path(tmp.name) / "r1_accept_citation_set.json"
        pin_path.write_bytes(_pin_bytes(doc))
        self._point_r1_pin(pin_path)
        self.assertNotEqual(
            sha256_bytes(pin_path.read_bytes()),
            fee_admission.R1_ACCEPT_CITATION_SET_SHA256,
        )

    def test_r1_accept_set_pin_unsorted_blocks(self):
        def mutate(doc):
            doc["line_sha256"] = list(reversed(doc["line_sha256"]))

        self._mutated_r1_pin(mutate)
        self._assert_r1_set_changed("")

    def test_r1_accept_set_pin_empty_lines_blocks(self):
        def mutate(doc):
            doc["line_sha256"] = []

        self._mutated_r1_pin(mutate)
        self._assert_r1_set_changed("")

    def test_r1_accept_set_pin_watched_mismatch_blocks(self):
        def mutate(doc):
            doc["watched_sha8"] = ["0123abcd"]

        self._mutated_r1_pin(mutate)
        self._assert_r1_set_changed("")

    def test_r1_accept_set_reordered_nonciting_index_admits(self):
        """The synthetic kit cites none of 69b98b2f, so reordering it still admits.

        Citing-line reorder on an index that matches the pin is the real-dir
        pair (swap, reverse, and move-to-end). Those cases skip without the dir.
        """
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = _copy_kit(root)
            index_path = paths[2]
            text = index_path.read_text(encoding="utf-8")
            lines = text.splitlines()
            self.assertGreater(len(lines), 1)
            newline = "\n" if text.endswith("\n") else ""
            swapped = list(lines)
            swapped[0], swapped[-1] = swapped[-1], swapped[0]
            index_path.write_text("\n".join(reversed(swapped)) + newline, encoding="utf-8")
            digest = sha256_bytes(paths[0].read_bytes())
            admitted = admit_fee_source_v2(
                fee_source_path=paths[0],
                fee_source_id="FEE_SOURCE_SYNTH_v2",
                fee_source_sha256=digest,
                packet_index_path=index_path,
                fee_accept_path=paths[1],
                series_used=["XS1"],
            )
            self.assertEqual(admitted.fee_admission, "ADMITTED_INDEX_ONLY")

    def test_r1_accept_set_changed_blocks_downstream_without_numbers(self):
        import json as json_mod
        import tempfile

        from card01_amc import pnl_cd
        from card01_amc.entry_gate import gate_v2
        from card01_amc.regime_split_secondary import build_report
        from card01_amc.swing_stress import evaluate
        from card01_amc.verdict import apply_verdict
        from tests.test_fee_admission_v2 import ADMITTED_ID, FEE_FORMULA_ID, _row
        from tests.test_regime_split_secondary import _selection
        from tests.test_v2_consumers import _score

        with tempfile.TemporaryDirectory() as tmp:
            paths = _copy_kit(Path(tmp))
            digest = sha256_bytes(paths[0].read_bytes())
            prior = gate_v2(
                [_row()],
                fee_source_path=paths[0],
                fee_source_id=ADMITTED_ID,
                fee_source_sha256=digest,
                packet_index_path=paths[2],
                fee_accept_path=paths[1],
            )
            self.assertEqual(prior["status"], "OK")
            paths[2].write_text(
                paths[2].read_text(encoding="utf-8")
                + "| `notes/x.md` (background on 69b98b2f only) | `"
                + ("ab" * 32)
                + "` |\n",
                encoding="utf-8",
            )
            reason = "ACCEPT_69B98B2F_CITATIONS_CHANGED"
            gated = gate_v2(
                [_row()],
                fee_source_path=paths[0],
                fee_source_id=ADMITTED_ID,
                fee_source_sha256=digest,
                packet_index_path=paths[2],
                fee_accept_path=paths[1],
            )
            self.assertEqual(gated["status"], "BLOCKED_FEE_UNVERIFIED")
            self.assertEqual(gated["fee_block_reason"], reason)
            self.assertEqual(gated["fee_block_detail"], "R1_ACCEPT_CITATION_SET")
            self.assertIsNone(gated["signals"])
            self.assertTrue(_no_fee_numbers(gated))
            swing = evaluate(
                [_row()],
                prior,
                "r",
                "g",
                "g",
                fee_source_path=paths[0],
                packet_index_path=paths[2],
                fee_accept_path=paths[1],
                fee_source_expected_id=ADMITTED_ID,
                fee_source_expected_sha256=digest,
                fee_source_expected_accept=prior["fee_source_accept_sha256"],
                fee_source_expected_formula=FEE_FORMULA_ID,
            )
            self.assertEqual(swing["stress_status"], "BLOCKED_FEE_UNVERIFIED")
            self.assertIsNone(swing["rows"])
            self.assertEqual(swing["fee_block_reason"], reason)
            self.assertTrue(_no_fee_numbers(swing))
            report = build_report(
                [_row()],
                selection=_selection(),
                gate=prior,
                fee_source_path=paths[0],
                fee_source_id=ADMITTED_ID,
                fee_source_sha256=digest,
                packet_index_path=paths[2],
                fee_accept_path=paths[1],
                series_used=["XS1"],
            )
            self.assertEqual(report["fee_state"], "BLOCKED_FEE_UNVERIFIED")
            self.assertEqual(report["secondary"]["fee_block_reason"], reason)
            self.assertIsNone(report["fee_views"])
            self.assertNotIn("fee_headline", json_mod.dumps(report))
            verdict = apply_verdict(
                _score(),
                gate=prior,
                regime_report=report,
                cd={"n_signals": 1, "reject_c": False, "reject_d": False},
            )
            self.assertEqual(verdict["fee_block_reason"], reason)
            self.assertNotIn("fee_headline", json_mod.dumps(verdict))
            book = pnl_cd.entry_book(
                gated,
                fee_ctx={
                    "fee_source_path": paths[0],
                    "packet_index_path": paths[2],
                    "fee_accept_path": paths[1],
                },
            )
            self.assertEqual(book["status"], "BLOCKED_FEE_UNVERIFIED")
            self.assertIsNone(book["entry_table"]["signals"])
            self.assertNotIn("fee_headline", json_mod.dumps(book))
            self.assertNotIn("net_headline", json_mod.dumps(book))


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

    def _index_parts(self, root):
        text = (root / "PACKET_INDEX.md").read_text(encoding="utf-8")
        self.assertEqual(
            sha256_bytes(text.encode("utf-8")),
            "4a1ceb4b036b45914d5c0a0b7f6eeac9efb208f7792f99423acbeaf852587dfe",
        )
        lines = text.splitlines()
        newline = "\n" if text.endswith("\n") else ""
        fee = json.loads((LAB / "card01_amc" / "fee_citation_set.json").read_text())
        r1 = json.loads((LAB / "card01_amc" / "r1_accept_citation_set.json").read_text())
        r1_idx = []
        fee_idx = []
        for i, line in enumerate(lines):
            folded = fee_admission._citation_fold(line.rstrip())
            if fee_admission._line_cites(folded, r1["watched_sha8"], []):
                r1_idx.append(i)
            if fee_admission._line_cites(folded, fee["watched_sha8"], fee["watched_files"]):
                fee_idx.append(i)
        self.assertEqual(len(r1_idx), 18)
        overlap = [i for i in r1_idx if i in set(fee_idx)]
        only = [i for i in r1_idx if i not in set(fee_idx)]
        self.assertEqual(len(overlap), 4)
        self.assertEqual(len(only), 14)
        found = sorted(sha256_bytes(lines[i].rstrip().encode("utf-8")) for i in r1_idx)
        self.assertEqual(found, r1["line_sha256"])
        return lines, newline, r1_idx, overlap, only

    def _admit_lines(self, root, lines, newline):
        import tempfile

        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / "PACKET_INDEX.md"
        path.write_text("\n".join(lines) + newline, encoding="utf-8")
        return self._admit(root, path)

    def _changed(self, admission):
        self.assertEqual(admission.fee_admission, "BLOCKED_FEE_UNVERIFIED")
        self.assertEqual(admission.fee_block_reason, "ACCEPT_69B98B2F_CITATIONS_CHANGED")
        self.assertEqual(admission.fee_block_detail, "R1_ACCEPT_CITATION_SET")
        self.assertTrue(_no_fee_numbers(admission.public_dict()))

    def test_r0_real_pair_admits_with_pinned_fees(self):
        from decimal import Decimal

        from card01_amc.fee_admission import pinned_entry_v2
        from card01_amc.fee_source import pinned_taker_fee

        root = self._root()
        admitted = self._admit(root, root / "PACKET_INDEX.md")
        self.assertEqual(admitted.fee_admission, "ADMITTED_INDEX_ONLY")
        entry = pinned_entry_v2(admitted, "KXHOUSERACE")
        for price, headline in (
            (Decimal("0.055"), Decimal("0.005")),
            (Decimal("0.072"), Decimal("0.008")),
            (Decimal("0.077"), Decimal("0.013")),
        ):
            self.assertEqual(pinned_taker_fee(entry, price)["headline"], headline)

    def test_r1_swap_citing_lines_admits(self):
        root = self._root()
        lines, newline, citing, _overlap, _only = self._index_parts(root)
        swapped = list(lines)
        swapped[citing[0]], swapped[citing[-1]] = swapped[citing[-1]], swapped[citing[0]]
        admitted = self._admit_lines(root, swapped, newline)
        self.assertEqual(admitted.fee_admission, "ADMITTED_INDEX_ONLY")

    def test_r2_reverse_citing_lines_admits(self):
        root = self._root()
        lines, newline, citing, _overlap, _only = self._index_parts(root)
        reversed_lines = list(lines)
        for index, line in zip(citing, reversed([lines[i] for i in citing])):
            reversed_lines[index] = line
        admitted = self._admit_lines(root, reversed_lines, newline)
        self.assertEqual(admitted.fee_admission, "ADMITTED_INDEX_ONLY")

    def test_r3_move_citing_line_to_end_admits(self):
        root = self._root()
        lines, newline, citing, _overlap, _only = self._index_parts(root)
        moved = list(lines)
        line = moved.pop(citing[0])
        moved.append(line)
        admitted = self._admit_lines(root, moved, newline)
        self.assertEqual(admitted.fee_admission, "ADMITTED_INDEX_ONLY")

    def test_r4_trailing_spaces_on_citing_line_admit(self):
        root = self._root()
        lines, newline, citing, _overlap, _only = self._index_parts(root)
        spaced = list(lines)
        spaced[citing[0]] = lines[citing[0]] + "   "
        admitted = self._admit_lines(root, spaced, newline)
        self.assertEqual(admitted.fee_admission, "ADMITTED_INDEX_ONLY")

    def test_r5_crlf_index_admits(self):
        import tempfile

        root = self._root()
        lines, newline, _citing, _overlap, _only = self._index_parts(root)
        raw = ("\n".join(lines) + newline).replace("\n", "\r\n").encode("utf-8")
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / "PACKET_INDEX.md"
        path.write_bytes(raw)
        admitted = self._admit(root, path)
        self.assertEqual(admitted.fee_admission, "ADMITTED_INDEX_ONLY")

    def test_r6_duplicate_citing_line_changed(self):
        root = self._root()
        lines, newline, _citing, _overlap, only = self._index_parts(root)
        duplicated = list(lines)
        duplicated.append(lines[only[0]])
        self._changed(self._admit_lines(root, duplicated, newline))

    def test_r7_appended_section_a_shape_changed(self):
        root = self._root()
        lines, newline, _citing, _overlap, _only = self._index_parts(root)
        extra = (
            "| `notes/x.md` (Conductor withdrawal of ACCEPT 69b98b2f) | `"
            + ("ab" * 32)
            + "` |"
        )
        appended = list(lines)
        appended.append(extra)
        self._changed(self._admit_lines(root, appended, newline))

    def test_r8_edit_citing_line_changed(self):
        root = self._root()
        lines, newline, _citing, _overlap, only = self._index_parts(root)
        edited = list(lines)
        edited[only[0]] = self._one_char_edit(lines[only[0]])
        self._changed(self._admit_lines(root, edited, newline))

    def test_r9_zero_width_in_citing_line_changed(self):
        root = self._root()
        lines, newline, _citing, _overlap, only = self._index_parts(root)
        edited = list(lines)
        edited[only[0]] = lines[only[0]][:1] + "\u200b" + lines[only[0]][1:]
        self._changed(self._admit_lines(root, edited, newline))

    def test_r10_delete_non_fee_citing_line_changed(self):
        root = self._root()
        lines, newline, _citing, _overlap, only = self._index_parts(root)
        kept = [line for i, line in enumerate(lines) if i != only[0]]
        self._changed(self._admit_lines(root, kept, newline))

    def test_r11_delete_fee_overlap_citing_line_is_fee_changed(self):
        root = self._root()
        lines, newline, _citing, overlap, _only = self._index_parts(root)
        kept = [line for i, line in enumerate(lines) if i != overlap[0]]
        blocked = self._admit_lines(root, kept, newline)
        self.assertEqual(blocked.fee_block_reason, "FEE_CITATIONS_CHANGED")
        self.assertTrue(_no_fee_numbers(blocked.public_dict()))

    def test_r12_delete_all_citing_lines_is_fee_changed(self):
        root = self._root()
        lines, newline, citing, _overlap, _only = self._index_parts(root)
        drop = set(citing)
        kept = [line for i, line in enumerate(lines) if i not in drop]
        blocked = self._admit_lines(root, kept, newline)
        self.assertEqual(blocked.fee_block_reason, "FEE_CITATIONS_CHANGED")
        self.assertTrue(_no_fee_numbers(blocked.public_dict()))

    def test_r13_delete_non_overlap_citing_lines_changed(self):
        root = self._root()
        lines, newline, _citing, _overlap, only = self._index_parts(root)
        drop = set(only)
        kept = [line for i, line in enumerate(lines) if i not in drop]
        self._changed(self._admit_lines(root, kept, newline))

    def test_r14_own_row_description_withdrawn_changed(self):
        root = self._root()
        lines, newline, _citing, _overlap, only = self._index_parts(root)
        hits = []
        for index, line in enumerate(lines):
            match = fee_admission._ROW_RE.match(line.rstrip())
            if match is not None and match.group(3).startswith("69b98b2"):
                hits.append(index)
        self.assertGreaterEqual(len(hits), 1)
        for index in hits:
            with self.subTest(row=index):
                self.assertIn(index, only)
                match = fee_admission._ROW_RE.match(lines[index].rstrip())
                edited = list(lines)
                edited[index] = (
                    "| `" + match.group(1) + "` WITHDRAWN | `" + match.group(3) + "` |"
                )
                self._changed(self._admit_lines(root, edited, newline))

    def _one_char_edit(self, line):
        for pos in range(len(line) - 1, -1, -1):
            replacement = "X" if line[pos] != "X" else "Y"
            candidate = line[:pos] + replacement + line[pos + 1:]
            folded = fee_admission._citation_fold(candidate.rstrip())
            if not fee_admission._line_cites(folded, ["69b98b2f"], []):
                continue
            if sha256_bytes(candidate.rstrip().encode("utf-8")) == sha256_bytes(line.rstrip().encode("utf-8")):
                continue
            return candidate
        self.fail("citing line had no one-character edit")


if __name__ == "__main__":
    unittest.main()
