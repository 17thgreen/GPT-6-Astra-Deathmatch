# R2-P1 hygiene stress on Q6-000

Status: hypothesis committed in this directory. Source, if frozen, follows in
the same directory. Unit outcomes, if recorded, live under `results/` and are
not profit. `EXPERIMENT_SPEC.md` is the hypothesis. `FROZEN_EXPERIMENT.json`
keeps `results`, `pnl`, and the three pre-settlement outputs null.

The lab imports `kalshi_feebook_lab_20260922` for examiner fees and
`kalshi_rails_lab_20260922` for queue labels, maker-credit admission, and the
content-fresh predicate. It does not read Q6 `common_config` fee coefficients.
Strategy pointer is Q6 label `000`. Capital arms and the queue-fragility twin
are not knobs.

From this directory, Python 3.12 standard library:

```bash
python3 -m unittest -v tests.test_hygiene
```

No live orders. This lab does not modify the feebook lab, the rails lab, the
capital-structure lab, or the Q1–Q7 trees. A Q6-`000` tape join is later
Examiner work. Until that join the pre-settlement outputs stay null.
