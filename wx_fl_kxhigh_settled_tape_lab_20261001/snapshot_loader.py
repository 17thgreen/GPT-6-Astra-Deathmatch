"""Read-only loader for the pinned WX-FL snapshot.

sqlite3 is imported only in this module. The database is opened with
file:...?mode=ro&immutable=1 after the tarball, MANIFEST, and snapshot
sha256 checks. Live weather archive paths and capture.sqlite are refused
and are not opened.
"""

import hashlib
import json
import sqlite3
import tarfile
import tempfile
import zlib
from pathlib import Path


LAB_ROOT = Path(__file__).resolve().parent
PINS = LAB_ROOT / 'pins'
BUNDLE_TGZ = PINS / 'WX_FL_KXHIGH_SETTLED_TAPE_authentic_pins_2026-10-01.tgz'
BUNDLE_DIRNAME = 'WX_FL_KXHIGH_SETTLED_TAPE_authentic_pins_2026-10-01'
BUNDLE_SHA256 = 'febc74af09b06db83fb686e904d6f3e305fe30414e4c4f67c05705f0de597807'
SNAPSHOT_REL = Path(
    'lab/governance/astra/packets/WX_FL_KXHIGH_SETTLED_TAPE/snapshot/archive.sqlite'
)
SNAPSHOT_SHA256 = 'd20d5e7d0cedc79ed77c92e905b2824f0ca1d79f8e524635bfd3a8f0e3c6eae2'
SNAPSHOT_BYTES = 94629888
GAPS_REL = Path(
    'lab/governance/astra/packets/WX_FL_KXHIGH_SETTLED_TAPE/GAP_LOG_gaps_table_export_2026-10-01.jsonl'
)
GAPS_SHA256 = '0211f5ca2fc6e9ec3ed0c889c5ed50e3ba35360f048a28986116892f090447f6'
POLLS_REL = Path(
    'lab/governance/astra/packets/WX_FL_KXHIGH_SETTLED_TAPE/GAP_LOG_trades_polls_export_2026-10-01.jsonl'
)
POLLS_SHA256 = 'a287572c53a69da5baa99f4f6746c9e31c2f58648a10fe9128ef381261d81cf8'
FROZEN_REL = Path(
    'lab/governance/astra/packets/WX_FL_KXHIGH_SETTLED_TAPE/FROZEN_EXPERIMENT.json'
)
FROZEN_SHA256 = '325013a62e5a1ee46285942e952f22af24abdc09947726cdcc31c9cf3cae6f1d'
REGISTRY_REL = Path('lab/governance/astra/packets/r3_p3_fl_maker_taker/bands_registry_10c.json')
REGISTRY_SHA256 = '0860cbe28d28ecc6142ddf6f1ebb67792084264ed82e0b4d868c3b3138ea5312'
SERIES = ('KXHIGHCHI', 'KXHIGHLAX', 'KXHIGHMIA', 'KXHIGHNY')
W0 = '2026-09-27T00:00:00Z'
W1 = '2026-09-30T04:00:00Z'
GAP_COLUMNS = ('id', 'stream', 'key', 'started_at', 'ended_at', 'reason', 'detail', 'n_polls')
POLL_COLUMNS = (
    'id', 'run_id', 'stream', 'key', 'url', 'requested_at', 'received_at',
    'http_status', 'ok', 'n_items', 'n_new', 'latency_ms', 'error',
)
TRADE_RAW_KEYS = ('taker_outcome_side', 'taker_book_side', 'is_block_trade', 'taker_side')

_FRAME = None


class SnapshotLoaderError(Exception):
    """The snapshot path is refused or a pin does not match."""


class SnapshotShaMismatch(SnapshotLoaderError):
    """A sha256 did not match. The database is not opened."""


class ManifestShaMismatch(SnapshotLoaderError):
    """A MANIFEST.sha256 line did not match. The payload is not used."""


class LiveDatabaseRefused(SnapshotLoaderError):
    """The live weather archive is not an input."""


class CaptureSqliteRefused(SnapshotLoaderError):
    """capture.sqlite is not opened."""


class ResultDisagreement(SnapshotLoaderError):
    """Later finalized rows disagree with the first finalized result."""


class UniverseMismatch(SnapshotLoaderError):
    """The snapshot universe is not the frozen 48 markets."""


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as handle:
        while True:
            block = handle.read(1024 * 1024)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def assert_sha256(path, expected):
    actual = sha256_file(path)
    if actual != expected:
        raise SnapshotShaMismatch(path)
    return actual


def assert_path_allowed(path):
    text = str(path).replace('\\', '/')
    name = Path(text).name
    if name == 'capture.sqlite' or text.endswith('/capture.sqlite'):
        raise CaptureSqliteRefused(text)
    if '/weather-nowcast/archive.sqlite' in text:
        raise LiveDatabaseRefused(text)
    return text


def ro_immutable_uri(path):
    """Build the sqlite URI. The path is not opened here."""
    text = str(Path(path).resolve())
    if any(mark in text for mark in ('?', '#', '%')):
        raise SnapshotLoaderError('uri')
    return 'file:%s?mode=ro&immutable=1' % text


def open_snapshot(path, expected_sha256):
    """Verify sha256, then open mode=ro&immutable=1. Nothing is written."""
    assert_path_allowed(path)
    assert_sha256(path, expected_sha256)
    uri = ro_immutable_uri(path)
    if 'mode=ro&immutable=1' not in uri:
        raise SnapshotLoaderError('uri')
    return sqlite3.connect(uri, uri=True)


def verify_manifest(root):
    """sha256sum -c equivalent for MANIFEST.sha256. Mismatch raises before use."""
    root = Path(root)
    manifest = root / 'MANIFEST.sha256'
    if not manifest.is_file():
        raise ManifestShaMismatch('MANIFEST.sha256')
    for line in manifest.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        digest, relative = line.split('  ', 1)
        target = root / relative
        if not target.is_file() or sha256_file(target) != digest:
            raise ManifestShaMismatch(relative)
    return True


def _json_export(rows):
    lines = []
    for row in rows:
        lines.append(json.dumps(row, sort_keys=True, separators=(',', ':')))
    text = '\n'.join(lines)
    if lines:
        text += '\n'
    return text.encode('utf-8')


def _rows(connection, sql, columns):
    exported = []
    for record in connection.execute(sql):
        exported.append(dict(zip(columns, record)))
    return exported


def regenerate_gap_exports(connection):
    gaps = _rows(
        connection,
        'SELECT id, stream, key, started_at, ended_at, reason, detail, n_polls '
        'FROM gaps ORDER BY id',
        GAP_COLUMNS,
    )
    polls = _rows(
        connection,
        "SELECT id, run_id, stream, key, url, requested_at, received_at, "
        'http_status, ok, n_items, n_new, latency_ms, error '
        "FROM polls WHERE stream='kalshi_trades' ORDER BY id",
        POLL_COLUMNS,
    )
    return _json_export(gaps), _json_export(polls), gaps, polls


def _timestamp_keys(blob):
    payload = json.loads(zlib.decompress(blob))
    return payload.get('settlement_ts'), payload.get('open_time')


def _parse_epoch_text(value):
    # Local copy of the feasibility parser so this module does not need gap_mapping
    # at import time for the universe filter. gap_mapping.parse_epoch is equivalent.
    from gap_mapping import parse_epoch
    return parse_epoch(value)


def _in_admit1(epoch, w0, w1):
    return w0 <= epoch < w1


def load_frame(bundle_tgz=None, dest=None):
    """Extract the pinned tarball, verify hashes, and return count inputs.

    The returned trades carry the fields arm assignment needs. Callers that
    write measurement files must not emit those prices.
    """
    global _FRAME
    if bundle_tgz is None and dest is None and _FRAME is not None:
        return _FRAME
    frame = _load_frame(bundle_tgz or BUNDLE_TGZ, dest)
    if bundle_tgz is None and dest is None:
        _FRAME = frame
    return frame


def _load_frame(bundle_tgz, dest):
    bundle_tgz = Path(bundle_tgz)
    assert_path_allowed(bundle_tgz)
    assert_sha256(bundle_tgz, BUNDLE_SHA256)
    owned = None
    if dest is None:
        owned = tempfile.TemporaryDirectory(prefix='wxfl-bundle-')
        dest = Path(owned.name)
    else:
        dest = Path(dest)
        dest.mkdir(parents=True, exist_ok=True)
    try:
        with tarfile.open(bundle_tgz, 'r:*') as archive:
            archive.extractall(dest, filter='data')
        root = dest / BUNDLE_DIRNAME
        verify_manifest(root)
        snapshot = root / SNAPSHOT_REL
        if snapshot.stat().st_size != SNAPSHOT_BYTES:
            raise SnapshotShaMismatch('snapshot bytes')
        connection = open_snapshot(snapshot, SNAPSHOT_SHA256)
        try:
            gap_bytes, poll_bytes, gap_rows, poll_rows = regenerate_gap_exports(connection)
            if hashlib.sha256(gap_bytes).hexdigest() != GAPS_SHA256:
                raise ManifestShaMismatch('gap export')
            if hashlib.sha256(poll_bytes).hexdigest() != POLLS_SHA256:
                raise ManifestShaMismatch('poll export')
            pinned_gaps = (root / GAPS_REL).read_bytes()
            pinned_polls = (root / POLLS_REL).read_bytes()
            if pinned_gaps != gap_bytes or hashlib.sha256(pinned_gaps).hexdigest() != GAPS_SHA256:
                raise ManifestShaMismatch('pinned gap export')
            if pinned_polls != poll_bytes or hashlib.sha256(pinned_polls).hexdigest() != POLLS_SHA256:
                raise ManifestShaMismatch('pinned poll export')
            frozen_path = root / FROZEN_REL
            assert_sha256(frozen_path, FROZEN_SHA256)
            frozen = json.loads(frozen_path.read_text(encoding='utf-8'))
            registry_path = root / REGISTRY_REL
            assert_sha256(registry_path, REGISTRY_SHA256)
            registry = json.loads(registry_path.read_text(encoding='utf-8'))
            markets, trades, timestamp = _read_universe(connection, frozen)
        finally:
            connection.close()
        payload = {
            'bundle_sha256': BUNDLE_SHA256,
            'snapshot_sha256': SNAPSHOT_SHA256,
            'snapshot_uri_suffix': 'mode=ro&immutable=1',
            'gaps_sha256': GAPS_SHA256,
            'polls_sha256': POLLS_SHA256,
            'frozen_sha256': FROZEN_SHA256,
            'registry_sha256': REGISTRY_SHA256,
            'registry': registry,
            'frozen_markets': list(frozen['universe']['markets']),
            'gap_rows': gap_rows,
            'poll_rows': poll_rows,
            'markets': markets,
            'trades_pre_w0': trades,
            'timestamp': timestamp,
            'results': None,
            'pnl': None,
        }
        return payload
    finally:
        if owned is not None:
            owned.cleanup()


def _read_universe(connection, frozen):
    w0 = _parse_epoch_text(W0)
    w1 = _parse_epoch_text(W1)
    placeholders = ','.join('?' for _ in SERIES)
    market_sql = (
        'SELECT ticker, event_ticker, series_ticker, received_at, status, close_time, result, raw '
        'FROM kalshi_markets WHERE series_ticker IN (%s) ORDER BY ticker, received_at' % placeholders
    )
    first = {}
    finalized_results = {}
    latest_status = {}
    for ticker, event, series, received, status, close_time, result, raw in connection.execute(
        market_sql, SERIES
    ):
        latest_status[ticker] = status
        if status == 'finalized' and result not in (None, ''):
            finalized_results.setdefault(ticker, [])
            if result not in finalized_results[ticker]:
                finalized_results[ticker].append(result)
            if ticker not in first:
                settlement_ts, open_time = _timestamp_keys(raw)
                first[ticker] = {
                    'ticker': ticker,
                    'event': event,
                    'series': series,
                    'received_at': received,
                    'close_time': close_time,
                    'result': result,
                    'settlement_ts': settlement_ts,
                    'open_time': open_time,
                }
    for ticker, results in finalized_results.items():
        if len(results) != 1:
            raise ResultDisagreement(ticker)
    scope = []
    for ticker, market in first.items():
        received = _parse_epoch_text(market['received_at'])
        close_time = _parse_epoch_text(market['close_time'])
        settlement = market['settlement_ts']
        settlement_epoch = _parse_epoch_text(settlement) if settlement else None
        if received >= w0:
            continue
        if close_time is not None and _in_admit1(close_time, w0, w1):
            continue
        if settlement_epoch is None or settlement_epoch >= w0:
            continue
        if _in_admit1(settlement_epoch, w0, w1):
            raise SnapshotLoaderError('settlement in window')
        scope.append(market)
    scope_tickers = sorted(market['ticker'] for market in scope)
    frozen_tickers = sorted(frozen['universe']['markets'])
    if scope_tickers != frozen_tickers:
        raise UniverseMismatch('markets')
    by_ticker = {market['ticker']: market for market in scope}
    trade_sql = (
        'SELECT trade_id, ticker, created_time, received_at, yes_price_dollars, '
        'no_price_dollars, count_fp, taker_side, raw FROM kalshi_trades'
    )
    pre = []
    created_ge_w0 = 0
    received_ge_w0 = 0
    post_close = 0
    for trade_id, ticker, created, received, yes_price, no_price, count_fp, taker_side, raw in (
        connection.execute(trade_sql)
    ):
        if ticker not in by_ticker:
            continue
        created_epoch = _parse_epoch_text(created)
        received_epoch = _parse_epoch_text(received)
        if created_epoch >= w0:
            created_ge_w0 += 1
            continue
        if received_epoch >= w0:
            received_ge_w0 += 1
        market = by_ticker[ticker]
        if created_epoch >= _parse_epoch_text(market['close_time']):
            post_close += 1
        payload = json.loads(raw)
        side_fields = {key: payload.get(key) for key in TRADE_RAW_KEYS}
        pre.append({
            'trade_id': trade_id,
            'ticker': ticker,
            'event': market['event'],
            'city': market['series'],
            'date': market['event'].split('-', 1)[1],
            'created_time': created,
            'created_epoch': created_epoch,
            'received_at': received,
            'yes_price_dollars': yes_price,
            'no_price_dollars': no_price,
            'count_fp': count_fp,
            'taker_side': taker_side,
            'taker_outcome_side': side_fields['taker_outcome_side'],
            'taker_book_side': side_fields['taker_book_side'],
            'raw_taker_side': side_fields['taker_side'],
            'is_block_trade': side_fields['is_block_trade'],
            'close_time': market['close_time'],
            'result': market['result'],
            'settlement_ts': market['settlement_ts'],
            'synthetic': False,
        })
    by_event = {}
    by_date = {}
    for trade in pre:
        by_event[trade['event']] = by_event.get(trade['event'], 0) + 1
        by_date[trade['date']] = by_date.get(trade['date'], 0) + 1
    timestamp = {
        'trades_in_scope_pre_w0': len(pre),
        'by_city_day': dict(sorted(by_event.items())),
        'by_date': dict(sorted(by_date.items())),
        'trades_created_ge_w0': created_ge_w0,
        'trades_received_ge_w0': received_ge_w0,
        'post_close_timestamp_only': post_close,
        'n_markets': len(scope),
        'n_city_days': len({market['event'] for market in scope}),
        'results': None,
        'pnl': None,
    }
    return scope, pre, timestamp
