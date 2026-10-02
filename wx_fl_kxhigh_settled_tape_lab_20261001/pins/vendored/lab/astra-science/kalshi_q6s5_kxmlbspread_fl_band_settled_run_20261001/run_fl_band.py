"""Simulator driver: run merged PR61 runner (main d7558fc4) on the pinned settled tape.

Offline only. A socket guard refuses any network attempt. Calls only the runner's own
entry points; does not modify the runner; does not call measure_rows on real rows
(freeze: metrics stay null until an Examiner-scored run; ruling 09763030 never:
results/pnl non-null before Examiner SCORE).
"""
import json, socket, sys
from datetime import datetime
from pathlib import Path

NET_ATTEMPTS = []
def _refuse(*a, **k):
    NET_ATTEMPTS.append(repr(a)[:200])
    raise RuntimeError('NETWORK_REFUSED_OFFLINE_RUN')
socket.socket.connect = _refuse
socket.socket.connect_ex = _refuse
socket.create_connection = _refuse
socket.getaddrinfo = _refuse

L = Path(__file__).resolve().parent
RT = L / 'runner_tree' / 'kalshi_q6s5_kxmlbspread_fl_band_settled_tape_lab_20260929'
OUT = L / 'results'
sys.path.insert(0, str(RT))
import orchestrator as o  # noqa: E402

def dump(name, obj):
    (OUT / name).write_text(json.dumps(obj, indent=1, sort_keys=True, default=str) + '\n')

started = datetime.now().astimezone().isoformat(timespec='seconds')
assert o.ROOT == RT, o.ROOT

# strict-< boundary on the runner's own function (ruling 09763030: created_time < panel admitted_at)
boundary = {
    'panel_admitted_at': o.PANEL_ADMITTED_AT,
    'cases': {
        '2026-09-25T04:37:46.999999Z': o.pre_admitted_at('2026-09-25T04:37:46.999999Z'),
        '2026-09-25T04:37:47Z': o.pre_admitted_at('2026-09-25T04:37:47Z'),
        '2026-09-25T04:37:47.000001Z': o.pre_admitted_at('2026-09-25T04:37:47.000001Z'),
    },
}
boundary['strict_lt_ok'] = boundary['cases'] == {
    '2026-09-25T04:37:46.999999Z': True, '2026-09-25T04:37:47Z': False, '2026-09-25T04:37:47.000001Z': False}
boundary['runner_flag_cli'] = None
boundary['note'] = ('Runner has no CLI/flag for the comparator; strict < is hard-coded in orchestrator.pre_admitted_at '
                    '(ts < PANEL_ADMITTED_AT_UTC). Default already equals ruling; nothing overridden.')
if not boundary['strict_lt_ok']:
    raise SystemExit('STRICT_LT_BOUNDARY_FAIL')
dump('PRE_ADMITTED_AT_BOUNDARY_CHECK.json', boundary)

addendum = o.verify_pins_manifest()
conduct = o.conduct()
dump('CONDUCT.json', conduct)
counts = o.admitted_at_arm_counts()
dump('ADMITTED_AT_ARM_COUNTS.json', counts)
inventory = o.inventory_pinned_prints()
dump('INVENTORY_PINNED_PRINTS.json', inventory)
digest = o.digest_status()
dump('RUNNER_DIGEST_STATUS.json', digest)
card = o.published_scorecard()
dump('PUBLISHED_SCORECARD.json', card)

scope = {
    'scope': 'Sep-24 markets only (6 markets / 3 events)',
    'in_scope_tickers': sorted(o.IN_SCOPE),
    'in_scope_events': sorted(set(o.IN_SCOPE.values())),
    'sep25_out_of_scope_tickers': sorted(o.SEP25_OUT_OF_SCOPE),
    'collector_prints_per_ticker': o.COLLECTOR_PRINTS,
    'enforced_by': 'orchestrator.IN_SCOPE / SEP25_OUT_OF_SCOPE (classify_trade) and _load_in_scope_markets',
}
dump('SCOPE.json', scope)

arm_total = sum(v['pre_admitted_at'] + v['post_admitted_at'] for v in counts['arms'].values())
summary = {
    'id': 'SIMULATOR_RUN_SUMMARY_Q6S5_FL_BAND_SETTLED_TAPE_PR61',
    'started_at_et': started,
    'finished_at_et': datetime.now().astimezone().isoformat(timespec='seconds'),
    'runner': str(RT / 'orchestrator.py'),
    'entry_points_called': ['pre_admitted_at (boundary)', 'verify_pins_manifest', 'conduct', 'admitted_at_arm_counts',
                            'inventory_pinned_prints', 'digest_status', 'published_scorecard'],
    'entry_points_not_called': {'measure_rows': 'not called on real rows: freeze fb6540f5 says all ROI/delta/LOEO/LOMO/exclusion-count fields stay null until an Examiner-scored run; ruling 09763030 never results/pnl non-null before Examiner SCORE; merged conduct() does not join tape to settlement ROI'},
    'evidence_class': o.EVIDENCE_CLASS,
    'label': o.LABEL,
    'n_prints_pinned': conduct['n_prints_pinned'],
    'included_rows_total': arm_total,
    'pinned_minus_included': conduct['n_prints_pinned'] - arm_total,
    'arms': counts['arms'],
    'results': None, 'pnl': None,
    'maker_gross_roi_delta_FL0_minus_FL1': conduct['maker_gross_roi_delta_FL0_minus_FL1'],
    'reading': conduct['reading'],
    'digest_all_match_claimed': conduct['digest_all_match_claimed'],
    'fee_label': o.FEE_LABEL, 'fee_type': o.FEE_TYPE, 'fee_multiplier': o.FEE_MULTIPLIER,
    'scored': False, 'keep_claim': False, 'counts_toward_keep': False, 'promote': False,
    'live_gets': conduct['live_gets'], 'orders': conduct['orders'],
    'network_attempts_blocked': len(NET_ATTEMPTS), 'network_attempts': NET_ATTEMPTS,
    'addendum_evidence_class_verified': addendum['ruling']['evidence_class'],
}
dump('RUN_SUMMARY.json', summary)
print(json.dumps(summary, indent=1, default=str))
