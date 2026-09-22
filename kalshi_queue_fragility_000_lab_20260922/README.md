# Queue fragility of Q6-000 under R1-P5

Status: one lab, `kalshi_queue_fragility_000_lab_20260922`. The canonical
freeze is `QUEUE_FRAGILITY_000_R1P5_FREEZE_2026-09-22.md`, sha256
`e01d684abefd2d919ac6546f85619a246ce73098c04f7b24c84451ff49b00308`.
`EXPERIMENT_SPEC.md` is the hypothesis. `FROZEN_EXPERIMENT.json` keeps
`results`, `pnl`, and the three pre-settlement outputs null.

The only knob is rails queue/fill stress (`QF0`, `QF1`, `QF2`). The fee
channel is the R1-P1 examiner formula imported from
`kalshi_feebook_lab_20260922` at
`22371178cb2663250b4762f328069571c48cb551`. Queue magnitudes come from
`kalshi_rails_lab_20260922` at
`6a28e0d6254327ea4e6451c781bec56215ac6cac`. Strategy pointer is Q6 label
`000`. Capital is the shared A1-equivalent 5000 USD pool. A2 and A3 stay
closed.

From this directory, Python 3.12 standard library:

```bash
python3 -m unittest -v tests.test_queue_fragility
```

No live orders. This lab does not modify the feebook lab, the rails lab, the
R2-P1 hygiene lab, the capital-structure lab, or the Q1–Q7 trees. A Q6-`000`
tape join is later Examiner work. Until that join the pre-settlement outputs
stay null.
