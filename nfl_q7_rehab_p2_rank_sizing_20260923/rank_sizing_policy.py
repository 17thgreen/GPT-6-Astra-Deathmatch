"""Q7 Arm B rehab, pass 2. Parent Q6 and Q7 modules are imported and not modified.

B0 is Q7 Arm B. D is Q7 Arm D. B2 adds only portfolio-rank capital-budget sizing.
The Pass-1 admission cadence stays closed.
"""
import hashlib
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent / 'nfl_paircheck_lab_20260922'
Q6_ROOT = ROOT.parent / 'nfl_factorial_lab_20260921'
FEEBOOK_ROOT = ROOT.parent / 'kalshi_feebook_lab_20260922'
PASS1_ROOT = ROOT.parent / 'nfl_q7_rehab_p1_cadence_20260923'
PACKETS = ROOT.parent / 'packets' / 'refiner'
for _path in (PARENT, Q6_ROOT, FEEBOOK_ROOT):
    if str(_path) not in sys.path:
        sys.path.append(str(_path))

from adaptive_policy import AdaptiveReplay, floor_qty
from factorial_policy import FactorialReplay, Factors
from paircheck_policy import (AllocatorPairCheck, OriginalPairCheck, combined_cost_margin)

ARMS = ('B0', 'B2', 'D')
Q6_000 = Factors(False, False, False)
SOURCE_PINS = PACKETS / 'PARENT_Q7_BD_LEDGER_SOURCE_PINS_2026-09-23.json'


class InventedPnlRefused(RuntimeError):
    """A freeze or not-run document tried to carry a profit."""


def entry_budget_fraction(allocation, total):
    """Imported allocation expression: min(1, budget/total), or 0 when total is 0."""
    if total == 0:
        return 0.0
    if allocation < 0 or total < 0:
        raise ValueError('allocation fraction')
    return min(1.0, allocation / total)


def sized_quantity(wanted, allocation, total):
    """floor_qty(wanted * fraction). Offset protection stays in the imported refresh."""
    return floor_qty(wanted * entry_budget_fraction(allocation, total))


class RankSizingReplay(OriginalPairCheck):
    """Arm B2. Original router, pair check on, continuous admission, rank sizing."""

    architecture = 'original_router'

    def __init__(self, markets, config):
        super().__init__(markets, config, True)
        if self.experiment != 'baseline':
            raise RuntimeError('B2 stays on the original baseline router')
        if self.pair_check is not True:
            raise RuntimeError('B2 keeps the pair check on')
        self.factors = Q6_000
        if self.factors.label != '000' or self.factors.flow or self.factors.protection or self.factors.ranking:
            raise RuntimeError('B2 rank semantics are Q6 000')
        self.arm = 'B2'
        self.portfolio_rank_sizing = True
        self.admission_cadence_seconds = None
        self.pass1_admission_gate = False

    def portfolio_rank(self, candidates, now):
        if self.factors != Q6_000:
            raise RuntimeError('B2 refuses an F/P/R retune')
        return FactorialReplay.portfolio_rank(self, candidates, now)

    def rebalance(self, now):
        """Imported 000 budget math on this refresh. The 600s admit clock stays disarmed."""
        if self.admission_cadence_seconds is not None or self.pass1_admission_gate:
            raise RuntimeError('B2 refuses the Pass-1 admission cadence gate')
        self.next_allocation = -math.inf
        FactorialReplay.rebalance(self, now)
        self.next_allocation = -math.inf

    def refresh(self, event, now):
        if self.admission_cadence_seconds is not None or self.pass1_admission_gate:
            raise RuntimeError('B2 refuses the Pass-1 admission cadence gate')
        self.experiment = 'allocation'
        try:
            return OriginalPairCheck.refresh(self, event, now)
        finally:
            self.experiment = 'baseline'

    def finish(self, end):
        result = super().finish(end)
        result['portfolio_rank_sizing'] = True
        result['sizing_branch'] = 'allocation'
        result['admission_cadence_seconds'] = None
        result['pass1_admission_gate'] = False
        result['q6_rank_factor_label'] = self.factors.label
        return result


def make_replay(markets, config, arm):
    if arm == 'B0':
        replay = OriginalPairCheck(markets, config, True)
        replay.arm = 'B0'
        replay.positive_control = 'Q7_ARM_B'
        replay.portfolio_rank_sizing = False
        replay.admission_cadence_seconds = None
        return replay
    if arm == 'B1':
        raise ValueError('Pass-1 admission_cadence is closed; B2 does not reopen it')
    if arm == 'B2':
        return RankSizingReplay(markets, config)
    if arm == 'D':
        replay = AllocatorPairCheck(markets, config, True)
        if replay.factors.label != '000' or replay.pair_check is not True or replay.arm != 'D':
            raise RuntimeError('D drifted from Q7 Arm D / Q6 000')
        replay.positive_control = 'Q7_ARM_D'
        replay.portfolio_rank_sizing = False
        return replay
    raise ValueError('Unknown arm')


def refuse_completed_profit_without_fee_channel(scorecard):
    """Imported feebook gate. A missing fee channel is not completed profit."""
    from feebook import classify_scorecard
    return classify_scorecard(scorecard)


def refuse_invented_pnl(document):
    if not isinstance(document, dict):
        raise InventedPnlRefused('document')
    if document.get('results') is not None or document.get('pnl') is not None:
        raise InventedPnlRefused('results and pnl stay null')
    if document.get('completed_strategy_pnl') is not None:
        raise InventedPnlRefused('completed_strategy_pnl')
    return document


def assert_freeze_null(frozen):
    if not isinstance(frozen, dict):
        raise InventedPnlRefused('freeze')
    if frozen.get('results') is not None or frozen.get('pnl') is not None:
        raise InventedPnlRefused('freeze results and pnl stay null')
    if frozen.get('score_run_in_this_freeze') is not False:
        raise InventedPnlRefused('score run is not part of this freeze')
    if frozen.get('status') not in ('HYPOTHESIS_FROZEN_NOT_RUN', 'IMPLEMENTED_FROZEN_NOT_RUN'):
        raise InventedPnlRefused('freeze status')
    if frozen.get('selection_rule', {}).get('live_promotion') is not False:
        raise InventedPnlRefused('live promotion')
    if frozen.get('one_knob') != 'portfolio_rank_sizing':
        raise InventedPnlRefused('one knob')
    if frozen.get('selection_rule', {}).get('require_B2_beats_B0_all_stresses') is not True:
        raise InventedPnlRefused('B2>B0 bar')
    if frozen.get('selection_rule', {}).get('require_D_positive_and_B2_at_least_95pct_of_D') is not True:
        raise InventedPnlRefused('95 percent of D')
    return frozen


def load_frozen():
    return json.loads((ROOT / 'FROZEN_EXPERIMENT.json').read_text())


def _sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parent_pin_mismatches():
    frozen = load_frozen()
    bad = []
    for name, digest in frozen['parent_q7_sha256'].items():
        path = PARENT / name
        if not path.exists() or _sha256(path) != digest:
            bad.append('q7:' + name)
    q6_freeze = Q6_ROOT / 'SHADOW_CANDIDATE_FREEZE.json'
    if not q6_freeze.exists() or _sha256(q6_freeze) != frozen['q6_000_freeze_sha256']:
        bad.append('SHADOW_CANDIDATE_FREEZE.json')
    for name, digest in frozen['q6_behavior_sha256'].items():
        path = Q6_ROOT / name
        if not path.exists() or _sha256(path) != digest:
            bad.append('q6:' + name)
    feebook = FEEBOOK_ROOT / 'feebook.py'
    if not feebook.exists() or _sha256(feebook) != frozen['feebook_sha256']:
        bad.append('feebook.py')
    for name, digest in frozen.get('pass1_dead_knob_sha256', {}).items():
        path = ROOT.parent / name
        if not path.exists() or _sha256(path) != digest:
            bad.append('pass1:' + name)
    spec = _sha256(ROOT / 'EXPERIMENT_SPEC.md')
    if spec != frozen['spec_sha256']:
        bad.append('EXPERIMENT_SPEC.md')
    pins = frozen.get('implementation_sha256')
    if pins:
        for name, digest in pins.items():
            path = ROOT / name
            if not path.exists() or _sha256(path) != digest:
                bad.append(name)
    packets = frozen.get('conductor_packets', {})
    for key, digest in packets.get('sha256', {}).items():
        rel = packets.get(key)
        if not rel or _sha256(ROOT.parent / rel) != digest:
            bad.append('packet:' + key)
    if not SOURCE_PINS.exists() or _sha256(SOURCE_PINS) != packets.get('sha256', {}).get('parent_ledger_source_pins'):
        bad.append('SOURCE_PINS')
    selected = json.loads(q6_freeze.read_text()).get('selected') if q6_freeze.exists() else None
    if selected != '000':
        bad.append('q6_selected_label')
    return bad
