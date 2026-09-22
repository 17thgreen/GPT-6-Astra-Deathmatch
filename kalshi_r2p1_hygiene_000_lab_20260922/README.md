# R2-P1 hygiene stress on Q6-000

Status: one lab, `kalshi_r2p1_hygiene_000_lab_20260922`. The canonical freeze
is `R2-P1_FEEBOOK_RAILS_HYGIENE_000_FREEZE_2026-09-22.md` (sha256 prefix
`ddcd4427`). Those bytes were not in this checkout, so this directory does not
substitute a file under that name. `fee_sensitivity_000_r1p1` is superseded by
R2-P1 and has no second lab. `EXPERIMENT_SPEC.md` is the hypothesis.
`FROZEN_EXPERIMENT.json` keeps `results`, `pnl`, and the three pre-settlement
outputs null.

The lab imports `kalshi_feebook_lab_20260922` for examiner fees and
`kalshi_rails_lab_20260922` for queue labels, maker-credit admission, and the
content-fresh predicate. It does not read Q6 `common_config` fee coefficients.
Strategy pointer is Q6 label `000`. Capital arms and the queue-fragility twin
are not knobs.

Pick A fixture join, freeze sha256
`e9bac91ca908b2ba704d966f0cf48cb181070ac11de1d117b93512bd2719ae1c`, is
`fixture_join.py` in this same directory. It calls these helpers. It does
not write the five scorecard fields. The production Q6-`000` gzip ledgers
are gitignored; see `fixtures/PIN.md`. Pick B stays deferred.

From this directory, Python 3.12 standard library:

```bash
python3 -m unittest -v tests.test_hygiene tests.test_fixture_join
```

No live orders. This lab does not modify the feebook lab, the rails lab, the
capital-structure lab, or the Q1–Q7 trees. There is no second R2-P1 lab.
Pre-settlement outputs in `FROZEN_EXPERIMENT.json` stay null.
