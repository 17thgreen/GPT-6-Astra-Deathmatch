"""Secondary metrics and the emitted fee views.

HEADLINE, FEES_2X and GROSS only. Sensitivity rows are not built here.
Fee paths use explicit loops rather than max or min.
"""
from __future__ import annotations

import math
from datetime import datetime, timezone
from decimal import Decimal, ROUND_FLOOR, ROUND_HALF_EVEN

from card01_amc.fee_source import pinned_taker_fee
from card01_amc.pinload import load_national_miss
from card01_amc.regime_split import is_headline, m3_rows

ENTRY = datetime(2026, 11, 2, 22, 0, 0, tzinfo=timezone.utc)
_SHARE = Decimal("0.000001")
_HOUR = Decimal("0.000001")
FEE_ASSUMPTIONS = {
    "assumed_non_direct": True,
    "single_fill_one_shot": True,
    "multi_fill_accumulator_rebate_modelled": False,
    "member_type_pinned": None,
}


def _arm_key(w):
    if w == 0:
        return "0"
    if w == 1:
        return "1.0"
    return str(w)


def _bin_index(probability):
    scaled = (Decimal(repr(probability)) * Decimal(10)).to_integral_value(ROUND_FLOOR)
    scaled_i = int(scaled)
    if scaled_i > 9:
        scaled_i = 9
    if scaled_i < 0:
        scaled_i = 0
    return scaled_i + 1


def _interval(bin_index):
    if bin_index == 10:
        return "[0.9,1.0]"
    return f"[{(bin_index - 1) / 10:.1f},{bin_index / 10:.1f})"


def log_loss_and_calibration(rows, pinned=None):
    pinned = pinned or load_national_miss()
    scored = [row for row in rows if is_headline(row)]
    n = len(scored)
    if n == 0:
        return {
            "log_loss": None,
            "log_loss_status": "EMPTY",
            "delta_log_loss": None,
            "delta_log_loss_status": "EMPTY",
            "calibration": None,
            "calibration_status": "EMPTY",
            "freeze_named": True,
        }
    losses = {}
    calibration = {}
    for weight in pinned.WS:
        brier_terms = []
        loss_terms = []
        bins = {
            index: {"count": 0, "forecast": 0.0, "observed": 0.0}
            for index in range(1, 11)
        }
        for row in scored:
            probability = pinned.arm_p(row, weight)
            y = row["y"]
            brier_terms.append((probability - y) ** 2)
            clipped = pinned.clip(probability)
            loss_terms.append(-(y * math.log(clipped) + (1 - y) * math.log(1 - clipped)))
            index = _bin_index(probability)
            cell = bins[index]
            cell["count"] += 1
            cell["forecast"] += probability
            cell["observed"] += y
        key = _arm_key(weight)
        losses[key] = sum(loss_terms) / n
        brier_sum = sum(brier_terms)
        published = []
        for index in range(1, 11):
            cell = bins[index]
            count = cell["count"]
            published.append({
                "bin": index,
                "interval": _interval(index),
                "count": count,
                "mean_forecast": None if count == 0 else cell["forecast"] / count,
                "observed_freq": None if count == 0 else cell["observed"] / count,
                "thin": count < 10,
            })
        calibration[key] = {"brier": brier_sum / n, "bins": published}
    base = losses["0"]
    delta = {key: value - base for key, value in losses.items()}
    return {
        "log_loss": losses,
        "log_loss_status": "OK",
        "delta_log_loss": delta,
        "delta_log_loss_status": "OK",
        "calibration": calibration,
        "calibration_status": "OK",
        "freeze_named": True,
    }


def m3_mids_gaps(rows):
    out = []
    for row in m3_rows(rows):
        reasons = list(row.get("exclusion_reasons") or [])
        item = {
            "race_id": row.get("race_id"),
            "state": row.get("state"),
            "mapping_status": row.get("mapping_status"),
            "exclusion_reasons": reasons,
        }
        if "mid_raw" not in row:
            item["mid_at_snapshot"] = None
            item["mid_at_snapshot_status"] = "INPUT_MISSING:mid_raw"
        else:
            item["mid_at_snapshot"] = row.get("mid_raw")
            item["mid_at_snapshot_status"] = row.get("mid_raw_status") or (
                "OK" if row.get("mid_raw") is not None else "no_two_sided_book"
            )
        if "p_model_raw" not in row:
            item["p_model_at_snapshot"] = None
            item["p_model_at_snapshot_status"] = "INPUT_MISSING:p_model_raw"
        else:
            item["p_model_at_snapshot"] = row.get("p_model_raw")
            item["p_model_at_snapshot_status"] = row.get("p_model_raw_status") or "OK"
        mid = item["mid_at_snapshot"]
        model = item["p_model_at_snapshot"]
        blocked = "NO_DEMOCRAT" in reasons or "SAME_PARTY_S5" in reasons
        if blocked or mid is None or model is None:
            item["gap"] = None
        else:
            item["gap"] = float(model) - float(mid)
        out.append(item)
    return out


def _money(value):
    if isinstance(value, Decimal):
        return value
    if isinstance(value, float):
        return Decimal(repr(value))
    return Decimal(str(value))


def _won(side, y):
    if y not in (0, 1):
        return None
    if side == "D_YES":
        return y == 1
    if side == "D_NO":
        return y == 0
    return None


def headline_quote(entry, price):
    quoted = pinned_taker_fee(entry, price)
    return quoted["headline"], quoted["raw"]


def fee_views(signals, rows_by_id, entries):
    """HEADLINE and FEES_2X nets, plus GROSS. One pinned entry per series."""
    per_signal = []
    totals = {
        "gross": Decimal(0),
        "fee_headline": Decimal(0),
        "fee_fees_2x": Decimal(0),
        "net_headline": Decimal(0),
        "net_fees_2x": Decimal(0),
    }
    defects = []
    for signal in signals:
        row = rows_by_id.get(signal.get("race_id")) or {}
        price = _money(signal.get("price"))
        headline, raw = headline_quote(entries[signal.get("series")], price)
        declared = signal.get("fee_decimal")
        if declared is not None and _money(declared) != headline:
            defects.append({"kind": "FEE_RECOMPUTE_MISMATCH", "status": "REPORTING_DEFECT"})
        won = _won(signal.get("side"), row.get("y"))
        payoff = Decimal(1) if won else Decimal(0)
        gross = payoff - price
        fee_2x = headline * 2
        net_h = gross - headline
        net_2 = gross - fee_2x
        per_signal.append({
            "race_id": signal.get("race_id"),
            "side": signal.get("side"),
            "price": str(price),
            "fee_raw": str(raw),
            "fee_headline": str(headline),
            "fee_fees_2x": str(fee_2x),
            "gross": str(gross),
            "net_headline": str(net_h),
            "net_fees_2x": str(net_2),
        })
        totals["gross"] += gross
        totals["fee_headline"] += headline
        totals["fee_fees_2x"] += fee_2x
        totals["net_headline"] += net_h
        totals["net_fees_2x"] += net_2
    status = "OK" if signals else "NO_SIGNALS_SELECTED"
    return {
        "per_signal": per_signal,
        "totals": {key: str(value) for key, value in totals.items()},
        "one_tick_worse_status": "PR_C_OUTPUT_ABSENT",
        "status": status,
        "reporting_defects": defects,
    }


def _nets(views):
    return [Decimal(item["net_headline"]) for item in views["per_signal"]]


def event_concentration(views, pr_c_output):
    nets = _nets(views)
    if not nets:
        return {
            "hhi": None,
            "top1_positive_share": None,
            "top1_flag": None,
            "status": "NO_SIGNALS_SELECTED",
            "pr_c_match": None,
            "pr_c_match_status": "PR_C_OUTPUT_ABSENT",
            "freeze_named": True,
            "class_hhi": "DISPLAY-ONLY",
            "class_top1_positive_share": "VERDICT-BEARING",
        }, []
    abs_sum = Decimal(0)
    for net in nets:
        if net < 0:
            abs_sum += -net
        else:
            abs_sum += net
    hhi = None
    if abs_sum != 0:
        acc = Decimal(0)
        for net in nets:
            magnitude = -net if net < 0 else net
            share = magnitude / abs_sum
            acc += share * share
        hhi = acc.quantize(_SHARE, rounding=ROUND_HALF_EVEN)
    positive_sum = Decimal(0)
    top = None
    any_positive = False
    for net in nets:
        if net > 0:
            positive_sum += net
            any_positive = True
            if top is None or net > top:
                top = net
    top_share = None
    flag = None
    if any_positive and positive_sum != 0:
        top_share = (top / positive_sum).quantize(_SHARE, rounding=ROUND_HALF_EVEN)
        flag = (top * 2) > positive_sum
    net_total = Decimal(0)
    for net in nets:
        net_total += net
    defects = []
    if pr_c_output is None:
        match = None
        match_status = "PR_C_OUTPUT_ABSENT"
    else:
        match = True
        reported_net = pr_c_output.get("net_headline_total")
        reported_top = pr_c_output.get("top1_positive_share")
        if reported_net is None or _money(reported_net) != net_total:
            match = False
        if top_share is None or reported_top is None or _money(reported_top) != top_share:
            match = False
        match_status = "OK" if match else "REPORTING_DEFECT"
        if not match:
            defects.append({"kind": "PNL_MISMATCH", "status": "REPORTING_DEFECT"})
    return {
        "hhi": None if hhi is None else str(hhi),
        "top1_positive_share": None if top_share is None else str(top_share),
        "top1_flag": flag,
        "net_headline_total": str(net_total),
        "status": "OK",
        "pr_c_match": match,
        "pr_c_match_status": match_status,
        "freeze_named": True,
        "class_hhi": "DISPLAY-ONLY",
        "class_top1_positive_share": "VERDICT-BEARING",
    }, defects


def holding_hours(settlement_ts):
    """Hours from 2026-11-02T22:00:00Z. Microseconds stay integer."""
    if settlement_ts is None or settlement_ts == "":
        return None, "INPUT_MISSING:settlement_ts"
    try:
        parsed = datetime.strptime(settlement_ts, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
    except (TypeError, ValueError):
        return None, "INPUT_MISSING:settlement_ts_unparseable"
    delta = parsed - ENTRY
    microseconds = delta.days * 86_400_000_000 + delta.seconds * 1_000_000 + delta.microseconds
    hours = (Decimal(microseconds) / Decimal(1000000) / Decimal(3600)).quantize(
        _HOUR, rounding=ROUND_HALF_EVEN
    )
    return hours, "OK"


def _lookup_settlement(signal, row, settled_by_ticker):
    ticker = None
    if isinstance(row, dict):
        ticker = row.get("ticker")
    if not ticker:
        ticker = signal.get("ticker")
    record = settled_by_ticker.get(ticker) if ticker else None
    if not isinstance(record, dict):
        return None, "INPUT_MISSING:settlement_ts"
    raw = record.get("settlement_ts")
    if raw is None or raw == "":
        return None, "INPUT_MISSING:settlement_ts"
    return raw, "PRESENT"


def capital_hours(signals, rows_by_id, views, settled_by_ticker):
    by_fee = {item["race_id"]: item for item in views["per_signal"]}
    per_signal = []
    total = Decimal(0)
    missing = None
    for signal in signals:
        row = rows_by_id.get(signal.get("race_id")) or {}
        raw, presence = _lookup_settlement(signal, row, settled_by_ticker)
        price = _money(by_fee[signal["race_id"]]["price"])
        if presence != "PRESENT":
            missing = presence
            per_signal.append({
                "race_id": signal.get("race_id"),
                "settlement_ts": None,
                "settled_at_utc": None,
                "hours": None,
                "usd_hours": None,
                "status": presence,
            })
            continue
        hours, status = holding_hours(raw)
        if status != "OK":
            missing = status
            per_signal.append({
                "race_id": signal.get("race_id"),
                "settlement_ts": raw,
                "settled_at_utc": raw,
                "hours": None,
                "usd_hours": None,
                "status": status,
            })
            continue
        usd = price * hours
        total += usd
        per_signal.append({
            "race_id": signal.get("race_id"),
            "settlement_ts": raw,
            "settled_at_utc": raw,
            "hours": str(hours),
            "usd_hours": str(usd),
            "status": "OK",
        })
    return {
        "basis": "price_x_hours",
        "per_signal": per_signal,
        "total_usd_hours": None if missing or not signals else str(total),
        "status": missing or ("OK" if signals else "NO_SIGNALS_SELECTED"),
        "freeze_named": True,
        "class": "DISPLAY-ONLY",
    }


def drawdown(signals, views, settled_by_ticker, rows_by_id):
    nets = {item["race_id"]: Decimal(item["net_headline"]) for item in views["per_signal"]}
    ordered = []
    for signal in signals:
        row = rows_by_id.get(signal.get("race_id")) or {}
        raw, presence = _lookup_settlement(signal, row, settled_by_ticker)
        if presence != "PRESENT":
            return {"drawdown_usd": None, "status": presence, "freeze_named": True, "class": "DISPLAY-ONLY"}
        hours, status = holding_hours(raw)
        if status != "OK":
            return {"drawdown_usd": None, "status": status, "freeze_named": True, "class": "DISPLAY-ONLY"}
        parsed = datetime.strptime(raw, "%Y-%m-%dT%H:%M:%S.%fZ")
        ordered.append((parsed, signal.get("race_id") or "", nets[signal["race_id"]]))
    ordered.sort()
    running = Decimal(0)
    peak = Decimal(0)
    worst = Decimal(0)
    for _ts, _race, net in ordered:
        running += net
        if running > peak:
            peak = running
        drop = peak - running
        if drop > worst:
            worst = drop
    return {
        "drawdown_usd": str(worst),
        "status": "OK" if signals else "NO_SIGNALS_SELECTED",
        "freeze_named": True,
        "class": "DISPLAY-ONLY",
    }


def executable_usd_per_day(signals, rows_by_id, views, pinned=None):
    pinned = pinned or load_national_miss()
    by_fee = {item["race_id"]: Decimal(item["fee_headline"]) for item in views["per_signal"]}
    per_signal = []
    day = Decimal(0)
    for signal in signals:
        row = rows_by_id.get(signal.get("race_id")) or {}
        arm = pinned.arm_p(row, pinned.HEADLINE_W)
        probability = arm if signal.get("side") == "D_YES" else 1.0 - arm
        edge = Decimal(repr(probability)) - _money(signal.get("price")) - by_fee[signal["race_id"]]
        day += edge
        per_signal.append({"race_id": signal.get("race_id"), "edge": str(edge)})
    if not signals:
        return {
            "decision_day": "2026-11-02",
            "per_signal": [],
            "day_sum": "0",
            "median_day": None,
            "p10_day": None,
            "n_days": 0,
            "status": "NO_SIGNALS_SELECTED",
            "freeze_named": True,
        }
    days = [day]
    n_days = len(days)
    ordered = sorted(days)
    if n_days % 2 == 1:
        median = ordered[n_days // 2]
    else:
        median = (ordered[n_days // 2 - 1] + ordered[n_days // 2]) / 2
    index = math.ceil(0.10 * n_days) - 1
    if index < 0:
        index = 0
    return {
        "decision_day": "2026-11-02",
        "per_signal": per_signal,
        "day_sum": str(day),
        "median_day": str(median),
        "p10_day": str(ordered[index]),
        "n_days": n_days,
        "status": "OK",
        "freeze_named": True,
        "class": "DISPLAY-ONLY",
    }


def unresolved_inventory(signals, rows_by_id, views, settled_by_ticker):
    by_fee = {item["race_id"]: item for item in views["per_signal"]}
    open_ids = []
    cost = Decimal(0)
    for signal in signals:
        row = rows_by_id.get(signal.get("race_id")) or {}
        raw, presence = _lookup_settlement(signal, row, settled_by_ticker)
        hours_status = "OK"
        if presence == "PRESENT":
            _hours, hours_status = holding_hours(raw)
        if presence != "PRESENT" or hours_status != "OK":
            open_ids.append(signal.get("race_id"))
            price = _money(by_fee[signal["race_id"]]["price"])
            fee = _money(by_fee[signal["race_id"]]["fee_headline"])
            cost += price + fee
    return {
        "n_contracts": len(open_ids),
        "race_ids": open_ids,
        "cost_basis": str(cost),
        "status": "OK",
        "freeze_named": True,
        "class": "DISPLAY-ONLY",
    }


def signals_and_size(gate):
    signals = gate.get("signals") if isinstance(gate, dict) else None
    signals = signals or []
    n_signals = len(signals)
    n_by_side = {"D_YES": 0, "D_NO": 0}
    for signal in signals:
        side = signal.get("side")
        if side in n_by_side:
            n_by_side[side] += 1
    if not isinstance(gate, dict) or "depth_rejected" not in gate or gate.get("depth_rejected") is None:
        requested = None
        depth_status = "INPUT_MISSING:depth_rejected"
    else:
        requested = n_signals + len(gate.get("depth_rejected") or [])
        depth_status = "OK"
    ratio = None
    if requested:
        ratio = (Decimal(n_signals) / Decimal(requested)).quantize(_SHARE, rounding=ROUND_HALF_EVEN)
    return {
        "n_signals": n_signals,
        "n_by_side": n_by_side,
        "n_requested": requested,
        "n_feasible": n_signals,
        "feasible_vs_requested": None if ratio is None else str(ratio),
        "depth_rejected_status": depth_status,
        "fill_rate": None,
        "fill_rate_status": "NO_ELIGIBLE_FILLS",
        "simulated_fills": {
            "label": "simulated",
            "filled": n_signals,
            "requested": requested,
            "fill_rate_simulated": None if ratio is None else str(ratio),
            "counts_toward_keep": False,
        },
        "status": "OK" if n_signals else "NO_SIGNALS_SELECTED",
        "freeze_named": True,
        "class": "DISPLAY-ONLY",
    }


def rewards():
    return {
        "rewards_actually_earned": None,
        "rewards_actually_earned_status": "NO_ORDERS_PLACED",
        "net_pnl_with_rewards": None,
        "net_pnl_with_rewards_status": "NO_REWARDS_CASH",
    }
