# Card01 NH-002-H Amendment C lab

Pre-outcome scoring code for the House-only prospective freeze. This tree does not
contain real 2026 prices, real outcomes, Kalshi responses, or ElectIndex captures.
It does not place orders. `results` and `pnl` stay null.

## Lineage

| Artifact | sha256 |
|---|---|
| Base freeze | `c31724463d81747702910a2d5296c2fc21d2a1dbc594727b26ac3d894b55ec59` |
| Amendment A | `4e36d0db5728148d5bb4688fd8626eca9907a8933747f85e0bc17ede0ac0936b` |
| Amendment B | `ee6af37cef95f1e468d28e5b06750caaca8b1706ec11ed5cf5cdce460524c2c6` |
| Conductor ACCEPT of B | `74c5d49c0452ce97def7b36129ba362ebc4387627b93d5611bb67c5f8dfcbd23` |
| Adversary review of B (AF-1..AF-11) | `271ec099481ca35a57e4605b28abeff78d2660b6fd2657044666d45bcb728f01` |
| Amendment C | `cc75f09614ad285756fd7cb7f7a5c2ce4e711b5adb98102c2dd043ccfc1af0f0` |
| Conductor ACCEPT of C | `2225c3fa0bea7c58cad59f52476f9fbe69e1d6fa813114a7557c748126dd2b1a` |
| Bootstrap-pin note | `fb4e5bc09af19971d67d479a67e387f61599294cd5fce3b64ca1518f4057b626` / `0c0992b19d1cc1f04c228871f84ff343d6c51f18ab89f6090af8843381b8cf5d` |
| Conductor ruling (degenerate block) | `86baa504c639a74c22db72821ac0c09cdf63cb7aaf8941e74012b14dac3bb256` |
| Pinned script (unchanged) | `049368f942741ff4a63acad328a49ff256252587d6c65f1e7e6d65d6101781f2` |
| Universe | `d8af74515e449b151016105f956c5e54a4fb4eac3ec570364da58f8fe47d8ca6` |

Vendored copies live in `pins/`. `PINS.json` records the sha of each pin and of
each module under `card01_amc/`.

## What this lab implements

- AF-8 input builder (`card01_amc/build_rows.py`): 92 rows in universe order,
  `state` = universe code `[:2]` (USPS2), no drops, outcome keys refused.
- AF-8 / AF-4 entry gate (`card01_amc/entry_gate.py`): no signal list unless an
  ADOPTED Archivist manifest has `series_endpoint` entries. There is no `0.07`
  path.
- AF-7 outcome-free swing stress (`card01_amc/swing_stress.py`): grid ±0.5, ±0.25,
  0 plus informational ±1.0. Fragility is read from ±0.5 only.
- Scorer (`card01_amc/score.py`): Amendment B keys reproduced from the pinned
  script, plus AF-5 `n_boundary_resamples` (same resample loop), AF-11
  `python_version` / `platform`, P8 provenance strings, P7 leave-one-state-out
  point estimates, and `headline_status`.
- Examiner aid (`card01_amc/verdict.py`): C1 / C5 / degenerate-block rules. It is
  not wired into the scorer's numbers.
- Post-settlement join (`card01_amc/join_outcomes.py`): sets `y` from synthetic
  settled results without reordering.

## Fee formula

Commit `22371178cb2663250b4762f328069571c48cb551` is present. Its feebook
`order_fee(role, contracts, price, ...)` does not map
`(fee_type, fee_multiplier, price)` to a per-contract taker fee. The admissible
gate path therefore returns `BLOCKED_FEE_UNVERIFIED` with reason
`FEE_FORMULA_NOT_PINNED` and `signals: null`. Tests may inject a fee function.
The command-line gate cannot.

## How to run

From this directory, CPython 3.12 or 3.13, standard library only:

```bash
python3 -m unittest discover -s tests -v
python3 -m card01_amc.build_rows pins/UNIVERSE_2026_HOUSE_FROZEN.json forecast.json mapping.json book.json
python3 -m card01_amc.entry_gate built_rows.json manifest.json
python3 -m card01_amc.swing_stress --rows built_rows.json --gate gate.json
python3 -m card01_amc.score rows_with_outcomes.json
python3 -m card01_amc.join_outcomes built_rows.json settled.json
python3 -m card01_amc.verdict score.json
```

The two full self-test reproductions each rerun 10,000 state-cluster resamples
on the synthetic 92-row input. They take on the order of a few minutes together.

`swing_stress` writes JSON whose `output_sha256` is the sha256 of
`json.dumps(obj_without_that_key, indent=1)` encoded as UTF-8. No
`computed_at_utc` field is emitted. The Examiner records hashing time separately.

## Verified unit results

`python3 -m unittest discover -s tests -v` from this directory: Ran 35 tests in 157.262s at 2026-10-04T00:27:46Z. Result: OK. Failures: 0. Errors: 0. Skipped: 0.

Both self-test reproductions matched sha256 `0e93e153b7fc03cb996f3200dc576dd770ad638b00a1a0e3ed1e28632b682f23`: the pinned script's stdout, and the scorer projection after deleting the added keys.

Interpreter: `3.12.3 (main, Mar 23 2026, 19:04:32) [GCC 13.3.0]`. Platform: `Linux-6.12.94+-x86_64-with-glibc2.39`. CPython 3.13 was not installed on this machine. The byte match still held.

This run is code verification on synthetic inputs. It is not an Examiner score. `results`, `pnl`, and `roi` stay null.

## Limits

- Pre-outcome. No real data run. No Kalshi call. No ElectIndex fetch.
- Script `049368f9` is vendored byte-for-byte and is not edited.
- `UNSTABLE_SPLIT`, the R4 district split, and secondary metrics (log loss,
  calibration, adverse selection, top-1 share) are out of scope.
- A raw Kalshi orderbook adapter is not in this tree. The builder consumes the
  normalized snapshot named in the lab spec.
- While the fee formula is unpinned, no net figure and no gate selection are
  produced on the production path.
- `INCONCLUSIVE_DEGENERATE_BLOCK` is a headline status for 0 scored races or
  fewer than 2 states. It is not a PASS and not a REJECT. The verdict helper
  checks it before REJECT (a) / REJECT (b).
- Adversary verification is required before the decision snapshot
  `2026-11-02T22:00Z`. This lab does not merge itself.

## Decisions recorded with the spec

These are fixed here so the code does not invent a second reading later.

- Built rows include `series` (mapping series, or null). The gate uses it to
  require an adopted series-endpoint entry. AF-4 cannot see the series from
  `mapping_status` alone when the series is legacy.
- An exclusion nulls both `p_market` and `p_model`. Raw quote fields stay when a
  snapshot was selected. Priority is `mapping_unresolved`,
  `no_admissible_forecast`, `snapshot_outside_window`,
  `market_closed_or_settled`, `no_two_sided_book`.
- `no_two_sided_book` covers a missing side, a crossed book (`bid > ask`),
  `bid <= 0`, and `ask >= 1`.
- A snapshot is tradable only when `market_status` is `active` or `open`.
- `dem_prob` must be a finite number in `[0, 100]`. `dem_name` equal to
  `(No Democrat)` is `no_admissible_forecast`.
- Gate JSON that is `OK` also carries `manifest_status` and `adopted_entry_ids`.
  Swing-stress emits a numeric `expected_net` only when those show an ADOPTED
  manifest and every signal fee is numeric with `fee_source` in that id list.
- `leave_one_state_out.by_state[s]` is either per-arm point estimates or the
  string `UNDEFINED`. Min and max ignore undefined remainders.
- `n_boundary_resamples` is a sibling of `arms` on each non-empty block.
- A reporting defect emits `rows: null`. It does not emit
  `NOT_FRAGILE_AT_PM0.5`.
- Conflicting settled results for one ticker leave `y` unchanged.
- `PINS.json` marks every listed file that is present, including the authored
  `card01_amc` modules, with `vendored: true`. The pin test treats
  `vendored: false` as "this path must not exist" (an unavailable attachment).
  All twenty code pins were present, so none are recorded that way. The file
  does not list its own sha256.
