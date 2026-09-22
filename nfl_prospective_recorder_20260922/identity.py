"""Match a schedule row to a public KXNFLGAME listing title.

Uses the Eastern kickoff date and ticker team codes only. Listing objects are
reduced to identity fields before a match, so a price or result on the wire
cannot decide membership.
"""
import re
from datetime import datetime
from zoneinfo import ZoneInfo

# Schedule abbreviations that already differ from published Kalshi tickers.
# JAX→JAC is the ticker on KXNFLGAME-26SEP13CLEJAC. LA→LAR is the ticker on
# KXNFLGAME-26SEP10SFLAR. No other alias is assumed.
TICKER_CODE = {'JAX': 'JAC', 'LA': 'LAR'}
_LISTING_KEYS = (
    'event_ticker', 'title', 'sub_title', 'series_ticker',
    'mutually_exclusive', 'collateral_return_type', 'category',
)


def ticker_code(schedule_code):
    if not isinstance(schedule_code, str) or not re.fullmatch(r'[A-Z]{2,3}', schedule_code):
        raise ValueError('team code must be 2-3 letters')
    return TICKER_CODE.get(schedule_code, schedule_code)


def eastern_stamp(kickoff):
    dt = datetime.fromisoformat(kickoff)
    if dt.tzinfo is None:
        raise ValueError('kickoff must be timezone-aware')
    local = dt.astimezone(ZoneInfo('America/New_York'))
    return local.strftime('%y%b%d').upper()


def expected_ticker(game):
    stamp = eastern_stamp(game['kickoff'])
    away = ticker_code(game['away'])
    home = ticker_code(game['home'])
    return f'KXNFLGAME-{stamp}{away}{home}'


def sanitize_listing_event(raw):
    if not isinstance(raw, dict):
        raise ValueError('listing event must be an object')
    return {key: raw[key] for key in _LISTING_KEYS if key in raw}


def match_game(game, listings):
    want = expected_ticker(game)
    hits = [row for row in listings if row.get('event_ticker') == want]
    if len(hits) > 1:
        return dict(status='ambiguous', event_ticker=None)
    if len(hits) == 1:
        away = ticker_code(game['away'])
        home = ticker_code(game['home'])
        subtitle = hits[0].get('sub_title') or ''
        prefix = f'{away} vs {home}'
        if subtitle != prefix and not subtitle.startswith(prefix + ' ') and not subtitle.startswith(prefix + '('):
            return dict(status='subtitle_mismatch', event_ticker=None)
        return dict(status='matched', event_ticker=want, sub_title=subtitle, title=hits[0].get('title'))
    return dict(status='unresolved', event_ticker=None, pattern_absent_from_listing=want)
