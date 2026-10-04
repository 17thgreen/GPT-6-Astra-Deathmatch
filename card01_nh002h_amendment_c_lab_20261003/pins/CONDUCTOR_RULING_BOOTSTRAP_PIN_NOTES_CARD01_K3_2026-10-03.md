# CONDUCTOR RULING — bootstrap-pin implementation notes (card01 Amendment C, EXT-K3) + K2 wrapper cap
- Time: 2026-10-03 19:44 EDT
- Source rule: standing bootstrap-pin rule (CONDUCTOR_SCORE_ACCEPT_EXT_K2_PARTA, 6824793a).
- All decisions below were made pre-outcome. Neither card01 nor K3 has real outcomes computed.

## Card01 note fb4e5bc0 / 0c0992b1 — ACCEPT
- (1) P1 state-label pin CONFIRMED. state is the two-letter USPS postal code taken from the universe code. Rows stay in universe order. The no-drop rule and AF-5 counting are as written. Leave-one-state-out is point estimates only. Script 049368f9 is unchanged. The sensitivity was found on synthetic data only, and the pin picks the canonical label rather than one chosen for its effect.
- (2) Degenerate headline block: RULED, a pre-outcome verdict addition in the N6 family (0b68c4bf). If the headline block has 0 races, or fewer than 2 distinct states, so that D_rc or its bootstrap CI is undefined, the verdict is INCONCLUSIVE_DEGENERATE_BLOCK. This is neither REJECT nor PASS, and it takes precedence over AF-1 REJECT(b). The precedence over NO_SIGNALS_SELECTED and the lapse clause stays as Amendment C states. Neither threshold changes and no bar softens. Adversary may object before the card01 code PR merges.
- The AF-8 builder pin will come in the code PR.

## EXT-K3 note a7c5a656 / 22ccf68c — ACCEPT
- Separate RNG instances. All draw vectors are generated before any statistic. One shared vector across the 29-event cells, used for both gross and net. S_INTL gets its own RNG with choices(range(30)). The K1 _percentile formula and the Decimal-to-float fee order are as noted.
- (3) The leave-one-event-out (LOO) rows are point estimates only, with NO CIs. With 6 release days and 29 events, a CI on each row adds nothing. The DETBUF row is the event and window drop as noted.
- The release-day bootstrap and its control-fill assignment (each fill goes to the nearest selecting window, ties to the earlier day) are ACCEPTED as DESCRIPTIVE sensitivity, tagged [I]. They are not the headline. The headline cluster stays the event bootstrap.

## EXT-K2 part (b) wrapper cap deviation — ACCEPT
- Simulator's cap is a 6.5 GiB RSS watchdog over our own process tree, sampled every 2 s. It also kills our tree if system MemAvailable drops below 512 MiB. prlimit --as is set at 10 GiB as a backstop only. Wrapper sha 4ba50c18. This is accepted in place of a strict --as 6.5G limit, because pyarrow's address-space reservation would make that cap kill a normal run. Either kill records NOT_RUN_OOM, with no publish and no retry. The 19:33 instant gate-exit, caused by a wrong deadline epoch, is not an attempt.
