# R2-P5 SOT-ID unit results

September 23, 2026. This file records a code check of the frozen SoT and
identity audit harness. It is a unit verification. It is not a simulated
trading run and not live validation. `FROZEN_EXPERIMENT.json` still has
`results: null` and `pnl: null`. `results/EMPTY_RESULTS.json` still has
`sot_pin_mismatch_n`, `holdout_mixed_refuse_n`, `delta_kickoff_sec_mode`,
`identity_join_ok_n`, and `external_odds_invent_refuse_n` null. Those
fields stay null on purpose. This page is not profit, and it is not folded
back into the freeze hashes. No tape walk was run. No P&L figure is
reported. This is not an Examiner pass and not a live-order certification.

## Command

From `kalshi_r2p5_sot_id_lab_20260923`, Python 3, standard library:

```bash
python3 -m unittest -v tests.test_orchestrator
```

Ran 8 tests in 0.083s at 2026-09-23T16:51:09Z. Result: OK. Failures: 0.
Errors: 0.

The checks that passed are the predeclared ones: harness freeze sha256
`0424455f062b7c46c7c6161b84fb7b29702719acc45bf6a61b4e8f16c5e26457`; parent
accept sha256
`712e4771bf2783dbee1e4c553194cd2896a468184f2849f24e58c3eb350ff499`; ADMIT-1
SoT seed sha256
`1edfa91979ab5dac72e28cc5e2ad5ff08aab414b5574fe115f86fb7d85e2ac4b` with 16
rows, all `KXNFLGAME`, all `window_clock_source=kalshi_occurrence`, all
`delta_kickoff_sec` 10800, `panel_version`
`2026-09-22.1-kalshi-occurrence-sot`, admit stamp
`2026-09-22T21:18:13Z`; schema sha256
`da7f6badd37d52fbd977681924379c3552f0dbfec94729d86ea411fb473ce53c`; PIT@CLE
identity cite sha256
`f5ca19f15940a80476d1590e506951df87df619160b477f1dff06cc3554cb520`. Fee pin
`22371178cb2663250b4762f328069571c48cb551` and rails pin
`6a28e0d6254327ea4e6451c781bec56215ac6cac` with those trees unchanged since
those commits. R2P5A0 `sot_pin_match` and R2P5A1 `holdout_delta_bin` leave
the five instrument fields, `results`, and `pnl` null. PIT@CLE holdout
stays `2026-10-02T00:15:00Z`.

`fee_source` is feebook. `rails_source` is rails. Both are import-only.
No fee quote was written onto a seed row. `external_odds_path` is null and
every `external_odds_present` value is false.

## Limitations

- The 16-row seed is the attached ADMIT-1 file. Structural uniformity
  (`window_clock_uniform`, `delta_values_uniform`) is a schema check. It
  is not `delta_kickoff_sec_mode`, and that scorecard field stays null.
  The seed's stated delta is 10800 on every row. That integer is not
  copied into the freeze scorecard.
- PIT@CLE identity was checked against the hash-freeze cite: event
  `KXNFLGAME-26OCT01PITCLE`, holdout unchanged, SoT
  `2026-10-02T03:15:00Z`, T−7d `2026-09-25T03:15:00Z`.
  `identity_join_ok_n` stays null. This check is not a panel re-admit.
  The holdout file bytes cited inside that markdown (`f8f6b577…`) are not
  in this commit. The cite file itself is pinned.
- An explicit `window_clock_source=holdout_mixed` row loads. A silent mix,
  where the T−7d anchor follows holdout while the source stays
  `kalshi_occurrence`, raises `HoldoutMixedRefused`. The refuse count
  stays null.
- Invented `edge_at_quote` while `external_odds_present` is false raises
  `ExternalOddsInventRefused`. Rewriting the PIT@CLE holdout to the SoT
  raises `RewriteHoldoutRefused`. A stated delta that disagrees with the
  two clocks raises `DeltaInconsistentRefused` and does not edit either
  clock.
- The attached pre-ACCEPT payload sha256
  `b796bfbbb3e78142569befd6a69801caaa662ed92072807df4068d49624f2926` is
  refused as a seed and as a scorecard. It is labeled `pre-ACCEPT empty`
  and omits two scorecard keys.
- `lab/governance/astra/` is absent. Packet bytes are the copies under the
  lab and under `packets/R2_P5_SOT_ID_HARNESS/`.
- No public GET was issued. No Logan key was read. No order route exists
  in this lab. `admit.py` was not run. S2 and R2-P4 stay queued. The
  ADMIT-1 recorder was not edited and its poll was not taken.
- Sibling labs in `DOES_NOT_MODIFY`, including L2-CAT, feebook, rails, and
  `nfl_prospective_recorder_20260922`, match
  `e54554ff79b663b30836cd34f8d20004a9022a0a`.
