"""Pure payoff compatibility checks. No market admission or order API.

State vectors must come from reviewed settlement rules, including postponement,
void, tie and retirement states. The checker cannot prove state exhaustiveness.
"""
from decimal import Decimal,InvalidOperation
from dataclasses import dataclass
from itertools import combinations


def vector(values,states):
    if set(values)!=set(states):raise ValueError('Every declared settlement state is required')
    try:out=tuple(Decimal(str(values[s])) for s in states)
    except InvalidOperation as e:raise ValueError('Invalid payout') from e
    if any(not v.is_finite() or not 0<=v<=1 for v in out):raise ValueError('Payout outside [0,1]')
    return out


def classify_routes(routes,states,*,state_space_reviewed=False):
    if not state_space_reviewed:raise ValueError('Unreviewed settlement state space')
    if len(states)<2 or len(set(states))!=len(states):raise ValueError('Invalid state labels')
    if len(routes)<2:raise ValueError('At least two routes required')
    vectors={key:vector(payouts,states) for key,payouts in routes.items()}
    equivalents=[];complements=[]
    for a,b in combinations(sorted(vectors),2):
        if vectors[a]==vectors[b]:equivalents.append([a,b])
        if all(x+y==1 for x,y in zip(vectors[a],vectors[b])):complements.append([a,b])
    anchor=vectors[sorted(vectors)[0]]
    opposite=tuple(1-v for v in anchor)
    binary=all(v in (0,1) for values in vectors.values() for v in values)
    nonconstant=len(set(anchor))==2
    two_direction=binary and nonconstant and all(v in (anchor,opposite) for v in vectors.values()) and opposite in vectors.values()
    return dict(equivalent_routes=equivalents,complementary_pairs=complements,
                current_two_direction_kernel_compatible=two_direction,
                directions={k:1 if v==anchor else -1 for k,v in vectors.items()} if two_direction else None,
                limitation='Algebra only; does not establish exhaustive states, immediate netting, executable prices or profitability.')


@dataclass(frozen=True)
class ResearchProfile:
    """Explicit transport requirements; no NFL defaults silently inherited."""
    series: str
    entry_lead_seconds: float
    stop_lead_seconds: float
    winddown_seconds: float
    flow_window_seconds: float
    quote_max_age_seconds: float
    maker_coefficient: float
    taker_coefficient: float
    tick_size: str
    event_cap: float
    exit_depth: float
    collateral_model: str

    def validate(self):
        numeric=[self.entry_lead_seconds,self.stop_lead_seconds,self.winddown_seconds,
                 self.flow_window_seconds,self.quote_max_age_seconds,self.maker_coefficient,
                 self.taker_coefficient,self.event_cap,self.exit_depth]
        import math
        if any(not math.isfinite(x) or x<0 for x in numeric):raise ValueError('Nonfinite or negative setting')
        if not self.series or self.entry_lead_seconds<=self.stop_lead_seconds:raise ValueError('Invalid entry window')
        if min(self.winddown_seconds,self.flow_window_seconds,self.quote_max_age_seconds,self.event_cap,self.exit_depth)<=0:raise ValueError('Positive mechanics settings required')
        tick=Decimal(self.tick_size)
        if not tick.is_finite() or not 0<tick<1:raise ValueError('Invalid tick')
        if self.collateral_model not in ('same_market_netting','reviewed_cross_market_netting','no_immediate_netting'):
            raise ValueError('Explicit collateral model required')
        return self
