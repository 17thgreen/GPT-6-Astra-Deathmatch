# R2-P5 SOT-ID kickoff SoT identity harness

September 23, 2026. This file is the hypothesis. It is committed before a
unit-test outcome is recorded. No figure in this document is a trading
result. Q6 outcomes that already exist are not re-labeled as evidence from
this probe. This is a measurement-only provenance gate. Feature family
**SOT-ID**.

## Placement

The harness freeze on this branch is
`R2_P5_SOT_ID_HARNESS_FREEZE_2026-09-23.md`, sha256
`0424455f062b7c46c7c6161b84fb7b29702719acc45bf6a61b4e8f16c5e26457`.
That digest is the sha256 of the attached Conductor-box file. The same
bytes sit at the lab root, the lab bundle, `packets/`, and
`packets/R2_P5_SOT_ID_HARNESS/`.

The parent Archivist accept is `R2-P5_SCHEMA_ACCEPT_2026-09-22.md`, sha256
`712e4771bf2783dbee1e4c553194cd2896a468184f2849f24e58c3eb350ff499`.

The ADMIT-1 SoT seed is
`R2-P5_SEED_INSTANCE_ADMIT1_SOT_ONLY_2026-09-22.json`, sha256
`1edfa91979ab5dac72e28cc5e2ad5ff08aab414b5574fe115f86fb7d85e2ac4b`.
It has 16 rows. Every row is `KXNFLGAME`, `window_clock_source` is
`kalshi_occurrence`, and `delta_kickoff_sec` is 10800.
`panel_version` is `2026-09-22.1-kalshi-occurrence-sot`.
`admit_stamp_utc` is `2026-09-22T21:18:13Z`. That stamp is the ADMIT-1
admit. This harness does not admit again.

The JSON schema is `r2_p5_admit_fields.schema.json`, sha256
`da7f6badd37d52fbd977681924379c3552f0dbfec94729d86ea411fb473ce53c`.

The PIT@CLE identity cite is
`PITCLE_HOLDOUT_IDENTITY_JOIN_HASH_FREEZE_2026-09-23.md`, sha256
`f5ca19f15940a80476d1590e506951df87df619160b477f1dff06cc3554cb520`.
It is a hash freeze, not a panel re-admit. The cite keeps
`KXNFLGAME-26OCT01PITCLE` and holdout kickoff `2026-10-02T00:15:00+00:00`.

`lab/governance/astra/` is not in this checkout. The schema accept prefers
`lab/governance/astra/registry/schemas/r2_p5_admit_fields.schema.json` and
`lab/governance/astra/packets/R2-P5_SCHEMA_ACCEPT_2026-09-22.md`. Those
directories are absent. The copies above are the bytes this lab pins.

`EXPERIMENT_SPEC.md` is the lab hypothesis. It is not a second freeze.

The conductor stamp `CONDUCTOR_FROZEN_EXPERIMENT.json` is sha256
`1ff111c61bbc518b176525fb40f538a229fc53b5c8460fae6f82929e0bbd4505`.
`results` and `pnl` on that stamp are null. `seed_rows` is 16.

`PRE_ACCEPT_EMPTY_RESULTS.json` is sha256
`b796bfbbb3e78142569befd6a69801caaa662ed92072807df4068d49624f2926`.
Its note is `pre-ACCEPT empty`. It omits `identity_join_ok_n` and
`external_odds_invent_refuse_n`. It is not the seed and not the scorecard.

## One knob

Audit slice, with the schema and the ADMIT-1 seed fixed.

| Arm | Slice |
|---|---|
| R2P5A0 | `sot_pin_match` — `sot_pin` equals `kalshi_occurrence_datetime`, and `window_clock_source` is `kalshi_occurrence`. A silent `holdout_mixed` clock is refused |
| R2P5A1 | `holdout_delta_bin` — `delta_kickoff_sec` is the occurrence-minus-holdout gap. The seed value is 10800. Invented odds or adverse fields while `external_odds_present` is false are refused |

Fee path, import only: `kalshi_feebook_lab_20260922` at
`22371178cb2663250b4762f328069571c48cb551`.
Rails path, import only: `kalshi_rails_lab_20260922` at
`6a28e0d6254327ea4e6451c781bec56215ac6cac`.
Adverse hedge fields stay null unless external odds are present. This seed
has `external_odds_path` null and `external_odds_present` false on every row.

## Question

Holding the R1-P1 feebook and the R1-P5 rails as import-only references,
does one harness do all of the following on a code check:

1. Load the attached ADMIT-1 SoT seed at the digests above, with 16 rows,
   all `kalshi_occurrence`, uniform `delta_kickoff_sec` 10800, and the
   ADMIT-1 stamp `2026-09-22T21:18:13Z`. Refuse a labeled recreation, an
   empty seed, and the pre-ACCEPT empty payload.
2. Run R2P5A0 and R2P5A1 as schema audits. Refuse a silent holdout mix,
   a `sot_pin` that differs from `kalshi_occurrence_datetime`, a holdout
   kickoff rewrite toward the SoT, and invented adverse numbers when
   `external_odds_present` is false.
3. Check the PIT@CLE row against the identity cite: event
   `KXNFLGAME-26OCT01PITCLE`, holdout kickoff unchanged, SoT
   `2026-10-02T03:15:00Z`, T−7d `2026-09-25T03:15:00Z`. Leave
   `identity_join_ok_n` null.
4. Leave `sot_pin_mismatch_n`, `holdout_mixed_refuse_n`,
   `delta_kickoff_sec_mode`, `identity_join_ok_n`,
   `external_odds_invent_refuse_n`, `results`, and `pnl` null.
5. Leave S2 and R2-P4 queued. Do not run `admit.py`. Do not open a second
   ADMIT-1 panel. Do not steal the ADMIT-1 poll. Do not read Logan keys.
   Do not place orders.

This is a code-verification question. It is not a tape walk, not an
Examiner score, and not live trading. The strategy pointer is null.

## Scorecard

Until Examiner opens the packet, each of these keys is present and null:

| Field | Meaning while null |
|---|---|
| `sot_pin_mismatch_n` | Rows whose `sot_pin` differs from `kalshi_occurrence_datetime` |
| `holdout_mixed_refuse_n` | Silent holdout/occurrence mixes refused |
| `delta_kickoff_sec_mode` | Mode of `delta_kickoff_sec` on the audited rows |
| `identity_join_ok_n` | PIT@CLE rows whose identity cite matched |
| `external_odds_invent_refuse_n` | Invented adverse/odds rows refused |
| `results` / `pnl` | Null in this freeze |

`write_scorecard` does not write these fields.

## Named refuses

| Refuse | Handling |
|---|---|
| Labeled recreation | Raised. The 16-row seed is the attached file |
| Empty seed | Raised. The pre-ACCEPT empty payload is in this class |
| Silent `holdout_mixed` | Raised when the window clock is mixed without `window_clock_source=holdout_mixed` |
| External odds invent | Raised when adverse fields are filled and `external_odds_present` is false |
| Holdout kickoff rewrite | Raised. PIT@CLE holdout stays `2026-10-02T00:15:00Z` |
| `admit.py` | Raised. This harness does not admit |
| Second ADMIT-1 panel | Raised. A different `admit_stamp_utc` is a competing admit |
| Poll steal | Raised. The recorder poll budget stays with ADMIT-1 |
| S2 / R2-P4 ungate | Raised. C1 smoke is still the gate |
| Logan keys / live orders | Raised |
| Q6-`000` retune, Cap-SR reopen, L2-CAT reopen, ATL@GB | Raised |

## Do-not

1. Do not edit feebook, rails, the ADMIT-1 recorder, L2-CAT, or the other
   sibling labs named in the freeze.
2. Do not invent odds or rewrite holdout kickoffs in place.
3. Do not treat a unit pass as an Examiner score.
