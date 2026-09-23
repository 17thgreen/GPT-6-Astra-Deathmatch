# R2-P3 KXNFLPASSYDS prop-ladder fee and queue honesty

September 23, 2026. This file is the hypothesis. It is committed before a
unit-test outcome is recorded. No figure in this document is a trading
result. Q6 outcomes that already exist are not re-labeled as evidence from
this probe. This is measurement-only NFL yards multi-strike fee and queue
honesty. Feature family PROP-LQ.

## Placement

The harness freeze on this branch is
`R2_P3_KXNFLPASSYDS_PROP_LADDER_HARNESS_FREEZE_2026-09-23.md`, sha256
`f8335eb0080cb1f82b1fad512509749134dd0e6e41ed85795347c3476796e87a`.
That digest matches the conductor claim. The same bytes sit at the lab
root, the lab bundle, `packets/`, and
`packets/R2_P3_PROP_LADDER_HARNESS/`.

The parent kernel on this branch is
`R2-P3_KXNFLPASSYDS_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md`, sha256
`a30108f658359590e170c73ea00d1a1f0852d5751cb15c9f2a9c6389f4dd3eaa`.
That digest matches the conductor parent claim on the same four paths.

The panel stub is `lab/astra-capture/r2-p3-prop-slate/panel_stub.json`,
`panel_version` `2026-09-22.r2-p3-prop-slate-v0`, sha256
`70e879e8738d033f392d821849dee3537af3e7b8a916670779d238f78ce098be`.
`admitted_at` is null. The file is the conductor stub: 6 events on Sun
2026-09-27 LAC@BUF + BAL@DAL, with empty `market_tickers` and null
`volume_fp`, `volume_24h_fp`, `open_interest_fp`, `results`, and `pnl`.
The same bytes are copied into the lab bundle and
`packets/R2_P3_PROP_LADDER_HARNESS/`. `panel_admitted.json` is absent and
is preferred when it appears.

`EXPERIMENT_SPEC.md` is the lab hypothesis. It is not a second freeze.
`lab/governance/astra/packets/` is not in this checkout.

`FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.
`results/EMPTY_RESULTS.json` keeps `cross_strike_residual_rms`,
`latent_fit_fragmentation`, `maker_credit_floor_zero_n`, `fresh_strike_n`,
and `settled_join_n` null.

The conductor stamp `CONDUCTOR_FROZEN_EXPERIMENT.json` is sha256
`9c4919c968a2cb1e9c70995ebc454da709109e2866ffb02668c9e803570f31bc`.
The adversary refuse-bind is sha256
`2c56d92d1b18544c640eedd7e76ae5978d3c7108a8c99faeb2a21364a92d6fad`.

## One knob

Residual monotone family, with feebook and rails fixed:

| Arm | Family |
|---|---|
| R2P3A0 | `isotonic` — monotone isotonic fit across strikes. Lee-Ready refused |
| R2P3A1 | `logit_monotone` — monotone fit in logit space, then the probability scale. Rails labels only. No fee invent |

Fee pin `22371178cb2663250b4762f328069571c48cb551` (import only).
Rails pin `6a28e0d6254327ea4e6451c781bec56215ac6cac` (import only).

Markout horizon is not the knob. `1m`, `5m`, and `15m` stay refused as arms.

## Slate

Sun 2026-09-27 LAC@BUF (`2026-09-27T20:00:00Z`) and BAL@DAL
(`2026-09-27T23:25:00Z`) only. Series on the stub: `KXNFLPASSYDS`,
`KXNFLRECYDS`, `KXNFLRSHYDS`. ATL@GB is excluded. The stub does not contain
admitted market tickers, cohort counts, or volume.

`fixtures/synthetic_mid_ladder.json` is a code-path stand-in with player ids
`SYNTHETIC_A` and `SYNTHETIC_B`. It is not a panel fill and not an Examiner
score.

## What this run does not claim

No live orders. No Logan keys. No invented fills, cohort, volume, or PnL.
No Q6-`000` retune. No queue-fragility reopen. No Cap-SR reopen. No
Cap-SR-FX reopen. No `admit.py`. Q7 Arm B stays killed. Q, Cap-SR,
Cap-SR-FX, C3, C5, R3-P3, S4, S5, feebook, and rails labs are not edited.
A later unit page is code verification only, not an Examiner score.
