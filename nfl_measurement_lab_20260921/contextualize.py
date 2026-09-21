"""Descriptive context only: preserve Q1/Q2's early versus final-12h distinction.

Added after primary measurements; no new candidate or performance selection.
"""
import json
import statistics
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def main():
    schedule=json.loads((ROOT/'inputs/schedule_only.json').read_text())
    kickoff={g['event']:datetime.fromisoformat(g['kickoff']).timestamp() for g in schedule if g['event']}
    out={}
    for panel in ['q1_development','q3_development']:
        features=json.loads((ROOT/'results'/f'{panel}_features.json').read_text())
        groups=defaultdict(list)
        for f in features:
            event=f['ticker'].rsplit('-',1)[0];hours=(kickoff[event]-f['decision_at'])/3600
            regime='early_over_12h' if hours>12 else 'final_12h'
            groups[(event,regime)].append(dict(**f,hours_to_kickoff=hours))
        out[panel]=[]
        for (event,regime),rows in groups.items():
            depth=[f['displayed_depth'] for f in rows];threshold=3300 if regime=='early_over_12h' else 1327847.005
            out[panel].append(dict(event=event,regime=regime,joins=len(rows),median_depth=statistics.median(depth),
                minimum_depth=min(depth),maximum_depth=max(depth),reference_assumption=threshold,
                above_reference=sum(q>threshold for q in depth),
                hours_to_kickoff_min=min(f['hours_to_kickoff'] for f in rows),
                hours_to_kickoff_max=max(f['hours_to_kickoff'] for f in rows)))
    (ROOT/'results/queue_context.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))


if __name__=='__main__':main()
