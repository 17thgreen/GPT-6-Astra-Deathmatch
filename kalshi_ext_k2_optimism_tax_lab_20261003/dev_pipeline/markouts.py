"""Quote-row markouts. Trade prints never form a mid."""

import bisect
import math
import random
import statistics

from shared.fees import (
    FEE_LABEL,
    MAKER_COEF,
    ceil_6dp,
    ceil_cent,
    model_quadratic,
    part_a_order_headline,
)

HORIZONS = (60, 300, 1800, 3600)
PRIMARY_H = 1800
PROXY_MAX_AGE = 300.0
BOOTSTRAP_B = 10000
BOOTSTRAP_SEED = 20261003


def quote_index(quotes_by_ticker, last_tape_at):
    """quotes_by_ticker[ticker] = list of (at, asof, bid, ask), sorted by at."""
    index = {}
    for ticker, rows in quotes_by_ticker.items():
        rows = sorted(rows)
        index[ticker] = {
            "at": [row[0] for row in rows],
            "rows": rows,
            "last": last_tape_at.get(ticker, -math.inf),
        }
    return index


def mid_out(index, ticker, t, outcome):
    """Latest quote with at <= t. Invalid or past the last tape row -> None."""
    slot = index.get(ticker)
    if slot is None:
        return None
    if t > slot["last"]:
        return None
    pos = bisect.bisect_right(slot["at"], t) - 1
    if pos < 0:
        return None
    at, asof, bid, ask = slot["rows"][pos]
    if not (0 < bid < ask < 1 and 0 <= (t - asof) < PROXY_MAX_AGE):
        return None
    mid = (bid + ask) / 2.0
    if outcome == "yes":
        return mid
    return 1.0 - mid


def order_fee_per_contract(fills, multiplier):
    """Map order_id -> headline fee per contract (K1 R24). Maker fills only."""
    groups = {}
    for fill in fills:
        if fill["kind"] != "maker":
            continue
        groups.setdefault(fill["order_id"], []).append((fill["size"], fill["price"]))
    out = {}
    for order_id, pairs in groups.items():
        _headline, per_contract = part_a_order_headline(pairs, multiplier)
        out[order_id] = per_contract
    return out


def _weighted_mean(pairs):
    weight = math.fsum(size for size, _value in pairs)
    if weight <= 0 or not pairs:
        return None
    return math.fsum(size * value for size, value in pairs) / weight


def _median(values):
    if not values:
        return None
    return statistics.median(values)


def score_portions(portions, index, fee_per_contract):
    """Attach gross, net, and mid-anchored markouts. Does not emit a per-fill file."""
    scored = []
    for portion in portions:
        fee_c = fee_per_contract.get(portion["order_id"])
        direct = None
        if portion.get("fee") is not None and portion["ledger_size"]:
            direct = portion["fee"] / portion["ledger_size"]
        horizons = {}
        for horizon in HORIZONS:
            gross = None
            mid = mid_out(index, portion["ticker"], portion["t_open"] + horizon, portion["outcome"])
            if mid is not None:
                gross = mid - portion["p_entry"]
            mid_anchored = None
            if mid is not None and portion["m_open"] is not None:
                mid_anchored = mid - portion["m_open"]
            net = None if gross is None or fee_c is None else gross - float(fee_c)
            net_direct = None if gross is None or direct is None else gross - direct
            horizons[horizon] = {
                "gross": gross,
                "net": net,
                "net_direct_member": net_direct,
                "mid_anchored": mid_anchored,
            }
        close_units = []
        for sliver in portion["closes"]:
            mid = mid_out(index, portion["ticker"], sliver["at"], portion["outcome"])
            gross = None if mid is None else mid - portion["p_entry"]
            net = None if gross is None or fee_c is None else gross - float(fee_c)
            mid_anchored = None
            if mid is not None and portion["m_open"] is not None:
                mid_anchored = mid - portion["m_open"]
            close_units.append({
                "size": sliver["size"],
                "gross": gross,
                "net": net,
                "mid_anchored": mid_anchored,
            })
        scored.append({
            "row_index": portion["row_index"],
            "event": portion["event"],
            "ticker": portion["ticker"],
            "outcome": portion["outcome"],
            "size_open": portion["size_open"],
            "t_open": portion["t_open"],
            "order_id": portion["order_id"],
            "fee_per_contract": None if fee_c is None else float(fee_c),
            "direct_member_per_contract": direct,
            "horizons": horizons,
            "close_units": close_units,
            "closes": portion["closes"],
        })
    return scored


def _empty_acc():
    return {
        "n": 0,
        "contracts": 0.0,
        "no_contracts": 0.0,
        "games": set(),
        "uch": 0.0,
    }


def aggregate(scored, labels, unit_key):
    """unit_key selects primary, secondary, or sensitivity on the label row."""
    by_index = {row["row_index"]: row for row in labels}
    groups = {name: _empty_acc() for name in ("T1_LOW", "T2_MID", "T3_HIGH", "UNCLASSIFIED")}
    per_game = {}
    for portion in scored:
        label = by_index[portion["row_index"]][unit_key]
        acc = groups[label]
        acc["n"] += 1
        acc["contracts"] += portion["size_open"]
        if portion["outcome"] == "no":
            acc["no_contracts"] += portion["size_open"]
        acc["games"].add(portion["event"])
        uch = 0.0
        for sliver in portion["closes"]:
            uch += sliver["size"] * (sliver["at"] - portion["t_open"]) / 3600.0
        acc["uch"] += uch
        game = per_game.setdefault(portion["event"], {})
        game.setdefault(label, []).append(portion)
        acc.setdefault("rows", []).append(portion)
    total_contracts = math.fsum(groups[name]["contracts"] for name in groups)
    total_uch = math.fsum(groups[name]["uch"] for name in groups)
    cells = []
    for name in ("T1_LOW", "T2_MID", "T3_HIGH", "UNCLASSIFIED"):
        acc = groups[name]
        cells.append(_cell(name, acc, total_contracts, total_uch))
    game_cells = []
    for event in sorted(per_game):
        for name in ("T1_LOW", "T2_MID", "T3_HIGH", "UNCLASSIFIED"):
            rows = per_game[event].get(name, [])
            if not rows:
                continue
            fake = _empty_acc()
            fake["rows"] = rows
            for portion in rows:
                fake["n"] += 1
                fake["contracts"] += portion["size_open"]
                if portion["outcome"] == "no":
                    fake["no_contracts"] += portion["size_open"]
                fake["games"].add(event)
                for sliver in portion["closes"]:
                    fake["uch"] += sliver["size"] * (sliver["at"] - portion["t_open"]) / 3600.0
            cell = _cell(name, fake, total_contracts, total_uch)
            cell["event"] = event
            game_cells.append(cell)
    return {"cells": cells, "per_game": game_cells, "groups": groups}


def _horizon_block(rows, horizon):
    if horizon == "CLOSE":
        gross_pairs = []
        net_pairs = []
        mid_pairs = []
        gross_values = []
        censored_n = 0
        censored_contracts = 0.0
        n_units = 0
        for portion in rows:
            for unit in portion["close_units"]:
                n_units += 1
                if unit["gross"] is None:
                    censored_n += 1
                    censored_contracts += unit["size"]
                else:
                    gross_pairs.append((unit["size"], unit["gross"]))
                    gross_values.append(unit["gross"])
                    if unit["net"] is not None:
                        net_pairs.append((unit["size"], unit["net"]))
                    if unit["mid_anchored"] is not None:
                        mid_pairs.append((unit["size"], unit["mid_anchored"]))
        return {
            "gross_weighted_mean": _weighted_mean(gross_pairs),
            "net_weighted_mean": _weighted_mean(net_pairs),
            "unweighted_median_gross": _median(gross_values),
            "n": len(gross_pairs),
            "censored_n": censored_n,
            "censored_contracts": censored_contracts,
            "mid_anchored_weighted_mean": _weighted_mean(mid_pairs),
            "fee_label": FEE_LABEL,
            "net_is_headline": False,
        }
    gross_pairs = []
    net_pairs = []
    direct_pairs = []
    mid_pairs = []
    gross_values = []
    censored_n = 0
    censored_contracts = 0.0
    for portion in rows:
        slot = portion["horizons"][horizon]
        if slot["gross"] is None:
            censored_n += 1
            censored_contracts += portion["size_open"]
        else:
            gross_pairs.append((portion["size_open"], slot["gross"]))
            gross_values.append(slot["gross"])
            if slot["net"] is not None:
                net_pairs.append((portion["size_open"], slot["net"]))
            if slot["net_direct_member"] is not None:
                direct_pairs.append((portion["size_open"], slot["net_direct_member"]))
            if slot["mid_anchored"] is not None:
                mid_pairs.append((portion["size_open"], slot["mid_anchored"]))
    return {
        "gross_weighted_mean": _weighted_mean(gross_pairs),
        "net_weighted_mean": _weighted_mean(net_pairs),
        "direct_member_sensitivity_weighted_mean": _weighted_mean(direct_pairs),
        "unweighted_median_gross": _median(gross_values),
        "n": len(gross_pairs),
        "censored_n": censored_n,
        "censored_contracts": censored_contracts,
        "mid_anchored_weighted_mean": _weighted_mean(mid_pairs),
        "fee_label": FEE_LABEL,
        "net_is_headline": False,
        "examiner_pin_account_class": None,
    }


def _cell(name, acc, total_contracts, total_uch):
    rows = acc.get("rows", [])
    horizons = {}
    for horizon in HORIZONS:
        horizons[str(horizon)] = _horizon_block(rows, horizon)
    horizons["CLOSE"] = _horizon_block(rows, "CLOSE")
    contracts = acc["contracts"]
    return {
        "tercile": name,
        "n_opening_portions": acc["n"],
        "opening_contracts": contracts,
        "opening_contract_share": (contracts / total_contracts) if total_contracts else None,
        "maker_no_share_of_opening_contracts": (acc["no_contracts"] / contracts) if contracts else None,
        "distinct_games": len(acc["games"]),
        "uch_contract_hours": acc["uch"],
        "uch_share": (acc["uch"] / total_uch) if total_uch else None,
        "horizons": horizons,
        "fee_label": FEE_LABEL,
    }


def _primary_pools(scored, labels):
    by_index = {row["row_index"]: row for row in labels}
    pools = {}
    for portion in scored:
        label = by_index[portion["row_index"]]["primary"]
        event = portion["event"]
        slot = portion["horizons"][PRIMARY_H]
        pools.setdefault(event, {}).setdefault(label, []).append(
            (portion["size_open"], slot["gross"], slot["net"])
        )
    return pools


def bootstrap_delta(scored, labels, games, b=BOOTSTRAP_B, seed=BOOTSTRAP_SEED):
    """Game-cluster bootstrap of gross MO_1800(T3) - MO_1800(T1).

    A resample is dropped when T1 or T3 has no non-null gross contracts.
    """
    pools = _primary_pools(scored, labels)
    rng = random.Random(seed)
    deltas_gross = []
    deltas_net = []
    dropped = 0
    n_games = len(games)
    for _ in range(b):
        draw = [games[rng.randrange(n_games)] for _ in range(n_games)]
        t1 = []
        t3 = []
        t1n = []
        t3n = []
        for event in draw:
            for size, gross, net in pools.get(event, {}).get("T1_LOW", ()):
                if gross is not None:
                    t1.append((size, gross))
                    if net is not None:
                        t1n.append((size, net))
            for size, gross, net in pools.get(event, {}).get("T3_HIGH", ()):
                if gross is not None:
                    t3.append((size, gross))
                    if net is not None:
                        t3n.append((size, net))
        if not t1 or not t3:
            dropped += 1
            continue
        deltas_gross.append(_weighted_mean(t3) - _weighted_mean(t1))
        if t1n and t3n:
            deltas_net.append(_weighted_mean(t3n) - _weighted_mean(t1n))
    deltas_gross.sort()
    deltas_net.sort()
    return {
        "b": b,
        "seed": seed,
        "dropped": dropped,
        "dropped_share": dropped / b if b else None,
        "n_used": len(deltas_gross),
        "delta_gross": _weighted_point(scored, labels, "gross"),
        "delta_net": _weighted_point(scored, labels, "net"),
        "ci95_gross": _ci(deltas_gross),
        "ci95_net": _ci(deltas_net),
        "fee_label": FEE_LABEL,
        "net_is_headline": False,
    }


def _weighted_point(scored, labels, field):
    by_index = {row["row_index"]: row for row in labels}
    buckets = {"T1_LOW": [], "T3_HIGH": []}
    for portion in scored:
        label = by_index[portion["row_index"]]["primary"]
        if label not in buckets:
            continue
        value = portion["horizons"][PRIMARY_H][field]
        if value is not None:
            buckets[label].append((portion["size_open"], value))
    if not buckets["T1_LOW"] or not buckets["T3_HIGH"]:
        return None
    return _weighted_mean(buckets["T3_HIGH"]) - _weighted_mean(buckets["T1_LOW"])


def _ci(sorted_deltas):
    if not sorted_deltas:
        return None
    from dev_pipeline.terciles import q7
    return [q7(sorted_deltas, 0.025), q7(sorted_deltas, 0.975)]


def ci_excludes_zero(interval):
    if not interval:
        return False
    lo, hi = interval
    return hi < 0 or lo > 0
