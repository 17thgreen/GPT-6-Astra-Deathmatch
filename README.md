# GPT-6-Astra-Deathmatch

A reproducible sports prediction-market research lab for Logan's Kalshi bot project.
Research source, frozen protocols, results, failed hypotheses and execution audits
are preserved here. No live order-enabled strategy has been validated or deployed.

## Current result

The Q6 simplification screen selected the core allocator with its three optional
features disabled. On 31 repeatedly examined NFL games, one shared $5,000 account,
250-contract event cap and assumed early queue of 3,300, completed simulated net
was **$345.24**, versus **$201.52** for the original router. At queue 10,000 it was
$75.90 versus $10.35. These are hypothetical historical executions, not live P&L.

The extra two-sided flow gate, cash earmark and portfolio ranking were unnecessary
to retain the improvement on this sample. Common budgeting, quote sizing,
offset-order handling and the chosen-pair margin check remain bundled.

Start with [Q6 results](nfl_factorial_lab_20260921/NFL_Allocation_Factorial_Results.md),
[the experiment registry](docs/EXPERIMENT_REGISTRY.md), and
[the next experiment](docs/NEXT_EXPERIMENT.md).

## Research history

| Directory | Work |
|---|---|
| `stern_lab` | Brownian/Stern adaptation, settlement corrections and second-round research |
| `strategy_review_20260921` | Original maker audit and strategy ranking |
| `maker_replay_round2` | Repaired historical execution replay |
| `nfl_queue_lab_20260921` | Q1 queue preservation, routing and queue stress |
| `nfl_completion_lab_20260921` | Q2 pair gating and inventory completion |
| `nfl_measurement_lab_20260921` | Q3 public collection, measurement and forward admission |
| `nfl_timing_lab_20260921` | Q4 size, early entry, stability and event-cap experiments |
| `nfl_adaptive_lab_20260921` | Q5 adaptive policies and capital controls |
| `nfl_factorial_lab_20260921` | Q6 eight-combination allocation study |
| `nfl_paircheck_lab_20260922` | Q7 chosen-pair cost check; frozen, not run |
| `nfl_prospective_recorder_20260922` | GET-only prospective recorder; reviewed, not deployed |
| `kalshi_c1_kxufcfight_honesty_lab_20260922` | C1 UFC fee+queue honesty bakeoff. Scorecard null. Admitted panel bytes not in this checkout |
| `kalshi_soft_blended_reserves_000_lab_20260923` | Cap-SR soft-policy measurement on the A2 substrate. Scorecard null. Not a promotion claim |
| `kalshi_r3p3_fl_maker_taker_lab_20260923` | R3-P3 maker/taker and 10¢ favorite–longshot bands. Supersedes draft PR15. Measurement only. Lee-Ready refused. Scorecard null. 14 unit tests green |
| `kalshi_cap_sr_effects_000_lab_20260923` | Cap-SR-FX effects path on Q6-000. Fixture stress only. Imports Cap-SR soft policies. Scorecard null. Not a second Cap-SR lab |
| `kalshi_s5_mve_filllegs_lab_20260923` | S5 KXMVECROSSCATEGORY fill-vs-legs harness. Feature family MVE-FL. Leg-mid knob only. Scorecard null. RFQ out of scope. 8 unit tests green |
| `kalshi_s4_ncaaf_feequue_lab_20260923` | S4 KXNCAAFGAME fee+queue honesty harness. Feature family NCAAF-FQ. Native taker partition and content-fresh bins. Lee-Ready refused. Scorecard null. Conductor freeze bytes were not in this checkout |
| `kalshi_r3p4_l2_cat_lab_20260923` | R3-P4 L2-CAT sports-versus-nonsports harness. Feature family L2-CAT. Category-slice knob only. Scorecard null. 7 unit tests green |
| `kalshi_r2p5_sot_id_lab_20260923` | R2-P5 SOT-ID kickoff SoT identity harness. Feature family SOT-ID. Audit-slice knob only. Scorecard null. 8 unit tests green |
| `kalshi_c1_empty_ob_lab_20260923` | C1 EMPTY-OB empty-orderbook refuse harness. Feature family EMPTY-OB. One gate: refuse scorecard or wait for fresh depth. Scorecard null. 7 unit tests green |
| `kalshi_c2_kxnhlgame_feequue_lab_20260923` | C2 KXNHLGAME fee+queue honesty harness. Feature family NHL-FQ. Native taker partition and content-fresh bins. Lee-Ready refused. Scorecard null. 12 unit tests green |
| `kalshi_c4_kxcpi_feequue_lab_20260923` | C4 KXCPI fee+queue honesty harness. Feature family CPI-FQ. Native taker partition and sparse-24h / missing-occurrence refuse bins. Lee-Ready refused. Scorecard null. 12 unit tests green |
| `kalshi_atp_kxatpmatch_feequue_lab_20260923` | ATP KXATPMATCH fee+queue honesty harness. Feature family ATP-FQ. Native taker partition and content-fresh bins. Lee-Ready refused. Missing occurrence_datetime left as counted. Scorecard null. Hypothesis committed before the unit outcome |

Historical source files are imported without refactoring so their original hashes
and regression anchors retain meaning. Archive READMEs may refer to their original
standalone kit; the repository's artifact policy below applies to this checkout.

## Run the current unit suite

Python 3.12, standard library:

```bash
cd nfl_factorial_lab_20260921
python -m unittest -v test_replay_v2 test_queue_policies test_completion test_timing test_adaptive test_factorial test_analysis
```

The imported Q6 run passed 94 unit tests, 36 independent financial-ledger checks,
and 10 exact prior fill/order-ledger regressions. Full replay/ledger verification
requires the indexed external inputs and compressed ledgers; unit tests do not.

## Data and provenance

Code, protocols, reports, JSON summaries, frozen hashes and tests are in Git.
Large/binary captures, normalized data and compressed ledgers remain in the
previously delivered research kits. `provenance/ARCHIVES.json` identifies kits by
filename, size and SHA-256; `EXTERNAL_ARTIFACTS.json` indexes omitted file bytes.
These indexes are not downloads. Obtain the matching kit from the project owner
or the existing project deliverables; run `scripts/restore_kit.py` to validate and
restore the indexed files. No claim is made that cloning alone supplies all data.

No third-party repository checkout, credentials, private communications or unrelated
project files are imported. No license for upstream source/data is inferred;
source manifests retain attribution and provenance for their original inputs.

## Working rule

Commit the hypothesis and frozen specification before execution, then commit the
implementation checkpoint and verified results with a clear status. Preserve
failed attempts and negative outcomes. See [AGENTS.md](AGENTS.md).

The next research step is an isolated test of the **actual chosen-pair price
check**, with the original router's timing and sizing held fixed. That check
is frozen and not run in `nfl_paircheck_lab_20260922`. Fresh-game
validation and a durable public recorder remain separate unmet gates. A
reviewed prospective recorder, not deployed by this commit, is in
`nfl_prospective_recorder_20260922/`. PHI@CHI's full T−7d window is already
missed and is not backfilled.
