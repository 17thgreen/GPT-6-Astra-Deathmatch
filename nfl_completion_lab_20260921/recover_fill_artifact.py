"""Regenerate one damaged ledger using frozen inputs and policy; compare outputs."""
import hashlib
import json
from datetime import datetime, timezone

from load_data import ROOT, load_all
from replay_v2 import Config
from run_experiment import run_one


def main():
    for filename, expected in json.loads((ROOT / 'FROZEN_CODE.json').read_text()).items():
        assert hashlib.sha256((ROOT / filename).read_bytes()).hexdigest() == expected
    name = 'combined_q291_q1_route'
    summary = json.loads((ROOT / 'results/experiment_summary.json').read_text())
    before = summary['scenarios'][name]
    ledger = ROOT / 'results' / (name + '_fills.jsonl.gz')
    record = dict(scenario=name, detected_error='EOFError: Compressed file ended before the end-of-stream marker was reached',
                  original_ledger_bytes=ledger.stat().st_size,
                  original_ledger_sha256=hashlib.sha256(ledger.read_bytes()).hexdigest(),
                  original_valid_lines_before_error=95716, expected_fills=before['fills'],
                  timestamp=datetime.now(timezone.utc).isoformat())
    events, markets, _ = load_all()['combined']
    after = run_one(name, events, markets, Config(**before['config']), 'q1_route')
    differences = [k for k in set(before) | set(after) if k != 'seconds' and before.get(k) != after.get(k)]
    record.update(summary_fields_changed_excluding_runtime=differences,
                  regenerated_ledger_bytes=ledger.stat().st_size,
                  regenerated_ledger_sha256=hashlib.sha256(ledger.read_bytes()).hexdigest(),
                  finished=datetime.now(timezone.utc).isoformat())
    (ROOT / 'results/artifact_recovery.json').write_text(json.dumps(record, indent=2))
    assert not differences, differences
    print('Recovered ledger; every saved summary field matches exactly except runtime.')


if __name__ == '__main__':
    main()
