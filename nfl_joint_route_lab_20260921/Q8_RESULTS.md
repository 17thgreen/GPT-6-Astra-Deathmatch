# Q8 results: extra pair access did not produce a robust improvement

Status: matrix completed on the same 31 reused NFL development games. Both
variants fail the preregistered selection screen. Retain Q7 GuardedRouter.
Each alternative uses the same shared $5000 account and unchanged 250 limits.

| Early queue | Submit/cancel delay | Q7 control | Recovery only | Joint routing |
|---:|---:|---:|---:|---:|
| 3,300 | 0.25s | $354.33 | $360.03 | $371.45 |
| 3,300 | 5s | $353.89 | $360.41 | $370.68 |
| 10,000 | 0.25s | $90.45 | $73.27 | $70.85 |
| 10,000 | 5s | $79.08 | $66.35 | $61.66 |

All 12 scenarios finish flat. The lighter-queue headline gain does not survive
queue stress. Neither variant improves both primary weeks: recovery reduces
Week 2 by $1.7977; joint routing reduces it by $0.0084. The tiny latter difference
is not economically decisive alone, but the queue-10000 losses are substantial.

## Primary mechanism diagnostics

| Measure, queue 3300 / .25s | Q7 | Recovery only | Joint |
|---|---:|---:|---:|
| Maker contracts | 326,041.18 | 321,428.52 | 320,198.95 |
| Taker exit contracts | 2,063.70 | 2,770.18 | 2,827.89 |
| Inventory contract-hours | 627,759.78 | 688,218.55 | 658,134.53 |
| Submitted orders | 43,660.00 | 42,499.00 | 43,329.00 |
| Profit excluding best two games | 184.28 | 189.98 | 201.40 |

Both alternatives trade fewer maker contracts yet need more taker exits. A
positive static pair margin and an improved service heuristic do not ensure
balanced fills or cheap completion. The experiment rejects these two particular
routing policies; it does not establish that every joint-routing method fails.
Inventory hours increase 4.5%–9.6%, within the screen's 1.25x limit in every
scenario. Read the exact screen in selection.json rather than replacing it
with a favorable aggregate. Routing decision counts are in
`results/routing_diagnostics.json`; repeated decisions are not unique trade
opportunities or independent samples. No annualized or non-NFL P&L claim follows.

## Verification and provenance

- Specification committed before implementation: `4e48fa6`.
- Source, tests and freeze committed before matrix: `410dc16`.
- 128 tests pass (13 new Q8 tests plus the 115-test inherited suite).
- All 12 independent ledger audits reconcile fees, cash, positions, orders,
  deadlines, exit depth and weekly contributions. Four unchanged Q7 controls
  reproduce exact uncompressed fill/order histories and financial aggregates.
- Input/source hashes are verified before/after. No matrix run failures; no
  parameter changes or reruns after outcomes.
- An initial pre-freeze unit test found a `self.mode` collision with the inherited
  completion layer. It was renamed `route_mode`; exact passing-decision behavior
  then passed before source freeze. This was a caught implementation defect, not
  a removed losing backtest.
- `results/verification.json`, `selection.json`, `run_completion.json` and the
  external archive indexes are the machine-readable evidence. Test/audit logs
  and all financial scenario summaries are committed. Large ledgers remain in
  the indexed data deliverable, with the unchanged Q7 archive supplying inputs.

## Engineering consequence

Do not promote either Q8 arm or pick a queue setting after seeing its result.
Keep Q7's admission and priority-preserving behavior. Next research should price
unbalanced fills and completion costs explicitly, rather than treating the
minimum of two trailing-flow service scores as sufficient. That is a new
hypothesis requiring a new specification, not a threshold adjustment to Q8.

In parallel, market breadth remains a separate growth route. The new
`market_portability` module supplies exact payoff compatibility checks, a
configuration schema without NFL defaults, a GET-only discovery tool and a
sourced adaptation roadmap. It is not yet a non-NFL replay or an order adapter.

The user owns forward validation. Queue, profit and portability research remain
the active lane; no live orders or risk-limit increases were introduced.
