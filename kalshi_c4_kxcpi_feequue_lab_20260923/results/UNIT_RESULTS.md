# C4 KXCPI fee+queue honesty harness unit results

September 23, 2026. This file records a code check of the frozen analysis-slice
harness. It is a unit verification. It is not a simulated trading run and
not live validation. `FROZEN_EXPERIMENT.json` still has `results: null` and
`pnl: null`. `results/EMPTY_RESULTS.json` still has
`maker_vs_taker_roi_delta`, `sparse_vs_fresh_gap`, `missing_sot_n`,
`settled_join_n`, and `n_books` null. Those fields stay null on purpose.
This page is not profit, and it is not folded back into the freeze hashes.
No tape walk was run. No P&L figure is reported. This is not an Examiner
score and not a live-order certification.

## Command

From `kalshi_c4_kxcpi_feequue_lab_20260923`, Python 3.12, standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

Ran 12 tests in 0.069s at 2026-09-23T18:07:27Z. Result: OK. Failures: 0.
Errors: 0.

An earlier local run in this session, before that check, failed 3 tests.
Omitted `occurrence_datetime` keys on 21 scout markets were not counted as
missing, so the panel refuse bins collapsed and two tests raised `KeyError`.
The source now treats an omitted key on a panel market as a missing source
of time and does not insert a null. The 2026-09-23T18:07:27Z run is the
check after that correction.

The checks that passed are the predeclared ones: fee pin
`22371178cb2663250b4762f328069571c48cb551` and rails pin
`6a28e0d6254327ea4e6451c781bec56215ac6cac` with those trees unchanged since
those commits; the freeze, scout-hunt, panel-stub, and accept-stamp digests
recorded in `orchestrator.py` and `SOURCE_PINS.json`; preference for a
temporary `panel_admitted.json` when that file exists; C4A0 native taker
partitions and C4A1 sparse-24h / missing-SoT / content-fresh bins with the
scorecard fields null; Lee-Ready refused on every sampled input, including
a well-formed native row; refusal of live orders, Logan keys, invented
fills, invented fill density, invented `occurrence_datetime`, invented
depth, invented markets, a fee literal, Q6 retune, QF / Cap-SR / Cap-SR-FX /
L2 / EMPTY-OB / SOT-ID / L2-SF / NHL-FQ reopen, `admit.py`, an S1-green
claim, an S1 / S2 / R2-P4 ungate, and an NFL `000` signal port.

`fee_source` is feebook. `queue_source` is rails. The hygiene module
supplies `content_fresh_flag` and `queue_attribution_bin`. The synthetic
sparse fixture bins to `(true, not sparse, not missing, q3300)`,
`(false, not sparse, not missing, q3300)`,
`(false, not sparse, not missing, q10000)`,
`(true, sparse, not missing, q3300)`, and
`(true, not sparse, missing, q3300)`. None of those in-memory flags are
copied into the freeze files. `sparse_vs_fresh_gap` stays null.
`missing_sot_n` stays null. `n_books` stays null. The panel schema count of
44 markets is not written into `n_books`.

The pinned feebook series table has an empty override map. A probe of
`KXCPI` and of the NFL pointer series `KXNFLGAME` both resolve as
`default_unknown_series` under the examiner formula. No series override was
installed. The numeric fee was not copied onto the scorecard. The freeze
text cites `quadratic_with_maker_fees`; that cite is not a second fee table.

On the authentic stub, 21 markets omit `occurrence_datetime`. Zero markets
store a JSON null for that field. The `KXCPI-26NOV` event stores
`occurrence_datetime` null, and all 7 of its markets omit the key. Event
occurrence elsewhere equals the single non-null market timestamp already
on the hunt. Twenty-one markets have `volume_24h_fp` `0.00`. That zero is
a refuse label. It is not a fill density. The four panel bins are
`(sparse, missing)` counts 14, 14, 9, and 7. `content_fresh_flag` on those
panel bins stays null because the stub is not a book pair.

Feebook, rails, Q, Cap-SR, Cap-SR-FX, C1, C2 NHL-FQ, C3, C5, S4, S5, R2-P3,
L2-CAT, L2-SF, EMPTY-OB, and SOT-ID match
`677d5d4f0d5ed1235b4827bf89dd98d82bc34356` for those trees.

## Pins verified on this branch

- harness freeze `949b255859196f02d73303a1019e51276c583f8d1e3ffb4f0a64d330467c6f93` at the lab root, the lab bundle, `packets/C4_KXCPI_FEEQUEUE_HARNESS_FREEZE_2026-09-23.md`, and `packets/C4_KXCPI_FEEQUEUE_HARNESS/`
- scout hunt `6033907bb739bc00c41c796a3c1ed24553e0b7a44116ec3ea4bbaf39066bdcc8` at `packets/scout_cashcow_hunt_2026-09-22/scout_hunt_KXCPI.json` and the lab copies (44 markets, 4 events)
- panel stub `b20b0cbee50c127d2e9bb2548b574b7d643cc708f54019d53bd91775f9762c13` at `lab/astra-capture/c4-kxcpi/panel_stub.json` and `packets/C4_KXCPI_PANEL_STUB_2026-09-23.json` (4 events, 44 markets, `admitted_at` null, full scout, each market equal to the scout object with the same ticker)
- accept stamp `19ae0ae1fca66fa5c45bf8c13e013e3d710423c3e04194cc617d8bac1db546d7`
- `SOURCE_PINS.json` sha256 `6560d7bf40cd6470f3cae52504ee3079c8b7bbf7404c84f66fa77d84d66fceb9`

`conductor_pin_status` reports all three matches and
`conductor_bytes_in_checkout` true. `results` and `pnl` stay null. The
2026-09-23T18:07:27Z unit run is code verification. It is not an Examiner
score. Examiner hold status stays `NOT_SCORED` and `stub_ready` stays false.

## Limitations

- `lab/governance/astra/packets/` is absent. The verified copies are the
  lab paths and `packets/` paths listed above. `SOURCE_PINS.json` lists
  digests. It does not contain the file bytes.
- C4A0 and C4A1 on the conductor stub report `event_count` 4 and
  `market_count` 44 and do not write a scorecard. The two-trade native
  partition and the five-row sparse bins are
  `fixtures/synthetic_native_trades.json` and
  `fixtures/synthetic_sparse_fresh.json` with source
  `synthetic_schema_standin`. They are not a Kalshi GET and not an admitted
  cohort. Their tickers are not in the scout hunt.
- A scout ticker passed in as a native trade is refused. Public size fields
  on the stub are not a depth ladder. `quote_depth` refuses. `n_books`
  stays null. `assign_fill_density` and `assign_occurrence` refuse.
- `panel_admitted.json` is absent. `admitted_at` on the seed is null.
  Clock admit is still closed, so Examiner scoring stays closed.
- `PRE_ACCEPT_EMPTY_RESULTS.json` is the attached pre-ACCEPT payload. It
  omits `missing_sot_n`, `settled_join_n`, and `n_books`. `load_scorecard`
  refuses it.
- No public orderbook GET was stored. No Logan key was read. No order
  route exists in this lab. The NFL `000` path is a pointer only and was
  not parsed for a signal. Loading hygiene does not import queue-fragility.
- This packet does not ungate S1, S2, or R2-P4.
