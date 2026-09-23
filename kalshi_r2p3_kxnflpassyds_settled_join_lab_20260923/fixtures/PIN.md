# Fixtures

This harness has no synthetic market, depth, fill, or settlement fixture.
The subject is the attached scout reget, seed summary, panel stub, and
settled reget capture. Those files are byte copies. This note does not
contain their bytes.

`markets?series_ticker=KXNFLPASSYDS&status=finalized` and
`events?series_ticker=KXNFLPASSYDS&status=closed|settled` are honest 429
gaps. The close-window `min_close_ts`/`max_close_ts` query is an honest
400 gap. No market object is backfilled there. The settled list that
returned HTTP 200 is limited to the attached 20 rows. A present cursor
is not followed.

Twenty prior-weekend SEP20/SEP21 markets are finalized with a non-empty
official `result` on that settled list (`yes` 6, `no` 14). That count is
the scout pin. It is not `settled_join_n`. Parent SEP27 prop-ladder seeds
stay active with a null `result`. The panel stub has empty
`market_tickers`, no settled `result`, and `admitted_at` stays null.
ATL@GB stays excluded.
