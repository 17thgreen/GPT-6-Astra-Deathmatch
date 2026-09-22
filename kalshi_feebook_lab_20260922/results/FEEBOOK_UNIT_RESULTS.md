# R1-P1 feebook unit results

September 22, 2026. This file records a code check of the frozen helpers. It is
not a simulated trading run and not live validation. `FROZEN_EXPERIMENT.json`
still has `results: null` and `pnl: null`. Those fields stay null on purpose:
this page is not profit, and it is not folded back into the freeze hashes.

## Command

From `kalshi_feebook_lab_20260922`, Python 3.12.3, standard library:

```bash
python3 -m unittest -v tests.test_feebook
```

Ran 37 tests in 0.004s. Result: OK. Failures: 0. Errors: 0.

The checks that passed are the predeclared ones: documented bids-only
reciprocity, hand ceil vectors, the transcribed 21-row general taker table,
partials left unrounded, the optional cap, polarity at the touch, the Claude
versus Grok maker split, and refusal of `completed_profit` without the
examiner fee channel.

## Limitations

- Sibling fee sources named in `SOURCE_PINS.json` were not retrieved. Public
  raw URLs returned 404. The examiner path follows this lab's specification
  and the public table transcription. It is not a line-by-line port of
  `fees.py` or `fees.ts`.
- The Grok quote is the pinned comparator: unrounded maker fee per unit, no
  contract count, no cap. It is not an examiner channel. At price 0.50 the
  maker pair is examiner `0.01` for one contract versus Grok `0.004375`.
- The July 7, 2026 fee-schedule PDF says rounding makes fee plus position cost
  land on a centicent. The general taker table matches ceiling the fee itself
  to one cent. A centicent ceiling of the one-contract $0.05 raw (`0.003325`
  to `0.0034`) disagrees with the table cell `$0.01`. The examiner uses the
  table. `positionCost` is not defined here.
- PDF prose says the maker multiplier defaults to 0. The stub default is
  `M = 1` with maker fees enabled. Overrides are empty. `KXNFLGAME` is not
  stored as an override; a call with that name resolves as
  `default_unknown_series`. That is not a live schedule lookup.
- The `0.035` per-contract cap is the Claude optional flag. It is off in the
  stub and is not a row in the general taker table. With the cap off, `M = 2`
  at price 0.50 ceilings `0.035` to `0.04`.
- `kalshi_general_fee_table.json` is a transcription of the numeric table
  retrieved 2026-09-22. It does not contain the PDF bytes.
- `bids_only_fixture.json` is the public documentation example, not a live
  capture. Touch fees do not walk deeper levels and do not mean the size
  filled.
- Queue defaults and `MICRO_V1` in the pin file are context. They are not
  implemented. R1-P5 is not implemented.
- No Q1–Q7 directory was modified. Historical replays were not rerun.

No profit is reported.
