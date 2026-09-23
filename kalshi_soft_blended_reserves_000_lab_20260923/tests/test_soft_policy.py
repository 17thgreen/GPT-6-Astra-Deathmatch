"""Unit pins for Cap-SR soft policies.

Synthetic cash movements check the frozen invariants. They are not a
historical walk and they are not profit.
"""
import hashlib
import inspect
import json
import subprocess
import sys
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(PARENT / 'kalshi_capital_structure_lab_20260922'))
sys.path.insert(0, str(PARENT / 'kalshi_feebook_lab_20260922'))
sys.path.insert(0, str(PARENT / 'kalshi_rails_lab_20260922'))

import capital_structure as capital
import feebook
import rails
import soft_policy as soft


def account(arm, event_ids=None):
    return soft.open_account(arm, event_ids)


def _rows(book):
    return [
        (row['borrower_event_id'], row['donor_event_id'], row['amount'], row['sequence'])
        for row in book.borrow_log
    ]


class PinTests(unittest.TestCase):
    def test_constants_match_the_freeze(self):
        frozen = json.loads(soft.FROZEN_EXPERIMENT.read_text())
        empty = json.loads(soft.EMPTY_RESULTS.read_text())
        self.assertEqual(soft.C_TOTAL, Decimal(frozen['C_total_usd']))
        self.assertEqual(soft.N_EVENTS, frozen['N_events'])
        self.assertEqual(soft.R_M, Decimal(frozen['slice_usd']))
        self.assertEqual(soft.RESIDUAL, Decimal(frozen['residual_usd']))
        self.assertEqual(soft.R_M * soft.N_EVENTS + soft.RESIDUAL, soft.C_TOTAL)
        self.assertEqual(soft.RESIDUAL_POLICY, frozen['residual_policy'])
        self.assertEqual(soft.BLEND_SEAT, Decimal('80'))
        self.assertEqual(soft.LOCAL_SEAT, Decimal('81'))
        self.assertEqual(
            soft.BLEND_SEAT * soft.N_EVENTS + soft.LOCAL_SEAT * soft.N_EVENTS + soft.RESIDUAL,
            soft.C_TOTAL,
        )
        self.assertEqual([arm['id'] for arm in frozen['arms']], list(soft.ARMS))
        self.assertEqual(frozen['arms'][0]['soft_policy'], soft.SR0_POLICY)
        self.assertEqual(frozen['arms'][1]['soft_policy'], soft.SR1_POLICY)
        self.assertEqual(frozen['arms'][2]['soft_policy'], soft.SR2_POLICY)
        self.assertEqual(frozen['arms'][2]['blend_fraction'], 0.5)
        self.assertEqual(soft.SR0_POLICY, capital.SOFT_POLICY)
        self.assertEqual(frozen['capital_substrate'], 'A2_shared_soft_reserve')
        self.assertEqual(frozen['knob'], 'soft_policy_only')
        self.assertEqual(frozen['feature_family'], 'Cap-SR')
        self.assertEqual(frozen['not_feature_families'], ['F1', 'F2', 'F3'])
        self.assertEqual(frozen['nearest_dead_cards'], ['C1_empty_book', 'Q7_Arm_B_kill'])
        self.assertEqual(frozen['promotion_scoreboard'], 'shared_account_only')
        self.assertEqual(frozen['forbidden'], soft.FORBIDDEN_COMPARISON)
        self.assertIs(frozen['signal_retune'], False)
        self.assertIs(frozen['live_orders'], False)
        self.assertIs(frozen['queue_fragility_reopen'], False)
        self.assertEqual(frozen['strategy_pointer'], 'Q6-000')
        self.assertEqual(frozen['fee_pin'], soft.FEEBOOK_COMMIT)
        self.assertEqual(frozen['rails_pin'], soft.RAILS_COMMIT)
        self.assertEqual(frozen['parent_capital_lab_pin'], 'ce4671b8')
        self.assertTrue(soft.PARENT_CAPITAL_PIN.startswith(frozen['parent_capital_lab_pin']))
        self.assertEqual(tuple(frozen['scorecard_fields']), soft.SCORECARD_FIELDS)
        self.assertIsNone(frozen['results'])
        self.assertIsNone(frozen['pnl'])
        for key in ('results', 'pnl', *soft.SCORECARD_FIELDS):
            self.assertIsNone(empty[key])
        self.assertEqual(empty['status'], 'EMPTY_RESULTS_PRE_EXAMINER')
        self.assertEqual(soft.published_scorecard()['pnl'], None)
        self.assertTrue(all(soft.published_scorecard()[key] is None for key in soft.SCORECARD_FIELDS))

    def test_packet_copies_and_shadow_hashes(self):
        frozen = json.loads(soft.FROZEN_EXPERIMENT.read_text())
        self.assertFalse(soft.GOVERNANCE_TREE.exists())
        copies = (
            soft.PACKET,
            soft.GOVERNANCE_PACKET,
            soft.LAB_BUNDLE / soft.PACKET.name,
            soft.GOVERNANCE_BUNDLE / soft.PACKET.name,
        )
        digest = hashlib.sha256(soft.PACKET.read_bytes()).hexdigest()
        self.assertEqual(digest, soft.PACKET_SHA256)
        self.assertEqual(digest, frozen['packet_sha256'])
        for path in copies:
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), soft.PACKET_SHA256)
        frozen_copies = (
            soft.FROZEN_EXPERIMENT,
            soft.LAB_BUNDLE / 'FROZEN_EXPERIMENT.json',
            soft.GOVERNANCE_BUNDLE / 'FROZEN_EXPERIMENT.json',
        )
        frozen_bytes = soft.FROZEN_EXPERIMENT.read_bytes()
        for path in frozen_copies:
            self.assertEqual(path.read_bytes(), frozen_bytes)
            payload = json.loads(path.read_text())
            self.assertIsNone(payload['results'])
            self.assertIsNone(payload['pnl'])
        empty_copies = (
            soft.EMPTY_RESULTS,
            soft.LAB_BUNDLE / 'results.json',
            soft.GOVERNANCE_BUNDLE / 'results.json',
        )
        empty_bytes = soft.EMPTY_RESULTS.read_bytes()
        for path in empty_copies:
            self.assertEqual(path.read_bytes(), empty_bytes)
        self.assertEqual(soft.sha256_file(soft.SHADOW_FREEZE), frozen['shadow_freeze_sha256'])
        self.assertEqual(soft.sha256_file(soft.TAPE_MANIFEST), frozen['tape_manifest_sha256'])
        shadow = json.loads(soft.SHADOW_FREEZE.read_text())
        self.assertEqual(shadow['selected'], '000')

    def test_fee_source_is_feebook_and_queue_source_is_rails(self):
        binding = soft.instrument_binding()
        self.assertEqual(binding['fee_source'], 'feebook')
        self.assertEqual(binding['queue_source'], 'rails')
        self.assertEqual(Path(feebook.__file__).resolve().parent.name, 'kalshi_feebook_lab_20260922')
        self.assertEqual(Path(rails.__file__).resolve().parent.name, 'kalshi_rails_lab_20260922')
        self.assertEqual(Path(capital.__file__).resolve().parent.name, 'kalshi_capital_structure_lab_20260922')
        self.assertEqual(binding['fee_pin'], '22371178cb2663250b4762f328069571c48cb551')
        self.assertEqual(binding['rails_pin'], '6a28e0d6254327ea4e6451c781bec56215ac6cac')
        self.assertEqual(binding['examiner_formula_id'], feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(binding['fee_credit_rule_id'], rails.FEE_CREDIT_RULE_ID)
        self.assertEqual(binding['primary_queue_ahead'], rails.scenario_queue('q3300'))
        self.assertEqual(binding['harsh_twin_queue_ahead'], rails.scenario_queue('q10000'))
        self.assertIs(binding['fee_is_knob'], False)
        self.assertIs(binding['queue_is_knob'], False)
        self.assertIs(binding['harsh_twin_is_capital_knob'], False)
        self.assertIs(binding['queue_fragility_reopen'], False)
        self.assertEqual(binding['knob'], 'soft_policy_only')
        self.assertEqual(binding['strategy_pointer'], 'Q6-000')
        rates = feebook.load_series_table()['rates']
        self.assertEqual(binding['taker_rate'], feebook.as_decimal(rates['taker'], 'taker'))
        self.assertEqual(binding['maker_rate'], feebook.as_decimal(rates['maker'], 'maker'))
        source = (ROOT / 'soft_policy.py').read_text()
        for banned in (
            '0.0175',
            '0.07',
            'maker_coefficient',
            'taker_coefficient',
            'common_config',
            'import queue_fragility',
            'kalshi_queue_fragility_000_lab_20260922',
            'factorial_policy',
            'paircheck_policy',
            'class KalshiExecutionAdapter',
        ):
            self.assertNotIn(banned, source)
        self.assertIn("fee_source': 'feebook'", source)
        self.assertIn("queue_source': 'rails'", source)

    def test_pinned_labs_match_their_commits(self):
        for commit, path in (
            (soft.FEEBOOK_COMMIT, 'kalshi_feebook_lab_20260922'),
            (soft.RAILS_COMMIT, 'kalshi_rails_lab_20260922'),
            (soft.PARENT_CAPITAL_PIN, 'kalshi_capital_structure_lab_20260922'),
        ):
            diff = subprocess.run(
                ['git', 'diff', '--exit-code', commit, '--', path],
                cwd=PARENT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(diff.returncode, 0, diff.stdout + diff.stderr)
            ancestor = subprocess.run(
                ['git', 'merge-base', '--is-ancestor', commit, 'HEAD'],
                cwd=PARENT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(ancestor.returncode, 0, ancestor.stderr)

    def test_default_cohort_is_31_development_events(self):
        membership = json.loads(soft.WEEK_MEMBERSHIP.read_text())
        ids = soft.development_cohort_event_ids()
        self.assertEqual(ids, tuple(sorted(membership.keys())))
        self.assertEqual(len(ids), 31)
        opened = account(soft.SR0)
        self.assertEqual(opened.event_ids, ids)

    def test_a1_and_a3_stay_closed(self):
        for arm in (capital.A1, capital.A3, 'A1', 'A3'):
            with self.assertRaises(soft.ClosedArm):
                soft.open_account(arm)
        book = account(soft.SR0)
        self.assertEqual(book.a2_control.arm, capital.A2)
        self.assertIsInstance(book.a2_control, capital.CapitalAccount)
        self.assertEqual(book.soft_policy, capital.SOFT_POLICY)

    def test_live_adapter_is_refused(self):
        with self.assertRaises(capital.LiveOrdersForbidden):
            soft.execution_adapter()
        self.assertIs(soft.LIVE_ORDERS, False)


class IdentityTests(unittest.TestCase):
    def test_every_arm_starts_at_the_same_c_total_with_residual_9(self):
        for arm in soft.ARMS:
            book = account(arm)
            self.assertEqual(book.c_total, soft.C_TOTAL)
            self.assertEqual(book.identity(), soft.C_TOTAL)
            self.assertEqual(book.non_trading_residual_bucket, soft.RESIDUAL)
            self.assertEqual(book.residual_policy, soft.RESIDUAL_POLICY)
            self.assertTrue(book.shared_account)
            self.assertEqual(book.borrow_log, [])
            self.assertEqual(book.blend_log, [])
            self.assertEqual(
                book.available + book.committed + book.non_trading_residual_bucket,
                soft.C_TOTAL,
            )

    def test_floats_are_rejected(self):
        book = account(soft.SR1)
        with self.assertRaises(TypeError):
            book.fund(book.event_ids[0], 1.5, order_id='float')
        self.assertEqual(book.identity(), soft.C_TOTAL)

    def test_residual_cannot_fund_orders_on_any_arm(self):
        for arm in soft.ARMS:
            book = account(arm)
            before = (book.available, book.committed, book.identity(), book.non_trading_residual_bucket)
            with self.assertRaises(capital.ResidualNotTradable):
                book.draw_residual(Decimal('1'))
            self.assertEqual(
                (book.available, book.committed, book.identity(), book.non_trading_residual_bucket),
                before,
            )
            self.assertEqual(book.non_trading_residual_bucket, Decimal('9'))


class FifoControlTests(unittest.TestCase):
    def test_within_reserve_matches_a2_and_writes_no_borrow(self):
        ids = account(soft.SR0).event_ids
        sr0 = account(soft.SR0, ids)
        a2 = capital.open_account(capital.A2, ids)
        order = sr0.fund(ids[3], soft.R_M, order_id='own')
        a2_order = a2.fund(ids[3], soft.R_M, order_id='own')
        self.assertEqual(order.own, soft.R_M)
        self.assertEqual(order.borrows, ())
        self.assertEqual(order.borrows, a2_order.borrows)
        self.assertEqual(sr0.borrow_log, [])
        self.assertEqual(_rows(sr0), _rows(a2))
        self.assertEqual(sr0.unused_reserve(ids[3]), Decimal('0'))
        self.assertEqual(sr0.identity(), soft.C_TOTAL)

    def test_borrow_order_matches_a2_fifo(self):
        ids = account(soft.SR0).event_ids
        sr0 = account(soft.SR0, ids)
        a2 = capital.open_account(capital.A2, ids)
        borrower = ids[5]
        limited = ids[1]
        second = ids[3]
        requests = []
        for event_id in ids:
            if event_id == borrower:
                continue
            if event_id == limited:
                amount = soft.R_M - Decimal('15')
            elif event_id == second:
                amount = soft.R_M - Decimal('100')
            else:
                amount = soft.R_M
            requests.append({
                'event_id': event_id,
                'amount': amount,
                'order_id': 'prep-%s' % event_id,
            })
        sr0.fund_many(requests)
        a2.fund_many(requests)
        self.assertEqual(sr0.borrow_log, [])
        sr0.fund(borrower, soft.R_M + Decimal('40'), order_id='need')
        a2.fund(borrower, soft.R_M + Decimal('40'), order_id='need')
        self.assertEqual(
            [(donor, amount) for donor, amount in sr0.order('need').borrows],
            [(limited, Decimal('15')), (second, Decimal('25'))],
        )
        self.assertEqual(_rows(sr0), _rows(a2))
        self.assertTrue(all(row['policy'] == soft.SR0_POLICY for row in sr0.borrow_log))
        self.assertEqual(sr0.unused_reserve(limited), a2.unused_reserve(limited))
        self.assertEqual(sr0.unused_reserve(second), Decimal('75'))
        self.assertEqual(sr0.identity(), soft.C_TOTAL)

    def test_batched_borrowers_match_a2_event_id_order(self):
        ids = account(soft.SR0).event_ids
        sr0 = account(soft.SR0, ids)
        a2 = capital.open_account(capital.A2, ids)
        prep = {'event_id': ids[0], 'amount': soft.R_M - Decimal('10'), 'order_id': 'thin'}
        sr0.fund_many([prep])
        a2.fund_many([prep])
        batch = [
            {'event_id': ids[4], 'amount': soft.R_M + Decimal('10'), 'order_id': 'later'},
            {'event_id': ids[2], 'amount': soft.R_M + Decimal('10'), 'order_id': 'earlier'},
        ]
        sr0.fund_many(batch)
        a2.fund_many(batch)
        self.assertEqual(_rows(sr0), _rows(a2))
        self.assertEqual(sr0.order('earlier').borrows, ((ids[0], Decimal('10')),))
        self.assertEqual(sr0.order('later').borrows, ((ids[1], Decimal('10')),))

    def test_failed_batch_matches_a2_and_applies_nothing(self):
        ids = account(soft.SR0).event_ids
        sr0 = account(soft.SR0, ids)
        before = (sr0.available, sr0.committed, sr0.identity())
        with self.assertRaises(capital.InsufficientCapital):
            sr0.fund_many([
                {'event_id': ids[4], 'amount': soft.C_TOTAL, 'order_id': 'first'},
                {'event_id': ids[0], 'amount': Decimal('1'), 'order_id': 'second'},
            ])
        self.assertEqual((sr0.available, sr0.committed, sr0.identity()), before)
        self.assertEqual(sr0.borrow_log, [])
        self.assertEqual(sr0.non_trading_residual_bucket, Decimal('9'))

    def test_release_restores_donors_and_keeps_the_log(self):
        ids = account(soft.SR0).event_ids
        sr0 = account(soft.SR0, ids)
        a2 = capital.open_account(capital.A2, ids)
        sr0.fund(ids[2], soft.R_M + Decimal('20'), order_id='borrowed')
        a2.fund(ids[2], soft.R_M + Decimal('20'), order_id='borrowed')
        donor = sr0.borrow_log[0]['donor_event_id']
        self.assertEqual(donor, ids[0])
        sr0.release('borrowed')
        a2.release('borrowed')
        self.assertEqual(sr0.unused_reserve(donor), soft.R_M)
        self.assertEqual(sr0.unused_reserve(donor), a2.unused_reserve(donor))
        self.assertEqual(len(sr0.borrow_log), 1)
        self.assertEqual(_rows(sr0), _rows(a2))
        self.assertEqual(sr0.available, soft.R_M * soft.N_EVENTS)
        self.assertEqual(sr0.identity(), soft.C_TOTAL)

    def test_reserved_pool_matches_a2_and_residual_stays_non_trading(self):
        ids = account(soft.SR0).event_ids
        sr0 = account(soft.SR0, ids)
        a2 = capital.open_account(capital.A2, ids)
        reserved = soft.R_M * soft.N_EVENTS
        sr0.fund(ids[0], reserved, order_id='pool')
        a2.fund(ids[0], reserved, order_id='pool')
        self.assertEqual(sr0.order('pool').own, soft.R_M)
        self.assertEqual(sr0.order('pool').unreserved, Decimal('0'))
        self.assertEqual(len(sr0.borrow_log), 30)
        self.assertEqual(_rows(sr0), _rows(a2))
        self.assertEqual(sr0.unreserved_draws, [])
        self.assertEqual(a2.unreserved_draws, [])
        self.assertEqual(sr0.available, Decimal('0'))
        self.assertEqual(sr0.non_trading_residual_bucket, Decimal('9'))
        self.assertEqual(a2.non_trading_residual_bucket, Decimal('0'))
        self.assertEqual(a2.unreserved_available, Decimal('9'))
        before = (sr0.available, sr0.committed, sr0.identity(), len(sr0.borrow_log))
        with self.assertRaises(capital.InsufficientCapital):
            sr0.fund(ids[1], Decimal('1'), order_id='residual')
        self.assertEqual(
            (sr0.available, sr0.committed, sr0.identity(), len(sr0.borrow_log)),
            before,
        )
        slack = a2.fund(ids[1], Decimal('1'), order_id='slack')
        self.assertEqual(slack.unreserved, Decimal('1'))
        self.assertEqual(sr0.non_trading_residual_bucket, Decimal('9'))
        self.assertEqual(sr0.identity(), soft.C_TOTAL)


class ProRataTests(unittest.TestCase):
    def _seat_three_donors(self, book, borrower):
        ids = book.event_ids
        donors = {
            ids[0]: Decimal('10'),
            ids[1]: Decimal('30'),
            ids[2]: Decimal('60'),
        }
        self.assertNotIn(borrower, donors)
        for event_id in ids:
            if event_id == borrower:
                continue
            unused = donors.get(event_id, Decimal('0'))
            book.fund(event_id, soft.R_M - unused, order_id='prep-%s' % event_id)
        return ids[0], ids[1], ids[2]

    def test_donors_pay_pro_rata_to_unused(self):
        book = account(soft.SR1)
        borrower = book.event_ids[10]
        first, second, third = self._seat_three_donors(book, borrower)
        order = book.fund(borrower, soft.R_M + Decimal('20'), order_id='need')
        self.assertEqual(order.own, soft.R_M)
        self.assertEqual(order.borrows, (
            (first, Decimal('2')),
            (second, Decimal('6')),
            (third, Decimal('12')),
        ))
        self.assertEqual([row['donor_event_id'] for row in book.borrow_log], [first, second, third])
        self.assertTrue(all(row['policy'] == soft.SR1_POLICY for row in book.borrow_log))
        self.assertEqual([row['amount'] for row in book.borrow_log], [
            Decimal('2'), Decimal('6'), Decimal('12'),
        ])
        borrowed = sum((row['amount'] for row in book.borrow_log), Decimal('0'))
        self.assertEqual(borrowed, Decimal('20'))
        self.assertEqual(book.unused_reserve(first), Decimal('8'))
        self.assertEqual(book.unused_reserve(second), Decimal('24'))
        self.assertEqual(book.unused_reserve(third), Decimal('48'))
        self.assertEqual(book.blend_log, [])
        self.assertEqual(book.non_trading_residual_bucket, Decimal('9'))
        self.assertEqual(book.identity(), soft.C_TOTAL)

    def test_same_seat_is_fifo_on_sr0(self):
        ids = account(soft.SR0).event_ids
        fifo = account(soft.SR0, ids)
        borrower = ids[10]
        self._seat_three_donors(fifo, borrower)
        order = fifo.fund(borrower, soft.R_M + Decimal('20'), order_id='need')
        self.assertEqual(order.borrows, (
            (ids[0], Decimal('10')),
            (ids[1], Decimal('10')),
        ))
        self.assertNotEqual(
            [row['donor_event_id'] for row in fifo.borrow_log],
            [ids[0], ids[1], ids[2]],
        )

    def test_over_unused_refuses_and_leaves_residual(self):
        book = account(soft.SR1)
        borrower = book.event_ids[4]
        self._seat_three_donors(book, borrower)
        before = (book.available, book.committed, book.identity(), list(book.borrow_log))
        with self.assertRaises(capital.InsufficientCapital):
            book.fund(borrower, soft.R_M + Decimal('101'), order_id='too-much')
        self.assertEqual(
            (book.available, book.committed, book.identity(), list(book.borrow_log)),
            before,
        )
        self.assertEqual(book.non_trading_residual_bucket, Decimal('9'))

    def test_hamilton_remainder_sums_and_respects_caps(self):
        book = account(soft.SR1)
        ids = book.event_ids
        borrower = ids[6]
        donors = (ids[0], ids[1], ids[2])
        for event_id in ids:
            if event_id == borrower:
                continue
            unused = Decimal('1') if event_id in donors else Decimal('0')
            book.fund(event_id, soft.R_M - unused, order_id='prep-%s' % event_id)
        order = book.fund(borrower, soft.R_M + Decimal('2'), order_id='split')
        takes = [amount for _donor, amount in order.borrows]
        self.assertEqual(sum(takes, Decimal('0')), Decimal('2'))
        self.assertEqual(len(takes), 3)
        self.assertTrue(all(amount <= Decimal('1') for amount in takes))
        self.assertTrue(all(amount > 0 for amount in takes))
        self.assertNotEqual(order.borrows, ((donors[0], Decimal('1')), (donors[1], Decimal('1'))))
        self.assertEqual(book.identity(), soft.C_TOTAL)

    def test_failed_batch_does_not_apply_the_earlier_borrow(self):
        book = account(soft.SR1)
        ids = book.event_ids
        with self.assertRaises(capital.InsufficientCapital):
            book.fund_many([
                {'event_id': ids[4], 'amount': soft.R_M * soft.N_EVENTS, 'order_id': 'first'},
                {'event_id': ids[0], 'amount': Decimal('1'), 'order_id': 'second'},
            ])
        self.assertEqual(book.borrow_log, [])
        self.assertEqual(book.available, soft.R_M * soft.N_EVENTS)
        self.assertEqual(book.identity(), soft.C_TOTAL)

    def test_release_restores_proportional_donors(self):
        book = account(soft.SR1)
        borrower = book.event_ids[10]
        first, second, third = self._seat_three_donors(book, borrower)
        book.fund(borrower, soft.R_M + Decimal('20'), order_id='need')
        book.release('need')
        self.assertEqual(book.unused_reserve(first), Decimal('10'))
        self.assertEqual(book.unused_reserve(second), Decimal('30'))
        self.assertEqual(book.unused_reserve(third), Decimal('60'))
        self.assertEqual(len(book.borrow_log), 3)
        self.assertEqual(book.identity(), soft.C_TOTAL)


class BlendPoolTests(unittest.TestCase):
    def test_local_spend_writes_no_blend_draw(self):
        book = account(soft.SR2)
        event = book.event_ids[4]
        order = book.fund(event, soft.LOCAL_SEAT, order_id='local')
        self.assertEqual(order.own, soft.LOCAL_SEAT)
        self.assertEqual(order.blend, Decimal('0'))
        self.assertEqual(order.borrows, ())
        self.assertEqual(book.blend_log, [])
        self.assertEqual(book.borrow_log, [])
        self.assertEqual(book.unused_reserve(event), Decimal('0'))
        self.assertEqual(book.blend_available, soft.BLEND_SEAT * soft.N_EVENTS)
        self.assertEqual(book.identity(), soft.C_TOTAL)

    def test_draw_order_is_local_then_blend_then_refuse(self):
        book = account(soft.SR2)
        ids = book.event_ids
        event = ids[7]
        neighbor = ids[1]
        order = book.fund(event, soft.LOCAL_SEAT + Decimal('25'), order_id='blend')
        self.assertEqual(order.own, soft.LOCAL_SEAT)
        self.assertEqual(order.blend, Decimal('25'))
        self.assertEqual(book.borrow_log, [])
        self.assertEqual(len(book.blend_log), 1)
        self.assertEqual(book.blend_log[0]['source'], 'blend_pool')
        self.assertEqual(book.blend_log[0]['amount'], Decimal('25'))
        self.assertEqual(book.blend_log[0]['borrower_event_id'], event)
        self.assertEqual(book.blend_log[0]['policy'], soft.SR2_POLICY)
        self.assertEqual(book.unused_reserve(neighbor), soft.LOCAL_SEAT)
        rest = book.blend_available
        taken = book.fund(event, rest, order_id='rest')
        self.assertEqual(taken.own, Decimal('0'))
        self.assertEqual(taken.blend, rest)
        self.assertEqual(book.blend_available, Decimal('0'))
        self.assertEqual(book.unused_reserve(neighbor), soft.LOCAL_SEAT)
        before = (book.available, book.committed, book.identity(), len(book.blend_log))
        with self.assertRaises(capital.InsufficientCapital):
            book.fund(event, Decimal('1'), order_id='past')
        self.assertEqual(
            (book.available, book.committed, book.identity(), len(book.blend_log)),
            before,
        )
        self.assertEqual(book.non_trading_residual_bucket, Decimal('9'))
        neighbor_order = book.fund(neighbor, soft.LOCAL_SEAT, order_id='neighbor')
        self.assertEqual(neighbor_order.blend, Decimal('0'))
        self.assertEqual(book.identity(), soft.C_TOTAL)

    def test_one_event_cannot_spend_another_events_local_reserve(self):
        book = account(soft.SR2)
        ids = book.event_ids
        pool = soft.BLEND_SEAT * soft.N_EVENTS
        order = book.fund(ids[0], soft.LOCAL_SEAT + pool, order_id='all-blend')
        self.assertEqual(order.own, soft.LOCAL_SEAT)
        self.assertEqual(order.blend, pool)
        self.assertEqual(book.borrow_log, [])
        self.assertEqual(len(book.blend_log), 1)
        for event_id in ids[1:]:
            self.assertEqual(book.unused_reserve(event_id), soft.LOCAL_SEAT)
        with self.assertRaises(capital.InsufficientCapital):
            book.fund(ids[0], Decimal('1'), order_id='other-local')
        self.assertEqual(book.unused_reserve(ids[1]), soft.LOCAL_SEAT)
        self.assertEqual(book.non_trading_residual_bucket, Decimal('9'))
        self.assertEqual(book.identity(), soft.C_TOTAL)

    def test_batched_borrowers_take_the_blend_pool_in_event_id_order(self):
        book = account(soft.SR2)
        ids = book.event_ids
        funded = book.fund_many([
            {'event_id': ids[5], 'amount': soft.LOCAL_SEAT + Decimal('5'), 'order_id': 'later'},
            {'event_id': ids[2], 'amount': soft.LOCAL_SEAT + Decimal('7'), 'order_id': 'earlier'},
        ])
        by_id = {order.order_id: order for order in funded}
        self.assertEqual(by_id['earlier'].blend, Decimal('7'))
        self.assertEqual(by_id['later'].blend, Decimal('5'))
        self.assertEqual(
            [row['borrower_event_id'] for row in book.blend_log],
            [ids[2], ids[5]],
        )

    def test_failed_blend_batch_applies_nothing(self):
        book = account(soft.SR2)
        event = book.event_ids[0]
        with self.assertRaises(capital.InsufficientCapital):
            book.fund_many([
                {'event_id': event, 'amount': soft.LOCAL_SEAT, 'order_id': 'local'},
                {'event_id': event, 'amount': soft.C_TOTAL, 'order_id': 'over'},
            ])
        self.assertEqual(book.blend_log, [])
        self.assertEqual(book.blend_available, soft.BLEND_SEAT * soft.N_EVENTS)
        self.assertEqual(book.unused_reserve(event), soft.LOCAL_SEAT)
        self.assertEqual(book.identity(), soft.C_TOTAL)

    def test_release_restores_local_and_blend_and_keeps_the_log(self):
        book = account(soft.SR2)
        event = book.event_ids[3]
        book.fund(event, soft.LOCAL_SEAT + Decimal('15'), order_id='blend')
        book.release('blend')
        self.assertEqual(book.unused_reserve(event), soft.LOCAL_SEAT)
        self.assertEqual(book.blend_available, soft.BLEND_SEAT * soft.N_EVENTS)
        self.assertEqual(len(book.blend_log), 1)
        self.assertEqual(book.available, soft.LOCAL_SEAT * soft.N_EVENTS + soft.BLEND_SEAT * soft.N_EVENTS)
        self.assertEqual(book.identity(), soft.C_TOTAL)


class ScoreboardTests(unittest.TestCase):
    def test_wallet_sum_comparison_is_forbidden(self):
        wallets = [soft.R_M] * soft.N_EVENTS
        with self.assertRaises(capital.IndependentWalletSumForbidden) as caught:
            soft.compare_independent_wallets_to_shared_account(wallets, soft.C_TOTAL)
        self.assertEqual(caught.exception.code, soft.FORBIDDEN_COMPARISON)
        source = inspect.getsource(soft.compare_independent_wallets_to_shared_account)
        self.assertNotIn('sum', source)
        self.assertNotIn('return', source)
        book = account(soft.SR1)
        with self.assertRaises(capital.IndependentWalletSumForbidden):
            soft.promotion_scoreboard(book, wallets=wallets)
        board = soft.promotion_scoreboard(book)
        self.assertEqual(board['promotion_scoreboard'], 'shared_account_only')
        self.assertEqual(board['c_total'], soft.C_TOTAL)
        self.assertEqual(board['identity'], soft.C_TOTAL)
        self.assertIsNone(board['pnl'])
        for key in soft.SCORECARD_FIELDS:
            self.assertIsNone(board[key])
        self.assertFalse(hasattr(soft, 'sum_of_independent_wallets'))

    def test_quote_lock_uses_the_examiner_fee_and_rails_admission(self):
        book = account(soft.SR0)
        event = book.event_ids[0]
        maker_fee = feebook.order_fee('maker', Decimal('1'), Decimal('0.50'), round_up=True)
        credit = rails.maker_quote_credit(Decimal('0.50'), Decimal('1'))
        order = book.fund_quote(event, 'maker', Decimal('1'), Decimal('0.50'), order_id='maker')
        self.assertEqual(order.lock, credit['gross'])
        self.assertEqual(order.fee, maker_fee['fee'])
        self.assertEqual(order.formula_id, feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(order.quote['rule_id'], rails.FEE_CREDIT_RULE_ID)
        taker_fee = feebook.order_fee('taker', Decimal('1'), Decimal('0.40'), round_up=True)
        taker = book.fund_quote(book.event_ids[1], 'taker', Decimal('1'), Decimal('0.40'), order_id='taker')
        self.assertEqual(taker.lock, taker_fee['price'] * taker_fee['contracts'] + taker_fee['fee'])
        self.assertEqual(taker.formula_id, feebook.EXAMINER_FORMULA_ID)
        self.assertEqual(book.identity(), soft.C_TOTAL)
        self.assertEqual(book.borrow_log, [])

    def test_refused_maker_credit_moves_no_cash(self):
        book = account(soft.SR2)
        before = (book.available, book.committed, book.identity(), list(book.blend_log))
        with self.assertRaises(rails.MakerCreditRefused):
            book.fund_quote(book.event_ids[0], 'maker', Decimal('1'), Decimal('0.01'), order_id='refused')
        self.assertEqual(
            (book.available, book.committed, book.identity(), list(book.blend_log)),
            before,
        )

    def test_scorecard_requires_the_examiner_channel_and_stores_no_pnl(self):
        book = account(soft.SR1)
        with self.assertRaises(feebook.CompletedProfitRefused):
            soft.measurement_scorecard(book, inventory_flat=True)
        taker = feebook.order_fee('taker', Decimal('1'), Decimal('0.50'))
        maker = feebook.order_fee('maker', Decimal('1'), Decimal('0.50'))
        channel = feebook.examiner_fee_channel(taker, maker)
        label = soft.measurement_scorecard(book, fee_channel=channel, inventory_flat=True)
        self.assertEqual(label, 'completed_profit')
        self.assertIsNone(soft.promotion_scoreboard(book)['pnl'])
        for key in soft.SCORECARD_FIELDS:
            self.assertIsNone(soft.published_scorecard()[key])


if __name__ == '__main__':
    unittest.main()
