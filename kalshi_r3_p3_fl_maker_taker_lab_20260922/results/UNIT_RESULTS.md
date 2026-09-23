# R3-P3 maker-taker unit results

September 23, 2026. This file records a code check of the frozen helpers. It is
not a simulated trading run and not live validation. `FROZEN_EXPERIMENT.json`
still has `results: null`, `pnl: null`, `MZ: null`, and `band_roi: null`.
Those fields stay null on purpose: this page is not profit, and it is not
folded back into the freeze hashes.

## Command

From `kalshi_r3_p3_fl_maker_taker_lab_20260922`, Python 3.12.3, standard library:

```bash
python3 -m unittest -v tests.test_maker_taker
```

Ran 21 tests in 0.007s. Result: OK. Failures: 0. Errors: 0.

The checks that passed are the predeclared ones: the 10¢ registry
`astra.r3p3.fl_maker_taker.price_bands_10c.v0` assigns b00–b09 with the low
edge included and the high edge excluded, except b09 which includes 1; an
outcome argument raises `RebinRefused`; taker classification uses native
public `taker_outcome_side`, `taker_book_side`, and legacy `taker_side`, and
those fields must agree; a missing `taker_*` field raises `TakerFieldRefused`;
`lee_ready` raises `LeeReadyRefused` for every sample, including prices above
a midpoint, prices below a midpoint, and a tick at the midpoint; fee quotes
equal imported `feebook.order_fee` on the examiner channel; `classify_scorecard`
can still return `completed_profit` for that channel, and `scorecard_refuse`
does not copy the label onto `MZ` or `band_roi`; the schema walk joins three
rows, refuses two rows with no side, and leaves the freeze bytes unchanged.

## Limitations

- Settled N is 0. The collector stub is READY at panel version
  `2026-09-22.r3-p3-fl-maker-taker-v0`. `clock_admit` raises. This run is not
  an Examiner pass.
- The fixture is schema-only. Rows use ticker `SCHEMA-ONLY` and created time
  `SCHEMA_ONLY`. They are not captures, not fills, and not resolutions. No
  account endpoint was called.
- `kalshi_feebook_lab_20260922` is imported at
  `22371178cb2663250b4762f328069571c48cb551`. It is not copied. The taker and
  maker coefficients are not restated in this lab.
- Fee quotes use the order-level cent ceiling (`round_up=True`). A null
  scorecard is still a null scorecard when the feebook would say
  `completed_profit`.
- Lee-Ready has no successful path. Quote fields on a row do not assign a
  side. `is_taker` alone does not classify a public trade.
- Band edges were not refit. No Mincer–Zarnowitz coefficient was computed.
  No per-band return was computed.
- The Burgi, Deng, and Whelan maker return on contracts priced at or above
  50 cents (2.6 percent) is not evidence and was not used as a target.
- No Q1–Q7 directory was modified. Q6 label `000` was not retuned. Historical
  replays were not rerun.

No profit is reported. `results`, `pnl`, `MZ`, and `band_roi` stay null.
