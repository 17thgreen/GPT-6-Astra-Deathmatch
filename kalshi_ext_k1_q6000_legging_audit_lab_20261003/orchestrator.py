"""EXT-K1 measurement runner. Reads pinned bytes, writes aggregates, places no orders."""

import gzip
import io
import json
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

from artifacts import artifact_bytes
from canonical import write_json
from consensus import (
    deviation,
    join_cohort,
    p_cons_for_team,
    settlement_value,
    split_dev,
    split_fav,
)
from constants import (
    ACCEPT_CLAIMED_MANIFEST_SHA256,
    ACCEPT_SHA256,
    BUNDLE_SHA256,
    DELTA_SENSITIVITY,
    EVENTS,
    EXPERIMENT_ID,
    FEE_LABEL,
    FILL_ROWS,
    FILLS_SHA256,
    FREEZE_JSON_SHA256,
    FREEZE_MD_SHA256,
    HORIZONS_S,
    LEDGER_UCH,
    MAKER_CONTRACTS,
    MAKER_NO_CONTRACTS,
    MAKER_NO_SHARE,
    MAKER_YES_CONTRACTS,
    MANIFEST_SHA256,
    OPENING_PORTIONS,
    ORDERS_SHA256,
    PAIRED_UNITS,
    PINS_REL,
    PRIMARY_DELTA,
    PRIMARY_GATE,
    PREREG_ACCEPT_SHA256,
    PREREG_ADDENDUM_SHA256,
    QUOTE_ROWS,
    REPLAY_SHA256,
    QUEUE_POLICIES_SHA256,
    RUN_EXPERIMENT_SHA256,
    SCOUT_MAKER_NO_SHARE,
    SCOUT_TAKER_YES_SHARE,
    SUMMARY_SHA256,
    TAKER_CONTRACTS,
    TAKER_YES_SHARE,
    TICKERS,
    TRADE_ROWS,
    UNPINNED_RULES,
)
from errors import ClosedUniverseRefused, StructureDrift
from fees import (
    D,
    ceil_cent,
    direct_member_per_contract,
    fee_labels,
    headline_order_fee,
    read_kxnflgame_maker_multiplier,
)
from gate import GRID_ROLE, cell_key, is_primary, iter_cells, portion_refused
from ledger_lots import build_lots
from markouts import QuoteBook, portion_markouts, reject_lee_ready
from pins_io import LAB, manifest_map, verified_bytes, verify_all
from refusals import assert_not_holdout, screen_clock_row
from report import (
    contrast,
    decide_verdict,
    hold_time_pairs,
    per_game_split_table,
    round_reported,
    split_table,
    stamp_ex_post,
    summarize,
    uch_by_split,
    weighted_quantile,
    censored_share,
)

RESULTS = LAB / "results"
_CACHE = None


def _gzip_rows(blob):
    with gzip.GzipFile(fileobj=io.BytesIO(blob)) as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def _load_fills():
    rows = []
    for index, row in enumerate(_gzip_rows(verified_bytes(PINS_REL["fills"]))):
        screen_clock_row(row)
        row["_index"] = index
        rows.append(row)
    return rows


def _stream_tape(book):
    stats = {
        "trades": 0,
        "quotes": 0,
        "taker_yes_contracts": 0.0,
        "taker_no_contracts": 0.0,
        "taker_yes_trades": 0,
        "taker_no_trades": 0,
        "block_trades": 0,
        "tickers": set(),
        "ats": [],
    }
    for row in _gzip_rows(verified_bytes(PINS_REL["events"])):
        screen_clock_row(row)
        reject_lee_ready(key=" ".join(row.keys()))
        ticker = row.get("ticker")
        if ticker is None:
            raise ClosedUniverseRefused("tape row without ticker")
        stats["tickers"].add(ticker)
        stats["ats"].append(row["at"])
        book.note(ticker, row["at"])
        if row.get("kind") == "quote":
            book.add_quote(row)
            stats["quotes"] += 1
        else:
            if row.get("is_block_trade"):
                stats["block_trades"] += 1
            side = row.get("taker_side")
            size = row.get("size") or 0.0
            if side == "yes":
                stats["taker_yes_contracts"] += size
                stats["taker_yes_trades"] += 1
            elif side == "no":
                stats["taker_no_contracts"] += size
                stats["taker_no_trades"] += 1
            stats["trades"] += 1
    return stats


def _fill_facts(fills):
    maker_no = maker_yes = taker = 0.0
    taker_rows = maker_rows = 0
    maker_orders = set()
    max_inventory = 0.0
    for row in fills:
        size = row["size"]
        max_inventory = max(max_inventory, abs(row["inventory_after"]))
        if row["kind"] == "maker":
            maker_rows += 1
            maker_orders.add(row["order_id"])
            if row["outcome"] == "no":
                maker_no += size
            elif row["outcome"] == "yes":
                maker_yes += size
        elif row["kind"] == "taker":
            taker += size
            taker_rows += 1
    maker = maker_no + maker_yes
    return {
        "rows": len(fills),
        "maker_rows": maker_rows,
        "taker_rows": taker_rows,
        "maker_no_contracts": maker_no,
        "maker_yes_contracts": maker_yes,
        "maker_contracts": maker,
        "maker_no_share": maker_no / maker if maker else None,
        "taker_contracts": taker,
        "maker_order_ids": len(maker_orders),
        "max_abs_inventory_after": max_inventory,
    }


def _within(value, target, tolerance):
    return value is not None and abs(value - target) <= tolerance


def _structural_failures(facts, tape, lots, markets, summary_uch):
    failures = []
    share = facts["maker_no_share"]
    if not _within(share, MAKER_NO_SHARE, 1e-6):
        failures.append("maker_no_share_rederived")
    if not _within(share, SCOUT_MAKER_NO_SHARE, 0.0005):
        failures.append("maker_no_share_scout")
    yes = tape["taker_yes_contracts"]
    no = tape["taker_no_contracts"]
    taker_share = yes / (yes + no) if yes + no else None
    tape["taker_yes_contract_share"] = taker_share
    if not _within(taker_share, TAKER_YES_SHARE, 1e-6):
        failures.append("taker_yes_share_rederived")
    if not _within(taker_share, SCOUT_TAKER_YES_SHARE, 0.0005):
        failures.append("taker_yes_share_scout")
    if facts["rows"] != FILL_ROWS or tape["trades"] != TRADE_ROWS or tape["quotes"] != QUOTE_ROWS:
        failures.append("row_counts")
    if len(tape["tickers"]) != TICKERS or len(markets) != TICKERS:
        failures.append("ticker_count")
    if not _within(facts["maker_no_contracts"], MAKER_NO_CONTRACTS, 0.01):
        failures.append("maker_no_contracts")
    if not _within(facts["maker_yes_contracts"], MAKER_YES_CONTRACTS, 0.01):
        failures.append("maker_yes_contracts")
    if not _within(facts["maker_contracts"], MAKER_CONTRACTS, 0.01):
        failures.append("maker_contracts")
    if not _within(facts["taker_contracts"], TAKER_CONTRACTS, 0.01):
        failures.append("taker_contracts")
    if not _within(lots["uch_integral"], LEDGER_UCH, 0.01):
        failures.append("uch_integral")
    if not _within(lots["uch_integral"], summary_uch, 0.01):
        failures.append("uch_vs_summary")
    if abs(lots["uch_fifo"] - lots["uch_integral"]) > 1e-6:
        failures.append("uch_fifo_identity")
    if len(lots["portions"]) != OPENING_PORTIONS:
        failures.append("opening_portions")
    if lots["open_at_window_end_contracts"] != 0:
        failures.append("open_at_window_end")
    if not _within(lots["opening_contracts"], PAIRED_UNITS, 0.01):
        failures.append("opening_contracts")
    if not _within(lots["closing_contracts"], PAIRED_UNITS, 0.01):
        failures.append("closing_contracts")
    if tape["block_trades"] != 0:
        failures.append("block_trades")
    late = 0
    for ticker, meta in markets.items():
        last = tape["book_last"].get(ticker)
        if last is None or abs((meta["kickoff"] - last) / 60.0 - 174.0) > 1e-6:
            failures.append(f"last_row_{ticker}")
            break
        # Maker fills at or after K-3h are counted below.
        _ = meta
    return failures, late


def _attach_consensus(portions, games_by_event):
    for portion in portions:
        game = games_by_event[portion["event"]]
        p_prop = p_cons_for_team(game, portion["team_long"], "proportional")
        p_shin = p_cons_for_team(game, portion["team_long"], "shin")
        portion["p_cons_proportional"] = p_prop
        portion["p_cons_shin"] = p_shin
        portion["dev_proportional"] = deviation(p_prop, portion["m_open"])
        portion["dev_shin"] = deviation(p_shin, portion["m_open"])
        portion["s_dev"] = split_dev(portion["dev_proportional"], PRIMARY_DELTA)
        portion["s_fav"] = split_fav(p_prop)
        portion["s_dev_sensitivity"] = {
            f"{delta:.2f}": split_dev(portion["dev_proportional"], delta)
            for delta in DELTA_SENSITIVITY
        }


def _attach_fees(portions, fills, multiplier):
    groups = defaultdict(list)
    direct_sum = Decimal(0)
    for row in fills:
        if row["kind"] != "maker":
            continue
        groups[row["order_id"]].append((row["size"], row["price"]))
        direct_sum += D(row["fee"])
    per_contract = {}
    headline_total = Decimal(0)
    for order_id, group in groups.items():
        order_fee, fee_per_contract, _six = headline_order_fee(group, multiplier)
        per_contract[order_id] = fee_per_contract
        headline_total += order_fee
    for portion in portions:
        fee_per = per_contract[portion["order_id"]]
        portion["headline_fee_per_contract"] = float(fee_per)
        portion["direct_member_fee_per_contract"] = float(
            direct_member_per_contract(portion["ledger_fee"], portion["fill_size"])
        )
    return {
        "headline_maker_order_fee_total": float(ceil_cent(headline_total)),
        "headline_maker_order_fee_total_raw": str(ceil_cent(headline_total)),
        "maker_orders": len(groups),
        "direct_member_maker_fee_total_sensitivity": float(direct_sum),
        **fee_labels(),
    }


def _attach_markouts(portions, book, games_by_event):
    for portion in portions:
        settlement = settlement_value(games_by_event[portion["event"]], portion["team_long"])
        portion["markouts"] = portion_markouts(
            portion,
            book,
            HORIZONS_S,
            portion["headline_fee_per_contract"],
            settlement,
        )


def _maker_after_cutoff(fills, markets):
    count = 0
    for row in fills:
        if row["kind"] != "maker":
            continue
        if row["at"] >= markets[row["ticker"]]["kickoff"] - 10800:
            count += 1
    return count


def _gate_report(portions):
    total_contracts = sum(portion["size"] for portion in portions)
    total_uch = sum(portion["uch"] for portion in portions)
    cells = []
    for x, exposure_floor, devig in iter_cells():
        refused = []
        kept = []
        for portion in portions:
            if portion_refused(portion, x, exposure_floor, devig):
                refused.append(portion)
            else:
                kept.append(portion)
        refused_contracts = sum(portion["size"] for portion in refused)
        refused_uch = sum(portion["uch"] for portion in refused)
        cells.append({
            "x": x,
            "E": exposure_floor,
            "devig": devig,
            "cell": cell_key(x, exposure_floor, devig),
            "primary": is_primary(x, exposure_floor, devig),
            "role": "PRIMARY" if is_primary(x, exposure_floor, devig) else GRID_ROLE,
            "refused_n_portions": len(refused),
            "kept_n_portions": len(kept),
            "refused_contracts": refused_contracts,
            "kept_contracts": total_contracts - refused_contracts,
            "refused_contract_share": refused_contracts / total_contracts if total_contracts else None,
            "uch_refused": refused_uch,
            "uch_share": refused_uch / total_uch if total_uch else None,
            "markouts_refused": horizon_safe(refused),
            "markouts_kept": horizon_safe(kept),
            "per_game": _gate_per_game(portions, x, exposure_floor, devig),
        })
    return {
        "grid_role": GRID_ROLE,
        "selection": "NONE_THE_GRID_DOES_NOT_PICK_A_WINNER",
        "primary_cell": PRIMARY_GATE,
        "static_attribution_only": True,
        "cells": cells,
    }


def horizon_safe(portions):
    from report import horizon_table
    return horizon_table(portions)


def _gate_per_game(portions, x, exposure_floor, devig):
    grouped = defaultdict(lambda: {"refused": [], "kept": []})
    for portion in portions:
        side = "refused" if portion_refused(portion, x, exposure_floor, devig) else "kept"
        grouped[portion["event"]][side].append(portion)
    out = {}
    for event in sorted(grouped):
        refused = grouped[event]["refused"]
        kept = grouped[event]["kept"]
        out[event] = {
            "refused_n_portions": len(refused),
            "kept_n_portions": len(kept),
            "refused_contracts": sum(portion["size"] for portion in refused),
            "kept_contracts": sum(portion["size"] for portion in kept),
            "uch_refused": sum(portion["uch"] for portion in refused),
            "uch_kept": sum(portion["uch"] for portion in kept),
            "markouts_refused": horizon_safe(refused),
            "markouts_kept": horizon_safe(kept),
        }
    return out


def _common_header():
    return {
        "experiment_id": EXPERIMENT_ID,
        "fee_label": FEE_LABEL,
        "examiner_pin_account_class": None,
        "promote": False,
        "counts_toward_keep": False,
        "family_size": 1,
        "evidence_class": "IN_SAMPLE_DEV / HISTORICAL_REPLAY",
        "DEV_GRADE_REUSED_31_GAME_COHORT": True,
        "HYPOTHETICAL_REPLAY_FILLS": True,
        "IN_SAMPLE_DEV": True,
        "results": None,
        "pnl": None,
        "roi": None,
        "unpinned_rules_resolved_in_freeze": list(UNPINNED_RULES),
        "new_knobs": 0,
    }


def measure(write=True):
    global _CACHE
    if _CACHE is not None:
        return _CACHE
    verify_all()
    digests = manifest_map()
    for rel, expected in (
        (PINS_REL["replay"], REPLAY_SHA256),
        (PINS_REL["queue"], QUEUE_POLICIES_SHA256),
        (PINS_REL["run"], RUN_EXPERIMENT_SHA256),
        (PINS_REL["summary"], SUMMARY_SHA256),
        (PINS_REL["fills"], FILLS_SHA256),
        (PINS_REL["orders"], ORDERS_SHA256),
        (PINS_REL["prereg_json"], PREREG_ACCEPT_SHA256),
        (PINS_REL["prereg_md"], PREREG_ADDENDUM_SHA256),
    ):
        if digests[rel] != expected:
            raise StructureDrift(rel)
    # Orders are hashed above and are not parsed. Decisions are not in the bundle.
    markets = verified_json(PINS_REL["markets"])
    weeks = verified_json(PINS_REL["weeks"])
    if set(weeks) != {meta["event"] for meta in markets.values()} or len(weeks) != EVENTS:
        raise ClosedUniverseRefused("week membership")
    for event in weeks:
        assert_not_holdout(event=event)
    summary = verified_json(PINS_REL["summary"])
    summary_uch = summary["unhedged_contract_hours"]
    fills = _load_fills()
    facts = _fill_facts(fills)
    book = QuoteBook()
    tape = _stream_tape(book)
    tape_ats = tape.pop("ats")
    tape["book_last"] = dict(book.last_at)
    for ticker in markets:
        if ticker not in tape["tickers"]:
            raise ClosedUniverseRefused(ticker)
    for ticker in tape["tickers"]:
        if ticker not in markets:
            raise ClosedUniverseRefused(ticker)
    lots = build_lots(fills, markets, weeks)
    csv_text = verified_bytes(PINS_REL["games"]).decode("utf-8")
    joined = join_cohort(markets, weeks, csv_text)
    schedule = verified_bytes(PINS_REL["schedule"]).decode("utf-8")
    multiplier, fee_rows = read_kxnflgame_maker_multiplier(schedule)
    failures, _late = _structural_failures(facts, tape, lots, markets, summary_uch)
    failures = [item for item in failures if not item.startswith("last_row_")]
    # Re-check last-row separately so one bad ticker does not hide the rest of the list.
    last_row_bad = []
    for ticker, meta in markets.items():
        last = book.last_at.get(ticker)
        if last is None or abs((meta["kickoff"] - last) / 60.0 - 174.0) > 1e-6:
            last_row_bad.append(ticker)
    if last_row_bad:
        failures.append("last_row_k_minus_174")
    late_maker = _maker_after_cutoff(fills, markets)
    if late_maker != 0:
        failures.append("maker_fills_at_or_after_k_minus_3h")
    structural_ok = not failures
    _attach_consensus(lots["portions"], joined["by_event"])
    fees = _attach_fees(lots["portions"], fills, multiplier)
    fees["kxnflgame_schedule_rows"] = [
        {"line": line_no, "maker_m": maker, "taker_m": taker}
        for line_no, maker, taker in fee_rows
    ]
    markouts_emitted = False
    if structural_ok:
        _attach_markouts(lots["portions"], book, joined["by_event"])
        markouts_emitted = True
    measurement = {
        "fills": fills,
        "markets": markets,
        "weeks": weeks,
        "facts": facts,
        "tape": {key: value for key, value in tape.items() if key != "book_last"},
        "tape_ats": tape_ats,
        "lots": lots,
        "joined": joined,
        "fees": fees,
        "book": book,
        "structural_failures": failures,
        "structural_ok": structural_ok,
        "markouts_emitted": markouts_emitted,
        "summary_uch": summary_uch,
        "late_maker_fills": late_maker,
        "bundle_sha256": BUNDLE_SHA256,
        "manifest_sha256": MANIFEST_SHA256,
        "freeze_md_sha256": FREEZE_MD_SHA256,
        "freeze_json_sha256": FREEZE_JSON_SHA256,
        "accept_sha256": ACCEPT_SHA256,
        "accept_claimed_manifest_sha256": ACCEPT_CLAIMED_MANIFEST_SHA256,
    }
    if markouts_emitted:
        measurement["contrast"] = contrast(lots["portions"], events=sorted(weeks))
        measurement["gate"] = _gate_report(lots["portions"])
        opening = lots["opening_contracts"]
        unclassified = sum(
            portion["size"] for portion in lots["portions"] if portion["s_dev"] == "UNCLASSIFIED"
        )
        unclassified_share = unclassified / opening if opening else None
        on_summary = measurement["contrast"]["on"]
        against_summary = measurement["contrast"]["against"]
        verdict, reasons = decide_verdict(
            join_ok=True,
            structural_ok=True,
            unclassified_share=unclassified_share,
            censored_on=censored_share(on_summary),
            censored_against=censored_share(against_summary),
            open_at_window_end_contracts=lots["open_at_window_end_contracts"],
            ci_excludes_0=measurement["contrast"]["ci_excludes_0"],
        )
        measurement["unclassified_contracts"] = unclassified
        measurement["unclassified_share"] = unclassified_share
        measurement["verdict"] = verdict
        measurement["verdict_reasons"] = reasons
    else:
        measurement["contrast"] = None
        measurement["gate"] = None
        measurement["verdict"] = "INCONCLUSIVE"
        measurement["verdict_reasons"] = ["R36"] + failures
        measurement["unclassified_share"] = None
    if write:
        _write_outputs(measurement)
    _CACHE = measurement
    return measurement


def verified_json(rel_path):
    return json.loads(verified_bytes(rel_path).decode("utf-8"))


def games_for_artifacts(measurement):
    """Score-bearing join rows. Permute only away_score and home_score."""
    return {
        event: {
            "away_team": row["away_team"],
            "home_team": row["home_team"],
            "away_score": row["away_score"],
            "home_score": row["home_score"],
        }
        for event, row in measurement["joined"]["by_event"].items()
    }


def invariance_blobs(measurement, games_by_event):
    if not measurement["markouts_emitted"]:
        raise StructureDrift("markouts were not emitted")
    return artifact_bytes(measurement["lots"]["portions"], games_by_event)


def _write_outputs(measurement):
    RESULTS.mkdir(parents=True, exist_ok=True)
    portions = measurement["lots"]["portions"]
    structural = _structural_document(measurement)
    uch = _uch_document(measurement)
    empty = _empty_document(measurement)
    write_json(RESULTS / "STRUCTURAL.json", stamp_ex_post(round_reported(structural)))
    write_json(RESULTS / "UCH.json", stamp_ex_post(round_reported(uch)))
    write_json(RESULTS / "EMPTY_RESULTS.json", stamp_ex_post(round_reported(empty)))
    fixture = _fixture_document(measurement)
    write_json(RESULTS / "CONSENSUS_FIXTURE.json", stamp_ex_post(fixture))
    if measurement["markouts_emitted"]:
        write_json(RESULTS / "MARKOUTS.json", stamp_ex_post(round_reported(_markouts_document(measurement))))
        write_json(RESULTS / "GATE.json", stamp_ex_post(round_reported(measurement["gate"] | _common_header() | {
            "verdict": measurement["verdict"],
            "verdict_reasons": measurement["verdict_reasons"],
        })))
    else:
        for name in ("MARKOUTS.json", "GATE.json"):
            path = RESULTS / name
            if path.exists():
                path.unlink()


def _structural_document(measurement):
    facts = measurement["facts"]
    tape = measurement["tape"]
    lots = measurement["lots"]
    joined = measurement["joined"]
    return _common_header() | {
        "verdict": measurement["verdict"],
        "verdict_reasons": measurement["verdict_reasons"],
        "structural_ok": measurement["structural_ok"],
        "structural_failures": measurement["structural_failures"],
        "markouts_emitted": measurement["markouts_emitted"],
        "fill_rows": facts["rows"],
        "trade_rows": tape["trades"],
        "quote_rows": tape["quotes"],
        "tickers": len(tape["tickers"]),
        "events": len(measurement["weeks"]),
        "block_trades": tape["block_trades"],
        "maker_no_contracts_raw": facts["maker_no_contracts"],
        "maker_yes_contracts_raw": facts["maker_yes_contracts"],
        "maker_contracts_raw": facts["maker_contracts"],
        "taker_contracts_raw": facts["taker_contracts"],
        "maker_no_share_raw": facts["maker_no_share"],
        "taker_yes_contract_share_raw": tape["taker_yes_contract_share"],
        "taker_yes_contracts_raw": tape["taker_yes_contracts"],
        "taker_no_contracts_raw": tape["taker_no_contracts"],
        "taker_yes_trades": tape["taker_yes_trades"],
        "taker_no_trades": tape["taker_no_trades"],
        "maker_no_share": facts["maker_no_share"],
        "taker_yes_contract_share": tape["taker_yes_contract_share"],
        "uch_integral_raw": lots["uch_integral"],
        "uch_fifo_raw": lots["uch_fifo"],
        "ledger_uch_raw": measurement["summary_uch"],
        "uch_integral": lots["uch_integral"],
        "opening_portions": len(portions_of(measurement)),
        "opening_contracts": lots["opening_contracts"],
        "closing_contracts": lots["closing_contracts"],
        "maker_closing_contracts": lots["maker_closing_contracts"],
        "taker_closing_contracts": lots["taker_closing_contracts"],
        "open_at_window_end_contracts": lots["open_at_window_end_contracts"],
        "maker_order_ids": facts["maker_order_ids"],
        "max_abs_inventory_after": facts["max_abs_inventory_after"],
        "maker_fills_at_or_after_k_minus_3h": measurement["late_maker_fills"],
        "join_n": len(joined["rows"]),
        "exact_without_alias": joined["exact_without_alias"],
        "alias_events": joined["alias_events"],
        "game_ids": list(joined["game_ids"]),
        "alias_map": {"JAC": "JAX", "LAR": "LA"},
        "fees": measurement["fees"],
        "bundle_sha256": measurement["bundle_sha256"],
        "manifest_sha256": measurement["manifest_sha256"],
        "freeze_md_sha256": measurement["freeze_md_sha256"],
        "freeze_json_sha256": measurement["freeze_json_sha256"],
        "accept_sha256": measurement["accept_sha256"],
        "accept_claimed_manifest_sha256_differs_from_inner_manifest": (
            measurement["accept_claimed_manifest_sha256"] != measurement["manifest_sha256"]
        ),
    }


def portions_of(measurement):
    return measurement["lots"]["portions"]


def _uch_document(measurement):
    portions = portions_of(measurement)
    lots = measurement["lots"]
    pairs = hold_time_pairs(portions)
    per_game = {}
    grouped = defaultdict(list)
    for portion in portions:
        grouped[portion["event"]].append(portion)
    for event, rows in sorted(grouped.items()):
        per_game[event] = {
            "uch": sum(portion["uch"] for portion in rows),
            "premium_hours": sum(portion["premium_hours"] for portion in rows),
            "contracts": sum(portion["size"] for portion in rows),
            "n_portions": len(rows),
        }
    sensitivity = {}
    for delta in DELTA_SENSITIVITY:
        buckets = {name: {"uch": 0.0, "contracts": 0.0, "n_portions": 0} for name in ("ON", "AGAINST", "NEUTRAL", "UNCLASSIFIED")}
        for portion in portions:
            label = portion["s_dev_sensitivity"][f"{delta:.2f}"]
            buckets[label]["uch"] += portion["uch"]
            buckets[label]["contracts"] += portion["size"]
            buckets[label]["n_portions"] += 1
        sensitivity[f"{delta:.2f}"] = {"role": "SENSITIVITY_NOT_SELECTION", "buckets": buckets}
    return _common_header() | {
        "verdict": measurement["verdict"],
        "uch_integral_raw": lots["uch_integral"],
        "uch_fifo_raw": lots["uch_fifo"],
        "uch_integral": lots["uch_integral"],
        "uch_fifo": lots["uch_fifo"],
        "premium_hours": lots["premium_hours"],
        "hold_time_seconds_p50": weighted_quantile(pairs, 0.5),
        "hold_time_seconds_p90": weighted_quantile(pairs, 0.9),
        "by_s_dev": uch_by_split(portions, "s_dev"),
        "by_s_fav": uch_by_split(portions, "s_fav"),
        "per_game": per_game,
        "delta_sensitivity": sensitivity,
        "primary_delta": PRIMARY_DELTA,
    }


def _markouts_document(measurement):
    portions = portions_of(measurement)
    delta_tables = {}
    for delta in DELTA_SENSITIVITY:
        grouped = {name: [] for name in ("ON", "AGAINST", "NEUTRAL", "UNCLASSIFIED")}
        for portion in portions:
            grouped[portion["s_dev_sensitivity"][f"{delta:.2f}"]].append(portion)
        delta_tables[f"{delta:.2f}"] = {
            "role": "SENSITIVITY_NOT_SELECTION",
            "buckets": {
                name: {"horizons": {"1800": summarize(rows, "1800"), "CLOSE": summarize(rows, "CLOSE")}}
                for name, rows in grouped.items()
            },
        }
    return _common_header() | {
        "verdict": measurement["verdict"],
        "verdict_reasons": measurement["verdict_reasons"],
        "primary_horizon_s": 1800,
        "primary_split": "S_DEV",
        "primary_delta": PRIMARY_DELTA,
        "contrast": measurement["contrast"],
        "s_dev": split_table(portions, "s_dev"),
        "s_fav": split_table(portions, "s_fav"),
        "per_game_s_dev": per_game_split_table(portions, "s_dev"),
        "per_game_s_fav": per_game_split_table(portions, "s_fav"),
        "delta_sensitivity": delta_tables,
        "unclassified_share": measurement["unclassified_share"],
        "settle_note": (
            "SETTLE is secondary and label-dependent. nflverse scores are assumed equal "
            "to the Kalshi settlement, which is not on box. It does not feed the gate or the splits."
        ),
    }


def _fixture_document(measurement):
    rows = []
    for row in measurement["joined"]["rows"]:
        rows.append({
            "event": row["event"],
            "game_id": row["game_id"],
            "away_team": row["away_team"],
            "home_team": row["home_team"],
            "away_moneyline": row["away_moneyline"],
            "home_moneyline": row["home_moneyline"],
            "overround": row["overround"],
            "p_home_prop": row["p_home_prop"],
            "p_home_shin": row["p_home_shin"],
            "shin_z": row["shin_z"],
            "unclassified": row["unclassified"],
        })
    return _common_header() | {
        "role": "INPUT_TRANSFORM_NOT_A_RESULT",
        "overround_definition": "q_away + q_home",
        "shin_solver": "bisection z on [0, 0.4] for 200 iterations; z is the final midpoint",
        "rows": rows,
    }


def _empty_document(measurement):
    return _common_header() | {
        "verdict": measurement["verdict"],
        "verdict_reasons": measurement["verdict_reasons"],
        "counted_simulation_fills_toward_promotion": False,
        "live_promotion": False,
    }


def reset_cache():
    global _CACHE
    _CACHE = None


if __name__ == "__main__":
    result = measure(write=True)
    print(result["verdict"])
    print(result["structural_failures"])
