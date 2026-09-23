"""How B0 and D must match Q7 Arm B and Arm D where those ledgers exist.

Missing parent result bytes are not a match and are not a pass. This module
does not invent ledger hashes. B2 has no parent ledger.
"""
import json
from pathlib import Path

from rank_sizing_policy import PARENT, SOURCE_PINS, parent_pin_mismatches

COMPARE_FIELDS = ('completed_strategy_pnl', 'all_flat', 'unresolved_contracts', 'week_contributions',
                  'unhedged_contract_hours', 'taker_contracts', 'maker_contracts', 'fills',
                  'pnl_excluding_top_two_games')
LEDGER_SUFFIXES = ('fills', 'orders', 'decisions')
STRESSES = ((3300, 0.25), (3300, 5), (10000, 0.25), (10000, 5))
ARM_MAP = {'B0': 'B', 'D': 'D'}


def parent_scenario_name(queue, delay, parent_arm):
    return f'q{queue}_d{delay:g}_{parent_arm}'


def expected_parent_paths():
    paths = []
    for queue, delay in STRESSES:
        for parent_arm in ('B', 'D'):
            name = parent_scenario_name(queue, delay, parent_arm)
            paths.append(PARENT / 'results' / f'{name}.json')
            for suffix in LEDGER_SUFFIXES:
                paths.append(PARENT / 'results' / f'{name}_{suffix}.jsonl.gz')
    return paths


def load_source_pins():
    """Read the conductor manifest. Do not synthesize artifact bytes or hashes."""
    if not SOURCE_PINS.exists():
        return dict(path=str(SOURCE_PINS.relative_to(SOURCE_PINS.parents[2])), present=False,
                    invented_hashes=False, artifacts={})
    payload = json.loads(SOURCE_PINS.read_text())
    return dict(path='packets/refiner/PARENT_Q7_BD_LEDGER_SOURCE_PINS_2026-09-23.json', present=True,
                waive=payload.get('waive'), artifacts=payload.get('artifacts', {}),
                paircheck_effects=payload.get('paircheck_effects.json'), invented_hashes=False)


def parent_ledger_status():
    missing = []
    present = []
    for path in expected_parent_paths():
        (present if path.exists() else missing).append(str(path.relative_to(PARENT.parent)))
    return dict(parent_ledgers_in_checkout=not missing and bool(present),
                missing=missing, present=present, absence_is_not_a_pass=True,
                invented_hashes=False, source_pins=load_source_pins()['path'])


def evaluate_positive_controls():
    """Pin check plus ledger presence. No produced rehab ledger is hashed here."""
    pins = parent_pin_mismatches()
    if pins:
        return dict(status='PIN_MISMATCH', all_checks_passed=False, scenarios_executed=0,
                    pnl=None, results=None, mismatches=pins, invented_hashes=False)
    ledgers = parent_ledger_status()
    if ledgers['missing']:
        return dict(status='PARENT_LEDGERS_ABSENT', all_checks_passed=None, scenarios_executed=0,
                    pnl=None, results=None, missing=ledgers['missing'], present=ledgers['present'],
                    compare_fields=list(COMPARE_FIELDS), compare_ledgers=list(LEDGER_SUFFIXES),
                    arm_map=ARM_MAP, invented_hashes=False, source_pins=ledgers['source_pins'],
                    note='Q7 Arm B and Arm D ledgers are absent. Absence is not a match and is not a pass.')
    return dict(status='PARENT_LEDGERS_PRESENT_UNCOMPARED', all_checks_passed=False,
                scenarios_executed=0, pnl=None, results=None, invented_hashes=False,
                note='Parent bytes exist. This freeze does not score or hash a rehab run against them.')


def comparison_contract():
    frozen = json.loads((Path(__file__).resolve().parent / 'FROZEN_EXPERIMENT.json').read_text())
    return dict(fields=list(COMPARE_FIELDS), ledgers=list(LEDGER_SUFFIXES),
                arm_map=dict(ARM_MAP), excluded=[],
                parent_ledgers_in_checkout=frozen['positive_controls']['parent_ledgers_in_checkout'],
                mismatch_is=frozen['positive_controls']['mismatch_is'],
                source_pins=frozen['positive_controls']['source_pins'])
