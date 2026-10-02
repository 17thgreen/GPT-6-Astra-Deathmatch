"""Synthetic tests for GM-COV proof and GM-LIT boundaries."""

import unittest

import gap_mapping


T0 = '2026-09-25T01:00:00Z'
T1 = '2026-09-25T01:10:00Z'
START = gap_mapping.parse_epoch(T0)
END = gap_mapping.parse_epoch(T1)


def _poll(poll_id, key, min_ts, requested_at, ok=1, status=200, n_items=1, error=None, cursor=False):
    url = 'https://example.invalid/markets/trades?ticker=%s&min_ts=%s&limit=1000' % (key, min_ts)
    if cursor:
        url += '&cursor=abc'
    return {
        'id': poll_id,
        'key': key,
        'url': url,
        'requested_at': requested_at,
        'ok': ok,
        'http_status': status,
        'n_items': n_items,
        'error': error,
    }


class GapMappingTests(unittest.TestCase):
    def test_gm_lit_boundaries_and_open_and_storm(self):
        windows = gap_mapping.flagged_windows([
            {
                'id': 1, 'stream': 'kalshi_trades_budget', 'key': 'T',
                'reason': 'budget_shortfall_sweep_late',
                'started_at': T0, 'ended_at': T1,
            },
            {
                'id': 2, 'stream': 'kalshi_trades', 'key': 'T',
                'reason': 'http_429',
                'started_at': '2026-09-25T02:00:00Z', 'ended_at': None,
            },
            {
                'id': 3, 'stream': 'kalshi_all', 'key': 'pause_429_storm',
                'reason': 'pause_429_storm',
                'started_at': '2026-09-25T03:00:00Z', 'ended_at': '2026-09-25T03:10:00Z',
            },
            {
                'id': 4, 'stream': 'kalshi_orderbook', 'key': 'T',
                'reason': 'http_429',
                'started_at': T0, 'ended_at': T1,
            },
        ], ['T', 'U'])
        self.assertEqual(len(windows), 3)
        self.assertTrue(gap_mapping.gm_lit_drops(START, 'T', windows))
        self.assertFalse(gap_mapping.gm_lit_drops(END, 'T', windows))
        open_start = gap_mapping.parse_epoch('2026-09-25T02:00:00Z')
        self.assertTrue(gap_mapping.gm_lit_drops(open_start, 'T', windows))
        self.assertTrue(gap_mapping.gm_lit_drops(open_start + 10 ** 7, 'T', windows))
        self.assertFalse(gap_mapping.gm_lit_drops(open_start - 0.001, 'T', windows))
        storm = gap_mapping.parse_epoch('2026-09-25T03:00:00Z')
        self.assertTrue(gap_mapping.gm_lit_drops(storm, 'T', windows))
        self.assertTrue(gap_mapping.gm_lit_drops(storm, 'U', windows))
        self.assertFalse(gap_mapping.gm_lit_drops(START, 'U', windows))

    def test_gm_lit_pad_widens_budget_only(self):
        windows = gap_mapping.flagged_windows([
            {
                'id': 1, 'stream': 'kalshi_trades_budget', 'key': 'T',
                'reason': 'budget_shortfall_sweep_late',
                'started_at': T0, 'ended_at': T1,
            },
        ], ['T'])
        just_before = START - 1919
        too_early = START - 1920.001
        self.assertFalse(gap_mapping.gm_lit_drops(just_before, 'T', windows, pad_budget=0))
        self.assertTrue(gap_mapping.gm_lit_drops(just_before, 'T', windows, pad_budget=1920))
        self.assertFalse(gap_mapping.gm_lit_drops(too_early, 'T', windows, pad_budget=1920))
        self.assertEqual(gap_mapping.BUDGET_PAD_SECONDS, 1920)

    def test_gm_cov_requires_a_spanning_complete_later_poll(self):
        window = gap_mapping.flagged_windows([
            {
                'id': 7, 'stream': 'kalshi_trades_budget', 'key': 'T',
                'reason': 'budget_shortfall_sweep_late',
                'started_at': T0, 'ended_at': T1,
            },
        ], ['T'])[0]
        spanning = _poll(1, 'T', int(START) - 10, T1)
        polls = gap_mapping.logical_polls([spanning])
        self.assertTrue(gap_mapping.poll_spans_window(polls[0], window['start'], window['end']))
        short = _poll(2, 'T', int(START) + 5, '2026-09-25T01:20:00Z')
        self.assertFalse(gap_mapping.poll_spans_window(
            gap_mapping.logical_polls([short])[0], window['start'], window['end']
        ))
        early_end = _poll(3, 'T', int(START) - 10, '2026-09-25T01:09:59Z')
        self.assertFalse(gap_mapping.poll_spans_window(
            gap_mapping.logical_polls([early_end])[0], window['start'], window['end']
        ))
        rate_limited = _poll(4, 'T', int(START) - 10, T1, ok=0, status=429, n_items=None, error='HTTP 429')
        self.assertIn('http_429', gap_mapping.logical_polls([rate_limited])[0]['failures'])
        self.assertFalse(gap_mapping.logical_polls([rate_limited])[0]['complete'])
        truncated = _poll(5, 'T', int(START) - 10, T1, n_items=1000)
        failures = gap_mapping.logical_polls([truncated])[0]['failures']
        self.assertIn('truncation', failures)
        self.assertIn('pagination_break', failures)
        continued = [
            _poll(6, 'T', int(START) - 10, T1, n_items=1000),
            _poll(7, 'T', int(START) - 10, '2026-09-25T01:10:01Z', n_items=3, cursor=True),
        ]
        logical = gap_mapping.logical_polls(continued)
        self.assertEqual(len(logical), 1)
        self.assertTrue(logical[0]['complete'])
        self.assertTrue(gap_mapping.poll_spans_window(logical[0], window['start'], window['end']))
        broken = [
            _poll(8, 'T', int(START) - 10, T1, n_items=1000),
            _poll(9, 'T', int(START) - 10, '2026-09-25T01:10:01Z', ok=0, status=429, n_items=None, cursor=True, error='HTTP 429'),
        ]
        self.assertFalse(gap_mapping.logical_polls(broken)[0]['complete'])

    def test_open_window_is_never_proven_and_cursor_minus_one_is_not_assumed(self):
        rows = [
            {
                'id': 1, 'stream': 'kalshi_trades', 'key': 'T', 'reason': 'http_429',
                'started_at': T0, 'ended_at': None,
            },
        ]
        polls = [_poll(1, 'T', 0, '2026-09-26T00:00:00Z', n_items=0)]
        proven = gap_mapping.attach_proof(
            gap_mapping.flagged_windows(rows, ['T']), polls, ['T']
        )
        self.assertFalse(proven[0]['proven'])
        self.assertTrue(gap_mapping.gm_cov_drops(START + 100, 'T', proven))
        # A poll whose min_ts is one second after the window start does not cover
        # the start, even though a cursor-minus-1s story would reach backward.
        closed = gap_mapping.flagged_windows([
            {
                'id': 2, 'stream': 'kalshi_trades_budget', 'key': 'T',
                'reason': 'budget_shortfall_sweep_late',
                'started_at': T0, 'ended_at': T1,
            },
        ], ['T'])
        later = [_poll(2, 'T', int(START) + 1, '2026-09-25T02:00:00Z')]
        stamped = gap_mapping.attach_proof(closed, later, ['T'])
        self.assertFalse(stamped[0]['proven'])
        self.assertTrue(gap_mapping.gm_cov_drops(START, 'T', stamped))
        self.assertFalse(gap_mapping.gm_cov_drops(END, 'T', stamped))

    def test_storm_proof_is_per_ticker(self):
        gaps = [{
            'id': 9, 'stream': 'kalshi_all', 'key': 'pause_429_storm',
            'reason': 'pause_429_storm', 'started_at': T0, 'ended_at': T1,
        }]
        polls = [_poll(1, 'T', int(START) - 5, T1, n_items=2)]
        windows = gap_mapping.attach_proof(gap_mapping.flagged_windows(gaps, ['T', 'U']), polls, ['T', 'U'])
        self.assertFalse(windows[0]['proven'])
        self.assertTrue(windows[0]['proven_tickers']['T'])
        self.assertFalse(windows[0]['proven_tickers']['U'])
        self.assertFalse(gap_mapping.gm_cov_drops(START, 'T', windows))
        self.assertTrue(gap_mapping.gm_cov_drops(START, 'U', windows))
        summary = gap_mapping.window_summary(windows, ['T', 'U'])
        self.assertEqual(summary['storm']['proven'], 0)
        self.assertEqual(summary['storm']['not_proven'], 1)

    def test_union_chains_complete_polls_and_rejects_holes_and_open_windows(self):
        window_rows = [{
            'id': 1, 'stream': 'kalshi_trades_budget', 'key': 'T',
            'reason': 'budget_shortfall_sweep_late',
            'started_at': T0, 'ended_at': T1,
        }]
        mid = '2026-09-25T01:05:00Z'
        mid_epoch = gap_mapping.parse_epoch(mid)
        chained = [
            _poll(1, 'T', int(START) - 1, mid),
            _poll(2, 'T', int(mid_epoch), T1),
        ]
        windows = gap_mapping.flagged_windows(window_rows, ['T'])
        union = gap_mapping.attach_proof(windows, chained, ['T'], mode='union')
        single = gap_mapping.attach_proof(windows, chained, ['T'], mode='single')
        self.assertTrue(union[0]['proven'])
        self.assertFalse(single[0]['proven'])
        self.assertFalse(gap_mapping.gm_cov_drops(START, 'T', union))
        hole = [
            _poll(3, 'T', int(START) - 1, mid),
            _poll(4, 'T', int(mid_epoch) + 30, T1),
        ]
        holed = gap_mapping.attach_proof(windows, hole, ['T'], mode='union')
        self.assertFalse(holed[0]['proven'])
        self.assertTrue(gap_mapping.gm_cov_drops(START, 'T', holed))
        incomplete = [
            _poll(5, 'T', int(START) - 1, mid),
            _poll(6, 'T', int(mid_epoch), T1, ok=0, status=429, n_items=None, error='HTTP 429'),
        ]
        broken = gap_mapping.attach_proof(windows, incomplete, ['T'], mode='union')
        self.assertFalse(broken[0]['proven'])
        self.assertFalse(gap_mapping.logical_polls(incomplete)[1]['complete'])
        open_rows = [{
            'id': 8, 'stream': 'kalshi_trades', 'key': 'T', 'reason': 'http_429',
            'started_at': T0, 'ended_at': None,
        }]
        covering = [_poll(9, 'T', int(START) - 5, '2026-09-26T00:00:00Z')]
        opened = gap_mapping.attach_proof(
            gap_mapping.flagged_windows(open_rows, ['T']), covering, ['T'], mode='union'
        )
        self.assertFalse(opened[0]['proven'])
        self.assertTrue(gap_mapping.gm_cov_drops(START + 10, 'T', opened))


if __name__ == '__main__':
    unittest.main()
