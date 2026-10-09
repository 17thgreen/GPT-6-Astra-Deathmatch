"""KD-13. Pure Decimal cost. The study never calls this. No rate literal is stored here."""

from decimal import Decimal, ROUND_CEILING

from .constants import FEE_ADMISSION, FEE_BLOCK_REASON, FUTURE_NET_LABEL
from .errors import FloatDecimalRefused

_MICRO = Decimal("0.000001")
_CENT = Decimal("0.01")


def _as_decimal(value):
    if isinstance(value, float) or isinstance(value, bool):
        raise FloatDecimalRefused(type(value).__name__)
    if isinstance(value, Decimal):
        return value
    if isinstance(value, str):
        return Decimal(value)
    raise FloatDecimalRefused(type(value).__name__)


def _ceil_to(amount, quantum):
    return (amount / quantum).to_integral_value(rounding=ROUND_CEILING) * quantum


def cost_hl(price, contracts, *, M, rate):
    """ceil_cent(P*C + fee_raw) - P*C. fee_raw ceils M*rate*C*P*(1-P) to 1e-6.

    price, contracts, M, and rate must be str or Decimal.
    """
    price_d = _as_decimal(price)
    contracts_d = _as_decimal(contracts)
    multiplier = _as_decimal(M)
    rate_d = _as_decimal(rate)
    raw = multiplier * rate_d * contracts_d * price_d * (Decimal(1) - price_d)
    fee_raw = _ceil_to(raw, _MICRO)
    notional = price_d * contracts_d
    return _ceil_to(notional + fee_raw, _CENT) - notional


def admission():
    return {
        "fee_admission": FEE_ADMISSION,
        "fee_block_reason": FEE_BLOCK_REASON,
        "future_net_label": FUTURE_NET_LABEL,
        "examiner_pin_account_class": None,
        "omitted_sensitivities": ["FEE_ONLY_CEIL", "DIRECT_MEMBER"],
        "sensitivity_status": "SENSITIVITY_BASIS_INCOMPLETE",
    }
