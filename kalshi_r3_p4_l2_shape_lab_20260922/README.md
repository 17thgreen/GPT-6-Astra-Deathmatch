# R3-P4 L2 shape (SF1 / SF2)

Status: hypothesis committed, then source frozen in this directory. Unit
outcomes, if recorded, live under `results/` and are not a Kalshi stylized
fact and not profit. `EXPERIMENT_SPEC.md` is the hypothesis.
`FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.

The shape module imports `kalshi_feebook_lab_20260922` for the reciprocal mid
and spread and `kalshi_rails_lab_20260922` for the content-fresh gate. It does
not copy those modules. SF1 is the median quoted half-spread in bps of mid by
absolute mid-price decile. SF2 is the L1 and top-10 depth share plus KL
divergence against a uniform `1/10` book. Fixtures are synthetic GET-shaped
books. Sports and non-sports are a category slice of those fixtures.

From this directory, Python 3.12 standard library:

```bash
python3 -m unittest -v tests.test_shape
```

No live orders. This lab does not modify the feebook lab, the rails lab, the
capital-structure lab, or the Q1–Q7 trees. Lee-Ready is not implemented.
`results/EMPTY_RESULTS.json` stays null.
