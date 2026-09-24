"""Conditional payoff screen, not an execution simulator."""
from decimal import Decimal,ROUND_CEILING
def dec(x):
    if isinstance(x,bool):raise ValueError('boolean')
    v=Decimal(str(x))
    if not v.is_finite():raise ValueError('nonfinite')
    return v
def purchase(book,side,quantity,multiplier):
    q=dec(quantity);m=dec(multiplier)
    if q<=0 or m<0:raise ValueError('quantity/multiplier')
    opposite='no_dollars' if side=='yes' else 'yes_dollars' if side=='no' else None
    if opposite is None:raise ValueError('side')
    rows=book['orderbook_fp'].get(opposite)
    if rows is None:return {'complete':False,'reason':'missing_side'}
    levels={}
    for p,n in rows:
        p,n=dec(p),dec(n)
        if not 0<=p<=1 or n<0:raise ValueError('invalid_level')
        price=1-p;levels[price]=levels.get(price,Decimal(0))+n
    cost=Decimal(0);fee=Decimal(0);fee_cent=Decimal(0);remaining=q;consumed=[]
    for price,size in sorted(levels.items()):
        take=min(remaining,size)
        if not take:continue
        raw=Decimal('.07')*m*take*price*(1-price)
        cost+=take*price;fee+=raw;fee_cent+=raw.quantize(Decimal('.01'),rounding=ROUND_CEILING)
        consumed.append({'price':str(price),'quantity':str(take)})
        remaining-=take
        if not remaining:break
    return {'complete':remaining==0,'quantity':q,'cost':cost,'raw_fee':fee,'cent_fee':fee_cent,'consumed':consumed,'missing':remaining}
def pair(low_book,high_book,strike_type,quantity,multiplier):
    if strike_type in ('greater','greater_or_equal'):yes,no=low_book,high_book
    elif strike_type in ('less','less_or_equal'):yes,no=high_book,low_book
    else:raise ValueError('comparator')
    a=purchase(yes,'yes',quantity,multiplier);b=purchase(no,'no',quantity,multiplier)
    result={'yes_leg':a,'no_leg':b,'complete':a['complete'] and b['complete']}
    if result['complete']:
        gross=dec(quantity)-a['cost']-b['cost']
        result.update(gross=gross,net_raw_fee=gross-a['raw_fee']-b['raw_fee'],net_cent_fee=gross-a['cent_fee']-b['cent_fee'])
    return result
