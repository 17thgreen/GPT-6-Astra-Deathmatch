"""Box-only runner. This checkout has no Becker rows, so start() refuses."""

import hashlib
import json
from pathlib import Path

from becker_pipeline.exclusion import market_columns, recompute_exclusion, trade_columns
from becker_pipeline.guards import REFUSED_MARKET_FIELDS, refuse_becker_input, refuse_tier_path
from becker_pipeline.metrics import build_cells
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

MANIFEST_SHA = "fd5e10531f488f30baf05e2dd6f17c8f8823603ecbae457170dbbde66126fb95"
EXCLUSION_SHA = "61a4c993fbea5940e5999177ffb5a0e3161219a8f84812af2d2f44d9f556641b"
RUNNER_PATH = Path(__file__).resolve()


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


def _receipt(commit, runner_sha, manifest_sha, exclusion_sha, dir_sha):
    return {
        "type": "EXT-K2-PART-B-PRE-RUN-RECEIPT",
        "commit_sha": commit,
        "runner_file_sha256": runner_sha,
        "becker_boxonly_manifest_sha256": manifest_sha,
        "exclusion_list_sha256": exclusion_sha,
        "becker_dir_all_files_sha256": dir_sha,
        "pinned_manifest_sha256": MANIFEST_SHA,
        "pinned_exclusion_sha256": EXCLUSION_SHA,
        "manifest_sha_match": manifest_sha == MANIFEST_SHA,
        "exclusion_sha_match": exclusion_sha == EXCLUSION_SHA,
    }


def start_box_run(becker_dir, manifest_path, exclusion_path, out_dir, repo=None):
    """Hash pins, write the receipt, then refuse on mismatch before any table read."""
    becker_dir = Path(becker_dir)
    out_dir = Path(out_dir)
    if not becker_dir.is_dir():
        raise BoxOnlyRefused("Becker directory is not on this filesystem")
    assert_outside_repo(out_dir)
    refuse_tier_path(becker_dir)
    manifest_sha = sha256_file(manifest_path)
    exclusion_sha = sha256_file(exclusion_path)
    runner_sha = sha256_file(RUNNER_PATH)
    dir_sha = directory_hash(becker_dir)
    commit = git_head(repo)
    receipt = _receipt(commit, runner_sha, manifest_sha, exclusion_sha, dir_sha)
    out_dir.mkdir(parents=True, exist_ok=True)
    receipt_path = out_dir / "PRE_RUN_RECEIPT.json"
    receipt_path.write_bytes(canon_bytes(receipt))
    if manifest_sha != MANIFEST_SHA or exclusion_sha != EXCLUSION_SHA:
        raise ReceiptMismatchRefused("INCONCLUSIVE")
    return _run_after_receipt(
        becker_dir, Path(manifest_path), Path(exclusion_path), out_dir, cloud_input_shas(),
    )


# Published structural counts. A mismatch is INCONCLUSIVE and writes no aggregate.
_EXPECTED_COUNTS = {
    "n_open_at_trade_fetch": 56,
    "n_closed_no_result": 8,
    "n_excluded_tickers": 64,
    "n_excluded_events": 33,
    "n_excluded_rows": 705549,
    "n_eligible_tickers": 420,
    "n_eligible_events": 210,
    "n_eligible_rows": 7592418,
}


def _manifest_items(doc):
    if isinstance(doc, list):
        return doc
    if isinstance(doc, dict):
        for key in ("items", "files", "pins"):
            if isinstance(doc.get(key), list):
                return doc[key]
    raise InconclusiveNoOutput("box manifest schema is not a pin list")


def _resolve_pin(becker_dir, item):
    raw = item.get("path") or item.get("relpath")
    if not raw:
        raise InconclusiveNoOutput("box manifest item has no path")
    path = Path(raw)
    if not path.is_absolute():
        candidate = becker_dir / path
        path = candidate if candidate.is_file() else path
    return path


def _run_after_receipt(becker_dir, manifest_path, exclusion_path, out_dir, cloud_shas):
    """Read tables only after the receipt shas matched. Writes aggregates outside the repo."""
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise InconclusiveNoOutput("box manifest is not JSON") from exc
    trades = None
    markets = None
    for item in _manifest_items(manifest):
        if not item.get("read_by_part_b_runner"):
            continue
        path = _resolve_pin(becker_dir, item)
        expected = item.get("sha256")
        refuse_becker_input(path, sha=expected, cloud_shas=cloud_shas)
        refuse_tier_path(path)
        if expected is None or sha256_file(path) != expected:
            raise ManifestTamper(str(path))
        name = path.name
        if "trades" in name:
            trades = _rows_from_parquet(path, trade_columns())
        elif "markets" in name:
            markets = _rows_from_parquet(path, market_columns())
    if trades is None or markets is None:
        raise InconclusiveNoOutput("runner pins did not yield t0 trades and markets")
    Provenanced(trades, "BECKER_A")
    Provenanced(markets, "BECKER_A")
    try:
        exclusion = recompute_exclusion(markets, trades)
    except IntegrityRefused as exc:
        raise InconclusiveNoOutput("integrity") from exc
    for key, expected in _EXPECTED_COUNTS.items():
        if exclusion.get(key) != expected:
            raise InconclusiveNoOutput("exclusion counts")
    pinned = exclusion_path.read_bytes()
    recomputed = canon_bytes(exclusion)
    if pinned != recomputed:
        try:
            pinned_doc = json.loads(pinned.decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise InconclusiveNoOutput("exclusion document") from exc
        pinned_ids = pinned_doc.get("excluded_tickers")
        if pinned_ids is None or set(pinned_ids) != set(exclusion["excluded_tickers"]):
            raise InconclusiveNoOutput("exclusion membership")
    eligible = set(exclusion["eligible_tickers"])
    market_by = {row["ticker"]: row for row in markets if row["ticker"] in eligible}
    kept = [row for row in trades if row["ticker"] in eligible]
    holdout_events, holdout_game_ids = load_holdout_sets()
    registry = load_registry(Path(__file__).resolve().parents[1] / "pins" / "bands_registry_10c.json")
    schedule = _fee_schedule_text()
    multiplier = read_kxnflgame_multiplier(schedule)
    document = build_cells(
        kept, market_by, registry, multiplier, exclusion["excluded_tickers"],
        net_enabled=True, holdout_events=holdout_events, holdout_game_ids=holdout_game_ids,
    )
    document["label"] = "DESCRIPTIVE"
    document["exclusion_list_sha256"] = EXCLUSION_SHA
    document["box_only_output_sha256"] = None
    target = write_aggregates(
        document, out_dir, [row["trade_id"] for row in trades], [row["ticker"] for row in trades],
    )
    digest = sha256_file(target)
    pointer = {"box_only_output_sha256": digest}
    (out_dir / "BOX_ONLY_OUTPUT_SHA256.json").write_bytes(canon_bytes(pointer))
    print(digest)
    return digest


def _fee_schedule_text():
    path = (
        Path(__file__).resolve().parents[1]
        / "pins/k1/EXT_K1_authentic_pins_2026-10-03/lab/governance/astra/packets"
        / "scout_house_fee_2026-09-24/raw/docs/kalshi_fee_schedule.txt"
    )
    expected = "d9435b8b7e30fecbe1a07539990667b23b828a8175962c0882d6c7bce93980ec"
    if sha256_file(path) != expected:
        raise ManifestTamper("fee schedule")
    return path.read_text(encoding="utf-8", errors="replace")


def _rows_from_parquet(path, columns):
    for name in columns:
        if name in REFUSED_MARKET_FIELDS:
            raise BeckerQuoteFieldRefused(name)
    try:
        import pyarrow.parquet as parquet
    except ImportError as exc:
        raise BoxOnlyRefused("parquet reader is not installed") from exc
    table = parquet.read_table(path, columns=columns)
    rows = table.to_pylist()
    for row in rows:
        for key, value in list(row.items()):
            if hasattr(value, "isoformat"):
                text = value.isoformat()
                row[key] = text[:-6] + "Z" if text.endswith("+00:00") else text
    return rows


def read_table(path, columns):
    """Project an allow-listed column set. Refused market fields raise."""
    refuse_tier_path(path)
    for name in columns:
        if name in REFUSED_MARKET_FIELDS:
            raise BeckerQuoteFieldRefused(name)
    raise BoxOnlyRefused("parquet reads stay on the box")


def expected_columns():
    return {"trades": trade_columns(), "markets": market_columns()}


def main():
    root = _repo_root()
    start_box_run(
        root / "lab/astra-capture/external/becker_2026-10-03/data",
        root / "lab/astra-capture/external/ext_k2_becker_boxonly_2026-10-03/BECKER_BOXONLY_PIN_MANIFEST.json",
        root / "lab/astra-capture/external/ext_k2_becker_boxonly_2026-10-03/BECKER_EXCLUSION_LIST_KXNFLGAME.json",
        Path("/tmp/ext-k2-part-b-refused"),
    )


if __name__ == "__main__":
    main()
