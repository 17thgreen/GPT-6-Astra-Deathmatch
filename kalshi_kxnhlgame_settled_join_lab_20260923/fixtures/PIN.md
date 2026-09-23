# Fixtures

This harness has no synthetic market, depth, fill, or settlement fixture.
The subject is the attached scout reget, seed summary, panel stub, and
settled reget capture. Those files are byte copies. This note does not
contain their bytes.

`GET /markets?series_ticker=KXNHLGAME&status=settled|finalized|open` and
`GET /events?series_ticker=KXNHLGAME&status=settled` are the honest 429
gaps. The scout records `settled_list_http` `429_honest`,
`settled_list_cursor_present` false, `open_list_http` `429_honest`, and
`open_list_n` null. No market object is backfilled there.

The overnight SEP22 cohort is 17 finalized markets with a non-empty
official `result` on the authentic reget. That count is a pin. It is
not `settled_join_n`. Three of those events have one market row. The
other side is not added.

Parent SEP26 seeds `KXNHLGAME-26SEP26TBFLA-TB`,
`KXNHLGAME-26SEP26TBFLA-FLA`, and `KXNHLGAME-26SEP26COLUTA-UTA` stay
active with an empty result. The reget also records
`KXNHLGAME-26SEP26WSHPHI-WSH` as active with `result` `""`. The panel
stub keeps `result` `""` on all 12 markets. Eight panel markets are
absent from this reget and stay absent.
