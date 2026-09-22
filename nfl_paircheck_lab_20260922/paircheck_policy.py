"""Q7 chosen-pair admission. Frozen Q6 modules are imported and not modified."""
import hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
Q6_ROOT = ROOT.parent / 'nfl_factorial_lab_20260921'
if str(Q6_ROOT) not in sys.path:
    sys.path.append(str(Q6_ROOT))

from adaptive_policy import AdaptiveReplay
from factorial_policy import FactorialReplay, Factors
from queue_policies import QueueReplay

ARMS = ('A', 'B', 'C', 'D')
Q6_FACTORS = Factors(False, False, False)
REJECTION_REASON = 'combined_acquisition_cost'


def combined_cost_margin(costs, quantity, balance_precision):
    """Inherited Q6 cushion on the two routes actually chosen."""
    if len(costs) != 2:
        raise ValueError('combined-cost check requires two chosen routes')
    if quantity <= 0:
        raise ValueError('quantity')
    return 1 - sum(costs) - .0002 - 2 * float(balance_precision) / quantity


def _leg_row(candidate):
    ticker, outcome = candidate['key']
    return dict(ticker=ticker, outcome=outcome, direction=candidate['direction'],
                cost=candidate['cost'], price=candidate['price'])


def _keys(candidates):
    return [[c['key'][0], c['key'][1]] for c in candidates]


def rejection_record(event, now, legs, margin, offset_legs, blocked_legs):
    return dict(kind='pair_rejection', at=now, event=event, reason=REJECTION_REASON,
                legs=[_leg_row(c) for c in legs], margin=margin,
                hypothetical_unit_margin=margin, counted_as_pnl=False,
                admitted_offset_keys=_keys(offset_legs),
                blocked_new_exposure_keys=_keys(blocked_legs),
                assumed_simultaneous_fills=False, used_future_quotes=False,
                cancelled_instantly=False)


def split_offset(legs, inventory):
    offsets = [c for c in legs if c['direction'] * inventory < 0]
    blocked = [c for c in legs if c['key'] not in {c['key'] for c in offsets}]
    return offsets, blocked


class OriginalPairCheck(AdaptiveReplay):
    """Baseline router. The check only withholds new paired exposure."""

    architecture = 'original_router'

    def __init__(self, markets, config, pair_check):
        if type(pair_check) is not bool:
            raise ValueError('pair_check must be bool')
        self.pair_check = pair_check
        self.pair_rejections = []
        super().__init__(markets, config, 'baseline')
        self.arm = 'B' if pair_check else 'A'

    def route_candidates(self, event, now):
        found = []
        for ticker in sorted(self.groups[event]):
            for outcome in ('yes', 'no'):
                candidate = self.candidate(ticker, outcome, now)
                if candidate:
                    found.append(candidate)
        return found

    def plan_admission(self, candidates, inventory, now, event):
        """Decide from the supplied candidates only. Does not read later quotes."""
        if not self.pair_check:
            return set(), None
        chosen = QueueReplay.choose(self, candidates)
        legs = [c for c in candidates if c['key'] in chosen]
        if len(legs) != 2:
            return set(), None
        margin = combined_cost_margin([c['cost'] for c in legs], self.cfg.order_size,
                                       self.cfg.balance_precision)
        if margin > 0:
            return set(), None
        offsets, blocked = split_offset(legs, inventory)
        return {c['key'] for c in blocked}, rejection_record(event, now, legs, margin, offsets, blocked)

    def refresh(self, event, now):
        if not self.pair_check:
            return super().refresh(event, now)
        blocked, rejection = self.plan_admission(self.route_candidates(event, now),
                                                 self.holdings[event], now, event)
        if rejection:
            self.pair_rejections.append(rejection)
        if not blocked:
            return super().refresh(event, now)
        original = AdaptiveReplay.quote

        def gated(ticker, outcome, price, wanted, now, _blocked=frozenset(blocked)):
            # A working order keeps the inherited delayed cancel/replace path.
            # No working order means this submit is new exposure and is skipped.
            if (ticker, outcome) in _blocked and self.orders.get((ticker, outcome)) is None:
                return
            return original(self, ticker, outcome, price, wanted, now)

        self.quote = gated
        try:
            return super().refresh(event, now)
        finally:
            del self.quote

    def finish(self, end):
        result = super().finish(end)
        return attach_arm(result, self)


class AllocatorPairCheck(FactorialReplay):
    """Q6 label 000. pair_check False removes only the combined-cost veto."""

    architecture = 'q6_allocator_000'

    def __init__(self, markets, config, pair_check):
        if type(pair_check) is not bool:
            raise ValueError('pair_check must be bool')
        self.pair_check = pair_check
        self.pair_rejections = []
        super().__init__(markets, config, Q6_FACTORS)
        if self.factors.label != '000':
            raise RuntimeError('Q7 allocator is frozen to label 000')
        self.arm = 'D' if pair_check else 'C'

    def portfolio_rank(self, candidates, now):
        if self.pair_check:
            rank = super().portfolio_rank(candidates, now)
            if rank is None:
                self._record_cost_rejection(candidates, now)
            return rank
        return self._rank_without_combined_cost_filter(candidates, now)

    def _record_cost_rejection(self, candidates, now):
        chosen = QueueReplay.choose(self, candidates)
        legs = [c for c in candidates if c['key'] in chosen]
        if len(legs) != 2 or (self.factors.flow and not all(c['rate'] > 0 for c in legs)):
            return
        margin = combined_cost_margin([c['cost'] for c in legs], self.cfg.order_size,
                                       self.cfg.balance_precision)
        if margin > 0:
            return
        event = self.event(legs[0]['key'][0])
        offsets, blocked = split_offset(legs, self.holdings[event])
        self.pair_rejections.append(rejection_record(event, now, legs, margin, offsets, blocked))

    def _rank_without_combined_cost_filter(self, candidates, now):
        chosen = self.choose(candidates)
        legs = [c for c in candidates if c['key'] in chosen]
        if len(legs) != 2:
            return None
        has_flow = all(c['rate'] > 0 for c in legs)
        if self.factors.flow and not has_flow:
            return None
        quantity = self.cfg.order_size
        margin = combined_cost_margin([c['cost'] for c in legs], quantity, self.cfg.balance_precision)
        capital = sum(quantity * (c['cost'] + .0001) + float(self.cfg.balance_precision) for c in legs)
        incumbent = any(c['key'] in self.orders and self.orders[c['key']].cancel_at is None for c in legs)
        if has_flow:
            wait = max((c['queue'] + quantity / self.cfg.fill_participation) / c['rate'] for c in legs)
            score = quantity * margin / (capital * max(wait / 3600, 1 / 60))
            reset_wait = max((self.queue(c['key'][0], now) + quantity / self.cfg.fill_participation) / c['rate']
                             for c in legs)
            lost = max(0, reset_wait - wait)
        else:
            wait = None
            score = 0.
            lost = None
        adjusted = score * (1.25 if incumbent else 1) if self.factors.ranking else 1.
        return dict(score=score, adjusted=adjusted, capital=capital, wait_seconds=wait,
                    lost_queue_wait_seconds=lost, incumbent=incumbent, has_observed_flow=has_flow)

    def finish(self, end):
        return attach_arm(super().finish(end), self)


def attach_arm(result, replay):
    result['arm'] = replay.arm
    result['architecture'] = replay.architecture
    result['pair_check'] = replay.pair_check
    result['q6_factor_label'] = replay.factors.label if replay.architecture == 'q6_allocator_000' else None
    result['pair_rejections'] = replay.pair_rejections
    result['pair_rejection_count'] = len(replay.pair_rejections)
    result['rejected_hypothetical_margins_are_not_pnl'] = True
    return result


def make_replay(markets, config, arm):
    if arm not in ARMS:
        raise ValueError('Unknown arm')
    if arm in ('A', 'B'):
        return OriginalPairCheck(markets, config, arm == 'B')
    return AllocatorPairCheck(markets, config, arm == 'D')


def q6_pin_mismatches():
    frozen = json.loads((ROOT / 'FROZEN_EXPERIMENT.json').read_text())
    bad = []
    for name, digest in frozen['q6_dependency_sha256'].items():
        path = Q6_ROOT / name
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            bad.append(name)
    if frozen['q6_selected_label'] != '000':
        bad.append('q6_selected_label')
    return bad


def implementation_pin_mismatches():
    frozen = json.loads((ROOT / 'FROZEN_EXPERIMENT.json').read_text())
    pins = frozen.get('implementation_sha256')
    if not pins:
        return ['implementation_sha256']
    bad = []
    for name, digest in pins.items():
        path = ROOT / name
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            bad.append(name)
    spec = hashlib.sha256((ROOT / 'EXPERIMENT_SPEC.md').read_bytes()).hexdigest()
    if spec != frozen['spec_sha256']:
        bad.append('EXPERIMENT_SPEC.md')
    return bad
