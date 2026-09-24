"""Reproduce the frozen scores from the included derived input; verify accounting."""
from contextlib import redirect_stdout
from decimal import Decimal
from pathlib import Path
import hashlib,io,json,tempfile
from run_study import run

def verify(root):
    freeze=json.loads((root/'IMPLEMENTATION_FREEZE_ADDENDUM.json').read_text())
    for name,expected in freeze['source_sha256'].items():
        assert hashlib.sha256((root/name).read_bytes()).hexdigest()==expected,('frozen source changed',name)
    provenance=json.loads((root/'data/PROVENANCE.json').read_text())
    data=root/'data/analysis_input.json'
    assert hashlib.sha256(data.read_bytes()).hexdigest()==provenance['input_sha256']
    with tempfile.TemporaryDirectory() as td,redirect_stdout(io.StringIO()):
        run(data,Path(td))
        for name in ['scorecard.json','hypothetical_trades.json','summary.csv']:
            assert (Path(td)/name).read_bytes()==(root/'results'/name).read_bytes(),('reproduction differs',name)
    ledger=json.loads((root/'results/hypothetical_trades.json').read_text())
    keys=set()
    for row in ledger:
        key=tuple(row[k] for k in ['study','family','decision','race_id','arm'])
        assert key not in keys;keys.add(key)
        p=Decimal(str(row['price']));y=Decimal(row['outcome_dem'])
        payout=y if row['side']=='yes' else 1-y
        expected=payout-p-Decimal('.07')*p*(1-p)-Decimal('.02')
        assert abs(expected-Decimal(str(row['net'])))<Decimal('1e-12'),row['ticker']
        assert abs(Decimal(str(row['net']))+Decimal(str(row['capital']))-payout)<Decimal('1e-12')
    return {'frozen_source_hashes_verified':len(freeze['source_sha256']),
            'published_input_hash_verified':True,'exact_result_files_reproduced':3,
            'independent_decimal_trade_ledger_checks':len(ledger),
            'live_validation':False}

if __name__=='__main__':
    root=Path(__file__).resolve().parent;result=verify(root)
    (root/'results/verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
