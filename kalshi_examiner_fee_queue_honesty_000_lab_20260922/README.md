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

Hypothesis only. Source is not frozen in this commit. No unit outcome is
recorded here.
