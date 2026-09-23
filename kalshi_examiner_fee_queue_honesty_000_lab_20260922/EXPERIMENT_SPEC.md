# Examiner-channel fee and queue honesty on Q6-000

September 22, 2026. This file is the hypothesis. It is committed before source is
frozen and before any unit-test outcome is recorded. No figure in this document
is a trading result. Q6 outcomes that already exist are not re-labeled as
evidence from this lab.

## Pin lock

The canonical freeze is
`packets/EXAMINER_FEE_QUEUE_HONESTY_000_FREEZE_2026-09-22.md`. Its sha256 is
`4799642e54cf233a925697e00c5a9e29f5cb39070962a2e011f0fbe090c169f2`.
The conductor kernel is `packets/EXAMINER_FEE_QUEUE_HONESTY_000/freeze.json`.
`EXPERIMENT_SPEC.md` is the lab hypothesis. It is not a second freeze.

This is one Examiner channel. Fee hygiene and queue fragility are not two
packets. The channel consumes the pick A hygiene join inside
`kalshi_r2p1_hygiene_000_lab_20260922` (R2-P1 join at
`79800a82b8ad2c1e10f614f69fd7105d11e0d041`) and the pick B queue-fragility
join inside `kalshi_queue_fragility_000_lab_20260922` (QF join at
`7026be5104cd00cabcf9b34154506a76b2768b8a`).

Fee path, fixed: `kalshi_feebook_lab_20260922` at
`22371178cb2663250b4762f328069571c48cb551`.

Rails path, fixed: `kalshi_rails_lab_20260922` at
`6a28e0d6254327ea4e6451c781bec56215ac6cac`.

## Placement

`kalshi_feebook_lab_20260922`, `kalshi_rails_lab_20260922`,
`hygiene.py`, and `queue_fragility.py` are frozen cores. This lab imports
the two fixture-join modules and does not edit those cores. It does not add
a second hygiene lab or a second queue-fragility lab. The new directory is
`kalshi_examiner_fee_queue_honesty_000_lab_20260922`.

## Question

Holding strategy Q6-`000`, the shared 5000 USD account, and one fills stream,
does one thin orchestrator do all of the following on a code check:

1. Import `kalshi_r2p1_hygiene_000_lab_20260922/fixture_join.py` and
   `kalshi_queue_fragility_000_lab_20260922/fixture_join.py` and call both
   on the same fill path and the same order path.
2. Prefer the production pair
   `nfl_factorial_lab_20260921/results/q3300_d0.25_000_fills.jsonl.gz` and
   its matching orders when both files exist and match the pinned sha256
   `9d56f5d3c599e092606be9f4a1ad41ae8baabff4921d3d722adf0b57ac944a3f` and
   `c390801b9a7cf6d182d2d097123ed944792980524a7975e6e59a904a530f4b1c`.
3. When that gzip pair is absent from the checkout, read one synthetic schema
   stand-in through both joins, and still leave the scorecard null.
4. Refuse `write_scorecard` when any scorecard field is non-null, and refuse
   to store a scorecard in the freeze files in either case.
5. Leave these fields null in `FROZEN_EXPERIMENT.json` and
   `results/EMPTY_RESULTS.json`: `fee_delta_vs_inherited_model`,
   `freshness_gap_sec`, `queue_bin_mismatch_rate`, `fill_rate_delta_vs_q3300`,
   `adverse_queue_exposure`, `participation_stress_gap`, `results`, and `pnl`.

This is a code-verification question. It is not a Q6 tape walk and not live
trading. Unit tests may show that both joins label the same rows in memory.
They may not copy those labels into the freeze files, and they may not invent
walk P&L.

## Constants

| Pin | Frozen value |
|---|---|
| Strategy pointer | Q6 label `000` |
| Shadow file | `nfl_factorial_lab_20260921/SHADOW_CANDIDATE_FREEZE.json` sha256 `b55ff36cb161c824a3d1b490795c8ac6891f01489456f61da311ac863366af48` |
| Capital | Shared 5000 USD, mode `A1_shared_pool` only |
| Examiner formula | Imported through the joins from `feebook.EXAMINER_FORMULA_ID` |
| Empty outputs | `results/EMPTY_RESULTS.json` |
| Packet results | `packets/EXAMINER_FEE_QUEUE_HONESTY_000/results.json` |
| Hygiene join | `79800a82b8ad2c1e10f614f69fd7105d11e0d041` |
| QF join | `7026be5104cd00cabcf9b34154506a76b2768b8a` |

The shadow freeze file contains fee coefficients under its common config.
This lab does not read that object and does not copy those coefficients into
source. Examiner rates stay inside the feebook module, reached only through
the imported joins.

## Scorecard

One packet. The fields are:

| Field | Channel |
|---|---|
| `fee_delta_vs_inherited_model` | Fee / R2-P1 hygiene join |
| `freshness_gap_sec` | Rails content-fresh, through the hygiene join |
| `queue_bin_mismatch_rate` | Rails queue bin, through the hygiene join |
| `fill_rate_delta_vs_q3300` | Queue-fragility join |
| `adverse_queue_exposure` | Queue-fragility join |
| `participation_stress_gap` | Queue-fragility join |
| `results` / `pnl` | Null in this freeze |

`write_scorecard` does not write these fields. A non-null value is refused.

## Later question, not a result

This packet is the frame for one later Examiner question: whether an honest
queue treatment changes the modeled edge relative to the current model. The
queue fields sit on the same scorecard as the fee fields, with the same
refuse path. This file does not state a target ratio and does not record P&L.

## Do-not

1. No live orders.
2. No 000 retune. No A2. No A3. No Q7 reopen. No capital-structure reopen.
3. Do not invent filled metrics from synthetic rows into freeze files.
4. Do not split fee and queue into two Examiner packets.
5. Do not edit feebook, rails, `hygiene.py`, or `queue_fragility.py`.
6. The harsh twin `q10000_d0.25_000_*` stays unloaded. It is not a fee knob.

## Empty results

`packets/EXAMINER_FEE_QUEUE_HONESTY_000/results.json` and
`results/EMPTY_RESULTS.json` stay null. The freeze kernel records that the
production fills file was present on the freeze desk. A checkout that lacks
the gitignored gzip does not change that kernel and does not fill the
scorecard.
