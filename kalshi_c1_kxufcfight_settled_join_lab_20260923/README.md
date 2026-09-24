# C1 KXUFCFIGHT settled-resolution join harness

Status: hypothesis committed, then source, then the unit page.
`python3 -m unittest -v tests.test_orchestrator` ran 10 tests in 0.024s.
Recorded at 2026-09-24T23:03:36Z. Result: OK. Failures: 0. Errors: 0.
That page is not profit and not an Examiner pass. Measurement only.
Feature family C1-RJ. The only knob is `join_gate`: J0
`nonempty_result_required` and J1 `occurrence_datetime_match`. J1 uses
`occurrence_datetime` on the four admitted parent seeds. It does not
invent `occurrence_datetime`.

The cited freeze sha256
`3ea3362ad3c16951369d5f90497ec6079213dd54e5556340c4d3738744126cf1`,
the Conductor ACCEPT, `MAXIMIZE_PIN_2026-09-23_1750ET.md`, and
`lab/governance/astra/packets/scout_c1_settled_rejoin_2026-09-23/`
were absent from this checkout. They were not regenerated.
`digest_all_match_claimed` is false. See `PIN_GAP.json`.

The panel parent is the existing admitted panel, sha256
`24426d804c51bde23cf2557a11a8481a12026da10024094c4ae546d1f7d3956e`,
`admitted_at` `2026-09-23T00:49:43Z`. The capture file was not rewritten.
This lab does not run `admit.py`. The declared scout N=4 is not
`settled_join_n`. `results` and `pnl` stay null.

Examiner status stays `HOLD_PRE_PR`. `stub_ready` is false. A later
READY state is NOT_SCORED only, and only after the authentic pins are
in the tree. This page is not that score.

From this directory, Python 3 standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

No Logan keys. No live orders. A passing unit run is not an Examiner score.
