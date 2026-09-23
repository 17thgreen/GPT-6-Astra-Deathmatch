# C1 KXUFCFIGHT production orderbook pin

September 23, 2026. This file is the hypothesis for a GET-only collector
scaffold. It is committed before that collector runs and before any public
orderbook response is recorded. No figure here is a trading result. The
fee and queue honesty hypothesis in `EXPERIMENT_SPEC.md` stays the prior
freeze. This file does not replace it and does not retune Q6-`000`.

## Question

On the Clock-admitted panel `lab/astra-capture/c1-kxufcfight/panel_admitted.json`
(`panel_version` `2026-09-22.c1-kxufcfight-v0`, `admitted_at`
`2026-09-23T00:49:43Z`, sha256 prefix `24426d80`), can one public GET pass
write orderbook bytes only under
`lab/astra-capture/c1-kxufcfight/orderbooks/` and pin each file's sha256 into
`FROZEN_EXPERIMENT.json` and `results/verification.json`?

If that pass cannot populate a complete four-market capture, the recorded
status is `FIXTURE_GAP` and the Examiner status stays `NOT_SCORED`. Either
outcome leaves `results` and `pnl` null.

This is a capture-pin question. It is not an Examiner score and not a tape
walk.

## Predeclared capture

One pass. No recorder loop. `recorder_started` on the admitted panel stays
false. This pass does not edit `panel_admitted.json`, the kernel, the
feebook core, or the rails core.

Host, exact: `https://api.elections.kalshi.com`.

Route, exact, GET only:
`/trade-api/v2/markets/{ticker}/orderbook`.

Tickers, exact, the four admitted markets and no others:

| Ticker |
|---|
| `KXUFCFIGHT-26SEP22CONGUA-GUA` |
| `KXUFCFIGHT-26SEP22CONGUA-CON` |
| `KXUFCFIGHT-26SEP22DEGMOR-MOR` |
| `KXUFCFIGHT-26SEP22DEGMOR-DEG` |

`KXUFCFIGHT-26SEP22ORTDAS-ORT` and `KXUFCFIGHT-26SEP22ORTDAS-DAS` stay
dropped. A query string, a fragment, a redirect, another host, another
method, and any portfolio or order route are refused. No `Authorization`
header is sent.

Spacing between ticker GETs on a live pass is 12 seconds, matching the
panel throttle note for single-ticker GETs. Unit tests may set the gap to
zero because they use a fake transport and do not open a socket.

A response is writable only when the HTTP status is 200 and the raw JSON
object contains `orderbook_fp` or `orderbook` with list-valued bid sides.
Empty bid lists are still the venue payload. They are not filled in. A
payload that carries `pnl`, `results`, `fills`, or `strategy_ev` is not
written. Non-200, invalid JSON, and transport errors write nothing.

The pass writes a file only when all four tickers succeed. A partial set is
`FIXTURE_GAP` and leaves the directory without new JSON. Existing JSON in
the directory is not overwritten.

Bytes are stored as received. The sha256 is of those bytes. The collector
does not edit `FROZEN_EXPERIMENT.json`.

## Pin and refuse

`production_orderbook_pins` in `FROZEN_EXPERIMENT.json` maps
`lab/astra-capture/c1-kxufcfight/orderbooks/{ticker}.json` to sha256.

When the directory contains a JSON file, every file's digest must equal the
pin and every pin must name a file that is present. Any other JSON is
refused with `production orderbook pin`. Absence of both files and pins is
not a silent score. The score gate treats that absence as `FIXTURE_GAP`.

Synthetic books at `fixtures/synthetic_orderbooks.json` remain the in-memory
label stand-in for reciprocal book, `order_fee`, freshness, maker-credit,
and queue-bin checks. They are refused for scorecard fill. A pinned
production file does not copy depth, volume, or open interest into the
scorecard.

## Examiner gate

`score_status` stays `NOT_SCORED`. `examiner_ready` stays false. `results`
and `pnl` stay null.

C1 becomes scorable only when both of the following are true: production
orderbooks are pinned under `lab/astra-capture/c1-kxufcfight/orderbooks/`,
and an Examiner-ready scorecard is opened outside this scaffold. This
hypothesis does not open that scorecard. `write_scorecard` still writes
nothing.

## Do-not

1. No live orders and no signed trading host.
2. No private routes and no invented fills, volume, open interest, or PnL.
3. No Q6-`000` retune and no edit to the feebook or rails cores.
4. No use of the synthetic stand-in as a production pin.
5. No backfill of the dropped ORTDAS tickers.
