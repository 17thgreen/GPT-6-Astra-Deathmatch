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

Q7 isolates the **actual chosen-pair price check** in
`nfl_paircheck_lab_20260922`. The 2×2 is implemented and frozen. The 16
historical scenarios have not been run, because the normalized event tape is
not in this clone. Fresh-game validation and a durable public recorder remain
separate unmet gates.
