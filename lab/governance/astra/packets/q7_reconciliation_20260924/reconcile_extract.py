#!/usr/bin/env python3
"""Read-only extractor for the Q7 reconciliation memo.

Reads git objects for two pinned commits and writes JSON to stdout.
Does not modify the work tree, does not retune, and does not open a network
connection. Absent blobs are reported as NOT_FOUND. Stored pin hashes are
copied from pin files and are not treated as recomputed digests.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys

MAIN = "34a2720218b4f4f2d6dd0cbde6334ee672a3684b"
REVIEWED = "a281adc944e4dacffcdb5677a140fabaed675a81"
BRANCH = "01c726ae9244d801d359e00df67d6a71f4012669"

STRESSES = ("q3300_d0.25", "q3300_d5", "q10000_d0.25", "q10000_d5")
BRANCH_ARMS = ("router_off", "router_on", "allocator_off", "allocator_on")
MAIN_ARMS = ("A", "B", "C", "D")

MAIN_PRESENT = [
    "nfl_paircheck_lab_20260922/paircheck_policy.py",
    "nfl_paircheck_lab_20260922/EXPERIMENT_SPEC.md",
    "nfl_paircheck_lab_20260922/FROZEN_EXPERIMENT.json",
    "nfl_paircheck_lab_20260922/README.md",
    "nfl_paircheck_lab_20260922/run_experiment.py",
    "nfl_paircheck_lab_20260922/analyze.py",
    "nfl_paircheck_lab_20260922/results/NOT_RUN.json",
    "nfl_paircheck_lab_20260922/results/analysis_status.json",
    "nfl_paircheck_lab_20260922/results/verification.json",
    "nfl_q7_rehab_p1_cadence_20260923/cadence_policy.py",
    "nfl_q7_rehab_p1_cadence_20260923/EXPERIMENT_SPEC.md",
    "nfl_q7_rehab_p1_cadence_20260923/FROZEN_EXPERIMENT.json",
    "nfl_q7_rehab_p1_cadence_20260923/results/NOT_RUN.json",
    "nfl_q7_rehab_p1_cadence_20260923/results/UNIT_RESULTS.md",
    "nfl_q7_rehab_p2_rank_sizing_20260923/rank_sizing_policy.py",
    "nfl_q7_rehab_p2_rank_sizing_20260923/EXPERIMENT_SPEC.md",
    "nfl_q7_rehab_p2_rank_sizing_20260923/FROZEN_EXPERIMENT.json",
    "nfl_q7_rehab_p2_rank_sizing_20260923/selection.py",
    "nfl_q7_rehab_p2_rank_sizing_20260923/results/NOT_RUN.json",
    "nfl_q7_rehab_p2_rank_sizing_20260923/results/UNIT_RESULTS.md",
    "packets/refiner/CONDUCTOR_ACCEPT_Q7_B_REHAB_P1_CADENCE_600_2026-09-23.json",
    "packets/refiner/CONDUCTOR_DECISION_Q7_B_P1_PARENT_LEDGERS_2026-09-23.json",
    "packets/refiner/PARENT_Q7_BD_LEDGER_SOURCE_PINS_2026-09-23.json",
    "packets/refiner/REFINER_HAND_SIMULATOR_Q7_B_PASS2_RANK_SIZING_2026-09-23.json",
    "packets/refiner/REFINER_PASS1_DIAGNOSIS_Q7_ARM_B_2026-09-23.md",
    "packets/refiner/REFINER_PASS1_FREEZE_Q7_B_CADENCE_600_2026-09-23.md",
    "packets/refiner/REFINER_PASS2_DIAGNOSIS_Q7_ARM_B_2026-09-23.md",
    "packets/refiner/REFINER_PASS2_FREEZE_Q7_B_PORTFOLIO_RANK_SIZING_2026-09-23.md",
    "nfl_factorial_lab_20260921/adaptive_policy.py",
    "nfl_factorial_lab_20260921/factorial_policy.py",
    "nfl_factorial_lab_20260921/queue_policies.py",
    "nfl_factorial_lab_20260921/replay_v2.py",
    "nfl_factorial_lab_20260921/inputs/manifest.json",
    "nfl_factorial_lab_20260921/inputs/markets.json",
    "nfl_factorial_lab_20260921/inputs/week_membership.json",
    "kalshi_capital_structure_lab_20260922/FROZEN_EXPERIMENT.json",
    "docs/EXPERIMENT_REGISTRY.md",
]

BRANCH_PRESENT = [
    "nfl_pair_price_lab_20260921/pair_policy.py",
    "nfl_pair_price_lab_20260921/Q7_RESULTS.md",
    "nfl_pair_price_lab_20260921/EXPERIMENT_SPEC.md",
    "nfl_pair_price_lab_20260921/FROZEN_EXPERIMENT.json",
    "nfl_pair_price_lab_20260921/README.md",
    "nfl_pair_price_lab_20260921/run_experiment.py",
    "nfl_pair_price_lab_20260921/q7_analysis.py",
    "nfl_pair_price_lab_20260921/EXTERNAL_ARTIFACTS.json",
    "nfl_pair_price_lab_20260921/results/effects.json",
    "nfl_pair_price_lab_20260921/results/selection.json",
    "nfl_pair_price_lab_20260921/results/experiment_summary.json",
    "nfl_pair_price_lab_20260921/results/verification.json",
    "nfl_pair_price_lab_20260921/inputs/manifest.json",
    "nfl_pair_price_lab_20260921/inputs/markets.json",
    "nfl_pair_price_lab_20260921/inputs/week_membership.json",
    "nfl_factorial_lab_20260921/adaptive_policy.py",
    "nfl_factorial_lab_20260921/factorial_policy.py",
    "nfl_factorial_lab_20260921/queue_policies.py",
    "nfl_factorial_lab_20260921/replay_v2.py",
]
BRANCH_PRESENT += [
    f"nfl_pair_price_lab_20260921/results/{stress}_{arm}.json"
    for stress in STRESSES
    for arm in BRANCH_ARMS
]

ABSENT_CHECKS = [
    (MAIN, "nfl_factorial_lab_20260921/inputs/events.jsonl.gz"),
    (MAIN, "nfl_paircheck_lab_20260922/results/paircheck_effects.json"),
    (MAIN, "nfl_paircheck_lab_20260922/results/experiment_summary.json"),
    (BRANCH, "nfl_pair_price_lab_20260921/inputs/events.jsonl.gz"),
    (MAIN, "packets/Q7_EXAMINER_SCORECARD_2026-09-22.md"),
    (MAIN, "reports/RPT-Q7.md"),
    (MAIN, "nfl_q7_rehab_p1_cadence_20260923/results/experiment_summary.json"),
]
for stress in STRESSES:
    for arm in MAIN_ARMS:
        ABSENT_CHECKS.append((MAIN, f"nfl_paircheck_lab_20260922/results/{stress}_{arm}.json"))
    for arm in ("B", "D"):
        for suffix in ("", "_decisions.jsonl.gz", "_fills.jsonl.gz", "_orders.jsonl.gz"):
            ABSENT_CHECKS.append(
                (MAIN, f"nfl_paircheck_lab_20260922/results/{stress}_{arm}{suffix}")
            )
    for arm in BRANCH_ARMS:
        for suffix in ("_decisions.jsonl.gz", "_fills.jsonl.gz", "_orders.jsonl.gz", "_pairs.jsonl.gz"):
            ABSENT_CHECKS.append(
                (BRANCH, f"nfl_pair_price_lab_20260921/results/{stress}_{arm}{suffix}")
            )


def git_ok(rev: str, path: str) -> bool:
    proc = subprocess.run(
        ["git", "cat-file", "-e", f"{rev}:{path}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return proc.returncode == 0


def git_bytes(rev: str, path: str) -> bytes | None:
    if not git_ok(rev, path):
        return None
    return subprocess.check_output(["git", "show", f"{rev}:{path}"])


def blob(rev: str, path: str) -> dict:
    data = git_bytes(rev, path)
    if data is None:
        return {
            "path": path,
            "commit": rev,
            "present": False,
            "recomputed_sha256": "NOT_FOUND",
            "bytes": "NOT_FOUND",
        }
    return {
        "path": path,
        "commit": rev,
        "present": True,
        "recomputed_sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data),
    }


def load_json(rev: str, path: str):
    data = git_bytes(rev, path)
    if data is None:
        return None
    return json.loads(data)


def money(value) -> str:
    """Same display helper as nfl_pair_price_lab_20260921/q7_analysis.py money()."""
    if value is None:
        return "Unresolved"
    return f"${value:+,.2f}"


def scenario_row(doc: dict) -> dict:
    metrics = doc.get("metrics") or {}
    return {
        "scenario": doc.get("scenario"),
        "arm": doc.get("arm"),
        "completed_strategy_pnl": doc.get("completed_strategy_pnl"),
        "unresolved_contracts": doc.get("unresolved_contracts"),
        "all_flat": doc.get("all_flat"),
        "fees": metrics.get("fees", "NOT_FOUND"),
        "fills": doc.get("fills"),
        "maker_contracts": doc.get("maker_contracts"),
        "taker_contracts": doc.get("taker_contracts"),
        "completed_window_games": doc.get("completed_window_games"),
        "decision_records": doc.get("decision_records"),
        "per_game_count": len(doc.get("per_game") or []),
        "fills_field_type": type(doc.get("fills")).__name__,
        "config": doc.get("config"),
    }


def ancestor(older: str, newer: str) -> bool:
    proc = subprocess.run(
        ["git", "merge-base", "--is-ancestor", older, newer],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return proc.returncode == 0


def path_diff(older: str, newer: str) -> list[str]:
    out = subprocess.check_output(
        ["git", "diff", "--name-only", older, newer], text=True
    )
    names = [line for line in out.splitlines() if line]
    needles = ("q7", "Q7", "paircheck", "pair_price", "refiner", "nfl_factorial")
    return [name for name in names if any(n in name for n in needles)]


def full_diff_count(older: str, newer: str) -> int:
    out = subprocess.check_output(
        ["git", "diff", "--name-only", older, newer], text=True
    )
    return len([line for line in out.splitlines() if line])


def main() -> int:
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    origin_main = subprocess.check_output(
        ["git", "rev-parse", "origin/main"], text=True
    ).strip()
    files = [blob(MAIN, path) for path in MAIN_PRESENT]
    files += [blob(BRANCH, path) for path in BRANCH_PRESENT]

    absent = []
    for rev, path in ABSENT_CHECKS:
        if git_ok(rev, path):
            absent.append({"commit": rev, "path": path, "status": "PRESENT_UNEXPECTED"})
        else:
            absent.append({"commit": rev, "path": path, "status": "NOT_FOUND"})

    effects = load_json(BRANCH, "nfl_pair_price_lab_20260921/results/effects.json")
    selection = load_json(BRANCH, "nfl_pair_price_lab_20260921/results/selection.json")
    summary = load_json(BRANCH, "nfl_pair_price_lab_20260921/results/experiment_summary.json")
    verification = load_json(BRANCH, "nfl_pair_price_lab_20260921/results/verification.json")
    results_md = git_bytes(BRANCH, "nfl_pair_price_lab_20260921/Q7_RESULTS.md").decode()
    external = load_json(BRANCH, "nfl_pair_price_lab_20260921/EXTERNAL_ARTIFACTS.json")
    pins = load_json(MAIN, "packets/refiner/PARENT_Q7_BD_LEDGER_SOURCE_PINS_2026-09-23.json")
    diagnosis1 = git_bytes(
        MAIN, "packets/refiner/REFINER_PASS1_DIAGNOSIS_Q7_ARM_B_2026-09-23.md"
    ).decode()
    diagnosis2 = git_bytes(
        MAIN, "packets/refiner/REFINER_PASS2_DIAGNOSIS_Q7_ARM_B_2026-09-23.md"
    ).decode()
    manifest = load_json(BRANCH, "nfl_pair_price_lab_20260921/inputs/manifest.json")
    main_manifest = load_json(MAIN, "nfl_factorial_lab_20260921/inputs/manifest.json")
    weeks = load_json(BRANCH, "nfl_pair_price_lab_20260921/inputs/week_membership.json")
    not_run = load_json(MAIN, "nfl_paircheck_lab_20260922/results/NOT_RUN.json")
    rehab1 = load_json(MAIN, "nfl_q7_rehab_p1_cadence_20260923/results/NOT_RUN.json")
    rehab2 = load_json(MAIN, "nfl_q7_rehab_p2_rank_sizing_20260923/results/NOT_RUN.json")
    cap = load_json(MAIN, "kalshi_capital_structure_lab_20260922/FROZEN_EXPERIMENT.json")

    scenarios = []
    summary_match = []
    for stress in STRESSES:
        for arm in BRANCH_ARMS:
            path = f"nfl_pair_price_lab_20260921/results/{stress}_{arm}.json"
            doc = load_json(BRANCH, path)
            row = scenario_row(doc)
            row["path"] = path
            row["commit"] = BRANCH
            standalone = doc.get("completed_strategy_pnl")
            embedded = summary["scenarios"][f"{stress}_{arm}"]["completed_strategy_pnl"]
            row["matches_experiment_summary_completed_strategy_pnl"] = standalone == embedded
            summary_match.append(row["matches_experiment_summary_completed_strategy_pnl"])
            scenarios.append(row)

    recomputed = []
    for stress in STRESSES:
        by_arm = {
            row["arm"]: row
            for row in scenarios
            if row["scenario"] == f"{stress}_{row['arm']}"
        }
        on = by_arm["router_on"]["completed_strategy_pnl"]
        off = by_arm["router_off"]["completed_strategy_pnl"]
        alloc_on = by_arm["allocator_on"]["completed_strategy_pnl"]
        alloc_off = by_arm["allocator_off"]["completed_strategy_pnl"]
        gap = on - off
        stored_gap = effects[stress]["guard_effect_router"]
        ratio = on / alloc_on
        recomputed.append(
            {
                "stress": stress,
                "formula_router_gap": "completed_strategy_pnl(router_on) - completed_strategy_pnl(router_off)",
                "router_on": on,
                "router_off": off,
                "recomputed_router_gap": gap,
                "stored_effects_guard_effect_router": stored_gap,
                "router_gap_matches_effects_json": gap == stored_gap,
                "formula_router_retention_vs_allocator_on": "completed_strategy_pnl(router_on) / completed_strategy_pnl(allocator_on)",
                "allocator_on": alloc_on,
                "recomputed_router_on_over_allocator_on": ratio,
                "router_on_ge_95pct_allocator_on": on >= 0.95 * alloc_on,
                "stored_selection_retains_allocator": selection["checks"][f"{stress}_retains_allocator"],
                "retention_check_matches_selection_json": (on >= 0.95 * alloc_on)
                == selection["checks"][f"{stress}_retains_allocator"],
                "formula_allocator_gap": "completed_strategy_pnl(allocator_on) - completed_strategy_pnl(allocator_off)",
                "recomputed_allocator_gap": alloc_on - alloc_off,
                "stored_effects_guard_effect_allocator": effects[stress]["guard_effect_allocator"],
                "allocator_gap_matches_effects_json": (alloc_on - alloc_off)
                == effects[stress]["guard_effect_allocator"],
                "displayed_router_on": money(on),
                "displayed_router_off": money(off),
                "displayed_router_gap": money(gap),
            }
        )

    headline_cells = {}
    first_table = results_md.split("## Within-simulator contrasts", 1)[0]
    for line in first_table.splitlines():
        if line.startswith("| router_") or line.startswith("| allocator_"):
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            headline_cells[cells[0]] = cells[1:]
    display_match = []
    for item in recomputed:
        idx = STRESSES.index(item["stress"])
        display_match.append(
            {
                "stress": item["stress"],
                "q7_results_router_on": headline_cells["router_on"][idx],
                "recomputed_display_router_on": item["displayed_router_on"],
                "router_on_display_matches": headline_cells["router_on"][idx]
                == item["displayed_router_on"],
                "q7_results_router_off": headline_cells["router_off"][idx],
                "recomputed_display_router_off": item["displayed_router_off"],
                "router_off_display_matches": headline_cells["router_off"][idx]
                == item["displayed_router_off"],
                "q7_results_router_gap_line": None,
            }
        )
    gap_cells = {}
    capture = False
    for line in results_md.splitlines():
        if line.startswith("| Scenario |"):
            capture = True
            continue
        if capture and line.startswith("| q"):
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            gap_cells[cells[0]] = cells[1]
        elif capture and line.startswith("|---"):
            continue
        elif capture and not line.startswith("|"):
            break
    for item in display_match:
        stored = gap_cells[item["stress"]]
        recomputed_display = next(
            row["displayed_router_gap"] for row in recomputed if row["stress"] == item["stress"]
        )
        item["q7_results_router_gap"] = stored
        item["recomputed_display_router_gap"] = recomputed_display
        item["router_gap_display_matches"] = stored == recomputed_display

    week_counts = {}
    for week in weeks.values():
        week_counts[week] = week_counts.get(week, 0) + 1

    verify_decisions = [
        {
            "scenario": case["scenario"],
            "fills": case["fills"],
            "orders": case["orders"],
            "decisions": case["decisions"],
            "passed": case["passed"],
        }
        for case in verification["cases"]
    ]

    external_by_path = {row["path"]: row for row in external["files"]}
    parent_artifacts = []
    for name, meta in pins["artifacts"].items():
        parent_artifacts.append(
            {
                "name": name,
                "stored_pin_sha256": meta["sha256"],
                "stored_pin_bytes": meta["bytes"],
                "recomputed_sha256": "NOT_FOUND",
                "present_in_main_commit": git_ok(
                    MAIN, f"nfl_paircheck_lab_20260922/results/{name}"
                ),
            }
        )

    seed_hits = []
    for rev, path in (
        (BRANCH, "nfl_pair_price_lab_20260921/run_experiment.py"),
        (BRANCH, "nfl_pair_price_lab_20260921/EXPERIMENT_SPEC.md"),
        (BRANCH, "nfl_pair_price_lab_20260921/FROZEN_EXPERIMENT.json"),
        (MAIN, "nfl_paircheck_lab_20260922/run_experiment.py"),
        (MAIN, "nfl_paircheck_lab_20260922/EXPERIMENT_SPEC.md"),
        (MAIN, "nfl_paircheck_lab_20260922/FROZEN_EXPERIMENT.json"),
        (MAIN, "nfl_factorial_lab_20260921/replay_v2.py"),
    ):
        text = git_bytes(rev, path).decode()
        if "seed" in text.lower():
            seed_hits.append({"commit": rev, "path": path})

    report = {
        "status": "RECONCILIATION_MEMO_READY_NOT_SCORED",
        "examiner_stamp": None,
        "pins": {
            "origin_main_HEAD": origin_main,
            "matches_pinned_main": origin_main == MAIN,
            "reviewed_main_commit": REVIEWED,
            "reviewed_main_is_ancestor_of_origin_main": ancestor(REVIEWED, MAIN),
            "q7_relevant_paths_changed_since_reviewed_main": path_diff(REVIEWED, MAIN),
            "files_changed_since_reviewed_main": full_diff_count(REVIEWED, MAIN),
            "research_commit": BRANCH,
            "extractor_HEAD_at_runtime": head,
        },
        "files": files,
        "absent_blobs": absent,
        "inputs": {
            "manifest_bytes_equal": git_bytes(MAIN, "nfl_factorial_lab_20260921/inputs/manifest.json")
            == git_bytes(BRANCH, "nfl_pair_price_lab_20260921/inputs/manifest.json"),
            "markets_bytes_equal": git_bytes(MAIN, "nfl_factorial_lab_20260921/inputs/markets.json")
            == git_bytes(BRANCH, "nfl_pair_price_lab_20260921/inputs/markets.json"),
            "week_membership_bytes_equal": git_bytes(
                MAIN, "nfl_factorial_lab_20260921/inputs/week_membership.json"
            )
            == git_bytes(BRANCH, "nfl_pair_price_lab_20260921/inputs/week_membership.json"),
            "manifest_sha256_field": manifest["sha256"],
            "main_manifest_sha256_field": main_manifest["sha256"],
            "cohort": manifest["cohort"],
            "week_counts": week_counts,
            "game_count": len(weeks),
            "events_jsonl_gz_in_either_commit": False,
            "same_declared_manifest": manifest["sha256"] == main_manifest["sha256"],
        },
        "seeds": "NOT_FOUND" if not seed_hits else seed_hits,
        "branch_scenarios": scenarios,
        "branch_summary_pnl_matches_standalone": all(summary_match),
        "branch_recomputed": recomputed,
        "branch_headline_display": display_match,
        "branch_verification_case_counts": verify_decisions,
        "branch_external_artifact_count": len(external["files"]),
        "branch_external_router_decision_pins": [
            {
                "path": path,
                "stored_pin_sha256": meta["sha256"],
                "stored_pin_bytes": meta["bytes"],
                "present_in_branch_commit": git_ok(BRANCH, path),
            }
            for path, meta in sorted(external_by_path.items())
            if path.endswith("_decisions.jsonl.gz") or path.endswith("_pairs.jsonl.gz")
        ],
        "main_in_tree_run_status": {
            "paircheck": not_run,
            "rehab_p1": rehab1,
            "rehab_p2": rehab2,
        },
        "main_parent_ledger_pins": {
            "source": "packets/refiner/PARENT_Q7_BD_LEDGER_SOURCE_PINS_2026-09-23.json",
            "commit": MAIN,
            "paircheck_effects_stored_pin": pins["paircheck_effects.json"],
            "artifacts": parent_artifacts,
            "q7_packet_pins": cap.get("q7_packet_pins"),
            "q7_checkout_observation": cap.get("q7_checkout_observation"),
        },
        "arm_crosswalk": [
            {
                "main_label": "A",
                "main_definition": "Original AdaptiveReplay baseline router, pair_check false",
                "branch_label": "router_off",
                "branch_definition": "Untouched AdaptiveReplay baseline",
                "relation": "code_path_counterpart",
                "output_equality": "NOT_SCORED_MAIN_LEDGER_ABSENT",
            },
            {
                "main_label": "B",
                "main_definition": "Original router, pair_check true, quote() gate skips a new submit when the key is blocked and no working order exists",
                "branch_label": "router_on",
                "branch_definition": "GuardedRouter.choose filters the selected set and applies bounded_quantity on inventory offsets when margin fails",
                "relation": "role_analogy_different_policy",
                "label_collision": True,
                "output_equality": "NOT_EQUIVALENT_POLICY",
            },
            {
                "main_label": "C",
                "main_definition": "Q6 allocator label 000 with the combined-cost veto removed",
                "branch_label": "allocator_off",
                "branch_definition": "PairAllocator guard false; rank_without_margin_rejection",
                "relation": "code_path_counterpart_plus_logging_difference",
                "output_equality": "NOT_SCORED_MAIN_LEDGER_ABSENT",
            },
            {
                "main_label": "D",
                "main_definition": "Untouched Q6 FactorialReplay label 000, pair_check true",
                "branch_label": "allocator_on",
                "branch_definition": "PairAllocator guard true; delegates portfolio_rank to FactorialReplay",
                "relation": "code_path_counterpart_plus_logging_difference",
                "output_equality": "NOT_SCORED_DECISION_PIN_HASHES_DIFFER_AND_BYTES_ABSENT",
            },
            {
                "main_label": "B0",
                "main_definition": "Rehab alias of Q7 Arm B",
                "branch_label": None,
                "relation": "no_branch_counterpart",
            },
            {
                "main_label": "B1",
                "main_definition": "Arm B plus 600-second new-exposure admission cadence; frozen not run",
                "branch_label": None,
                "relation": "no_branch_counterpart",
            },
            {
                "main_label": "B2",
                "main_definition": "Arm B plus portfolio_rank capital-budget sizing; frozen not run",
                "branch_label": None,
                "relation": "no_branch_counterpart",
            },
        ],
        "main_headline_0_843": {
            "stored_text_contains_0.843": "0.843" in diagnosis1,
            "stored_sentence": next(
                line.strip() for line in diagnosis1.splitlines() if "0.843" in line
            ),
            "formula_that_would_apply": "completed_strategy_pnl(B) / completed_strategy_pnl(D)",
            "primary_stress_named_by_diagnosis": "primary",
            "numerator_completed_strategy_pnl_B": "NOT_FOUND",
            "denominator_completed_strategy_pnl_D": "NOT_FOUND",
            "recomputed_ratio": "NOT_FOUND",
            "reproduces_from_ledger": False,
            "reason": "B and D scenario JSON ledgers and paircheck_effects.json are absent from the pinned main commit",
        },
        "main_pass2_approximate_prose": {
            "stored_sentence": next(
                line.strip() for line in diagnosis2.splitlines() if "B0≈291" in line or "B0" in line and "291" in line
            ),
            "recomputed_from_ledger": "NOT_FOUND",
        },
        "engine_queue_default_line": "nfl_factorial_lab_20260921/replay_v2.py:41 queue_early default 290.595",
        "q7_scenario_queues_from_branch_configs": sorted(
            {row["config"]["queue_early"] for row in scenarios}
        ),
    }
    json.dump(report, sys.stdout, indent=2, allow_nan=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
