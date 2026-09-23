# Fixtures

This harness has no synthetic market, depth, fill, or settlement fixture.
The subject is the attached scout reget, seed summary, panel stub, and
settled reget capture. Those files are byte copies. This note does not
contain their bytes.

`markets?series_ticker=KXNCAAFGAME&status=settled|finalized|open` and
`events?series_ticker=KXNCAAFGAME&status=settled` are honest 429 gaps.
No market object is backfilled there. Named event and market GETs that
returned `not_found` or `too_many_requests` stay gaps.

Eighteen prior-weekend SEP05/SEP12/SEP19 markets are finalized with a
non-empty official `result` on event embeds and single-market GETs
(`yes` 9, `no` 9). That count is the scout pin. It is not
`settled_join_n`. Parent SEP26 FQ seeds stay active with a null
`result`. The panel stub has no settled `result` and `admitted_at`
stays null.
