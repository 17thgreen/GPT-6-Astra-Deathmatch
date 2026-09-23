"""Q7 Arm B rehab. Parent Q7 and Q6 modules are imported and not modified.

B0 is Q7 Arm B. D is Q7 Arm D. B1 adds only the 600s entry-budget cadence.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent / 'nfl_paircheck_lab_20260922'
Q6_ROOT = ROOT.parent / 'nfl_factorial_lab_20260921'
FEEBOOK_ROOT = ROOT.parent / 'kalshi_feebook_lab_20260922'
for _path in (PARENT, Q6_ROOT, FEEBOOK_ROOT):
    if str(_path) not in sys.path:
        sys.path.append(str(_path))

from adaptive_policy import AdaptiveReplay
from paircheck_policy import (AllocatorPairCheck, OriginalPairCheck, combined_cost_margin,
                              split_offset)
from queue_policies import QueueReplay

ADMISSION_CADENCE_SECONDS = 600
ARMS = ('B0', 'B1', 'D')


class InventedPnlRefused(RuntimeError):
    """A freeze or not-run document tried to carry a profit."""


class RehabCadenceReplay(OriginalPairCheck):
    """Arm B1. Original router, pair check on, 600s new-exposure cadence."""

    architecture = 'original_router'

    def __init__(self, markets, config):
        super().__init__(markets, config, True)
        if self.experiment != 'baseline':
            raise RuntimeError('B1 stays on the original baseline router')
        if self.pair_check is not True:
            raise RuntimeError('B1 keeps the pair check on')
        self.arm = 'B1'
        self.admission_cadence_seconds = ADMISSION_CADENCE_SECONDS
        self.cadence_blocks = []
        self.admit_attempts = []

    def _new_exposure_keys(self, candidates, inventory):
        chosen = QueueReplay.choose(self, candidates)
        legs = [c for c in candidates if c['key'] in chosen]
        if len(legs) != 2:
            return set()
        _offsets, new_legs = split_offset(legs, inventory)
        return {c['key'] for c in new_legs}

    def _record_block(self, event, now, keys):
        self.cadence_blocks.append(dict(
            kind='cadence_block', at=now, event=event, reason='admission_cadence',
            admission_cadence_seconds=ADMISSION_CADENCE_SECONDS,
            next_allocation=self.next_allocation,
            blocked_new_exposure_keys=[[key[0], key[1]] for key in sorted(keys)],
            counted_as_pnl=False, cancelled_instantly=False, used_future_quotes=False))

    def _gated_refresh(self, event, now, extra):
        """Parent admission, plus keys the closed cadence must not submit."""
        blocked, rejection = self.plan_admission(self.route_candidates(event, now),
                                                 self.holdings[event], now, event)
        if rejection:
            self.pair_rejections.append(rejection)
        blocked = set(blocked) | set(extra)
        original = AdaptiveReplay.quote

        def gated(ticker, outcome, price, wanted, now, _blocked=frozenset(blocked)):
            if (ticker, outcome) in _blocked and self.orders.get((ticker, outcome)) is None:
                return
            return original(self, ticker, outcome, price, wanted, now)

        self.quote = gated
        try:
            return AdaptiveReplay.refresh(self, event, now)
        finally:
            del self.quote

    def refresh(self, event, now):
        candidates = self.route_candidates(event, now)
        new_keys = self._new_exposure_keys(candidates, self.holdings[event])
        if not new_keys:
            return super().refresh(event, now)
        if now >= self.next_allocation:
            self.next_allocation = now + ADMISSION_CADENCE_SECONDS
            self.admit_attempts.append(dict(
                kind='admit_attempt', at=now, event=event,
                next_allocation=self.next_allocation, counted_as_pnl=False))
            return super().refresh(event, now)
        missing = {key for key in new_keys if self.orders.get(key) is None}
        if missing:
            self._record_block(event, now, missing)
        return self._gated_refresh(event, now, new_keys)

    def finish(self, end):
        result = super().finish(end)
        result['admission_cadence_seconds'] = ADMISSION_CADENCE_SECONDS
        result['cadence_block_count'] = len(self.cadence_blocks)
        result['cadence_blocks'] = self.cadence_blocks
        result['cadence_blocks_counted_as_pnl'] = False
        result['admit_attempt_count'] = len(self.admit_attempts)
        return result


def make_replay(markets, config, arm):
    if arm == 'B0':
        replay = OriginalPairCheck(markets, config, True)
        replay.arm = 'B0'
        replay.positive_control = 'Q7_ARM_B'
        return replay
    if arm == 'B1':
        return RehabCadenceReplay(markets, config)
    if arm == 'D':
        replay = AllocatorPairCheck(markets, config, True)
        if replay.factors.label != '000' or replay.pair_check is not True or replay.arm != 'D':
            raise RuntimeError('D drifted from Q7 Arm D / Q6 000')
        replay.positive_control = 'Q7_ARM_D'
        return replay
    raise ValueError('Unknown arm')


def refuse_completed_profit_without_fee_channel(scorecard):
    """Imported feebook gate. A missing fee channel is not completed profit."""
    from feebook import classify_scorecard
    return classify_scorecard(scorecard)


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
    spec = _sha256(ROOT / 'EXPERIMENT_SPEC.md')
    if spec != frozen['spec_sha256']:
        bad.append('EXPERIMENT_SPEC.md')
    pins = frozen.get('implementation_sha256')
    if pins:
        for name, digest in pins.items():
            path = ROOT / name
            if not path.exists() or _sha256(path) != digest:
                bad.append(name)
    selected = json.loads(q6_freeze.read_text()).get('selected') if q6_freeze.exists() else None
    if selected != '000':
        bad.append('q6_selected_label')
    return bad
