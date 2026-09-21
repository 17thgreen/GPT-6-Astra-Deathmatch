# Q6 selected-candidate handoff

Use SHADOW_CANDIDATE_FREEZE.json for the selected F/P/R label, exact source
hashes, the unchanged execution-engine hashes and the four scenario settings.
A null label means the predeclared rule selected no candidate. Do not substitute
the largest development P&L result. Use results/selection.json to audit the rule.

This is an offline policy package; it contains no live order endpoint, account
credentials or durable collector deployment. The frozen candidate is created by
FactorialReplay(markets, config, Factors(flow, protection, ranking)). The original
router control is AdaptiveReplay(markets, config, 'baseline'); full bundle111
uses the same FactorialReplay with all flags True. They are separate alternative
accounts consuming one identical received data stream, not concurrent bots
claiming independent fills from shared liquidity.

For a prospective check, retain the selected candidate, original router and111
as named comparison arms, all with the same5k initial capital,250event cap,
250assumed exit budget (or a separately frozen observed-depth treatment), fee
assumptions, quote latency and queue stress. Actual trading requires additional
verification of queue service, venue fees and collateral/netting mechanics.
The old Q5 capital-only two-cent buffer is not part of the Q6 policy.

FORWARD_PROTOCOL.md is the carried-forward Q5 collection/admission protocol;
its references to three earlier Q5 candidate policies are provenance, not the
new Q6 arm definitions above. The schedule-only reservation still requires
complete venue identity and a functioning durable public-data collector before
the applicable full T−7d window. The first such start is2026-09-22T00:15UTC.
Missing an admission/capture deadline cannot be fixed by backdating a freeze or
calling partial coverage complete. A replacement cohort must be admitted from
schedule-only information before its windows/outcomes are examined.

Current status: no completed fresh Q6 evaluation and no always-on recorder.
Past 31-game results are repeatedly examined development evidence. Keep all
negative results and both weeks visible; do not retune the candidate after
inspecting future outcomes and still call that cohort untouched.
