"""CLI. Inputs come only from SOURCE_PINS.json. No path override."""

import argparse
import json
import sys
from pathlib import Path

from .canonical import canonical_bytes, canonical_sha256
from .constants import BUILDER_RELATIVE_PATH, PRODUCTION_PINS
from .errors import SourcePinMismatch
from .pins_io import (
    REPO_ROOT,
    entry_by_role,
    load_verified_json,
    read_git_commit,
    sweeps_module_sha256,
    verify_run_pins,
)
from .report import (
    body_if_sweeps_sha_differs,
    build_receipt,
    build_results,
    published_results,
    structure_timestamp_malformed,
)
from .tape import iter_jsonl_gz, load_jsonl_gz


def build_parser():
    parser = argparse.ArgumentParser(prog="ext2k1")
    commands = parser.add_subparsers(dest="command", required=True)
    receipt = commands.add_parser("receipt")
    receipt.add_argument("--out-dir", required=True)
    score = commands.add_parser("score")
    score.add_argument("--receipt", required=True)
    score.add_argument("--receipt-sha256", required=True)
    score.add_argument("--out-dir", required=True)
    return parser


def output_dir_in_repo(path):
    resolved = Path(path).resolve()
    cursor = resolved
    while True:
        if (cursor / ".git").exists():
            return True
        parent = cursor.parent
        if parent == cursor:
            return False
        cursor = parent


def _fail(message, code=2):
    print(message, file=sys.stderr)
    return code


def _write(path, obj):
    Path(path).write_bytes(canonical_bytes(obj))


def _load_tape_rows(tape_path):
    return list(iter_jsonl_gz(tape_path))


def _production_inputs():
    """Hash every pin first. A bad quote builder is a C2 fact, not SourcePinMismatch."""
    checked = verify_run_pins()
    builder = entry_by_role(checked, "B1 quote builder")
    if builder["path"] != BUILDER_RELATIVE_PATH:
        raise SourcePinMismatch("B1 quote builder")
    markets = load_verified_json("B1 markets")
    week_membership = load_verified_json("B1 cohort")
    tape_path = REPO_ROOT / entry_by_role(checked, "B1 dev tape")["path"]
    rows = _load_tape_rows(tape_path)
    return checked, builder["sha256"], markets, week_membership, rows


def cmd_receipt(out_dir):
    if output_dir_in_repo(out_dir):
        return _fail("OUTPUT_PATH_IN_REPO")
    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    checked, builder_sha, markets, week_membership, rows = _production_inputs()
    receipt, document = build_receipt(
        rows,
        markets,
        week_membership,
        PRODUCTION_PINS,
        builder_sha256=builder_sha,
        source_pins=checked,
        sweeps_module_sha256=sweeps_module_sha256(),
    )
    _write(destination / "SWEEPS.json", document)
    _write(destination / "RECEIPT.json", receipt)
    print("receipt_sha256 " + canonical_sha256(receipt))
    print("sweeps_sha256 " + receipt["sweeps_sha256"])
    return 0


def _gates_ok(record):
    return bool(record.get("count_gate", {}).get("pass")) and bool(
        record.get("structure_gate", {}).get("pass")
    ) and bool(record.get("b1_quote_builder", {}).get("match"))


def cmd_score(receipt_path, receipt_sha, out_dir):
    if output_dir_in_repo(out_dir):
        return _fail("OUTPUT_PATH_IN_REPO")
    try:
        payload = json.loads(Path(receipt_path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return _fail("RECEIPT_NOT_VERIFIED")
    if canonical_sha256(payload) != str(receipt_sha).strip().lower():
        return _fail("RECEIPT_NOT_VERIFIED")
    checked, builder_sha, markets, week_membership, rows = _production_inputs()
    module_sha = sweeps_module_sha256()
    receipt, _document = build_receipt(
        rows,
        markets,
        week_membership,
        PRODUCTION_PINS,
        builder_sha256=builder_sha,
        source_pins=checked,
        sweeps_module_sha256=module_sha,
    )
    # A malformed trade time is V1s. Do not build sweeps, and do not refuse with no output.
    if not structure_timestamp_malformed(receipt):
        mismatch = body_if_sweeps_sha_differs(receipt, payload.get("sweeps_sha256"), read_git_commit())
        if mismatch is not None:
            destination = Path(out_dir)
            destination.mkdir(parents=True, exist_ok=True)
            published = published_results(mismatch)
            _write(destination / "RESULTS.json", published)
            print("output_sha256 " + published["output_sha256"])
            return 0
        if _gates_ok(payload) != _gates_ok(receipt):
            return _fail("RECEIPT_NOT_VERIFIED")
    b2_rows = None
    if _gates_ok(receipt):
        b2_path = REPO_ROOT / entry_by_role(checked, "B2 000 fills")["path"]
        b2_rows = load_jsonl_gz(b2_path)
    _receipt, _document, body = build_results(
        rows,
        markets,
        week_membership,
        PRODUCTION_PINS,
        builder_sha256=builder_sha,
        source_pins=checked,
        sweeps_module_sha256=module_sha,
        b2_rows=b2_rows,
        git_commit=read_git_commit(),
    )
    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    published = published_results(body)
    _write(destination / "RESULTS.json", published)
    print("output_sha256 " + published["output_sha256"])
    return 0


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "receipt":
            return cmd_receipt(args.out_dir)
        if args.command == "score":
            return cmd_score(args.receipt, args.receipt_sha256, args.out_dir)
    except SourcePinMismatch:
        print("SourcePinMismatch", file=sys.stderr)
        return 1
    return _fail("RECEIPT_NOT_VERIFIED")


if __name__ == "__main__":
    sys.exit(main())
