# GPT-6-Astra-Deathmatch

A reproducible sports prediction-market research lab for Logan's Kalshi bot project.
Research source, frozen protocols, results, failed hypotheses and execution audits
are preserved here. No live order-enabled strategy has been validated or deployed.

## Current result

September 22: [other-market update](market_access_lab_20260922/MARKET_UPDATE.md)
adds tested adapter components and a 28-event, 56-ticker public-book census.
50 usable snapshots; six retained timeouts. No non-NFL profitability claim.


Q8 joint routing is complete: both new variants improve the lighter-queue
headline but lose to Q7 under queue-10000 stress, so **Q7 remains selected**.
[Q8 results](nfl_joint_route_lab_20260921/Q8_RESULTS.md) preserve all twelve
comparisons. [Market expansion roadmap](market_portability/RESEARCH_ROADMAP.md)
covers queue access, profitability and rule-aware portability; the new payoff
checker passes eight focused tests. The user owns forward validation.


Q7 selects the original router plus a chosen-pair price guard as the simpler
shadow research candidate. On the same 31 reused NFL games and shared $5,000,
it earns completed simulated net **$354.33**, versus **$201.52** for the original
router and **$345.24** for the prior Q6 allocator at queue 3,300/.25s. It beats
both across all four frozen queue/delay scenarios. All sixteen ledgers reconcile;
eight unchanged controls reproduce exact Q6 fill/order histories; 115 tests pass.

The result supports paired-price admission as the main mechanism in the prior
allocator gain on these development data. It does not establish live execution
or fresh profitability. Full results: [Q7 report](nfl_pair_price_lab_20260921/Q7_RESULTS.md).
The original Q6 record and candidate remain unchanged.

Start with [the continuity handoff](docs/CONTINUITY_HANDOFF_2026-09-21.md),
[the registry](docs/EXPERIMENT_REGISTRY.md), and
[forward capture readiness](docs/FORWARD_CAPTURE_READINESS.md).

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
| `nfl_pair_price_lab_20260921` | Q7 chosen-pair guard isolation and simpler candidate |
| `nfl_joint_route_lab_20260921` | Q8 joint-route and rejected-pair recovery experiment |
| `market_portability` | Payoff compatibility, explicit profiles and sourced expansion roadmap |

Historical source files are imported without refactoring so their original hashes
and regression anchors retain meaning. Archive READMEs may refer to their original
standalone kit; the repository's artifact policy below applies to this checkout.

## Run the current unit suite

Python 3.12, standard library:

```bash
cd nfl_pair_price_lab_20260921
python -m unittest -v test_pair_policy test_q7_analysis test_replay_v2 test_queue_policies test_completion test_timing test_adaptive test_factorial test_analysis
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

The approved Q7 mechanism test is complete. Current authorized work is Q8 joint
routing, queue access, profitability and market portability. The user owns forward
validation; it does not block this research lane.
Neither a continuous recorder nor live trading is operating. Q7's large data and
ledger archive is indexed in its DATA_ARCHIVE.json and EXTERNAL_ARTIFACTS.json;
see DELIVERY_NOTES.md there for restoration without duplicating source code.
