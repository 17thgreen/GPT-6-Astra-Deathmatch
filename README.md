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
| `nfl_paircheck_lab_20260922` | Q7 chosen-pair cost check. Later registry rows record a Q7 Arm B kill and frozen rehab pass 1 (PR38) and pass 2 (PR47), with desk-verified `q3300_d0.25_B.json` / `q3300_d0.25_D.json` summary hashes. In-tree `results/NOT_RUN.json` stays `NOT_RUN_INPUTS_MISSING` (`scenarios_executed` 0). The reconciliation memo is not a score |
| `nfl_q7_rehab_p1_cadence_20260923` | Q7 Arm B rehab pass 1. One knob: 600s admission cadence on new paired exposure. Scorecard null. Parent Q7 is imported, not edited |
| `nfl_prospective_recorder_20260922` | GET-only prospective recorder (ADMIT-1); deployed and running since 2026-09-22. Fleet evidence: `17thgreen/Grokbot-Deathmatch-Dedicated-Repo` commit `1825ec8c` |
| `kalshi_c1_kxufcfight_lab_20260922` | C1 KXUFCFIGHT admit-wire scaffold. Clock accepts the admitted panel. Scorecard null. 16 unit tests green |
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
| `kalshi_atp_kxatpmatch_feequue_lab_20260923` | ATP KXATPMATCH fee+queue honesty harness. Feature family ATP-FQ. Native taker partition and content-fresh bins. Lee-Ready refused. Missing occurrence_datetime left as counted. Scorecard null. 13 unit tests green |
| `kalshi_eth_kxeth15m_feequue_lab_20260923` | ETH KXETH15M fee+queue honesty harness. Feature family ETH-FQ. Native taker partition and content-fresh bins. Lee-Ready refused. Scorecard null. Not live crypto trading |
| `kalshi_c3_kxhighny_settled_join_lab_20260923` | C3-RJ KXHIGHNY settled-resolution join harness. One knob: join_gate. J0 nonempty result required. J1 occurrence datetime match. Scorecard null. CHI B66.5 429 gap left empty. admit.py not run |
| `kalshi_r3_p2_queue_position_lab_20260923` | R3-P2 queue_position calibration ingest. Series schema `{meta, samples[]}`. Desk series pinned sha256 `74ef9a9bb54054691e26b7b752568c8e833f51d21292034b1f40b9f3ca4ba8b4`, samples_n 38, leftover_resting `no`. Scorecard null. Status SAMPLE_INGESTED_CALIBRATION_NOT_RUN. Calibration not run. 6 unit tests green |
| `kalshi_c5_kxbtc15m_settled_join_lab_20260923` | C5-RJ KXBTC15M settled-resolution join harness. One knob: join_gate. J0 nonempty result required. J1 occurrence datetime match. Scorecard null. Scout N=20 is not settled_join_n. Finalized and closed list 429 gaps left empty. admit.py not run. Not live crypto trading. 10 unit tests green |
| `kalshi_r3p3_fl_settled_join_lab_20260923` | R3P3-RJ FL maker/taker settled-resolution join harness. One knob: join_gate. J0 nonempty result required. J1 occurrence datetime match. Scorecard null. Scout N=20 is not settled_join_n. CHI settled list and NY open list 429 gaps left empty. admit.py not run. 10 unit tests green |
| `kalshi_c1_kxufcfight_settled_join_lab_20260923` | C1-RJ KXUFCFIGHT settled-resolution join harness. One knob: join_gate. J0 nonempty result required. J1 occurrence datetime match on the four admitted parent seeds. Scorecard null. Cited freeze, ACCEPT, 1750 ET pin, and scout reget are present (PR49). `digest_all_match_claimed` is true. Examiner status is `READY_NOT_SCORED` (`stub_ready` true, `NOT_SCORED`). Declared scout N=4 is not settled_join_n. admit.py not run. 10 unit tests green |
| `kalshi_c4_kxcpi_settled_join_lab_20260924` | C4-RJ KXCPI settled-resolution join harness. One knob: join_gate. J0 nonempty result required. J1 occurrence datetime match, with expected_expiration_time fallback labeled per row when occurrence_datetime is null. Scorecard null. Scout N=25 is a pin and is not settled_join_n. admitted_at stays null. admit.py not run. CPI-FQ stays closed. 10 unit tests green |

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
is frozen in `nfl_paircheck_lab_20260922`. The registry records a Q7 Arm B
kill (Cap-SR row and S4 KXNCAAFGAME fee+queue row) and records frozen rehab
pass 1 (PR38) and pass 2 (PR47), with desk-verified `q3300_d0.25_B.json` sha256
`370ccbcf342db59aa1697d448d3274791cf17c015d8e9eead17d788fbe79ffb5` and
`q3300_d0.25_D.json` sha256
`fc38cfbc134ca313a6cd2b8763ef49c3a56f6b5cc763c50f82e2b4545cda898f`. The
in-tree pair-check result file remains `NOT_RUN_INPUTS_MISSING`
(`scenarios_executed` 0). Rehab result files in this checkout also record
`scenarios_executed` 0. The read-only reconciliation memo
`lab/governance/astra/packets/q7_reconciliation_20260924/Q7_RECONCILIATION_MEMO_2026-09-24.md`
(PR51, on main) is documentation and is not a score. This paragraph does not
report Q7 P&L. Fresh-game validation remains a separate gate. The prospective
recorder (ADMIT-1) in `nfl_prospective_recorder_20260922/` has been deployed
and running since 2026-09-22. Fleet evidence is
`17thgreen/Grokbot-Deathmatch-Dedicated-Repo` commit `1825ec8c`. PHI@CHI's
full T−7d window is already missed and is not backfilled.
