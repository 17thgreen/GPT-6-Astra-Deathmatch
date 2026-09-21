# Post-result diagnostic: neutral portfolio ordering

This diagnostic was added after seeing the primary q3300 allocation result
(+$342.76) and its baseline (+$201.52). It is not a predeclared primary candidate,
not a new winner eligible for promotion, and not a retuning of the frozen policy.

Risk to interpretation: allocation also requires positive observed flow on both
legs and protects inventory-offset cash. Its gain against the original router
might come from these requirements, rather than profit-per-cash-hour ranking.

Run two additional controls at .25-second latency, queues3300 and10000, same
5k account and all other allocation rules. Replace only the adjusted ranking
score with a constant1; tie-break by event ID. This removes both value ranking
and the explicit incumbent bonus, while preserving eligibility, cash protection,
rebalance cadence, quantity budgets, actual retained queue positions, and normal
cancel/resize delays. This is deterministic neutral ordering, not an average of
random orderings. Compare its profit with the primary allocation arm. A positive
neutral result alone is no proof of ranking value; a primary advantage here is
still exploratory and must be checked on fresh games.
