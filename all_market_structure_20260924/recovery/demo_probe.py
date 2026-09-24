"""Bounded demo market-data probe. Credentials supplied as JSON on stdin."""
import asyncio,base64,json,sys,time,urllib.request,urllib.error
from pathlib import Path
from collections import Counter
import websockets
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
ROOT=Path(__file__).resolve().parent
FIELDS={'market_ticker','yes_dollars_fp','no_dollars_fp','yes_dollars','no_dollars','price_dollars','delta_fp','side','ts','ts_ms','yes_price_dollars','no_price_dollars','count_fp','taker_side','channel'}
def public_message(data):
    msg=data.get('msg',{})
    return {**{k:data[k] for k in ('type','sid','seq','id') if k in data},'msg':{k:v for k,v in msg.items() if k in FIELDS}}
async def main():
    out=ROOT/'demo_result.json'
    if out.exists():raise SystemExit('existing probe; refusing overwrite')
    credential=json.load(sys.stdin)
    key=load_pem_private_key(credential['private_key'].encode(),password=None)
    if not isinstance(key,Ed25519PrivateKey):raise ValueError('expected Ed25519')
    result={'environment':'demo','orders_placed':0,'attempts':[],'selected':[],'pnl':None}
    def save():out.write_text(json.dumps(result,indent=2)+'\n')
    save()
    for base in ['https://external-api.demo.kalshi.co','https://demo-api.kalshi.co']:
        try:
            with urllib.request.urlopen(base+'/trade-api/v2/markets?status=open&limit=100',timeout=12) as r:
                markets=json.load(r)['markets']
            result['selected']=sorted(m['ticker'] for m in markets)[:3]
            result['selection_host']=base;save();break
        except Exception as e:result['attempts'].append({'stage':'selection','host':base,'error_type':type(e).__name__});save()
    if not result['selected']:return
    for host in ['external-api-ws.demo.kalshi.co','demo-api.kalshi.co']:
        attempt={'host':host,'connected':False,'message_counts':{}}
        result['attempts'].append(attempt);save()
        ts=str(time.time_ns()//1000000)
        headers={'KALSHI-ACCESS-KEY':credential['key_id'],'KALSHI-ACCESS-TIMESTAMP':ts,'KALSHI-ACCESS-SIGNATURE':base64.b64encode(key.sign((ts+'GET/trade-api/ws/v2').encode())).decode()}
        try:
            async with websockets.connect('wss://'+host+'/trade-api/ws/v2',additional_headers=headers,open_timeout=12,close_timeout=2) as ws:
                attempt['connected']=True;attempt['connected_ns']=time.time_ns();save()
                for ident,channel in enumerate(['orderbook_delta','trade'],1):
                    await ws.send(json.dumps({'id':ident,'cmd':'subscribe','params':{'channels':[channel],'market_tickers':result['selected']}}))
                deadline=time.monotonic()+30;counts=Counter()
                with (ROOT/'demo_messages.jsonl').open('a') as f:
                    while sum(counts.values())<500:
                        left=deadline-time.monotonic()
                        if left<=0:break
                        try:raw=await asyncio.wait_for(ws.recv(),timeout=left)
                        except asyncio.TimeoutError:break
                        now=time.time_ns();mono=time.monotonic_ns();data=json.loads(raw)
                        counts[data.get('type','missing')]+=1
                        f.write(json.dumps({'received_ns':now,'monotonic_ns':mono,'message':public_message(data)})+'\n');f.flush()
                        attempt['message_counts']=dict(counts);save()
                attempt['finished_ns']=time.time_ns();save()
                break
        except Exception as e:
            attempt['error_type']=type(e).__name__
            response=getattr(e,'response',None)
            if response is not None:attempt['http_status']=getattr(response,'status_code',None)
            save()
            if attempt['connected']:break
    print(json.dumps(result))
if __name__=='__main__':asyncio.run(main())
