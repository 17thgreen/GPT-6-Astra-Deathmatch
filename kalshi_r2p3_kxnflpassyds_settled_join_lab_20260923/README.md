# R2P3 KXNFLPASSYDS settled-resolution join harness

Status: hypothesis committed, then source frozen. The unit page is
`results/UNIT_RESULTS.md`. `python3 -m unittest -v tests.test_orchestrator`
ran 10 tests in 0.157s. Recorded at 2026-09-23T21:24:42Z. Result: OK.
Failures: 0. Errors: 0. That page is not profit and not an Examiner pass.
`EXPERIMENT_SPEC.md` is the hypothesis.
`FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.
`results/EMPTY_RESULTS.json` keeps `results`, `pnl`, `settled_join_n`,
`occurrence_match_n`, and `admit_ready_flag` null.

This lab is measurement-only. Feature family R2P3-RJ. The only knob is
`join_gate`: J0 `nonempty_result_required` and J1
`occurrence_datetime_match`. The scout pin says settled nonempty
`result` N=20. That pin is not `settled_join_n`. The settled list on
the attached reget is HTTP 200 with limit 20 and a cursor present.
Markets past that cursor are not invented. The finalized list and the
events closed/settled lists stay the honest 429 gaps. The close-window
query stays the honest 400 gap. Parent SEP27 prop-ladder seeds stay
active with a null `result`. The panel stub `market_tickers` stay
empty. `admitted_at` stays null. This lab does not run `admit.py`.
This is orthogonal to R2-P3 prop-ladder and PASSYDS-PROP. It is not a
reopen of Cap-SR, C3-RJ, C5-RJ, R3P3-RJ, NHL-RJ, or S4-RJ.

Attached bytes are also at
`lab/governance/astra/packets/`,
`lab/astra-capture/r2-p3-prop-slate/settled_reget_2026-09-23.json`,
`lab/astra-science/kalshi_r2p3_kxnflpassyds_settled_join_lab_20260923/`,
and `packets/R2P3_KXNFLPASSYDS_SETTLED_JOIN_HARNESS/`.
The capture `panel_stub.json` is the existing file and is not rewritten.

- Freeze sha256 `9ad3b0112243c1020aec2bd6ef0df15011b065c30aa691a988da02eb08be1e0b`
- Scout reget sha256 `2c3664ac240887026076a84e451ca798e0c2d10d42bdaf61a9a83844881681e5`
- Seed summary sha256 `534a617bc3f18be501c07237d261e945b1bcf0301ac956cddae46e0431b75cd3`
- Panel stub sha256 `70e879e8738d033f392d821849dee3537af3e7b8a916670779d238f78ce098be` (`2026-09-22.r2-p3-prop-slate-v0`, `admitted_at` null)
- Settled reget sha256 `2ce8426edb4ee5053f63bf2fe1439dbd046978eb76afa1e0537b17cca9b8b0e4`
- Accept sha256 `e5218cf2511607211ec1d825a9dad36abaee3d9cfda24488524c3d6bcbe3a565`

Feebook and rails commits are fixed path pins and are not imported.
No fee arm. No live orders. No Logan keys.

From this directory, Python 3 standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

No Logan keys. No live orders. A passing unit run is not an Examiner score.
