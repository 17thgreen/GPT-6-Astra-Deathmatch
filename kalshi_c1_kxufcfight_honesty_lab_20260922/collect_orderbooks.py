"""GET-only orderbook collector for the admitted C1 KXUFCFIGHT panel.

One public pass. Writes under lab/astra-capture/c1-kxufcfight/orderbooks/
only when all four admitted markets return a book. Does not place orders,
does not call private routes, and does not edit the freeze files.
"""
import hashlib
import json
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

import orchestrator

PUBLIC_ORIGIN = 'https://api.elections.kalshi.com'
PUBLIC_PREFIX = '/trade-api/v2'
ORDERBOOK_SUFFIX = ('lab', 'astra-capture', 'c1-kxufcfight', 'orderbooks')
FORBIDDEN_HEADERS = ('authorization', 'cookie', 'x-api-key')
ECONOMICS_KEYS = ('pnl', 'results', 'fills', 'strategy_ev')
USER_AGENT = 'AstraC1OrderbookCapture/0'


class RouteRefused(orchestrator.OrchestratorError):
    """The request left the public orderbook allowlist."""

    def __init__(self, reason='route'):
        super().__init__(reason)


class _RefuseRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise RouteRefused('redirect')


def assert_public_get(method, url, headers=None):
    """Accept one GET of an admitted ticker orderbook. Nothing else."""
    if method != 'GET':
        raise RouteRefused('method')
    if headers:
        for name in headers:
            if str(name).lower() in FORBIDDEN_HEADERS:
                raise RouteRefused('header')
    parts = urlsplit(url)
    if parts.scheme != 'https' or parts.netloc != 'api.elections.kalshi.com':
        raise RouteRefused('host')
    if parts.username or parts.password or parts.query or parts.fragment:
        raise RouteRefused('query')
    prefix = PUBLIC_PREFIX + '/markets/'
    path = parts.path
    if not path.startswith(prefix) or not path.endswith('/orderbook'):
        raise RouteRefused('route')
    if '/portfolio' in path or '/orders' in path:
        raise RouteRefused('private')
    ticker = path[len(prefix):-len('/orderbook')]
    if ticker not in orchestrator.ADMITTED_ORDERBOOK_TICKERS:
        raise RouteRefused('ticker')
    return ticker


def orderbook_url(ticker):
    url = '%s%s/markets/%s/orderbook' % (PUBLIC_ORIGIN, PUBLIC_PREFIX, ticker)
    assert_public_get('GET', url)
    return url


def assert_orderbook_dir(dest):
    """Require the capture slot. A sibling directory is refused."""
    resolved = Path(dest).resolve()
    if resolved.parts[-4:] != ORDERBOOK_SUFFIX:
        raise RouteRefused('destination')
    return resolved


def _book_sides(payload):
    if not isinstance(payload, dict):
        return None
    for key in ECONOMICS_KEYS:
        if payload.get(key) is not None:
            return None
    book = payload.get('orderbook_fp')
    if book is None:
        book = payload.get('orderbook')
    if not isinstance(book, dict):
        return None
    if 'yes_dollars' in book or 'no_dollars' in book:
        yes = book.get('yes_dollars')
        no = book.get('no_dollars')
    elif 'yes' in book or 'no' in book:
        yes = book.get('yes')
        no = book.get('no')
    else:
        return None
    if not isinstance(yes, list) or not isinstance(no, list):
        return None
    return book


def capture_bytes_acceptable(raw):
    """Raw venue bytes with bid lists. Empty lists stay empty."""
    if not isinstance(raw, (bytes, bytearray)):
        return False
    try:
        payload = json.loads(bytes(raw).decode('utf-8'))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return False
    return _book_sides(payload) is not None


def _public_row(row):
    return {key: value for key, value in row.items() if key != 'body'}


def collect(transport, dest, tickers=None, gap_seconds=12, sleep=None):
    """Write four orderbooks or write nothing.

    ``transport(url)`` returns ``(http_status, body_bytes)``. A live pass
    uses 12 seconds between tickers. Tests pass a fake transport and may
    set the gap to zero.
    """
    dest = assert_orderbook_dir(dest)
    if tickers is None:
        tickers = orchestrator.ADMITTED_ORDERBOOK_TICKERS
    tickers = tuple(tickers)
    if tickers != tuple(orchestrator.ADMITTED_ORDERBOOK_TICKERS):
        raise RouteRefused('ticker')
    if gap_seconds < 0:
        raise RouteRefused('gap')
    dest.mkdir(parents=True, exist_ok=True)
    if any(path.is_file() for path in dest.iterdir()):
        raise orchestrator.OrchestratorError('production orderbook pin')
    if sleep is None:
        sleep = time.sleep
    rows = []
    gap = False
    for index, ticker in enumerate(tickers):
        if index and gap_seconds:
            sleep(gap_seconds)
        url = orderbook_url(ticker)
        error = None
        try:
            status, body = transport(url)
        except Exception as exc:
            status, body = None, b''
            error = type(exc).__name__
        if not isinstance(body, (bytes, bytearray)):
            body = b''
            gap = True
            error = error or 'body'
        accepted = error is None and status == 200 and capture_bytes_acceptable(body)
        if not accepted:
            gap = True
        rows.append({
            'market_ticker': ticker,
            'url': url,
            'method': 'GET',
            'http_status': status,
            'accepted': accepted,
            'error': error,
            'sha256': hashlib.sha256(bytes(body)).hexdigest() if accepted else None,
            'body': bytes(body) if accepted else None,
        })
    report = {
        'status': 'FIXTURE_GAP' if gap else 'PINNED_CANDIDATE',
        'score_status': 'NOT_SCORED',
        'examiner_ready': False,
        'results': None,
        'pnl': None,
        'written': [],
        'tickers': [_public_row(row) for row in rows],
    }
    if gap:
        return report
    written = []
    for row in rows:
        target = dest / (row['market_ticker'] + '.json')
        if target.parent != dest:
            raise RouteRefused('destination')
        target.write_bytes(row['body'])
        digest = orchestrator.sha256_file(target)
        if digest != row['sha256']:
            target.unlink()
            raise orchestrator.OrchestratorError('production orderbook pin')
        written.append({
            'path': 'lab/astra-capture/c1-kxufcfight/orderbooks/' + target.name,
            'sha256': digest,
            'market_ticker': row['market_ticker'],
        })
    report['written'] = written
    return report


def urllib_get(url):
    """One public GET. Redirects and credential headers are refused."""
    assert_public_get('GET', url)
    opener = build_opener(_RefuseRedirect)
    request = Request(
        url,
        method='GET',
        headers={
            'User-Agent': USER_AGENT,
            'Accept': 'application/json',
        },
    )
    try:
        with opener.open(request, timeout=20) as response:
            return response.status, response.read()
    except HTTPError as exc:
        payload = exc.read()
        return exc.code, payload
    except URLError:
        raise


def collect_live(dest=None, gap_seconds=12):
    """Bounded public pass. Loads the admitted panel before any socket."""
    orchestrator.load_panel()
    if dest is None:
        dest = orchestrator.PRODUCTION_ORDERBOOK_DIR
    return collect(urllib_get, dest, gap_seconds=gap_seconds)


if __name__ == '__main__':
    outcome = collect_live()
    public = {key: value for key, value in outcome.items() if key != 'written'}
    public['written'] = [
        {'path': row['path'], 'sha256': row['sha256'], 'market_ticker': row['market_ticker']}
        for row in outcome['written']
    ]
    print(json.dumps(public, indent=2, sort_keys=True))
