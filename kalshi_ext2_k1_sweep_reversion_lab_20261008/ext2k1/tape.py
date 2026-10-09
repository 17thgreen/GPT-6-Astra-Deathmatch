"""Stream a gzip JSONL tape one line at a time. No other I/O."""

import gzip
import json


def iter_jsonl_gz(path):
    with gzip.open(path, "rb") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line.decode("utf-8"))


def load_jsonl_gz(path):
    return list(iter_jsonl_gz(path))
