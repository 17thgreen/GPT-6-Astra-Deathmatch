# Q6S5 KXMLBSPREAD FEE+QUEUE — CAPTURE PLAN 2026-09-25 (ET)

**Packet:** `Q6S5-KXMLBSPREAD-FEEQUEUE-HARNESS`  
**Series:** `KXMLBSPREAD` ONLY (NOT KXMLBGAME ML / NOT S1 retune)  
**Status:** STUB — freeze-before-implement; GET-only; no orders; no `admit.py`  
**Panel stub:** `lab/astra-capture/q6s5-kxmlbspread/panel_stub.json` · sha256 `c7f1f1f4ca263838c4600ed46db8f525b68efc5399a567bd60929d18d76803cc` · `2026-09-25.q6s5-kxmlbspread-v0` · admitted_at **null** · 6 events / 12 markets  

## Purpose
Seed GET-only fee+queue honesty capture under fee_type=quadratic multiplier=0.5 **CACHE-LABELED** (not live R1-P1 `/series` pin until Examiner tests) vs Q6-000 $5k bakeoff pointer.

## Subset selection (panel stub)
Authentic subset of scout raw `markets_open_KXMLBSPREAD.json` (sha256 `80b52f47c836248d5869806d7f59617535e6b78258367ebe6045af4275fff7e7`; 93 markets / 15 events):
1. Sort `event_ticker` lexicographically; take **first 6 events**.
2. Per event: group markets by team-side (ticker suffix stripped of trailing digits); pick **lowest `floor_strike`** market per side; keep 2 (even YES-side pair across the two teams).
3. Markets copied **verbatim** from scout raw — no invented fields / fills / depth / PnL.

Selected events/markets are enumerated in `panel_stub.json` → `subset_selection.rows`.

## Capture slots (post-ACCEPT implement only)
| Slot | Path | Notes |
|---|---|---|
| Panel stub | `lab/astra-capture/q6s5-kxmlbspread/panel_stub.json` | NOT_ADMITTED |
| Future admitted | `lab/astra-capture/q6s5-kxmlbspread/panel_admitted.json` | Clock only; Variants does NOT run admit.py |
| Lab | `lab/astra-science/kalshi_q6s5_kxmlbspread_feequue_lab_20260925/` | created on IMPLEMENT |
| Scout raw (pin) | `packets/scout_sports_q6_screen/raw/markets_open_KXMLBSPREAD.json` | immutable pin |

## Hard refuse
GET-only · no Logan keys · no live orders · no invent fills/PnL/depth/settled counts · no KXMLBGAME ML retune · no Q6-000 retune · no Cap-SR reopen · no dual-cloud · Examiner HOLD_PRE_PR until merge · fee remains cache-labeled until live `/series` pin.

## Done =
Freeze MD + harness folder + panel stub + this capture plan + maximize pin + ACCEPT ping on disk. No cloud until Conductor ACCEPT+IMPLEMENT GO.
