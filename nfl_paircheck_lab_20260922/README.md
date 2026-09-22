# Q7 chosen-pair cost check

Status: **implemented and frozen, not run**. This directory does not contain Q7
profit. `EXPERIMENT_SPEC.md` is the hypothesis. `FROZEN_EXPERIMENT.json` pins
arms A–D, the 16 scenarios, and the Q6 sources this lab imports but does not
modify.

## Question

Does the combined acquisition cost of the two routes actually chosen explain
the Q6 difference, or do the allocator's scheduling and sizing rules matter?

| Arm | What it is |
|---|---|
| A | Original router, pair check off |
| B | Original router, pair check on for new paired exposure only |
| C | Q6 allocator label `000`, combined-cost filter removed and not reintroduced |
| D | Q6 allocator label `000`, pair check on |

Fixed for every arm: one $5,000 account, the same 31 development games, order
size 250, event cap 250, assumed exit depth 250. Stresses are early queues
3,300 and 10,000 crossed with submit/cancel delays 0.25s and 5s (16 scenarios).

The check does not block inventory reduction, require both legs to be fillable
together, read a later quote, or remove a resting order immediately. Rejected
pairs are recorded with `counted_as_pnl: false`.

## Tests that run without the historical kit

From this directory, Python 3.12 standard library:

```bash
python3 -m unittest -v test_paircheck test_runner
```

Those tests cover admission and rejection, the absence of a residual cost gate
on arm C, offset-only admission, and the rejection ledger. They do not replay
the 31 games.

## How to execute the 16 scenarios

The normalized event tape is not in git. `events.jsonl.gz` is indexed in
`provenance/EXTERNAL_ARTIFACTS.json` and delivered inside
`nfl_factorial_lab_20260921/NFL_Allocation_Factorial_Kit.zip`. From the
repository root, with that zip available locally:

```bash
python3 scripts/restore_kit.py /path/to/NFL_Allocation_Factorial_Kit.zip
```

The restore checks the archive and file hashes and writes under the frozen Q6
input path. Do not commit the zip or the restored gzip bytes.

Then, from this directory:

```bash
python3 run_experiment.py
python3 verify_results.py
python3 analyze.py
```

`run_experiment.py` runs `q3300_d0.25_{A,B,C,D}`, `q3300_d5_{A,B,C,D}`,
`q10000_d0.25_{A,B,C,D}`, and `q10000_d5_{A,B,C,D}`. It refuses to start if
the Q6 pins or the input manifest do not match.

If the tape is still missing, `run_experiment.py` writes `results/NOT_RUN.json`
and exits 3. It does not create scenario ledgers or P&L. `analyze.py` and
`verify_results.py` likewise record a not-run status and do not treat the gap
as a zero effect or a passing control.

After a real run, verification compares arm A with the Q6 baseline summaries
and `Q5_REFERENCES.json` ledger hashes, and arm D with the Q6 `000` summaries
and ledgers when those bytes are present. A mismatch is a failed reproduction.
Analysis then reports the guard effect inside each architecture and their
interaction. The predeclared rule can name arm B as a shadow-research candidate
only. It does not place orders or replace the Q6 candidate on its own.

No live orders, credentials, or holdout outcomes are used.
