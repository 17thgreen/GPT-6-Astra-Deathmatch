# Schema-only KXUFCFIGHT fixture

`schema_only_kxufcfight.json` is a field-shape sheet for packet
`C1-KXUFCFIGHT-MEAS`.

- Label: `SCHEMA_ONLY`.
- Collector stub: `READY`. The schema sheet clock stays `NOT_ADMITTED`.
  Scorecard settled N: 0.
- The books are synthetic bids-only shapes. They are not captures.
- No row is a fill or a resolution.
- `queue_ahead` values are schema vectors for the rails bin helper. They are
  not observed UFC queues and not observed `000` queues.
- The `000` arm is the instrument pointer. It is not the production
  `q3300_d0.25_000` gzip and it is not a retune of that strategy.
- The shared `5000` figure is the measurement-contrast label on both arms.
- `panel_admitted.json` is a byte copy of
  `lab/astra-capture/c1-kxufcfight/panel_admitted.json`.
  `panel_version` `2026-09-22.c1-kxufcfight-v0`.
  sha256 `24426d804c51bde23cf2557a11a8481a12026da10024094c4ae546d1f7d3956e`.
  `admitted_at` `2026-09-23T00:49:43Z`. Stub
  `PANEL_ADMITTED_C1_UFC_ONLY`. Two events, four markets.
- `resolution_join_admitted.json` copies the four
  `result_observed_live_get` labels from that panel. `results`, `pnl`,
  `MZ`, and `roi` on the fixture are null. The cited directory
  `lab/astra-capture/c1-kxufcfight/resolutions/` has no JSON in this
  checkout. This fixture is not those missing bytes and it is not a payoff.
- `resolution_hook_not_admitted.json` is the closed-PR placeholder.
  Label `NOT_ADMITTED`. The wiring path refuses it.

This file does not contain ledger bytes.
