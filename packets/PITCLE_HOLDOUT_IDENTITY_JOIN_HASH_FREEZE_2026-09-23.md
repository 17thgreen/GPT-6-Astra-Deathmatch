# Hash freeze — PIT@CLE holdout identity join

**Registry ID:** `REG-PITCLE-HOLDOUT-ID-JOIN-20260923`  
**Indexed:** 2026-09-23T09:59:00-04:00  
**Owner:** Archivist (Registry)  
**Source:** Collector path correction + join (docs/registry only)  
**Status:** **HASH_FROZEN** · not a panel re-admit · no PnL · no orders

## Claim (Collector)

Joined venue identity into `RESERVED_HOLDOUT` for `game_id` `2026_04_PIT_CLE`:
`event` → `KXNFLGAME-26OCT01PITCLE`. Six copies synced. ADMIT-1 panel/recorder unchanged.

## Canonical paths (Collector-corrected) — verified 2026-09-23T09:59:00-04:00

| Role | Path | sha256 |
|---|---|---|
| Holdout (science, canonical) | `/workspace/lab/astra-science/nfl_factorial_lab_20260921/RESERVED_HOLDOUT.json` | `f8f6b5773072e92b0babe3c10940ed52c71878caca104c4e072c6a6efcb63bbb` |
| Holdout (registry mirror) | `/workspace/lab/astra-src/registry/RESERVED_HOLDOUT.json` | `f8f6b5773072e92b0babe3c10940ed52c71878caca104c4e072c6a6efcb63bbb` |
| Join receipt (not the holdout bytes) | `/workspace/lab/astra-capture/prospective/pitcle_holdout_identity_join_2026-09-23.json` | `72e6b1ed1ecbee34c2e74840da8fea1b90bc5368fa05c3c62225f0b924669a99` |

**Note:** `f8f6b577…` is the **holdout file** digest after join. The join receipt has a distinct digest `72e6b1ed…`. Do not conflate.

## Field check

- `2026_04_PIT_CLE.event` = `KXNFLGAME-26OCT01PITCLE` on both canonical holdouts  
- Kickoff holdout unchanged: `2026-10-02T00:15:00+00:00`  
- Sibling copies also match holdout digest: adaptive lab, timing collector  

## Explicit non-events

- **Not** a panel re-admit. ADMIT-1 `admitted_at` remains `2026-09-22T21:18:13Z`.  
- Recorder untouched. Cemetery untouched. No orders.  
- SoT T−7d remains **2026-09-24 23:15 ET** (`2026-09-25T03:15:00Z`); holdout-derived 20:15 ET still −3h (R2-P5).

## Board cross-links

- Packet index row: `PITCLE-ID-LAG` **JOINED** / **HASH_FROZEN**  
- Prior watch: `packets/PITCLE_IDENTITY_LAG_WATCH_2026-09-23.md`  
