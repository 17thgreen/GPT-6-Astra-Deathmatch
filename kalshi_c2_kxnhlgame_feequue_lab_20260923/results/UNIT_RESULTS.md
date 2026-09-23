# C2 KXNHLGAME fee+queue honesty harness unit results

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

From `kalshi_c2_kxnhlgame_feequue_lab_20260923`, Python 3.12, standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

Ran 12 tests in 0.057s at 2026-09-23T17:49:26Z. Result: OK. Failures: 0.
Errors: 0.

The checks that passed are the predeclared ones: fee pin
`22371178cb2663250b4762f328069571c48cb551` and rails pin
`6a28e0d6254327ea4e6451c781bec56215ac6cac` with those trees unchanged since
those commits; the freeze, scout-hunt, and panel-stub digests recorded in
`orchestrator.py` and `SOURCE_PINS.json`; preference for a temporary
`panel_admitted.json` when that file exists; C2A0 native taker partitions
and C2A1 content-fresh / queue bins with the scorecard fields null;
Lee-Ready refused on every sampled input, including a well-formed native
row; refusal of live orders, Logan keys, invented fills, invented depth,
invented markets, a fee literal, Q6 retune, QF / Cap-SR / Cap-SR-FX / L2 /
EMPTY-OB / SOT-ID / L2-SF reopen, `admit.py`, an S1-green claim, an S1 /
S2 / R2-P4 ungate, and an NFL `000` signal port.

`fee_source` is feebook. `queue_source` is rails. The hygiene module
supplies `content_fresh_flag` and `queue_attribution_bin`. The synthetic
fresh fixture bins to `(true, q3300)`, `(false, q3300)`, and
`(false, q10000)`. None of those in-memory flags are copied into the freeze
files. `fresh_vs_stale_gap` stays null. `n_books` stays null. The panel
schema count of 12 markets is not written into `n_books`.

The pinned feebook series table has an empty override map. A probe of
`KXNHLGAME` and of the NFL pointer series `KXNFLGAME` both resolve as
`default_unknown_series` under the examiner formula. No series override was
installed. The numeric fee was not copied onto the scorecard. The freeze
text cites `quadratic_with_maker_fees`; that cite is not a second fee table.

Feebook, rails, Q, Cap-SR, Cap-SR-FX, C1, C3, C5, S4, S5, R2-P3, L2-CAT,
L2-SF, EMPTY-OB, and SOT-ID match
`ead2cb41d5d171d8972a27b98d144849b6f8c371` for those trees.

## Pins verified on this branch

- harness freeze `a36ec35143a32c7cd24e9fdf2a33f645d356b93e34c131bb1b8a94e3f92e38f5` at the lab root, the lab bundle, `packets/C2_KXNHLGAME_FEEQUEUE_HARNESS_FREEZE_2026-09-23.md`, and `packets/C2_KXNHLGAME_FEEQUEUE_HARNESS/`
- scout hunt `1ab794ad688ba31e0178e78294dcdbe50cf2799a71f40245e5a04a80e9dd5762` at `packets/scout_cashcow_hunt_2026-09-22/scout_hunt_KXNHLGAME.json` and the lab copies (66 markets, 33 events)
- panel stub `60d183e7bdcf25adbc94eeeb3bb361b5232c19c0fe3e6a115f45ab3fcb100c79` at `lab/astra-capture/c2-kxnhlgame/panel_stub.json` and `packets/C2_KXNHLGAME_PANEL_STUB_2026-09-23.json` (6 events, 12 markets, `admitted_at` null, each market equal to the scout object with the same ticker)
- `SOURCE_PINS.json` sha256 `2f1a9da6b5365c79300d8883847358beeb940f1f6ccf5a2e770a1ee136720ded`

`conductor_pin_status` reports all three matches and
`conductor_bytes_in_checkout` true. `results` and `pnl` stay null. The
2026-09-23T17:49:26Z unit run is code verification. It is not an Examiner
score. Examiner hold status stays `NOT_SCORED` and `stub_ready` stays false.

## Limitations

- `lab/governance/astra/packets/` is absent. The verified copies are the
  lab paths and `packets/` paths listed above. `SOURCE_PINS.json` lists
  digests. It does not contain the file bytes.
- C2A0 and C2A1 on the conductor stub report `event_count` 6 and
  `market_count` 12 and do not write a scorecard. The two-trade native
  partition and the three-row freshness bins are
  `fixtures/synthetic_native_trades.json` and
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
