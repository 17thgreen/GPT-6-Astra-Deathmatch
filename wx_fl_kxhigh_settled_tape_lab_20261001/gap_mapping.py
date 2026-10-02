"""Gap-window mappings for WX-FL-KXHIGH-SETTLED-TAPE.

PRIMARY mapping is GM-COV, per Conductor ACCEPT decision 1. A flagged gap
window is covered only when a later poll's cursor range spans the whole
window and that poll completed with no 429, no truncation, and no pagination
break. The collector's cursor-minus-1-second retry is not treated as proof.

GM-LIT and GM-LIT-PAD are sensitivities. They do not decide the verdict.
"""

import re
from datetime import datetime


PAGE_LIMIT = 1000
BUDGET_PAD_SECONDS = 1920
PER_TICKER_STREAMS = ('kalshi_trades', 'kalshi_trades_budget')
ALL_TICKER_STREAMS = ('kalshi_all', 'collector')
_TS = re.compile(r'^(.*T\d\d:\d\d:\d\d)(\.\d+)?(\+00:00)$')
_MIN_TS = re.compile(r'min_ts=(\d+)')


class GapMappingError(Exception):
    """A gap or poll record cannot be mapped."""


def parse_epoch(value):
    """Parse an ISO-8601 UTC timestamp the same way the freeze feasibility tool does.

    Fractional seconds are truncated to six digits. A None value stays None.
    Numbers are already epochs.
    """
    if value is None:
        return None
    if isinstance(value, bool):
        raise GapMappingError('timestamp')
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip().replace('Z', '+00:00')
    matched = _TS.match(text)
    if matched:
        frac = (matched.group(2) or '')[:7]
        text = matched.group(1) + frac + matched.group(3)
    return datetime.fromisoformat(text).timestamp()


def min_ts_from_url(url):
    """Return the integer min_ts query parameter, or None if the URL has none."""
    if not isinstance(url, str):
        return None
    matched = _MIN_TS.search(url)
    if matched is None:
        return None
    return int(matched.group(1))


def gap_type_for(stream, reason):
    """Bucket a flagged gap. Unmapped streams return None."""
    if stream == 'kalshi_trades_budget' and reason == 'budget_shortfall_sweep_late':
        return 'budget'
    if stream == 'kalshi_trades':
        return 'per_ticker_429'
    if stream == 'kalshi_all' and reason == 'pause_429_storm':
        return 'storm'
    if stream == 'collector':
        return 'collector'
    return None


def flagged_windows(gap_rows, in_scope_tickers):
    """Windows that can drop an in-scope trade.

    Per-ticker windows whose key is outside the universe are omitted.
    All-ticker windows are kept. ended_at None is an open window (+infinity).
    """
    scope = set(in_scope_tickers)
    windows = []
    for row in gap_rows:
        kind = gap_type_for(row.get('stream'), row.get('reason'))
        if kind is None:
            continue
        applies_all = row.get('stream') in ALL_TICKER_STREAMS
        key = row.get('key')
        if not applies_all and key not in scope:
            continue
        ended = row.get('ended_at')
        windows.append({
            'id': row.get('id'),
            'stream': row.get('stream'),
            'key': key,
            'reason': row.get('reason'),
            'gap_type': kind,
            'start': parse_epoch(row.get('started_at')),
            'end': None if ended in (None, '') else parse_epoch(ended),
            'applies_all': applies_all,
        })
    return windows


def _failure_list(pages):
    failures = []

    def add(name):
        if name not in failures:
            failures.append(name)

    if not pages:
        add('pagination_break')
        return failures
    first_url = pages[0].get('url') or ''
    if '&cursor=' in first_url:
        add('pagination_break')
    if min_ts_from_url(first_url) is None:
        add('missing_min_ts')
    for index, page in enumerate(pages):
        status = page.get('http_status')
        error = page.get('error') or ''
        if page.get('ok') != 1 or status != 200:
            add('not_ok')
        if status == 429 or '429' in str(error):
            add('http_429')
        if index > 0 and '&cursor=' not in (page.get('url') or ''):
            add('pagination_break')
    last_n = pages[-1].get('n_items')
    if isinstance(last_n, bool) or not isinstance(last_n, int) or last_n >= PAGE_LIMIT:
        add('truncation')
        add('pagination_break')
    if len(pages) > 10:
        add('pagination_break')
    return failures


def logical_polls(poll_rows):
    """Group trades-poll rows into logical polls.

    Sort is (key, id), matching the freeze feasibility tool. A row whose URL
    has no '&cursor=' starts a poll. Later '&cursor=' rows for the same key
    continue it. This function does not invent a one-second overlap.
    """
    rows = sorted(poll_rows, key=lambda row: (str(row.get('key')), int(row.get('id'))))
    polls = []
    current = None

    def flush():
        nonlocal current
        if current is None:
            return
        pages = current['pages']
        failures = _failure_list(pages)
        first = pages[0]
        polls.append({
            'key': current['key'],
            'min_ts': min_ts_from_url(first.get('url') or ''),
            'requested_at': parse_epoch(first.get('requested_at')),
            'page_count': len(pages),
            'complete': len(failures) == 0,
            'failures': tuple(failures),
        })
        current = None

    for row in rows:
        url = row.get('url') or ''
        starts = '&cursor=' not in url
        if current is None or starts or current['key'] != row.get('key'):
            flush()
            current = {'key': row.get('key'), 'pages': []}
        current['pages'].append(row)
    flush()
    return polls


def poll_spans_window(poll, start, end):
    """True only when a complete later poll's cursor range contains the window.

    Cursor range is the half-open interval [min_ts, requested_at). It is not
    widened by the collector's cursor-minus-1-second design. An open window
    (end is None) is never spanned.
    """
    if not poll.get('complete'):
        return False
    if end is None or start is None:
        return False
    min_ts = poll.get('min_ts')
    requested_at = poll.get('requested_at')
    if min_ts is None or requested_at is None:
        return False
    if not (requested_at > start):
        return False
    if min_ts > start:
        return False
    if requested_at < end:
        return False
    return True


def attach_proof(windows, poll_rows, in_scope_tickers):
    """Copy windows with per-ticker proof flags.

    A per-ticker window is proven when that ticker has a spanning complete poll.
    An all-ticker window is proven for a ticker on the same test. The window's
    headline `proven` flag is true only when every in-scope ticker is proven,
    which for a per-ticker window is that one ticker.
    """
    polls = logical_polls(poll_rows)
    by_key = {}
    for poll in polls:
        by_key.setdefault(poll['key'], []).append(poll)
    tickers = list(in_scope_tickers)
    stamped = []
    for window in windows:
        flags = {}
        if window['applies_all']:
            keys = tickers
        else:
            keys = [window['key']]
        for ticker in keys:
            flags[ticker] = any(
                poll_spans_window(poll, window['start'], window['end'])
                for poll in by_key.get(ticker, ())
            )
        copied = dict(window)
        copied['proven_tickers'] = flags
        copied['proven'] = bool(keys) and all(flags.values())
        stamped.append(copied)
    return stamped


def in_window(created, window, pad_seconds=0.0):
    """Half-open membership. Open windows run to +infinity."""
    start = window['start'] - pad_seconds
    end = window['end']
    if end is None:
        return created >= start
    return start <= created < end


def _applies(window, ticker):
    return window['applies_all'] or window['key'] == ticker


def gm_lit_drops(created, ticker, windows, pad_budget=0.0):
    """GM-LIT: drop when created_time falls in any flagged window.

    pad_budget widens budget windows only (GM-LIT-PAD). Open windows drop
    every later trade on the applicable ticker.
    """
    for window in windows:
        if not _applies(window, ticker):
            continue
        pad = pad_budget if window['gap_type'] == 'budget' else 0.0
        if in_window(created, window, pad):
            return True
    return False


def gm_cov_drops(created, ticker, proven_windows):
    """GM-COV: drop when created_time falls in a window that is not proven for this ticker."""
    for window in proven_windows:
        if not _applies(window, ticker):
            continue
        if not in_window(created, window, 0.0):
            continue
        if not window['proven_tickers'].get(ticker, False):
            return True
    return False


def near_miss_requested_before_end(windows, poll_rows):
    """Count finite unproven windows that a complete poll almost spans.

    The poll has min_ts <= start and requested_at > start, but requested_at < end.
    Those windows stay not proven. This counter does not loosen the rule.
    """
    polls = logical_polls(poll_rows)
    by_key = {}
    for poll in polls:
        by_key.setdefault(poll['key'], []).append(poll)
    count = 0
    for window in windows:
        if window.get('proven') or window.get('end') is None or window.get('applies_all'):
            continue
        start = window['start']
        end = window['end']
        close = False
        for poll in by_key.get(window['key'], ()):
            if not poll.get('complete'):
                continue
            min_ts = poll.get('min_ts')
            requested_at = poll.get('requested_at')
            if min_ts is None or requested_at is None:
                continue
            if min_ts <= start and start < requested_at < end:
                close = True
                break
        if close:
            count += 1
    return count


def window_summary(proven_windows, in_scope_tickers):
    """Proven versus not-proven counts by gap type. No prices."""
    tickers = list(in_scope_tickers)
    buckets = ('budget', 'per_ticker_429', 'storm', 'collector')
    summary = {}
    for kind in buckets:
        rows = [window for window in proven_windows if window['gap_type'] == kind]
        open_ended = sum(1 for window in rows if window['end'] is None)
        if kind in ('storm', 'collector'):
            proven = sum(1 for window in rows if window['proven'])
            summary[kind] = {
                'n_windows': len(rows),
                'proven': proven,
                'not_proven': len(rows) - proven,
                'open_ended': open_ended,
                'proven_means': (
                    'every in-scope ticker has a later complete poll whose '
                    'cursor range spans the whole window'
                ),
                'n_in_scope_tickers': len(tickers),
            }
        else:
            proven = sum(1 for window in rows if window['proven'])
            summary[kind] = {
                'n_windows': len(rows),
                'proven': proven,
                'not_proven': len(rows) - proven,
                'open_ended': open_ended,
                'proven_means': (
                    'that ticker has a later complete poll whose cursor range '
                    'spans the whole window'
                ),
            }
    return summary
