import hashlib,json
from dataclasses import replace
from concurrent.futures import ProcessPoolExecutor,as_completed
from run_queue_suite import ROOT,load_capture,load_quotes,Config,Policy,run_one

def main():
    spec=ROOT/'POST_RESULT_DIAGNOSTICS.md'
    (ROOT/'results/mechanism_spec_sha256.txt').write_text(hashlib.sha256(spec.read_bytes()).hexdigest()+'\n')
    rows,markets,_=load_capture();quotes,_=load_quotes();events=rows+quotes
    events.sort(key=lambda r:(r['at'],0 if r.get('kind')=='quote' else 1,r.get('trade_id',r['ticker'])))
    base=replace(Config(),quote_source='candles',liquidation_lead_seconds=300)
    output={}
    with ProcessPoolExecutor(max_workers=2) as pool:
        jobs=[pool.submit(run_one,label+'_margin_only',replace(base,queue_early=q),
              Policy(name='route',use_flow=False),events,markets,quotes) for label,q in [('q291',290.595),('q3300',3300)]]
        for job in as_completed(jobs):
            s=job.result();s['diagnostic']='POST_RESULT_FLOW_SCORE_ABLATION'
            output[s['scenario']]=s
            print(s['scenario'],s['completed_strategy_pnl'],flush=True)
    (ROOT/'results/mechanism_summary.json').write_text(json.dumps(output,indent=2,allow_nan=False))

if __name__=='__main__':main()
