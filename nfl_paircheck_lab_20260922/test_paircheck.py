"""Admission behavior for the Q7 2×2. No historical tape and no P&L claim."""
import inspect
import unittest
from paircheck_policy import (AllocatorPairCheck, OriginalPairCheck, combined_cost_margin,
                              make_replay, q6_pin_mismatches)
from adaptive_policy import AdaptiveReplay
from factorial_policy import FactorialReplay, Factors
from replay_v2 import Config
from test_adaptive import AT, KO, position
from test_replay_v2 import markets
from dataclasses import replace

def config(**overrides):
    values = dict(quote_source='candles', queue_early=100, queue_last12h=100,
                  liquidation_lead_seconds=300, cancel_delay_seconds=.25, order_delay_seconds=.25)
    values.update(overrides)
    return replace(Config(), **values)

def new(arm, **overrides):
    return make_replay(markets(KO), config(**overrides), arm)

def bad_pair(replay):
    for ticker in ('A', 'B'):
        replay.books[ticker] = dict(bid=.40, ask=.45, bid_at=AT, ask_at=AT)
    replay.flow.add(dict(ticker='A', at=AT - 1, yes_price=.55, size=100000, taker_side='yes'))
    replay.flow.add(dict(ticker='B', at=AT - 1, yes_price=.45, size=100000, taker_side='yes'))

def good_pair(replay):
    for ticker in ('A', 'B'):
        replay.books[ticker] = dict(bid=.49, ask=.51, bid_at=AT, ask_at=AT)

def live_orders(replay):
    return {key: order for key, order in replay.orders.items() if order.cancel_at is None}

class PairCheckTests(unittest.TestCase):
    def test_q6_sources_match_frozen_pins(self):
        self.assertEqual(q6_pin_mismatches(), [])

    def test_pair_check_flag_must_be_bool(self):
        with self.assertRaises(ValueError):
            OriginalPairCheck(markets(KO), config(), 1)
        with self.assertRaises(ValueError):
            AllocatorPairCheck(markets(KO), config(), 0)

    def test_allocator_arms_are_label_000(self):
        for arm in ('C', 'D'):
            replay = new(arm)
            self.assertEqual(replay.factors.label, '000')
            self.assertFalse(replay.factors.flow or replay.factors.protection or replay.factors.ranking)

    def test_profitable_original_pair_is_admitted(self):
        baseline = AdaptiveReplay(markets(KO), config(), 'baseline')
        checked = new('B')
        untouched = new('A')
        for replay in (baseline, checked, untouched):
            good_pair(replay)
            replay.refresh('G', AT)
        self.assertEqual(order_snapshot(checked), order_snapshot(baseline))
        self.assertEqual(order_snapshot(untouched), order_snapshot(baseline))
        self.assertEqual(checked.pair_rejections, [])
        self.assertEqual(checked.experiment, 'baseline')
        self.assertEqual(checked.metrics['portfolio_rebalances'], 0)
        self.assertEqual(len(checked.orders), 2)

    def test_unprofitable_chosen_pair_is_rejected(self):
        replay = new('B')
        bad_pair(replay)
        cash = replay.cash
        replay.refresh('G', AT)
        self.assertEqual(replay.orders, {})
        self.assertEqual(replay.cash, cash)
        self.assertEqual(len(replay.pair_rejections), 1)
        row = replay.pair_rejections[0]
        self.assertEqual(row['reason'], 'combined_acquisition_cost')
        self.assertLessEqual(row['margin'], 0)
        self.assertFalse(row['counted_as_pnl'])
        self.assertFalse(row['assumed_simultaneous_fills'])
        self.assertFalse(row['used_future_quotes'])
        self.assertFalse(row['cancelled_instantly'])
        self.assertEqual(sorted(row['blocked_new_exposure_keys']), [['A', 'no'], ['B', 'no']])
        self.assertEqual(row['admitted_offset_keys'], [])

    def test_check_off_original_still_quotes_the_unprofitable_pair(self):
        replay = new('A')
        bad_pair(replay)
        replay.refresh('G', AT)
        self.assertEqual(set(replay.orders), {('A', 'no'), ('B', 'no')})
        self.assertEqual(replay.pair_rejections, [])

    def test_offset_only_order_is_not_blocked(self):
        replay = new('B')
        bad_pair(replay)
        position(replay, 25)
        replay.refresh('G', AT)
        self.assertIn(('A', 'no'), replay.orders)
        self.assertNotIn(('B', 'no'), replay.orders)
        self.assertLess(replay.orders[('A', 'no')].direction, 0)
        self.assertGreater(replay.orders[('A', 'no')].remaining, 0)
        row = replay.pair_rejections[0]
        self.assertIn(['A', 'no'], row['admitted_offset_keys'])
        self.assertIn(['B', 'no'], row['blocked_new_exposure_keys'])
        self.assertFalse(row['counted_as_pnl'])

    def test_allocator_offset_stays_available_when_check_rejects_entry(self):
        replay = new('D')
        bad_pair(replay)
        position(replay, 25)
        replay.refresh('G', AT)
        self.assertTrue(replay.pair_rejections)
        self.assertTrue(replay.orders)
        self.assertTrue(all(order.direction < 0 for order in replay.orders.values()))
        self.assertFalse(any(rank for decision in replay.decisions for rank in decision.get('ranks', [])))

    def test_rejection_does_not_cancel_a_resting_order_instantly(self):
        replay = new('B', cancel_delay_seconds=5)
        good_pair(replay)
        replay.refresh('G', AT)
        before = {key: (order.identity, order.remaining, order.price) for key, order in replay.orders.items()}
        self.assertTrue(before)
        bad_pair(replay)
        cash = replay.cash
        replay.refresh('G', AT + 1)
        self.assertEqual(replay.cash, cash)
        self.assertEqual(set(replay.orders), set(before))
        for key, order in replay.orders.items():
            self.assertEqual((order.identity, order.remaining, order.price), before[key])
            self.assertEqual(order.cancel_at, AT + 1 + 5)
        order = replay.orders[('A', 'yes')]
        order.queue = 0
        replay.on_trade(dict(ticker='A', at=AT + 2, yes_price=.49, size=20, taker_side='no'))
        self.assertGreater(replay.holdings['G'], 0)
        self.assertGreater(replay.metrics['fills_while_cancel_pending'], 0)
        self.assertIn(('A', 'yes'), replay.orders)

    def test_blocked_replacement_is_not_submitted_after_cancel_ack(self):
        checked = new('B', cancel_delay_seconds=5)
        plain = new('A', cancel_delay_seconds=5)
        for replay in (checked, plain):
            good_pair(replay)
            replay.refresh('G', AT)
            bad_pair(replay)
            replay.refresh('G', AT + 1)
            if replay is checked:
                self.assertNotIn(('B', 'no'), replay.orders)
            replay.advance(AT + 6)
            self.assertFalse(any(abs(order.price - .49) < 1e-9 for order in replay.orders.values()))
            replay.refresh('G', AT + 6.1)
        self.assertEqual(checked.orders, {})
        self.assertEqual(set(plain.orders), {('A', 'no'), ('B', 'no')})
        self.assertTrue(checked.pair_rejections)
        self.assertTrue(all(row['counted_as_pnl'] is False for row in checked.pair_rejections))

    def test_check_does_not_require_joint_capacity_or_future_quotes(self):
        replay = new('B')
        good_pair(replay)
        candidates = replay.route_candidates('G', AT)
        for candidate in candidates:
            candidate['capacity'] = 0
        blocked, rejection = replay.plan_admission(candidates, 0, AT, 'G')
        self.assertEqual(blocked, set())
        self.assertIsNone(rejection)
        replay.refresh('G', AT)
        self.assertEqual(len(replay.orders), 2)
        self.assertTrue(all(order.remaining == 100 for order in replay.orders.values()))
        bad = new('B')
        bad_pair(bad)
        frozen = bad.route_candidates('G', AT)
        _, first = bad.plan_admission(frozen, 0, AT, 'G')
        bad.books['A']['bid'] = .2
        bad.books['A']['ask'] = .25
        _, second = bad.plan_admission(frozen, 0, AT, 'G')
        self.assertEqual(second['margin'], first['margin'])
        self.assertFalse(second['used_future_quotes'])
        source = inspect.getsource(OriginalPairCheck.plan_admission)
        self.assertNotIn('on_quote', source)
        self.assertNotIn('.cancel', source)
        self.assertNotIn('orders.pop', source)

    def test_rejection_margin_is_not_added_to_cash(self):
        replay = new('B')
        bad_pair(replay)
        replay.refresh('G', AT)
        margin = replay.pair_rejections[0]['hypothetical_unit_margin']
        self.assertLess(margin, 0)
        self.assertEqual(replay.cash, replay.cfg.starting_cash)
        self.assertNotIn('pair_rejection', {row['kind'] for row in replay.decisions})

    def test_check_off_allocator_has_no_residual_cost_gate(self):
        source = inspect.getsource(AllocatorPairCheck._rank_without_combined_cost_filter)
        compact = source.replace(' ', '')
        self.assertNotIn('margin<=0', compact)
        self.assertNotIn('score<=0', compact)
        self.assertNotIn('adjusted<=0', compact)
        replay = new('C')
        bad_pair(replay)
        rank = replay.portfolio_rank(replay.event_candidates('G', AT), AT)
        self.assertIsNotNone(rank)
        self.assertLess(rank['score'], 0)
        self.assertEqual(rank['adjusted'], 1)
        self.assertGreater(rank['capital'], 0)
        self.assertEqual(replay.pair_rejections, [])
        replay.refresh('G', AT)
        self.assertEqual(set(live_orders(replay)), {('A', 'no'), ('B', 'no')})
        self.assertGreater(replay.allocations['G'], 0)
        self.assertEqual(replay.pair_rejections, [])

    def test_route_screen_is_not_the_combined_cost_filter(self):
        replay = new('C')
        candidates = []
        for key, direction in ((('A', 'yes'), 1), (('B', 'no'), 1), (('B', 'yes'), -1), (('A', 'no'), -1)):
            candidates.append(dict(key=key, direction=direction, cost=.9, service=1, rate=1,
                                   queue=100, wanted=250, price=.9, inside=False))
        self.assertIsNone(replay.portfolio_rank(candidates, AT))
        self.assertEqual(replay.choose(candidates), set())

    def test_arm_d_rank_matches_frozen_q6_and_records_rejection_aside(self):
        left = new('D')
        right = FactorialReplay(markets(KO), config(), Factors(False, False, False))
        good_pair(left)
        good_pair(right)
        for replay in (left, right):
            rows = replay.event_candidates('G', AT)
            for row in rows:
                row['rate'] = 1
            self.assertEqual(replay.portfolio_rank(rows, AT)['adjusted'] > 0, True)
        left_rows = with_rate(left)
        right_rows = with_rate(right)
        self.assertEqual(left.portfolio_rank(left_rows, AT), right.portfolio_rank(right_rows, AT))
        bad_pair(left)
        bad_pair(right)
        self.assertIsNone(right.portfolio_rank(right.event_candidates('G', AT), AT))
        self.assertIsNone(left.portfolio_rank(left.event_candidates('G', AT), AT))
        self.assertTrue(left.pair_rejections)
        self.assertFalse(any(row['kind'] == 'pair_rejection' for row in left.decisions))
        left.rebalance(AT)
        right.rebalance(AT)
        self.assertEqual(left.decisions[-1], right.decisions[-1])
        self.assertEqual(left.factors.label, right.factors.label)

    def test_combined_margin_uses_order_size_not_joint_fill(self):
        margin = combined_cost_margin([.55, .55], 250, '.0001')
        self.assertLess(margin, 0)
        self.assertNotEqual(combined_cost_margin([.55, .55], 250, '.0001'),
                            combined_cost_margin([.55, .55], 1, '.0001'))

def order_snapshot(replay):
    return sorted((key, order.price, order.remaining) for key, order in replay.orders.items())

def with_rate(replay):
    rows = replay.event_candidates('G', AT)
    for row in rows:
        row['rate'] = 1
    return rows

if __name__ == '__main__':
    unittest.main()
