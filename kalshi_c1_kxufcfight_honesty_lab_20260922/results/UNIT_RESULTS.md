# C1 KXUFCFIGHT honesty unit results

September 23, 2026. This file records a code check of the UFC fee and queue
harness after the source freeze. It is not a simulated trading run and not
live validation. `FROZEN_EXPERIMENT.json` and `results/EMPTY_RESULTS.json`
still have every measurement field, `results`, and `pnl` null. No
completed-net figure is reported.

Kernel sha256
`a191c9b3f71030445d1d32684feb6dc1bf09abb7e09403d5dbdf1927eafc63c9`.
`panel_version` `2026-09-22.c1-kxufcfight-v0`. Clock stamp
`2026-09-23T00:49:43Z`. Admitted-panel sha256 prefix `24426d80`.
R1-P1 `22371178cb2663250b4762f328069571c48cb551`.
R1-P5 `6a28e0d6254327ea4e6451c781bec56215ac6cac`.

## Command

From `kalshi_c1_kxufcfight_honesty_lab_20260922`, Python 3.12.3, standard
library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

Ran 12 tests in 0.026s. Result: FAILED. Failures: 2. Errors: 0.

The two failures are `test_binding_pins_the_admitted_panel_and_the_instruments`
and `test_admitted_panel_is_the_subject_and_the_stub_is_refused`. Both stop
because `lab/astra-capture/c1-kxufcfight/panel_admitted.json` is not in this
checkout. The harness does not invent that file. Its sha256 was not computed
here, so the prefix `24426d80` is not verified against bytes.

The ten checks that passed are the predeclared ones that do not need those
bytes: reciprocal identities on the synthetic extreme-favorite book, feebook
`order_fee` bound to `astra.r1p1.feebook.claude_order_level_ceil.v1` with
series resolution `default_unknown_series`, rails freshness / maker-credit
refuse / queue-bin labels matching the Q6-`000` instrument helpers,
completed-profit refused without the examiner fee channel, shadow formula ids
refused, scorecard promotion refused, live orders refused, capital modes A1,
A2, and A3 refused, unpinned production orderbooks refused, feebook and rails
trees unchanged versus their pin commits, and the other listed cores unchanged
versus `d8957a0061ba601a11b3b03145b1516937239988`. Those label rows were built
from a stamped copy of the pre-admit stub plus `fixtures/synthetic_orderbooks.json`.
That stand-in is not `panel_admitted.json`.

## Limitations

- `panel_admitted.json` was absent. `panel_admitted_sha256` in
  `FROZEN_EXPERIMENT.json` stays null. The prefix `24426d80` is the pin the
  loader will require when the file is present.
- In-memory reciprocal, fee, and rails labels were not copied into the freeze
  files. `volume_fp` and `open_interest_fp` stay null. Scout page-sample sums
  in the kernel were not copied onto the panel.
- No live order client was added. The feebook lab, the rails lab, the `000`
  honesty lab, the hygiene lab, the queue-fragility lab, the capital-structure
  lab, and the Q1–Q7 trees were not modified. Q6-`000` was not retuned.
- `results` and `pnl` stay null. No strategy EV is recorded.

No profit is reported.
