# Cap-SR soft-blended reserves

Status: hypothesis committed in this directory. Unit outcomes, if recorded,
live under `results/` and are not profit. `EXPERIMENT_SPEC.md` is the
hypothesis. `FROZEN_EXPERIMENT.json` keeps `results` and `pnl` null.
`results/EMPTY_RESULTS.json` keeps `borrow_count_delta_vs_fifo`,
`blend_utilization_gap`, and `soft_breach_or_blend_rate` null.

Feature family Cap-SR. Not F1, not F2, not F3. Nearest dead cards: C1
empty-book and Q7 Arm B kill. The only knob is `soft_policy` on the A2
substrate. The promotion scoreboard is one shared 5000 USD account.

`lab/governance/astra/packets/` is not in this checkout. Freeze copies:

- `SOFT_BLENDED_RESERVES_000_FREEZE_2026-09-23.md` (sha256 `1f263dec7d7810515c3e32c13f3c5eca4344c4951db762a88ea01a8dfde7b1b3`)
- `SOFT_BLENDED_RESERVES_000/`
- `packets/SOFT_BLENDED_RESERVES_000_FREEZE_2026-09-23.md`
- `packets/SOFT_BLENDED_RESERVES_000/`

SR0 reuses the capital-structure A2 engine (`ce4671b8`) for FIFO unused
borrows. Fees come from `kalshi_feebook_lab_20260922` (`fee_source=feebook`).
Queue labels come from `kalshi_rails_lab_20260922` (`queue_source=rails`).
Those labs are not edited.

From this directory, Python 3.12 standard library:

```bash
python3 -m unittest -v tests.test_soft_policy
```

No live orders. This page does not retune Q6-`000`, reopen queue-fragility,
or re-arm A1 or A3.
