# Reward scoring clarification discovered during AMS-010

Kalshi's July 15, 2026 filing states a July 30 effective date. Its clean terms
(PDF page 8, zero-index page 7) include every bid at the price level that brings
cumulative size to target. The entire level scores; it is not clipped at target.
The previous whole_level sensitivity matches this published procedure. The capped
calculation remains a deliberately stricter stress for our one-cent proposals.
Frozen AMS-009/010 outputs are preserved, and AMS-011 uses whole-level scoring.

Source: https://www.cftc.gov/filings/orgrules/rules07152610358.pdf

Kalshi separately documents execution queue position using price-time priority:
https://docs.kalshi.com/api-reference/orders/get-order-queue-position

Our inference: later orders at the same qualifying price may earn proportional
rewards while earlier orders retain execution priority. We have not measured
individual queue position, cancellations ahead, actual fill protection or credits.
This motivates smaller supported-level quotes within the same liquidity strategy.

The filing retains eligibility and participation conditions. This is a scoring
clarification, not confirmation of our account entitlement or approval of a bot.
Current help: https://help.kalshi.com/en/articles/13823851-liquidity-incentive-program
