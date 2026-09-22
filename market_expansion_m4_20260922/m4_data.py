"""Validate complete reserved cohorts without winner/price-based admission."""
import math
from m4_common import ROOT, read, sha, epoch, lines
from m4_capture import quote_schema
from normalize import normalize_trade, normalize_quote, covered_seconds


def load_new(series):
    cohort, capture = read(ROOT/'COHORT.json'), read(ROOT/'CAPTURE.json')
    if not cohort['sports'][series]['admitted'] or not capture['sports'][series]['complete']:
        raise ValueError('Incomplete reserved sport; no subset replay')
    games = [g for g in cohort['games'] if g['series']==series]
    if len(games)!=8 or {g['event'] for g in games}!=set(cohort['reserved'][series]):
        raise ValueError('Cohort membership changed')
    captures = [m for m in capture['markets'] if m['series']==series]
    expected = {t for g in games for t in g['tickers']}
    if len(captures)!=16 or {m['ticker'] for m in captures}!=expected:
        raise ValueError('Capture membership changed')
    indexes = {m['ticker']:m for m in captures}
    records, markets, coverage, seen = [], {}, [], set()
    for game in games:
        for market in sorted(game['markets'],key=lambda m:m['ticker']):
            ticker = market['ticker']
            manifest = indexes[ticker]
            folder = ROOT/'data'/ticker
            start = max(game['kickoff']-604800,epoch(market['open_time']))
            end = game['kickoff']-1500
            if read(folder/'manifest.json')!=manifest or not manifest['pagination_exhausted']:
                raise ValueError('Capture manifest mismatch')
            for key,value in dict(ticker=ticker,event=game['event'],series=series,
                                  kickoff=game['kickoff'],start=start,end=end).items():
                if manifest[key]!=value:
                    raise ValueError('Changed capture identity/window')
            if set(manifest['sha256'])!={'trades.jsonl.gz','candles.jsonl.gz'}:
                raise ValueError('Missing raw inputs')
            for name,digest in manifest['sha256'].items():
                if sha(folder/name)!=digest:
                    raise ValueError('Raw hash mismatch')
            trades, quotes, minutes = [], [], set()
            for raw in lines(folder/'trades.jsonl.gz'):
                row = normalize_trade(raw,ticker,start,end)
                if row['trade_id'] in seen:
                    raise ValueError('Duplicate trade in finalized cohort')
                seen.add(row['trade_id']);trades.append(row)
            for raw in lines(folder/'candles.jsonl.gz'):
                if raw['end_period_ts'] in minutes:
                    raise ValueError('Duplicate candle')
                minutes.add(raw['end_period_ts'])
                row = normalize_quote(quote_schema(raw,manifest['archived_candles']),ticker,start,end)
                if row is not None:
                    quotes.append(row)
            if len(trades)!=manifest['trades'] or len(minutes)!=manifest['candles']:
                raise ValueError('Row count mismatch')
            markets[ticker] = dict(event=game['event'],series=series,kickoff=game['kickoff'],
                listed_at=epoch(market['open_time']),direction=1 if ticker==game['tickers'][0] else -1,
                verified_mecnet=True)
            expected_minutes = set(range(math.ceil(start/60)*60,math.floor(end/60)*60+1,60))
            entry_end = game['kickoff']-2100
            coverage.append(dict(ticker=ticker,trades=len(trades),minutes=len(minutes),
                missing_minutes=len(expected_minutes-minutes),null_quotes=len(minutes)-len(quotes),
                entry_window_seconds=entry_end-start,
                quote_coverage_fraction=covered_seconds(quotes,start,entry_end)/(entry_end-start)))
            records.extend(trades);records.extend(quotes)
    records.sort(key=lambda r:(r['at'],0 if r.get('kind')=='quote' else 1,r.get('trade_id',r['ticker'])))
    return records,markets,dict(markets=coverage,records=len(records),
        coefficients=cohort['sports'][series]['coefficients'],cohort_sha256=sha(ROOT/'COHORT.json'),
        capture_sha256=sha(ROOT/'CAPTURE.json'),status='RETROSPECTIVE_RECONSTRUCTION')


if __name__=='__main__':
    from m4_common import save
    audits={}
    for series in ('KXNCAAFGAME','KXMLBGAME'):
        try:
            tape,markets,audit=load_new(series);audits[series]=audit
            print(series,len(markets),'markets',len(tape),'observations')
        except Exception as error:
            audits[series]=dict(error=str(error),blocked=True)
            print(series,'BLOCKED',str(error))
    save(ROOT/'INPUT_AUDIT.json',audits)
