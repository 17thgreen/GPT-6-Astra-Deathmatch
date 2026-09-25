# CEM-ASTRA-20260922-001 — Q7 Arm B candidacy KILL

- **CEM_ID:** CEM-ASTRA-20260922-001
- **LINE:** Q7 Chosen-pair cost check · Arm B (original router · pair check on)
- **DECISION:** **KILL** as new shadow candidate
- **KEPT:** Q6 shadow incumbent label `000` (Arm D reference)
- **SELECTION:** `NO_NEW_SELECTION` · `live_promotion=false`
- **SCORED:** 2026-09-22 (ET) · Examiner (Kalshi)
- **PACKET:** `lab/governance/astra/packets/Q7_EXAMINER_SCORECARD_2026-09-22.md`

## Why killed (Examiner, frozen rule)

Arm B failed the pre-declared retention gate: `retains_95pct_of_D` = **false** on every stress (B/D ≈ 0.84 primary; lower on harsh queues). Other gates passed (beats original all stresses; improves both primary weeks; inventory within limit). Selection status **`NO_NEW_SELECTION`**; fallback shadow **`000`**.

## Not claimed

- No live promotion · no live orders
- No annualized / holdout / causal claim
- No ITERATE on this 2×2 without a new freeze
- Archivist does not re-score

## Artifact pins (from Examiner scorecard)

- Lab: `lab/astra-science/nfl_paircheck_lab_20260922`
- `results/paircheck_effects.json` sha256 `5d87ea610f22482c980868d8a31a228ca1931368d9eeab73add4256d2e117fdf`
- `results/verification.json` sha256 `eb1586bf13b1631951a4f177293350cb89fc7948a50fbb7044f4f05313ebc06f`
- `FROZEN_EXPERIMENT.json` sha256 `b0dd91699d2170e42c3a0ae9e27769a80f64f8121b116da030f253ac0d8a7f2b`
- Hash check (Archivist 2026-09-22 18:45 ET): pins match on-disk bytes


## Conductor addendum (2026-09-22)

- **95%-of-D displace bar STANDS** for this packet (Examiner refuse post-outcome soften/drop; new tolerance only via new freeze).
- This KILL does **not** prove the pair-check effect is zero — only that Arm B fails the predeclared displace bar vs D/`000`.
- Mechanism is **not** declared worthless; check helped both architectures; B still fails retention.
- Packet **CLOSED** for measurement. No invented PnL. No orders.
- Sources: `packets/Q7_EXAMINER_SCORECARD_2026-09-22.md` · `reports/RPT-Q7.md` (SCORED).
