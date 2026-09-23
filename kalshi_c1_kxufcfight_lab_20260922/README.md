# C1 KXUFCFIGHT measurement

Status: hypothesis committed, then source frozen in this directory. Unit
outcomes, if recorded, live under `results/` and are not profit.
`EXPERIMENT_SPEC.md` is the hypothesis. `FROZEN_EXPERIMENT.json` keeps
`results`, `pnl`, `MZ`, and `roi` null.

Packet `C1-KXUFCFIGHT-MEAS`. Collector stub `READY`. The admitted panel is
`2026-09-22.c1-kxufcfight-v0`, `admitted_at` `2026-09-23T00:49:43Z`, stub
`PANEL_ADMITTED_C1_UFC_ONLY`, sha256
`24426d804c51bde23cf2557a11a8481a12026da10024094c4ae546d1f7d3956e`.
Two events, four markets. `clock_admit` accepts that stamp. Scorecard
settled N stays 0.

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
present. `lee_ready` raises. The schema fixture is schema-only and does not
award fills. `fixtures/panel_admitted.json` matches the capture panel bytes.
`fixtures/resolution_join_admitted.json` joins the four
`result_observed_live_get` labels. `lab/astra-capture/c1-kxufcfight/resolutions/`
has no JSON in this checkout, so those cited capture bytes are not claimed.
`fixtures/resolution_hook_not_admitted.json` is the closed-PR placeholder
and the wiring path refuses it. `mz`, `roi`, and `write_scorecard` raise.
`clock_admit('ADMIT_PASS')` raises.

From this directory, Python 3.12 standard library:

```bash
python3 -m unittest -v tests.test_bakeoff
```

No live orders. This lab does not modify the feebook lab, the rails lab, the
capital-structure lab, the hygiene lab, the queue-fragility lab, the examiner
lab, the R3 labs, or the Q1–Q7 trees. An Examiner pass is not this scaffold.
`MZ` and `roi` stay null after the `ADMITTED` stamp. The stamp is not profit.
