# Unit results

Code verification from this directory:

`python3 -m unittest discover -s tests -v`

Ran 22 tests in 106.526s at 2026-10-03T20:39:33Z. Result: OK. Failures: 0. Errors: 0. This run is not an Examiner score. The suite covers T01–T14: label-permutation invariance, lookahead, the 31/31 join, holdout and ADMIT-1 refusals, fee formula, structural reproduction, unhedged contract-hours, markout nulls, Lee-Ready refusal, manifest tamper, de-vig examples, framing, untouched 000 files, and the ex-post `[U]` tag.

Built on `761eaaedc153dca9807d7630adcea1ae3387d9c1`.

## Pins

| Pin | sha256 |
|---|---|
| Bundle `pins/EXT_K1_authentic_pins_2026-10-03.tgz` | `0f8f529733bfd1ccb01b36f312cdc20865cc2811c04dcd3c812d50c67295db38` |
| Inner MANIFEST (37 files) | `a041561e130fb97eaa8d7bfab5dd6fa53963fa4fbdb13c00cd4f71089e0e3db5` |
| Freeze markdown | `5c40fb9d03a924e40577a81f262231701e331c98922f60f6dc7ab65a2dbed6d3` |
| Freeze JSON twin | `be3e88336389bc62c40413785e6ffb4a572e1dbd006d7cf3dfbc962f8184efaa` |
| Conductor ACCEPT | `021290077cbbed277455145d2e56e1335f6ae331d56c2ad79d4d85b405559397` |
| 000 fills ledger | `9d56f5d3c599e092606be9f4a1ad41ae8baabff4921d3d722adf0b57ac944a3f` |

The runner hashes every manifest path before parsing it. ACCEPT `verified.manifest` `5e8f79063f132fe2db97ad3ecff5fea463d429f167abed09c58398a87fcadf01` differs from the inner MANIFEST. The runner binds to the inner MANIFEST that ships in the bundle.

## Structural reproduction

These are ledger and tape counts. `results`, `pnl`, and `roi` are null.

| Fact | Value |
|---|---|
| Fill rows | 12,853 |
| Trade rows | 681,732 |
| Quote rows | 364,988 |
| Tickers / events | 62 / 31 |
| Maker NO-side share | 0.989706 (raw 0.9897056563576855) |
| Taker YES contract share | 0.916882 (raw 0.9168821893495998) |
| Unhedged contract-hours | 603262.7291176913 exact against the ledger (reported 603262.7291) |
| FIFO contract-hours | 603262.729117692 |
| Opening portions | 6,161, all maker |
| Opening = closing = paired units | 163,518.22 |
| Open at window end | 0 |
| Join | 31/31 (28 exact, 3 via `{JAC→JAX, LAR→LA}`) |
| Block trades | 0 |
| Maker fills at or after K−3h | 0 |
| `structural_ok` | true |
| `structural_failures` | empty |

## Headline measurement

Every figure below uses the nflverse consensus anchor and carries `EX_POST_ANCHOR_U`. nflverse line timing undocumented [U]; ex-post anchor only; cannot support a tradable pre-game signal claim.

Verdict `DESCRIPTIVE`. Reason `delta_star_ci95_does_not_exclude_0`. `counts_toward_keep` false. `promote` false. `family_size` 1. `evidence_class` `IN_SAMPLE_DEV / HISTORICAL_REPLAY`. `new_knobs` 0. `examiner_pin_account_class` null.

Primary split `S_DEV` at δ = 0.005. Primary horizon 1,800 s. Primary contrast Δ* is the contract-weighted gross markout of AGAINST minus ON.

| Quantity | Value |
|---|---|
| Δ* gross | −0.000205 |
| Δ* net (beside gross; does not move the verdict) | −0.000373 |
| 95% CI gross | [−0.000577, 0.000188] |
| `ci_excludes_0` | false |
| Bootstrap | `random.Random(20261003).choices`, B = 10,000 kept, 0 dropped |
| ON at 1,800 s | n = 2,664, contracts 68,640.58, mean gross 0.004955, censored contracts 154.29 |
| AGAINST at 1,800 s | n = 2,578, contracts 72,781.55, mean gross 0.00475, censored contracts 313.26 |
| NEUTRAL at 1,800 s | n = 919, contracts 22,096.09, mean gross 0.005211, censored contracts 154.38 |
| UNCLASSIFIED | n = 0, contract share 0 |
| UCH ON / AGAINST / NEUTRAL | 290,467.1399 / 204,907.8475 / 107,887.7416 |
| Premium-hours | 270,526.4574 |
| Hold-time p50 / p90 | 1,002.461117 s / 30,789.805693 s |

Primary refusal gate `x=0.02|E=0|devig=proportional`: refused 700 portions, kept 5,461. Refused contracts 20,031.8 (share 0.122505). UCH refused 86,964.4417 (share 0.144157). Refused mean gross at 1,800 s is 0.003685. Kept mean gross at 1,800 s is 0.005068. Grid role `SENSITIVITY_ONLY_NEVER_SELECTION`. No cell is selected.

Headline maker-order fee total is $1,286.22, label `CACHE_NOT_R1P1`, name `NON_DIRECT_CENT_HEADLINE`. Direct-member maker-fee total sensitivity is 1,277.0453 and is not the headline. Maker coefficient 0.0175. Cached `KXNFLGAME` maker multiplier is 1 (schedule lines 485 and 492).

## Invariance

One thousand `Random(20261003)` shuffles of the 31-game `(away_score, home_score)` pairs, plus a shift-1 derangement, left these artifacts byte-identical. The shift-1 derangement changes only the settlement artifact, which is outside the constancy hash.

| Artifact | sha256 |
|---|---|
| gate_assignments | `1594860cb1d20ee38cb03877d9ec30eab11fc74dd0d9d51734d9b12b280aae70` |
| splits | `6fb24d902c0e1cc89869ac6dab815792b1bb894eb90cb9535a5ecfb870a60ee2` |
| uch | `947970df887c49d1f7656c4666f2ebaf4de76ec865c718a9513ecf0f4f5c3733` |
| markouts_h | `c0d4d2a28b9f4167a4dcefed4262ad7635637a59ac0b835e2b1dc45d1ef91461` |
| constancy | `a73a90e0156c1b64b0ae3d70fd1b58e7279d4fff0b1c0b00a93108f62061d2d7` |

## Limitations

The 31-game cohort is development-grade and reused. Fills are hypothetical replay fills. The nflverse moneyline is an ex-post anchor. Settlement uses nflverse scores and assumes they equal the Kalshi settlement, which is not on the box. The decisions ledger sha256 `e6db52374f834bba210d5c17836828ac3bf0dd54ca9feb5836ea71a611c61b71` is not in the bundle and is not read. `SOURCE_PINS.json` and a precomputed `CONSENSUS_FIXTURE.json` were not in the bundle; the lab recomputes the fixture. The account class remains an Examiner-owned pin. Markouts are the measurement. This file does not retune `q3300_d0.25_000`. Examiner status stays `HOLD_PRE_PR`. Zero live orders. Zero GETs. `capture.sqlite` is refused. Lee-Ready is refused.
