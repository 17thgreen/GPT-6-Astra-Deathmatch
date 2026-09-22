"""Positive-control checks for a real Q7 run. A missing tape is not a pass."""
import gzip, hashlib, json
from pathlib import Path
from paircheck_policy import Q6_ROOT, implementation_pin_mismatches, q6_pin_mismatches
from run_experiment import ROOT, scenario_grid

COMPARE_FIELDS = ('completed_strategy_pnl', 'all_flat', 'unresolved_contracts', 'week_contributions',
                  'unhedged_contract_hours', 'taker_contracts', 'maker_contracts', 'fills',
                  'pnl_excluding_top_two_games')
LEDGER_SUFFIXES = ('fills', 'orders', 'decisions')


def _read(path):
    return json.loads(path.read_text())


def uncompressed_ledger_hash(path):
    return hashlib.sha256(gzip.decompress(path.read_bytes())).hexdigest()


def not_run_document(state):
    return dict(status=state.get('status', 'NOT_RUN_NO_OUTPUT'), all_checks_passed=None,
                scenarios_executed=0, pnl=None,
                note='Verification did not run. all_checks_passed null means not applicable, not success.')


def _q6_reference(queue, delay, label):
    name = f'q{queue}_d{delay:g}_{label}'
    path = Q6_ROOT / 'results' / f'{name}.json'
    if not path.exists():
        return None, name
    return _read(path), name


def _baseline_ledger_targets():
    if not (Q6_ROOT / 'Q5_REFERENCES.json').exists():
        return {}
    data = _read(Q6_ROOT / 'Q5_REFERENCES.json')
    return {name: row.get('ledger_uncompressed_sha256') for name, row in data.items()
            if name.endswith('_baseline') and isinstance(row, dict)}


def compare_run(summary):
    mismatches = []
    scenarios = summary.get('scenarios', {})
    if set(scenarios) != set(scenario_grid()) or summary.get('failures'):
        mismatches.append('scenario_grid')
    ledger_targets = _baseline_ledger_targets()
    for name, result in scenarios.items():
        if result.get('config', {}).get('starting_cash') != 5000:
            mismatches.append(name + ':cash')
        if result.get('config', {}).get('order_size') != 250 or result.get('config', {}).get('exposure_cap') != 250:
            mismatches.append(name + ':cap')
        if result.get('config', {}).get('assumed_exit_depth') != 250:
            mismatches.append(name + ':exit_depth')
        if result.get('completed_strategy_pnl') is not None and (
                not result.get('all_flat') or result.get('unresolved_contracts', 1) >= .009):
            mismatches.append(name + ':unresolved_counted_as_profit')
        for row in result.get('pair_rejections', []):
            if row.get('counted_as_pnl') or row.get('reason') != 'combined_acquisition_cost':
                mismatches.append(name + ':rejection_ledger')
        arm = name.rsplit('_', 1)[-1]
        queue = int(name.split('_')[0][1:])
        delay = float(name.split('_')[1][1:])
        reference_label = {'A': 'baseline', 'D': '000'}.get(arm)
        if reference_label:
            reference, reference_name = _q6_reference(queue, delay, reference_label)
            if reference is None:
                mismatches.append(reference_name + ':missing_q6_summary')
            else:
                for field in COMPARE_FIELDS:
                    if result.get(field) != reference.get(field):
                        mismatches.append(f'{name}:{field}')
            if arm == 'A':
                expected = ledger_targets.get(f'q{queue}_d{delay:g}_baseline')
                if expected:
                    for suffix in ('fills', 'orders'):
                        path = ROOT / 'results' / f'{name}_{suffix}.jsonl.gz'
                        if not path.exists() or uncompressed_ledger_hash(path) != expected.get(suffix):
                            mismatches.append(f'{name}:{suffix}_hash')
            if arm == 'D':
                for suffix in LEDGER_SUFFIXES:
                    produced = ROOT / 'results' / f'{name}_{suffix}.jsonl.gz'
                    prior = Q6_ROOT / 'results' / f'q{queue}_d{delay:g}_000_{suffix}.jsonl.gz'
                    if prior.exists():
                        if not produced.exists() or uncompressed_ledger_hash(produced) != uncompressed_ledger_hash(prior):
                            mismatches.append(f'{name}:{suffix}_hash')
    return mismatches


def evaluate():
    pins = q6_pin_mismatches() + implementation_pin_mismatches()
    if pins:
        return dict(status='PIN_MISMATCH', all_checks_passed=False, scenarios_executed=0,
                    pnl=None, mismatches=pins)
    summary_path = ROOT / 'results' / 'experiment_summary.json'
    if not summary_path.exists():
        not_run = ROOT / 'results' / 'NOT_RUN.json'
        state = _read(not_run) if not_run.exists() else dict(status='NOT_RUN_NO_OUTPUT')
        return not_run_document(state)
    summary = _read(summary_path)
    if summary.get('status') != 'COMPLETE':
        return dict(status=summary.get('status', 'INCOMPLETE'), all_checks_passed=False,
                    scenarios_executed=len(summary.get('scenarios', {})), pnl=None,
                    note='A failed or partial run is not verified profit.')
    mismatches = compare_run(summary)
    return dict(status='VERIFIED' if not mismatches else 'CONTROL_MISMATCH',
                all_checks_passed=not mismatches, scenarios_executed=len(summary.get('scenarios', {})),
                pnl=None, mismatches=mismatches)


def main():
    document = evaluate()
    out = ROOT / 'results' / 'verification.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(document, indent=2, allow_nan=False))
    print(document['status'], flush=True)
    if document['status'] == 'VERIFIED':
        return
    if document.get('all_checks_passed') is None:
        raise SystemExit(3)
    raise SystemExit(1)
if __name__ == '__main__':
    main()
