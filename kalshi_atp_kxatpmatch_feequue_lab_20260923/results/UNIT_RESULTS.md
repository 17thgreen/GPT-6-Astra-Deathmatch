# ATP KXATPMATCH fee+queue honesty harness unit results

September 23, 2026. This file records a code check of the frozen analysis-slice
harness. It is a unit verification. It is not a simulated trading run and
not live validation. `FROZEN_EXPERIMENT.json` still has `results: null` and
`pnl: null`. `results/EMPTY_RESULTS.json` still has
`maker_vs_taker_roi_delta`, `fresh_vs_stale_gap`, `settled_join_n`, and
`n_books` null. Those fields stay null on purpose. This page is not profit,
and it is not folded back into the freeze hashes. No tape walk was run. No
P&L figure is reported. This is not an Examiner score and not a live-order
certification.

## Command

From `kalshi_atp_kxatpmatch_feequue_lab_20260923`, Python 3.12, standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

Ran 13 tests in 0.069s at 2026-09-23T18:23:56Z. Result: OK. Failures: 0.
Errors: 0.

The checks that passed are the predeclared ones: fee pin
`22371178cb2663250b4762f328069571c48cb551` and rails pin
`6a28e0d6254327ea4e6451c781bec56215ac6cac` with those trees unchanged since
those commits; the freeze, scout-hunt, panel-stub, and accept digests
recorded in `orchestrator.py` and `SOURCE_PINS.json`; preference for a
temporary `panel_admitted.json` when that file exists; ATPA0 native taker
partitions and ATPA1 content-fresh / queue bins with the scorecard fields
null; Lee-Ready refused on every sampled input, including a well-formed
native row; refusal of live orders, Logan keys, invented fills, invented
depth, invented markets, invented fill density, an invented
`occurrence_datetime`, a fee literal, Q6 retune, QF / Cap-SR / Cap-SR-FX /
L2 / EMPTY-OB / SOT-ID / L2-SF / NHL-FQ / CPI-FQ reopen, `admit.py`, an
S1-green claim, an S1 / S2 / R2-P4 ungate, and an NFL `000` signal port.

`fee_source` is feebook. `queue_source` is rails. The hygiene module
supplies `content_fresh_flag` and `queue_attribution_bin`. The synthetic
fresh fixture bins to `(true, q3300)`, `(false, q3300)`, and
`(false, q10000)`. None of those in-memory flags are copied into the freeze
files. `fresh_vs_stale_gap` stays null. `n_books` stays null. The panel
schema count of 12 markets is not written into `n_books`.

The attached hunt has `occurrence_datetime` on all 48 scout markets and all
12 panel markets. The missing count is 0. Dropping the key or setting it
null on a detached copy is counted as missing and is not filled back in.
A non-timestamp value is refused. An event timestamp that disagrees with
the scout market timestamp is refused. `assign_fill_density` is refused.
`fill_density` is absent from the committed hunt.

The pinned feebook series table has an empty override map. A probe of
`KXATPMATCH` and of the NFL pointer series `KXNFLGAME` both resolve as
`default_unknown_series` under the examiner formula. No series override was
installed. The numeric fee was not copied onto the scorecard. The freeze
text cites `quadratic_with_maker_fees`; that cite is not a second fee table.

Feebook, rails, Q, Cap-SR, Cap-SR-FX, C1, C2, C3, C4, C5, S4, S5, R2-P3,
L2-CAT, L2-SF, EMPTY-OB, and SOT-ID match
`6e55a99790f4cc09a437d2e16ccf4e8e826a154b` for those trees.

## Pins verified on this branch

- harness freeze `4d4ce944946e72dd40567d14388fe11c6145fbbb32505a880bcf80a4c8b4dffe` at the lab root, the lab bundle, `packets/ATP_KXATPMATCH_FEEQUEUE_HARNESS_FREEZE_2026-09-23.md`, and `packets/ATP_KXATPMATCH_FEEQUEUE_HARNESS/`
- scout hunt `14c99ec8ea00bae507a21d0e6a1879fb94d32ef69ad4b5e3b40a9952821e5da7` at `packets/scout_cashcow_hunt_2026-09-22/scout_hunt_KXATPMATCH.json` and the lab copies (48 markets, 24 events)
- panel stub `ed041c502d1f775d33c44bf900ac91b1339d99045bddd2052edd09a139ae2d3f` at `lab/astra-capture/atp-kxatpmatch/panel_stub.json` and `packets/ATP_KXATPMATCH_PANEL_STUB_2026-09-23.json` (6 events, 12 markets, `admitted_at` null, each market equal to the scout object with the same ticker)
- accept stamp `b038994585e19d28d014882594239eafc2657b6de7da105f238c90d49954bd8b`
- `SOURCE_PINS.json` sha256 `b9dadbf3a844c20f11468669addb90a22c7f72e28921a123f433f1547a6bbe72`

`conductor_pin_status` reports all three matches and
`conductor_bytes_in_checkout` true. `results` and `pnl` stay null. The
2026-09-23T18:23:56Z unit run is code verification. It is not an Examiner
score. Examiner hold status stays `NOT_SCORED` and `stub_ready` stays false.

## Limitations

- `lab/governance/astra/packets/` is absent. The verified copies are the
  lab paths and `packets/` paths listed above. `SOURCE_PINS.json` lists
  digests. It does not contain the file bytes.
- ATPA0 and ATPA1 on the conductor stub report `event_count` 6,
  `market_count` 12, and `missing_occurrence_datetime_n` 0. They do not
  write a scorecard. The two-trade native partition and the three-row
  freshness bins are `fixtures/synthetic_native_trades.json` and
  `fixtures/synthetic_fresh_queue.json` with source
  `synthetic_schema_standin`. They are not a Kalshi GET and not an admitted
  cohort. Their tickers are not in the scout hunt.
- A scout ticker passed in as a native trade is refused. Public
  `yes_bid_size_fp` on the stub is not a depth ladder. `quote_depth`
  refuses. `n_books` stays null.
- `panel_admitted.json` is absent. `admitted_at` on the seed is null.
  Clock admit is still closed, so Examiner scoring stays closed.
- `PRE_ACCEPT_EMPTY_RESULTS.json` is the attached pre-ACCEPT payload. It
  omits `settled_join_n` and `n_books`. `load_scorecard` refuses it.
- No public orderbook GET was stored. No Logan key was read. No order
  route exists in this lab. The NFL `000` path is a pointer only and was
  not parsed for a signal. Loading hygiene does not import queue-fragility.
- This packet does not claim S1 green and does not ungate S1, S2, or R2-P4.
