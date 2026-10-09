# CONDUCTOR RULING — disposition of Examiner R1 r4 addendum
Issued: 2026-10-08T23:39Z (19:39 ET). Seat: Conductor "KALSHI".

r4 addendum (md 61fbb3fc9db0965777720f2937a6ec738fe68bd8dc5be497df1e0227c93989c1, json d55e877ea4db0f102b8a9dcf0493a24f168c93764097dc2452498a45ce1725dc) is SUPERSEDED by ACCEPT 69b98b2f643a7510280cd6b959c30e285df081c8142b910808001db8cad5b81a. r4 is not binding, and its "wins on conflict" clause has no force. Governing pair: r3 c5b08459 + ACCEPT 69b98b2f + this ruling.

Folded in from r4 (tests only, ADDED; T19 is KEPT, not replaced):
- T20 ADMITTED_INDEX_ONLY happy path
- T21a–d each of amendment 2c870cd5 checks (a)–(d) failing alone gives BLOCKED_FEE_UNVERIFIED
- T22 fee_multiplier ≠ 1 gives BLOCKED (HEADLINE_SCOPE_MISMATCH)
- T23 retired values (PENDING_ADOPTION_RULE_AMENDMENT, FEE_ATTESTATION_MISSING) never emitted

Tightening of 69b98b2f §2, adopted from r4 and Variants' default: the unattested sensitivity rows (FEE_ONLY_CEIL, DIRECT_MEMBER_GRID) are OMITTED from output until a later attested fill. Record sensitivity_rows_status = SENSITIVITY_BASIS_INCOMPLETE. This is stricter than display-only and softens no bar. T4's identity still holds for any view that is emitted.

NOT folded in: r4's "R-OQ-2 open". It is ruled in 69b98b2f §4 as NO_TWO_SIDED_BOOK_IN_WINDOW.

Also accepted: Variants' default for PR69 FU2. The fee scope stays as it is, so the fee result is BLOCKED_FEE_UNVERIFIED and PR69 merges forecast-only. The v2 gate lands in the R1 PR from post-PR69 main.

Nits on amendment 2c870cd5, logged as REPORTING_DEFECT with no change to validity:
- The header time 23:40Z should read the mtime 23:33:51Z.
- §2(c): any other in-file value fails via (a) (sha), with the same BLOCKED outcome.
- §5 "CANONICAL" reads "adopted per 715fbafd row 75 'prefer docs path'".
