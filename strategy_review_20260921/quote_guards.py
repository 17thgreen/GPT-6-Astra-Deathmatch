"""Research-only admission and worst-case reservation primitives. No orders sent."""
from dataclasses import dataclass, replace
import math


def in_quote_window(*, now_seconds, kickoff_seconds):
    if not all(math.isfinite(v) for v in [now_seconds,kickoff_seconds]):
        raise ValueError('Finite UTC timestamps required')
    remaining=kickoff_seconds-now_seconds
    return 3*3600 < remaining <= 7*86400


def quote_admission(*, now_seconds, kickoff_seconds, bid, ask, book_received_seconds,
                    max_book_age_seconds, sequence_valid):
    """Call on a wall-clock timer and before simulated matching, not only on trade arrival.

    CANCEL_AND_BLOCK is an instruction to the caller, not an exchange acknowledgment. Existing orders
    must remain reserved until cancellation is acknowledged. This primitive does not send cancels.
    Bid/ask must be from an actual, sequenced book; trade prints do not qualify as book updates.
    The freshness threshold is supplied by the caller and must be frozen before evaluation.
    """
    if not math.isfinite(max_book_age_seconds) or max_book_age_seconds <= 0:
        raise ValueError('Positive finite freshness threshold required')
    reasons=[]
    if not in_quote_window(now_seconds=now_seconds,kickoff_seconds=kickoff_seconds):
        reasons.append('OUTSIDE_QUOTE_WINDOW')
    if not all(math.isfinite(x) for x in [bid,ask,book_received_seconds]):
        reasons.append('INVALID_BOOK')
    else:
        if not 0 < bid < ask < 1:reasons.append('INVALID_BOOK')
        age=now_seconds-book_received_seconds
        if age < 0 or age > max_book_age_seconds:reasons.append('STALE_OR_FUTURE_BOOK')
    if not sequence_valid:reasons.append('BOOK_SEQUENCE_GAP')
    return {'action':'CANCEL_AND_BLOCK' if reasons else 'ELIGIBLE_FOR_RISK_CHECK', 'reasons':reasons}


@dataclass(frozen=True)
class Candidate:
    key: str
    # Only after verifying settlement payoff equivalence, including ties/cancellations:
    home_payoff_direction: int  # +1: home YES or away NO; -1: home NO or away YES
    size: float
    price: float
    fee_per_contract: float


def _validate(order):
    if order.home_payoff_direction not in (-1,1):raise ValueError('Invalid payoff direction')
    if not all(math.isfinite(x) for x in [order.size,order.price,order.fee_per_contract]):raise ValueError('Nonfinite order')
    if order.size<0 or not 0<order.price<1 or order.fee_per_contract<0:raise ValueError('Invalid order')


def reserve_candidates(candidates, *, current_home_exposure, resting, free_cash, exposure_cap):
    """Allocate all game legs jointly, reserving pending orders until cancellation is acknowledged.

    Caller supplies proposals in its desired priority order and only orders for this game. Never credit
    an unfilled hedge against another unfilled order. Existing orders in `resting` remain obligations.
    free_cash is cash before reservations listed here; already reserved unrelated-event cash must have
    been deducted by the caller. Full purchase cost is reserved, conservatively ignoring cross-market
    collateral offsets. Prices/fees must come from verified book/fee data, not this primitive. The
    caller must verify the two payoff directions, including tie/cancel rules, and round accepted
    quantities DOWN to the permitted quantity increment; this is not a generalized multi-outcome model.
    """
    if not all(math.isfinite(x) for x in [current_home_exposure,free_cash,exposure_cap]):raise ValueError('Nonfinite risk input')
    if free_cash<0 or exposure_cap<=0:raise ValueError('Invalid budget')
    resting,candidates=list(resting),list(candidates)
    for order in resting+candidates:_validate(order)
    keys=[o.key for o in resting+candidates]
    if len(keys)!=len(set(keys)):raise ValueError('Duplicate order key; process cancel/replace explicitly')
    low=current_home_exposure-sum(o.size for o in resting if o.home_payoff_direction==-1)
    high=current_home_exposure+sum(o.size for o in resting if o.home_payoff_direction==1)
    cash=free_cash-sum(o.size*(o.price+o.fee_per_contract) for o in resting)
    if low < -exposure_cap-1e-9 or high > exposure_cap+1e-9 or cash < -1e-9:
        return [],{'status':'EXISTING_OBLIGATIONS_EXCEED_LIMITS','exposure_low':low,'exposure_high':high,'unreserved_cash':cash}
    admitted=[]
    for order in candidates:
        room=exposure_cap-high if order.home_payoff_direction==1 else low+exposure_cap
        quantity=max(0.,min(order.size,room,cash/(order.price+order.fee_per_contract)))
        if quantity<=1e-9:continue
        accepted=replace(order,size=quantity);admitted.append(accepted)
        cash-=quantity*(order.price+order.fee_per_contract)
        if order.home_payoff_direction==1:high+=quantity
        else:low-=quantity
    return admitted,{'status':'RESEARCH_ONLY','exposure_low':low,'exposure_high':high,'unreserved_cash':cash}


def conservative_remaining_size(*, old_remaining, requested_size):
    """Same-price downsizing can preserve remaining queue; upsizing needs a separate new order."""
    if not all(math.isfinite(x) and x>=0 for x in [old_remaining,requested_size]):raise ValueError('Invalid size')
    return min(old_remaining,requested_size)


def marginal_pair_value(*, completion_probability, paired_profit, forced_exit_loss):
    """Expected value per initially filled leg under an explicitly supplied two-scenario model.

    paired_profit and forced_exit_loss include both-leg costs, fees and delay assumptions. This does
    not fit completion probability or assert that only these two scenarios describe real fills.
    """
    if not all(math.isfinite(x) for x in [completion_probability,paired_profit,forced_exit_loss]):raise ValueError('Nonfinite value')
    if not 0<=completion_probability<=1 or paired_profit<0 or forced_exit_loss<0:raise ValueError('Invalid value')
    value=completion_probability*paired_profit-(1-completion_probability)*forced_exit_loss
    total=paired_profit+forced_exit_loss
    return {'expected_value':value,'break_even_completion':forced_exit_loss/total if total else None}
