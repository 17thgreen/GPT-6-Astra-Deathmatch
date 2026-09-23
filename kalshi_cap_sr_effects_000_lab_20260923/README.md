# Cap-SR-FX effects path

Status: hypothesis committed, then source frozen. The unit page is
`results/UNIT_RESULTS.md` (11 tests, OK, 2026-09-23T14:49:04Z). That page is
not profit and not an Examiner pass.
`EXPERIMENT_SPEC.md` is the hypothesis. `FROZEN_EXPERIMENT.json` keeps
`results` and `pnl` null. `results/EMPTY_RESULTS.json` keeps
`borrow_count_delta_vs_fifo`, `blend_utilization_gap`,
`soft_breach_or_blend_rate`, and `effects_path_fixture_id` null.

Feature family Cap-SR-FX. The only knob is fixture stress: FX0
`q3300_d0.25`, FX1 `synthetic_borrow_stress`. SR0, SR1, and SR2 are imported
from `kalshi_soft_blended_reserves_000_lab_20260923` (`45863037`). This
directory does not re-implement that math and does not edit that tree.

`lab/governance/astra/packets/` is not in this checkout. Freeze copies:

- `CAP_SR_EFFECTS_PATH_000_FREEZE_2026-09-23.md` (sha256 `cd08a93af2659c36f83cd1b9ffc3174364cc767efc374a4e0669e128f6a29074`)
- `CAP_SR_EFFECTS_PATH_000/`
- `packets/CAP_SR_EFFECTS_PATH_000_FREEZE_2026-09-23.md`
- `packets/CAP_SR_EFFECTS_PATH_000/`

The promotion scoreboard is one shared 5000 USD account. Fees come from
`kalshi_feebook_lab_20260922`. Queue labels come from
`kalshi_rails_lab_20260922`. Those labs are not edited.

From this directory, Python 3.12 standard library:

```bash
python3 -m unittest -v tests.test_effects_path
```

No live orders. This page does not retune Q6-`000`, reopen queue-fragility,
or reopen Cap-SR soft_policy arms. S1 empty-events stays deferred.
