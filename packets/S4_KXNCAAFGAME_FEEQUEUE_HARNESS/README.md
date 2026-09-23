# S4-KXNCAAFGAME-FEEQUEUE-HARNESS packet bundle

`lab/governance/astra/packets/` is not in this checkout. This directory is
the governance bundle. The same bytes are copied beside the lab engine.

The harness freeze in this directory is sha256
`3318204bf6e962f4f3372dad8c0f302e62d85c26b855de7369718654d0114728`.
The parent kernel in this directory is sha256
`9e6556c150c726b679ac8393f1f5338cf983489259b0f34cdedf221c030be795`.
Both match the conductor claims. `FROZEN_EXPERIMENT.json` records those
digests and keeps `results` and `pnl` null.

| File | Role |
|---|---|
| `S4_KXNCAAFGAME_FEEQUEUE_HARNESS_FREEZE_2026-09-23.md` | Harness freeze, conductor sha256 verified |
| `S4_KXNCAAFGAME_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md` | Parent kernel, conductor sha256 verified |
| `FROZEN_EXPERIMENT.json` | `results` and `pnl` null |
| `results.json` | Instrument fields null until Examiner |
| `results/EMPTY_RESULTS.json` | Same empty scorecard bytes |

Lab: `kalshi_s4_ncaaf_feequue_lab_20260923/`.
Panel seed: `lab/astra-capture/s4-kxncaafgame/panel_stub.json`.
Not a live-order lab.
