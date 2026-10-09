# GOVERNANCE EXTRACT — card01 PR-C (REJECT (c)/(d) P&L incl. one-tick-worse stress)
Sanitized extract written for the PR-C cloud kit (2026-10-08; rev 2 adds ruling 61c1e4ea). Every quoted line below is copied byte-for-byte from the source line named (the `>` prefix and the 'L<n>' tag are added). The sources govern; this extract changes nothing. Lines that are not quoted are not restated. It contains no forecast values, no candidate names and no private paths. Pre-outcome: no outcome, result or settled data was read to write it.
## Sources (pinned by sha256)
| Key | Source | sha256 |
|---|---|---|
| `BASE` | Base freeze (FROZEN 2026-09-24) | `c31724463d81747702910a2d5296c2fc21d2a1dbc594727b26ac3d894b55ec59` |
| `AMB` | Amendment B | `ee6af37cef95f1e468d28e5b06750caaca8b1706ec11ed5cf5cdce460524c2c6` |
| `ACCB` | Conductor ACCEPT-B | `74c5d49c0452ce97def7b36129ba362ebc4387627b93d5611bb67c5f8dfcbd23` |
| `AMC` | Amendment C | `cc75f09614ad285756fd7cb7f7a5c2ce4e711b5adb98102c2dd043ccfc1af0f0` |
| `ACCC` | Conductor ACCEPT-C | `2225c3fa0bea7c58cad59f52476f9fbe69e1d6fa813114a7557c748126dd2b1a` |
| `K3` | Conductor ruling 86baa504 (impl note fb4e5bc0/0c0992b1 ACCEPT + degenerate block) | `86baa504c639a74c22db72821ac0c09cdf63cb7aaf8941e74012b14dac3bb256` |
| `K2` | Standing bootstrap-pin rule | `6824793a44f5a10ee1d6e869e694d6681cfaba1681ff9b4bfb7cd0ed98242502` |
| `NH001` | NH-001 core (the 'NH-001 check' named by base §9 (d)); in repo at pins/NH001_recovered_2253c03c_core.py | `0f58065615726c4195e3c172557c87676e70658482ecef03458e42bb3ee813b7` |
| `PREC` | Conductor ruling b8cb27e0 (fee source, Q6, precedence) | `b8cb27e0e94c2a27c22fd1d92395109168a90ca78bb5928a65fbf0f89c397517` |
| `FU2` | Conductor ruling c05d7003 (PR69 FU2) | `c05d70037b82d62a9cf01740b50a34773f87025cd6887f5dcfc68f8a443bb813` |
| `FEEFIX` | Conductor ruling 715fbafd (FU2 item 1 rewrite) | `715fbafd588845867d7fe0af59b32a21d2411afc14bfb6da718f5592e0608703` |
| `V2` | Conductor amendment 2c870cd5 (v2 index-only admission) | `2c870cd57fc4acb4290c1273e06876e8380159f2f6614a5519314b43817a8583` |
| `R1ACC` | Conductor ACCEPT 69b98b2f (R1 spec r3) | `69b98b2f643a7510280cd6b959c30e285df081c8142b910808001db8cad5b81a` |
| `DISP` | Conductor ruling 861b7d14 (DISPOSITION) | `861b7d14e75979f798b872a2c16b6e440d4f5b6332d4ad9e1e81d713863f5757` |
| `OQ` | Conductor ruling e5227270 (R1 spec OQ1-11) | `e5227270b6e767b0c25fdfe68b8a859351a1a84d42200816c0f7eac6aad56bde` |
| `PRCR` | Conductor ruling 61c1e4ea (PR-C kit OQ1-9 + schedule) | `61c1e4ea948109508ef12497a96b45f728f8e183168b26bffb87f11fda6107ca` |
| `R3` | Examiner spec r3 (Conductor-ACCEPTED by 69b98b2f); interface to PR-C only | `c5b08459dd6f1e1e6cae65dbb13c4aa5b0d6a1418d79d3bae54c9370d9beede5` |

## 1. REJECT (c) and (d): definitions
- `BASE` §9 'Rejection rule (verbatim, research PDF Card 01)', L283:
  > **Rejection rule (verbatim, research PDF Card 01):** "Freeze one family and its forecast sources before observing future outcomes. Record revisions and orderbooks at actual receipt time. Compare the three baselines under identical feasible fills, then test the hybrid on untouched events. Reject if its gains disappear against market-only, are concentrated in one correlated event, or exist only at midpoints. Treat this as a slower research stream; one election cycle is not hundreds of independent experiments."
- `BASE` §9 'Operationalized', L285:
  > **Operationalized (any one means REJECT):**
- `BASE` §9 (c), L288:
  > - (c) The gain exists only against the mid, not against executable prices: the hypothetical taker P&L at ask is ≤ 0, or ≤ 0 under the one-tick-worse stress.
- `BASE` §9 (d), L289:
  > - (d) Top-1 race share of positive P&L is > 50%, or dropping the best two winners leaves ≤ $0 (the NH-001 check).
- `AMB` header 'What this amendment leaves unchanged', L22:
  > - PASS (i)/(ii) and REJECT (a)–(d) logic;
- `AMC` header 'What Amendment C leaves unchanged', L35:
  > - PASS (i)/(ii) and REJECT (a), (c), (d) wording;

## 2. Fills, prices, sizing, holding, stress (the P&L accounting)
- `BASE` §5 'Order timing and fill model', L187:
  > - **Order timing and fill model:**
- `BASE` §5, L188:
  > - Hypothetical taker at the snapshot: buy D YES at the YES ask, or D NO at (1 − YES bid).
- `BASE` §5, L189:
  > - Fill only if visible quantity at that price is ≥ 1.
- `BASE` §5, L190:
  > - Stress rows (v1.2 §G): one tick worse; fees 2×.
- `AMC` §C4.1 (anchor pattern mirrored for the PR-C entry table, ruling 61c1e4ea (9)), L114:
  > It uses no outcome. The Examiner emits it, computes its sha256, and sends the sha256 together with the UTC timestamp of hashing to the Archivist for the hash register, **before any race in the 92-race universe is called** (by any Designated Media Source or by a Kalshi determination). A stress row anchored after the first universe race call is not the frozen row; it may be shown only as labelled late and cannot clear the defect in §C4.3.
- `BASE` §5 Sizing, L191:
  > - **Sizing:** at most one contract per race, on the side where (p_hybrid of that side − price − fee − 2c buffer) > 3c reserve. This is the NH-001 gate, unchanged. Feasible size = min(1, visible depth).
- `BASE` §5 Holding, L192:
  > - **Holding:** hold to Kalshi settlement.
- `BASE` §9 p16 item 8 (stopping rules), L277:
  > | 8 | Stopping rules | Single decision time; scoring after all universe contracts settle or on 2027-02-15, whichever is first. Unsettled contracts are reported as unresolved inventory, never marked. No early stop. |
- `BASE` §1 purpose, L22:
  > On untouched 2026 House races, test whether a fixed 50/50 blend of an admitted external specialist forecast (ElectIndex) and the Kalshi mid has lower paired Brier loss than the market mid alone. Hypothetical one-contract hold-to-settlement trades are also scored, under frozen fees and fills.
- `BASE` §7 caveat (3), L249:
  > - (3) Hypothetical P&L has almost no power: about 9 signals are expected (2024 rate 2/19), so it is reported descriptively.
- `BASE` §6 secondary, L218:
  > - capital-hours, drawdown, event concentration (top-1 and HHI; flag if > 50%);
- `BASE` §13 do-not-modify item 2, L322:
  > 2. No invented PnL.

## 3. Fee: what the P&L uses
- `BASE` §5 Fee regime (superseded for card01 by the fee-source chain below), L185:
  > - **Fee regime:** R1-P1 feebook @ `22371178cb2663250b4762f328069571c48cb551`. The fee is taken from the pinned feebook for `KXHOUSERACE`. The illustrative `0.07·p·(1−p)` from NH-001 is recorded as a sensitivity only. Net P&L stays null until the Archivist fee/account manifest lands (v1.2).
- `AMB` §(c), L113:
  > - **Until then:** the after-cost numbers are **BLOCKED**, not computed with the fallback. This covers the net P&L, the stress-row net and the signal set itself, because the fee enters the entry gate.
- `FEEFIX` §3 replacement item 1, L49:
  > > **1. SUB-CENT ROUNDING — HEADLINE (non-direct, buyer / taker-at-ask)** = `ceil_cent(P·C + fee_raw) − P·C`, with `fee_raw = M × 0.07 × C × P × (1−P)` and `ceil_cent(x) = ceil(x·100)/100`.
- `FEEFIX` §3, L61:
  > > **Promote / fee-honest claim:** use the **headline** (venue-faithful for non-direct buy). Do **not** invent `max(headline, FEE_ONLY)` as the admitted cost. Sensitivity rows may be reported alongside; they do not replace the headline for net P&L gates.
- `FEEFIX` §4 table (single-fill disclosure), L76:
  > | Per-fill + order accumulator + rebate | Headline is single-fill / one-shot. Multi-fill rebate path not modelled; card01 sims that assume one fill must disclose that. |
- `PREC` DR item (5) member type, L22:
  > - (5) Member type: the HEADLINE uses non-direct $0.01 round-up, the conservative choice and the same as the K1/K2 precedent. Direct-member $0.0001 is a sensitivity row. […]
- `V2` §2 (d), L12:
  > (d) series_status = PINNED for the series used, and the trade is inside applies_to (BUY / TAKER / NON_DIRECT / SINGLE_FILL / quadratic). Anything outside that stays BLOCKED_FEE_UNVERIFIED with no computation.
- `V2` §6 Effect, L29:
  > The card01 fee input is UNBLOCKED for the headline only. […]
- `R1ACC` §2, L12:
  > - Sensitivity views (FEE_ONLY_CEIL, DIRECT) are display-only with sensitivity_rows_attested=false, and are never used in net, gates, selection or concentration.
- `DISP` tightening of 69b98b2f §2, L12:
  > Tightening of 69b98b2f §2, adopted from r4 and Variants' default: the unattested sensitivity rows (FEE_ONLY_CEIL, DIRECT_MEMBER_GRID) are OMITTED from output until a later attested fill. Record sensitivity_rows_status = SENSITIVITY_BASIS_INCOMPLETE. This is stricter than display-only and softens no bar. T4's identity still holds for any view that is emitted.
- `OQ` OQ-10, L24:
  > 10. **REJECT (c)/(d) P&L basis:** PR-C owns it — hold-to-settlement net of the HEADLINE fee (corrected FU2). On mismatch PR-C governs and this module logs `REPORTING_DEFECT`.

## 4. Verdict scope and precedence
- `AMC` §C5 Pin (governs), L136:
  > - While the fee is BLOCKED, REJECT (c) and REJECT (d) are reported as **`BLOCKED_FEE_UNVERIFIED`**. They count neither as fired nor as cleared.
- `AMC` §C5 Pin (governs), L137:
  > - The verdict is then **`FORECAST_ONLY_FEE_BLOCKED`**, evaluated on REJECT (a)/(b) and PASS (i)/(ii) only:
- `AMC` §C5 Pin (governs), L138:
  > - `FORECAST_ONLY_FEE_BLOCKED: PASS-FORECAST` iff PASS (i) and PASS (ii) both hold (equivalently, neither REJECT (a) nor REJECT (b), per §C1);
- `AMC` §C5 Pin (governs), L139:
  > - `FORECAST_ONLY_FEE_BLOCKED: REJECT` iff REJECT (a) or REJECT (b) holds, with the firing item(s) named. A REJECT on (a)/(b) is final regardless of fee status.
- `AMC` §C5 Pin (governs), L140:
  > - Under `FORECAST_ONLY_FEE_BLOCKED`, **no after-cost, net, executable, tradeable, capacity-as-profit or KEEP claim is allowed** in any write-up, summary or index entry. Gross or hypothetical P&L figures, if shown, carry `BLOCKED_FEE_UNVERIFIED`.
- `AMC` §C5 Pin (governs), L141:
  > - "Fee BLOCKED" has the meaning already frozen in Amendment B §(c) and the Conductor ACCEPT: the Archivist fee/account manifest does not hold series-endpoint `fee_type`/`fee_multiplier` for `KXHOUSERACE` and every legacy series used, in an adopted entry. A draft or not-adopted entry (for example ADDENDUM_02, currently `DRAFT_NOT_ADOPTED`) is BLOCKED. Per Amendment B §(c), the entry must exist before any outcome; this amendment adds no new path to unblock (c)/(d).
- `AMC` §C4.3, L125:
  > - If the gate (with an admissible fee) selected zero signals, the row is emitted and anchored with status `NO_SIGNALS_SELECTED`, together with the anchored gate output showing zero. There is no P&L figure for the label to attach to.
- `ACCC` rulings 2 and 4, L2:
  > "rulings":{"1_AF7_entry_point":"CONFIRMED BLOCKER: Variants codes and pins a new outcome-free swing-stress entry point (no placeholder outcomes) plus AF-8 input-builder/entry-gate pins before 2026-11-02T22:00Z; Adversary verifies pre-snapshot","2_fee_timing":"Stricter rule stands: fee entry must exist before any outcome (B §(c)); otherwise FORECAST_ONLY_FEE_BLOCKED","3_AF10_part2":"NOT ADMITTED; series-list fee fields do not satisfy 'series endpoint' absent Examiner pin; fee stays BLOCKED","4_additions":"KEEP both: lapse clause (B stands if C not ACCEPTED) moot on this ACCEPT; NO_SIGNALS_SELECTED accepted as pre-declared status" […]
- `K3` (2) degenerate block, L8:
  > - (2) Degenerate headline block: RULED, a pre-outcome verdict addition in the N6 family (0b68c4bf). If the headline block has 0 races, or fewer than 2 distinct states, so that D_rc or its bootstrap CI is undefined, the verdict is INCONCLUSIVE_DEGENERATE_BLOCK. This is neither REJECT nor PASS, and it takes precedence over AF-1 REJECT(b). The precedence over NO_SIGNALS_SELECTED and the lapse clause stays as Amendment C states. Neither threshold changes and no bar softens. Adversary may object before the card01 code PR merges.
- `PREC` DR item (3), L25:
  > - (3) REJECT(c) with zero signals once fee is admitted: apply the frozen wording LITERALLY. P&L = 0, which is <= 0, so REJECT(c), with a NO_SIGNALS_SELECTED note attached. The profit leg cannot pass with no trades. This is not reinterpreted.
- `PREC` precedence, L26:
  > - Precedence as DR wrote it is ACCEPTED: validity > INCONCLUSIVE_DEGENERATE_BLOCK > REJECT(a)/(b) > fee branch (BLOCKED gives FORECAST_ONLY_FEE_BLOCKED; admitted gives REJECT(c)/(d), else PASS-FORECAST). Notes do not rank.
- `FU2` item 7, L10:
  > 7. REJECT(d) with zero signals: apply it literally, with the same NO_SIGNALS_SELECTED note as (c). The b8cb27e0 precedence order is unchanged and there is no new verdict class.
- `FU2` item 8, L11:
  > 8. PR-C (REJECT(c)/(d) P&L incl. one-tick-worse stress): GO, as a separate PR after PR69 merges. It must be pinned pre-outcome. Targets: draft by 10-22, merged by 10-26, so Adversary's pre-snapshot verify (due 10-28) covers it. Synthetic fixtures only; public rules apply.

## 4b. PR-C kit rulings (61c1e4ea; line 2 of the source is not quoted)
- `PRCR` ruling, L3:
  > 1. Stress tick $0.01: ACCEPTED.
- `PRCR` ruling, L4:
  > 2. Stress fee = headline recomputed at worse price: ACCEPTED.
- `PRCR` ruling, L5:
  > 3. Stress set = same trades, no re-gate/depth: ACCEPTED.
- `PRCR` ruling, L6:
  > 4. 2c buffer EXCLUDED everywhere incl. (d) (e5227270 / r3 govern; the NH-001 citation in (d) refers to the concentration test shape only). Log the citation wording as REPORTING_DEFECT; no validity change. A buffered row may appear only as labelled descriptive sensitivity, not as a verdict input.
- `PRCR` ruling, L7:
  > 5. Unsettled/void/conflicting at the 2027-02-15 stop => fail closed => FULL_VERDICT_REQUIRES_EXAMINER: ACCEPTED.
- `PRCR` ruling, L8:
  > 6. Scope: w=0.5 set only; (d) on at-ask nets; totals over all signals: ACCEPTED.
- `PRCR` ruling, L9:
  > 7. Admission: v2 ADMITTED_INDEX_ONLY only; v1 d4dc8e72 refused (715fbafd §5.3, R1 deny-list). This supersedes my earlier "v1 ATTEST_PASS or v2" wording.
- `PRCR` ruling, L10:
  > 8. Hand-off check = format + output hash + fee source, else Examiner: ACCEPTED.
- `PRCR` ruling, L11:
  > 9. OVERRIDE to YES: anchor the outcome-free entry-price + fee table (sha, recorded in a packet) BEFORE the snapshot/outcome join, same pattern as swing_stress. Cheap holdout-integrity guard.
- `PRCR` ruling, L12:
  > SCHEDULE: The order is confirmed: R1 first, then PR-C, one cloud at a time. PR-C draft due date MOVED from 10-22 to R1-merge + 3 days, hard cap 2026-10-31. No other dates move. No live orders; no GETs.

## 5. Bootstrap pin rule (applies only if resampling is used)
- `K2` Anomaly 1, L9:
  > - Anomaly 1, bootstrap draw order not pinned: the verdict is robust (every alternate CI includes 0). STANDING RULE from today: every new freeze must pin the bootstrap draw method and order (RNG, seed, resampling unit, draw sequence).

## 6. The 'NH-001 check' named by base §9 (d) (code lines, pins/NH001_recovered_2253c03c_core.py)
- `NH001` trade()/summarize(), L78:
  > def trade(q, bid, ask, outcome, extra_cost=0.02, reserve=0.03):
- `NH001` trade()/summarize(), L83:
  > for side,prob,price,payout in [('yes',q,ask,outcome),('no',1-q,1-bid,1-outcome)]:
- `NH001` trade()/summarize(), L84:
  > cost=price+fee(price)+extra_cost
- `NH001` trade()/summarize(), L87:
  > 'net':payout-cost})
- `NH001` trade()/summarize(), L88:
  > best=max(choices,key=lambda r:(r['expected_net'],r['side']=='yes'))
- `NH001` trade()/summarize(), L89:
  > return best if best['expected_net'] > reserve + 1e-12 else None
- `NH001` trade()/summarize(), L115:
  > net=sum(t['net'] for t in trades)
- `NH001` trade()/summarize(), L117:
  > best=sorted([t['net'] for t in trades if t['net']>0],reverse=True)[:2]
- `NH001` trade()/summarize(), L135:
  > 'excluding_best_two_winners_net':net-sum(best),

## 7. Interface expected by the R1 module (Conductor-ACCEPTED spec r3; PR-C governs the values)
- `R3` §3.8, L119:
  > **3.8 `event_concentration`** (event = race). Basis: per-signal **HEADLINE** net `net_i` (§4). `hhi = Σ_i (|net_i| / Σ_j|net_j|)²` (0–1; null if Σ|net| = 0 or no signals). `top1_positive_share = max(net_i > 0) / Σ(net_i > 0)` (null if no positive net). `top1_flag = (2·max_pos > Σpos)`. **`top1_positive_share` is VERDICT-BEARING** (REJECT (d)(i)); `hhi` DISPLAY-ONLY. Ownership — RESOLVED (OQ-10, ruling e5227270): "PR-C owns it — hold-to-settlement net of the HEADLINE fee (corrected FU2). On mismatch PR-C governs and this module logs `REPORTING_DEFECT`." REJECT (d)(ii) is PR-C's and only referenced here. […]
- `R3` §3.14, L134:
  > **3.14 Referenced, not re-specified.** D(0.5) raw CI → PASS (i)/REJECT (a) and D_rc(0.5) CI → PASS (ii)/REJECT (b): VERDICT-BEARING (PR69). w = 0.25 / 1.0 comparators, M1/M2 split, n_boundary_resamples, leave-one-state-out, swing stress/fragility: DISPLAY-ONLY (PR69). REJECT (c) taker P&L at ask, one-tick-worse and (d)(ii) drop-best-two: VERDICT-BEARING (PR-C).
- `R3` §4.3 view row, L155:
  > | `ONE_TICK_WORSE` | PR-C only | — | `PR_C_OUTPUT_ABSENT` if absent |
- `R3` §7 T10, L518:
  > | T10 | PR-C consistency | when `pr_c_output` is given: Σ net_HEADLINE and top1 equal PR-C; mismatch → `REPORTING_DEFECT` (kind `PNL_MISMATCH`), PR-C governs; absent → `PR_C_OUTPUT_ABSENT` |

---
Not quoted on purpose: universe rows, forecast values, race-level resolution text, private paths. Their sources stay pinned by sha above.
