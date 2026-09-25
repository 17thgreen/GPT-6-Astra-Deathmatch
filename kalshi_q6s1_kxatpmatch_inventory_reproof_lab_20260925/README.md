# Q6S1 KXATPMATCH inventory re-proof harness

Status: hypothesis committed with the frozen pins. The unit page is
`results/UNIT_RESULTS.md` after the stub-transport run. That page is not
profit and not an Examiner pass. `EXPERIMENT_SPEC.md` is the hypothesis.
`FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.
`results/EMPTY_RESULTS.json` keeps inventory deltas, `settled_join_n`,
`n_books`, `results`, and `pnl` null, and keeps the Examiner scorecard
v1.2 fields null.

This lab is measurement-only. Feature family Q6S1-ATP-INVENTORY. The
series is `KXATPMATCH` only. The only knob is `inventory_slice`: Q6S1A0
`flat_control` and Q6S1A1 `inventory_bin_exposure`. ATP-FQ `analysis_slice`
and ATP-RJ `join_gate` stay closed. Lee-Ready is refused. The fee is
cache-labeled `quadratic_with_maker_fees` multiplier 1. Every fee output
sets `cache_labeled` true and `live_r1p1` false. That label is not a live
R1-P1 `/series` pin and it is not multiplier 0.5.

- Freeze sha256 `d86f7a402ea63fb132d80480f844a954fe9061a27b9b6bed125f9785ae64640e`
- Conductor ACCEPT sha256 `162100624297588516390aab51ba0161cf15d0659c439ec6b60e940b99845635`
- Panel stub sha256 `ed041c502d1f775d33c44bf900ac91b1339d99045bddd2052edd09a139ae2d3f` (`2026-09-23.atp-kxatpmatch-v0`, `admitted_at` null, 6 events / 12 markets)
- Bundle sha256 `62de476ec3d27b64183d1eba0d223c2c5ad61a6bc8abffde9873f6e76a5e633e`
- `SOURCE_PINS.json` sha256 `cddb85e83e679a101108c45cd82b2e9b59e68f9afd0d89d141a5bee0460376e7` (identical copies)

`digest_all_match_claimed` stays false. Absent pins are panel_admitted,
the live `/series` fee pin, a fresh 28/14 screen panel, invented
fills/PnL/inventory deltas, and a Q6S1-specific scout PDF. Those files
were not invented. Examiner status stays `HOLD_PRE_PR`.

Fee pin `22371178cb2663250b4762f328069571c48cb551`.
Rails pin `6a28e0d6254327ea4e6451c781bec56215ac6cac`.
Those trees are not edited. This harness does not run `admit.py`.

Code verification `python3 -m unittest -v tests.test_orchestrator`: Ran 13 tests in 0.047s, recorded at 2026-09-25T04:53:15Z. Result: OK. Failures: 0. Errors: 0. That run is not an Examiner score. See `results/UNIT_RESULTS.md`.

From this directory, Python 3.12 standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

No Logan keys. No live orders. No live Kalshi GET. A passing unit run is
not an Examiner score.
