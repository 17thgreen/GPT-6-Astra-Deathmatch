from decimal import Decimal
def dec(x):
    if isinstance(x,bool):raise ValueError('boolean')
    v=Decimal(str(x))
    if not v.is_finite():raise ValueError('nonfinite')
    return v
def walk(rows,q,buy):
    q=dec(q)
    if q<=0:raise ValueError('quantity')
    levels=[]
    for row in rows:
        p,n=map(dec,row[:2])
        if p<=0 or n<0:raise ValueError('invalid level')
        levels.append((p,n))
    left=q;value=Decimal(0)
    for p,n in sorted(levels,reverse=not buy):
        used=min(left,n);value+=used*p;left-=used
        if left==0:break
    return {'complete':left==0,'quantity':q,'missing':left,'value':value}
def basis(perp,spot,size,multiplier,q=10):
    if spot.get('auction_mode'):return {'status':'AUCTION_REJECTED'}
    units=dec(size)*dec(multiplier)*dec(q)
    if units<=0:raise ValueError('units')
    out={'underlying_units':units,'directions':{}}
    for direction,p_buy in [('buy_perp_sell_spot',True),('sell_perp_buy_spot',False)]:
        p=walk(perp['orderbook']['asks' if p_buy else 'bids'],q,p_buy)
        s=walk(spot['bids' if p_buy else 'asks'],units,not p_buy)
        row={'perp':p,'spot':s,'complete':p['complete'] and s['complete']}
        if row['complete']:
            gross=s['value']-p['value'] if p_buy else p['value']-s['value']
            budget=gross/s['value']*10000
            row.update(entry_basis_dollars=gross,entry_basis_bps=budget,entry_fee_sensitivity_bps={str(c):budget-c for c in [0,5,10,25,50]})
        out['directions'][direction]=row
    out['status']='ENTRY_BASIS_ONLY'
    return out
def side_depth(rows,target):
    target=dec(target)
    if target<=0:raise ValueError('target')
    levels=[]
    for p,n in rows:
        p,n=dec(p),dec(n)
        if not 0<=p<=1 or n<0:raise ValueError('event level')
        levels.append((p,n))
    levels.sort(reverse=True);total=sum((q for _,q in levels),Decimal(0));cum=Decimal(0);ref=None
    for p,n in levels:
        cum+=n
        if cum>=target/5:ref=p;break
    return {'total_depth':total,'target_met':total>=target,'target_deficit':max(Decimal(0),target-total),'reference_price':ref}
def volume_bound(p):
    p=dec(p)
    if not Decimal('.03')<=p<=Decimal('.97'):return None
    fee=Decimal('.07')*p*(1-p)
    return {'raw_fee':fee,'max_reward':Decimal('.005'),'reward_minus_fee':Decimal('.005')-fee}
