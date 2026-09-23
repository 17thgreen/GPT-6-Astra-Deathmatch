# C1 KXUFCFIGHT honesty unit results

September 23, 2026. This file records a code check of the UFC fee and queue
harness after the Clock-admitted panel was placed in the checkout. It is not
a simulated trading run and not live validation. Admit of the panel is not an
Examiner score. C1 remains `NOT_SCORED`. `FROZEN_EXPERIMENT.json` status stays
`FROZEN_NOT_RUN`. That file and `results/EMPTY_RESULTS.json` still have every
measurement field, `results`, and `pnl` null. No completed-net figure is
reported.

Kernel sha256
`a191c9b3f71030445d1d32684feb6dc1bf09abb7e09403d5dbdf1927eafc63c9`.
`panel_version` `2026-09-22.c1-kxufcfight-v0`. Clock stamp
`2026-09-23T00:49:43Z`. Admitted panel
`lab/astra-capture/c1-kxufcfight/panel_admitted.json`, sha256
`24426d804c51bde23cf2557a11a8481a12026da10024094c4ae546d1f7d3956e`
(prefix `24426d80`). The same digest is `panel_admitted_sha256` in
`FROZEN_EXPERIMENT.json`.
R1-P1 `22371178cb2663250b4762f328069571c48cb551`.
R1-P5 `6a28e0d6254327ea4e6451c781bec56215ac6cac`.

## Command

From `kalshi_c1_kxufcfight_honesty_lab_20260922`, Python 3.12.3, standard
library, at `2026-09-23T02:06:09Z`:

```bash
python3 -m unittest -v tests.test_orchestrator
```

Ran 12 tests in 0.027s. Result: OK. Failures: 0. Errors: 0.

The subject is `panel_admitted.json`. `load_panel` refuses
`panel_stub.json`. The pin checks match `panel_version`
`2026-09-22.c1-kxufcfight-v0`, `admitted_at` `2026-09-23T00:49:43Z`, and the
full sha256 above. Reciprocal identities on the synthetic extreme-favorite
book, feebook `order_fee` bound to
`astra.r1p1.feebook.claude_order_level_ceil.v1` with series resolution
`default_unknown_series`, rails freshness / maker-credit refuse / queue-bin
labels matching the Q6-`000` instrument helpers, completed-profit refused
without the examiner fee channel, shadow formula ids refused, scorecard
promotion refused, live orders refused, capital modes A1, A2, and A3 refused,
unpinned production orderbooks refused, feebook and rails trees unchanged
versus their pin commits, and the other listed cores unchanged versus
`d8957a0061ba601a11b3b03145b1516937239988` all passed. In-memory label rows
used the admitted panel as the schema and
`fixtures/synthetic_orderbooks.json` as the books (`synthetic_schema_standin`).
Those rows were not copied into the freeze files.

## Limitations

- This check is code verification. It is not Examiner scoring. C1 stays
  `NOT_SCORED` and the freeze stays `FROZEN_NOT_RUN`.
- In-memory reciprocal, fee, and rails labels were not copied into the freeze
  files. `volume_fp` and `open_interest_fp` stay null. Scout page-sample sums
  in the kernel were not copied onto the panel.
- No live order client was added. The feebook lab, the rails lab, the `000`
  honesty lab, the hygiene lab, the queue-fragility lab, the capital-structure
  lab, and the Q1–Q7 trees were not modified. Q6-`000` was not retuned.
- `results` and `pnl` stay null. No strategy EV is recorded.

No profit is reported.
