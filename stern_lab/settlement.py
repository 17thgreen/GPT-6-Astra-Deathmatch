"""Explicit contract-payoff conversion. Does not estimate tie probability."""
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class PayoutBounds:
    lower: float
    upper: float


def _prob(value):
    if not math.isfinite(value) or not 0 <= value <= 1:
        raise ValueError("Probability/payout must be finite and in [0,1]")
    return float(value)


def _interval(bounds):
    if len(bounds) != 2:
        raise ValueError("Interval requires two endpoints")
    lo, hi = map(_prob, bounds)
    if lo > hi:
        raise ValueError("Reversed probability interval")
    return lo, hi


def expected_payout(*, home_win, away_win, tie, side, tie_payout):
    """Use a full outcome distribution and the exact selected contract's tie payoff.

    Outcomes refer to final settlement, including overtime when the contract includes it.
    A tie is never silently converted into an away victory. For a $1 binary team-winner
    contract, the selected team wins $1 and loses $0; only tie payout is rule-dependent.
    """
    h, a, t, tie_pay = map(_prob, [home_win, away_win, tie, tie_payout])
    if not math.isclose(h+a+t, 1., rel_tol=0., abs_tol=1e-9):
        raise ValueError("Outcome probabilities must sum to one")
    if side not in ["home", "away"]:
        raise ValueError("Side must be home or away")
    return (h if side == "home" else a) + t*tie_pay


def payout_bounds(*, conditional_home_win_bounds, tie_probability_bounds, side, tie_payout):
    """Conservative payoff range for supplied uncertainty/tie probability intervals.

    q=P(home wins | game does not tie), t=P(game ties). Payout is (1-t)q+t*tie_payout
    for the home contract and (1-t)(1-q)+t*tie_payout for the away contract. Extremes
    over the rectangular input set occur at its corners. Correlated or tighter input
    information could narrow this set, but is not assumed. Inputs are not estimated
    by this function and intervals are not statistical confidence guarantees.
    """
    qs = _interval(conditional_home_win_bounds)
    ts = _interval(tie_probability_bounds)
    values = [expected_payout(home_win=(1-t)*q, away_win=(1-t)*(1-q), tie=t,
                             side=side, tie_payout=tie_payout) for q in qs for t in ts]
    return PayoutBounds(min(values), max(values))
