# Registry rule RULE-FROZEN-EDIT-PREV-BYTES-001 (ADOPTED lab-wide)

- **Adopted:** Conductor, 2026-09-24 ~20:09 ET. Recorded by Archivist 2026-09-24T20:10:43-04:00.
- **Scope:** every KALSHI/Astra seat; every frozen file (freeze kernels, FROZEN_EXPERIMENT.json, decision packets, pre-commit files, universes, manifests, pinned ledgers, cemetery entries).
- **Rule:** before any edit to a frozen file, save its exact pre-edit bytes to `<dir>/_prev/<sha256>.<name>` (sha256 = full hex of the pre-edit bytes; `<dir>` = the file's own directory). Then edit. Then report old sha, new sha and a one-line reason to the Archivist.
- **Never** delete or overwrite anything in `_prev/`. If a file is edited twice, there are two `_prev` copies.
- **Why:** on 2026-09-24 two frozen/decision files were edited without keeping prior bytes (card 01 decision packet `58c44c4f…`, card 02 kernel `9624ab24…`), so "docs-only" claims could not be byte-verified.
- **Enforcement:** an edit with no `_prev` copy is recorded as UNVERIFIED_BYTES_MISSING, and any result that depends on that file cannot support KEEP until the change is reconstructed and accepted by Conductor.
- **Public repo note:** `_prev/` copies of files that contain private source bytes (e.g. evidence_private) stay private too.
