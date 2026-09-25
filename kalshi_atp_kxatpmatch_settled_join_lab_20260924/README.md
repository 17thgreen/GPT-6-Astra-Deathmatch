# ATP KXATPMATCH settled-resolution join harness

Status: hypothesis committed, then source. The unit page is
`results/UNIT_RESULTS.md`. That page is not profit and not an Examiner
pass. Measurement only. Feature family ATP-RJ. The only knob is
`join_gate`: J0 `nonempty_result_required` and J1
`occurrence_datetime_match`. When `occurrence_datetime` is null, J1 labels
the row `join_source=expected_expiration_time_fallback` and does not write
`expected_expiration_time` into `occurrence_datetime`.

Nearest dead card: ATP-FQ PR34 at
`438f4abf28a3c0156daf6c96ece5efda9557f1dc`. PR35 was a closed duplicate.
This harness joins already-settled KXATPMATCH markets only. It has no fee,
queue, book, fill, or tape metric.

Conductor ACCEPT sha256
`e42d75834086f34090581aee88563ab9849d60864c2d9e59c4ef495b3e8e5af5`.
Freeze sha256
`dc9fcb326a97ce24267ed96438bf403687bc9aef6b79dccef3483d0e4cdeeb69`.
Panel parent sha256
`ed041c502d1f775d33c44bf900ac91b1339d99045bddd2052edd09a139ae2d3f`,
`admitted_at` null. This lab does not run `admit.py`. Scout N=30 is a pin
and is not `settled_join_n`. `results` and `pnl` stay null.

Examiner status stays `HOLD_PRE_PR`. `stub_ready` is false.

Measurement mode, after Clock admit, pages public GET reads and writes
counts only to the given output path. This checkout does not commit those
counts. `admitted_at` stays null and admit_ready stays `pending Clock`.

```bash
python3 orchestrator.py measure --since 2026-09-24T23:52:00Z --out <path>
```

From this directory, Python 3 standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

No Logan keys. No live orders. A passing unit run is not an Examiner score.
