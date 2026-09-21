"""Render the completed, immutable experiment results into the research memo."""
import json
from pathlib import Path


def main():
    root = Path(__file__).parent
    result = json.loads((root/"results/round2/forecast_results.json").read_text())
    selection = json.loads((root/"results/round2/selection.json").read_text())
    model = json.loads((root/"results/round2/model.json").read_text())
    tests = result["tests"]
    n = sum(v["games"] for v in tests.values())
    kind = model["kind"]
    description = {"clock":"clock-conditioned Stern probit", "residual":"Stern model with symmetric nonlinear state corrections",
                   "v1":"the original state-conditioned prototype refitted on more history"}[kind]
    all_better = all(v["models"]["challenger"]["logloss"] < v["models"]["published_v1"]["logloss"] for v in tests.values())
    opening = ("The selected challenger improves log loss over the first prototype in every evaluation season."
               if all_better else "**Further complexity did not establish a reliable improvement over the first prototype. Keep V1 as the research reference.**")
    lines = ["# Stern lab — second-round results", "", "**21 September 2026**", "",
        f"{opening} The selected specification is **{description}** (`{selection['selected']}`).",
        f"I evaluated it on **{n:,} non-tied NFL games across 2023–2025**, using equal game weights.",
        "These are historical forecasting results; Kalshi trading profitability remains untested.", "",
        "## Comparison on identical states", "", "Lower log loss and Brier score are better.", "",
        "| Season | Original Stern LL | Published V1 LL | V1, more training data LL | Selected LL | Change vs published V1 |",
        "|---|---:|---:|---:|---:|---:|"]
    for year,t in tests.items():
        m=t["models"]; c=m["challenger"]["logloss"]; v=m["published_v1"]["logloss"]
        lines.append(f"| {year} | {m['original_stern']['logloss']:.6f} | {v:.6f} | {m['expanded_v1']['logloss']:.6f} | {c:.6f} | {(c/v-1)*100:+.2f}% |")
    lines += ["", "| Season | Published V1 Brier | Selected Brier | Published V1 late LL | Selected late LL | Games / states |",
              "|---|---:|---:|---:|---:|---:|"]
    for year,t in tests.items():
        p=t['models']['published_v1']; c=t['models']['challenger']
        lines.append(f"| {year} | {p['brier']:.6f} | {c['brier']:.6f} | {p['late_logloss']:.6f} | {c['late_logloss']:.6f} | {t['games']} / {t['states']:,} |")
    lines += ["", "Late means 3–15 minutes remaining within the admitted sample. The last three minutes and overtime remain excluded.", "",
              "## Does the gain survive clustered uncertainty?", "",
              "Entries below are selected-minus-control log loss. Negative favors the challenger. Intervals use 5,000",
              "paired bootstrap replicates; week resampling keeps games within each season-week together. These intervals",
              "are descriptive, do not correct for the project's repeated research, and are not prospective proof.", "",
              "| Season | Control | Mean change | Game-bootstrap 95% interval | Week-cluster 95% interval |",
              "|---|---|---:|---:|---:|"]
    for year,t in tests.items():
        for baseline in ['published_v1','expanded_v1','original_stern']:
            b=t['paired_contrasts']['challenger_minus_'+baseline]
            lines.append(f"| {year} | {baseline} | {b['mean']:+.6f} | [{b['ci95'][0]:+.6f}, {b['ci95'][1]:+.6f}] | [{b['week_cluster_ci95'][0]:+.6f}, {b['week_cluster_ci95'][1]:+.6f}] |")
    lines += ["", "The larger-data V1 control separates a model change from the benefit of additional training seasons.",
              "An interval crossing zero leaves the direction uncertain for that comparison, even if its point estimate improves.", "",
              "## Selection, fixed before evaluation", "",
              f"Candidate training used 2016–2021: {selection['train_games']:,} games and {selection['train_states']:,} states.",
              f"Selection used only 2022: {selection['selection_games']:,} games and {selection['selection_states']:,} states.",
              f"The chosen specification was refitted on 2016–2022 ({result['training_games']:,} games; {result['training_states']:,} states)",
              "and saved before loading evaluation outcomes. No test-driven ensemble or subsequent parameter change was made.", "",
              "| Candidate | 2022 log loss | 2022 Brier | Selected |", "|---|---:|---:|---|"]
    for s in sorted(selection['candidates'],key=lambda x:x['logloss']):
        lines.append(f"| {s['name']} | {s['logloss']:.6f} | {s['brier']:.6f} | {'Yes' if s['name']==selection['selected'] else ''} |")
    lines += ["", "Selection minimized equal-game log loss; ties within 0.00001 favored lower complexity. All nine development models",
              "and scores are preserved. The larger-data V1 was eligible to win. The 2023/2024 seasons were examined in round one;",
              "2025 outcomes and original repository summaries had also been seen. These are chronological evaluation seasons,",
              "not a fresh sealed holdout at the project level.", "", "## What changed mathematically", "",
              "The clock candidate replaces constant score/strength coefficients with six smooth-in-log-time basis weights.",
              "The residual candidate starts from Stern's fitted log odds and learns state-dependent corrections with small trees.",
              "Its final prediction averages the original view with the complement of the mirrored team view, enforcing symmetry.",
              "The residual features add half-clock and pregame total to possession, field position, down, distance and timeouts.",
              "The selected model and all rejected alternatives are distinguished in the table above.", "",
              "These are engineering adaptations, not claims that state-aware forecasts or residual boosting are new inventions.",
              "The clock model is a terminal probability model; it is not automatically a coherent diffusion process.",
              "See `ROUND2_MODEL_SPEC.md` for equations, exact features, priors, clipping and timing qualifications.", "",
              "## Engineering checks and artifacts", ""]
    e=result['engineering']
    lines += [f"JSON reload prediction error: {e['json_roundtrip_max_error']:.3g}. Team-swap complement error: {e['team_swap_max_error']:.3g}.",
              f"Single-state inference: median {e['single_state_median_ms']:.2f} ms; observed p95 {e['single_state_p95_ms']:.2f} ms over {e['timing_repeats']} calls",
              "in this environment. This measures local Python inference only; it excludes feed and exchange latency.", "",
              "Fifteen unit checks pass, covering baseline reduction, clock monotonicity, symmetry, serialized trees,",
              "outcome-label exclusion, invalid inputs, diffusion integration, market transport and research gates.", "",
              "- `results/round2/model.json`: selected fitted research model.",
              "- `results/round2/expanded_v1.json`: same-training-data control.",
              "- `results/round2/selection.json`: all development comparisons.",
              "- `results/round2/forecast_results.json`: full scores, calibration bins, intervals, timing and source hashes.",
              "- `results/round2/predictions_*.csv`: forecasts and loss rows with game/play identifiers.",
              "- `stern_round2.py`, `run_round2.py`: inference and reproducible experimental runner.", "",
              "## Additional improvement: explicit settlement uncertainty", "",
              "`settlement.py` adds an explicit home-win/away-win/tie payoff converter and conservative payout bounds.",
              "Given conditional non-tie home-win probability q, tie probability t and the contract's tie payout s,",
              "the home contract's expected payout is `(1-t)*q + t*s`. The away contract uses `(1-q)` instead.",
              "The function requires s explicitly. Bounds are calculated over supplied q and t intervals; it does not",
              "invent a fitted tie estimate or confidence interval. For example, q in [0.61,0.72], t in [0,0.04],",
              "and s=0.50 imply a home payout range [0.6056,0.7200]. These example inputs are hypothetical.",
              "The lower endpoint can enter the existing cost gate as a conservative payout input, with model admission",
              "still required. This fixes the target conversion; it does not supply the missing tie/endgame forecaster.", "",
              "## What this establishes and what it leaves open", "",
              "The experiment measures historical home-win forecasting on games that did not end tied. Retrospectively excluding",
              "ties changes the target; these probabilities are not unconditional contract expected payouts. Pregame spread/total",
              "are untimestamped historical proxies, and archived play states do not establish live receipt times. No fee,",
              "slippage, queue priority or execution profit is inferred from the forecasting scores.", "",
              "For Kalshi, the next informative experiment is an event-aligned replay: preserve the pre-event market anchor,",
              "compute the model's odds update after the state actually arrives, and compare it with the executable book after",
              "measured delay. Fit anchor reliability on earlier data and compare against a market-only control. The first-round",
              "anchor function remains a hypothesis; this round does not validate it. A separate tie/endgame/OT model is needed",
              "before broadening the domain. The verified tie-settlement correction and repository audit remain applicable below.", "",
              "Public data: [nflverse play-by-play releases](https://github.com/nflverse/nflverse-data/releases/tag/pbp).",
              "The original model reference is [Stern (1994)](https://www.stat.berkeley.edu/~aldous/157/Papers/stern.pdf).", ""]
    report='\n'.join(lines)
    (root/'ROUND2_RESULTS.md').write_text(report)
    old=root/'ROUND1_MEMO.md'
    if not old.exists():old.write_text((root/'Stern_Kalshi_Research_Memo.md').read_text())
    (root/'Stern_Kalshi_Research_Memo.md').write_text(report+'\n---\n\n# Preserved first-round research and repository audit\n\n'+old.read_text())


if __name__ == '__main__':main()
