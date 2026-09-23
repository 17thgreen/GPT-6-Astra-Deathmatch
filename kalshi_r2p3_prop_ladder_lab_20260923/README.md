# R2-P3 KXNFLPASSYDS prop-ladder fee+queue honesty harness

Status: hypothesis committed, then source frozen. The unit page is
`results/UNIT_RESULTS.md`. `python3 -m unittest -v tests.test_orchestrator`
ran 8 tests in 0.046s at 2026-09-23T16:15:40Z. Result: OK. Failures: 0.
Errors: 0. That page is not profit and not an Examiner pass.
`EXPERIMENT_SPEC.md` is the hypothesis.
`FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.
`results/EMPTY_RESULTS.json` keeps `cross_strike_residual_rms`,
`latent_fit_fragmentation`, `maker_credit_floor_zero_n`, `fresh_strike_n`,
and `settled_join_n` null.

This lab is measurement-only. Feature family PROP-LQ. The kernel series is
`KXNFLPASSYDS`, with sibling events `KXNFLRECYDS` and `KXNFLRSHYDS` on the
same slate. The only knob is the residual monotone family: R2P3A0
`isotonic` and R2P3A1 `logit_monotone`. Lee-Ready is refused on every
input. ATL@GB is refused. The slate is Sun 2026-09-27 LAC@BUF + BAL@DAL.
Q7 Arm B stays killed. QF, Cap-SR, Cap-SR-FX, and `000` retune stay closed.
Q, Cap-SR, Cap-SR-FX, C3, C5, R3-P3, S4, and S5 are not edited.

`lab/governance/astra/packets/` is not in this checkout. The conductor-box
freeze, parent kernel, and panel stub on this branch match the conductor
sha256 claims. Copies:

- `R2_P3_KXNFLPASSYDS_PROP_LADDER_HARNESS_FREEZE_2026-09-23.md` sha256 `f8335eb0080cb1f82b1fad512509749134dd0e6e41ed85795347c3476796e87a` (lab root, lab bundle, `packets/`, and `packets/R2_P3_PROP_LADDER_HARNESS/`)
- `R2-P3_KXNFLPASSYDS_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md` sha256 `a30108f658359590e170c73ea00d1a1f0852d5751cb15c9f2a9c6389f4dd3eaa` (same four paths)
- `lab/astra-capture/r2-p3-prop-slate/panel_stub.json` sha256 `70e879e8738d033f392d821849dee3537af3e7b8a916670779d238f78ce098be` (also the lab bundle and `packets/R2_P3_PROP_LADDER_HARNESS/`)
- `R2_P3_PROP_LADDER_HARNESS/`
- `packets/R2_P3_PROP_LADDER_HARNESS/`

Panel stub: `panel_version` `2026-09-22.r2-p3-prop-slate-v0`, `admitted_at`
null, 6 events, empty `market_tickers`, volume fields null.

Fee pin `22371178cb2663250b4762f328069571c48cb551`.
Rails pin `6a28e0d6254327ea4e6451c781bec56215ac6cac`.
Those trees are not edited.

From this directory, Python 3 standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

No Logan keys. No live orders. A passing unit run is not an Examiner score.
