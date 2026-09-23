# C1 KXUFCFIGHT unit results

September 23, 2026. This file records a code check of the frozen fee and
queue label helpers. It is not a simulated trading run, not a UFC panel, and
not live validation. `FROZEN_EXPERIMENT.json` still has `results: null`,
`pnl: null`, `MZ: null`, and `roi: null`. `results/EMPTY_RESULTS.json` still
has those fields null, and `winner` null. Those fields stay null on purpose:
this page is not profit, and the schema probes are not folded back into the
freeze. No fill was awarded. No P&L figure is reported.

## Command

From `kalshi_c1_kxufcfight_lab_20260922`, Python 3.12.3, standard library:

```bash
python3 -m unittest -v tests.test_bakeoff
```

Ran 16 tests in 0.004s. Result: OK. Failures: 0. Errors: 0.

The checks that passed are the predeclared ones: the feebook and rails
modules are imported at the pinned commits and file hashes, and neither is
copied; series `KXUFCFIGHT` resolves as `default_unknown_series` because the
stub override map is empty; the `000` pointer matches the shadow-file sha256
and does not parse that JSON; both arms carry the same `5000` USD
measurement-contrast label; spending that label, porting the `000` strategy,
and retuning `000` raise; the collector stub is `READY`; clock re-join is
`KICKED`; admit is `NOT_ADMITTED` with reported settled N 4 and admitted
settled N 0; `clock_admit` raises on an `ADMIT_PASS` argument; `mz`, `roi`,
and `apply_resolutions` raise `ClockRefused`; the resolution hook names four
empty slots and refuses a stored resolution or a stored pnl; `lee_ready` raises when a price sits
above or below a midpoint and when native `taker_*` fields are already
present; native `taker_outcome_side`, `taker_book_side`, and legacy
`taker_side` agree, and a disagreement or a missing field refuses a side;
queue bins are exact equality with `rails.scenario_queue` and an absent
ahead stays null; freshness follows `rails.judge_freshness`, including a
keepalive and an unchanged book; a one-cent maker quote is the rails credit
refusal and places no order; a schema touch probe matches
`feebook.polarity_fill` and leaves `awarded_fill` null; the feebook would
call that examiner channel `completed_profit`, and this lab does not copy
that label; a missing taker and an incomplete book do not invent a side; an
invented `fill_count` is refused; the schema walk labels both arms, keeps
`results`, `pnl`, `MZ`, `roi`, and `winner` null, and does not rewrite the
empty results file or the freeze.

The frozen feebook suite was rerun from its own directory: 37 tests, OK.
The frozen rails suite was rerun from its own directory: 44 tests, OK.
Those reruns check unchanged modules. They are not KXUFCFIGHT results.

## Limitations

- Maker and taker fees are whatever `feebook.order_fee` and
  `feebook.polarity_fill` return at pin
  `22371178cb2663250b4762f328069571c48cb551`, with `round_up=True`. This lab
  does not copy that function. Series `KXUFCFIGHT` is
  `default_unknown_series`. No UFC fee-schedule override was added. The Grok
  unrounded comparator is not an input.
- Freshness is `rails.judge_freshness` at
  `6a28e0d6254327ea4e6451c781bec56215ac6cac`. A keepalive is not a book.
  Queue bins are `rails.scenario_queue` for `q3300` and `q10000`. Other
  sizes are `outside_pinned_bins`. Schema `queue_ahead` values are vectors,
  not observed queues. No queue-fill simulator ran.
- The shared `5000` USD figure is a measurement-contrast label on
  `KXUFCFIGHT` and on the `000` pointer. It was not read from
  `common_config` or from `starting_cash`. It does not lock cash. It does
  not retune `000` and it does not port that strategy.
- Taker side comes only from native public `taker_*` fields. Lee-Ready has
  no successful path. A missing bid stays an incomplete book.
- `schema_probe_contracts` is a field shape. `awarded_fill` is null. No
  resolution was attached.
- The conductor reports settled N of 4 on two finalized events, and the
  clock re-join is `KICKED`. Admit status is `NOT_ADMITTED`. Admitted
  settled N is 0. The four resolution slots are empty placeholders.
  `MZ` and `roi` were not computed from those settles. No live order
  client was added. No Q1–Q7 directory, and neither the feebook lab nor
  the rails lab, was modified.

No profit is reported.
