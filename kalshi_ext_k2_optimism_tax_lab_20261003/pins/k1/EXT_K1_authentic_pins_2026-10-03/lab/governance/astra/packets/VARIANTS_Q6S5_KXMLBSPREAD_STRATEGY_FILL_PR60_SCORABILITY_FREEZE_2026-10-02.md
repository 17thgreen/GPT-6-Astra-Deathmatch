# Q6S5 KXMLBSPREAD STRATEGY-FILL PR60 SCORABILITY — FREEZE KERNEL (no new knob: settled-join + tape-to-quote, Sep-25 only)

**File date:** `2026-10-02` (UTC date, same as the Simulator READY `973692b0…`). **Frozen / declared at:** `2026-10-01T23:51:21-04:00` (ET). Every rule below, including each UNPINNED resolution, is stated here **before** any implementation. No quote, fill, PnL or ROI has been computed by Variants for this packet.
**Owner:** R&D Variants (freeze; implement only after Conductor ACCEPT) → Simulator → Examiner
**Status:** FROZEN — FREEZE_ONLY. Awaiting Conductor **ACCEPT + IMPLEMENT GO**. No cloud agent, no PR, no push, no live Kalshi HTTP, no orders, no `admit.py`. This packet writes files on the box only.
**Parent chain:** `Q6S5-KXMLBSPREAD-STRATEGY-FILL` (PR60 freeze `9f50ba19…`, ACCEPT `c6f95b32…` + companion `a5398129…`, merged as PR60 squash `12e760f5…`) ← `Q6S5-KXMLBSPREAD-FEEQUEUE-HARNESS` (freeze `4f65dcdf…`).
**Freeze ID / experiment id:** `Q6S5-KXMLBSPREAD-STRATEGY-FILL-PR60-SCORABILITY`
**Feature family:** `strategy_fill_pnl_path` (**unchanged**). **Knob:** `fill_model` (**unchanged**), implemented value `public_trade_through_conservative` only; `mechanic_demo_observed` stays null / UNAVAILABLE. **Zero new knobs, zero new parameters.** This freeze adds plumbing only: (a) a settled-join, (b) a tape-to-quote builder plus the 9f50ba19 fill engine that PR60 never implemented.
**Repo:** `https://github.com/17thgreen/GPT-6-Astra-Deathmatch`, main `f233079d9e7d2a91e2100f2085bcf85d0006e28f` (PR63 squash). Cloned fresh to `/workspace/pr60s_main`, read-only. PR60 squash `12e760f5bd3b622d8f0d70a74c28655464e2b93c` is present in that clone; PR60 lab tree `78fca23c47fd8475771bec39bddc516efd92b06d` is identical at `12e760f5` and `f233079d`; runner `orchestrator.py` sha256 `296cfe64…` = git blob `2f4ca4e3…`.
**Proposed lab dir:** `kalshi_q6s5_kxmlbspread_strategy_fill_scorability_lab_20261002/`. Not created. Created at implement, after ACCEPT, by the **single** cloud.
**Amendment role:** freeze `9f50ba19…` line 49 (rule 6) and line 91 admit Sep-25 settlements only if a Collector settled re-GET is "pinned by amendment before the run". **This freeze is that amendment.** It pins the Collector settlement-only folder (`0dd61920…`) and the Simulator join manifest (`73af8822…`).

**Disclosure (what Variants read before freezing):** the Simulator READY `973692b0…` and the Examiner ACK `1f72dd05…`, which both list the per-ticker settlement mapping. So the labels are known to the author: **1 YES / 5 NO**. I also read guard fields of the 6 settlement GETs (`status`, `close_time`, `settlement_ts`, `expiration_time`, request/response times). From the book bytes I read side presence, crossed/locked checks, content-change flags, and the top-of-book snippets printed during sha checks. From the Sep-25 tape I read only structural fields: `created_time` ranges, `is_block_trade`, native taker-field agreement, and yes+no consistency counts. I did **not** compare any quote to any print, and I computed **no** fill, PnL or ROI. Where labels could matter, the protection is the lookahead declaration below: the strategy is symmetric (both sides are quoted at every placement, so no rule can pick a side), every rule is either frozen in `9f50ba19…` (2026-09-29 16:52 ET, before the settlements were fetched on 2026-10-01 23:29 ET) or resolved here by a label-blind criterion, and a label-permutation unit test is required.

## Commission (Conductor, relayed; verbatim intent)

"MAXIMIZE NEXT: PR60 scorability." The commission was relayed to Variants by the parent agent. No Conductor commission packet is on disk; the Examiner ACK `1f72dd05…` records the same relayed do-not-score instruction. Requirements and where each is met:

| # | Requirement | Where met |
|---|---|---|
| (a) | Settled-join reading `settlement_value_dollars` from the Collector folder `0dd61920…`, post-close only | §Settled-join (S1–S9) |
| (b) | Tape-to-quote builder from SOURCE_PINS `1846a971…`, using only 9f50ba19 / 4f65dcdf rules; zero new knobs or parameters; each unpinned rule resolved conservatively and stated before implementation | §Rules R01–R30; UNPINNED list |
| (c) | Lookahead declaration; label-permutation test (PnL changes, quotes and fills byte-identical) | §Lookahead declaration; tests T1–T4 |
| (d) | Verdict cap ITERATE; no KEEP; simulated fills never count toward KEEP (v1.2) | §Verdict mapping |
| (e) | A0 and A1 verbatim from PR60 | §PR60 as merged |
| — | Universe Sep-25 KXMLBSPREAD only; Sep-24 KXMLBSPREAD and the KXHIGH snapshot CLOSED; one cloud from f233079d after ACCEPT | §Universe; §Cloud instructions |

## Pins (all re-hashed on box 2026-10-01 23:41–23:50 ET; the box was restored ~23:12 ET, every pin below matched)

| Item | Path | sha256 | Verify |
|---|---|---|---|
| **PR60 freeze** | `packets/Q6S5_KXMLBSPREAD_STRATEGY_FILL_FREEZE_2026-09-25.md` (identical copy in `packets/Q6S5_KXMLBSPREAD_STRATEGY_FILL/` and vendored in the PR60 lab) | `9f50ba19694083c774bbe2a6cff491d1a2f81ed3a6f9cc21a3641a938c84955d` | MATCH ×3 |
| **Parent freeze** | `packets/Q6S5_KXMLBSPREAD_FEEQUEUE_HARNESS_FREEZE_2026-09-25.md` (identical copy in `packets/Q6S5_KXMLBSPREAD_FEEQUEUE_HARNESS/`) | `4f65dcdf536755b9f7dc2449c2dcd90b2df74cdf99a441b676f1a71c4d709c6e` | MATCH ×2 |
| **PR60 ACCEPT (implementation)** | `packets/CONDUCTOR_ACCEPT_VARIANTS_Q6S5_STRATEGY_FILL_FREEZE_2026-09-29.json` | `c6f95b32a9224a6beede1a8c0e3d7f0a5a4530cc8b3d0b9d997995f65d64f8f3` | MATCH |
| PR60 ACCEPT (companion rulings) | `packets/CONDUCTOR_ACCEPT_Q6S5_KXMLBSPREAD_STRATEGY_FILL_FREEZE_2026-09-29.json` | `a5398129aa45c5dee5fdd15656a252bb6c460d00e4f5b06360ce522de0f968b4` | MATCH |
| PR60 dual-ACCEPT reconcile | `packets/CONDUCTOR_RECONCILE_Q6S5_STRATEGY_FILL_DUAL_ACCEPT_SOLE_CLOUD_2026-09-29.json` | `0f33a94c970eec6a9863041396071c78ce64b58abc8a7ab91f48062fbfc052b0` | MATCH |
| **PR60 MERGE** | `packets/CONDUCTOR_MERGE_Q6S5_KXMLBSPREAD_STRATEGY_FILL_PR60_2026-09-29.json` | `3486a2fe71da0be40a3cb6202abcc30e1783515180e20f594b3c25b034414bef` | MATCH (merge `12e760f5…`, squash, 2026-09-29 17:18 ET) |
| PR60 FROZEN_EXPERIMENT / kick | `packets/Q6S5_KXMLBSPREAD_STRATEGY_FILL/FROZEN_EXPERIMENT.json` / `packets/CONDUCTOR_KICK_VARIANTS_Q6S5_STRATEGY_FILL_FREEZE_2026-09-25.json` | `7383b4836a378b1da8afe889d82a13997b9b3a4584bdc454ae1c67785eab5fff` / `dc19794bdb8e26c3a3f4fe86eadc9bec1b02db97d508fca9426e3c3eddfb6bc8` | MATCH |
| **Simulator READY (settled, NOT_SCORABLE)** | `packets/SIMULATOR_READY_Q6S5_KXMLBSPREAD_STRATEGY_FILL_PR60_SETTLED_2026-10-02.json` | `973692b0c83e8068f4623d7e47168f40c5cd8d3da85c7a66dac86710259c40b0` | MATCH (prefix `973692b0` confirmed) |
| Examiner ACK NOT_SCORABLE | `packets/EXAMINER_ACK_Q6S5_KXMLBSPREAD_STRATEGY_FILL_PR60_SETTLED_NOT_SCORABLE_2026-10-01.json` | `1f72dd05536070a7aeac3c4b7311f781e47d955c05952a51689d1a1071e05e43` | pinned (context) |
| Examiner READY_NOT_SCORED PR60 | `packets/EXAMINER_READY_NOT_SCORED_Q6S5_KXMLBSPREAD_STRATEGY_FILL_PR60_2026-09-25.json` | `85cdd05c3333da3eb373212d1bb4647729f6586185d518288df417e8de963698` | MATCH |
| **Collector settlement READY** | `lab/astra-capture/q6s5-kxmlbspread/settlement_only_2026-10-02/COLLECTOR_READY_SETTLEMENT_ONLY.json` | `0dd61920f8e622c336cf9ab2ac88d0d78b04d4152c93cf98cecb14550b7d924c` | MATCH |
| Settlement DIGESTS.txt | `…/settlement_only_2026-10-02/DIGESTS.txt` | `5905c137089d42ae07c53720762b9dcc9c8b0ad9c4f17ebe51340d18198a1044` | MATCH; `sha256sum -c` 8/8 OK |
| **Settlement folder digest** | sha256 of the sorted `sha256sum` listing of all 10 files in `settlement_only_2026-10-02/` (listing in `Q6S5_PR60_SCORABILITY/SOURCE_PINS.json`) | `65cfe9e4855038263853b236df8eb4852d85d789546215a59f350c6a91feed03` | computed |
| **Join manifest** | `lab/astra-science/kalshi_q6s5_kxmlbspread_strategy_fill_settled_run_20261002/outputs/SETTLEMENT_JOIN_MANIFEST_SEP25.json` | `73af8822508ce95f5a6765ba0dd3949b58e0cbc8df8cce8301b313337a722e17` | MATCH |
| Simulator run DIGESTS.txt | `lab/astra-science/kalshi_q6s5_kxmlbspread_strategy_fill_settled_run_20261002/DIGESTS.txt` | `4e670303d576678fce40568f45d60059ca6078e0001e697129de7a04750ee530` | MATCH; `sha256sum -c` 14/14 OK |
| **SOURCE_PINS (tape)** | `packets/Q6S5_KXMLBSPREAD_STRATEGY_FILL/SOURCE_PINS.json` (= PR60-vendored copy) | `1846a9710375dd418983e1a03e05ac15386138ada7c405923b7fd0514cf116a1` | MATCH; **inputs_core 9/9 + inputs_raw 87/87 re-hash PASS** |
| Panel admitted / panel stub | `lab/astra-capture/q6s5-kxmlbspread/panel_admitted.json` / `panel_stub.json` | `e36de2d1ce6286dff90d25f2fae680170c8a469c443c1beed974ffe80383fba1` / `c7f1f1f4ca263838c4600ed46db8f525b68efc5399a567bd60929d18d76803cc` | MATCH (same 12 tickers; both contain all 6 Sep-25 tickers) |
| FEE_PIN | `packets/EXAMINER_FEE_PIN_Q6S5_KXMLBSPREAD_LIVE_SERIES_2026-09-25.json` | `9c0f3554eedc582ed4bed940575bf7ee6c0540ce5134140c5ea19e7c458d2b6a` | MATCH |
| ADMIT-1 ruling / gap record | `packets/CONDUCTOR_RULING_ADMIT1_OUTAGE_GAP_WEATHER_CARD03_RELAUNCH_2026-09-29.json` / `lab/astra-capture/prospective/ADMIT1_OUTAGE_GAP_2026-09-27_to_2026-09-29.json` | `ac7cfe63623ca342ab5b4285ff58382a8138b58fb6cd8e95310a5d30d90304f2` / `4f2a5e2693f809e592238c0bf58ecac93f982fb8809c98ca81e51a41d8a65198` | MATCH |
| **v1.2 rule on simulated fills** | `templates/EXAMINER_KALSHI_SCORECARD_TEMPLATE_v1.2.json` (`simulated_fills` block lines 446–463; rule line 777) / `.md` (Section F line 85; rule line 171) | `56bcf6269a42031d9d90496e9a65c2292321aed2165033f6fb44ff8cc4d6b1cc` / `ad1dd2834652b8e9be331ddf2f3ec900ea587efb042251fde6452532b2e36394` | MATCH |
| IN_SAMPLE_DEV ruling (precedent) | `packets/CONDUCTOR_RULING_Q6S5_FL_BAND_IN_SAMPLE_DEV_LABEL_2026-10-01.json` | `09763030c67df066f2b59346200813e181777670cd46fcee6b8877a6dd74d754` | MATCH |
| Holdout prereg addendum + ACCEPT | `packets/VARIANTS_HOLDOUT_PREREG_ADDENDUM_Q6S5_KXMLBSPREAD_UNTOUCHED_CAPTURE_2026-10-01.md` / `packets/CONDUCTOR_ACCEPT_VARIANTS_HOLDOUT_PREREG_ADDENDUM_…_2026-10-01.json` | `370dc31df17191446013b6cebb52d44ee8346f47d2f5b543a1c73049ba52c063` / `9a987a77e6cd6293ddaeb14fadbf33a25c1a6cc392af25f46eaaaaae33ebb273` | MATCH (untouched by this freeze) |
| House-style freezes | `packets/Q6S5_KXMLBSPREAD_GAME_PHASE_SETTLED_TAPE_FREEZE_2026-10-01.md` / `packets/WX_FL_KXHIGH_SETTLED_TAPE_FREEZE_2026-10-01.md` | `5beba803f3f6d33410409acc23ad3b782be62dc8829a0f54584e1da8ac18575a` / `aec5b760f8539ea9f30aa1c3601534dccf78a62ee2026cb939842656e3c20e0f` | MATCH |
| RULE-FROZEN-EDIT-PREV-BYTES-001 | `registry/RULE_FROZEN_EDIT_PREV_BYTES_2026-09-24.md` | `f0aab7d15ca78a097644008db02013eae3a56cb81b2a6aef2cfe6faf21e3e6d1` | pinned |
| p16 source | `research/KALSHI_EDGE_RESEARCH_2026-09-24.pdf` | `7e55bc260526aa5088ee31f74475851219ab2cd7f19fdd2f0dd5e9f998c8b45e` | pinned |

**Code pins at main `f233079d` (sha256 / git blob):**

| File | sha256 | blob |
|---|---|---|
| `kalshi_q6s5_kxmlbspread_strategy_fill_lab_20260925/orchestrator.py` (PR60 runner) | `296cfe64ff24c2fad0437ce9a9ec11458f557ee94ee900bd621160dc283fa597` | `2f4ca4e3d5521e0057c969532618a760f63b0bba` |
| `kalshi_q6s5_kxmlbspread_strategy_fill_lab_20260925/tests/test_orchestrator.py` | `0877f7d142ea04ee568a81bf878d8b13ebab88076b75d59aa254bdd04ae970b3` | `21ab27c77bedca3b544d0dad74135b4884123e34` |
| `kalshi_q6s5_kxmlbspread_strategy_fill_lab_20260925/EXPERIMENT_SPEC.md` | `33806f416c7c21acebbd0b32e632ded7567d5bccb48f2af5f8c2c57270a4517a` | `a7e2a75bd32029143059e9181720d2ad11485526` |
| `kalshi_q6s5_kxmlbspread_feequue_lab_20260925/orchestrator.py` (parent; `settled_join`, `classify_native_taker`) | `e224686a1bbe4173f00e62c3d2cba78a3c48eecef45ed77c678564def9d5bbfc` | `d4223e05904fa847e5a6849d130137291365619f` |
| `kalshi_feebook_lab_20260922/feebook.py` / `series_fee_table.stub.json` (unchanged vs `22371178…`) | `eaf5aac7126efcd574c972fa77438c4118d44d50acafa17c504bdd48768bebe7` / `600d56beda64c2edd9af2c9d220398ff1a7158dba140603a42f7cb7f95212384` | `f6438083…` / `21ab882d…` |
| `kalshi_rails_lab_20260922/rails.py` (unchanged vs `6a28e0d6…`) | `834386506dd72210d77ee063d4a96248d76ce09a4be6ce771b9609337d3388e1` | `ade53ec9e09da5de9573e9362bb1e3e72bded4c4` |
| `kalshi_r2p1_hygiene_000_lab_20260922/hygiene.py` | `65310a88ec7602a3fa2e50f2444e64c431dd29ef648992cb7861a5b74ca3b69f` | `bef10e81b10dc3b6112c1d85a4b34806f58c8814` |
| `kalshi_q6s5_kxmlbspread_game_phase_settled_tape_lab_20261001/orchestrator.py` (PR62; CACHE fee precedent) | `c6c4c0a13be65e51250c011cca58c22a000e0d2cc65163520a3ad719a1646521` | `9cd5cfad7493ae281b6b64f51f8598be99c94610` |

## PR60 as merged (documented from main f233079d; commission (e) and step 2)

**A0 / A1, verbatim.** PR60 freeze `9f50ba19…` arms table (lines 100–101):

| **Q6S5A0** | `maker_vs_taker_native` | Splits the fill/PnL series into maker legs vs taker legs; produces `maker_vs_taker_roi_delta` |
| **Q6S5A1** | `content_fresh_vs_stale_bin` | Splits placements by rails `content_fresh_flag` at the placement snapshot; produces `fresh_vs_stale_gap` |

PR60 freeze line 93 (arm metrics):

- **Arm metrics:** `maker_vs_taker_roi_delta` = ROI(maker legs) − ROI(taker legs), where ROI = Σpnl / Σ(fill_price + fee) over resolved filled contracts. `fresh_vs_stale_gap` = ROI(content_fresh placements) − ROI(stale placements), using the rails `content_fresh_flag` at the placement snapshot.

PR60 runner `orchestrator.py` lines 31–34:

```python
ARMS = {
    Q6S5A0: 'maker_vs_taker_native',
    Q6S5A1: 'content_fresh_vs_stale_bin',
}
```

Parent freeze `4f65dcdf…` arms (lines 47–48), carried by PR60:

| **Q6S5A0** | Native taker | Partition on native `taker_*` fields only; Lee-Ready **REFUSED** |
| **Q6S5A1** | Freshness bin | Rails `content_fresh_flag` / queue-attribution bins; no fee invent; no invent fills |

**Classifier input schema (PR60 `public_trade_through_conservative`, lines 409–446; called by `classify_fill`, lines 449–489).** A caller-built `dict` with required keys `quote_ts` (UTC `…Z` string), `trade_ts` (UTC `…Z` string), `resting_side` ∈ {`bid`, `ask`}, `resting_price` (decimal string or int in [0,1]; floats refused), `trade_yes_price` (same), `ticker` (must start `KXMLBSPREAD-` and be in panel stub `c7f1f1f4…`; else `InventedMarketRefused`). A missing key returns `status=INCOMPLETE_NOT_INVENTED`. All rows pass `_guard_row` (lines 335–365): Lee-Ready keys refused; any non-null `fill`/`fills`/`contracts`/`pnl`/`roi`/`simulated_fill` refused; any `*_ts` inside the ADMIT-1 window → `Admit1WindowRejected`; any non-null `LOOKAHEAD_KEYS` → `LookaheadRefused`; `KXMLBGAME` refused.

**Fill rules as implemented.** PR60 implements the strict-through **observation only**: `_through` (lines 395–406). Bid is through iff print < resting price, ask iff print > resting price, and equality is `TOUCH_NOT_THROUGH`. It also raises `LookaheadRefused` if `trade_ts ≤ quote_ts` (lines 419–423). It returns `contracts`/`simulated_fill`/`pnl`/`roi` = null always ("A through flag is not a fill and not PnL"). The 9f50ba19 queue-depletion fill rule (lines 82–86), the strategy (lines 73–77) and the PnL arithmetic (lines 90–93) were **frozen but never implemented**. There is no tape loader and no quote builder.

**Fee model.** `fee_output()` (lines 217–235) returns label `CACHE_NOT_R1P1`, `fee_type=quadratic`, `multiplier=0.5`, `formula_id=None`, `fee_dollars=None`; `claim_live_r1p1` always raises. Freeze line 92: - **Fee:** `feebook.order_fee(role, 1, price)` @ `22371178…`, using **only** the FEE_PIN-observed series terms `fee_type=quadratic`, `fee_multiplier=0.5`. The maker role resolves through `feebook.resolve_terms`, and this freeze does not assert its value. Label **CACHE_NOT_R1P1** (see Fee).

**Where settlement refuses.** (1) PR60 `LOOKAHEAD_KEYS` (lines 64–70) includes `settlement_ts`, so `classify_fill` on any row carrying it raises `LookaheadRefused` (Simulator probe confirmed). A row with only `settlement_value_dollars` is ignored (`INCOMPLETE_NOT_INVENTED`). (2) Parent `settled_join(panel)` (feequeue orchestrator lines 594–600) returns `None` by design ("No settlement join is published"). (3) PR60 has no settlement argument, config or loader. **This freeze does not change any of that.** The new join lives in the new lab, runs strictly after fills are frozen, and never passes a settlement field into `classify_fill`.

## Universe (Sep-25 only; 6 markets / 3 games)

| Game (event_ticker) | Markets | Sep-25 dated books in SOURCE_PINS | Sep-25 prints in pinned tape |
|---|---|---|---|
| `KXMLBSPREAD-26SEP251840PITDET` | `KXMLBSPREAD-26SEP251840PITDET-DET2`, `KXMLBSPREAD-26SEP251840PITDET-PIT2` | 3 + 2 | 1 + 4 |
| `KXMLBSPREAD-26SEP251840TBPHI` | `KXMLBSPREAD-26SEP251840TBPHI-PHI2`, `KXMLBSPREAD-26SEP251840TBPHI-TB2` | 3 + 3 | 10 + 0 |
| `KXMLBSPREAD-26SEP251845NYMWSH` | `KXMLBSPREAD-26SEP251845NYMWSH-NYM2`, `KXMLBSPREAD-26SEP251845NYMWSH-WSH2` | 3 + 1 | 5 + 1 |

Source of the ticker list: Collector settlement folder `0dd61920…` (6 raw GETs), join manifest `73af8822…` (6 rows, `all_sep25_in_panel_no_sep24=true`), panel `e36de2d1…` / `c7f1f1f4…`. All are 1.5-run spread markets (`floor_strike=1.5`, `strike_type=greater`). **Outcomes:** 1 YES / 5 NO in aggregate. Per-ticker outcomes are in the pinned files only and are not restated here.
**CLOSED (refused by the runner):** every Sep-24 KXMLBSPREAD ticker (HOUATH, LAASEA, SDLAD; family_size 4, MAXIMIZE `2053ET` `closed_universes`) and the WX-FL KXHIGH snapshot. A Sep-24 ticker passed to the builder, engine or join raises `ClosedUniverseRefused`.

## ADMIT-1 window (carried verbatim from 9f50ba19) and settlement admissibility

1. **Enforced exclusion window:** `[2026-09-27T00:00:00Z, 2026-09-30T04:00:00Z)`. This is a calendar superset of the ruling's exact gap and covers all of Sep 27–29 in both UTC and ET. Any **capture, book, trade, market-status or settlement record** whose timestamp falls in this window is **excluded**. That covers book `captured_utc`/filename stamp, trade `created_time`, market GET `captured_utc`, and the settlement GET `captured_utc` plus `settlement_ts`/determination time. The narrower ruling window is recorded as `ruling_gap_utc` for reference. This packet-local over-exclusion does not change the ruling's "post-relaunch capture scorable as normal" for ADMIT-1 itself.

6. **Future settled re-GET** (Collector-owned, public GET-only, not Variants) is admissible only if its `captured_utc` is outside the window and it is pinned by amendment before the run.

Application here: the Sep-25 books are `2026-09-25T04:48:31Z..05:34:06Z`, the Sep-25 prints `2026-09-25T00:43:58Z..05:55:24Z`, and the trades request `ts_utc` values `06:00:51Z..06:03:02Z`. Settlement GET responses were `2026-10-02T03:29:21Z..03:31:56Z` (2026-10-01 23:29–23:31 ET) and `settlement_ts` values `2026-09-26T01:17:56Z..02:02:46Z`. **All are outside the window. Expected `excluded_admit1_window_n = 0`;** any non-zero count must be reported. `capture.sqlite` is refused and never opened. Companion ACCEPT `a5398129…` ruled that "settlement data is post-gap public state, not in-window capture", and this freeze pins the re-GET (rule 6 satisfied).

## Rules: tape → quote → fill (every rule needed; frozen source or UNPINNED + resolution)

Conservative criterion used for every UNPINNED resolution, fixed before implementation: choose the reading that gives **fewer or worse fills**, assumes the **worst queue position**, never uses a print **at or after** the quote's own timestamp, never invents a value, and **introduces no number** that is not already frozen. If a rule could not be resolved without a new number it would be a BLOCKER. None was.

| # | Rule | Source (frozen) / resolution |
|---|---|---|
| R01 | Universe = the 6 Sep-25 tickers above | 9f50ba19 L73 (12 panel_admitted) ∩ Conductor commission "Sep-25 only". PR60 L431–432 requires panel membership (all 6 present). |
| R02 | Closed input manifest; sha-check before read; fail-closed | 9f50ba19 L45: 2. **Closed input manifest:** the runner may read only the sha-pinned inputs in `SOURCE_PINS.json` and must check each sha256 before reading. A mismatch is a hard fail. Nothing is filled in to cover a gap. |
| R03 | Placement instants = each dated measured orderbook snapshot of a universe ticker; undated "latest" copies ignored | 9f50ba19 L74 |
| R04 | `captured_utc` of a snapshot | **UNPINNED** → the filename stamp `YYYYMMDDTHHMMSSZ` (e.g. `20260925T044831Z`). The book body holds only `orderbook_fp`. `measured/requests.jsonl` is not in SOURCE_PINS. This is the only pinned capture time, and no sub-second precision is invented. |
| R05 | Status gate: place only if the latest dated market GET for that ticker with stamp ≤ `captured_utc` shows `status=="active"`; no such GET ⇒ no placement | 9f50ba19 L74 ("only if"). Expected: 15/15 eligible. |
| R06 | Maker price = best displayed bid of that side = **max** price level in `orderbook_fp.yes_dollars` / `no_dollars` | 9f50ba19 L75. Implemented as max, not as "last element", so no ordering of the arrays is assumed. |
| R07 | `queue_ahead` = displayed size at that price, Decimal as-is | 9f50ba19 L75 + L84 |
| R08 | Side with no displayed bid | **UNPINNED** → no maker order on that side (nothing to join; not invented). Expected 0 occurrences. |
| R09 | Crossed or locked snapshot (best yes bid + best no bid ≥ 1) | **UNPINNED** → no placement for either leg at that snapshot, counted. A post-only bid would be rejected, and the derived ask would sit at or through our own bid. Expected 0 occurrences. |
| R10 | Size = 1 contract per leg per side | 9f50ba19 L75, L76; p16 item 6 |
| R11 | Cancel/replace at the next dated snapshot of the same ticker; the replacement joins the **back** with a fresh `queue_ahead` (no priority carried) | 9f50ba19 L75. **Resolution (UNPINNED detail):** the next dated snapshot is the cancel time even if that snapshot were ineligible (earliest cancel). |
| R12 | Last order rests until the earliest of (a later pinned GET showing status ≠ active, tape end) | 9f50ba19 L75. **UNPINNED detail:** tape end = the **earliest** `ts_utc` among all rows for that ticker in `trades_fills_2026-09-25/requests.jsonl`, any status. Only WSH2 has two rows (429 at `06:02:31Z`, 200 at `06:03:02Z`) → `06:02:31Z`. Shorter rest ⇒ fewer or equal fills. Rest end uses only SOURCE_PINS GETs; the settlement folder is never read by the builder or the engine. |
| R13 | Print window for an order placed at `t0`: `created_time > t0` and `created_time <` cancel time | 9f50ba19 L82. **UNPINNED precision:** `t0` is a whole-second stamp, so a print qualifies only if `created_time` truncated to whole seconds is **strictly greater** than the `t0` stamp. Prints in the stamped second itself are excluded, because the book may already reflect them. The upper bounds (cancel, tape end) are strict at full precision. A print at exactly the next snapshot stamp belongs to neither order. |
| R14 | Our-side prints: YES bid ← native `taker_side=="no"`; NO bid ← `taker_side=="yes"`. Native fields must agree (parent `classify_native_taker`, feequeue orchestrator L781–837); disagreement ⇒ row excluded and counted. Lee-Ready REFUSED. | 9f50ba19 L83 + L81 ("symmetrically"). Expected native conflicts in the Sep-25 tape: 0. |
| R15 | Block trades (`is_block_trade=true`) | **UNPINNED** → excluded from both queue depletion and the fill trigger, counted. They are negotiated off-book and cannot execute against or deplete a resting book order, so excluding them can only reduce fills. Expected 0 (0 block rows in the Sep-25 tape). |
| R16 | Price consistency | **UNPINNED** → rows with `yes_price_dollars + no_price_dollars ≠ 1` (exact Decimal; **no tolerance number**) are excluded and counted. This is needed because the PR60 classifier works in the YES frame while 9f50ba19 states the NO rule in `no_price_dollars`. Expected 0. |
| R17 | Queue depletion and fill trigger | 9f50ba19 L84–L85 verbatim: 3. **Conservative queue depletion:** `cum` = sum of `count_fp` over our-side prints with `yes_price_dollars ≤ p` since `t0`. No credit is given for cancels or modifies ahead of us. Displayed fractional sizes are used as-is. / 4. **Fill:** at the **first** our-side print with `yes_price_dollars < p` (strictly through) at which `cum` (including that print) is ≥ `queue_ahead + 1`. Fill quantity = 1, fill price = **p** (our limit, not the through price), fill time = that print's `created_time`. NO bid at `q`: the same with `no_price_dollars` (L81). |
| R18 | Through flag comes from PR60 `classify_fill` | PR60 L395–446. YES bid `p` → `resting_side='bid'`, `resting_price=p`; NO bid `q` → `resting_side='ask'`, `resting_price=1−q` (YES frame); `trade_yes_price` = print `yes_price_dollars`; `quote_ts`=`t0` stamp, `trade_ts`=print `created_time`. The engine asserts that PR60's `through` equals its own `no_price` comparison; any disagreement is a hard fail. No settlement field is ever in these rows. |
| R19 | Labels on every modeled fill row | 9f50ba19 L86: 5. **Labels on every modeled fill row:** `fill_source="MODEL:public_trade_through_conservative"`, `observed=false`, `tag="replay"`. **Stated assumptions:** price-time priority holds; our order joins at the back; no hidden liquidity or latency advantage; the public tape is complete for our window (429 gaps and empty tickers such as `TBPHI-TB2` count as no prints and are never imputed). Taker rows carry `fill_source="MODEL:displayed_touch"`, `observed=false`, `tag="replay"`. |
| R20 | Taker leg | 9f50ba19 L76: - **Taker legs (per placement × side):** buy 1 contract at the **displayed best ask** for that side (= 1 − best opposite bid), at `captured_utc`. This needs a displayed opposite-bid size ≥ 1. If there is no displayed opposite bid, there is no taker fill (null, not invented). **UNPINNED detail:** "displayed opposite-bid size" = the size at the **best** opposite level only (no aggregation, no book walk). |
| R21 | Taker vs our own maker order at the same snapshot | **UNPINNED** → the taker executes first against pre-existing displayed size, and the maker order then joins the back. `queue_ahead` is **not** reduced by our own taker contract (no credit), and a self-match is impossible by this ordering. |
| R22 | Hold to settlement; inventory | 9f50ba19 L77. No inventory cap is frozen, and none is added (a cap would be a new number). The bound is structural: at most 1 maker + 1 taker contract per (ticker, side, placement). |
| R23 | Fee per filled contract | 9f50ba19 L92 + L107. **Mechanism UNPINNED in 9f50ba19 → resolved by merged precedent:** PR62 `cache_fee_table` / `cache_order_fee` (orchestrator `c6c4c0a1…` L680–704) verbatim, i.e. `feebook.order_fee(role, 1, fill_price, round_up=True, series='KXMLBSPREAD', table=stub with default M='0.5', formula_id=None)`. Maker terms come from `resolve_terms` and are not asserted. Label CACHE_NOT_R1P1. |
| R24 | PnL per filled contract | 9f50ba19 L90: For each filled contract with an **observed** settlement: `pnl = settle_value − fill_price − fee`, with `settle_value = $1.00` if our side matches the observed `result`, else `$0`. **Source substitution (commission (a)):** `settle_value` for a YES leg = `settlement_value_dollars`; for a NO leg = `1 − settlement_value_dollars`. `result` is not read by the runner. For finalized binary markets the two are identical (Examiner ACK: 6/6 agreement). |
| R25 | Arm metrics | 9f50ba19 L93 verbatim (see §PR60 as merged) |
| R26 | A1 freshness flag at the placement snapshot | rails `content_fresh_flag` via `hygiene.content_fresh_flag(previous, current, keepalive=False)` (hygiene L246–252, rails L302–316). **UNPINNED inputs:** `current.content = rails.canonical_book_content(orderbook_fp)`; `previous` = the immediately preceding dated snapshot of the same ticker in SOURCE_PINS (none ⇒ rails `initial` ⇒ fresh); `transaction_time=None` for both (no exchange transaction time exists in the pinned bytes, and a capture stamp is not a transaction time). **Structural consequence (book bytes only):** all 15 Sep-25 placements are fresh (5 `initial` + 9 content changed + WSH2 `initial`), and they would be under the stamp-as-transaction-time alternative too. So the stale bin is empty and `fresh_vs_stale_gap` is **NOT_ESTIMABLE (null, reason `stale_bin_empty`)**. This resolution cannot move any outcome. |
| R27 | Empty bin or zero ROI denominator | **UNPINNED** → metric null with a reason, never 0 |
| R28 | Stresses | 9f50ba19 L107 (`fees_2x`, `one_tick_worse`). `fees_2x` = fee × 2 (PR62 `times=2`). `one_tick_worse` = fill price + $0.01 on every fill (every leg is a buy). **UNPINNED:** fee under one_tick_worse = max(fee(p), fee(p+0.01)), so the stress never lowers cost. Stresses never change the fill set. |
| R29 | Clock flag | Each placement and fill row carries `pre_admitted_at = t < 2026-09-25T04:37:47Z` (strict; ruling `09763030…` precedent). Label only. Expected: all Sep-25 placements are post-admission. |
| R30 | ADMIT-1 window on books, GETs, prints, settlement response and `settlement_ts` | 9f50ba19 L44–L50 verbatim |

**UNPINNED rules (14), each resolved above:** R04, R08, R09, R11 (cancel-time detail), R12 (tape-end detail), R13 (stamp precision), R15, R16, R20 (best-level size), R21, R23 (fee mechanism), R26 (freshness inputs), R27, R28 (fee under tick stress). Settled-join rules S1–S9 are new by commission (a).
**BLOCKERS: none.** No rule needs a number without a frozen value.

## Settled-join (commission (a))

| # | Rule |
|---|---|
| S1 | **Inputs (pinned):** the 10 files of `lab/astra-capture/q6s5-kxmlbspread/settlement_only_2026-10-02/` (READY `0dd61920…`, DIGESTS `5905c137…`, folder digest `65cfe9e4…`) and join manifest `73af8822…`. Every sha is checked before read; any mismatch is a hard fail. |
| S2 | **Value field:** `settlement_value_dollars` only, from each raw GET body `raw/<ticker>.json`. **Guard-only fields** (never emitted into any quote, fill or PnL row, never passed to PR60): `ticker`, `status`, `close_time`, `settlement_ts` from the raw body, plus `response_utc`, `http_status`, `sha256` from `requests.jsonl`. `result` is not read. The join manifest is a cross-check only: same 6 tickers, same raw shas, same `settlement_value_dollars` strings, otherwise hard fail. |
| S3 | **Integrity chain:** `http_status==200`; raw file sha == `requests.jsonl` sha == DIGESTS entry; READY `digests_txt_sha256` == DIGESTS sha. |
| S4 | **Post-close guard:** `status=="finalized"` **and** `close_time < settlement_ts < response_utc` **and** `close_time < response_utc` (the read is post-close) **and** every joined fill has `fill_time < close_time`. Any failure ⇒ `PreCloseJoinRefused`. Here the settlement-GET `close_time` values are `2026-09-26T01:15:52Z..02:00:40Z` (2026-09-25 21:15–22:00 ET), early close per `can_close_early=true`, and every fill time is ≤ tape end `2026-09-25T06:03Z`. |
| S5 | **ADMIT-1:** `response_utc` and `settlement_ts` outside `[2026-09-27T00:00Z, 2026-09-30T04:00Z)`. `expiration_time` / `latest_expiration_time` (`2026-09-28T22:40/45Z`) are contract-schedule fields, not capture or determination timestamps; they are not read by the join. |
| S6 | **Value domain:** `Decimal(settlement_value_dollars) ∈ {1, 0}`, otherwise refused. Nothing fractional or void is imputed. |
| S7 | **Refusal effect:** a refused ticker's fills become `unresolved_inventory` with PnL null. They are never imputed and never dropped silently (counted). |
| S8 | **Ordering:** `settled_join(fills_bytes, fills_sha256, settlement_dir)` accepts only the serialized, hashed fills artifact produced by the engine. The builder and engine modules must not import the join module or reference the settlement folder (import-graph test). |
| S9 | **Scope:** Sep-24 tickers ⇒ `ClosedUniverseRefused`. PR60 behavior is unchanged: a `classify_fill` row with `settlement_ts` still raises `LookaheadRefused`. |

Join manifest `73af8822…` and the Collector READY both report 6/6 finalized and 1 YES / 5 NO.

## PnL and metrics (9f50ba19 verbatim; all null now)

- PnL: R24. ROI and arm metrics: 9f50ba19 L93 (quoted above). `requested_contracts_simulated`, `filled_contracts_simulated`, `fill_rate_simulated` (maker legs and taker legs reported separately and pooled), `unresolved_inventory`, `settled_join_n`, `n_books`, `excluded_*_n`, per-arm ROI, `pnl` (Σ over resolved fills), plus stresses `fees_2x` and `one_tick_worse`.
- v1.2 `common_scorecard.net_pnl_*` stays null (formula `pending_definition`; Archivist fee/account-version manifest absent). `common_scorecard.fill_rate` stays null (no demo/shadow/live fills).
- No robustness split, stratifier or extra metric is added; any other cut needs a new freeze.

## Lookahead declaration (commission (c))

Timeline (ET): games final 2026-09-25 21:15–22:00 (`close_time`) → PR60 freeze `9f50ba19…` declared 2026-09-29 16:52 → ACCEPT 16:55 → PR60 merged 17:18 → Collector settlement GET 2026-10-01 23:29–23:31 → Simulator READY 23:40 → **this freeze 2026-10-01T23:51:21-04:00**. Games were final before 9f50ba19 was written. Settlements were not on the box until 2026-10-01 23:29.

| Choice | Source | Why it is fixed independently of the labels |
|---|---|---|
| Universe (6 tickers) | 9f50ba19 L73 ∩ Conductor scope | It covers all Sep-25 panel markets, with no ticker or side selected; a permutation of labels leaves it unchanged |
| Placement instants, status gate, captured_utc | L74; R04, R05 | Book and GET stamps only, all captured 2026-09-25 04:48–05:34Z, pregame |
| Maker price / size / queue / cancel / rest end | L75; R06–R12 | Functions of the book at `t0`, the stamps and the trades request log only |
| Both sides quoted at every placement | L75, L76 | Symmetric two-sided strategy, so no rule can prefer the side that later won |
| Print window, our-side, depletion, trigger, exclusions | L82–L86; R13–R18 | Use only prints with `created_time` strictly after `t0` (second-truncated) and before cancel. Prints at or after a quote's own stamp never influence that quote. |
| Taker leg | L76; R20–R21 | Book at `t0` only |
| Fee | L92, L107; R23 | Function of role and fill price only |
| Freshness bin | R26 | Book bytes only; structurally all-fresh |
| Settlement | S1–S9 | Read only after fills are frozen and hashed; enters only `settle_value` in R24 |

**Required label-permutation property:** quotes and fills are a function of (SOURCE_PINS bytes) only; PnL is a function of (fills, settlement_value_dollars). Permuting the `settlement_value_dollars` vector across the 6 tickers must leave the canonical bytes (sorted-key JSON, `separators=(',',':')`) of `quotes.json` and `fills.json` byte-identical and their sha256 identical, while PnL changes whenever a filled ticker's label flips.

**Required tests (named; all green before PR leaves draft):**
- **T1 label permutation (fixture):** a synthetic 2-ticker fixture with ≥1 maker fill and ≥1 taker fill on a ticker whose label flips under the swap. Assert quotes and fills bytes are identical, sha identical, and PnL differs. **T1b (pinned tape):** over all 720 permutations of the real 6-value vector, assert that the quotes/fills sha is constant. It asserts identity only and prints no PnL, count or label.
- **T2 pre-close join refusal:** `response_utc ≤ close_time`, `settlement_ts ≤ close_time`, `status≠finalized`, missing `close_time`, or a fill at/after `close_time` each raise `PreCloseJoinRefused`. `settlement_value_dollars ∉ {0,1}` is refused. A Sep-24 ticker raises `ClosedUniverseRefused`.
- **T3 tape-prints-after-quote refusal:** (i) the quote builder takes no trades argument, and passing one raises `LookaheadRefused`; (ii) a book or GET stamped after `t0` cannot change the quote at `t0`; (iii) a print at `t0`, or within `t0`'s stamped second, is never used by the engine, and PR60 `classify_fill` with `trade_ts == quote_ts` raises `LookaheadRefused`; (iv) a print exactly at the cancel stamp is used by neither order.
- **T4 A0/A1 verbatim:** 9f50ba19 lines 93, 100 and 101 and 4f65dcdf lines 47–48 match the strings in this freeze byte-for-byte (sha256 in FROZEN_EXPERIMENT `verbatim_sha256`). PR60 `ARMS` == parent `ANALYSIS_SLICE` == {Q6S5A0: maker_vs_taker_native, Q6S5A1: content_fresh_vs_stale_bin}. PR60 `orchestrator.py` sha256 == `296cfe64…` and lab tree == `78fca23c…` (unchanged).
- Carried / supporting: ADMIT-1 rejection (synthetic book, print, GET, settlement response and `settlement_ts`); closed-manifest sha fail-closed (one-byte tamper); Lee-Ready refusal; native-conflict exclusion; block-trade exclusion; price-inconsistency exclusion; crossed-book no-placement; no-bid-side no-order; queue boundary (`cum == queue_ahead` ⇒ no fill; `queue_ahead+1` with a strict-through print ⇒ fill at `p`; a touch print counts toward `cum` but cannot trigger); taker needs best-level size ≥ 1; no-invent (no qualifying print ⇒ no fill; no join ⇒ PnL null); CACHE fee label with `formula_id` null; `counts_toward_keep=false`; committed `results`/`pnl`/`roi` null; forbidden imports (`urllib`, `requests`, `http`, `socket`, `sqlite3`); import graph (builder/engine never import the join); `capture.sqlite` and the weather `archive.sqlite` paths refused.

## Verdict mapping (commission (d))

- **Ceiling ITERATE. KEEP impossible.** `counts_toward_keep=false`, `promote=false`, `live_promotion=false`, `counted_as_experiment_pnl=false`.
- **v1.2 rule (verbatim, template json line 777):** "fill_rate counts only fills tagged demo, shadow or live. Replay/simulated fills go to simulated_fills, labeled \"simulated\", and never count toward KEEP." Every fill here is `MODEL` / `tag=replay`, so the fills go to `simulated_fills` only. Companion ACCEPT `a5398129…` `keep_eligibility`: "public_trade_through_conservative is MODEL evidence: counts_toward_keep=false. Best achievable outcome for this run is ITERATE (or KILL)."
- **Evidence class:** `IN_SAMPLE_DEV` / `HISTORICAL_REPLAY` (labels known; study_label proposed "historical replay", owned by Examiner/Archivist).
- **family_size = 1** on the Sep-25 universe. Confirmed vs PR60: one knob `fill_model`, one implemented value, and no other knob has ever been outcome-scored on the 3 Sep-25 games. Note that PR60 is also counted as 1 of the 4 knobs in the CLOSED Sep-24 family (holdout addendum `370dc31d…` line 160); that family is not touched here. **Effective n = 3 games** (6 same-game-sibling markets).
- **Decision rule:** PR60 froze **no outcome hypothesis and no threshold**. FROZEN_EXPERIMENT `7383b483…` has no hypothesis field; the PR60 EXPERIMENT_SPEC says "Measurement infrastructure only". So the primary is measurement-only: **co-primary** `Q6S5A0 maker_vs_taker_roi_delta` (CACHE-fee-net per 9f50ba19 L90/L93) and `Q6S5A1 fresh_vs_stale_gap` (expected NOT_ESTIMABLE, R26). PR60 defines no A1−A0 contrast (the arms are two slices of one strategy, not competing strategies), so none is computed. **No new thresholds.** Any reading is descriptive and ITERATE-capped. The Examiner owns the verdict, within {ITERATE, KILL per a5398129, NOT_SCORED}; this freeze proposes no KILL criterion.

## Fee

FEE_PIN `9c0f3554…`: `fee_type=quadratic`, `fee_multiplier=0.5`, `feebook_formula_id=null` → **CACHE_NOT_R1P1**, `fee_honest=false`, `claim_as_live_R1P1=false`. Not R1-P1. Mechanism R23.

## Expected structural counts (pre-run; book/GET/tape structure only; NOT results)

`n_books` (Sep-25 dated) = 15 · eligible placements = 15 · crossed/locked = 0 · empty sides = 0 · fresh = 15 / stale = 0 · requested maker contracts = 30 · Sep-25 prints = 21 (block 0, native conflict 0, price-inconsistent 0) · `excluded_admit1_window_n` = 0 · settled tickers = 6/6. Requested taker contracts depend on best-level size ≥ 1 and are computed at run time.

## Cloud instructions (after Conductor ACCEPT only)

1. **One** cloud (sole Variants cloud), base **main `f233079d9e7d2a91e2100f2085bcf85d0006e28f`**, **draft PR**. No second cloud. No dual implement.
2. New lab dir `kalshi_q6s5_kxmlbspread_strategy_fill_scorability_lab_20261002/` with `tape_quotes.py`, `fill_engine.py`, `settled_join.py`, `scoring.py`, `orchestrator.py`, `tests/`, `pins/`, `results/`, `EXPERIMENT_SPEC.md`, `README.md`, `FROZEN_EXPERIMENT.json`, an Examiner HOLD_PRE_PR file, and one registry row in `docs/EXPERIMENT_REGISTRY.md`.
3. PR60 lab, the parent feequeue lab, feebook, rails, hygiene and the PR61/62/63 labs stay **byte-unchanged**. Import PR60 `orchestrator.py` and the parent orchestrator read-only via `importlib` from their paths.
4. **Do not create** `lab/astra-capture/q6s5-kxmlbspread/panel_admitted.json` at the repo path: PR60 `load_panel` raises if it exists (L506–507). Vendored inputs live under the new lab's `pins/`.
5. Vendor the authentic pin bundle (below) **verbatim** under `pins/` (tgz plus extracted tree) and check it against its MANIFEST. The settlement folder and join manifest come only from the bundle. No GET.
6. No `sqlite3` import at all (no sqlite input). No network imports. Never open `capture.sqlite` or `lab/astra-capture/weather-nowcast/archive.sqlite`.
7. Committed outputs: `results/EMPTY_RESULTS.json` with `results`/`pnl`/`roi` and all metrics **null**, and `results/UNIT_RESULTS.md`. **No real-tape quote, fill or PnL artifact is committed.** Simulator runs the merged runner; Examiner scores. Examiner status stays HOLD_PRE_PR until merge.
8. Units T1–T4 and the supporting list are green before the PR leaves draft.

## Conductor attention items (not blockers)

1. **Sep-25 "permanently out of scope" wording.** The FL-band freeze `fb6540f5…` rule 6, the game-phase freeze `5beba803…` rule 6, ruling `09763030…` (`sep25_markets`, "for FL-band") and the holdout addendum `370dc31d…` (line 61: Sep-25 excluded from the holdout; line 177: "no re-GET of the Sep-25 markets" in that addendum's refusals) put the Sep-25 markets out of scope **for those packets**. The cited reason was the pre-close GET `close_time` `2026-09-28T22:40/45Z` falling in the window. The settlement GETs show the actual early close `2026-09-26T01:15–02:00Z`, outside the window. The scheduled field now survives only as `expiration_time`. PR60's own companion ruling `a5398129…` authorized the settlement-only fetch, and the commission directs this join. **This freeze touches neither the holdout nor its Sep-25 exclusion.** Conductor ACCEPT should confirm the scoping explicitly.
2. **No commission packet on disk.** The commission and the do-not-score instruction were relayed (as the Examiner ACK also notes).
3. **A1 structurally NOT_ESTIMABLE** (R26). Only A0 can produce a number.
4. **Thin tape.** 21 Sep-25 prints, of which only those strictly after each placement and before cancel/tape end can fill maker legs. Many maker legs may end unfilled; that is the honest outcome and is not compensated.

## p16 preregistration checklist

| # | Item | Status | Evidence |
|---|---|---|---|
| 1 | market_universe | **satisfied** | 6 Sep-25 tickers / 3 games; panel `e36de2d1…`; KXMLBSPREAD only |
| 2 | exclusions | **satisfied** | Sep-24 + KXHIGH CLOSED; ADMIT-1 window; `capture.sqlite`; native conflicts; block trades; price-inconsistent rows; crossed books |
| 3 | receipt_time_information_set | **satisfied** | book at `t0` + prints strictly after `t0` (second-truncated) and before cancel; settlement post-fills only |
| 4 | fee_regime | **satisfied** | feebook @22371178 CACHE table M=0.5 (PR62 precedent); CACHE_NOT_R1P1; fees_2x |
| 5 | order_timing | **satisfied** | R03–R05, R11–R13, R20 |
| 6 | sizing | **satisfied** | 1 contract per leg per side |
| 7 | fill_model | **satisfied** | `public_trade_through_conservative` (9f50ba19 L82–86 + PR60 `_through`); demo UNAVAILABLE |
| 8 | stopping_rules | **satisfied** | freeze-before-implement; ACCEPT before cloud; single cloud; single pass over closed manifest; hold to settlement |
| 9 | evaluation_metrics | **satisfied** | 9f50ba19 L93 co-primary + simulated_fills + stresses; v1.2 nulls |
| 10 | limit_candidate_variants | **satisfied** | no new knob; 1 value |
| 11 | log_every_attempted_variant | **satisfied** | only this run; any other variant needs a new freeze |
| 12 | separate_discovery_tuning_evaluation_periods | **missing** | labels known before freeze; no untouched set; holdout = approved KXMLBSPREAD prereg `370dc31d…` (queued) |

Counts: satisfied 11, n/a 0, missing 1.

## Integrity

- Pinned bytes carried **verbatim** and checked with `sha256sum`. The authentic pin bundle is `/workspace/Q6S5_PR60_SCORABILITY_authentic_pins_2026-10-02.tgz`; its sha, size and file count are in the ACCEPT ping (they cannot be inside the bundle).
- Packet folder: `packets/Q6S5_PR60_SCORABILITY/` (`FROZEN_EXPERIMENT.json`, `SOURCE_PINS.json`, `EMPTY_RESULTS.json`, `DIGESTS.txt`, `MANIFEST.sha256`). JSON twin: `packets/VARIANTS_Q6S5_KXMLBSPREAD_STRATEGY_FILL_PR60_SCORABILITY_FREEZE_2026-10-02.json`.
- `digest_all_match_claimed=true` for every pin cited. Absent (declared, not recreated): Mechanic demo KXMLBSPREAD artifact; Examiner `formula_id`; Archivist fee/account-version manifest; untouched evaluation set; Conductor commission packet; queue bytes `08aa54de…` (superseded, routing-only).
- RULE-FROZEN-EDIT-PREV-BYTES-001: this freeze **creates only new files**. No frozen file was edited, so there was no `_prev` write.

## Refuse binds

invent fills / PnL / depth / markets / settlement_ts · label known outcomes as prospective · pass any settlement field into PR60 `classify_fill` · read settlement before fills are frozen · Lee-Ready · tick-rule or mid inference · live or demo orders by Variants · any GET · dual-cloud · claim CACHE as R1-P1 · count simulated fills toward KEEP · new knob or parameter · move any rule after a run · Sep-24 KXMLBSPREAD or KXHIGH reuse · S1 KXMLBGAME ML / Q6-000 / Cap-SR / Q6S1 retune · Refiner routing · `admit.py` · `capture.sqlite` · weather `archive.sqlite` · ADMIT-1 window data · backfill / interpolate · editing PR60 / parent / feebook / rails / hygiene bytes or prior SCORE / ACCEPT / READY / FEE_PIN / HOLD bytes
