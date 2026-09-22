# Q7 chosen-pair cost check: frozen 2×2

September 22, 2026. This specification is the hypothesis. It is committed before
Q7 source is frozen and before any Q7 scenario is executed. No P&L in this
document is a Q7 result. Q6 development outcomes are already known and are the
reason for the question; they are not re-labeled as Q7 evidence.

Do not modify `nfl_factorial_lab_20260921` or any earlier frozen lab. This
directory imports those modules read-only. A hash mismatch against the pins in
`FROZEN_EXPERIMENT.json` is a failed control, not permission to edit the older
tree.

## Question

Does checking the combined acquisition cost of the two routes actually chosen
explain the Q6 improvement, or do the allocator's scheduling and sizing rules
matter? The Q6 synthetic probe shows that the original router can choose two
routes that each look acceptable against a cheaper alternative counterparty
while the pair that is actually chosen costs more than its payout. That probe
is not a historical profit attribution.

## Arms

The architecture factor and the chosen-pair check are crossed. Nothing else
moves.

| Arm | Architecture | Chosen-pair check |
|---|---|---|
| A | Original router: `AdaptiveReplay(..., 'baseline')` | Off. Untouched reference. |
| B | Original router | On. Change only admission of new paired exposure. |
| C | Q6 simplified allocator, factor label `000` | Off. Remove only the combined-cost filter. |
| D | Q6 simplified allocator, factor label `000` | On. Untouched Q6 reference. |

Label `000` is the selected row in
`nfl_factorial_lab_20260921/SHADOW_CANDIDATE_FREEZE.json`: flow off, protection
off, ranking off. Ranking off is the neutral score already selected by Q6
(adjusted score 1, event-id tie break). Do not enable F, P, or R. Do not
re-rank, re-threshold, or resize as part of this study.

Arm C is not a new router. It is the Q6 `000` allocator with exactly one
predicate removed: the return that drops a pair when

```
margin = 1 - (cost of chosen leg 1 + cost of chosen leg 2)
         - 0.0002 - 2 * balance_precision / order_size
```

is less than or equal to zero. `cost` is the inherited maker acquisition cost
on that candidate (`price + maker_coefficient * price * (1 - price)`), taken
from the two routes `choose()` actually returned. The quantity in the cushion
is the configured order size (250), the same quantity Q6 uses. Do not retune
the cushion, the fee coefficients, or the order size.

That predicate is the combined-cost filter. The per-direction screen inside
`choose()` — each route's margin against the cheapest counterleg — is route
selection shared by the original router and by Q6. It is not the combined-cost
filter, and it stays in every arm. Turning it off would change which routes
are chosen. Arm C must not recreate the combined-cost filter through another
score, budget, or eligibility rule. A negative combined margin must still
receive an entry budget under neutral ranking. A non-positive score must not
become a second veto while ranking is off.

## What the check may and may not do

The check is an admission rule for new paired exposure. It is not a new
execution model.

- Offset-only orders stay unblocked. A chosen route whose direction reduces
  current net inventory (`direction * holdings < 0`) is inventory reduction.
  A failing combined-cost check must not suppress it. Flat inventory has no
  offset leg. A partially filled pair has one reducing direction: that leg
  may be quoted alone, and the inventory-increasing leg is new paired exposure.
- Do not assume simultaneous fills. The check does not require both legs to
  have projected capacity in the same horizon, does not size either leg down
  to the other leg's capacity, and does not wait for one fill before admitting
  the other. Passing pairs keep the architecture's own sizes. Fills, if any,
  still arrive later from the tape, independently.
- Do not inspect future quotes. Costs come from candidates built at the
  decision time from books already known. A quote with a later timestamp is
  not an input to this decision.
- Do not cancel instantly. The check does not pop an order or zero its
  remaining size at decision time. On the original router, an order that is
  already working is left to the inherited quote path: a price change still
  waits out `cancel_delay_seconds`, and a same-price working order is not
  pulled merely because the pair would fail. A blocked key with no working
  order is simply not submitted. The allocator check continues to act only by
  withholding an entry budget on the inherited ten-minute cadence. It does
  not add a faster cancel loop. Offset quotes keep the allocator's existing
  offset-size rule.
- Record every rejected pair and why. The reason for this filter is
  `combined_acquisition_cost`. Store the two chosen legs, their costs, the
  margin, which offset keys remained admissible, and which new-exposure keys
  were blocked. `counted_as_pnl` is false. Hypothetical margin is not cash,
  not a fill, and not a completed-profit adjustment.

Arm A does not consult the check. Its refresh path stays the baseline router.
Arm D calls the frozen Q6 `000` rank function unchanged. Rejection rows for
Arm D are a side ledger. They are not appended to the inherited `decisions`
stream, so fill, order, and decision ledgers can be compared with Q6.

## Fixed design

All sixteen scenarios share one account and one development cohort:

- Starting cash $5,000. One pooled account. Arms are separate counterfactual
  replays, not concurrent bots, and do not share fills.
- The Q6 31-game development cohort (16 Week 1, 15 Week 2). Not a holdout.
  Do not read `RESERVED_HOLDOUT.json` outcomes. Do not admit or drop games
  after looking at results.
- Desired order size 250, hard event exposure 250, assumed total exit depth
  250 per game.
- Inherited fee model, balance precision, candle quotes, five-minute
  liquidation lead, participation 0.5, and the Q6 last-12-hour queue.
- Early queues 3,300 and 10,000. Submit and cancel delays 0.25 seconds and
  5 seconds. Both delays move together, as in Q6.

Scenario names are `q{queue}_d{delay}_{arm}` with delay formatted so the four
stresses are `d0.25` and `d5`:

1. `q3300_d0.25_A` through `q3300_d0.25_D`
2. `q3300_d5_A` through `q3300_d5_D`
3. `q10000_d0.25_A` through `q10000_d0.25_D`
4. `q10000_d5_A` through `q10000_d5_D`

No paid data, live orders, credentialed trading, external predictors, or
multi-wallet simulation. No parameter search after any output exists.

Historical inputs are the Q6 normalized kit files under
`nfl_factorial_lab_20260921/inputs/`, checked against that directory's
`inputs/manifest.json`. Those bytes are not copied here. If `events.jsonl.gz`
or a manifest hash is missing, the runner writes a not-run status and stops.
It does not invent fills, cash, or P&L. Restoring the owner kit with
`scripts/restore_kit.py` into the Q6 input path is what makes a run possible.

## Metrics, effects, and selection

Report these only from an actual replay. Unresolved inventory makes
`completed_strategy_pnl` null. Null is not zero and is not a profit. Losses
stay negative. Rejection margins stay out of the cash ledger.

Per scenario, from the inherited accounting result plus the side ledger:

- Completed net after fees, terminal payout bounds, unresolved contracts,
  flatness, and the two week cashflow contributions.
- Unhedged contract-hours, taker-exit contracts, maker contracts, minimum
  cash, peak reserved cash, and peak absolute event exposure.
- P&L excluding the two largest game cashflows, using the Q6 definition,
  and only when the scenario is fully flat.
- Pair-rejection count. The count is not a P&L.

Within each of the four queue/delay stresses, when all four arm P&Ls are
non-null:

- Original-router guard effect: B minus A.
- Allocator guard effect: D minus C.
- Interaction: (D minus C) minus (B minus A).
- Architecture effect with the check off: C minus A.
- Architecture effect with the check on: D minus B.

These are deterministic within-simulator contrasts on a repeatedly used
development cohort. They are not live causal effects. No p-value is attached.

Candidate rule, fixed before outcomes. Apply it only if every one of the
sixteen scenarios has flat inventory and a non-null completed P&L. Otherwise
the status is `NO_NEW_SELECTION` and the Q6 `000` shadow candidate stands.

Arm B becomes a development shadow candidate only when all of the following
hold:

- B's completed P&L is strictly above A's in every stress.
- D's completed P&L is strictly positive in every stress, and B's completed
  P&L is at least 95 percent of D's in every stress. The 95 percent figure is
  the same engineering simplification tolerance Q6 already declared, not a
  new fit.
- At queue 3,300 and delay 0.25 seconds, both week contributions of B are
  strictly above A's.
- B's unhedged contract-hours are at most 1.25 times A's in every stress.

Arm C is an ablation, not a candidate. There is no live promotion either way.
If B fails the rule, the allocator bundle including its check remains the
combined mechanism. A passing B is still only a candidate for a later
prospective shadow on fresh data. This study does not collect that data.

## Positive controls

When a real run exists, compare it before interpreting guard effects.

- Arm A must reproduce the original-router references: Q6 result summaries
  named `q{queue}_d{delay}_baseline`, and the baseline rows in
  `nfl_factorial_lab_20260921/Q5_REFERENCES.json`, including uncompressed
  fill and order ledger hashes where those ledger bytes are present.
- Arm D must reproduce Q6 label `000` summaries
  `q{queue}_d{delay}_000` on completed net, flatness, unresolved size, week
  contributions, and fill/order/decision ledger hashes. The side rejection
  ledger is excluded from that comparison.
- A control mismatch is a failed reproduction. It is not a Q7 finding.

Until those inputs and ledgers are restored, the controls are unrun. Unit
tests may still check that Arm D's rank function matches frozen Q6 `000` on
synthetic books, and that Arm A's unchecked refresh matches a direct baseline
router on synthetic books.

## Forward boundary

No always-on collector is running. The prior 32-game reservation is
schedule-only. This experiment does not admit games, deploy a recorder, or
place orders. Fresh-game validation remains a separate gate.
