import hashlib,json
from dataclasses import replace
from concurrent.futures import ProcessPoolExecutor,as_completed
from run_queue_suite import ROOT,load_capture,load_quotes,Config,Policy,run_one

def main():
    (ROOT/'results/queue_stress_spec_sha256.txt').write_text(hashlib.sha256((ROOT/'QUEUE_STRESS_SPEC.md').read_bytes()).hexdigest()+'\n')
    rows,markets,_=load_capture();quotes,_=load_quotes();events=rows+quotes
    events.sort(key=lambda r:(r['at'],0 if r.get('kind')=='quote' else 1,r.get('trade_id',r['ticker'])))
    base=replace(Config(),quote_source='candles',liquidation_lead_seconds=300)
    output={}
    with ProcessPoolExecutor(max_workers=2) as pool:
        jobs=[pool.submit(run_one,label+'_'+p,replace(base,queue_early=q),Policy(name=p),events,markets,quotes)
              for label,q in [('q10000',10000),('q100000',100000)] for p in ['preserve','route']]
        for job in as_completed(jobs):
            s=job.result();s['diagnostic']='POST_RESULT_HYPOTHETICAL_LARGER_QUEUE_STRESS'
            output[s['scenario']]=s
            print(s['scenario'],s['completed_strategy_pnl'],flush=True)
    (ROOT/'results/queue_stress_summary.json').write_text(json.dumps(output,indent=2,allow_nan=False))

if __name__=='__main__':main()
