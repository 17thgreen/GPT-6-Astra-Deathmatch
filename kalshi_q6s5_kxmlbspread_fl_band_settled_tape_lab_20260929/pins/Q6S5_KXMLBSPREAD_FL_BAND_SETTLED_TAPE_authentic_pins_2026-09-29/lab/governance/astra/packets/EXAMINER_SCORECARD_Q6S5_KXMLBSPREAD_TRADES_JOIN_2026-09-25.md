# EXAMINER SCORECARD — Q6S5 KXMLBSPREAD TRADES JOIN 2026-09-25

**Seat:** Examiner (Kalshi) · Astra desk  
**Packet:** `Q6S5-KXMLBSPREAD-FEEQUEUE-HARNESS` · family `Q6S5-MLBSPREAD-FEEQUEUE`  
**Template:** v1.2 (`56bcf626…`)  
**Status:** SCORED  
**Verdict:** **ITERATE** (3rd / trades-join re-SCORE)  
**promote / live_promotion / counted_as_experiment_pnl:** false / false / false  
**Stamped ET:** 2026-09-25T02:17:39-04:00  
**Score packet sha256:** `a18f2ad2f704d10ec526ccd2808edf8088f88de307ff8b3fe9845fa14ddde05a`

## Desk headline

Trades-join re-SCORE=**ITERATE** (3rd): `n_trades_joined=11744` native classified (side counts yes=6947 / no=4797); `maker_vs_taker_roi_delta=null` (classification≠ROI; no strategy fill/PnL); `fresh_vs_stale_gap=null` (content_fresh True=29); `settled_join_n=6` observational; `n_books=12`; `results`/`pnl=null`; `lee_ready=REFUSED`. Fee **CACHE×0.5 / CACHE_NOT_R1P1** (FEE_PIN `9c0f3554…` formula_id absent). Q6-000 unchanged. Prior harness SCORE `348e2981…` untouched; ACCEPT harness iterate `54b0b1b7…` superseded in context only. Capture SCORE `db9bd220…` earlier lineage.

## Authority pins (verified on disk)

| Item | sha256 |
|---|---|
| RESCORE kick | `650283a7a69b4e6411b51c036e876694f27eb8db7908a52325092a1e2142e96f` |
| ACK Simulator READY | `f338a09652f1da4442bdfcf579087660f435529885eb110a884b87acda3a23f2` |
| Simulator kick (cite) | `76de2f1fa2461008bc1205e5004230ffd45fd2d3e6193d6cc0c11c616b499006` |
| Simulator READY | `5b47dea926a57e3f1c424e8df62f56ef9b1f02eea87bdd426b4e9248c21465f4` |
| TRADES_JOIN_RUN_RESULTS | `f707bcbdfddbc1505c0b22464200d07747656e703efba1c9cc66aa80eb0819ef` |
| TRADES_JOIN_METRICS | `3dcdf2ab5af1cc58a60f9664f9313ccb2cd95e87f346a009f7e2be2fcc491c32` |
| DIGESTS (lab) | `02478c879bba61f1e634742c0df31e9fb0bc038b9d90cc0cc3324e313192732c` |
| Trades READY | `57194f272ab6bbe7a4d116c1fd4aabd5199e3a02a6cd96ed5cc6b7bd4bafb867` |
| Trades DIGESTS | `12b537a25b02fb33177d5a41c821f94677f1da88e8d1dd63178c3c9f59fac12b` |
| Freeze | `4f65dcdf536755b9f7dc2449c2dcd90b2df74cdf99a441b676f1a71c4d709c6e` |
| ACCEPT harness | `5adc42f9c9533238a2187aafe7593bdf1b8cdec6d12b8d3e9b12cb5ab29000fc` |
| ACCEPT harness iterate | `54b0b1b7d57d42f3a2f2d0caefd72be734532eaae8d8c54fbcb8817a7df99a71` |
| FEE_PIN | `9c0f3554eedc582ed4bed940575bf7ee6c0540ce5134140c5ea19e7c458d2b6a` |
| Examiner ACK Simulator READY | `5e2235c1d3ee100c5b7dcb1cb7c93579046f5d515b3e52d3cf0fa77d9bc7aacf` |
| Prior harness SCORE (cite) | `348e2981d191fda5a228ef77fc578b0821bd731ae6aa38b1b8004d9d82ba3d62` |
| Capture SCORE lineage | `db9bd220b5dd61229b6481a27d03222f36ac0ec816efa3402ef35404a0d4fb8e` |
| Prior HOLD (cite) | `bd34d2075dc285b2bd2e2a83b15fdb85715b24389aa41e99f46b20672c8a91eb` |
| Runner | `9a52bcb7eb72466f8189c835062cb54216d73ddc5ca6c88e2909a3c553b31c88` |
| Orchestrator | `e224686a1bbe4173f00e62c3d2cba78a3c48eecef45ed77c678564def9d5bbfc` |

## Metrics from disk (TRADES_JOIN_METRICS / RESULTS)

| Field | Value |
|---|---|
| maker_vs_taker_roi_delta | null |
| fresh_vs_stale_gap | null |
| settled_join_n | **6** (observational; not fills/PnL) |
| n_books | **12** |
| n_trades_joined | **11744** |
| n_classified_native | **11744** |
| arm_a0_taker_outcome_side_counts | yes=**6947** / no=**4797** (verified RESULTS; matches kick) |
| empty_honest | KXMLBSPREAD-26SEP251840TBPHI-TB2 (n_trades=0) |
| arm A1 content_fresh True | 29 rows classified |
| results | null |
| pnl | null |
| lee_ready | REFUSED |

## Fee honesty

**CACHE_NOT_R1P1** — CACHE quadratic×0.5; `fee_honest=false`; FEE_PIN confirmed `formula_id` absent. Do **not** claim `astra.r1p1.feebook.claude_order_level_ceil.v1`.

## Freeze / ACCEPT / kick clauses (quoted)

- Freeze hard rules: "No invent fills/PnL/depth/settled counts" · "`results`/`pnl` null until Examiner after Clock admit"
- Freeze fee: "CACHE-LABELED quadratic×0.5 (not R1-P1 live until Examiner tests `/series` pin)"
- Freeze arms: Q6S5A0 native `taker_*` only / Lee-Ready REFUSED; Q6S5A1 content_fresh bins; invent fills REFUSED
- Freeze refuse: "claim cache fee = R1-P1 live without Examiner `/series` test"
- No freeze fail-closed KILL when arm ROI null after honest harness (invent fills refused)
- ACCEPT harness: "Fee remains CACHE-LABELED … do not claim R1-P1"
- ACCEPT harness iterate `54b0b1b7…`: measurement ITERATE not strategy-corporeal; Not Refiner (bytes untouched; superseded in context only)
- RESCORE kick: "Arm ROI/gap still honest-null (classification only; no strategy fill/PnL) — do not invent"; "Coverage / settled_join_n / n_books / classification counts ≠ KEEP"; "promote=false unless KEEP bar met"

## Verdict bar

| Candidate | Decision |
|---|---|
| KEEP | **REFUSED** — required arm ROI/gap null; results/pnl null; CACHE_NOT_R1P1; coverage/n_trades/classification ≠ KEEP |
| KILL | **REFUSED** — freeze does not fail-closed KILL on honest null after invent-fills refused; measurement progressing (native classification now present vs prior harness 0 taker hits); not Refiner |
| **ITERATE** | **STAMPED (3rd)** — trades join + native classification complete; KEEP gates still blocked; wait strategy fills/PnL (classification ≠ ROI) + optional R1-P1 formula_id if fee-honest KEEP sought |

## Relation to prior ITERATE `348e2981…` / `db9bd220…`

Prior harness SCORE = harness-present / 0 native taker hits / arm-ROI honest-null ITERATE (2nd). Capture SCORE `db9bd220…` = capture-complete / harness-absent ITERATE (1st). This packet = trades-join native classified (11744) / ROI still honest-null ITERATE (3rd). Prior bytes untouched; this re-SCORE supersedes context only. ACCEPT harness iterate `54b0b1b7…` untouched, superseded in context only.

## wait_for / blockers

**wait_for:** strategy fills/PnL so Q6S5A0 ROI and Q6S5A1 gap can be non-null (classification ≠ ROI); optional Examiner R1-P1 formula_id pin if fee-honest KEEP sought; Conductor ACCEPT/allocate (Not Refiner).

**blockers:** maker_vs_taker_roi_delta=null · fresh_vs_stale_gap=null · results=null · pnl=null · fee_class=CACHE_NOT_R1P1

## Scoreboard

**Unchanged:** Q6-000 / Arm D KEEP +$345.24 / +6.90%

## Calibration

N/A (`emits_probabilities=false`)

## Refuse

KEEP with null ROI/gap/PnL · invent fills/PnL · treat classification as ROI/KEEP · claim CACHE as R1-P1 · treat coverage/n_trades/settled_join as KEEP · live orders · Q6-000/Cap-SR/S1 retune · edit prior SCORE/ACCEPT/FEE_PIN/HOLD bytes · route to Refiner
