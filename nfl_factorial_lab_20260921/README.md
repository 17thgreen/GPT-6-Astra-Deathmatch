# NFL allocation mechanism study Q6

Read NFL_Allocation_Factorial_Results.md, then EXPERIMENT_SPEC.md. This offline
study runs eight F/P/R combinations plus the original router under four queue /
latency assumptions: 36 alternative counterfactual replays of the same 31 games.
It is not a concurrent multi-bot simulator and not forward validation.

F = additional two-sided positive-flow admission gate.
P = prospective cash earmark for net-inventory offsets.
R = cross-game cash-hour ranking plus incumbent multiplier.

000 still uses the common allocator; it is not the original router. Normal
within-game flow routing, offset quotes, cash constraints, event caps and delayed
cancellations remain active regardless of factor flags. Missing trade flow is
never synthesized. See the frozen specification for exact off-state semantics.

Requires Python 3.12 standard library on Linux and enough RAM for approximately
one million normalized rows plus three forked workers. From this directory:

```bash
python3 -m unittest -v test_replay_v2 test_queue_policies test_completion test_timing test_adaptive test_factorial test_analysis
python3 run_experiment.py
python3 verify_results.py
python3 analyze.py
python3 build_report.py
```

A rerun replaces its result files; preserve this delivered ZIP if you need the
original record. Run failures produce retained JSON/tracebacks and cannot become
completed P&L or silently bypass the analysis gates. SHADOW_CANDIDATE_FREEZE.json
is selected by the predeclared simplicity/retention rule, not a live promotion.
A later rerun changes its timestamp; keep the delivered original for provenance.

inputs/ contains standalone normalized quotes, trades, market mapping and week
membership. Its manifest also references the original raw Q2 files retained in
the prior Q2 package. FROZEN_EXPERIMENT.json pins rules, runner, policy, analyses,
tests and inputs before outcomes. BASELINE_HASHES.json pins inherited code.
Q5_REFERENCES.json contains ten prior summaries plus uncompressed fill/order
hashes for exact regression. DELIVERY_MANIFEST.json covers the packaged files.

results/ contains all scenarios, compressed fill/order/decision ledgers,
verification, factorial effects, screening and selection. Effects are model
comparisons on a repeatedly used cohort, not independently estimated live effects.
FORWARD_PROTOCOL.md and RESERVED_HOLDOUT.json carry the prior admission plan;
no always-on capture, live execution or completed future games are included.

The captured progress text stops before all final case lines. It is retained as
observed; results/run_completion.json and verification.json document the successful
process exit and all 36 complete, independently verified case ledgers.
