# RESERVED_HOLDOUT re-pin — 2026-09-24

**Recorded by:** The Archivist (Registry) · 2026-09-24T19:54:23-04:00 (ET)
**Authority:** Conductor registry item (1), 2026-09-24.
**Verification result: VERIFIED.** The diff between the original pinned bytes and the current bytes is exactly the PIT@CLE event ticker plus a trailing newline. Details below.
**Rules:** append-only. No freeze file was edited. The original pin stays in every freeze as written.

## Pins

| Role | sha256 | git blob | bytes |
|---|---|---|---|
| **ORIGINAL** (kept ON FILE; still cited by the freezes) | `74507e1a4371d69bc79ea2369f9bff030a74f51ee80c8072ba9c0f5345d377ca` | `3af85f2e0211a1e03efdea5990bb59b5345b77ca` | 7,446 |
| **CURRENT** (working tree, re-pinned 2026-09-24) | `f8f6b5773072e92b0babe3c10940ed52c71878caca104c4e072c6a6efcb63bbb` | `113d3292250d1570bd592db6408190f51f290d93` | 7,468 |

The original pin is **not superseded in the freezes** and is **not deleted**. It stays the ORIGINAL pin of record. The current pin is recorded alongside it as a dated re-pin.

## Where the original pin appears (freeze files not edited) [V]

| File (box) | Line | Text |
|---|---|---|
| `/workspace/lab/astra-science/nfl_factorial_lab_20260921/FROZEN_EXPERIMENT.json` (Q6; blob `06223859`, same as main) | 14 | `"RESERVED_HOLDOUT.json": "74507e1a4371d69bc79ea2369f9bff030a74f51ee80c8072ba9c0f5345d377ca",` |
| `/workspace/lab/astra-science/nfl_factorial_lab_20260921/SHADOW_CANDIDATE_FREEZE.json` (Q6 shadow freeze; blob `d7e2f54a`, same as main) | 15 | `"RESERVED_HOLDOUT.json": "74507e1a4371d69bc79ea2369f9bff030a74f51ee80c8072ba9c0f5345d377ca",` |
| `/workspace/lab/astra-science/nfl_factorial_lab_20260921/DELIVERY_MANIFEST.json` (Q6; blob `e985c533`, same as main) | 44–46 | `"path": "RESERVED_HOLDOUT.json", "bytes": 7446, "sha256": "74507e1a4371d69bc79ea2369f9bff030a74f51ee80c8072ba9c0f5345d377ca"` |
| `/workspace/lab/astra-science/nfl_paircheck_lab_20260922/FROZEN_EXPERIMENT.json` (Q7 paircheck; sha256 `b0dd9169…`, blob `1b1e160a`, same as main) | 175 | `"RESERVED_HOLDOUT.json": "74507e1a4371d69bc79ea2369f9bff030a74f51ee80c8072ba9c0f5345d377ca",` (in the Q6 pin set) |

Also cited at `packets/EXAMINER_HOLD_Q7_B_PASS2_TAPE_WALK_BYTES_2026-09-24.json` lines 929–937 (Examiner's own check of the same drift).

## Older copies with the original hash [V]

- **GitHub main (read-only):** `nfl_factorial_lab_20260921/RESERVED_HOLDOUT.json` is blob `3af85f2e`, size 7,446, at main `37ad5b7b366c10dcdf278c2325611e6f426a62c6`. The only commit touching the path on main is `7da067ada9faf255e672791975c8835959ead75b` (2026-09-21 14:11:33 ET, "Preserve Stern and NFL research through Q6 with verified results"). Main tree `34a27202` has the same blob at `nfl_adaptive_lab_20260921/` and `nfl_timing_lab_20260921/collector/`. The later PR51 (`eb4a4a94`, 19:52:59 ET) touched only the Q7 reconciliation packet [I from the Examiner/Conductor stamps: 3 files].
- **Local git objects:** in the `/workspace/lab/astra-science` clone, `HEAD:` is blob `3af85f2e` for all three paths. `git cat-file -p 3af85f2e` hashes to sha256 `74507e1a4371d69bc79ea2369f9bff030a74f51ee80c8072ba9c0f5345d377ca`.
- **Box file copies with sha256 `74507e1a4371d69bc79ea2369f9bff030a74f51ee80c8072ba9c0f5345d377ca`:** `/workspace/lab/tmp/ams_branch_ro/{nfl_factorial_lab_20260921,nfl_adaptive_lab_20260921,nfl_timing_lab_20260921/collector}/RESERVED_HOLDOUT.json`, and the same three paths under `/tmp/c1rj/repo/` and `/tmp/examiner_pr50_verify/` (read-only checkouts).
- **Box copies with the current sha256 `f8f6b5773072e92b0babe3c10940ed52c71878caca104c4e072c6a6efcb63bbb`:** the three `astra-science` working-tree paths, `/workspace/lab/astra-src/registry/RESERVED_HOLDOUT.json`, `/workspace/lab/astra-kits/recovered/NFL_Allocation_Factorial_Kit/RESERVED_HOLDOUT.json`, `/workspace/lab/astra-kits/recovered/NFL_Adaptive_Kit/RESERVED_HOLDOUT.json`.

## Diff (original blob 3af85f2e → current working tree) [V]

`git diff HEAD -- nfl_factorial_lab_20260921/RESERVED_HOLDOUT.json`: 2 hunks, 2 insertions, 2 deletions. The adaptive and timing copies show the same stat.

```
@@ -54,7 +54,7 @@   (game_id "2026_04_PIT_CLE", kickoff 2026-10-02T00:15:00+00:00, week 4, PIT at CLE)
-      "event": null
+      "event": "KXNFLGAME-26OCT01PITCLE"
@@ -304,4 +304,4 @@
-}
\ No newline at end of file
+}
```

**Byte-exact check:** take the original bytes and replace the single occurrence of `"away": "PIT",\n      "home": "CLE",\n      "event": null` with the same text ending `"event": "KXNFLGAME-26OCT01PITCLE"`. Append one `\n`. The result hashes to `f8f6b5773072e92b0babe3c10940ed52c71878caca104c4e072c6a6efcb63bbb` and is byte-equal to the current file.
- The size difference (+22 bytes: +21 for the ticker in place of `null`, +1 newline) agrees.
- No other field changed. The other 30 `"event": null` entries are untouched. No outcome, score or settlement field changed.

**Conclusion: the diff is exactly the PIT@CLE ticker plus a trailing newline. VERIFIED.**

## Explanation (Conductor) and timing [V]

- The ticker `KXNFLGAME-26OCT01PITCLE` was joined for `game_id` `2026_04_PIT_CLE` under registry `REG-PITCLE-HOLDOUT-ID-JOIN-20260923`.
  - Packet: `packets/PITCLE_HOLDOUT_IDENTITY_JOIN_HASH_FREEZE_2026-09-23.md` (sha256 `f5ca19f15940a80476d1590e506951df87df619160b477f1dff06cc3554cb520`).
  - It is indexed 2026-09-23T09:59:00-04:00 and records holdout sha256 `f8f6b5773072e92b0babe3c10940ed52c71878caca104c4e072c6a6efcb63bbb` after the join. The join receipt digest `72e6b1ed…` is a different file.
- **Predates Refiner P1** [V ordering]:
  - Join indexed 09:59 ET 2026-09-23.
  - Refiner P1 freeze accepted 14:51 ET (`packets/refiner/CONDUCTOR_ACCEPT_Q7_B_REHAB_P1_CADENCE_600_2026-09-23.json`).
  - PR38 merged 15:13 ET.
  - P1 SIMULATOR_READY stamped 17:29 ET (per the Examiner hold packet).
- The Examiner hold records that no module in the P1/P2 walk import closure reads `RESERVED_HOLDOUT.json`, and that PIT@CLE is not on the Q6 31-game development tape. The Archivist recorded this and did not re-derive it [I].

## What this does NOT do

- It does not edit `FROZEN_EXPERIMENT.json`, `SHADOW_CANDIDATE_FREEZE.json`, `DELIVERY_MANIFEST.json` or the paircheck freeze. Those still pin `74507e1a…` as ORIGINAL.
- It does not change any Q6, Q7, P1 or P2 result.
- It does not commit the working-tree holdout to main. Main still carries the original blob `3af85f2e`.
