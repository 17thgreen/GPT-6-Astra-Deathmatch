# FREEZE — Scout external hunt while box-IP Kalshi CLOSED (2026-10-03)

**Seat:** Market Scout "KALSHI" (executor) · Astra/Kalshi desk (Logan M)
**Commission:** CONDUCTOR_KICK_SCOUT_EXTERNAL_HUNT_WHILE_BOX_IP_CLOSED_2026-10-03.json (sha256 9c583e82aec1c5d622f222875c19c1edc5f4c11de4908fe32f503494aa7f60c9)
**Governing ruling:** CONDUCTOR_RULING_WEATHER_BOX_IP_CLOSED_AFTER_R2E_429_2026-10-03.json (sha256 dd1d70396472a72fce2bad5233ba0190f5df4c14568d9b7746bf282ef892b2dc) — BOX_IP_KALSHI_CLOSED.
**Frozen before any external pull.** Local box inventory (read-only, metadata-level) was performed before this freeze; no web/GitHub fetch yet.

## Scope
- Output: <=5 kernels (triage only) that could beat or stress Q6-000 (NFL KXNFLGAME ML maker allocator, SHADOW, +$345.24 / 6.90% on 31 dev games, maker 0.0175 / taker 0.07 modeled).
- Each kernel: economic thesis (who pays), data needed + on-box status (exact paths, verified counts/ranges) or external source (free/public?), fee+cost path (taker 0.07*M*C*p(1-p) round-up; maker 0.0175*M; spread/queue), evidence tags [V]/[I]/[H]/[A]/[U], rec TRY/HOLD/DEFER/SKIP.
- Priority: kernels scorable on data ALREADY ON THE BOX.

## Search plan (pre-declared)
1. GitHub (MCP search_repositories / search_code / get_file_contents; web): open-source Kalshi bots with documented sports/microstructure strategies (2025–2026), Polymarket↔Kalshi cross-venue tools, free sportsbook odds archives (nflverse games.csv lines; MLB/NHL/tennis odds datasets; tennis-data.co.uk), settlement/resolution-lag tooling.
2. Papers: Bürgi/Deng/Whelan Kalshi (re-cite), arXiv/SSRN 2025–2026 on Kalshi/prediction-market sports efficiency, favorite-longshot bias, closing-line value, prediction market vs sportsbook.
3. Public web: Polymarket public data docs (gamma/CLOB prices-history), NFL operations rules (inactives timing), sports-data free sources.
4. Save every fetched source used as evidence to raw/ with MANIFEST.sha256 (url, fetch time UTC+ET, sha256).

## Exclusions (occupied — not re-proposed as new; reuse of their data allowed with distinct thesis)
S1 KXMLBGAME ML ADMIT; R2-P3 NFL props ADMIT; S4 KXNCAAFGAME TRY; S5 KXMVECROSSCATEGORY measurement FREEZE; S2 NFL SPREAD/TOTAL wait-C1; cash-cow freezes KXUFCFIGHT, KXHIGHNY/CHI weather, KXBTC15M; Q6S5 KXMLBSPREAD (parked, Variants); Q6S1 KXATPMATCH (ATP bakeoff); Q6S2 KXNHLGAME C2; CEM-006 macros + CPI CEM-003; Card 06 open-window; Card 04 perps (REJECT); Cap-SR/FQ/Variants capital structure; RFQ Card 07; 000 retune; empty KXMVENFL*. Also prior-covered: R3-P3 FL-band maker/taker (Bürgi–Deng–Whelan), R3-P4 Dubach longshot spread, R1-P3 sportsbook de-vig real-time gate (ACCEPT measurement/Adversary only), FL-band H1 KXMLBSPREAD KILL (CEM-ASTRA-20261001-001), card03 liquidity-subsidy.

## Rules
- NO Kalshi API calls from the box (api.elections / external-api / trading-api / demo). Avoid kalshi.com domains entirely; fee facts cited from on-box CACHE (scout_house_fee_2026-09-24/raw/docs, labeled cache).
- No live orders; no invented P&L, fills, backtests, inventory. No freezing/scoring strategies (Variants/Examiner own that).
- ADMIT-1 prospective capture (astra-capture/prospective/capture.sqlite) is holdout-class: metadata-level inventory only (row counts, ticker counts, timestamp bounds); no price/outcome peeks.
- RULE-FROZEN-EDIT-PREV-BYTES-001 for any edit to filed files.
- No messages to other agents; report to parent only.
