"""Part (a) orchestrator. Writes aggregate results_a files. No per-fill dump."""

import json
import math
from pathlib import Path

from dev_pipeline.load import load_dev
from dev_pipeline.lots import reconstruct
from dev_pipeline.markouts import (
    PRIMARY_H,
    aggregate,
    bootstrap_delta,
    ci_excludes_zero,
    order_fee_per_contract,
    quote_index,
    score_portions,
)
from dev_pipeline.terciles import (
    PINNED_BUCKET_SHA,
    PINNED_C1,
    PINNED_C2,
    PINNED_E1,
    PINNED_E2,
    bucket_document,
    flow_terciles,
    index_trades,
    portion_labels,
)
from shared.canonical import canon_bytes, canon_sha256, q4, q6
from shared.fees import FEE_LABEL, read_kxnflgame_multiplier
from shared.exceptions import LabelDependentToGateRefused

LAB = Path(__file__).resolve().parents[1]
RESULTS = LAB / "results_a"
TAGS = [
    "DEV_GRADE_REUSED_31_GAME_COHORT",
    "HYPOTHETICAL_REPLAY_FILLS",
    "IN_SAMPLE_DEV",
]
MAKER_NO_SHARE_PIN = 0.989706
UCH_PIN = 603262.7291176913
TAKER_YES_PIN = 0.9168821893496498
N_PORTIONS_PIN = 6161
CONTRACT_PINS = {
    "maker_no": 321622.45,
    "maker_yes": 3345.33,
    "maker": 324967.78,
    "taker": 2068.66,
}


def _round_cell(cell):
    out = {
        "tercile": cell["tercile"],
        "n_opening_portions": cell["n_opening_portions"],
        "opening_contracts": q6(cell["opening_contracts"]),
        "opening_contract_share": q6(cell["opening_contract_share"]),
        "maker_no_share_of_opening_contracts": q6(cell["maker_no_share_of_opening_contracts"]),
        "distinct_games": cell["distinct_games"],
        "uch_contract_hours": q4(cell["uch_contract_hours"]),
        "uch_share": q6(cell["uch_share"]),
        "fee_label": FEE_LABEL,
        "horizons": {},
        "tags": list(TAGS),
    }
    if "event" in cell:
        out["event"] = cell["event"]
    for key, block in cell["horizons"].items():
        rounded = {}
        for name, value in block.items():
            if name in ("n", "censored_n", "fee_label", "net_is_headline", "examiner_pin_account_class"):
                rounded[name] = value
            elif name == "censored_contracts":
                rounded[name] = q6(value)
            else:
                rounded[name] = q6(value)
        out["horizons"][key] = rounded
    return out


def _counts(labels, key):
    found = {"T1_LOW": 0, "T2_MID": 0, "T3_HIGH": 0, "UNCLASSIFIED": 0}
    for row in labels:
        found[row[key]] += 1
    return found


def structural_gate(dev, built, lots, bucket_sha):
    fills = dev["fills"]
    maker_no = math.fsum(row["size"] for row in fills if row["kind"] == "maker" and row["outcome"] == "no")
    maker_yes = math.fsum(row["size"] for row in fills if row["kind"] == "maker" and row["outcome"] == "yes")
    taker = math.fsum(row["size"] for row in fills if row["kind"] == "taker")
    maker = maker_no + maker_yes
    share = maker_no / maker
    taker_yes = dev["yes_contracts"] / dev["all_contracts"]
    failures = []
    if abs(share - MAKER_NO_SHARE_PIN) > 1e-6:
        failures.append("maker_no_share")
    if abs(taker_yes - 0.916882) > 1e-6 or abs(taker_yes - TAKER_YES_PIN) > 1e-12:
        failures.append("taker_yes_share")
    if dev["n_trade"] != 681732 or dev["n_quote"] != 364988:
        failures.append("tape_counts")
    if len(dev["markets"]) != 62 or len(dev["weeks"]) != 31 or len(fills) != 12853:
        failures.append("row_counts")
    if any(abs(got - pin) > 0.01 for got, pin in (
        (maker_no, CONTRACT_PINS["maker_no"]),
        (maker_yes, CONTRACT_PINS["maker_yes"]),
        (maker, CONTRACT_PINS["maker"]),
        (taker, CONTRACT_PINS["taker"]),
    )):
        failures.append("contract_sums")
    if abs(lots["uch_integral"] - UCH_PIN) > 0.01 or abs(lots["uch_fifo"] - UCH_PIN) > 0.01:
        failures.append("uch")
    if abs(lots["uch_integral"] - lots["uch_fifo"]) > 1e-6:
        failures.append("uch_identity")
    if lots["n_portions"] != N_PORTIONS_PIN:
        failures.append("n_portions")
    if any(portion["kind"] != "maker" for portion in lots["portions"]):
        failures.append("taker_portion")
    if lots["residual_contracts"] > 1e-6:
        failures.append("residual")
    if abs(built["c1"] - PINNED_C1) > 1e-12 or abs(built["c2"] - PINNED_C2) > 1e-12:
        failures.append("primary_cuts")
    if abs(built["e1"] - PINNED_E1) > 1e-12 or abs(built["e2"] - PINNED_E2) > 1e-12:
        failures.append("event_cuts")
    if bucket_sha != PINNED_BUCKET_SHA:
        failures.append("bucket_sha")
    opening = math.fsum(portion["size_open"] for portion in lots["portions"])
    closing = math.fsum(sliver["size"] for portion in lots["portions"] for sliver in portion["closes"])
    if abs(opening - 163518.22) > 0.01 or abs(closing - opening) > 0.01:
        failures.append("opening_contracts")
    return {
        "ok": not failures,
        "failures": failures,
        "maker_no_share": maker_no / maker,
        "maker_no_contracts": maker_no,
        "maker_yes_contracts": maker_yes,
        "maker_contracts": maker,
        "taker_contracts": taker,
        "taker_yes_contract_share": taker_yes,
        "trade_rows": dev["n_trade"],
        "quote_rows": dev["n_quote"],
        "tickers": len(dev["markets"]),
        "events": len(dev["weeks"]),
        "fill_rows": len(fills),
        "uch_integral": lots["uch_integral"],
        "uch_fifo": lots["uch_fifo"],
        "n_portions": lots["n_portions"],
        "opening_contracts": opening,
        "closing_contracts": closing,
        "residual_contracts": lots["residual_contracts"],
        "pair_hold_weighted_median_seconds": dev["pair_hold_weighted_median"],
        "primary_horizon_seconds": PRIMARY_H,
        "c1": built["c1"],
        "c2": built["c2"],
        "e1": built["e1"],
        "e2": built["e2"],
    }


def _bucket_counts(built):
    found = {"T1_LOW": 0, "T2_MID": 0, "T3_HIGH": 0, "UNCLASSIFIED": 0}
    for row in built["rows"]:
        found[row["tercile"]] += 1
    return found


def _event_counts(built):
    found = {"T1_LOW": 0, "T2_MID": 0, "T3_HIGH": 0, "UNCLASSIFIED": 0}
    for label in built["event_tercile"].values():
        found[label] += 1
    return found


def decide_verdict(gate, primary_cells, boot):
    reasons = []
    if not gate["ok"]:
        reasons.append("K1_R36")
    by_name = {cell["tercile"]: cell for cell in primary_cells}
    unclass = by_name["UNCLASSIFIED"]["opening_contracts"]
    total = math.fsum(cell["opening_contracts"] for cell in primary_cells)
    if total and unclass / total > 0.20:
        reasons.append("UNCLASSIFIED")
    for name in ("T1_LOW", "T3_HIGH"):
        cell = by_name[name]
        opening = cell["opening_contracts"]
        censored = cell["horizons"]["1800"]["censored_contracts"]
        if opening and censored / opening > 0.20:
            reasons.append("censor_" + name)
        if cell["distinct_games"] < 5:
            reasons.append("games_" + name)
    if boot["dropped_share"] is not None and boot["dropped_share"] > 0.05:
        reasons.append("bootstrap_dropped")
    if reasons:
        return "INCONCLUSIVE", reasons
    if ci_excludes_zero(boot["ci95_gross"]):
        return "ITERATE", []
    return "DESCRIPTIVE", []


def refuse_becker_value(value, provenance):
    """Part (b) numbers cannot move the part (a) verdict."""
    if provenance in ("BECKER_A", "SYNTHETIC_NOT_BECKER"):
        raise LabelDependentToGateRefused(provenance)
    return value


def run_part_a(out_dir=None):
    dev = load_dev()
    multiplier = read_kxnflgame_multiplier(dev["fee_schedule_text"])
    built = flow_terciles(dev["flow"])
    document = bucket_document(built)
    bucket_sha = canon_sha256(document)
    lots = reconstruct(dev["fills"], dev["markets"])
    gate = structural_gate(dev, built, lots, bucket_sha)
    labels = portion_labels(lots["portions"], built, index_trades(dev["flow"]))
    index = quote_index(dev["quotes"], dev["last_at"])
    fees = order_fee_per_contract(dev["fills"], multiplier)
    scored = score_portions(lots["portions"], index, fees)
    units = {}
    raw_primary = None
    for unit_name, key in (
        ("primary_ticker_hour", "primary"),
        ("secondary_event", "secondary"),
        ("sensitivity_trailing_60min", "sensitivity"),
    ):
        agg = aggregate(scored, labels, key)
        units[unit_name] = {
            "cells": [_round_cell(cell) for cell in agg["cells"]],
            "per_game": [_round_cell(cell) for cell in agg["per_game"]],
            "tags": list(TAGS),
            "descriptive_only": unit_name != "primary_ticker_hour",
        }
        if unit_name == "primary_ticker_hour":
            raw_primary = agg["cells"]
    boot = bootstrap_delta(scored, labels, dev["games"])
    # Verdict uses unrounded primary cells and the unrounded interval.
    verdict, reasons = decide_verdict(gate, raw_primary, boot)
    boot_out = {
        "b": boot["b"],
        "seed": boot["seed"],
        "dropped": boot["dropped"],
        "dropped_share": q6(boot["dropped_share"]),
        "n_used": boot["n_used"],
        "delta_star_a_gross": q6(boot["delta_gross"]),
        "delta_star_a_net": q6(boot["delta_net"]),
        "ci95_gross": None if boot["ci95_gross"] is None else [q6(v) for v in boot["ci95_gross"]],
        "ci95_net": None if boot["ci95_net"] is None else [q6(v) for v in boot["ci95_net"]],
        "fee_label": FEE_LABEL,
        "net_is_headline": False,
        "gross_is_headline": True,
        "ci_method": "type-7 percentile at 0.025 and 0.975",
        "cluster": "game",
        "tags": list(TAGS),
    }
    # Recompute the exclude-zero decision on the same raw interval the verdict used.
    boot_out["ci_excludes_zero_gross"] = ci_excludes_zero(boot["ci95_gross"])
    constancy = canon_sha256({
        "bucket_terciles_sha256": bucket_sha,
        "portion_terciles_sha256": canon_sha256(labels),
        "tercile_cuts_sha256": canon_sha256({
            "c1": built["c1"], "c2": built["c2"], "e1": built["e1"], "e2": built["e2"],
        }),
    })
    terciles = {
        "experiment_id": "EXT-K2-OPTIMISM-TAX-DEPENDENCE-STRESS",
        "tags": list(TAGS),
        "fee_label": FEE_LABEL,
        "c1": built["c1"],
        "c2": built["c2"],
        "e1": built["e1"],
        "e2": built["e2"],
        "bucket_counts": _bucket_counts(built),
        "event_counts": _event_counts(built),
        "n_buckets_total": len(built["rows"]),
        "n_buckets_eligible": built["n_eligible"],
        "bucket_table_sha256": bucket_sha,
        "bucket_table_matches_pin": bucket_sha == PINNED_BUCKET_SHA,
        "portion_assignment_counts": {
            "primary": _counts(labels, "primary"),
            "secondary": _counts(labels, "secondary"),
            "sensitivity": _counts(labels, "sensitivity"),
        },
        "constancy_sha256": constancy,
        "results": None,
        "pnl": None,
        "roi": None,
    }
    structural = {
        "experiment_id": "EXT-K2-OPTIMISM-TAX-DEPENDENCE-STRESS",
        "tags": list(TAGS),
        "gate": {
            key: (
                q4(value) if key in ("uch_integral", "uch_fifo") and isinstance(value, float)
                else q6(value) if isinstance(value, float)
                else value
            )
            for key, value in gate.items()
        },
        "results": None,
        "pnl": None,
        "roi": None,
    }
    markouts = {
        "experiment_id": "EXT-K2-OPTIMISM-TAX-DEPENDENCE-STRESS",
        "tags": list(TAGS),
        "fee_label": FEE_LABEL,
        "examiner_pin_account_class": None,
        "gross_is_headline": True,
        "primary_horizon_seconds": PRIMARY_H,
        "units": units,
        "primary_contrast": boot_out,
        "verdict": verdict,
        "verdict_reasons": reasons,
        "counts_toward_keep": False,
        "promote": False,
        "feeds_gate": False,
        "results": None,
        "pnl": None,
        "roi": None,
        "note": "Static attribution of recorded open legs. Not a retune and not a gate.",
    }
    uch = {
        "experiment_id": "EXT-K2-OPTIMISM-TAX-DEPENDENCE-STRESS",
        "tags": list(TAGS),
        "uch_integral_contract_hours": q4(lots["uch_integral"]),
        "uch_fifo_contract_hours": q4(lots["uch_fifo"]),
        "by_primary_tercile": [
            {
                "tercile": cell["tercile"],
                "uch_contract_hours": cell["uch_contract_hours"],
                "uch_share": cell["uch_share"],
                "opening_contracts": cell["opening_contracts"],
            }
            for cell in units["primary_ticker_hour"]["cells"]
        ],
        "results": None,
        "pnl": None,
        "roi": None,
    }
    empty = {
        "experiment_id": "EXT-K2-OPTIMISM-TAX-DEPENDENCE-STRESS",
        "status": "PART_A_RUN",
        "results": None,
        "pnl": None,
        "roi": None,
        "part_a": {
            "markouts_by_tercile": "results_a/MARKOUTS_BY_TERCILE.json",
            "uch_by_tercile": "results_a/UCH_BY_TERCILE.json",
            "primary_contrast_delta_star_a": boot_out["delta_star_a_gross"],
            "verdict": verdict,
        },
        "part_b": {
            "taker_yes_share_by_week": None,
            "taker_yes_share_by_band": None,
            "maker_no_excess_gross_by_week": None,
            "maker_no_excess_net_by_week": None,
            "maker_no_excess_by_band": None,
            "dispersion": None,
            "verdict": None,
            "box_only_output_sha256": None,
        },
        "verdict": verdict,
        "counts_toward_keep": False,
        "promote": False,
        "feeds_gate": False,
        "examiner_pin_account_class": None,
        "fee_label": FEE_LABEL,
        "tags": list(TAGS),
    }
    payload = {
        "structural": structural,
        "terciles": terciles,
        "markouts": markouts,
        "uch": uch,
        "empty": empty,
        "constancy_sha256": constancy,
        "verdict": verdict,
        "built": built,
        "labels": labels,
        "bucket_document_sha256": bucket_sha,
    }
    if out_dir is not None:
        out = Path(out_dir)
        out.mkdir(parents=True, exist_ok=True)
        mapping = {
            "STRUCTURAL.json": structural,
            "TERCILES.json": terciles,
            "MARKOUTS_BY_TERCILE.json": markouts,
            "UCH_BY_TERCILE.json": uch,
            "EMPTY_RESULTS.json": empty,
        }
        for name, doc in mapping.items():
            (out / name).write_bytes(canon_bytes(doc))
        lines = [
            "# EXT-K2 part (a) dev-tape measurement",
            "",
            "Tags: " + ", ".join(TAGS) + ".",
            "Fee label: " + FEE_LABEL + ". Gross is the headline. Account class is unpinned.",
            "Verdict: " + verdict + ".",
            "Reasons: " + (", ".join(reasons) if reasons else "none") + ".",
            "Primary contrast is contract-weighted gross MO at 1800 seconds, T3 minus T1.",
            "delta_star_a_gross: " + str(boot_out["delta_star_a_gross"]),
            "ci95_gross: " + str(boot_out["ci95_gross"]),
            "delta_star_a_net: " + str(boot_out["delta_star_a_net"]) + " (CACHE_NOT_R1P1, not the headline)",
            "Constancy sha256: " + constancy,
            "Bucket table sha256: " + bucket_sha,
            "results, pnl, and roi are null.",
            "Part (b) was not run. No Becker number is in this file.",
            "",
        ]
        (out / "UNIT_RESULTS.md").write_text("\n".join(lines), encoding="utf-8")
    return payload


def main():
    payload = run_part_a(RESULTS)
    print(payload["verdict"])
    print(payload["constancy_sha256"])


if __name__ == "__main__":
    main()
