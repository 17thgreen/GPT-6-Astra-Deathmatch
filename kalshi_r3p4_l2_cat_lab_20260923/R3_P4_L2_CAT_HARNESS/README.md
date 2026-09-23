# R3-P4 L2-CAT harness bundle

Same freeze bytes as `packets/R3_P4_L2_CAT_HARNESS/`.
`results` and `pnl` stay null. This bundle is not an Examiner score.

`lab/governance/astra/packets/` is not in this checkout. This directory is
the lab-side copy of the packet.

The harness freeze in this directory is sha256
`3fc370d93f0ea42864f7bf482d7f6515254999c76e2fc4477df1273bfcdc051f`.
The parent kernel in this directory is sha256
`4a4e7cc61efcb436955c566edc7a2681603a014725bc79047f9d825392064528`.
The panel stub in this directory is sha256
`7477e023ab70c59a6739650155ddb9d77077766e3afd80443e540d60b5a86cbb`
(4 events, 6 markets, sports 4, nonsports 2). All three match the
attached conductor files.

| File | Role |
|---|---|
| `R3_P4_L2_CAT_HARNESS_FREEZE_2026-09-23_2259.md` | Harness freeze, conductor sha256 verified |
| `R3-P4_L2_SHAPE_LONGSHOT_DEPTH_FREEZE_KERNEL_2026-09-22.md` | Parent kernel, conductor sha256 verified |
| `panel_stub.json` | Conductor panel stub, `admitted_at` null |
| `SEED_SUMMARY.json` | Import-only seed summary, not a second panel |
| `CONDUCTOR_FROZEN_EXPERIMENT.json` | Conductor stamp, `results` and `pnl` null |
| `FROZEN_EXPERIMENT.json` | Lab freeze record, `results` and `pnl` null |
| `results.json` | Instrument fields null until Examiner |
| `results/EMPTY_RESULTS.json` | Same empty scorecard bytes |

Lab: `kalshi_r3p4_l2_cat_lab_20260923/`.
Capture path: `lab/astra-capture/r3-p4-l2-shape/panel_stub.json`.
Not a live-order lab.
