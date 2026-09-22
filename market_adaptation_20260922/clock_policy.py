"""Adapt boundary timestamps around the immutable Q7 kernel."""
import copy
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'cross_sport_replay_20260922'))
from transport import ListingRouter, Config


class ClockRouter(ListingRouter):
    def __init__(self, markets, config, cutoff_minutes=180, queue_profile='nfl'):
        if cutoff_minutes not in (180, 30) or queue_profile not in ('nfl', 'constant'):
            raise ValueError('Unfrozen M3 profile')
        self.cutoff_minutes, self.queue_profile = cutoff_minutes, queue_profile
        adjusted = copy.deepcopy(markets)
        for m in adjusted.values():
            m['actual_start'] = m['kickoff']
            m['actual_cutoff'] = m['actual_start'] - cutoff_minutes*60
            # Internal reference clock, explicitly NOT a replacement real schedule.
            m['kickoff'] = m['actual_cutoff'] + 10800
        super().__init__(adjusted, config)

    def queue(self, ticker, now):
        if self.queue_profile == 'constant':
            return self.cfg.queue_early
        return self.cfg.queue_last12h if self.markets[ticker]['actual_start']-now < 43200 else self.cfg.queue_early

    def eligible(self, ticker, now):
        m = self.markets[ticker]
        return (max(m['listed_at'], m['actual_start']-604800) <= now
            and now+self.cfg.order_delay_seconds < m['actual_cutoff']-self.cfg.liquidation_lead_seconds-self.cfg.cancel_delay_seconds
            and self.event(ticker) not in self.closed and self.book_valid(ticker, now))

    def entry_open(self, event, now):
        m = self.markets[self.groups[event][0]]
        return (m['actual_start']-604800 <= now and now+self.cfg.order_delay_seconds
            < m['actual_cutoff']-self.cfg.liquidation_lead_seconds-self.cfg.cancel_delay_seconds)

    def candidate(self, ticker, outcome, now):
        c = super().candidate(ticker, outcome, now)
        if c is None or (self.cutoff_minutes == 180 and self.queue_profile == 'nfl'):
            return c
        # QueueReplay.candidate calls Replay.queue directly. Correct that observer
        # to the same physical queue used when the order is submitted.
        old = self.orders.get(c['key'])
        incumbent = old and old.cancel_at is None and abs(old.price-c['price']) < 1e-9
        c['queue'] = old.queue if incumbent else self.queue(ticker, now)
        c['service'] = min(1, c['rate']*self.policy.service_horizon /
                           (c['queue']+c['wanted']/self.cfg.fill_participation))
        return c
