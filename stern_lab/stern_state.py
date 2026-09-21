"""Research-only Stern adaptation. No network calls or order placement.

Prediction domain: regulation, 0.05 <= remaining fraction <= 0.97, non-tied outcome.
The market transport is a hypothesis; it is NOT a fitted trading strategy.
"""
from __future__ import annotations
from dataclasses import dataclass
import math
import numpy as np
from scipy.special import ndtr, expit, logit

SIGMA = 13.7
FEATURES = ["margin", "pregame_strength", "possession", "field_progress",
            "field_progress_squared", "second_down", "third_down", "fourth_down",
            "yards_to_go", "late_possession", "late_timeout_difference"]


def remaining_diffusion_variance(r, sigma0=SIGMA, kappa=0.0):
    """Integral of sigma(u)^2 from elapsed time 1-r to 1, sigma(u)=sigma0*(1+kappa*u).

    Analytical utility only; not a fitted feature in the forecasting experiment.
    """
    if not all(math.isfinite(v) for v in [r, sigma0, kappa]):
        raise ValueError("Nonfinite diffusion parameter")
    if not 0 <= r <= 1 or sigma0 <= 0 or kappa < 0:
        raise ValueError("Invalid diffusion domain")
    a = 1 + kappa
    return sigma0**2 * (a*a*r - a*kappa*r*r + kappa*kappa*r**3/3)


def design(frame):
    required = ["r", "margin", "spread_line", "possession", "yardline_100", "down",
                "ydstogo", "home_timeouts_remaining", "away_timeouts_remaining"]
    if not np.isfinite(frame[required].to_numpy(dtype=float)).all():
        raise ValueError("Missing or nonfinite game state")
    r = frame.r.to_numpy(dtype=float)
    if ((r < .05) | (r > .97)).any():
        raise ValueError("State outside validated research domain; use a separate endgame model")
    possession = frame.possession.to_numpy(dtype=float)
    if not np.isin(possession, [-1, 1]).all():
        raise ValueError("Possession must be known: home=+1, away=-1")
    if not frame.down.isin([1, 2, 3, 4]).all():
        raise ValueError("Down must be in 1..4")
    if not frame.yardline_100.between(0, 100).all() or not frame.ydstogo.between(0, 100).all():
        raise ValueError("Invalid field position or yards-to-go")
    for name in ["home_timeouts_remaining", "away_timeouts_remaining"]:
        if not frame[name].between(0, 3).all():
            raise ValueError("Timeout count must be in 0..3")
    progress = (100. - frame.yardline_100.to_numpy(dtype=float)) / 100.
    sd = SIGMA * np.sqrt(r)
    return np.column_stack([
        frame.margin / sd,
        frame.spread_line * r / sd,
        possession / sd,
        possession * progress / sd,
        possession * progress**2 / sd,
        possession * (frame.down == 2) / sd,
        possession * (frame.down == 3) / sd,
        possession * (frame.down == 4) / sd,
        possession * np.log1p(frame.ydstogo) / np.log(21.) / sd,
        possession * (1. - r) / sd,
        (frame.home_timeouts_remaining - frame.away_timeouts_remaining) * (1. - r) / 3. / sd,
    ]).astype(float)


def stern_probability(frame):
    x = design(frame)
    return ndtr(x[:, 0] + x[:, 1])


def state_probability(frame, coefficients):
    beta = np.asarray(coefficients, dtype=float)
    if beta.shape != (len(FEATURES),) or not np.isfinite(beta).all() or (beta[:2] < 0).any():
        raise ValueError("Invalid fitted coefficient vector")
    return ndtr(design(frame) @ beta)


def anchored_update(anchor_probability, previous_model_probability, current_model_probability,
                    reliability=1.0):
    """Transport a pre-event market anchor by the model's change in log odds.

    Assumes the model's odds ratio is informative about the new event. This assumption
    needs prospective testing. The anchor must precede the event; it is not today's
    target quote. Inputs should refer to the exact same binary event/settlement rules.
    """
    values = [anchor_probability, previous_model_probability, current_model_probability]
    if not all(math.isfinite(x) and 0 < x < 1 for x in values):
        raise ValueError("Probabilities must be finite and strictly between zero and one")
    if not math.isfinite(reliability) or not 0 <= reliability <= 1:
        raise ValueError("Reliability must be in [0, 1]")
    return float(expit(logit(anchor_probability) + reliability * (
        logit(current_model_probability) - logit(previous_model_probability))))


@dataclass(frozen=True)
class ResearchEdge:
    eligible: bool
    reason: str
    net_edge_per_contract: float | None


def assess_buy(*, expected_payout, ask, quantity, total_fee, uncertainty_buffer,
               latency_buffer, state_received_ms, quote_received_ms, decision_ms,
               max_age_ms, settlement_verified=False, model_admitted=False,
               available_quantity=0):
    """A conservative research gate, not a fill simulator or trading actuator.

    Fees are supplied from a versioned schedule. Stale/future data and missing
    admission block a signal. Separate scenario gates are needed for portfolio risk.
    """
    values = [expected_payout, ask, quantity, total_fee, uncertainty_buffer, latency_buffer,
              state_received_ms, quote_received_ms, decision_ms, max_age_ms, available_quantity]
    if not all(math.isfinite(v) for v in values):
        raise ValueError("Nonfinite gate input")
    if not (0 <= expected_payout <= 1 and 0 < ask < 1 and quantity > 0):
        raise ValueError("Invalid payout, ask, or quantity")
    if min(total_fee, uncertainty_buffer, latency_buffer, max_age_ms, available_quantity) < 0:
        raise ValueError("Negative cost, buffer, age limit, or depth")
    if max(state_received_ms, quote_received_ms) > decision_ms:
        return ResearchEdge(False, "future_information", None)
    if decision_ms - min(state_received_ms, quote_received_ms) > max_age_ms:
        return ResearchEdge(False, "stale_information", None)
    if not settlement_verified:
        return ResearchEdge(False, "settlement_unverified", None)
    if not model_admitted:
        return ResearchEdge(False, "research_model_not_admitted", None)
    if available_quantity < quantity:
        return ResearchEdge(False, "insufficient_depth_at_ask", None)
    edge = expected_payout - ask - total_fee / quantity - uncertainty_buffer - latency_buffer
    return ResearchEdge(edge > 0, "positive_research_edge" if edge > 0 else "costs_exceed_edge", edge)
