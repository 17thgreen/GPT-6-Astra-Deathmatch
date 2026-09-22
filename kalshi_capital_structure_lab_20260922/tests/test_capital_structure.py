"""Unit pins for the capital-structure partition rules.

Synthetic cash movements check the frozen invariants. They are not a
historical walk and they are not profit.
"""
import inspect
import json
import sys
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(PARENT / 'kalshi_feebook_lab_20260922'))
sys.path.insert(0, str(PARENT / 'kalshi_rails_lab_20260922'))

import capital_structure as capital
import feebook
import rails


def account(arm, event_ids=None):
    return capital.open_account(arm, event_ids)


class PinTests(unittest.TestCase):
    def test_floor_division_matches_the_freeze_packet(self):
        frozen = json.loads((ROOT / 'capital_structure_freeze.json').read_text())
        self.assertEqual(capital.C_TOTAL, Decimal(frozen['C_total_usd']))
        self.assertEqual(capital.N_EVENTS, frozen['N_events'])
        self.assertEqual(capital.SLICE, Decimal(frozen['slice_usd']))
        self.assertEqual(capital.RESIDUAL, Decimal(frozen['residual_usd']))
        self.assertEqual(capital.SLICE * capital.N_EVENTS + capital.RESIDUAL, capital.C_TOTAL)
        self.assertEqual(capital.SOFT_POLICY, frozen['soft_policy'])
        self.assertEqual(capital.RESIDUAL_POLICY, frozen['residual_policy'])
        self.assertEqual(capital.ARMS, tuple(frozen['arms']))
        self.assertEqual(capital.FORBIDDEN_COMPARISON, frozen['forbidden'])
        self.assertEqual(capital.PROMOTION_SCOREBOARD, frozen['promotion_scoreboard'])

    def test_packet_shadow_and_manifest_hashes(self):
        frozen = json.loads((ROOT / 'FROZEN_EXPERIMENT.json').read_text())
        packet = ROOT / 'CAPITAL_STRUCTURE_PROBE_FREEZE_KERNEL_2026-09-22.md'
        self.assertEqual(capital.sha256_file(packet), frozen['packet_sha256'])
        self.assertEqual(capital.sha256_file(capital.SHADOW_FREEZE), frozen['shadow_freeze_sha256'])
        self.assertEqual(capital.sha256_file(capital.TAPE_MANIFEST), frozen['tape_manifest_sha256'])
        shadow = json.loads(capital.SHADOW_FREEZE.read_text())
        self.assertEqual(shadow['selected'], '000')
        self.assertEqual(frozen['strategy_pointer'], 'Q6-000')
        self.assertIs(frozen['paircheck_varied'], False)
        self.assertIsNone(frozen['results'])
        self.assertIsNone(frozen['pnl'])

    def test_default_cohort_is_the_development_membership(self):
        membership = json.loads(capital.WEEK_MEMBERSHIP.read_text())
        ids = capital.development_cohort_event_ids()
        self.assertEqual(ids, tuple(sorted(membership.keys())))
        self.assertEqual(len(ids), 31)
        opened = account(capital.A1)
        self.assertEqual(opened.event_ids, ids)

    def test_fee_and_queue_binding_comes_from_feebook_and_rails(self):
        binding = capital.instrument_binding()
        rates = feebook.load_series_table()['rates']
        self.assertEqual(Path(feebook.__file__).resolve().parent.name, 'kalshi_feebook_lab_20260922')
        self.assertEqual(Path(rails.__file__).resolve().parent.name, 'kalshi_rails_lab_20260922')
        self.assertEqual(binding['taker_rate'], feebook.as_decimal(rates['taker'], 'taker'))
        self.assertEqual(binding['maker_rate'], feebook.as_decimal(rates['maker'], 'maker'))
        self.assertEqual(binding['examiner_formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(binding['fee_credit_rule_id'], rails.FEE_CREDIT_RULE_ID)
        self.assertEqual(binding['primary_queue_ahead'], rails.scenario_queue('q3300'))
        self.assertEqual(binding['harsh_twin_queue_ahead'], rails.scenario_queue('q10000'))
        self.assertIs(binding['harsh_twin_is_capital_knob'], False)
        self.assertIs(binding['paircheck_varied'], False)
        self.assertEqual(binding['strategy_pointer'], 'Q6-000')
        source = (ROOT / 'capital_structure.py').read_text()
        for banned in (
            'maker_coefficient',
            'taker_coefficient',
            'common_config',
            '0.0175',
            '0.07',
            'factorial_policy',
            'paircheck_policy',
            'class KalshiExecutionAdapter',
        ):
            self.assertNotIn(banned, source)
        for arm in capital.ARMS:
            self.assertEqual(account(arm).binding['primary_queue_ahead'], binding['primary_queue_ahead'])


class IdentityTests(unittest.TestCase):
    def test_every_arm_starts_at_the_same_c_total(self):
        totals = []
        for arm in capital.ARMS:
            book = account(arm)
            self.assertEqual(book.c_total, capital.C_TOTAL)
            self.assertEqual(book.identity(), capital.C_TOTAL)
            self.assertEqual(book.available + book.committed + book.non_trading_residual_bucket, capital.C_TOTAL)
            self.assertTrue(book.shared_account)
            totals.append(book.c_total)
        self.assertEqual(totals, [capital.C_TOTAL, capital.C_TOTAL, capital.C_TOTAL])

    def test_a1_one_event_can_take_the_whole_pool(self):
        book = account(capital.A1)
        event = book.event_ids[0]
        order = book.fund(event, capital.C_TOTAL, order_id='all')
        self.assertEqual(order.amount, capital.C_TOTAL)
        self.assertEqual(book.available, Decimal('0'))
        self.assertEqual(book.committed, capital.C_TOTAL)
        self.assertEqual(book.borrow_log, [])
        self.assertEqual(book.non_trading_residual_bucket, Decimal('0'))
        self.assertEqual(book.identity(), capital.C_TOTAL)
        with self.assertRaises(capital.InsufficientCapital):
            book.fund(book.event_ids[1], Decimal('1'), order_id='more')
        self.assertEqual(book.identity(), capital.C_TOTAL)
        book.release('all')
        self.assertEqual(book.available, capital.C_TOTAL)
        self.assertEqual(book.identity(), capital.C_TOTAL)

    def test_over_pool_is_all_or_nothing_on_every_arm(self):
        for arm in (capital.A1, capital.A2):
            book = account(arm)
            before = (book.available, book.committed, book.identity())
            with self.assertRaises(capital.InsufficientCapital):
                book.fund(book.event_ids[0], capital.C_TOTAL + Decimal('1'), order_id='too-much')
            self.assertEqual((book.available, book.committed, book.identity()), before)
            self.assertEqual(book.borrow_log, [])
        hard = account(capital.A3)
        before = (hard.available, hard.committed, hard.identity(), hard.non_trading_residual_bucket)
        with self.assertRaises(capital.CrossEventBorrowForbidden):
            hard.fund(hard.event_ids[0], capital.C_TOTAL + Decimal('1'), order_id='too-much')
        self.assertEqual(
            (hard.available, hard.committed, hard.identity(), hard.non_trading_residual_bucket),
            before,
        )

    def test_floats_are_rejected(self):
        book = account(capital.A1)
        with self.assertRaises(TypeError):
            book.fund(book.event_ids[0], 1.5, order_id='float')
        self.assertEqual(book.identity(), capital.C_TOTAL)


class SoftReserveTests(unittest.TestCase):
    def test_within_reserve_writes_no_borrow(self):
        book = account(capital.A2)
        event = book.event_ids[3]
        order = book.fund(event, capital.SLICE, order_id='own')
        self.assertEqual(order.own, capital.SLICE)
        self.assertEqual(order.borrows, ())
        self.assertEqual(book.borrow_log, [])
        self.assertEqual(book.unused_reserve(event), Decimal('0'))
        self.assertEqual(book.identity(), capital.C_TOTAL)

    def test_borrow_is_unused_only_and_fifo_by_event_id(self):
        book = account(capital.A2)
        ids = book.event_ids
        borrower = ids[5]
        limited = ids[1]
        second = ids[3]
        for event_id in ids:
            if event_id == borrower:
                continue
            if event_id == limited:
                amount = capital.SLICE - Decimal('15')
            elif event_id == second:
                amount = capital.SLICE - Decimal('100')
            else:
                amount = capital.SLICE
            book.fund(event_id, amount, order_id='prep-%s' % event_id)
        self.assertEqual(book.borrow_log, [])
        order = book.fund(borrower, capital.SLICE + Decimal('40'), order_id='need')
        self.assertEqual(order.own, capital.SLICE)
        self.assertEqual(order.borrows, ((limited, Decimal('15')), (second, Decimal('25'))))
        self.assertEqual([row['donor_event_id'] for row in book.borrow_log], [limited, second])
        self.assertEqual([row['borrower_event_id'] for row in book.borrow_log], [borrower, borrower])
        self.assertTrue(all(row['policy'] == capital.SOFT_POLICY for row in book.borrow_log))
        self.assertEqual([row['sequence'] for row in book.borrow_log], [1, 2])
        self.assertNotIn(borrower, [row['donor_event_id'] for row in book.borrow_log])
        self.assertEqual(book.unused_reserve(limited), Decimal('0'))
        self.assertEqual(book.unused_reserve(second), Decimal('75'))
        self.assertEqual(book.identity(), capital.C_TOTAL)

    def test_borrowers_in_one_batch_run_in_event_id_order(self):
        book = account(capital.A2)
        ids = book.event_ids
        book.fund(ids[0], capital.SLICE - Decimal('10'), order_id='thin')
        later = ids[4]
        earlier = ids[2]
        funded = book.fund_many([
            {'event_id': later, 'amount': capital.SLICE + Decimal('10'), 'order_id': 'later'},
            {'event_id': earlier, 'amount': capital.SLICE + Decimal('10'), 'order_id': 'earlier'},
        ])
        by_id = {order.order_id: order for order in funded}
        self.assertEqual(by_id['earlier'].borrows, ((ids[0], Decimal('10')),))
        self.assertEqual(by_id['later'].borrows, ((ids[1], Decimal('10')),))
        self.assertEqual(
            [(row['borrower_event_id'], row['donor_event_id']) for row in book.borrow_log],
            [(earlier, ids[0]), (later, ids[1])],
        )

    def test_a_failed_batch_does_not_apply_earlier_borrows(self):
        book = account(capital.A2)
        ids = book.event_ids
        with self.assertRaises(capital.InsufficientCapital):
            book.fund_many([
                {'event_id': ids[4], 'amount': capital.C_TOTAL, 'order_id': 'first'},
                {'event_id': ids[0], 'amount': Decimal('1'), 'order_id': 'second'},
            ])
        self.assertEqual(book.borrow_log, [])
        self.assertEqual(book.available, capital.C_TOTAL)
        self.assertEqual(book.identity(), capital.C_TOTAL)

    def test_release_restores_donor_unused_and_keeps_the_log(self):
        book = account(capital.A2)
        ids = book.event_ids
        book.fund(ids[2], capital.SLICE + Decimal('20'), order_id='borrowed')
        self.assertEqual(len(book.borrow_log), 1)
        donor = book.borrow_log[0]['donor_event_id']
        self.assertEqual(donor, ids[0])
        self.assertEqual(book.unused_reserve(donor), capital.SLICE - Decimal('20'))
        book.release('borrowed')
        self.assertEqual(book.unused_reserve(donor), capital.SLICE)
        self.assertEqual(book.available, capital.C_TOTAL)
        self.assertEqual(len(book.borrow_log), 1)
        self.assertEqual(book.identity(), capital.C_TOTAL)

    def test_one_event_can_consume_the_pool_only_by_logging_each_borrow(self):
        book = account(capital.A2)
        borrower = book.event_ids[0]
        order = book.fund(borrower, capital.C_TOTAL, order_id='pool')
        donors = book.event_ids[1:]
        self.assertEqual(order.own, capital.SLICE)
        self.assertEqual(order.unreserved, capital.RESIDUAL)
        self.assertEqual([donor for donor, _amount in order.borrows], list(donors))
        self.assertEqual(len(book.borrow_log), 30)
        borrowed = sum((row['amount'] for row in book.borrow_log), Decimal('0'))
        self.assertEqual(borrowed, capital.SLICE * 30)
        self.assertEqual(book.unreserved_draws[0]['amount'], capital.RESIDUAL)
        self.assertEqual(book.available, Decimal('0'))
        self.assertEqual(book.non_trading_residual_bucket, Decimal('0'))
        self.assertEqual(book.identity(), capital.C_TOTAL)
        with self.assertRaises(capital.InsufficientCapital):
            book.fund(book.event_ids[1], Decimal('1'), order_id='past-pool')

    def test_unreserved_slack_is_drawn_only_after_unused_reserves(self):
        book = account(capital.A2)
        for event_id in book.event_ids:
            book.fund(event_id, capital.SLICE, order_id='slice-%s' % event_id)
        self.assertEqual(book.borrow_log, [])
        self.assertEqual(book.unreserved_available, capital.RESIDUAL)
        drawn = book.fund(book.event_ids[0], capital.RESIDUAL, order_id='slack')
        self.assertEqual(drawn.borrows, ())
        self.assertEqual(drawn.unreserved, capital.RESIDUAL)
        self.assertEqual(book.borrow_log, [])
        self.assertEqual(book.unreserved_draws[0]['amount'], capital.RESIDUAL)
        self.assertEqual(book.available, Decimal('0'))
        before = book.identity()
        with self.assertRaises(capital.InsufficientCapital):
            book.fund(book.event_ids[1], Decimal('1'), order_id='past-slack')
        self.assertEqual(book.unreserved_available, Decimal('0'))
        self.assertEqual(book.identity(), before)


class HardSliceTests(unittest.TestCase):
    def test_a3_refuses_cross_event_borrow(self):
        book = account(capital.A3)
        ids = book.event_ids
        with self.assertRaises(capital.CrossEventBorrowForbidden):
            book.fund(ids[0], capital.SLICE + Decimal('1'), order_id='borrow')
        self.assertEqual(book.borrow_log, [])
        self.assertEqual(book.unused_reserve(ids[0]), capital.SLICE)
        self.assertEqual(book.unused_reserve(ids[1]), capital.SLICE)
        self.assertEqual(book.identity(), capital.C_TOTAL)
        own = book.fund(ids[0], capital.SLICE, order_id='own')
        self.assertEqual(own.borrows, ())
        self.assertEqual(book.borrow_log, [])
        self.assertEqual(book.available, capital.SLICE * 30)
        self.assertEqual(book.non_trading_residual_bucket, capital.RESIDUAL)

    def test_residual_bucket_cannot_fund_orders(self):
        book = account(capital.A3)
        self.assertEqual(book.non_trading_residual_bucket, Decimal('9'))
        self.assertEqual(book.residual_policy, capital.RESIDUAL_POLICY)
        for event_id in book.event_ids:
            book.fund(event_id, capital.SLICE, order_id='slice-%s' % event_id)
        self.assertEqual(book.available, Decimal('0'))
        self.assertEqual(book.committed + book.non_trading_residual_bucket, capital.C_TOTAL)
        with self.assertRaises(capital.ResidualNotTradable):
            book.draw_residual(Decimal('1'))
        with self.assertRaises(capital.CrossEventBorrowForbidden):
            book.fund(book.event_ids[0], Decimal('1'), order_id='from-residual')
        self.assertEqual(book.non_trading_residual_bucket, Decimal('9'))
        self.assertEqual(book.identity(), capital.C_TOTAL)

    def test_a3_batch_failure_leaves_slices_untouched(self):
        book = account(capital.A3)
        event = book.event_ids[0]
        with self.assertRaises(capital.CrossEventBorrowForbidden):
            book.fund_many([
                {'event_id': event, 'amount': capital.SLICE, 'order_id': 'full'},
                {'event_id': event, 'amount': Decimal('1'), 'order_id': 'extra'},
            ])
        self.assertEqual(book.available, capital.SLICE * capital.N_EVENTS)
        self.assertEqual(book.committed, Decimal('0'))
        self.assertEqual(book.identity(), capital.C_TOTAL)


class ScoreboardTests(unittest.TestCase):
    def test_wallet_sum_comparison_is_forbidden(self):
        wallets = [capital.SLICE] * capital.N_EVENTS
        with self.assertRaises(capital.IndependentWalletSumForbidden) as caught:
            capital.compare_independent_wallets_to_shared_account(wallets, capital.C_TOTAL)
        self.assertEqual(caught.exception.code, capital.FORBIDDEN_COMPARISON)
        source = inspect.getsource(capital.compare_independent_wallets_to_shared_account)
        self.assertNotIn('sum', source)
        self.assertNotIn('return', source)
        book = account(capital.A1)
        with self.assertRaises(capital.IndependentWalletSumForbidden):
            capital.promotion_scoreboard(book, wallets=wallets)
        board = capital.promotion_scoreboard(book)
        self.assertEqual(board['promotion_scoreboard'], 'shared_account_only')
        self.assertEqual(board['c_total'], capital.C_TOTAL)
        self.assertEqual(board['identity'], capital.C_TOTAL)
        self.assertIsNone(board['pnl'])
        self.assertFalse(hasattr(capital, 'sum_of_independent_wallets'))

    def test_quote_lock_uses_the_examiner_fee_and_rails_admission(self):
        book = account(capital.A2)
        event = book.event_ids[0]
        maker_fee = feebook.order_fee('maker', Decimal('1'), Decimal('0.50'), round_up=True)
        credit = rails.maker_quote_credit(Decimal('0.50'), Decimal('1'))
        order = book.fund_quote(event, 'maker', Decimal('1'), Decimal('0.50'), order_id='maker')
        self.assertEqual(order.lock, credit['gross'])
        self.assertEqual(order.fee, maker_fee['fee'])
        self.assertEqual(order.fee, credit['fee'])
        self.assertEqual(order.formula_id, feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(order.quote['rule_id'], rails.FEE_CREDIT_RULE_ID)
        self.assertEqual(book.committed, credit['gross'])
        taker_fee = feebook.order_fee('taker', Decimal('1'), Decimal('0.40'), round_up=True)
        taker = book.fund_quote(book.event_ids[1], 'taker', Decimal('1'), Decimal('0.40'), order_id='taker')
        self.assertEqual(taker.lock, taker_fee['price'] * taker_fee['contracts'] + taker_fee['fee'])
        self.assertEqual(taker.formula_id, feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(book.identity(), capital.C_TOTAL)

    def test_refused_maker_credit_moves_no_cash(self):
        book = account(capital.A3)
        before = (book.available, book.committed, book.identity())
        with self.assertRaises(rails.MakerCreditRefused):
            book.fund_quote(book.event_ids[0], 'maker', Decimal('1'), Decimal('0.01'), order_id='refused')
        self.assertEqual((book.available, book.committed, book.identity()), before)
        self.assertEqual(book.borrow_log, [])

    def test_scorecard_requires_the_examiner_channel_and_stores_no_pnl(self):
        book = account(capital.A1)
        with self.assertRaises(feebook.CompletedProfitRefused):
            capital.measurement_scorecard(book, inventory_flat=True)
        taker = feebook.order_fee('taker', Decimal('1'), Decimal('0.50'))
        maker = feebook.order_fee('maker', Decimal('1'), Decimal('0.50'))
        channel = feebook.examiner_fee_channel(taker, maker)
        card = {
            'kind': 'measurement',
            'arm': book.arm,
            'c_total': format(book.c_total, 'f'),
            'pnl': None,
            'inventory_flat': True,
            'fee_channel': channel,
        }
        self.assertEqual(
            capital.measurement_scorecard(book, fee_channel=channel, inventory_flat=True),
            feebook.classify_scorecard(card),
        )
        self.assertIsNone(capital.promotion_scoreboard(book)['pnl'])

    def test_live_adapter_is_refused(self):
        with self.assertRaises(capital.LiveOrdersForbidden):
            capital.execution_adapter()
        self.assertIs(capital.LIVE_ORDERS, False)


if __name__ == '__main__':
    unittest.main()
