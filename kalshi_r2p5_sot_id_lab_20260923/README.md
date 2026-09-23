# R2-P5 SOT-ID kickoff SoT identity harness

Status: hypothesis committed. Source and the unit page follow in later
commits on this branch. `EXPERIMENT_SPEC.md` is the hypothesis.
`results/EMPTY_RESULTS.json` keeps `sot_pin_mismatch_n`,
`holdout_mixed_refuse_n`, `delta_kickoff_sec_mode`, `identity_join_ok_n`,
`external_odds_invent_refuse_n`, `results`, and `pnl` null.

This lab is measurement-only. Feature family SOT-ID. The only knob is the
audit slice: R2P5A0 `sot_pin_match` and R2P5A1 `holdout_delta_bin`.
The seed is the attached ADMIT-1 SoT file, 16 rows, all
`kalshi_occurrence`, `delta_kickoff_sec` 10800. Scorecard fields stay null.

`lab/governance/astra/` is not in this checkout. Authentic copies:

| File | sha256 |
|---|---|
| `R2_P5_SOT_ID_HARNESS_FREEZE_2026-09-23.md` | `0424455f062b7c46c7c6161b84fb7b29702719acc45bf6a61b4e8f16c5e26457` |
| `R2-P5_SCHEMA_ACCEPT_2026-09-22.md` | `712e4771bf2783dbee1e4c553194cd2896a468184f2849f24e58c3eb350ff499` |
| `R2-P5_SEED_INSTANCE_ADMIT1_SOT_ONLY_2026-09-22.json` | `1edfa91979ab5dac72e28cc5e2ad5ff08aab414b5574fe115f86fb7d85e2ac4b` |
| `r2_p5_admit_fields.schema.json` | `da7f6badd37d52fbd977681924379c3552f0dbfec94729d86ea411fb473ce53c` |
| `PITCLE_HOLDOUT_IDENTITY_JOIN_HASH_FREEZE_2026-09-23.md` | `f5ca19f15940a80476d1590e506951df87df619160b477f1dff06cc3554cb520` |

The same five files sit at the lab root, `R2_P5_SOT_ID_HARNESS/`,
`packets/`, and `packets/R2_P5_SOT_ID_HARNESS/`.

Conductor stamp `CONDUCTOR_FROZEN_EXPERIMENT.json` sha256
`1ff111c61bbc518b176525fb40f538a229fc53b5c8460fae6f82929e0bbd4505`.
Pre-ACCEPT empty payload `PRE_ACCEPT_EMPTY_RESULTS.json` sha256
`b796bfbbb3e78142569befd6a69801caaa662ed92072807df4068d49624f2926`
is refused as a seed and as a scorecard.

Fee pin `22371178cb2663250b4762f328069571c48cb551` (import only).
Rails pin `6a28e0d6254327ea4e6451c781bec56215ac6cac` (import only).
Those trees are not edited. The ADMIT-1 recorder is not edited.

From this directory, Python 3 standard library, once the source commit is
present:

```bash
python3 -m unittest -v tests.test_orchestrator
```

A passing unit run is code verification. It is not an Examiner score.
