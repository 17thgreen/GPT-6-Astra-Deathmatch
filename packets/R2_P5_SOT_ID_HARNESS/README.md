# R2-P5-SOT-ID-HARNESS packet bundle

`lab/governance/astra/` is not in this checkout. This directory is the
packets-side copy. The same authentic bytes sit in
`kalshi_r2p5_sot_id_lab_20260923/R2_P5_SOT_ID_HARNESS/` and at the lab root.
Top-level copies of the five conductor files also sit in `packets/`.

| File | Role |
|---|---|
| `R2_P5_SOT_ID_HARNESS_FREEZE_2026-09-23.md` | Harness freeze, sha256 `0424455f062b7c46c7c6161b84fb7b29702719acc45bf6a61b4e8f16c5e26457` |
| `R2-P5_SCHEMA_ACCEPT_2026-09-22.md` | Parent accept, sha256 `712e4771bf2783dbee1e4c553194cd2896a468184f2849f24e58c3eb350ff499` |
| `R2-P5_SEED_INSTANCE_ADMIT1_SOT_ONLY_2026-09-22.json` | ADMIT-1 SoT seed, sha256 `1edfa91979ab5dac72e28cc5e2ad5ff08aab414b5574fe115f86fb7d85e2ac4b`, 16 rows |
| `r2_p5_admit_fields.schema.json` | JSON schema, sha256 `da7f6badd37d52fbd977681924379c3552f0dbfec94729d86ea411fb473ce53c` |
| `PITCLE_HOLDOUT_IDENTITY_JOIN_HASH_FREEZE_2026-09-23.md` | PIT@CLE identity cite, sha256 `f5ca19f15940a80476d1590e506951df87df619160b477f1dff06cc3554cb520` |
| `CONDUCTOR_FROZEN_EXPERIMENT.json` | Conductor stamp, `results` and `pnl` null, `seed_rows` 16 |
| `PRE_ACCEPT_EMPTY_RESULTS.json` | Attached pre-ACCEPT payload. Refused as a seed and as a scorecard |
| `FROZEN_EXPERIMENT.json` | Lab freeze record, `results` and `pnl` null |
| `results.json` | Instrument fields null until Examiner |
| `results/EMPTY_RESULTS.json` | Same empty scorecard bytes |

Feature family SOT-ID. Scorecard fields stay null.
This packet does not ungate S2 or R2-P4.
