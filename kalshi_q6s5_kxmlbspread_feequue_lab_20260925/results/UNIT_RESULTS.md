# Q6S5 KXMLBSPREAD fee+queue honesty harness unit results

September 25, 2026. This file records a code check of the frozen analysis-slice
harness. It is a unit verification. It is not a simulated trading run and
not live validation. `FROZEN_EXPERIMENT.json` still has `results: null` and
`pnl: null`. `results/EMPTY_RESULTS.json` still has
`maker_vs_taker_roi_delta`, `fresh_vs_stale_gap`, `settled_join_n`, and
`n_books` null. Examiner scorecard v1.2 fields stay null. Those fields stay
null on purpose. This page is not profit, and it is not folded back into
the freeze hashes. No tape walk was run. No P&L figure is reported. This
is not an Examiner score and not a live-order certification. Examiner
status stays `HOLD_PRE_PR`.

## Command

From `kalshi_q6s5_kxmlbspread_feequue_lab_20260925`, Python 3.12, standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

Ran 12 tests in 0.047s at 2026-09-25T04:23:16Z. Result: OK. Failures: 0.
Errors: 0.

The checks that passed are the predeclared ones: series `KXMLBSPREAD` only;
fee pin `22371178cb2663250b4762f328069571c48cb551` and rails pin
`6a28e0d6254327ea4e6451c781bec56215ac6cac` with those trees unchanged since
those commits; freeze sha256
`4f65dcdf536755b9f7dc2449c2dcd90b2df74cdf99a441b676f1a71c4d709c6e`;
Conductor ACCEPT sha256
`5adc42f9c9533238a2187aafe7593bdf1b8cdec6d12b8d3e9b12cb5ab29000fc`;
panel stub sha256
`c7f1f1f4ca263838c4600ed46db8f525b68efc5399a567bd60929d18d76803cc`;
identical `SOURCE_PINS.json` copies; Q6S5A0 native taker partitions and
Q6S5A1 content-fresh / queue bins with the scorecard fields null; every
fee output `cache_labeled` true and `live_r1p1` false; Lee-Ready refused;
refusal of live orders, Logan keys, invented fills, invented depth,
invented markets, a KXMLBGAME ML retune, an NFL `000` signal port, `admit.py`,
dual-cloud, and an S1 / S2 / R2-P4 ungate. The stub transport recorded
`live_gets` 0. A hot `/markets` request was rewritten to `/events`. `/orders`
and `/portfolio` were refused. No network client was opened.

`digest_all_match_claimed` is false on this checkout. Scout raw markets,
scout summary, the p16 PDF, and the archivist ping are absent and were not
invented. A reduced pin list of the files that are present re-hashes true.
One altered digest forces the flag false.

The synthetic native trades and freshness rows are not panel fills.
`admitted_at` stays null on every committed panel file.
