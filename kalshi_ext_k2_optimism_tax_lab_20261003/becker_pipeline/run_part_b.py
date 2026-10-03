"""Box-only runner. Becker tables are read from the manifest, never from this clone."""

import argparse
import hashlib
import json
import re
from pathlib import Path

from becker_pipeline.exclusion import (
    LIST_KEYS,
    exclusion_from_scan,
    empty_scan,
    market_columns,
    note_trade,
    summarize_counts,
    trade_columns,
)
from becker_pipeline.guards import REFUSED_MARKET_FIELDS, refuse_becker_input, refuse_tier_path
from becker_pipeline.metrics import Accumulator, document_from_events, prepare_trade
from becker_pipeline.pins import cloud_input_shas, load_holdout_sets
from becker_pipeline.writer import assert_outside_repo, write_aggregates
from shared.bands import load_registry
from shared.canonical import canon_bytes, sha256_file
from shared.exceptions import (
    BeckerQuoteFieldRefused,
    BoxOnlyRefused,
    InconclusiveNoOutput,
    IntegrityRefused,
    ManifestTamper,
    ReceiptMismatchRefused,
)
from shared.fees import read_kxnflgame_multiplier
from shared.provenance import Provenanced
from shared.refusals import assert_not_holdout, assert_timestamp_allowed

MANIFEST_SHA = "fd5e10531f488f30baf05e2dd6f17c8f8823603ecbae457170dbbde66126fb95"
EXCLUSION_SHA = "61a4c993fbea5940e5999177ffb5a0e3161219a8f84812af2d2f44d9f556641b"
RUNNER_PATH = Path(__file__).resolve()
LAB = Path(__file__).resolve().parents[1]


def _repo_root():
    return Path(__file__).resolve().parents[2]


def git_head(repo=None):
    repo = Path(repo) if repo is not None else _repo_root()
    git_path = repo / ".git"
    if git_path.is_file():
        text = git_path.read_text(encoding="utf-8").strip()
        if text.startswith("gitdir: "):
            git_path = Path(text.split(" ", 1)[1].strip())
            if not git_path.is_absolute():
                git_path = (repo / git_path).resolve()
    head = (git_path / "HEAD").read_text(encoding="utf-8").strip()
    if head.startswith("ref: "):
        return (git_path / head[5:].strip()).read_text(encoding="utf-8").strip()
    return head


def directory_hash(root):
    root = Path(root)
    lines = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        rel = path.relative_to(root).as_posix()
        lines.append(rel + ":" + sha256_file(path))
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()


def freeze_pin_shas():
    path = LAB / "pins" / "governance" / "FREEZE_SHA256.json"
    doc = json.loads(path.read_text(encoding="utf-8"))
    return doc["freeze_md_sha256"], doc["freeze_json_sha256"]


def resolve_item_path(manifest, item):
    """Resolve a manifest path against manifest['root'], not the process cwd."""
    raw = item.get("path")
    if not raw:
        raise InconclusiveNoOutput("box manifest item has no path")
    path = Path(raw)
    if path.is_absolute():
        return path
    root = manifest.get("root")
    if not root:
        raise InconclusiveNoOutput("manifest root")
    return Path(root) / path


def is_data_table(item):
    path = str(item.get("path") or "")
    if not path.endswith(".parquet"):
        return False
    if item.get("becker_data_or_derived") is True:
        return True
    blob = (str(item.get("role") or "") + " " + Path(path).name).lower()
    return "trade" in blob or "market" in blob


def table_kind(item):
    blob = (str(item.get("role") or "") + " " + Path(str(item.get("path") or "")).name).lower()
    if "trade" in blob:
        return "trades"
    if "market" in blob:
        return "markets"
    return "other"


def verify_runner_item_shas(manifest):
    """Sha-check only items the runner is allowed to read. Hashing a pin is not a mix."""
    items = manifest.get("items") if isinstance(manifest, dict) else None
    if not isinstance(items, list):
        raise InconclusiveNoOutput("box manifest schema is not a pin list")
    verified = []
    for item in items:
        if item.get("read_by_part_b_runner") is not True:
            continue
        path = resolve_item_path(manifest, item)
        expected = item.get("sha256")
        if not isinstance(expected, str) or sha256_file(path) != expected:
            raise ManifestTamper(str(path))
        verified.append((item, path))
    return verified


def refuse_data_items(verified, cloud_shas):
    """Path, tier, sqlite, and mix refusals for data tables. Pins are not loaded."""
    for item, path in verified:
        if not is_data_table(item):
            continue
        refuse_becker_input(path, sha=item.get("sha256"), cloud_shas=cloud_shas)
        refuse_tier_path(path)
        columns = trade_columns() if table_kind(item) == "trades" else market_columns()
        for name in columns:
            if name in REFUSED_MARKET_FIELDS:
                raise BeckerQuoteFieldRefused(name)


def open_runner_tables(manifest, cloud_shas, loader):
    """Verify pins, refuse data paths, and only then call loader."""
    verified = verify_runner_item_shas(manifest)
    refuse_data_items(verified, cloud_shas)
    tables = {}
    for item, path in verified:
        if not is_data_table(item):
            continue
        kind = table_kind(item)
        columns = trade_columns() if kind == "trades" else market_columns()
        tables[kind] = loader(path, columns)
    return tables, verified


def compare_exclusion(pinned, recomputed, trades_sha, markets_sha):
    if not isinstance(pinned, dict):
        raise InconclusiveNoOutput("exclusion document")
    for key in LIST_KEYS:
        if not isinstance(pinned.get(key), list) or not isinstance(recomputed.get(key), list):
            raise InconclusiveNoOutput("exclusion schema")
        if sorted(pinned[key]) != list(recomputed[key]):
            raise InconclusiveNoOutput("exclusion membership")
    if pinned.get("source_trades_sha256") != trades_sha:
        raise InconclusiveNoOutput("source trades sha")
    if pinned.get("source_markets_sha256") != markets_sha:
        raise InconclusiveNoOutput("source markets sha")
    if pinned.get("experiment_id") != recomputed["experiment_id"]:
        raise InconclusiveNoOutput("experiment id")
    rule = pinned.get("rule")
    if not isinstance(rule, str) or not rule.strip():
        raise InconclusiveNoOutput("exclusion rule")


def _fact_cell(text, predicate):
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        parts = [part.strip() for part in line.split("|")]
        if len(parts) >= 3 and predicate(parts[1]):
            return parts[2]
    raise InconclusiveNoOutput("freeze counts")


def _labeled(cell, word):
    match = re.search(r"(\d[\d,]*)\s+" + re.escape(word), cell)
    if match is None:
        raise InconclusiveNoOutput("freeze counts")
    return int(match.group(1).replace(",", ""))


def _ints(cell):
    return [int(token.replace(",", "")) for token in re.findall(r"\d[\d,]*", cell)]


def parse_freeze_expectations(text):
    """Read structural counts and the selection-bias paragraph from the freeze markdown."""
    trade = _fact_cell(text, lambda fact: fact.startswith("Trade rows / traded tickers"))
    opened = _fact_cell(text, lambda fact: "Open at trade fetch" in fact)
    missing = _fact_cell(text, lambda fact: fact.startswith("No yes/no"))
    excluded = _fact_cell(text, lambda fact: "ticker-level union" in fact)
    eligible = _fact_cell(text, lambda fact: fact == "**Eligible**")
    trade_nums = _ints(trade)
    if len(trade_nums) < 3:
        raise InconclusiveNoOutput("freeze counts")
    orphan = re.search(r"no markets row \((\d[\d,]*)\)", text)
    if orphan is None:
        raise InconclusiveNoOutput("freeze counts")
    bias_at = text.find("Selection-bias statement")
    if bias_at < 0:
        raise InconclusiveNoOutput("selection-bias statement")
    bias_body = text[bias_at:]
    colon = bias_body.find(":")
    paragraph = bias_body[colon + 1:].split("\n\n", 1)[0]
    selection = " ".join(paragraph.split())
    if not selection:
        raise InconclusiveNoOutput("selection-bias statement")
    cover_at = text.find("coverage statement:")
    if cover_at < 0:
        raise InconclusiveNoOutput("coverage statement")
    cover_body = text[cover_at + len("coverage statement:"):].strip()
    period = cover_body.find(".")
    if period < 0:
        raise InconclusiveNoOutput("coverage statement")
    coverage = " ".join(cover_body[:period + 1].split())
    return {
        "n_trade_rows": trade_nums[0],
        "n_traded_tickers": trade_nums[1],
        "n_open_tickers": _labeled(opened, "tickers"),
        "n_open_rows": _labeled(opened, "rows"),
        "n_open_missing": _labeled(missing, "open"),
        "n_closed_tickers": _labeled(missing, "closed"),
        "n_closed_rows": _labeled(missing, "rows"),
        "n_orphan_tickers": int(orphan.group(1).replace(",", "")),
        "n_excluded_tickers": _labeled(excluded, "tickers"),
        "n_excluded_events": _labeled(excluded, "events"),
        "n_excluded_rows": _labeled(excluded, "rows"),
        "n_eligible_tickers": _labeled(eligible, "tickers"),
        "n_eligible_events": _labeled(eligible, "events"),
        "n_eligible_rows": _labeled(eligible, "rows"),
        "selection_bias": selection,
        "coverage": coverage,
    }


def counts_match(expected, actual, n_eligible_events):
    pairs = (
        (expected["n_trade_rows"], actual["n_traded_rows"]),
        (expected["n_traded_tickers"], actual["n_traded_tickers"]),
        (expected["n_open_tickers"], actual["n_open_tickers"]),
        (expected["n_open_rows"], actual["n_open_rows"]),
        (expected["n_open_missing"], actual["n_open_missing"]),
        (expected["n_closed_tickers"], actual["n_closed_tickers"]),
        (expected["n_closed_rows"], actual["n_closed_rows"]),
        (expected["n_orphan_tickers"], actual["n_orphan_tickers"]),
        (expected["n_excluded_tickers"], actual["n_excluded_tickers_event"]),
        (expected["n_excluded_tickers"], actual["n_excluded_tickers_direct"]),
        (expected["n_excluded_events"], actual["n_excluded_events"]),
        (expected["n_excluded_rows"], actual["n_excluded_rows"]),
        (expected["n_eligible_tickers"], actual["n_eligible_tickers"]),
        (expected["n_eligible_events"], n_eligible_events),
        (expected["n_eligible_rows"], actual["n_eligible_rows"]),
    )
    return all(left == right for left, right in pairs)


def _eligible_events(doc, markets, n_rows):
    excluded = set(doc["excluded_tickers_event_level"])
    market_by = {market["ticker"]: market for market in markets}
    events = set()
    for ticker in n_rows:
        if ticker in excluded:
            continue
        market = market_by.get(ticker)
        if market is None:
            events.add(ticker.rsplit("-", 1)[0])
        else:
            events.add(market["event_ticker"])
    return len(events)


def _download_dir(trade_path, market_path):
    trade_parent = Path(trade_path).resolve().parent
    market_parent = Path(market_path).resolve().parent
    if trade_parent != market_parent:
        raise InconclusiveNoOutput("data files do not share a download directory")
    return trade_parent


def _overlaps(left, right):
    left = Path(left).resolve()
    right = Path(right).resolve()
    return left == right or left in right.parents or right in left.parents


def _normalize_row(row):
    for key, value in list(row.items()):
        if hasattr(value, "isoformat"):
            text = value.isoformat()
            row[key] = text[:-6] + "Z" if text.endswith("+00:00") else text
    for key in ("yes_price", "no_price", "count"):
        if key in row and row[key] is not None:
            row[key] = int(row[key])
    return row


def iter_parquet_rows(path, columns):
    """Stream an allow-listed column set. Batches are discarded after each yield."""
    for name in columns:
        if name in REFUSED_MARKET_FIELDS:
            raise BeckerQuoteFieldRefused(name)
    try:
        import pyarrow as pa
        import pyarrow.parquet as parquet
    except ImportError as exc:
        raise BoxOnlyRefused("parquet reader is not installed") from exc
    frame = parquet.ParquetFile(path)
    available = set(frame.schema_arrow.names)
    for name in columns:
        if name not in available:
            raise InconclusiveNoOutput("column")
    casts = {"count": pa.int32(), "yes_price": pa.int16(), "no_price": pa.int16()}
    for batch in frame.iter_batches(batch_size=65536, columns=columns):
        arrays = []
        for name in columns:
            column = batch.column(name)
            if name in casts:
                column = column.cast(casts[name], safe=False)
            arrays.append(column)
        cast = pa.RecordBatch.from_arrays(arrays, names=columns)
        columns_py = [cast.column(i).to_pylist() for i in range(len(columns))]
        for index in range(cast.num_rows):
            yield _normalize_row({name: columns_py[pos][index] for pos, name in enumerate(columns)})


def _fee_schedule_text():
    path = (
        LAB / "pins/k1/EXT_K1_authentic_pins_2026-10-03/lab/governance/astra/packets"
        / "scout_house_fee_2026-09-24/raw/docs/kalshi_fee_schedule.txt"
    )
    expected = "d9435b8b7e30fecbe1a07539990667b23b828a8175962c0882d6c7bce93980ec"
    if sha256_file(path) != expected:
        raise ManifestTamper("fee schedule")
    return path.read_text(encoding="utf-8", errors="replace")


def _net_enabled():
    path = LAB / "pins/governance/CONDUCTOR_ACCEPT_EXT_K2_FREEZE_2026-10-03.json"
    doc = json.loads(path.read_text(encoding="utf-8"))
    ruling = doc.get("rulings", {}).get("R39_net_fees", "")
    return isinstance(ruling, str) and ruling.startswith("ALLOW")


def _receipt(commit, runner_sha, manifest_sha, exclusion_sha, freeze_sha, freeze_json_sha, dir_sha):
    pinned_md, pinned_json = freeze_pin_shas()
    return {
        "type": "EXT-K2-PART-B-PRE-RUN-RECEIPT",
        "commit_sha": commit,
        "runner_file_sha256": runner_sha,
        "becker_boxonly_manifest_sha256": manifest_sha,
        "exclusion_list_sha256": exclusion_sha,
        "freeze_md_sha256": freeze_sha,
        "becker_dir_all_files_sha256": dir_sha,
        "pinned_manifest_sha256": MANIFEST_SHA,
        "pinned_exclusion_sha256": EXCLUSION_SHA,
        "pinned_freeze_md_sha256": pinned_md,
        "pinned_freeze_json_sha256": pinned_json if freeze_json_sha is None else freeze_json_sha,
        "manifest_sha_match": manifest_sha == MANIFEST_SHA,
        "exclusion_sha_match": exclusion_sha == EXCLUSION_SHA,
        "freeze_md_sha_match": freeze_sha == pinned_md,
    }


def _write_receipt(out_dir, receipt):
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "PRE_RUN_RECEIPT.json").write_bytes(canon_bytes(receipt))


def _data_paths(verified):
    trades = None
    markets = None
    for item, path in verified:
        if not is_data_table(item):
            continue
        kind = table_kind(item)
        if kind == "trades":
            if trades is not None:
                raise InconclusiveNoOutput("trades pin")
            trades = (item, path)
        elif kind == "markets":
            if markets is not None:
                raise InconclusiveNoOutput("markets pin")
            markets = (item, path)
    if trades is None or markets is None:
        raise InconclusiveNoOutput("runner pins did not yield t0 trades and markets")
    return trades, markets


def publish_or_refuse(out_dir, target, before_sha, download_dir):
    """Re-hash the download directory. A changed tree is not published."""
    after = directory_hash(download_dir)
    if after != before_sha:
        if Path(target).exists():
            Path(target).unlink()
        pointer = Path(out_dir) / "BOX_ONLY_OUTPUT_SHA256.json"
        if pointer.exists():
            pointer.unlink()
        raise InconclusiveNoOutput("download directory changed")
    digest = sha256_file(target)
    pointer = {"box_only_output_sha256": digest}
    (Path(out_dir) / "BOX_ONLY_OUTPUT_SHA256.json").write_bytes(canon_bytes(pointer))
    print(digest)
    return digest


def start_box_run(manifest_path, exclusion_path, freeze_md_path, run_dir, repo=None):
    """Hash pins, write the receipt, refuse on mismatch, and only then read tables."""
    manifest_path = Path(manifest_path)
    exclusion_path = Path(exclusion_path)
    freeze_md_path = Path(freeze_md_path)
    run_dir = Path(run_dir)
    if not manifest_path.is_file() or not exclusion_path.is_file() or not freeze_md_path.is_file():
        raise BoxOnlyRefused("box inputs are not on this filesystem")
    assert_outside_repo(run_dir)
    manifest_sha = sha256_file(manifest_path)
    exclusion_sha = sha256_file(exclusion_path)
    freeze_sha = sha256_file(freeze_md_path)
    pinned_md, pinned_json = freeze_pin_shas()
    commit = git_head(repo)
    runner_sha = sha256_file(RUNNER_PATH)
    matched = (
        manifest_sha == MANIFEST_SHA
        and exclusion_sha == EXCLUSION_SHA
        and freeze_sha == pinned_md
    )
    if not matched:
        _write_receipt(
            run_dir,
            _receipt(commit, runner_sha, manifest_sha, exclusion_sha, freeze_sha, pinned_json, None),
        )
        raise ReceiptMismatchRefused("INCONCLUSIVE")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("exclusion_list_sha256") not in (None, EXCLUSION_SHA):
        _write_receipt(
            run_dir,
            _receipt(commit, runner_sha, manifest_sha, exclusion_sha, freeze_sha, pinned_json, None),
        )
        raise ReceiptMismatchRefused("INCONCLUSIVE")
    (trade_item, trade_path), (market_item, market_path) = _data_paths([
        (item, resolve_item_path(manifest, item))
        for item in manifest.get("items", [])
        if isinstance(item, dict) and item.get("read_by_part_b_runner") is True
    ])
    download = _download_dir(trade_path, market_path)
    if not download.is_dir():
        raise InconclusiveNoOutput("download directory")
    if _overlaps(run_dir, download):
        raise BoxOnlyRefused("run directory overlaps the download directory")
    refuse_tier_path(download)
    dir_sha = directory_hash(download)
    _write_receipt(
        run_dir,
        _receipt(commit, runner_sha, manifest_sha, exclusion_sha, freeze_sha, pinned_json, dir_sha),
    )
    cloud_shas = cloud_input_shas()
    verified = verify_runner_item_shas(manifest)
    refuse_data_items(verified, cloud_shas)
    (trade_item, trade_path), (market_item, market_path) = _data_paths(verified)
    return _run_after_receipt(
        manifest, verified, exclusion_path, freeze_md_path, run_dir, download, dir_sha,
        trade_item, trade_path, market_item, market_path, cloud_shas,
    )


def _run_after_receipt(manifest, verified, exclusion_path, freeze_md_path, run_dir, download, dir_sha,
                       trade_item, trade_path, market_item, market_path, cloud_shas):
    del manifest, verified, cloud_shas
    expectations = parse_freeze_expectations(freeze_md_path.read_text(encoding="utf-8"))
    pinned = json.loads(exclusion_path.read_text(encoding="utf-8"))
    trades_sha = trade_item.get("sha256")
    markets_sha = market_item.get("sha256")
    holdout_events, holdout_game_ids = load_holdout_sets()
    try:
        markets = list(iter_parquet_rows(market_path, market_columns()))
    except IntegrityRefused as exc:
        raise InconclusiveNoOutput("integrity") from exc
    for market in markets:
        assert_not_holdout(
            event=market.get("event_ticker"),
            ticker=market.get("ticker"),
            game_id=None,
            holdout_events=holdout_events,
            holdout_game_ids=holdout_game_ids,
        )
    scan = empty_scan()
    try:
        for row in iter_parquet_rows(trade_path, trade_columns()):
            if row.get("created_time") is not None:
                assert_timestamp_allowed(row["created_time"])
            note_trade(scan, row)
    except IntegrityRefused as exc:
        raise InconclusiveNoOutput("integrity") from exc
    recomputed = exclusion_from_scan(
        markets, scan, source_trades_sha256=trades_sha, source_markets_sha256=markets_sha, rule=pinned.get("rule", ""),
    )
    compare_exclusion(pinned, recomputed, trades_sha, markets_sha)
    actual = summarize_counts(recomputed, scan["n_rows"])
    n_events = _eligible_events(recomputed, markets, scan["n_rows"])
    if not counts_match(expectations, actual, n_events):
        raise InconclusiveNoOutput("exclusion counts")
    excluded = set(recomputed["excluded_tickers_event_level"])
    market_by = {row["ticker"]: row for row in markets if row["ticker"] not in excluded}
    registry = load_registry(LAB / "pins" / "bands_registry_10c.json")
    multiplier = read_kxnflgame_multiplier(_fee_schedule_text())
    acc = Accumulator()
    for row in iter_parquet_rows(trade_path, trade_columns()):
        ticker = row["ticker"]
        if ticker in excluded:
            continue
        market = market_by.get(ticker)
        if market is None:
            raise InconclusiveNoOutput("market")
        assert_not_holdout(
            event=market.get("event_ticker"),
            ticker=ticker,
            game_id=row.get("game_id"),
            holdout_events=holdout_events,
            holdout_game_ids=holdout_game_ids,
        )
        if row.get("created_time") is not None:
            assert_timestamp_allowed(row["created_time"])
        acc.add(prepare_trade(row, market, registry, multiplier))
    document = document_from_events(
        acc.finish(), net_enabled=_net_enabled(),
        selection_bias=expectations["selection_bias"], coverage=expectations["coverage"],
    )
    document["label"] = "DESCRIPTIVE"
    document["exclusion_list_sha256"] = EXCLUSION_SHA
    document["box_only_output_sha256"] = None
    Provenanced([{"table": "trades"}], "BECKER_A")
    Provenanced([{"table": "markets"}], "BECKER_A")
    target = write_aggregates(document, run_dir, scan["seen"], list(scan["n_rows"]))
    return publish_or_refuse(run_dir, target, dir_sha, download)


def read_table(path, columns):
    """Project an allow-listed column set. Refused market fields raise before any read."""
    refuse_tier_path(path)
    for name in columns:
        if name in REFUSED_MARKET_FIELDS:
            raise BeckerQuoteFieldRefused(name)
    raise BoxOnlyRefused("parquet reads stay on the box")


def expected_columns():
    return {"trades": trade_columns(), "markets": market_columns()}


def main(argv=None):
    parser = argparse.ArgumentParser(prog="becker_pipeline.run_part_b")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--exclusion", required=True)
    parser.add_argument("--freeze-md", required=True)
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args(argv)
    start_box_run(args.manifest, args.exclusion, args.freeze_md, args.run_dir)


if __name__ == "__main__":
    main()
