"""Bounded GET-only research utilities. No authenticated/order endpoints."""
import gzip
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
M2 = REPO / 'cross_sport_replay_20260922'
M3 = REPO / 'market_adaptation_20260922'
sys.path.insert(0, str(M2))
from discover import get, epoch


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')


def read(path):
    return json.loads(Path(path).read_text())


def write_rows(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(path, 'wt') as stream:
        for row in rows:
            stream.write(json.dumps(row, separators=(',', ':')) + '\n')


def lines(path):
    with gzip.open(path, 'rt') as stream:
        yield from (json.loads(line) for line in stream)


def pages(path, params, limit=20):
    cursor, seen, result = None, set(), []
    for _ in range(limit):
        query = dict(params)
        if cursor:
            query['cursor'] = cursor
        data, source = get(path, query)
        result.append(dict(response=data, source=source))
        cursor = data.get('cursor')
        if not cursor:
            return result
        if cursor in seen:
            raise ValueError('Repeated cursor')
        seen.add(cursor)
    raise ValueError('Pagination limit reached')
