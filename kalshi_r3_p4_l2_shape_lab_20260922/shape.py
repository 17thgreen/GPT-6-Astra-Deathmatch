"""SF1 and SF2 quote shape on Kalshi bids-only books.

Mids and spreads come from kalshi_feebook_lab_20260922. A snapshot is included
only when kalshi_rails_lab_20260922 says the book is content-fresh. This module
does not place live orders and does not compute a fee or a profit.
"""
import json
import sys
from decimal import Decimal, ROUND_FLOOR
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent
FEEBOOK_DIR = PARENT / 'kalshi_feebook_lab_20260922'
RAILS_DIR = PARENT / 'kalshi_rails_lab_20260922'
for _path in (FEEBOOK_DIR, RAILS_DIR):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import feebook
import rails

EXPERIMENT_ID = 'R3-P4-L2-SHAPE-SF1-SF2'
BPS = Decimal('10000')
N_LEVELS = 10
UNIFORM = Fraction(1, N_LEVELS)
TOP_HEAVY_MIN = Fraction(1, 2)
CATEGORIES = ('sports', 'non_sports')
LIVE_ORDERS = False
LEE_READY = False
SIGNAL_RETUNE_000 = False


class StaleSnapshotRefused(Exception):
    """The rails predicate did not call this snapshot content-fresh."""

    def __init__(self, reason):
        super().__init__(reason)
        self.reason = reason


class ShapeProfitRefused(Exception):
    """A quote-shape row is not a fee and not a profit."""


class LeeReadyRefused(Exception):
    """Trade-sign inference is out of scope."""


class ShapeRefused(Exception):
    """The YES mid is not positive, so bps of mid is undefined."""


def mid_decile(mid):
    """Absolute Dubach Table 1 bin. High edges are exclusive except mid 1."""
    mid = feebook.as_decimal(mid, 'mid')
    if mid < 0 or mid > feebook.ONE:
        raise ValueError('mid')
    if mid == feebook.ONE:
        return 9
    index = int((mid * N_LEVELS).to_integral_value(rounding=ROUND_FLOOR))
    if index < 0 or index > 9:
        raise ValueError('decile')
    return index


def decile_edges(index):
    if isinstance(index, bool) or not isinstance(index, int) or index < 0 or index > 9:
        raise ValueError('decile')
    return (Decimal(index) / Decimal(N_LEVELS),
            Decimal(index + 1) / Decimal(N_LEVELS))


def quoted_yes(orderbook):
    """YES half-spread in bps of the reciprocal mid. A missing side stays unset."""
    book = feebook.reciprocal_book(orderbook)
    if (book['bid_yes'] is None or book['bid_no'] is None
            or book['ask_yes'] is None or book['spread_yes'] is None):
        raise feebook.BookIncomplete('missing bid')
    mid = (book['bid_yes'] + book['ask_yes']) / 2
    if mid <= 0:
        raise ShapeRefused('mid must be positive')
    half = book['spread_yes'] / 2
    return {
        'mid': mid,
        'spread': book['spread_yes'],
        'half_spread': half,
        'half_spread_bps': half / mid * BPS,
        'decile': mid_decile(mid),
        'book': book,
    }


def _fraction_size(size):
    if isinstance(size, Fraction):
        return size
    if not isinstance(size, Decimal):
        size = feebook.as_decimal(size, 'size')
    return Fraction(size)


def bid_ladder(levels):
    """Positive sizes aggregated by price, best bid first. Zero size is skipped."""
    buckets = {}
    for price, size in levels:
        if size < 0:
            raise ValueError('size')
        if size == 0:
            continue
        buckets[price] = buckets.get(price, Decimal('0')) + size
    return sorted(buckets.items(), key=lambda row: row[0], reverse=True)


def top10_depth(orderbook):
    """Rank-aligned YES bid size plus NO bid size. Missing ranks stay zero."""
    yes = bid_ladder(feebook._levels(orderbook, 'yes'))
    no = bid_ladder(feebook._levels(orderbook, 'no'))
    if not yes or not no:
        raise feebook.BookIncomplete('missing side')
    depths = []
    for rank in range(N_LEVELS):
        yes_size = yes[rank][1] if rank < len(yes) else Decimal('0')
        no_size = no[rank][1] if rank < len(no) else Decimal('0')
        depths.append(_fraction_size(yes_size) + _fraction_size(no_size))
    total = sum(depths, Fraction(0))
    if total <= 0:
        raise feebook.BookIncomplete('no positive depth')
    shares = tuple(depth / total for depth in depths)
    return {
        'depths': tuple(depths),
        'shares': shares,
        'l1_share': shares[0],
        'kl_nats': kl_vs_uniform(shares),
        'top_heavy': shares[0] > TOP_HEAVY_MIN,
        'observed_depth': total,
    }


def kl_vs_uniform(shares):
    """KL(share || uniform 1/10) in nats. A zero share contributes nothing."""
    if len(shares) != N_LEVELS:
        raise ValueError('shares')
    total = Decimal('0')
    uniform = Decimal(1) / Decimal(N_LEVELS)
    for share in shares:
        if isinstance(share, Fraction):
            if share == 0:
                continue
            if share < 0:
                raise ValueError('share')
            probability = Decimal(share.numerator) / Decimal(share.denominator)
        else:
            probability = feebook.as_decimal(share, 'share')
            if probability == 0:
                continue
            if probability < 0:
                raise ValueError('share')
        total += probability * (probability / uniform).ln()
    return total


def median(values):
    rows = list(values)
    if not rows:
        return None
    ordered = sorted(rows)
    count = len(ordered)
    center = count // 2
    if count % 2 == 1:
        return ordered[center]
    return (ordered[center - 1] + ordered[center]) / 2


def require_content_fresh(previous, current, *, keepalive=False):
    """Raise unless rails.judge_freshness accepts the snapshot."""
    verdict = rails.judge_freshness(previous, current, keepalive=keepalive)
    if not verdict.fresh:
        raise StaleSnapshotRefused(verdict.reason)
    return verdict


def observation(orderbook, transaction_time):
    return rails.BookObservation(
        rails.canonical_book_content(orderbook),
        transaction_time,
    )


def _category(value):
    if value not in CATEGORIES:
        raise ValueError('category')
    return value


def _ticker(value):
    if not isinstance(value, str) or value == '':
        raise ValueError('ticker')
    return value


def screen_snapshots(snapshots):
    """Keep content-fresh rows. Stale rows and keepalives are refused."""
    previous = {}
    included = []
    refused = []
    for snap in snapshots:
        if not isinstance(snap, dict):
            raise TypeError('snapshot')
        ticker = _ticker(snap.get('ticker'))
        category = _category(snap.get('category'))
        keepalive = snap.get('keepalive', False)
        if not isinstance(keepalive, bool):
            raise TypeError('keepalive')
        orderbook = snap.get('orderbook_fp')
        if not isinstance(orderbook, dict):
            raise TypeError('orderbook_fp')
        current = observation(orderbook, snap.get('transaction_time'))
        try:
            verdict = require_content_fresh(
                previous.get(ticker), current, keepalive=keepalive,
            )
        except StaleSnapshotRefused as exc:
            refused.append({'ticker': ticker, 'reason': exc.reason})
            continue
        previous[ticker] = current
        included.append({
            'ticker': ticker,
            'category': category,
            'transaction_time': snap.get('transaction_time'),
            'orderbook_fp': orderbook,
            'freshness': verdict.reason,
        })
    return included, refused


def _market_row(ticker, snaps):
    categories = {snap['category'] for snap in snaps}
    if len(categories) != 1:
        raise ValueError('category')
    quotes = [quoted_yes(snap['orderbook_fp']) for snap in snaps]
    depths = [top10_depth(snap['orderbook_fp']) for snap in snaps]
    count = len(quotes)
    mean_mid = sum((row['mid'] for row in quotes), Decimal('0')) / Decimal(count)
    average = []
    for rank in range(N_LEVELS):
        average.append(
            sum((row['depths'][rank] for row in depths), Fraction(0)) / count
        )
    total = sum(average, Fraction(0))
    if total <= 0:
        raise feebook.BookIncomplete('no positive depth')
    shares = tuple(depth / total for depth in average)
    return {
        'ticker': ticker,
        'category': categories.pop(),
        'n_snapshots': count,
        'mean_mid': mean_mid,
        'decile': mid_decile(mean_mid),
        'median_half_spread_bps': median(row['half_spread_bps'] for row in quotes),
        'shares': shares,
        'l1_share': shares[0],
        'kl_nats': kl_vs_uniform(shares),
        'top_heavy': shares[0] > TOP_HEAVY_MIN,
    }


def market_rows(included):
    groups = {}
    order = []
    for snap in included:
        if snap['ticker'] not in groups:
            order.append(snap['ticker'])
            groups[snap['ticker']] = []
        groups[snap['ticker']].append(snap)
    rows = []
    for ticker in order:
        categories = {snap['category'] for snap in groups[ticker]}
        if len(categories) != 1:
            raise ValueError('category')
        rows.append(_market_row(ticker, groups[ticker]))
    return rows


def sf1_table(rows):
    bins = []
    for index in range(N_LEVELS):
        low, high = decile_edges(index)
        members = [row for row in rows if row['decile'] == index]
        bins.append({
            'bin': index,
            'mid_lo': low,
            'mid_hi': high,
            'n': len(members),
            'median_half_spread_bps': median(
                row['median_half_spread_bps'] for row in members
            ),
        })
    return bins


def sf2_summary(rows):
    return {
        'n': len(rows),
        'median_l1_share': median(row['l1_share'] for row in rows),
        'median_kl_nats': median(row['kl_nats'] for row in rows),
        'level_median_shares': [
            median(row['shares'][rank] for row in rows) for rank in range(N_LEVELS)
        ],
        'top_heavy_count': sum(1 for row in rows if row['top_heavy']),
    }


def _by_category(rows, category):
    return [row for row in rows if row['category'] == category]


def _usable(included, refused):
    usable = []
    for snap in included:
        try:
            quoted_yes(snap['orderbook_fp'])
            top10_depth(snap['orderbook_fp'])
        except (feebook.BookIncomplete, ShapeRefused):
            refused.append({'ticker': snap['ticker'], 'reason': 'book_incomplete'})
            continue
        usable.append(snap)
    return usable


def shape_panel(snapshots):
    """SF1 and SF2 for content-fresh snapshots. results and pnl stay null."""
    included, refused = screen_snapshots(snapshots)
    usable = _usable(included, refused)
    rows = market_rows(usable)
    return {
        'experiment': EXPERIMENT_ID,
        'results': None,
        'pnl': None,
        'lee_ready': None,
        'live_orders': LIVE_ORDERS,
        'included_snapshots': len(usable),
        'refused_snapshots': len(refused),
        'refusals': refused,
        'markets': rows,
        'sf1': {
            'all': sf1_table(rows),
            'sports': sf1_table(_by_category(rows, 'sports')),
            'non_sports': sf1_table(_by_category(rows, 'non_sports')),
        },
        'sf2': {
            'all': sf2_summary(rows),
            'sports': sf2_summary(_by_category(rows, 'sports')),
            'non_sports': sf2_summary(_by_category(rows, 'non_sports')),
        },
    }


def load_fixtures(path=None):
    if path is None:
        path = ROOT / 'fixtures' / 'l2_shape_fixtures.json'
    return json.loads(Path(path).read_text())


def empty_outputs():
    return {
        'results': None,
        'pnl': None,
        'sf1': None,
        'sf2': None,
        'status': 'NOT_RUN',
    }


def completed_profit(*_args, **_kwargs):
    raise ShapeProfitRefused('quote shape is not a fee and not a profit')


def infer_trade_sign(*_args, **_kwargs):
    raise LeeReadyRefused('Lee-Ready is out of scope')
