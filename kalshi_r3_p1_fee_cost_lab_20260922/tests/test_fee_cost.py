"""Unit pins for venue fee_cost versus the imported R1-P1 fee model.

Deltas are Decimal. A model-only completed net is refused when fee_cost was
available. Freeze results and pnl stay null.
"""
import hashlib
import json
import subprocess
import sys
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT.parent
FEEBOOK = PARENT / 'kalshi_feebook_lab_20260922'
sys.path.insert(0, str(ROOT))

import fee_cost
import feebook


def _by_case(scored=None):
    if scored is None:
        scored = fee_cost.score_fixture()
    return {row['case_id']: row for row in scored['rows']}


class PinTests(unittest.TestCase):
    def test_binding_cites_packet_and_imported_feebook(self):
        binding = fee_cost.instrument_binding()
        self.assertEqual(binding['packet_id'], 'R3-P1-FEE-COST-VS-MODEL')
        self.assertEqual(binding['feebook_commit'], fee_cost.FEEBOOK_COMMIT)
        self.assertEqual(
            binding['feebook_commit'],
            '22371178cb2663250b4762f328069571c48cb551',
        )
        self.assertIs(binding['feebook_imported'], True)
        self.assertIs(binding['feebook_copied'], False)
        self.assertEqual(
            binding['examiner_formula_id'],
            feebook.EXAMINER_FORMULA_ID,
        )
        self.assertNotEqual(
            binding['examiner_formula_id'],
            binding['comparator_formula_id'],
        )
        self.assertEqual(
            binding['symbols'],
            ('order_fee', 'examiner_fee_channel', 'classify_scorecard'),
        )
        self.assertIs(binding['q6_000_retune'], False)
        self.assertIs(binding['signal_retune'], False)
        self.assertIs(binding['live_orders'], False)
        table = feebook.load_series_table()
        self.assertEqual(
            binding['taker_rate'],
            feebook.as_decimal(table['rates']['taker'], 'taker'),
        )
        self.assertEqual(
            binding['maker_rate'],
            feebook.as_decimal(table['rates']['maker'], 'maker'),
        )
        self.assertNotEqual(binding['taker_rate'], binding['maker_rate'])

    def test_feebook_import_is_the_sibling_pin(self):
        self.assertFalse((ROOT / 'feebook.py').exists())
        resolved = Path(fee_cost.feebook.__file__).resolve()
        self.assertEqual(resolved, (FEEBOOK / 'feebook.py').resolve())
        proc = subprocess.run(
            ['git', 'diff', '--exit-code', fee_cost.FEEBOOK_COMMIT, '--', fee_cost.FEEBOOK_DIRECTORY],
            cwd=PARENT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        frozen = json.loads((FEEBOOK / 'FROZEN_EXPERIMENT.json').read_text())
        digest = hashlib.sha256((FEEBOOK / 'feebook.py').read_bytes()).hexdigest()
        self.assertEqual(digest, frozen['implementation_sha256']['feebook.py'])

    def test_naked_fee_literals_are_absent_from_source(self):
        source = (ROOT / 'fee_cost.py').read_text()
        for banned in (
            '0.0175',
            '0.07',
            '.0175',
            'maker_coefficient',
            'taker_coefficient',
            'common_config',
            'factorial_policy',
            'paircheck_policy',
            'replay_v2',
            'class KalshiExecutionAdapter',
            'portfolio',
            'urllib',
            'requests',
            'api.kalshi',
            'nfl_factorial_lab',
            'nfl_paircheck_lab',
        ):
            self.assertNotIn(banned, source)
        self.assertFalse(hasattr(fee_cost, 'KalshiExecutionAdapter'))

    def test_freeze_and_empty_results_stay_null(self):
        frozen = json.loads(fee_cost.FROZEN_EXPERIMENT.read_text())
        empty = json.loads(fee_cost.EMPTY_RESULTS.read_text())
        for key in fee_cost.OUTPUT_KEYS:
            self.assertIsNone(frozen[key])
            self.assertIsNone(empty[key])
            self.assertIsNone(fee_cost.frozen_output_snapshot()[key])
            self.assertIsNone(fee_cost.empty_outputs()[key])
        self.assertEqual(empty['status'], 'EMPTY')
        self.assertEqual(frozen['packet_id'], fee_cost.PACKET_ID)
        self.assertIs(frozen['q6_000_retune'], False)
        self.assertIs(frozen['signal_retune'], False)
        self.assertIs(frozen['live_orders'], False)
        self.assertIs(frozen['forbid_invented_pnl'], True)
        self.assertIs(frozen['forbid_naked_q7_fee_literals'], True)
        self.assertIs(frozen['not_a_strategy'], True)
        digest = hashlib.sha256((ROOT / 'EXPERIMENT_SPEC.md').read_bytes()).hexdigest()
        self.assertEqual(digest, frozen['specification_sha256']['EXPERIMENT_SPEC.md'])
        pins = hashlib.sha256((ROOT / 'SOURCE_PINS.json').read_bytes()).hexdigest()
        self.assertEqual(pins, frozen['specification_sha256']['SOURCE_PINS.json'])
        empty_digest = hashlib.sha256(fee_cost.EMPTY_RESULTS.read_bytes()).hexdigest()
        self.assertEqual(empty_digest, frozen['specification_sha256']['results/EMPTY_RESULTS.json'])
        self.assertIsInstance(frozen['implementation_sha256'], dict)
        for name in (
            'README.md',
            'fee_cost.py',
            'tests/__init__.py',
            'tests/test_fee_cost.py',
            'fixtures/synthetic_fills.json',
        ):
            self.assertEqual(
                hashlib.sha256((ROOT / name).read_bytes()).hexdigest(),
                frozen['implementation_sha256'][name],
            )

    def test_live_orders_are_refused(self):
        with self.assertRaises(fee_cost.LiveOrdersForbidden):
            fee_cost.execution_adapter()


class JoinTests(unittest.TestCase):
    def setUp(self):
        self.scored = fee_cost.score_fixture()
        self.rows = _by_case(self.scored)

    def test_fixture_covers_match_mismatch_null_and_both_roles(self):
        self.assertEqual(
            set(self.rows),
            {
                'venue_match_taker',
                'venue_mismatch_taker',
                'venue_mismatch_subcent_taker',
                'venue_match_maker',
                'venue_mismatch_maker',
                'venue_null_taker',
                'venue_null_maker',
                'venue_match_taker_c100',
                'venue_mismatch_maker_c1000',
            },
        )
        roles = {row['role'] for row in self.rows.values()}
        self.assertEqual(roles, {'taker', 'maker'})
        self.assertTrue(any(row['fee_cost'] is None for row in self.rows.values()))
        self.assertTrue(any(row['fee_cost'] is not None for row in self.rows.values()))

    def test_fee_model_is_the_imported_order_fee(self):
        table = feebook.load_series_table()
        default_m = feebook.as_decimal(table['default']['M'], 'M')
        for row in self.rows.values():
            quote = feebook.order_fee(
                row['role'], row['contracts'], row['price'], round_up=True,
            )
            self.assertEqual(row['formula_id'], feebook.EXAMINER_FORMULA_ID)
            self.assertEqual(row['fee_model'], quote['fee'])
            self.assertEqual(row['fee_model'], feebook.round_up_to_cent(row['raw']))
            self.assertEqual(row['M'], default_m)
            self.assertEqual(
                row['raw'],
                row['M'] * row['rate'] * row['contracts'] * row['price'] * (feebook.ONE - row['price']),
            )
            self.assertIsNone(row['results'])
            self.assertIsNone(row['pnl'])
            self.assertIsInstance(row['fee_model'], Decimal)

    def test_side_price_is_the_filled_side(self):
        maker = self.rows['venue_match_maker']
        self.assertEqual(maker['side'], 'no')
        self.assertEqual(maker['price'], Decimal('0.6000'))
        self.assertNotEqual(maker['price'], Decimal('0.4000'))
        taker = self.rows['venue_match_taker']
        self.assertEqual(taker['side'], 'yes')
        self.assertEqual(taker['price'], Decimal('0.5000'))

    def test_hand_vector_ceilings_match_the_feebook_pin(self):
        vectors = json.loads((FEEBOOK / 'fee_fixture_vectors.json').read_text())

        def ceiling(role, price, contracts):
            for vector in vectors['vectors']:
                if (
                    vector['role'] == role
                    and Decimal(str(vector['P'])) == price
                    and Decimal(str(vector['C'])) == contracts
                ):
                    return Decimal(str(vector['ceil_cent']))
            self.fail('vector missing')

        taker = self.rows['venue_match_taker']
        self.assertEqual(
            taker['fee_model'],
            ceiling('taker', taker['price'], taker['contracts']),
        )
        wide = self.rows['venue_match_taker_c100']
        self.assertEqual(
            wide['fee_model'],
            ceiling('taker', wide['price'], wide['contracts']),
        )
        maker = self.rows['venue_mismatch_maker_c1000']
        self.assertEqual(
            maker['fee_model'],
            ceiling('maker', maker['price'], maker['contracts']),
        )

    def test_delta_is_model_minus_venue_on_decimal(self):
        matched = self.rows['venue_match_taker']
        self.assertEqual(matched['fee_model_minus_venue_delta'], Decimal('0'))
        self.assertEqual(matched['preferred_fee_source'], 'venue')
        self.assertEqual(matched['preferred_fee'], matched['fee_cost'])
        self.assertIs(matched['is_taker'], True)

        mismatch = self.rows['venue_mismatch_taker']
        self.assertEqual(
            mismatch['fee_model_minus_venue_delta'],
            mismatch['fee_model'] - mismatch['fee_cost'],
        )
        self.assertEqual(mismatch['fee_model_minus_venue_delta'], Decimal('-0.01'))
        self.assertNotEqual(mismatch['fee_model'], mismatch['fee_cost'])

        subcent = self.rows['venue_mismatch_subcent_taker']
        delta = subcent['fee_model_minus_venue_delta']
        self.assertEqual(delta, subcent['fee_model'] - subcent['fee_cost'])
        self.assertIsInstance(delta, Decimal)
        cents = delta * 100
        self.assertNotEqual(cents, cents.to_integral_value())

        zero_venue = self.rows['venue_mismatch_maker']
        self.assertEqual(zero_venue['fee_cost'], Decimal('0'))
        self.assertIsNotNone(zero_venue['fee_cost'])
        self.assertEqual(zero_venue['preferred_fee_source'], 'venue')
        self.assertGreater(zero_venue['fee_model_minus_venue_delta'], Decimal('0'))
        self.assertIs(zero_venue['is_taker'], False)

        self.assertNotEqual(
            self.rows['venue_match_taker']['fee_model'],
            self.rows['venue_mismatch_maker']['fee_model'],
        )

    def test_null_venue_fee_is_not_a_zero_delta(self):
        for case_id in ('venue_null_taker', 'venue_null_maker'):
            row = self.rows[case_id]
            self.assertIsNone(row['fee_cost'])
            self.assertIsNone(row['fee_model_minus_venue_delta'])
            self.assertEqual(row['preferred_fee_source'], 'model_only')
            self.assertEqual(row['preferred_fee'], row['fee_model'])
            self.assertIs(row['projection_only'], True)
            self.assertIsNotNone(row['fee_model'])

    def test_aggregate_skips_null_venue_rows_and_is_not_profit(self):
        manual = Decimal('0')
        seen = 0
        for row in self.scored['rows']:
            if row['fee_cost'] is None:
                self.assertIsNone(row['fee_model_minus_venue_delta'])
                continue
            manual += row['fee_model'] - row['fee_cost']
            seen += 1
        self.assertGreater(seen, 0)
        self.assertEqual(self.scored['fee_model_minus_venue_delta'], manual)
        self.assertEqual(self.scored['rows_with_venue_fee'], seen)
        self.assertEqual(self.scored['rows_model_only'], 2)
        self.assertIsNone(self.scored['results'])
        self.assertIsNone(self.scored['pnl'])
        self.assertEqual(self.scored['status'], 'SYNTHETIC_FIXTURE_ONLY')
        before = fee_cost.FROZEN_EXPERIMENT.read_bytes()
        again = fee_cost.score_fixture()
        self.assertEqual(again['fee_model_minus_venue_delta'], manual)
        self.assertEqual(fee_cost.FROZEN_EXPERIMENT.read_bytes(), before)
        self.assertIsNone(fee_cost.frozen_output_snapshot()['pnl'])

    def test_float_and_missing_fields_are_rejected(self):
        good = dict(fee_cost.load_fills()['fills'][0])
        floated = dict(good)
        floated['fee_cost'] = 0.02
        with self.assertRaises(TypeError):
            fee_cost.join_fill(floated)
        missing = dict(good)
        del missing['fee_cost']
        with self.assertRaises(fee_cost.FeeCostError):
            fee_cost.join_fill(missing)
        flag = dict(good)
        flag['is_taker'] = 'true'
        with self.assertRaises(TypeError):
            fee_cost.join_fill(flag)
        crossed = dict(good)
        crossed['no_price_dollars'] = '0.4000'
        with self.assertRaises(fee_cost.FeeCostError):
            fee_cost.join_fill(crossed)
        negative = dict(good)
        negative['fee_cost'] = '-0.01'
        with self.assertRaises(ValueError):
            fee_cost.join_fill(negative)
        disagree = dict(good)
        disagree['count'] = '2.00'
        with self.assertRaises(fee_cost.FeeCostError):
            fee_cost.join_fill(disagree)


class RefuseTests(unittest.TestCase):
    def setUp(self):
        self.rows = _by_case()

    def _other(self, row):
        return fee_cost.other_role_quote(row)

    def test_model_only_completed_net_is_refused_when_fee_cost_is_present(self):
        row = self.rows['venue_mismatch_taker']
        other = self._other(row)
        channel = fee_cost.examiner_channel(row, other)
        model_label = feebook.classify_scorecard({
            'kind': 'execution',
            'inventory_flat': True,
            'fee_channel': channel,
        })
        self.assertEqual(model_label, 'completed_profit')
        with self.assertRaises(fee_cost.CompletedNetRefused) as caught:
            fee_cost.claim_completed_net(
                row, fee_basis='model', other_role_quote=other,
            )
        self.assertIn('fee_cost was available', str(caught.exception))
        zero = self.rows['venue_mismatch_maker']
        with self.assertRaises(fee_cost.CompletedNetRefused):
            fee_cost.claim_completed_net(
                zero, fee_basis='model', other_role_quote=self._other(zero),
            )

    def test_null_fee_cost_allows_projection_and_refuses_completed_net(self):
        row = self.rows['venue_null_taker']
        other = self._other(row)
        projected = fee_cost.claim_completed_net(
            row,
            fee_basis='model',
            other_role_quote=other,
            kind='extrapolation',
        )
        self.assertEqual(projected['label'], 'projection')
        self.assertEqual(projected['projection_fee'], row['fee_model'])
        self.assertEqual(projected['preferred_fee_source'], 'model_only')
        self.assertIsNone(projected['pnl'])
        self.assertIsNone(projected['results'])
        self.assertIsNone(projected['fee_model_minus_venue_delta'])
        with self.assertRaises(fee_cost.CompletedNetRefused) as caught:
            fee_cost.claim_completed_net(
                row, fee_basis='model', other_role_quote=other, kind='execution',
            )
        self.assertIn('projection', str(caught.exception))
        maker = self.rows['venue_null_maker']
        with self.assertRaises(fee_cost.CompletedNetRefused):
            fee_cost.claim_completed_net(
                maker,
                fee_basis='venue',
                other_role_quote=self._other(maker),
                kind='execution',
            )

    def test_reported_fee_still_allows_a_model_projection(self):
        row = self.rows['venue_mismatch_subcent_taker']
        projected = fee_cost.claim_completed_net(
            row,
            fee_basis='model',
            other_role_quote=self._other(row),
            kind='extrapolation',
        )
        self.assertEqual(projected['label'], 'projection')
        self.assertEqual(projected['projection_fee'], row['fee_model'])
        self.assertEqual(projected['preferred_fee_source'], 'venue')
        self.assertEqual(projected['preferred_fee'], row['fee_cost'])
        self.assertNotEqual(projected['projection_fee'], projected['preferred_fee'])
        self.assertIsNone(projected['pnl'])

    def test_venue_basis_binds_fee_cost_and_does_not_invent_pnl(self):
        row = self.rows['venue_mismatch_taker']
        bound = fee_cost.claim_completed_net(
            row, fee_basis='venue', other_role_quote=self._other(row),
        )
        self.assertEqual(bound['label'], 'venue_fee_bound')
        self.assertEqual(bound['model_label'], 'completed_profit')
        self.assertEqual(bound['accounting_fee'], row['fee_cost'])
        self.assertNotEqual(bound['accounting_fee'], bound['fee_model'])
        self.assertEqual(
            bound['fee_model_minus_venue_delta'],
            row['fee_model'] - row['fee_cost'],
        )
        self.assertIsNone(bound['results'])
        self.assertIsNone(bound['pnl'])
        self.assertNotIn('net', bound)
        self.assertNotIn('completed_net', bound)
        matched = self.rows['venue_match_maker']
        same = fee_cost.claim_completed_net(
            matched, fee_basis='venue', other_role_quote=self._other(matched),
        )
        self.assertEqual(same['accounting_fee'], matched['fee_cost'])
        self.assertEqual(same['fee_model_minus_venue_delta'], Decimal('0'))
        self.assertIsNone(same['pnl'])

    def test_non_examiner_counterpart_and_open_inventory_still_refuse(self):
        row = self.rows['venue_match_taker']
        grok = feebook.grok_unrounded_maker_per_unit(row['price'])
        with self.assertRaises(feebook.CompletedProfitRefused):
            fee_cost.claim_completed_net(
                row, fee_basis='venue', other_role_quote=grok,
            )
        with self.assertRaises(feebook.CompletedProfitRefused):
            fee_cost.claim_completed_net(
                row,
                fee_basis='venue',
                other_role_quote=self._other(row),
                inventory_flat=False,
            )


if __name__ == '__main__':
    unittest.main()
