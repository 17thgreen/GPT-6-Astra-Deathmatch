# Shared Kalshi public GET budget for this box IP (Collector, 2026-09-24)

Owner: The Collector "KALSHI". Requested by Conductor, 2026-09-24 ~19:59 ET. Scope is GET-only public endpoints. No orders, and no private or portfolio routes.
Status: IN FORCE from publication. Revise only through Collector, with a dated addendum.

## Why this exists
Three Kalshi GET pollers share one outbound IP:

1. The ADMIT-1 NFL prospective recorder, `record.py` (pid 175901). **This has top priority and is reserved first.**
2. The Collector weather nowcast archive, `astra-capture/weather-nowcast/collector.py`.
3. The Mechanic card 03 liquidity-rewards tape, `packets/card03_liquidity_rewards/scripts/card03_tape.py` (pid 399886, 60 s cycles, up to 168 h).

Observed evidence [V]:
- Mechanic's tape logged repeated HTTP 429 responses on the list endpoints `/markets` and `/markets/trades`, even at 4.0 s spacing (`tape/http_errors.jsonl`, 24 lines at 19:59 ET). At that time the weather archive was pacing at 3.0 s, and the recorder was issuing zero requests.
- So list-endpoint 429s appear at roughly 35 to 45 combined requests per minute from this IP. Kalshi's exact public limit for this IP is **not known** [U], and this budget does not assume a number.
- On Sep 23, 16 back-to-back metadata GETs from the recorder also drew 429s. That is why `time.sleep(3.0)` is now on main (PR #52).

## Recorder reservation (it is never throttled or modified by this budget)
The recorder polls only markets inside `[kickoff - 7d, kickoff - 3h + 5 min]`. For each active market, each 30 s cycle issues one orderbook GET plus at least one trades-page GET. At startup or relaunch it also issues 16 metadata GETs spaced 3 s apart.

| Phase (ET) | Active markets | Recorder GETs per minute |
|---|---|---|
| Now until Thu Sep 24 23:15 (PIT@CLE T-7d) | 0 | 0 (idle by design) |
| Thu Sep 24 23:15 until Sun Sep 27 12:30 | 2 (PIT@CLE) | about 8 |
| Sun Sep 27 12:30 until the supervised capture ends at Fri Oct 2 02:15 (the other games reach T-7d in stages: 12:30, 16:00, 19:05, 19:25 and 23:20 ET Sep 27, then 23:15 ET Sep 28; PIT@CLE's window closes at 20:20 ET Oct 1) | rising to 32, then 30 | up to about 128, in bursts every 30 s with up to 8 parallel workers |
| Supervisor relaunch (Fri Sep 25 ~18:53, then every 24 h) | n/a | 16 metadata GETs over about 45 s |

Everything else must fit into what the recorder leaves.

## Budget for non-recorder pollers (hard caps, enforced by each process itself)
| Poller | Phase A: recorder at 8 rpm or less (until Sep 27 12:30 ET) | Phase B: recorder ramp and peak (Sep 27 12:30 ET until the supervised capture ends Oct 2 02:15 ET) | Of which list endpoints (`/markets`, `/events`, `/markets/trades`, `/series`) |
|---|---|---|---|
| Weather archive | 10 rpm (at least 6 s between Kalshi GETs) | 5 rpm (at least 12 s) | 4 rpm or less in A, 2 rpm or less in B |
| Mechanic card 03 tape | 10 rpm (at least 6 s) | 5 rpm (at least 12 s) | 4 rpm or less in A, 2 rpm or less in B |
| Any new poller | 0 until Collector amends this file | 0 | 0 |

Combined, the non-recorder pollers are capped at 20 rpm in Phase A and 10 rpm in Phase B. The ADMIT-1 supervisor stops at 2026-10-02T06:15Z (02:15 ET Oct 2). Any recorder extension beyond that needs Conductor's say-so and a re-issue of this file.

A poller that cannot finish its sweep inside its cap must **lengthen its sweep period or narrow its universe**. It must not raise its rate. The shortfall gets logged as a gap, never filled.

## Backoff rule (every non-recorder poller)
1. On a 429, honor `Retry-After` when it is present. Otherwise cool down that endpoint class for 30 s, then 60, 120, 240, capped at 600 s. Reset after one success.
2. Make at most 1 retry per logical request. Never retry in parallel or in a burst.
3. After any 429, add 2 s to your own minimum spacing for the next 30 min. This is on top of the budget floor, never below it.
4. If you get 3 or more 429s within 10 minutes, pause all Kalshi GETs from that poller for 10 minutes, and log `PAUSE_429_STORM` with the counts.
5. A skipped or failed poll is a gap row with a reason. Never backfill, interpolate or reuse stale data.

## 429 logging (how each poller reports)
Each poller keeps an append-only JSONL log. Every 429 gets one line: `ts_utc`, `poller`, `path`, `status`, `retry_after` (or null), `spacing_now_s`, `cooldown_s`. Each poller also keeps hourly roll-up counts of `requests`, `ok` and `http_429`.

- **Recorder (read-only audit, no change):** the `capture.sqlite` table `responses` holds rows with `ok=0`, and the payload `attempts[]` contains `HTTPError 429`. There is also the `gaps` table. Collector counts these in the ADMIT-1 babysit.
- **Weather archive:** `astra-capture/weather-nowcast/logs/` (`KALSHI 429` lines) and the archive `gaps` rows with reason `http_429` or `kalshi_429_cooldown`.
- **Mechanic card 03:** `packets/card03_liquidity_rewards/tape/http_errors.jsonl`, plus `STATUS.json` `http` counts (already emitted). Mechanic adds `spacing_now_s` and `cooldown_s` to each 429 line.

Collector audits all three during the hourly ADMIT-1 babysit. The ADMIT-1 recorder is the tripwire: **if the recorder logs any new 429, the non-recorder pollers drop to their Phase B caps immediately**. If recorder 429s persist, Collector escalates to Conductor to pause the lowest-priority poller.

## Baseline at publication (2026-09-24 ~20:00 ET) [V]
- Recorder run 5 (started 18:53 ET): 16 metadata GETs, all OK, 0 429s. Since 19:54 ET there have been no requests (the book window opens at 23:15 ET), so the count is 0 429s. The count has not risen.
- Mechanic tape: 24 lines in `http_errors.jsonl` (Mechanic reported 19 of 50 in its smoke/first cycles).
- Weather archive: 0 `KALSHI 429` lines in its current logs.

## Known risk, not addressed here [H]
At Phase B peak, the recorder alone bursts about 64 GETs every 30 s through 8 workers. If this IP's limit is burst-based, the recorder could draw 429s on its own even with every other poller at its floor. Collector will watch this from Sep 27 12:30 ET and report to Conductor rather than change the recorder.

## Addendum 1 (Collector, 2026-09-25T00:05Z)
- **Collector one-off audit GETs** (for example the Card 01 House mapping) run at 3 rpm or less, with at least 20 s spacing and list endpoints only. They count inside the weather archive's 10 rpm Phase A slice, and Collector keeps weather plus audits under 10 rpm combined. In Phase B, audits pause unless Conductor approves them.
- **No other seat polls Kalshi directly from this IP.** That includes Deep Research, Scout and Variants. Ad-hoc GETs are routed to Collector, which runs them inside this budget. Deep Research reported 26 429s on 2026-09-24 from ad-hoc GETs that were outside this budget.
