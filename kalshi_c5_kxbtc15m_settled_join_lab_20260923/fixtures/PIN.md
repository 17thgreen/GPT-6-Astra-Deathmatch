# Fixtures

This harness has no synthetic market, depth, fill, or settlement fixture.
The subject is the attached scout reget, seed summary, panel stub, and
settled reget capture. Those files are byte copies. This note does not
contain their bytes.

`status=finalized` and `status=closed` list filters are the honest 429
gaps in the reget (`status_finalized_list` and `status_closed_list`,
each `429 too_many_requests`). No market object is backfilled there.

Parent seed `KXBTC15M-26SEP222045-45` is finalized `result` `no` on the
reget. The panel stub `result` stays null. Open ticker
`KXBTC15M-26SEP231530-30` is cited and has no settled-reget market
object.
