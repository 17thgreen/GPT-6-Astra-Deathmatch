# R3-P1 fee_cost versus the R1-P1 model

Status: hypothesis committed in this directory. Source is not frozen in this
commit. `EXPERIMENT_SPEC.md` is the hypothesis. `FROZEN_EXPERIMENT.json` keeps
`results`, `pnl`, and `fee_model_minus_venue_delta` null.

Packet `R3-P1-FEE-COST-VS-MODEL`. The lab imports
`kalshi_feebook_lab_20260922` at
`22371178cb2663250b4762f328069571c48cb551` and does not copy it. Venue
`fee_cost` is preferred when the synthetic fill reports it. The model is the
comparator. This is not a strategy and it does not retune Q6 label `000`.

No live orders.
