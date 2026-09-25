# ATP KXATPMATCH settled-resolution join unit results

The official unit log is recorded after `python3 -m unittest -v tests.test_orchestrator`.
This page is a code check. It is not a simulated trading run and not live
validation. `results` and `pnl` stay null. `settled_join_n`,
`occurrence_match_n`, `fallback_join_n`, and `admitted_at` stay null in the
committed scorecard. Scout N=30 is a pin and is not `settled_join_n`.
