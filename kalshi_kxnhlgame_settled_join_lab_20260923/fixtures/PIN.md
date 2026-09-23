# Fixtures

This harness has no synthetic market, depth, fill, or settlement fixture.
The subject is the attached scout reget, seed summary, panel stub, and
settled reget capture. Those files are byte copies. This note does not
contain their bytes.

`markets?series_ticker=KXNHLGAME&status=settled|finalized|open` and
`events?series_ticker=KXNHLGAME&status=settled` are honest 429 gaps.
No market object is backfilled there.

Seventeen overnight SEP22 markets are finalized with a non-empty official
`result` on single-market GETs (`yes` 8, `no` 9). That count is the scout
pin. It is not `settled_join_n`. Parent SEP26 FQ seeds stay active with
an empty `result`. The panel stub `result` stays empty and `admitted_at`
stays null.
