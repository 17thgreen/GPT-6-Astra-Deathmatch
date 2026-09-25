# Q6S5 KXMLBSPREAD fee+queue honesty harness

Status: hypothesis committed with the frozen pins. The unit page is
`results/UNIT_RESULTS.md` after the stub-transport run. That page is not
profit and not an Examiner pass. `EXPERIMENT_SPEC.md` is the hypothesis.
`FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.
`results/EMPTY_RESULTS.json` keeps `maker_vs_taker_roi_delta`,
`fresh_vs_stale_gap`, `settled_join_n`, and `n_books` null, and keeps the
Examiner scorecard v1.2 fields null.

This lab is measurement-only. Feature family Q6S5-MLBSPREAD-FEEQUEUE. The
series is `KXMLBSPREAD` only. It is not `KXMLBGAME` and it is not an S1 ML
retune. The only knob is `analysis_slice`: Q6S5A0 `maker_vs_taker_native`
and Q6S5A1 `content_fresh_vs_stale_bin`. Lee-Ready is refused on every
input. The fee is cache-labeled quadratic multiplier 0.5. Every fee output
sets `cache_labeled` true. That label is not a live R1-P1 `/series` pin.
The NFL `000` file is a pointer only.

- Freeze sha256 `4f65dcdf536755b9f7dc2449c2dcd90b2df74cdf99a441b676f1a71c4d709c6e`
- Conductor ACCEPT sha256 `5adc42f9c9533238a2187aafe7593bdf1b8cdec6d12b8d3e9b12cb5ab29000fc`
- Panel stub sha256 `c7f1f1f4ca263838c4600ed46db8f525b68efc5399a567bd60929d18d76803cc` (`2026-09-25.q6s5-kxmlbspread-v0`, `admitted_at` null, 6 events / 12 markets)
- `SOURCE_PINS.json` sha256 `588fdbd0a293823cf96b66ace00145ad10f56efb40badc4b2007b5e4bc832fde` (identical copies)

Scout raw markets and summary bytes are cited and are not in this checkout.
They were not invented. `digest_all_match_claimed` is true only when every
claimed pin re-hashes.

Fee pin `22371178cb2663250b4762f328069571c48cb551`.
Rails pin `6a28e0d6254327ea4e6451c781bec56215ac6cac`.
Those trees are not edited.

From this directory, Python 3.12 standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

No Logan keys. No live orders. No live Kalshi GET. A passing unit run is
not an Examiner score. Examiner status stays `HOLD_PRE_PR`.
