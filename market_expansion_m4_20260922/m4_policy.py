"""Separate size/completion experiment; imported Q7/M3 implementations unchanged."""
import sys
from m4_common import M3
sys.path.insert(0, str(M3))
from clock_policy import ClockRouter, Config


class SizeRouter(ClockRouter):
    def __init__(self, markets, config, complete_first=False):
        if type(complete_first) is not bool:
            raise ValueError('Boolean policy required')
        self.complete_first = complete_first
        super().__init__(markets, config, 30, 'constant')

    def choose(self, candidates):
        chosen = super().choose(candidates)
        if not self.complete_first or not candidates:
            return chosen
        event = self.event(candidates[0]['key'][0])
        inventory = self.holdings[event]
        if abs(inventory) < .01:
            return chosen
        allowed = set()
        for candidate in candidates:
            if candidate['key'] not in chosen:
                continue
            if candidate['direction']*inventory >= 0:
                self.metrics['complete_first_exposure_blocks'] += 1
                continue
            quantity, _ = self.bounded_quantity(candidate, 0)
            if quantity >= .01:
                candidate['wanted'] = quantity
                allowed.add(candidate['key'])
        return allowed

    def match(self, row):
        before = len(self.fills)
        super().match(row)
        if self.complete_first and len(self.fills) > before:
            self.refresh(self.event(row['ticker']), row['at'])
