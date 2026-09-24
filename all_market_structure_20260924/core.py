"""Pure research measurements; no network or execution operations."""
from decimal import Decimal

def number(v):
    if isinstance(v, bool): raise ValueError('boolean')
    x=Decimal(str(v))
    if not x.is_finite(): raise ValueError('nonfinite')
    return x

def best(rows):
    levels=[]
    for p,q in rows:
        p,q=number(p),number(q)
        if not 0 <= p <= 1 or q < 0: raise ValueError('invalid event level')
        if q: levels.append((p,q))
    if not levels: return None,None
    p=max(x[0] for x in levels)
    return p,sum(q for px,q in levels if px==p)

def event_top(body):
    book=body.get('orderbook_fp')
    if not isinstance(book,dict): raise ValueError('fixed-point event book absent')
    y,yq=best(book.get('yes_dollars') or [])
    n,nq=best(book.get('no_dollars') or [])
    return dict(yes_bid=str(y) if y is not None else None,
                yes_ask=str(1-n) if n is not None else None,
                yes_bid_size=str(yq) if yq is not None else None,
                yes_ask_size=str(nq) if nq is not None else None,
                two_sided=y is not None and n is not None)

def walk_asks(levels, quantity):
    """Depth cost only, not a fill guarantee. Does not mutate the observed book."""
    q=number(quantity)
    if q<=0: raise ValueError('quantity')
    remaining=q; cost=Decimal(0)
    checked=[]
    for p,n in levels:
        p,n=number(p),number(n)
        if p<0 or n<0: raise ValueError('negative level')
        checked.append((p,n))
    for p,n in sorted(checked):
        used=min(n,remaining);cost+=p*used;remaining-=used
        if not remaining: break
    return dict(quantity=q,filled=q-remaining,cost=cost,complete=remaining==0)

def guaranteed_edge(payoff_floor, costs, fees, quantity):
    """Only for a separately verified payoff proof; all legs must be complete."""
    q=number(quantity); floor=number(payoff_floor); f=number(fees)
    if q<=0 or floor<0 or f<0 or not costs: raise ValueError('invalid inputs')
    if any(not c['complete'] or c['filled']!=q for c in costs):return None
    return floor*q-sum(c['cost'] for c in costs)-f
