# C3-KXHIGHNY bordering-strike unit results

September 23, 2026. This file records a code check of the frozen helpers. It is
not a simulated trading run and not live validation. `FROZEN_EXPERIMENT.json`
still has `results: null`, `pnl: null`, `MZ: null`, and `ROI: null`. Those
fields stay null on purpose: this page is not profit, and it is not folded
back into the freeze hashes.

## Command

From `kalshi_c3_kxhighny_lab_20260922`, Python 3.12.3, standard library:

```bash
python3 -m unittest -v tests.test_ladder
```

Ran 17 tests in 0.006s. Result: OK. Failures: 0. Errors: 0.

The checks that passed are the predeclared ones: two borders and one gap on
the New York schema ladder, one Chicago interior border, reciprocal YES spread
`0.05` on the 76–77 rung, refusal of the one-cent YES bid by the imported
maker-credit rail, an unset YES bid left unset, overlap and `KXHIGHMIA`
refusals, whole-degree strikes, keepalive freshness, and a null scorecard
after the walk. An in-memory `result` key is refused. The committed fixture
has no resolution or fill keys.

The frozen feebook suite was rerun from its own directory: 37 tests, OK,
0.004s. The frozen rails suite was rerun from its own directory: 44 tests,
OK, 0.004s. Those reruns are regression checks of unchanged modules. They are
not C3 results.

## Limitations

- The ladder is a schema sheet. It is not a capture, not a listing, and not
  a settled panel. Settled N is 0. The collector stub is READY and the clock
  is REFUSED.
- `kalshi_feebook_lab_20260922` is imported at
  `22371178cb2663250b4762f328069571c48cb551`.
  `kalshi_rails_lab_20260922` is imported at
  `6a28e0d6254327ea4e6451c781bec56215ac6cac`. Neither module is copied.
  `KXHIGHNY` and `KXHIGHCHI` resolve as `default_unknown_series` on the
  feebook stub. That mark is not a live fee schedule.
- Queue labels `q3300` and `q10000` are read from the rails. No queue volume
  is awarded. Touch size is not a fill.
- GitHub `kalshi_weather.py` blob
  `323463cd7538464dfe90ec8b6acea9c76e10ee29` is the hypothesis citation.
  The forecast client and the mid-sum are not ported. Published weather
  returns are not evidence.
- `MZ` and `ROI` stay null. A later R3-P3 weather panel is preferred and is
  not joined. R3-P3 is not modified. Q6 label `000` is not retuned. No live
  order was sent.
