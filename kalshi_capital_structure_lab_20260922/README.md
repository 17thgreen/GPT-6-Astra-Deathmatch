# Capital structure probe

Status: hypothesis committed, then source frozen in this directory. Unit
outcomes, if recorded, live under `results/` and are not profit.
`EXPERIMENT_SPEC.md` is the hypothesis. `FROZEN_EXPERIMENT.json` keeps
`results` and `pnl` null.

Arms A1, A2, and A3 share one `C_total` of 5000 USD. The engine imports
`kalshi_feebook_lab_20260922` for examiner fees and
`kalshi_rails_lab_20260922` for queue labels and maker-credit admission.
It does not read Q6 `common_config` fee coefficients. Strategy pointer is
Q6 label `000`. Pair-check is not a knob.

From this directory, Python 3.12 standard library:

```bash
python3 -m unittest -v tests.test_capital_structure
```

No live orders. This lab does not modify the feebook lab, the rails lab, or
the Q1–Q7 trees. A Q6-`000` tape walk is later Examiner work.
