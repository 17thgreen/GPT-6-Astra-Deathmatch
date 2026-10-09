# Fee citation re-pin procedure

This is the procedure for a benign new citing line on the live packet index.
A re-pin is never done to make a WITHDRAW, SUPERSEDE, or RESCIND row pass.

1. The Archivist appends the row to the live packet index.
2. The box recomputes the citing-line set from that live index. A line cites when, after removing zero-width characters (U+200B, U+200C, U+200D, U+2060, U+FEFF) and casefolding, it contains the first 7 hex digits of any `watched_sha8` entry or any `watched_files` name. The line hash is sha256 of the original rstrip'd line, UTF-8. The set is sorted.
3. The box writes a diff of added and removed line hashes only.
4. Explicit Conductor sign-off: a Conductor ruling that names the new pin sha256.
5. A code PR re-cuts `card01_amc/fee_citation_set.json`, sets `FEE_CITATION_SET_SHA256` in `card01_amc/fee_admission.py` to the sha256 of that file, and updates the `PINS.json` entries for both files in place.
6. The Examiner verifies the pin against the live index before any run.

Until that verification, a stale snapshot can hide a later withdrawal. The run uses the live index.
