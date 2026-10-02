# Q6S5-KXMLBSPREAD-STRATEGY-FILL-PR60-SCORABILITY

Freeze `213ee6dd33f292c8041977b0b8d7566da9412fd3debe0597643c500dc1e42db4`.
Conductor ACCEPT `9c6e19ca11a855015fb4e3e63cd65ae5e5c334875240e817e164e988426df9f5`.
That ACCEPT is the settlement-pin amendment to freeze `9f50ba19…` and the implement GO. The packet `FROZEN_EXPERIMENT.json` is copied byte-identical and still records the pre-accept freeze status.

## What this lab measures

Feature family `strategy_fill_pnl_path`. Knob `fill_model` with the single value `public_trade_through_conservative`. `mechanic_demo_observed` stays unavailable. Family size is 1. Evidence class is `IN_SAMPLE_DEV / HISTORICAL_REPLAY`.

Universe: the six Sep-25 KXMLBSPREAD markets named in the freeze. Sep-24 tickers and KXHIGH raise `ClosedUniverseRefused`. The ADMIT-1 window `[2026-09-27T00:00:00Z, 2026-09-30T04:00:00Z)` is excluded. `capture.sqlite` and the weather `archive.sqlite` are refused without being opened.

## Rules

`tape_quotes.py` implements R01 and R03–R12, R20–R21, R26, and R29–R30. `captured_utc` is the filename stamp. Maker price is the max displayed bid. `queue_ahead` is the displayed size at that price. A missing bid places no maker on that side. A crossed or locked book places neither leg. Cancel is the next dated snapshot, including an ineligible one. The last order rests until the earlier of a later inactive GET and the earliest trades-request `ts_utc`.

`fill_engine.py` implements R13–R22. The print window requires the print's whole second to be strictly after the placement stamp and the full timestamp to be strictly before cancel. A print exactly at the cancel stamp belongs to neither order. YES bids consume native `taker_side=="no"`; NO bids consume `taker_side=="yes"`. Native fields are checked with the parent `classify_native_taker` called without a ticker, because a panel ticker is refused by that function before the agreement check. Disagreement is excluded and counted. Lee-Ready raises. Block trades and price rows whose yes and no dollars do not sum to 1 are excluded. The fill is one contract at the limit when cumulative size at or through the limit reaches `queue_ahead + 1` on a strict-through print. PR60 `classify_fill` supplies the through flag and must agree. Taker legs buy one contract at `1 - best opposite bid` when that level's size is at least 1. The taker does not reduce `queue_ahead`.

`scoring.py` copies PR62 `cache_fee_table` and `cache_order_fee` verbatim. The label is `CACHE_NOT_R1P1` and `formula_id` is null. PnL is settlement dollars minus fill price minus fee. A YES leg uses `settlement_value_dollars`. A NO leg uses one minus that value. The outcome field on the settlement body is not read. Empty bins and zero denominators are null. A computed sum of zero stays zero. `fees_2x` uses `times=2`. `one_tick_worse` adds `0.01` to every buy and charges the greater of the fee at the fill and the fee at the worse price. Stresses do not change which legs filled.

`settled_join.py` is `settled_join(fills_bytes, fills_sha256, settlement_dir)`. The manifest cross-check is a separate function. The join requires finalized status, `close_time < settlement_ts < response_utc`, and every fill before close. Values must be 0 or 1. A filled ticker with no settlement row is unresolved inventory. Guard failures raise.

## Lookahead

Quotes and fills are functions of the pinned tape. Settlement dollars are applied only after the fill bytes are hashed. Passing trades into `build_quotes` raises `LookaheadRefused`. A book or GET stamped after `t0` does not change the placement price, size, queue, side, or freshness at `t0`. The cancel time of the last resting order still follows R12, and the cancel time of an earlier order still follows R11. Those stamps are not a new price.

## Committed outputs

`results/EMPTY_RESULTS.json` keeps results, pnl, roi, and every metric null. `results/UNIT_RESULTS.md` may record structural counts and the quote/fill sha constancy check. Quote files, fill files, and PnL figures are not committed. The Simulator runs the merged runner. The Examiner scores. Examiner status stays `HOLD_PRE_PR`.

Verdict domain on every output is `ITERATE|INCONCLUSIVE`. `counts_toward_keep` is false. `promote` is false. Fills are `MODEL` with tag `replay`. `A1_null_reason` is `STALE_BIN_EMPTY` because the pinned books leave the stale bin empty. That reason is pre-declared by the ACCEPT.

## Verification

From this directory:

```bash
python3 -m unittest discover -s tests -v
```

That run is a code check. It is not an Examiner score.
