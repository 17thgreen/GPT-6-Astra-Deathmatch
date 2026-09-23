# Fixtures

This harness has no synthetic market, depth, fill, or settlement fixture.
The subject is the attached scout reget, seed summary, panel stub, and
settled reget capture. Those files are byte copies. This note does not
contain their bytes.

`markets?series_ticker=KXHIGHCHI&status=settled` and
`markets?series_ticker=KXHIGHNY&status=open` are the honest 429 gaps in
the reget (`markets_settled_KXHIGHCHI_lim20.json` and
`markets_open_KXHIGHNY_lim4.json`, each `too_many_requests`). No market
object is backfilled there.

Parent seeds `KXHIGHNY-26SEP22-B67.5` (`yes`), `KXHIGHNY-26SEP22-T70`
(`no`), and `KXHIGHCHI-26SEP22-B64.5` (`yes`) are finalized on the
reget. The panel stub `result` stays null. The CHI open tickers
`KXHIGHCHI-26SEP24-T73`, `KXHIGHCHI-26SEP24-T66`,
`KXHIGHCHI-26SEP24-B72.5`, and `KXHIGHCHI-26SEP24-B70.5` are cited with
empty `result` and are not settled-join markets.
