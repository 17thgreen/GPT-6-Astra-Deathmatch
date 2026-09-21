# Fresh-data admission and validation

The included RESERVED_HOLDOUT.json is the prior schedule-only reservation of 32
games, not a claim that venue identity or complete data coverage was secured.
Retain Q4's development exclusions. Never backdate an admission or replace games
after inspecting their outcomes. The first reserved T−7d window begins
2026-09-22T00:15:00Z. If complete capture cannot be secured before the applicable
start, label that game incomplete; do not count it as a full-window holdout.
A replacement complete cohort requires a new schedule-only freeze before its
windows/outcomes, and a separate identity/version.

1. Freeze this experiment's code and exact policies before admission. Resolve
   venue team tickers, kickoff, complementary settlement and netting mapping
   from metadata. Unknown identities remain unavailable. All three policies,
   including historical losers, can be recorded as predeclared shadow arms;
   no selecting the best after looking at future outcomes.
2. Use the existing Q4 GET-only durable recorder on a host that stays running.
   Keep first receipt times, full book snapshots, deduplicated paginated trades,
   metadata, failures, restarts and coverage gaps. Book capture must cover
   T−7d through T−3h; no fabricated missing snapshots. Q4's Docker configuration
   remains prepared, not deployed or Docker-verified in this task.
3. After each game, audit coverage before examining strategy profit. Publish
   coverage and gap duration by game; incomplete games remain a separate cohort.
   Public REST snapshots cannot determine cancellation allocation or actual
   queue position. Keep conservative queue bounds; do not equate a print at a
   price to an executable fill. No account credentials or real orders required
   for public shadow collection.
4. Replay the identical received stream into four isolated 5k accounts: baseline
   plus each candidate, preserving timing and all three predeclared controls.
   Capture 300-second markouts only when their source quote has actually arrived.
   Use measured data receipt delay; trading latency remains a separate stress
   until order acknowledgments can be measured in an authorized execution test.
5. Keep the same common fee assumptions visibly labeled until actual event fees,
   netting mechanics and fee rounding are verified. Use observed exit books
   with constrained depth, preserving unresolved inventory when depth/coverage
   is insufficient. Report optimistic/conservative bounds rather than invented
   precision where queue service cannot be identified.
6. Evaluate only after all scheduled games have reached T−3h and coverage
   adjudication is locked. Report paired per-game deltas and week-cluster
   uncertainty for all three candidates. Three comparisons require multiplicity
   control; few independent weeks imply weak statistical evidence regardless of
   trade count. No live promotion from the present development screen.

Current status at packaging: zero completed fresh games; no always-on recorder
running; venue identities unresolved for most scheduled games. Fresh outcomes
cannot be produced immediately or promised as an ongoing background task.
