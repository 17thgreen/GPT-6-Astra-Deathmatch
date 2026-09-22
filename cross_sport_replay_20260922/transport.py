"""M2 listing gate; all Q7 strategy, fee and portfolio accounting stays imported."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'nfl_pair_price_lab_20260921'))
from pair_policy import GuardedRouter
from replay_v2 import Config


class ListingRouter(GuardedRouter):
    def eligible(self, ticker, now):
        return now >= self.markets[ticker]['listed_at'] and super().eligible(ticker, now)
