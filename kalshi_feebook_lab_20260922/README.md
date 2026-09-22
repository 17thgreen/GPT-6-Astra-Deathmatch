# R1-P1 Kalshi feebook

Status: hypothesis and source frozen in this directory. Unit outcomes, if
recorded, live under `results/` and are not profit. `EXPERIMENT_SPEC.md` is
the hypothesis. `FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.

The examiner fee is order-level Decimal cent ceiling
(`astra.r1p1.feebook.claude_order_level_ceil.v1`). The Grok unrounded maker
quote is a comparator only.

From this directory, Python 3.12 standard library:

```bash
python3 -m unittest -v tests.test_feebook
```

No live orders. This lab does not import or modify the Q1–Q7 trees.
