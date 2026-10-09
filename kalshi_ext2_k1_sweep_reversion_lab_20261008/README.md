# EXT2-K1 sweep reversion

Price-pressure reversion after large sweeps, both sides, on the reused 31-game development cohort. This directory is the implementation and the synthetic tests. It is pre-outcome. Synthetic tests only. No results.

The runner writes a verdict-table evaluation. That evaluation is not an Examiner score. The verdict domain is `KILL_EXT2K1`, `CLOSE_NULL`, `ITERATE_DESCRIPTIVE`, `INCONCLUSIVE`, and `INCONCLUSIVE(STRUCTURE)`. `ITERATE_DESCRIPTIVE` means gross mid reversion. It has no promote path and no Refiner pass. `results`, `pnl`, and `roi` stay null. `counts_toward_keep`, `promote`, `live_promotion`, and `feeds_gate` stay false.

## Data plan

The public inputs are already on main and are pinned in `SOURCE_PINS.json`. This lab does not add a new copy. The box is the only place that reads those inputs and the only place that writes the real receipt, sweeps, and results. Real outputs stay outside this repo. The cloud suite hashes the pinned bytes and does not decompress the tape. Tests that need the real tape are skipped unless `EXT2K1_REAL_DATA=1`.

No exchange calls. No live orders. The fee stays `BLOCKED_FEE_UNVERIFIED`. The KXNFLGAME fee source is a separate later card.

## CLI

From this directory:

```
python -m ext2k1 receipt --out-dir DIR
python -m ext2k1 score --receipt DIR/RECEIPT.json --receipt-sha256 HEX --out-dir DIR
```

`DIR` must not sit inside a checkout. There is no option for an input path, a pins path, or an override.

## Box order

1. Check out the PR head and run the full test suite, including `EXT2K1_REAL_DATA=1`, so T01–T13 are green.
2. Run `receipt`. The Archivist files `RECEIPT.json` with its sha before any mid.
3. Run `score` once, with the filed receipt sha.
4. Adversary pre-score review before the Examiner.

The cloud never executes that order.

## Kit defaults

KD-1 through KD-21 are implemented as written, except KD-20, which is amended pending Conductor ratification: a rebuilt sweeps sha that differs from the filed receipt writes `INCONCLUSIVE` / V1 / `SWEEPS_SHA_MISMATCH` (rc 0, no statistics) instead of refusing, and a malformed timestamp writes `INCONCLUSIVE(STRUCTURE)` / V1s / `STRUCTURE_TIMESTAMP_MALFORMED` before the sweeps-sha check. KD-5, KD-6, KD-7, and KD-19 are frozen at the kit values (Conductor addendum 2026-10-09). The other defaults remain pending Conductor confirmation.

KD-21 logs one reporting defect on every receipt and every results object: `FREEZE_R2_CHANGELOG_OMITS_FIVE_WORDING_CHANGES`. It is non-blocking and does not change the verdict.

## Governing identities

- Freeze markdown `8f35fa77cab5872f7956df34c145fda2e8ae5587e1c1396ca2d39b5e347676a9` (not vendored)
- Freeze JSON `afbcd089888c84fb5db4e611b1e58ef59a558d4b379c843bae68c82a386ed8af` (not vendored)
- Conductor ACCEPT `d3ddc2ca50db07f36142acce38add4153beeba2c466cfdebba647671049abf21` (vendored under `pins/`)
