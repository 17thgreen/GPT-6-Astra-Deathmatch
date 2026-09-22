"""Public GET allowlists. No account, portfolio, or order routes."""
import re

# Same recorder routes as the frozen Q4 collector. The bare events collection
# is intentionally absent so a long-running process cannot be aimed at an
# arbitrary listing query.
_RECORDER = re.compile(
    r'events/KXNFLGAME-[A-Z0-9]+'
    r'|markets/KXNFLGAME-[A-Z0-9]+-[A-Z0-9]+/orderbook'
    r'|markets/trades'
)
_CURSOR = re.compile(r'[A-Za-z0-9_=.+/-]{1,800}')


def allowed_recorder_path(path):
    return bool(_RECORDER.fullmatch(path))


def allowed_listing(path, params):
    """Events collection only, NFL game series, no nested markets or settlements."""
    if path != 'events' or not isinstance(params, dict):
        return False
    if set(params) - {'series_ticker', 'status', 'limit', 'cursor', 'with_nested_markets'}:
        return False
    if params.get('series_ticker') != 'KXNFLGAME':
        return False
    if params.get('status') not in ('open', 'unopened'):
        return False
    if params.get('with_nested_markets') != 'false':
        return False
    limit = params.get('limit')
    if not isinstance(limit, str) or not limit.isdigit() or not 1 <= int(limit) <= 200:
        return False
    cursor = params.get('cursor')
    if cursor is not None and (not isinstance(cursor, str) or '..' in cursor or not _CURSOR.fullmatch(cursor)):
        return False
    return True
