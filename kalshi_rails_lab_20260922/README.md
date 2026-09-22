# R1-P5 Kalshi rails

Status: hypothesis committed, then source frozen in this directory. Unit
outcomes, if recorded, live under `results/` and are not profit.
`EXPERIMENT_SPEC.md` is the hypothesis. `FROZEN_EXPERIMENT.json` keeps
`results` and `pnl` null.

The queue instrument imports `kalshi_feebook_lab_20260922` and does not modify
it. Partial maker fills use `round_up=False`. Quote admission uses the
venue-rounded maker-credit floor. Book freshness is a predicate stub. The
MICRO helper is a scorecard shape with evidence stage
`HISTORICAL_OUT_OF_SAMPLE`.

From this directory, Python 3.12 standard library:

```bash
python3 -m unittest -v tests.test_rails
```

No live orders. This lab does not import or modify the Q1–Q7 trees. Collector
hooks and an Examiner pass are later work.
