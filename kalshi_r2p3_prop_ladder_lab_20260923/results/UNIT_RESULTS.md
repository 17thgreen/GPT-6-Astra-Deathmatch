# R2-P3 KXNFLPASSYDS prop-ladder harness unit results

September 23, 2026. This file records a code check of the frozen prop-ladder
harness. It is a unit verification. It is not a simulated trading run and
not live validation. `FROZEN_EXPERIMENT.json` still has `results: null` and
`pnl: null`. `results/EMPTY_RESULTS.json` still has
`cross_strike_residual_rms`, `latent_fit_fragmentation`,
`maker_credit_floor_zero_n`, `fresh_strike_n`, and `settled_join_n` null.
Those fields stay null on purpose. This page is not profit, and it is not
folded back into the freeze hashes. No tape walk was run. No P&L figure is
reported. This is not an Examiner score and not a live-order certification.

## Command

From `kalshi_r2p3_prop_ladder_lab_20260923`, Python 3.12, standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

Ran 8 tests in 0.046s at 2026-09-23T16:15:40Z. Result: OK. Failures: 0.
Errors: 0.

The checks that passed are the predeclared ones: fee pin
`22371178cb2663250b4762f328069571c48cb551` and rails pin
`6a28e0d6254327ea4e6451c781bec56215ac6cac` with those trees unchanged since
those commits; the packet, parent kernel, and panel-stub digests equal the
conductor claims; event count 6; preference for a temporary
`panel_admitted.json` when that file exists; a 5-event recreation refused;
R2P3A0 isotonic and R2P3A1 logit-monotone fits on the synthetic ladder with
the scorecard fields null; Lee-Ready refused, including on a well-formed
strike row; ATL@GB refused; a supplied fee literal refused; WS-ping
freshness refused; live orders, Logan keys, invented fills, Q6 retune, QF
reopen, Cap-SR reopen, Cap-SR-FX reopen, and `admit.py` refused.

`fee_source` is feebook. `queue_source` is rails. The hygiene module
supplies `content_fresh_flag`, `maker_credit_floor_zero_refuse`, and
`queue_attribution_bin`. On the synthetic ladder, player `SYNTHETIC_A`
strikes 250 and 275 pool under isotonic to fitted mid 0.76, the 325 strike
stamps maker-credit floor-zero refuse, and the keepalive row stays stale.
Those in-memory labels are not copied into the freeze files.
`cross_strike_residual_rms` stays null. The logit-monotone fit on the same
violation is monotone and is not the isotonic 0.76 pool.

Feebook, rails, Q, Cap-SR, Cap-SR-FX, C3, C5, R3-P3, S4, and S5 match
`d7584dd48a67d38d81f5141654b6f498915a70a5` for those trees.

## Conductor bytes

Verified sha256 on this branch:

- harness freeze `f8335eb0080cb1f82b1fad512509749134dd0e6e41ed85795347c3476796e87a` at the lab root, the lab bundle, `packets/R2_P3_KXNFLPASSYDS_PROP_LADDER_HARNESS_FREEZE_2026-09-23.md`, and `packets/R2_P3_PROP_LADDER_HARNESS/`
- parent kernel `a30108f658359590e170c73ea00d1a1f0852d5751cb15c9f2a9c6389f4dd3eaa` at the same four locations
- panel stub `70e879e8738d033f392d821849dee3537af3e7b8a916670779d238f78ce098be` at `lab/astra-capture/r2-p3-prop-slate/panel_stub.json` (6 events; empty `market_tickers`; `volume_fp`, `open_interest_fp`, `results`, and `pnl` null; `admitted_at` null) and at the lab bundle and `packets/R2_P3_PROP_LADDER_HARNESS/`

`PACKET_SHA256`, `KERNEL_SHA256`, and `PANEL_STUB_SHA256` equal those
conductor digests. `conductor_pin_status` reports all three matches and
`conductor_bytes_in_checkout` true. The panel stub loads as 6 events.
`results` and `pnl` stay null. The 2026-09-23T16:15:40Z unit run is code
verification. It is not an Examiner score.

## Limitations

- `lab/governance/astra/packets/` is absent. The verified copies are the
  lab paths and `packets/` paths listed above. The capture README is
  lab-authored and is not a conductor-box byte.
- R2P3A0 and R2P3A1 on the conductor stub report `event_count` 6 and
  `market_count` 0. They do not write a scorecard. The seven-strike ladder
  is `fixtures/synthetic_mid_ladder.json` with source
  `synthetic_schema_standin` and player ids `SYNTHETIC_A` and `SYNTHETIC_B`.
  It is not a Kalshi GET and not an admitted cohort.
- `panel_admitted.json` is absent. `admitted_at` on the seed is null.
  Clock admit is still closed, so Examiner scoring stays closed.
- No public GET of the slate was stored. The stub's own live-resolution
  note remains HTTP 429, and that note was not rewritten.
- No Logan key was read. No order route exists in this lab. Loading
  hygiene does not import queue-fragility.
