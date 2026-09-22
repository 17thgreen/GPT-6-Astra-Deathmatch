# R2-P1 fixture join on Q6-000

Status: pick **A**, lab `kalshi_r2p1_fixture_join_000_lab_20260922`. The
canonical freeze is
`packets/R2-P1_FIXTURE_JOIN_000_FREEZE_2026-09-22.md`, sha256
`e9bac91ca908b2ba704d966f0cf48cb181070ac11de1d117b93512bd2719ae1c`.
`EXPERIMENT_SPEC.md` is the hypothesis. `FROZEN_EXPERIMENT.json` keeps
`fee_delta_vs_inherited_model`, `freshness_gap_sec`,
`queue_bin_mismatch_rate`, `results`, and `pnl` null.

The harness reads Q6-`000` fill and order ledgers and calls the frozen
R2-P1 hygiene helpers. Examiner fees come from `kalshi_feebook_lab_20260922`
at `22371178cb2663250b4762f328069571c48cb551`. Queue bins, maker-credit
admission, and content freshness come from `kalshi_rails_lab_20260922` at
`6a28e0d6254327ea4e6451c781bec56215ac6cac`. The hygiene module is imported
from `kalshi_r2p1_hygiene_000_lab_20260922` and is not edited.

Primary production pin:
`nfl_factorial_lab_20260921/results/q3300_d0.25_000_fills.jsonl.gz` and the
matching orders file. Those gzip ledgers are gitignored. See
`fixtures/PIN.md`. The synthetic jsonl pair in `fixtures/` exercises the same
schema when the production bytes are absent.

From this directory, Python 3.12 standard library:

```bash
python3 -m unittest -v tests.test_fixture_join
```

No live orders. No Q6-`000` retune. No capital A2/A3. Pick B stays deferred.
Helper arithmetic on synthetic rows is not written into the freeze packet.
