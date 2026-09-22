"""Freeze exact-event metadata; no tape/price selection or simulated outcomes."""
import concurrent.futures
import re
from collections import defaultdict
from decimal import Decimal
from m4_common import ROOT, M3, get, epoch, read, save, write_rows, sha

TYPES = {'KXNCAAFGAME':'football_game', 'KXMLBGAME':'baseball_game',
         'KXNHLGAME':'hockey_match', 'KXNBAGAME':'basketball_game'}


def coefficients(series, event):
    kind = event.get('fee_type_override') or series.get('fee_type')
    multiplier = event.get('fee_multiplier_override')
    if multiplier is None:
        multiplier = series.get('fee_multiplier')
    multiplier = Decimal(str(multiplier))
    if not multiplier.is_finite() or multiplier < 0:
        raise ValueError('Invalid fee multiplier')
    if kind not in ('quadratic', 'quadratic_with_maker_fees'):
        raise ValueError('Unsupported fees')
    return dict(maker=float(Decimal('.0175')*multiplier) if kind.endswith('maker_fees') else 0.,
                taker=float(Decimal('.07')*multiplier), type=kind, multiplier=str(multiplier),
                evidence='CURRENT_RULE_COUNTERFACTUAL_NOT_HISTORICAL_FEE_VERIFICATION')


def select_nba(ids):
    dates = defaultdict(list)
    for event in sorted(set(ids)):
        match = re.fullmatch(r'KXNBAGAME-26MAY(0[1-9]|1[0-9]|20)[A-Z0-9]+', event)
        if match:
            dates[match[1]].append(event)
    selected, rank = [], 0
    while len(selected) < 8:
        added = False
        for day in sorted(dates):
            if rank < len(dates[day]):
                selected.append(dates[day][rank]); added = True
                if len(selected) == 8:
                    break
        if not added:
            break
        rank += 1
    return selected, dict(dates)


def discover_nba():
    out = dict(complete=False, endpoints=[], failures=[])
    ids = set()
    for path in ('markets', 'historical/markets'):
        raw, cursor, seen = [], None, set()
        try:
            for _ in range(20):
                params = dict(series_ticker='KXNBAGAME', limit=1000)
                if path == 'markets':
                    params.update(min_close_ts=int(epoch('2026-05-01T00:00:00Z')),
                                  max_close_ts=int(epoch('2026-05-21T00:00:00Z')))
                if cursor:
                    params['cursor'] = cursor
                data, source = get(path, params)
                raw.append(dict(response=data, source=source))
                ids.update(m['event_ticker'] for m in data.get('markets', []))
                cursor = data.get('cursor')
                if not cursor:
                    break
                if cursor in seen:
                    raise ValueError('Repeated NBA cursor')
                seen.add(cursor)
            else:
                raise ValueError('NBA pagination limit')
        except Exception as error:
            out['failures'].append(dict(endpoint=path, error=str(error)))
        filename = ROOT/'metadata'/('nba_'+path.replace('/', '_')+'.jsonl.gz')
        write_rows(filename, raw)
        out['endpoints'].append(dict(endpoint=path, pages=len(raw), sha256=sha(filename),
                                    file=str(filename.relative_to(ROOT)), exhausted=not cursor))
    selected, dates = select_nba(ids)
    out.update(complete=not out['failures'], reserved=selected if not out['failures'] else [],
               candidate_selection=selected, events_by_day=dates)
    save(ROOT/'NBA_RESERVATION.json', out)
    return out


def validate_structure(series, event, markets, milestones):
    if event.get('series_ticker') != series or event.get('collateral_return_type') != 'MECNET' or not event.get('mutually_exclusive'):
        raise ValueError('Unsupported event structure/series')
    if len(markets) != 2 or len({m.get('yes_sub_title') for m in markets}) != 2:
        raise ValueError('Not two distinct team markets')
    for market in markets:
        if (market['event_ticker'] != event['event_ticker'] or market['market_type'] != 'binary'
            or Decimal(market['notional_value_dollars']) != 1
            or market.get('price_level_structure') != 'linear_cent'
            or market.get('mve_selected_legs')):
            raise ValueError('Unsupported market identity/notional/grid')
        if not market.get('rules_primary') or not market.get('rules_secondary'):
            raise ValueError('Missing contract rules')
    matches = [m for m in milestones.get('milestones', [])
               if m.get('type') == TYPES[series] and m.get('category') == 'Sports'
               and event['event_ticker'] in m.get('related_event_tickers', [])]
    if milestones.get('cursor') or len(matches) != 1:
        raise ValueError('Missing/ambiguous/unexhausted exact-event schedule')
    start = epoch(matches[0]['start_date'])
    if any(epoch(m['open_time']) >= start-11100 for m in markets):
        raise ValueError('Insufficient listing window for control')
    return start, matches[0]


def resolve(item, series_responses):
    series, event_id = item
    result = dict(series=series, event=event_id, structurally_admitted=False,
                  replay_admitted=False, manual_review_required=True)
    try:
        metadata, source = get('events/'+event_id)
        result.update(metadata=metadata, metadata_source=source)
        event = metadata['event']
        markets = metadata.get('markets', event.get('markets', []))
        if len(markets) != 2:
            historical, hs = get('historical/markets', dict(event_ticker=event_id, limit=1000))
            result['historical_markets'] = dict(response=historical, source=hs)
            if historical.get('cursor'):
                raise ValueError('Unexhausted historical event markets')
            combined = {m['ticker']:m for m in historical.get('markets', [])}
            combined.update({m['ticker']:m for m in markets})
            markets = list(combined.values())
        result['markets'] = markets
        milestones, source = get('milestones', dict(related_event_ticker=event_id, limit=100))
        result.update(milestones=milestones, schedule_source=source)
        start, match = validate_structure(series, event, markets, milestones)
        result.update(kickoff=start, matched_milestone=match,
                      tickers=sorted(m['ticker'] for m in markets),
                      coefficients=coefficients(series_responses[series]['response']['series'], event),
                      structurally_admitted=True)
    except Exception as error:
        result['failure'] = str(error)
    save(ROOT/'metadata'/f'{event_id}.json', result)
    print(event_id, 'STRUCTURE_OK' if result['structurally_admitted'] else result['failure'], flush=True)
    return result


def main():
    if (ROOT/'COHORT_METADATA.json').exists():
        raise ValueError('Metadata already frozen; do not overwrite')
    out = dict(games=[], series={}, failures=[])
    try:
        response, source = get('historical/cutoff')
        out['cutoffs'] = dict(response=response, source=source)
    except Exception as error:
        out['failures'].append(dict(stage='cutoffs', error=str(error)))
    for series in TYPES:
        try:
            response, source = get('series/'+series)
            out['series'][series] = dict(response=response, source=source)
        except Exception as error:
            out['failures'].append(dict(stage=series, error=str(error)))
    availability = read(M3/'MARKET_AVAILABILITY.json')
    pairs = [(s['series'], event) for s in availability['series']
             if s['series'] in TYPES and s['series'] != 'KXNBAGAME' for event in s['reserved']]
    nba = discover_nba()
    pairs.extend(('KXNBAGAME', event) for event in nba['reserved'])
    out['reserved'] = {s:[event for series,event in pairs if series==s] for s in TYPES}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for result in pool.map(lambda pair:resolve(pair, out['series']), pairs):
            out['games'].append(result)
            save(ROOT/'COHORT_METADATA.partial.json', out)
    out['nba_discovery_complete'] = nba['complete']
    save(ROOT/'COHORT_METADATA.json', out)
    print('METADATA_COMPLETE', len(out['games']), 'reserved events', flush=True)


if __name__ == '__main__':
    main()
