# R3-P4 L2 shape capture slot (stub only)

**panel_version:** `2026-09-22.r3-p4-l2-shape-v0`  
**status:** no recorder running — the conductor stub is on disk (`admitted_at` null)  
**events / markets:** 4 events, 6 markets (sports 4 NCAAF, nonsports 2 KXBTC)  
**panel stub sha256:** `7477e023ab70c59a6739650155ddb9d77077766e3afd80443e540d60b5a86cbb`  
**seed summary sha256:** `e0d5281133d89d5f0215a8f02ae438b688bf53e4a48f2eb4c3727db4a29bb6f2`  
**isolation:** separate from ADMIT-1, S1, S4, S5, and R2-P3 — do not steal poll budget  
**admit gate:** do not run `admit.py`; stub only

This README is lab-authored. It is not a conductor-box byte. The panel stub
beside it is the conductor file, copied verbatim. `SEED_SUMMARY.json` is
the attached import-only summary, also copied verbatim. Volume fields are
null. `half_spread_bps` and `l2_shape` on each market are null.

`panel_admitted.json` is absent. When Clock join writes one, the harness
prefers that file and still refuses invented depth, Lee-Ready, ATL@GB,
live orders, and a non-null `results` or `pnl`.

`packets/r3_p4_l2_shape/live_get_2026-09-22/` is not in this checkout.
This directory does not invent it. Recorded order books are the ones
already inside `panel_stub.json`.

No recorder is started. The planned db path, if a later seat starts one, is
`lab/astra-capture/r3-p4-l2-shape/capture.sqlite`. GET-only. No Logan keys.

Category-slice harness: `kalshi_r3p4_l2_cat_lab_20260923/`.
