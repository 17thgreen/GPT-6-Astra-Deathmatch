# Adversary refuse-bind — R2-P3 KXNFLPASSYDS prop-ladder
**Date:** 2026-09-22 (America/New_York)  
**Packet:** R2-P3-KXNFLPASSYDS-MEAS (**FROZEN** — Conductor ACCEPTED)  
**Owner:** The Adversary · **Reviewer:** Conductor  
**Cite:** `R2-P3_KXNFLPASSYDS_MEASUREMENT_FREEZE_KERNEL_2026-09-22.md` · Scout slate LAC@BUF + BAL@DAL 2026-09-27 · R1-P1 feebook · R1-P5 rails  
**Stance:** Bind refuse on freeze accept. No Q6-000 verdict change. No orders. No invented PnL. Measurement / provenance refuse — not a strategy kill.

---

## Direct answer

**Yes — refuse.**

1. **Completed-profit** without **R1-P1 fee channel** (forbid inherited Q7/Q6 fee literals).  
2. **Freshness from WS ping** — freshness must use content/transaction time (`content_fresh_flag`), not WS ping.  
3. **Maker-credit floor-zero** near 0/1 strikes — must stamp `maker_credit_floor_zero_refuse`; refuse silent credit.  
4. **`000` retune claims** — measurement contrast only; no quote/size/route retune.  
5. **ATL@GB substitution** — slate is LAC@BUF + BAL@DAL only; ATL@GB explicitly excluded.

**Results null until Examiner.**

---

## Refuse matrix (short)

| Claim | Condition | Adversary stamp |
|---|---|---|
| Completed-profit / fee-honest ladder EV | No R1-P1 fee channel | **REFUSE** |
| Fresh book / actionable tape | Freshness from WS ping only | **REFUSE** |
| Maker credit near 0/1 | Floor-zero not labeled refuse | **REFUSE** |
| `000` parameter / capacity change | Any from this packet | **REFUSE** |
| ATL@GB (or non-slate) enrichment | Outside LAC@BUF+BAL@DAL | **REFUSE** |
| Promote / live / invented PnL | Any | **DENIED** / RESULTS_NULL |

---

## Explicit non-actions

- No change to Q6-000 KEEP / Q7 KILL_B.  
- No Examiner replacement.  
- No orders.

**Artifact:** `lab/governance/astra/packets/R2-P3_ADVERSARY_REFUSE_BIND_2026-09-22.md`
