# R2-P5-SOT-ID-HARNESS packet bundle

Same freeze bytes as `packets/R2_P5_SOT_ID_HARNESS/`.
`results` and `pnl` stay null. This bundle is not an Examiner score.

`lab/governance/astra/` is not in this checkout. This directory is the
lab-side copy of the packet. The schema accept prefers
`lab/governance/astra/registry/schemas/r2_p5_admit_fields.schema.json`.
That tree is absent, so the schema bytes are here.

| File | sha256 |
|---|---|
| `R2_P5_SOT_ID_HARNESS_FREEZE_2026-09-23.md` | `0424455f062b7c46c7c6161b84fb7b29702719acc45bf6a61b4e8f16c5e26457` |
| `R2-P5_SCHEMA_ACCEPT_2026-09-22.md` | `712e4771bf2783dbee1e4c553194cd2896a468184f2849f24e58c3eb350ff499` |
| `R2-P5_SEED_INSTANCE_ADMIT1_SOT_ONLY_2026-09-22.json` | `1edfa91979ab5dac72e28cc5e2ad5ff08aab414b5574fe115f86fb7d85e2ac4b` (16 rows) |
| `r2_p5_admit_fields.schema.json` | `da7f6badd37d52fbd977681924379c3552f0dbfec94729d86ea411fb473ce53c` |
| `PITCLE_HOLDOUT_IDENTITY_JOIN_HASH_FREEZE_2026-09-23.md` | `f5ca19f15940a80476d1590e506951df87df619160b477f1dff06cc3554cb520` |
| `CONDUCTOR_FROZEN_EXPERIMENT.json` | `1ff111c61bbc518b176525fb40f538a229fc53b5c8460fae6f82929e0bbd4505` |
| `PRE_ACCEPT_EMPTY_RESULTS.json` | `b796bfbbb3e78142569befd6a69801caaa662ed92072807df4068d49624f2926` (refused as a seed) |

Lab: `kalshi_r2p5_sot_id_lab_20260923/`.
Feature family SOT-ID. One knob: audit slice.
Not a live-order lab. Not a second ADMIT-1 panel.
