import json,random,sys,time,math
sys.path.insert(0,'.')
import NH002H_AMENDMENT_B_national_miss as M
rng=random.Random(1)
rows=[]
for i in range(92):
    pm=rng.uniform(0.05,0.95); pe=min(max(pm+rng.gauss(0,0.08),0.01),0.99)
    y=1 if rng.random()<M.sig(M.logit(pm)-0.3) else 0
    rows.append({"race_id":f"R{i}","state":f"S{i%28}","mapping_status":"KXHOUSERACE" if i<58 else ("LEGACY" if i<88 else "UNRESOLVED"),"p_market":pm,"p_model":pe,"y":y})
st=M.stats([r for r in rows if r["mapping_status"]!="UNRESOLVED"])
for w,v in st.items(): assert abs(v["M_recentered"])<1e-9,(w,v)
print("recentered miss ~0: OK", {w:round(v["delta"],4) for w,v in st.items()})
# boundary
d,b=M.delta_mle([0.3,0.6],[1,1]); assert b and d==10.0; print("boundary flag OK")
json.dump({"rows":rows,"signals":[{"race_id":"R1","side":"D_YES","price":0.4,"fee":None},{"race_id":"R2","side":"D_NO","price":0.3,"fee":None}]},open('/tmp/synth_ab.json','w'))
t=time.time(); M.B_RESAMPLES=500; r=M.stats(rows[:88]); M.boot(rows[:88]); print("500 resamples sec",round(time.time()-t,2))
