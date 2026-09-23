# Schema-only KXUFCFIGHT fixture

`schema_only_kxufcfight.json` is a field-shape sheet for packet
`C1-KXUFCFIGHT-MEAS`.

- Label: `SCHEMA_ONLY`.
- Collector stub: `READY`. Clock: `REFUSED`. Settled N: 0.
- The books are synthetic bids-only shapes. They are not captures.
- No row is a fill, a resolution, or an admitted settled panel.
- `queue_ahead` values are schema vectors for the rails bin helper. They are
  not observed UFC queues and not observed `000` queues.
- The `000` arm is the instrument pointer. It is not the production
  `q3300_d0.25_000` gzip and it is not a retune of that strategy.
- The shared `5000` figure is the measurement-contrast label on both arms.

This file does not contain ledger bytes.
