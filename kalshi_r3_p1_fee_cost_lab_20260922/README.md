# R3-P1 fee_cost versus the R1-P1 model

Status: hypothesis committed, then source frozen in this directory. Unit
outcomes, if recorded, live under `results/` and are not profit.
`EXPERIMENT_SPEC.md` is the hypothesis. `FROZEN_EXPERIMENT.json` keeps
`results`, `pnl`, and `fee_model_minus_venue_delta` null.

Packet `R3-P1-FEE-COST-VS-MODEL`. The harness imports
`kalshi_feebook_lab_20260922` at
`22371178cb2663250b4762f328069571c48cb551` and does not copy that module.
`fee_model` is `order_fee` with the examiner cent ceiling. Reported
`fee_cost` is the accounting fee when the fill has one. The delta is
`fee_model` minus `fee_cost`. A model-only completed net is refused when
`fee_cost` was available. A null `fee_cost` may support a projection only.

From this directory, Python 3.12 standard library:

```bash
python3 -m unittest -v tests.test_fee_cost
```

No live orders. This lab does not modify the feebook lab, the rails lab,
the capital-structure lab, the hygiene lab, the queue-fragility lab, or the
Q1–Q7 trees. It does not retune Q6 label `000`.
