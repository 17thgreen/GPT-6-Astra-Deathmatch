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
| Builder dem_name ruling | `3bff01cd6e60779fd2081703d05a8ffc304c9f08f414c0827a984d474cf96f41` |
| Fee, Q6, and precedence ruling | `b8cb27e0e94c2a27c22fd1d92395109168a90ca78bb5928a65fbf0f89c397517` |
| Public-repo routing ruling | `b1c1851f3edfd04ad9d2d0c91fed17e86f6fd543ad0f489f4775d1540478017f` |
| Fee-source format spec | `488a443bfff2b91ca22e8546801448866269d6ad25a3dbdca4f9e0a068975072` |
| Fee-source template (vendored) | `13e9554277a6eeebef86c1191f9cbca6f4a5521cad875c649b99dc97d8fd3614` |
| Adopted fee source (runtime only) | `d4dc8e72ae2b2a72824487eb386d6684c451a5e3b2e9dce58c1a68aaea9436cd` |
| Conductor ACCEPT of that fee source | `5b2eb82613d74bbfb2dd937efa43e239083367f832430a46d011759ccf451b59` |
| Q6 forecast-file rule | `5535ff2a60223587bef9b9f3a0d981f01387ca57cf23e02a0bc2e6d991d6ac0c` |
| Decision packet (precedence) | `817e5dd0f9e2b7e903f318a15a4e65d7614b6a00da62b5bedde1eae53d4f6b19` |
| add_dem_name script (runtime only) | `19250333e6f5f1acaa80fd82fc7f02c01ed2de2101fb557165a04453a247036e` |
| run_daily (record only) | `4f0854e56265e10b2505a9f371260caa6eaddb57726244a4435e1a424a54d5c8` |

Code pins and the governance texts that do not carry private paths live in
`pins/`. `PINS.json` records the sha of each pin and of each module under
`card01_amc/`. Six earlier governance documents stay `vendored: false` with
reason `PUBLIC_REPO_REDACTION_PENDING_TOS_REGATE`. Follow-up 2 context
documents stay `vendored: false` with reason `PUBLIC_REPO_REDACTION`. The
adopted fee file is never committed. It is read at runtime from `--fee-source`.
The add_dem_name script is never committed. The builder runs it by path after
a sha check. Amendment B requires a Terms of Service §06 re-gate before
ElectIndex values are published.

## What this lab implements

- Q6 selector (`card01_amc/select_forecast.py`): strict no-step-back file
  selection. A non-`SELECTED` status gives the builder no forecast.
- AF-8 input builder (`card01_amc/build_rows.py`): 92 rows in universe order,
  `state` = universe code `[:2]` (USPS2), no drops, outcome keys refused.
  A selected forecast is accepted only when its sha matches the Q6 record and
  the runtime dem_name step passes.
- AF-8 / AF-4 entry gate (`card01_amc/entry_gate.py`): signals require an
  `ADOPTED` + `PINNED` `astra.fee_source.v1` file and a passing fee attestation.
  `ADOPTED` + `PINNED` alone does not admit the fee. There is no
  default-multiplier path. An unknown fee-source schema version fails closed.
- AF-7 outcome-free swing stress (`card01_amc/swing_stress.py`): grid ±0.5, ±0.25,
  0 plus informational ±1.0. Fragility is read from ±0.5 gross and sign flips
  only. Numeric nets require a matching gate sha and a recomputed headline fee.
- Scorer (`card01_amc/score.py`): Amendment B keys reproduced from the pinned
  script, plus AF-5 `n_boundary_resamples` (same resample loop), AF-11
  `python_version` / `platform`, P8 provenance strings, P7 leave-one-state-out
  point estimates, and `headline_status`.
- Examiner aid (`card01_amc/verdict.py`): validity, then the degenerate block,
  then REJECT (a)/(b), then the fee branch. It is not wired into the scorer's
  numbers. Realized P&L for (c)/(d) is supplied by the caller.
- Post-settlement join (`card01_amc/join_outcomes.py`): sets `y` from synthetic
  settled results without reordering.

## Fee formula

The taker formula is pinned inside `pinned_taker_fee`: round up
`M × rate × C × P × (1−P)` to six decimal dollars. The headline is
`ceil_cent(P × C + fee_raw) − P × C` on the one-cent grid. `FEE_ONLY_CEIL` is
`ceil_cent(fee_raw)`. It is a labeled sensitivity-only row. It is not the
headline and it does not drive the verdict. The headline can be lower than
`FEE_ONLY_CEIL` when `P × C` is off a whole cent. The direct one-ten-thousandth figure is a
second sensitivity row. `M` and `fee_type` come only from a `PINNED` series
entry. Any series in use that is not `PINNED` blocks the whole card. No fee
is computed in that case, and there is no default-multiplier row.

The adopted file id is `FEE_SOURCE_CARD01_v1`, sha256
`d4dc8e72ae2b2a72824487eb386d6684c451a5e3b2e9dce58c1a68aaea9436cd`, accepted by
`5b2eb82613d74bbfb2dd937efa43e239083367f832430a46d011759ccf451b59`. Ruling
`715fbafd` records that examiner attestation as `ATTEST_FAIL`. The command
line loads the fee file from `--fee-source` and an attestation from
`--fee-attest`. The adopted file is not embedded. The fee stays `BLOCKED`
until an `ATTEST_PASS` attestation is supplied. Without that attestation the
gate stays `BLOCKED_FEE_UNVERIFIED` and money rows stay forecast-only. A fee
file whose bytes are not that adopted sha, including a future
`astra.fee_source.v2` document, is rejected as `FEE_SOURCE_SHA_MISMATCH`
before the version check runs, so it is still blocked. Commit
`22371178cb2663250b4762f328069571c48cb551` remains in the pin list with
`superseded: true`. Its feebook does not price this gate.

## How to run

From this directory, CPython 3.12 or 3.13, standard library only:

```bash
python3 -m unittest discover -s tests -v
python3 -m card01_amc.select_forecast --capture-log LOG --daily-runs RUNS --root ROOT --run-at-utc T
python3 -m card01_amc.build_rows --universe pins/UNIVERSE_2026_HOUSE_FROZEN.json --selection SEL.json --forecast forecast.json --mapping mapping.json --book book.json --add-dem-name PATH
python3 -m card01_amc.entry_gate built_rows.json --fee-source PATH --fee-attest ATTEST.json
python3 -m card01_amc.swing_stress --rows built_rows.json --gate gate.json --gate-sha256 SHA --fee-source PATH
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

`python3 -m unittest discover -s tests -v --durations 10` from this directory: Ran 75 tests in 170.057s at 2026-10-09T00:01:39Z. Result: OK. Failures: 0. Errors: 0. Skipped: 0. Ruling `715fbafd` keeps the adopted fee blocked without `ATTEST_PASS`, allows the headline to sit below `FEE_ONLY_CEIL`, and fails closed on an unknown fee-source version. Ruling `c05d7003` remains in force for the sensitivity row, the dem_name fail-closed result, and literal REJECT (d) at zero signals.

Both self-test reproductions matched sha256 `0e93e153b7fc03cb996f3200dc576dd770ad638b00a1a0e3ed1e28632b682f23`: the pinned script's stdout, and the scorer projection after deleting the added keys.

Interpreter: `3.12.3 (main, Mar 23 2026, 19:04:32) [GCC 13.3.0]`. Platform: `Linux-6.12.94+-x86_64-with-glibc2.39`. CPython 3.13 was not installed on this machine. The byte match still held.

This run is code verification on synthetic inputs. It is not an Examiner score. `results`, `pnl`, and `roi` stay null.

## Limits

- Pre-outcome. No real data run. No Kalshi call. No ElectIndex fetch.
- Script `049368f9` is vendored byte-for-byte and is not edited.
- `UNSTABLE_SPLIT`, the R4 district split, and secondary metrics (log loss,
  calibration, adverse selection, top-1 share) are out of scope.
- The Q5 orderbook adapter is deferred (ruling `c05d7003`). Any Q5 status
  this tree emits is `UNAVAILABLE_NEEDS_EGRESS`. The builder consumes the
  normalized snapshot named in the lab spec.
- The adopted fee file is a runtime input. This tree does not contain it.
- `INCONCLUSIVE_DEGENERATE_BLOCK` is a headline status for 0 scored races or
  fewer than 2 states. It is not a PASS and not a REJECT. The verdict helper
  ranks validity above that status, then REJECT (a) / (b), then the fee branch.
- REJECT (c) and (d) realized P&L, including one-tick-worse fills, is out of
  scope for this PR (ruling `c05d7003`; a later PR-C). The helper does not
  compute it. A missing boolean stays fail-closed. Zero admitted signals
  make both (c) and (d) true, with note `NO_SIGNALS_SELECTED`. Precedence is
  unchanged.
- Adversary verification is required before the decision snapshot
  `2026-11-02T22:00Z`. This lab does not merge itself.

## Decisions recorded with the spec

These are fixed here so the code does not invent a second reading later.

- Built rows include `series` (mapping series, or null). The gate uses it to
  require a PINNED series entry. AF-4 cannot see the series from
  `mapping_status` alone when the series is legacy.
- An exclusion nulls both `p_market` and `p_model`. Raw quote fields stay when a
  snapshot was selected. `exclusion_reason` is the first code in this order:
  `mapping_unresolved`, file-level `no_admissible_forecast`, `NO_DEMOCRAT`,
  `SAME_PARTY_S5`, `DEM_NAME_UNRESOLVED`, per-race `no_admissible_forecast`,
  `no_ticker_for_mapped_race`, `snapshot_outside_window`,
  `market_closed_or_settled`, `no_two_sided_book`. `exclusion_reasons` lists
  every firing code in that order.
- A mapped race with no `chosen_ticker` is `no_ticker_for_mapped_race`. It is
  not recorded as a snapshot-window miss.
- `same_party_race` is retired. `SAME_PARTY_S5` fires only when the sha-checked
  dem_name file has `same_party_excluded_s5` true. `NO_DEMOCRAT` matches a
  case-insensitive leading `(no democrat` token and then a word boundary
  (ruling `c05d7003`). A name such as `(No Democratic primary)` does not
  match. A null or unresolved name is `DEM_NAME_UNRESOLVED`. A refused dem_name step is
  `DEM_NAME_STEP_REFUSED` plus its sub-reason. Usable rows become
  `DEM_NAME_UNRESOLVED`, and `closed_result` is
  `INCONCLUSIVE_DEGENERATE_BLOCK`. An accepted dem_name step must carry
  `original_sha256` equal to the sha of the forecast file actually passed to
  `build()`. A mismatch is `DEM_NAME_STEP_REFUSED` / `BASE_SHA_MISMATCH`, the
  same refusal the command line records. Original forecast keys `same_party`,
  `rep_name`, and `dem_name` are ignored. The builder does not copy name
  strings into its output.
- `no_two_sided_book` covers a missing side, a crossed book (`bid > ask`),
  `bid <= 0`, and `ask >= 1`.
- A snapshot is tradable only when `market_status` is `active` or `open`.
- `dem_prob` must be a finite number in `[0, 100]`.
- The builder refuses a forecast whose bytes do not match
  `selected_derived_sha256`, and a forecast passed with a non-`SELECTED`
  selection. A non-selected record builds 92 rows of `no_admissible_forecast`
  and records `q6_status`.
- Gate JSON that is `OK` carries `fee_source`, `fee_source_sha256`,
  `fee_source_status`, `fee_attest_verdict` (`ATTEST_PASS`),
  `fee_attest_fee_source_sha256`, `conductor_accept_sha256`, and `series_used`.
  A missing, mismatched, or non-pass attestation leaves the gate
  `BLOCKED_FEE_UNVERIFIED` with no signals. The attestation object is
  `{fee_source_sha256, verdict}` and the sha must equal the fee-source bytes.
  An unknown `astra.fee_source` schema version is
  `FEE_SOURCE_VERSION_UNSUPPORTED` once the sha check has passed.
  `astra.fee_source.v1` stays supported. A v2 file that is not the adopted
  sha is `FEE_SOURCE_SHA_MISMATCH` before that version check. Swing-stress
  emits a numeric `expected_net` only when `--gate-sha256` matches the gate
  file, `--fee-source` loads, the gate records `fee_attest_verdict`
  `ATTEST_PASS` for that `fee_source_sha256`, the gate and every signal carry
  that pair, and each headline fee recomputes. Without that recorded
  attestation the stress rows are null and the status is
  `BLOCKED_FEE_UNVERIFIED`. The output includes `fee_source` and
  `fee_source_sha256` when the gate carries them. Otherwise `expected_net` is
  `BLOCKED_FEE_UNVERIFIED` with `net_block_reason` set. A gate file cannot
  self-certify its net. The direct-member net is a sensitivity field and is
  not used for fragility. The fee stays blocked until an `ATTEST_PASS`
  attestation is supplied.
- `leave_one_state_out.by_state[s]` is either per-arm point estimates or the
  string `UNDEFINED`. Min and max ignore undefined remainders.
- `n_boundary_resamples` is a sibling of `arms` on each non-empty block.
- A reporting defect emits `rows: null`. It does not emit
  `NOT_FRAGILE_AT_PM0.5`.
- Conflicting settled results for one ticker leave `y` unchanged. A result with
  a missing or empty ticker is ignored and counted in `ignored_results`.
- `pinload` compiles the bytes that passed the sha check. It does not read the
  path a second time to execute them.
- `PINS.json` marks every listed file that is present, including the authored
  `card01_amc` modules, with `vendored: true`. The pin test treats
  `vendored: false` as "this path must not exist". The six earlier redacted
  governance documents use reason `PUBLIC_REPO_REDACTION_PENDING_TOS_REGATE`.
  Follow-up context documents use `PUBLIC_REPO_REDACTION`. The Q5 spec stays
  unvendored. Ruling `c05d7003` defers the adapter; the emitted status is
  `UNAVAILABLE_NEEDS_EGRESS`. The file does not list its own sha256.
