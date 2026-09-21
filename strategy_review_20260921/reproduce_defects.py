"""Synthetic reproductions against unchanged source. No claim about historical P&L impact."""
from pathlib import Path
import ast
from dataclasses import asdict
import json
import sys
import numpy as np
import pandas as pd

ROOT=Path(__file__).parent
sys.path.insert(0,str(ROOT/'repo/src'))
from flatstake.paper.account import Portfolio
from flatstake.paper.execution import SimulatedExecutionAdapter
from flatstake.paper.fees import FeeModel
from flatstake.paper.policy import MarketMakerPolicy,MarketState,PolicyConfig,QuoteIntent


def original_replay():
    # Execute the exact two replay function bodies. Skip unused DB/experiment-registry imports so the
    # reproduction needs only the pure source files. Original text is preserved in repo/ and hashed.
    tree=ast.parse((ROOT/'repo/src/flatstake/paper/replay.py').read_text())
    selected=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['_event_exposure','replay']]
    module=ast.Module(body=[ast.ImportFrom(module='__future__',names=[ast.alias(name='annotations')],level=0)]+selected,type_ignores=[])
    env=globals().copy()
    exec(compile(ast.fix_missing_locations(module),'unchanged_repo_replay_functions','exec'),env)
    return env['replay']


def evidence():
    ticker='KXNFLGAME-26SEP20TEST-A'
    cfg=PolicyConfig(order_size=100,max_event_exposure=250,flatten_seconds_before_close=10800,
                     quote_from_seconds_before_start=604800,max_size_book_fraction=None)
    kickoff=pd.Timestamp('2026-09-20T17:00:00Z');cutoff=kickoff-pd.Timedelta(hours=3)
    def trade(at,side,yes,size):
        return dict(ticker=ticker,created_time=pd.Timestamp(at),taker_side=side,yes_price=yes,no_price=1-yes,size=size)
    tape=pd.DataFrame([
        trade('2026-09-20T13:58:00Z','no',.49,1),
        trade('2026-09-20T13:58:01Z','yes',.50,1),
        trade('2026-09-20T13:59:02Z','yes',.50,1),
        trade('2026-09-20T14:00:00Z','no',.49,100)])
    r=original_replay()(tape,MarketMakerPolicy(cfg),queue_ahead=0,queue_model='front',
                        requote_seconds=60,close_times={ticker:kickoff},require_close_time=True)
    late=r['fills'][(r['fills'].kind=='maker')&(r['fills']['at']>=cutoff)]
    ad=SimulatedExecutionAdapter(queue_ahead_contracts=0,fill_participation=1)
    ad.replace_quotes([QuoteIntent(ticker,'yes',.49,100)])
    ad.replace_quotes([QuoteIntent(ticker,'yes',.49,5)])
    reduced=ad.resting()[0].size
    pol=MarketMakerPolicy(PolicyConfig(max_event_exposure=250,max_size_book_fraction=None))
    intents=pol.quotes(MarketState(ticker,.49,.50,1000,1000,24*3600),200,5000,event_exposure=200)
    increase=sum(i.size for i in intents if i.outcome=='yes')
    invalid=pd.DataFrame([
        trade('2026-09-20T10:00:00Z','no',.49,1),
        trade('2026-09-20T10:00:01Z','yes',.50,1),
        trade('2026-09-20T10:01:02Z','yes',.50,1),
        trade('2026-09-20T10:02:03Z','no',.60,1), # inferred bid exceeds stale ask; no valid state
        trade('2026-09-20T10:02:04Z','no',.49,100)])
    s=original_replay()(invalid,MarketMakerPolicy(cfg),queue_ahead=0,queue_model='front',
                        requote_seconds=60,close_times={ticker:kickoff},require_close_time=True)
    after_invalid=s['fills'][(s['fills'].kind=='maker')&(s['fills']['at']==pd.Timestamp('2026-09-20T10:02:04Z'))]
    return {'kind':'SYNTHETIC_COUNTEREXAMPLES_NOT_HISTORICAL_RETURNS',
            'late_fill':{'cutoff':str(cutoff),'maker_contracts_at_or_after_cutoff':float(late['size'].sum()),'fills':late.to_dict('records')},
            'same_price_downsize':{'old_size':100,'requested_size':5,'actual_resting_size':reduced},
            'event_cap':{'exposure_before':200,'configured_cap':250,'additional_risk_quote':increase,'possible_exposure_after_fill':200+increase},
            'invalid_book_retains_quote':{'maker_contracts_after_invalid_book':float(after_invalid['size'].sum())}}


if __name__=='__main__':
    out=evidence();(ROOT/'results').mkdir(exist_ok=True)
    (ROOT/'results/defect_reproductions.json').write_text(json.dumps(out,indent=2,default=str))
    print(json.dumps(out,indent=2,default=str))
