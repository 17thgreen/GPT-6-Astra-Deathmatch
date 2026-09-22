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
python3 -m unittest -v tests.test_queue_fragility tests.test_fixture_join
```

Pick **B** joins Q6-`000` fill and order fixtures through `QF0`, `QF1`, and
`QF2` in `fixture_join.py`. The canonical join freeze is
`packets/QF_FIXTURE_JOIN_000_FREEZE_2026-09-22.md`, sha256
`d95adb9b7e8aba852134c96b8f0f7d35a76bbf68254b8808f82f99ec82bb6ca4`.
Pick A stays in `kalshi_r2p1_hygiene_000_lab_20260922/fixture_join.py`.
There is no second queue-fragility directory and no
`kalshi_r2p1_fixture_join_000_lab_*` directory. Production gzip pins are in
`fixtures/PIN.md`. When those files are absent the harness reads the synthetic
jsonl pair in `fixtures/`.

No live orders. The R2-P1 pin-lock allows this directory as its queue-fragility
sibling and still forbids a second fee-sensitivity lab and a second R2-P1
directory. This lab does not modify the feebook lab, the rails lab, the
hygiene lab, the capital-structure lab, or the Q1–Q7 trees. `queue_fragility.py`
is unchanged. The five scorecard fields stay null.
