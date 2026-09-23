# Examiner-channel fee and queue honesty on Q6-000

Status: one lab, `kalshi_examiner_fee_queue_honesty_000_lab_20260922`. The
canonical freeze is `packets/EXAMINER_FEE_QUEUE_HONESTY_000_FREEZE_2026-09-22.md`,
sha256 `4799642e54cf233a925697e00c5a9e29f5cb39070962a2e011f0fbe090c169f2`.
`EXPERIMENT_SPEC.md` is the hypothesis. `FROZEN_EXPERIMENT.json` keeps
`results`, `pnl`, and the six scorecard fields null.

The lab imports the pick A join in `kalshi_r2p1_hygiene_000_lab_20260922`
and the pick B join in `kalshi_queue_fragility_000_lab_20260922`. Fee stays
on `kalshi_feebook_lab_20260922` at
`22371178cb2663250b4762f328069571c48cb551`. Rails stay on
`kalshi_rails_lab_20260922` at
`6a28e0d6254327ea4e6451c781bec56215ac6cac`. Strategy pointer is Q6 label
`000`. Capital is the shared A1-equivalent 5000 USD pool. A2 and A3 stay
closed. There is one Examiner packet.

From this directory, Python 3.12 standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

`fill_rate_delta_vs_q3300`, `adverse_queue_exposure`, and
`participation_stress_gap` are required scorecard keys beside
`fee_delta_vs_inherited_model`, `freshness_gap_sec`, and
`queue_bin_mismatch_rate`. The same `write_scorecard` path refuses a missing
key or a non-null value on either side. The queue side asks whether an
honest queue treatment lifts the modeled edge relative to the current model.
The lab does not state a target edge ratio and does not record P&L.

When `nfl_factorial_lab_20260921/results/q3300_d0.25_000_fills.jsonl.gz` and
the matching orders file are both on disk and match the pinned sha256, both
joins read that pair. A different hash is refused. If either file is missing,
both joins read the queue-fragility synthetic stand-in. A unit may place the
same relative names under a temporary root. Synthetic labels stay out of the
freeze files.

No live orders. This lab does not modify the feebook lab, the rails lab,
`hygiene.py`, `queue_fragility.py`, or either fixture-join module. There is
no second Examiner packet. The six scorecard fields stay null.
