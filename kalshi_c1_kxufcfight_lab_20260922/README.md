# C1 KXUFCFIGHT measurement

Status: hypothesis committed, then source frozen in this directory. Unit
outcomes, if recorded, live under `results/` and are not profit.
`EXPERIMENT_SPEC.md` is the hypothesis. `FROZEN_EXPERIMENT.json` keeps
`results`, `pnl`, `MZ`, and `roi` null.

Packet `C1-KXUFCFIGHT-MEAS`. Collector stub `READY` at panel version
`2026-09-22.c1-kxufcfight-meas-v0`. Clock re-join `KICKED`. Admit
`NOT_ADMITTED`, awaiting `CLOCK_ADMIT_PASS`. The conductor reports settled
N of 4 on two finalized events. Admitted settled N stays 0.

The harness imports `kalshi_feebook_lab_20260922` at
`22371178cb2663250b4762f328069571c48cb551` for fee-honest maker and taker
quotes, and `kalshi_rails_lab_20260922` at
`6a28e0d6254327ea4e6451c781bec56215ac6cac` for freshness and queue labels.
It does not copy those modules. Series `KXUFCFIGHT` stays
`default_unknown_series` on the feebook stub. The `000` arm is the Q6
instrument-file pointer. Both arms carry the same shared $5,000
measurement-contrast label. That label is not a strategy claim and it does
not retune `000`.

Taker classification uses native public `taker_*` fields when they are
present. `lee_ready` raises. The fixture is schema-only. It is not an
admitted settled panel and it does not award fills.
`fixtures/resolution_hook_not_admitted.json` is the placeholder for a later
resolution join. `wire_resolution_hook` leaves every resolution unwired.
`apply_resolutions` and `clock_admit` raise.

From this directory, Python 3.12 standard library:

```bash
python3 -m unittest -v tests.test_bakeoff
```

No live orders. This lab does not modify the feebook lab, the rails lab, the
capital-structure lab, the hygiene lab, the queue-fragility lab, the examiner
lab, the R3 labs, or the Q1–Q7 trees. An Examiner pass is not this scaffold.
`MZ` and `roi` stay null until a Clock admit pass, which this scaffold does not obtain.
