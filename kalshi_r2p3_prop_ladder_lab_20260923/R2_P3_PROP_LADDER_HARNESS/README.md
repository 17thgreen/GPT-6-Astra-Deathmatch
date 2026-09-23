# R2-P3 KXNFLPASSYDS prop-ladder harness bundle

Same freeze bytes as `packets/R2_P3_PROP_LADDER_HARNESS/`.
`results` and `pnl` stay null. This bundle is not an Examiner score.

`lab/governance/astra/packets/` is not in this checkout. This directory is
the lab-side copy of the packet.

The harness freeze in this directory is sha256
`f8335eb0080cb1f82b1fad512509749134dd0e6e41ed85795347c3476796e87a`.
The parent kernel in this directory is sha256
`a30108f658359590e170c73ea00d1a1f0852d5751cb15c9f2a9c6389f4dd3eaa`.
The panel stub in this directory is sha256
`70e879e8738d033f392d821849dee3537af3e7b8a916670779d238f78ce098be`
(6 events). All three match the conductor claims.

| File | Role |
|---|---|
| `R2_P3_KXNFLPASSYDS_PROP_LADDER_HARNESS_FREEZE_2026-09-23.md` | Harness freeze, conductor sha256 verified |
| `R2-P3_KXNFLPASSYDS_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md` | Parent kernel, conductor sha256 verified |
| `panel_stub.json` | Conductor panel stub, 6 events, `admitted_at` null |
| `CONDUCTOR_FROZEN_EXPERIMENT.json` | Conductor stamp, `results` and `pnl` null |
| `R2-P3_ADVERSARY_REFUSE_BIND_2026-09-22.md` | Adversary refuse-bind, copied verbatim |
| `FROZEN_EXPERIMENT.json` | Lab freeze record, `results` and `pnl` null |
| `results.json` | Instrument fields null until Examiner |
| `results/EMPTY_RESULTS.json` | Same empty scorecard bytes |

Lab: `kalshi_r2p3_prop_ladder_lab_20260923/`.
Capture path: `lab/astra-capture/r2-p3-prop-slate/panel_stub.json`.
Not a live-order lab.
