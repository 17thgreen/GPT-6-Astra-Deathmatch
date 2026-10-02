"""Post-fill settlement join. Three arguments. Runs only on hashed fill bytes.

Guard fields stay inside this module. They are not copied onto fill rows.
"""
import hashlib
import json
from decimal import Decimal
from pathlib import Path

from tape_quotes import (
    Admit1WindowRejected,
    ClosedUniverseRefused,
    LabError,
    assert_open_universe,
    in_admit1_window,
    parse_ts,
    sha256_file,
)


class PreCloseJoinRefused(LabError):
    pass


class SettlementValueRefused(LabError):
    pass


class JoinIntegrityError(LabError):
    pass


_ALLOWED = (
    'ticker',
    'status',
    'close_time',
    'settlement_ts',
    'settlement_value_dollars',
)


def _sha_bytes(payload):
    return hashlib.sha256(payload).hexdigest()


def _digest_rows(text):
    rows = []
    for line in text.splitlines():
        if not line.strip():
            continue
        digest, rel = line.split('  ', 1)
        rows.append((digest, rel))
    return rows


def _pick(market):
    if not isinstance(market, dict):
        raise JoinIntegrityError('market')
    picked = {}
    for key in _ALLOWED:
        if key in market:
            picked[key] = market[key]
    return picked


def _load_settlement(settlement_dir):
    root = Path(settlement_dir)
    ready_path = root / 'COLLECTOR_READY_SETTLEMENT_ONLY.json'
    digests_path = root / 'DIGESTS.txt'
    requests_path = root / 'requests.jsonl'
    ready = json.loads(ready_path.read_text())
    digests_bytes = digests_path.read_bytes()
    if ready.get('digests_txt_sha256') != _sha_bytes(digests_bytes):
        raise JoinIntegrityError('digests')
    listing = _digest_rows(digests_bytes.decode('utf-8'))
    listed = {}
    for digest, rel in listing:
        target = root / rel
        got = sha256_file(target)
        if got != digest:
            raise JoinIntegrityError(rel)
        listed[rel] = digest
    requests = []
    for line in requests_path.read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get('http_status') != 200:
            raise JoinIntegrityError('http_status')
        rel = row['raw_path']
        raw_path = root / rel
        got = sha256_file(raw_path)
        claimed = row.get('sha256')
        if got != claimed or listed.get(rel) != claimed:
            raise JoinIntegrityError(rel)
        ticker = assert_open_universe(row['ticker'])
        response_utc = row['response_utc']
        if in_admit1_window(response_utc):
            raise Admit1WindowRejected(response_utc)
        body = json.loads(raw_path.read_text())
        market = _pick(body.get('market') or {})
        if market.get('ticker') != ticker:
            raise JoinIntegrityError('ticker')
        requests.append({
            'ticker': ticker,
            'response_utc': response_utc,
            'sha256': claimed,
            'market': market,
        })
    return requests


def _value_ok(text):
    if not isinstance(text, str):
        raise SettlementValueRefused(text)
    try:
        value = Decimal(text)
    except Exception as exc:
        raise SettlementValueRefused(text) from exc
    if value not in (Decimal('0'), Decimal('1')):
        raise SettlementValueRefused(text)
    return text


def _guard_times(market, response_utc, fill_rows):
    if market.get('status') != 'finalized':
        raise PreCloseJoinRefused('status')
    close_text = market.get('close_time')
    settle_text = market.get('settlement_ts')
    if not close_text or not settle_text or not response_utc:
        raise PreCloseJoinRefused('clock')
    if in_admit1_window(settle_text):
        raise Admit1WindowRejected(settle_text)
    close = parse_ts(close_text)
    settle = parse_ts(settle_text)
    response = parse_ts(response_utc)
    if not (close < settle < response and close < response):
        raise PreCloseJoinRefused('order')
    for row in fill_rows:
        if not row.get('filled'):
            continue
        fill_time = row.get('fill_time')
        if not fill_time:
            raise PreCloseJoinRefused('fill_time')
        if parse_ts(fill_time) >= close:
            raise PreCloseJoinRefused('fill_time')


def settled_join(fills_bytes, fills_sha256, settlement_dir):
    """Join hashed fills to settlement dollars. Signature is exactly these three arguments."""
    if not isinstance(fills_bytes, (bytes, bytearray)):
        raise JoinIntegrityError('fills_bytes')
    if _sha_bytes(fills_bytes) != fills_sha256:
        raise JoinIntegrityError('fills_sha256')
    payload = json.loads(fills_bytes.decode('utf-8'))
    fill_rows = payload.get('rows') or []
    by_ticker = {}
    for row in fill_rows:
        ticker = assert_open_universe(row['ticker'])
        by_ticker.setdefault(ticker, []).append(row)
    loaded = _load_settlement(settlement_dir)
    values = {}
    raw_sha256 = {}
    for item in loaded:
        ticker = item['ticker']
        if ticker in values:
            raise JoinIntegrityError('duplicate')
        market = item['market']
        _guard_times(market, item['response_utc'], by_ticker.get(ticker, []))
        values[ticker] = _value_ok(market.get('settlement_value_dollars'))
        raw_sha256[ticker] = item['sha256']
    unresolved = []
    for ticker, rows in by_ticker.items():
        if any(row.get('filled') for row in rows) and ticker not in values:
            unresolved.append(ticker)
    unresolved.sort()
    return {
        'values': values,
        'unresolved_tickers': unresolved,
        'settled_join_n': len(values),
        'raw_sha256': raw_sha256,
    }


def assert_join_manifest(joined, manifest_bytes):
    """Cross-check the pinned manifest. It is not an argument of settled_join."""
    if not isinstance(manifest_bytes, (bytes, bytearray)):
        raise JoinIntegrityError('manifest')
    manifest = json.loads(manifest_bytes.decode('utf-8'))
    if manifest.get('all_sep25_in_panel_no_sep24') is not True:
        raise JoinIntegrityError('scope')
    rows = manifest.get('rows') or []
    if len(rows) != 6:
        raise JoinIntegrityError('rows')
    seen = {}
    shas = {}
    for row in rows:
        ticker = row.get('ticker')
        if row.get('sep24') is True:
            raise ClosedUniverseRefused(ticker)
        assert_open_universe(ticker)
        seen[ticker] = row.get('settlement_value_dollars')
        shas[ticker] = row.get('raw_sha256')
    if set(seen) != set(joined['values']) or set(shas) != set(joined['raw_sha256']):
        raise JoinIntegrityError('tickers')
    for ticker, value in seen.items():
        if joined['values'].get(ticker) != value:
            raise JoinIntegrityError(ticker)
        if joined['raw_sha256'].get(ticker) != shas[ticker]:
            raise JoinIntegrityError(ticker)
    return True


def settlement_folder_digest(settlement_dir):
    """sha256 of the sorted sha256sum listing. The listing text is not file bytes."""
    root = Path(settlement_dir)
    rels = sorted(
        path.relative_to(root).as_posix()
        for path in root.rglob('*')
        if path.is_file()
    )
    lines = []
    for rel in rels:
        lines.append('%s  ./%s\n' % (sha256_file(root / rel), rel))
    blob = ''.join(lines).encode('utf-8')
    return hashlib.sha256(blob).hexdigest()
