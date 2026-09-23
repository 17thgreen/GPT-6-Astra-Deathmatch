# R3-P3 favorite–longshot maker and taker

Status: hypothesis committed, then source frozen in this directory. Unit
outcomes, if recorded, live under `results/` and are not profit.
`EXPERIMENT_SPEC.md` is the hypothesis. `FROZEN_EXPERIMENT.json` keeps
`results`, `pnl`, `MZ`, and `band_roi` null.

Packet `R3-P3-FL-MAKER-TAKER`. Collector stub `READY` at panel version
`2026-09-22.r3-p3-fl-maker-taker-v0`. Clock `REFUSED`. Settled N is 0.
The harness imports `kalshi_feebook_lab_20260922` at
`22371178cb2663250b4762f328069571c48cb551` and does not copy that module.
Taker classification uses native public `taker_*` fields. `lee_ready` raises.
Price bands are `astra.r3p3.fl_maker_taker.price_bands_10c.v0` (b00–b09) and
are not rebinned after outcomes. The fixture is schema-only. It is not an
admitted settled panel.

From this directory, Python 3.12 standard library:

```bash
python3 -m unittest -v tests.test_maker_taker
```

No live orders. This lab does not modify the feebook lab, the rails lab, the
capital-structure lab, the hygiene lab, the queue-fragility lab, the examiner
lab, the R3-P1 lab, the R3-P4 lab, or the Q1–Q7 trees. It does not retune Q6
label `000`. An Examiner pass is not this scaffold.
