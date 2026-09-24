# AMS-004: reward-market depth survey

Captured 2026-09-24T03:32:10.474036+00:00 through 2026-09-24T03:35:44.411968+00:00.

Fresh API catalog: 5447 active-liquidity program entries; 5441 distinct tickers after positive-reward, positive-target, unpaid and current-window filters. Cursor remaining at cap: False.

Selected 200 tickers by a prespecified hash ordering before observing depth. 199 were open, in their listed reward window, and had usable metadata and full books. 32 of those (16.1%) were below target on at least one side; 30 had an entirely empty side.

| Classification | Markets |
|---|---:|
| both_meet | 167 |
| both_short | 3 |
| no_short | 10 |
| outside_open_window | 1 |
| yes_short | 19 |

## Observed gaps

| Market | Classification | YES depth | NO depth | Target |
|---|---|---:|---:|---:|
| KXTXERCOTPEAKD-26SEP24-T83500 | no_short | 23869.00 | 0 | 1000.00 |
| KXTRUEV-26SEP23-T1288.69 | yes_short | 0 | 2178.00 | 1000.00 |
| KXAAAGASDMN-26SEP24-4.3700 | both_short | 313.00 | 49.00 | 1000.00 |
| KXTRUEV-26SEP23-T1238.69 | both_short | 0 | 129.00 | 1000.00 |
| KXCPICOREYOY-26SEP-T3.5 | yes_short | 0 | 58026.01 | 1000.00 |
| KXYTTOPVIDEOG2D-26SEP23-NEW | yes_short | 0 | 5297.00 | 1000.00 |
| KXWNBAPLAYOFFHOST-26IND-9 | yes_short | 0 | 12576.20 | 1000.00 |
| KXAGTWINNER-26SEP24-ACR | yes_short | 0 | 8811.81 | 1000.00 |
| KXSOFRD-26SEP24-T3.82 | yes_short | 0 | 17720.61 | 1000.00 |
| KXAAAGASDCA-26SEP24-6.2000 | no_short | 1106.00 | 0 | 1000.00 |
| KXAGTWINNER-26SEP24-GEN | yes_short | 0 | 19837.43 | 1000.00 |
| KXAAAGASDFL-26SEP24-4.4750 | yes_short | 0 | 5264.00 | 1000.00 |
| KXRAIN-26SEP23-MIA | no_short | 284960.45 | 0 | 1000.00 |
| KXCPIYOY-26SEP-T4.2 | yes_short | 0 | 29112.00 | 1000.00 |
| KXNETFLIXTOPVIEWSTV-26SEP28-35 | yes_short | 0 | 12174.01 | 1000.00 |
| KXAAAGASDIN-26SEP24-4.0200 | yes_short | 0 | 2259.00 | 1000.00 |
| KXTOPMODEL-26SEP28-CLAU | yes_short | 0 | 11221.01 | 1000.00 |
| KXVELOPOS-26OCT03-T175 | no_short | 9416.62 | 0 | 1000.00 |
| KXDIESELD-26SEP24-T6.495 | no_short | 4532.00 | 0 | 1000.00 |
| KXYTDAILYTOPVIDEOG-26SEP23-BAS | yes_short | 0 | 1234.00 | 1000.00 |
| KXRT-DIG-25 | no_short | 36079.01 | 0 | 1000.00 |
| KXAAAGASDFL-26SEP24-4.4350 | yes_short | 0 | 7102.30 | 1000.00 |
| KXRT-PRI-55 | no_short | 70417.01 | 0 | 1000.00 |
| KXLLM1-26SEP28-MOON | yes_short | 0 | 42782.00 | 1000.00 |
| KXTRUMPSAY-26SEP28-BLOC | no_short | 95777.70 | 0 | 1000.00 |
| KXYTDAILYTOPVIDEOG-26SEP23-XAM | yes_short | 0 | 1234.00 | 1000.00 |
| KXTXERCOTPEAKD-26SEP24-T82500 | no_short | 20381.00 | 0 | 1000.00 |
| KXAAAGASDOR-26SEP24-5.0800 | both_short | 93.00 | 28.00 | 1000.00 |
| KXAAAGASDIL-26SEP24-4.8950 | yes_short | 0 | 2259.00 | 1000.00 |
| KXDWTSRANK-226DEC31-GDEL | yes_short | 0 | 6162.79 | 1000.00 |
| KXAAAGASDFL-26SEP24-4.3300 | no_short | 3453.00 | 0 | 1000.00 |
| KXAAAGASW-26SEP28-4.6800 | yes_short | 0 | 35893.46 | 1000.00 |

## Post-hoc entry feasibility

A separately labelled post-hoc screen (ENTRY_SCREEN.json) considers one target-sized one-cent order only when exactly one side is empty and the other meets target. Of 29 such markets, 16 would cross an opposite 99-cent bid and cannot supply a wholly resting target at that price. Thirteen permit a resting one-cent quote; only three have ideal remaining half-pool rewards exceeding the $10 principal of one full losing fill. These are Netflix top-show views, Claude top-model ranking, and weekly U.S. gas prices. Their ideal gross rates are approximately $0.39, $0.65 and $0.32 per hour respectively. This is a feasibility filter, not a claim that a fill loss occurs only once or that the reward lasts long enough to offset it.

The entry screen was selected after seeing the survey and is not an independent holdout. It led to the separately preregistered AMS-005 full-catalog screen.

## Interpretation and limitations

These are depth gaps, not measured profitable trades. Depth is total resting contract quantity; a candidate still needs valid quote prices, genuine fill exposure, reward scoring, eligibility, and sufficient remaining time. No orders were placed and no reward or profit was realized.

The denominator is the sampled current positive-reward market frame, not all Kalshi markets. One snapshot per market cannot measure gap duration. Metadata and books were fetched at different times. Overlapping programs were reduced to one program ID per ticker, so another active program can impose a different target. Account eligibility and governing terms were not independently validated.

The batch orderbook requests used comma-joined tickers and received HTTP 400 parameter-validation errors. The prespecified fallback used individual full-depth GETs and preserved the failures. A future collector should use the documented array encoding; frozen code was not changed during acquisition. Missing observations and time-window exclusions remain in the denominator table.

HTTP receipt statuses: {'200': 205, '400': 4}. Acquisition elapsed 221.02 seconds. Three focused classification tests passed before acquisition; raw-body hashes, frozen sources, panel hash, and individual-book classifications verified after acquisition.

Hypothesis/specification commit: 49e46781b7af755f1303123824dee82d067724df. Acquisition/test freeze: 092eb61704cc0a64ca3df2efa899038e32c53759.

Public scoring: https://help.kalshi.com/en/articles/13823851-liquidity-incentive-program
Public catalog: https://docs.kalshi.com/api-reference/incentive-programs/get-incentives

The archive contains raw receipts, code, tests, frozen specification, fixed panel and results. No process remains running after this bounded survey.
