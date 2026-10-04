"""Post-settlement join. Sets y from a settled-results file. Does not reorder."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def join(rows, results_doc):
    """Copy rows in order. y = 1 for yes, 0 for no, otherwise unchanged."""
    results = results_doc.get("results") if isinstance(results_doc, dict) else None
    if not isinstance(results, list):
        raise ValueError("results must be a list")
    index = {}
    conflicts = set()
    for item in results:
        if not isinstance(item, dict):
            continue
        ticker = item.get("ticker")
        result = item.get("result")
        if ticker in index and index[ticker] != result:
            conflicts.add(ticker)
        index[ticker] = result
    out = []
    for row in rows:
        copied = dict(row)
        ticker = copied.get("ticker")
        if ticker not in conflicts:
            result = index.get(ticker)
            if result == "yes":
                copied["y"] = 1
            elif result == "no":
                copied["y"] = 0
        out.append(copied)
    return {"rows": out}


def main(argv):
    if len(argv) != 2:
        print("usage: python -m card01_amc.join_outcomes rows.json results.json", file=sys.stderr)
        return 2
    rows_doc = json.loads(Path(argv[0]).read_text())
    rows = rows_doc["rows"] if isinstance(rows_doc, dict) else rows_doc
    results = json.loads(Path(argv[1]).read_text())
    json.dump(join(rows, results), sys.stdout, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
