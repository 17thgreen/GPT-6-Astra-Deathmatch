# C1 KXUFCFIGHT fee and queue honesty bakeoff

Status: one lab, `kalshi_c1_kxufcfight_honesty_lab_20260922`. The canonical
kernel is `packets/C1_KXUFCFIGHT_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md`,
sha256 `a191c9b3f71030445d1d32684feb6dc1bf09abb7e09403d5dbdf1927eafc63c9`.
`EXPERIMENT_SPEC.md` is the hypothesis. `FROZEN_EXPERIMENT.json` keeps every
measurement field, `results`, and `pnl` null.

The subject is the admitted UFC panel `lab/astra-capture/c1-kxufcfight/panel_admitted.json`,
`panel_version` `2026-09-22.c1-kxufcfight-v0`, `admitted_at` `2026-09-23T00:49:43Z`,
sha256 prefix `24426d80`. The pre-admit stub
`lab/astra-capture/c1-kxufcfight/panel_stub.json` (sha256
`2cc661d86202d3daf9ffa45320e39d249852a97490f458f72ab7ea8ec5c81a00`) is refused.
Fee stays on `kalshi_feebook_lab_20260922` at
`22371178cb2663250b4762f328069571c48cb551`. Rails stay on
`kalshi_rails_lab_20260922` at
`6a28e0d6254327ea4e6451c781bec56215ac6cac`. Those are the Q6-`000` instrument
commits. This lab does not retune `000` and does not read the `000` fills gzip.

The shared 5000 USD figure is a measurement label. Capital-structure modes
A1, A2, and A3 are refused. There is no strategy pointer.

From this directory, Python 3.12 standard library:

```bash
python3 -m unittest -v tests.test_orchestrator tests.test_collect_orderbooks
```

`write_scorecard` refuses a missing measurement field and a non-null value.
In-memory fixture labels stay out of the freeze files. `volume_fp` and
`open_interest_fp` stay null.

Production orderbooks belong at
`lab/astra-capture/c1-kxufcfight/orderbooks/`. The GET-only collector is
`collect_orderbooks.py`. The hypothesis is `ORDERBOOK_CAPTURE_SPEC.md`.
Unpinned JSON in that directory is refused. A sha256 pin is recorded in
`FROZEN_EXPERIMENT.json` when a real four-market capture is present. Until
then the score gate is `FIXTURE_GAP`. Either way Examiner status stays
`NOT_SCORED` until those pinned books and an Examiner-ready scorecard both
exist. Synthetic fixtures are refused for scorecard fill. Units for the
label algebra use `fixtures/synthetic_orderbooks.json`. See `fixtures/PIN.md`.

No live orders. This lab does not modify the feebook lab, the rails lab, the
`000` honesty lab, the hygiene lab, the queue-fragility lab, or the
capital-structure lab.
