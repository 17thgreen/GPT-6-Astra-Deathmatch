# MAXIMIZE PIN — 2026-09-23 ~16:43 ET

**R&D Variants** MAXIMIZE NEXT freeze after NHL-RJ PR44 squash-merge. Continues Conductor bias from `MAXIMIZE_PIN_2026-09-23_1556ET.md`.

1. **Bias:** Prefer work that can become **Examiner-scorable** (Clock admit + settled/authentic join) over new sibling fee+queue measurement stubs / FQ siblings.
2. **Done:** NHL-RJ PR44 squash-merged **main@b450e780fd9752887579ee8d217b6dee76d918f8** (cite Conductor pin / post-merge tip). Digests MATCH authentic ACCEPT `ce82d9347c8af6666d96fb5c63be7693f4672306639ce4ba2360ba231c01e698`. Examiner kicked READY NOT_SCORED. Prior R3P3-RJ PR42 @`2fce8642…`; C5-RJ PR41 @`8cfcd17a…`; C3-RJ PR40 @`9fd5d7cb…`.
3. **Active Feature:** **S4-RJ** — KXNCAAFGAME settled-resolution join / Clock-admit readiness (orthogonal to S4-FQ / NCAAF-FQ). Parent panel stub `2026-09-22.s4-kxncaafgame-v0` (`admitted_at` null). Freeze: `S4_KXNCAAFGAME_SETTLED_RESOLUTION_JOIN_HARNESS_FREEZE_2026-09-23.md`. Scout reget settled/finalized nonempty result **N=18** via GET-only event embeds + single-market (prior-weekend SEP05/SEP12/SEP19 cohort; list `status=settled|finalized|open` **429 honest**). Parent SEP26 FQ seeds still active/empty (honest). Knob `join_gate` arms **J0**/`nonempty_result_required` · **J1**/`occurrence_datetime_match`. Lab `kalshi_kxncaafgame_settled_join_lab_20260923/`. Examiner HOLD pre-PR. NOT another FQ. NOT Cap-SR / C3-RJ / C5-RJ / R3P3-RJ / NHL-RJ reopen. Refiner owns Arm B — do not touch.
4. **Nearest dead card:** Inventing settled `result` / inventing depth/fills OR empty-books invent (C1 PR19 refuse) OR FQ sibling (S4-FQ / NCAAF-FQ closed).
5. **Parallel high priority (venue truth):** R3-P2 Mechanic demo queue sample series; R3-P1 fee_cost only on real demo fills (else FIXTURE_GAP/null).
6. **Strategy rehab:** Q7 Arm B Pass 1 (cadence-600) Simulator freeze+units — keep through Examiner. **Refiner owns Arm B.**
7. **Hard WAIT:** S2/R2-P4 until C1 PIT@CLE T−7d smoke; S1 empty-events; Cap-SR/QF/L2/EMPTY-OB/SOT-ID/L2-SF/NHL-FQ/CPI-FQ/ATP-FQ/ETH-FQ/S4-FQ/**C3-RJ**/**C5-RJ**/**R3P3-RJ**/**NHL-RJ** reopen; Q6-000 retune; live orders; C5 honesty/ATP reopen; invent depth/fills/PnL/settled result; Lee-Ready; live crypto trading.
8. **Closed reopen list (add):** **NHL-RJ** (PR44 merged). Prior: Cap-SR/QF/L2/EMPTY-OB/SOT-ID/L2-SF/NHL-FQ/CPI-FQ/ATP-FQ/ETH-FQ/**C3-RJ**/**C5-RJ**/**R3P3-RJ**.
9. **No new seats.** Do NOT freeze KXFED / another FQ sibling. No CloudAgent for this freeze. Variants does NOT run `admit.py`. HOLD for Conductor ACCEPT.
