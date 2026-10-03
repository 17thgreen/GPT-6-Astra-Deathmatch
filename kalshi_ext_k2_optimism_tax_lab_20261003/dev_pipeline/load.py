"""Load B1/B2 once per process, after the manifest check."""

import gzip
import json
import math
from collections import defaultdict

from dev_pipeline.pins import (
    K1_ROOT,
    assert_dev_row,
    checked_bytes,
    load_holdout_sets,
)
from shared.exceptions import LeeReadyRefused
from shared.refusals import assert_no_lee_ready

FACTORIAL = K1_ROOT / "lab/astra-science/nfl_factorial_lab_20260921"
SHA = {
    "events": "cd300e664c2c5f2ff344c4b1eb17dd3f8e5f3326168b9dd8e3ade94a3a7382b4",
    "markets": "66cc07e9e9e1543b3fdcbcded30ff50af0abae87bb2aa3d5fcb3d0be7925632f",
    "manifest": "375ea6e2c9125a411d5444a88115213542d5b19c874d73a2bed0b9355fd6277d",
    "weeks": "a47d0e0dc5a64d79335bc5588f8aa5e1d937503d36ebcbaaf219965a68adf88c",
    "fills": "9d56f5d3c599e092606be9f4a1ad41ae8baabff4921d3d722adf0b57ac944a3f",
    "orders": "c390801b9a7cf6d182d2d097123ed944792980524a7975e6e59a904a530f4b1c",
    "summary": "78b94ae5a846dfa81a1baec8fdc0b7992e479af1ddbc67908195f47500a7930a",
    "replay": "5aba1bf36385d9defeb032040dd6560d3eb1a192fc0203e984a47d9e7c3f37c3",
    "queue": "641d0df3913f4a66fb926c84d170fe1fe61347a2fad16959b6824abb0c135fc2",
    "run": "c1a0fd2d85637b4fe909a24ca96784d3a99fe0a07c03bcef024c9fa16bbf84bc",
    "fee_schedule": "d9435b8b7e30fecbe1a07539990667b23b828a8175962c0882d6c7bce93980ec",
}

_CACHE = {}


def load_dev():
    if "dev" in _CACHE:
        return _CACHE["dev"]
    holdout_events, holdout_game_ids = load_holdout_sets()
    markets_raw, _ = checked_bytes(FACTORIAL / "inputs/markets.json", SHA["markets"])
    weeks_raw, _ = checked_bytes(FACTORIAL / "inputs/week_membership.json", SHA["weeks"])
    checked_bytes(FACTORIAL / "inputs/manifest.json", SHA["manifest"])
    checked_bytes(FACTORIAL / "inputs/events.jsonl.gz", SHA["events"])
    checked_bytes(FACTORIAL / "results/q3300_d0.25_000_fills.jsonl.gz", SHA["fills"])
    checked_bytes(FACTORIAL / "results/q3300_d0.25_000_orders.jsonl.gz", SHA["orders"])
    summary_raw, _ = checked_bytes(FACTORIAL / "results/q3300_d0.25_000.json", SHA["summary"])
    checked_bytes(FACTORIAL / "replay_v2.py", SHA["replay"])
    checked_bytes(FACTORIAL / "queue_policies.py", SHA["queue"])
    checked_bytes(FACTORIAL / "run_experiment.py", SHA["run"])
    fee_raw, _ = checked_bytes(
        K1_ROOT / "lab/governance/astra/packets/scout_house_fee_2026-09-24/raw/docs/kalshi_fee_schedule.txt",
        SHA["fee_schedule"],
    )
    markets = json.loads(markets_raw.decode("utf-8"))
    weeks = json.loads(weeks_raw.decode("utf-8"))
    if len(markets) != 62 or len(weeks) != 31:
        from shared.exceptions import ClosedUniverseRefused
        raise ClosedUniverseRefused("universe size")
    summary = json.loads(summary_raw.decode("utf-8"))
    flow = []
    trade_ids = []
    quotes = defaultdict(list)
    last_at = {}
    n_quote = 0
    yes_sizes = []
    all_sizes = []
    with gzip.open(FACTORIAL / "inputs/events.jsonl.gz", "rt") as handle:
        for line in handle:
            row = json.loads(line)
            assert_no_lee_ready(row)
            assert_dev_row(row, holdout_events, holdout_game_ids, markets, weeks)
            last_at[row["ticker"]] = max(last_at.get(row["ticker"], -math.inf), row["at"])
            if row.get("kind") == "quote":
                n_quote += 1
                quotes[row["ticker"]].append((row["at"], row["asof"], row["bid"], row["ask"]))
            else:
                flow.append((row["ticker"], row["at"], row["taker_side"], row["size"]))
                trade_ids.append(row["trade_id"])
                all_sizes.append(row["size"])
                if row["taker_side"] == "yes":
                    yes_sizes.append(row["size"])
    fills = []
    with gzip.open(FACTORIAL / "results/q3300_d0.25_000_fills.jsonl.gz", "rt") as handle:
        for line in handle:
            row = json.loads(line)
            assert_no_lee_ready(row)
            assert_dev_row(row, holdout_events, holdout_game_ids, markets, weeks)
            fills.append(row)
    bundle = {
        "markets": markets,
        "weeks": weeks,
        "flow": flow,
        "trade_ids": trade_ids,
        "quotes": quotes,
        "last_at": last_at,
        "n_quote": n_quote,
        "n_trade": len(flow),
        "yes_contracts": math.fsum(yes_sizes),
        "all_contracts": math.fsum(all_sizes),
        "fills": fills,
        "summary_uch": summary["unhedged_contract_hours"],
        "pair_hold_weighted_median": summary["pair_holding_time_seconds"]["weighted_median"],
        "fee_schedule_text": fee_raw.decode("utf-8", errors="replace"),
        "holdout_events": holdout_events,
        "holdout_game_ids": holdout_game_ids,
        "games": list(weeks.keys()),
    }
    _CACHE["dev"] = bundle
    return bundle


def assert_code_shas():
    """T16: pinned replay code matches the vendored bytes. The repo tree is checked by the test."""
    checked_bytes(FACTORIAL / "replay_v2.py", SHA["replay"])
    checked_bytes(FACTORIAL / "queue_policies.py", SHA["queue"])
    return True
