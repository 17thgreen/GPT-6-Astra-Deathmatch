# C4 KXCPI settled-resolution join harness

Status: hypothesis committed, then source, then the unit page.
`python3 -m unittest -v tests.test_orchestrator` ran 10 tests in 0.026s.
Recorded at 2026-09-24T23:38:32Z. Result: OK. Failures: 0. Errors: 0.
That page is not profit and not an Examiner pass. Measurement only.
Feature family C4-RJ. The only knob is
`join_gate`: J0 `nonempty_result_required` and J1
`occurrence_datetime_match`. When `occurrence_datetime` is null, J1 labels
the row `join_source=expected_expiration_time_fallback` and does not write
`expected_expiration_time` into `occurrence_datetime`.

Nearest dead card: CPI-FQ PR33 at
`6e55a99790f4cc09a437d2e16ccf4e8e826a154b`. This harness joins already-settled
KXCPI markets only. It has no fee, queue, book, fill, or tape metric.

Conductor ACCEPT sha256
`8a86ae6b9dfb0e80d80de8404750501e44aeb873e7f31789ece5fddf8dd03fc5`.
Freeze sha256
`5e37f81a8959e83c3d2c0c42739e1ca6c127c748442ac6fe28c0013edee12e2f`.
Panel parent sha256
`b20b0cbee50c127d2e9bb2548b574b7d643cc708f54019d53bd91775f9762c13`,
`admitted_at` null. This lab does not run `admit.py`. Scout N=25 is a pin
and is not `settled_join_n`. `results` and `pnl` stay null.

Examiner status stays `HOLD_PRE_PR`. `stub_ready` is false.

From this directory, Python 3 standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

No Logan keys. No live orders. A passing unit run is not an Examiner score.
