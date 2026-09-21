# Q3 measurement protocol

Frozen before this round's new capture or historical markout outputs. Q1 and Q2
remain unchanged. No trading or account access is included.

## Purpose and evidence tiers

Measure the bottleneck behind completion: persistence of displayed prices,
displayed depth, previously received matching flow, and price movement after a
hypothetical fill. Public snapshots cannot identify cancellations ahead of an
order, our order's actual queue position, hidden transient changes, or execution.
Use trade-only service as an explicitly conditional diagnostic, never as a fill
label for a calibrated actual-execution model or as realized profit.

## Fixed measurements

- Development panel: the same NYG–LAR and ATL–GB events used in Q1. They cannot
  enter the holdout. Capture four team tickers for 720 seconds, target five-second
  book polls, trades every 30 seconds, ten book levels, public GETs only.
- Record request, receipt and local write timestamps. Use receipt/write time for
  information availability; exchange trade time only for later outcome labels.
  Start with trailing-hour trades, overlap subsequent queries by 120 seconds,
  exhaust pagination and deduplicate IDs. Failures remain in the record. A
  complete paginated response does not prove all late prints have arrived.
- Select best bids by maximum price, irrespective of array ordering. Convert NO
  bids to YES asks via one minus price. Reject crossed/invalid quotes.
- A displayed-price spell ends at a first observed price change or at a gap
  exceeding 30 seconds. Record interval censoring at changes and right censoring
  at gaps/end. Initial spells are left censored. These are observed unchanged
  prices, not uninterrupted individual-order lifetimes. Depth changes do not
  identify whose queue position improved.
- Shadow joins: nonoverlapping per ticker/outcome, 250 contracts, .25-second
  assumed arrival delay, half participation after displayed starting depth has
  been consumed by exact-price opposite-taker prints. Stop at 600 seconds,
  observed best-price change, gap above 30 seconds, or capture end. Through-gap
  or right-censored unfilled joins cannot be labeled failed ten-minute fills.
  Report both observed fill events and censoring; no probability calibration.
- Features use only trades received strictly before the decision and with
  exchange times before it. Measure trailing-hour matching flow and projected
  volume minus depth. Feature rows and later labels are stored separately.
- Shadow post-fill markouts: first book received at/after fill+30/60/300 seconds,
  with at most 30 seconds target lateness; require no >30-second observation gap
  between fill and measurement. Record midpoint change and midpoint less fill
  price; neither is liquidation P&L. Exact fill time is itself hypothetical.
- Historical development markouts: original 31 games, q3300 Q1 router and Q2
  completion variant only. Use 120/300/600-second horizons. Select the most recent
  candle available by target under Q2's fixed 60-second publication assumption;
  require its as-of timestamp strictly after fill and age <=120 seconds at target.
  Report volume-weighted markouts, coverage, and per-game values, without treating
  fills as independent observations. No historical outcome becomes a new signal
  in this round. Shorter horizons cannot be resolved honestly from minute candles.

## Frozen future evaluation

HOLDOUT_MANIFEST.json reserves 32 schedule-selected future games whose complete
seven-day windows start after this freeze. Existing 31 games and the two forward
development events are excluded. Missing venue identities remain unresolved.
Schedule changes require dated amendments, not silent replacements.

Before any holdout labels are opened, lock the candidate and baseline code,
feature/schema versions, fees, latency, queue assumptions and risk settings.
Use one shared $5,000 account, identical execution assumptions and the original
T−7d to T−3h interval with five-minute winddown. Compare completed net P&L,
unhedged contract-hours, taker exits, concentration and unresolved inventory.
Require all 32 complete windows, verified identities, immutable data manifests,
no development overlap, and no unresolved positions before a profit comparison
can pass. Missing or partial captures yield INSUFFICIENT, never an omitted game.
Even a passing simulation remains conditional execution evidence.

No model is promoted in this measurement round. A short capture cannot train or
validate conditional actual-fill probabilities. A candidate must be frozen
before the reserved windows begin; otherwise that registry is ineligible and a
new future registry must be declared before collecting its outcomes.
