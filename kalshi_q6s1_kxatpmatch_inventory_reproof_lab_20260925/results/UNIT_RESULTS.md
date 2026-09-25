# Q6S1 KXATPMATCH inventory re-proof harness unit results

September 25, 2026. This file records a code check of the frozen inventory-slice
harness. It is a unit verification. It is not a simulated trading run and
not live validation. `FROZEN_EXPERIMENT.json` still has `results: null` and
`pnl: null`. `results/EMPTY_RESULTS.json` still has
`inventory_delta_flat_vs_binned`, `unresolved_inventory`,
`position_bucket_gap`, `settled_join_n`, `n_books`, `results`, and `pnl`
null. Examiner scorecard v1.2 fields stay null. Those fields stay null on
purpose. This page is not profit, and it is not folded back into the freeze
hashes. No tape walk was run. No P&L figure is reported. This is not an
Examiner score and not a live-order certification. Examiner status stays
`HOLD_PRE_PR`.

## Command

From `kalshi_q6s1_kxatpmatch_inventory_reproof_lab_20260925`, Python 3.12, standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

Ran 13 tests in 0.047s, recorded at 2026-09-25T04:53:15Z. Result: OK.
Failures: 0. Errors: 0.

The checks that passed are the predeclared ones: series `KXATPMATCH` only;
fee pin `22371178cb2663250b4762f328069571c48cb551` and rails pin
`6a28e0d6254327ea4e6451c781bec56215ac6cac` with those trees unchanged since
those commits; freeze sha256
`d86f7a402ea63fb132d80480f844a954fe9061a27b9b6bed125f9785ae64640e`;
Conductor ACCEPT sha256
`162100624297588516390aab51ba0161cf15d0659c439ec6b60e940b99845635`;
panel stub sha256
`ed041c502d1f775d33c44bf900ac91b1339d99045bddd2052edd09a139ae2d3f`;
identical `SOURCE_PINS.json` copies; Q6S1A0 `flat_control` and Q6S1A1
`inventory_bin_exposure` with the scorecard fields null; every fee output
`cache_labeled` true, multiplier 1, and `live_r1p1` false; multiplier 0.5
refused; Lee-Ready refused; refusal of live orders, `/orders`, `/portfolio`,
invented fills, invented depth, invented inventory deltas, invented
`settlement_ts`, a screen 28/14 panel copy, ATP-FQ `analysis_slice`, ATP-RJ
`join_gate`, `admit.py`, dual-cloud, and an S1 / S2 / R2-P4 ungate. The stub
transport recorded `live_gets` 0. A hot `/markets` request was rewritten to
`/events`. `digest_all_match_claimed` stays false because the absent pins
are still absent.

`digest_all_match_claimed=false`. Absent: panel_admitted, live `/series` fee,
fresh 28/14 panel, invented fills/PnL/inventory deltas, Q6S1-specific scout PDF.
