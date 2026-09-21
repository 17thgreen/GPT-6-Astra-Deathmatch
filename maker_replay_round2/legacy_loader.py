"""Load unchanged pinned replay functions without unrelated database imports."""
from pathlib import Path
import ast,sys,json,hashlib
from dataclasses import asdict
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
for row in manifest['files']:
    if row['required_for_reproduction']:
        p=ROOT/'repo'/row['path']
        if not p.exists():raise FileNotFoundError('Restore private comparator sources with fetch_sources.py first')
        if hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:raise ValueError('Comparator source hash mismatch')
sys.path.insert(0,str(ROOT/'repo/src'))
from flatstake.paper.account import Portfolio
from flatstake.paper.execution import SimulatedExecutionAdapter
from flatstake.paper.fees import FeeModel
from flatstake.paper.policy import MarketMakerPolicy,PolicyConfig,MarketState


def original_replay():
    tree=ast.parse((ROOT/'repo/src/flatstake/paper/replay.py').read_text())
    functions=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('_event_exposure','replay')]
    module=ast.Module(body=[ast.ImportFrom(module='__future__',names=[ast.alias(name='annotations')],level=0)]+functions,type_ignores=[])
    scope=globals().copy();exec(compile(ast.fix_missing_locations(module),'unchanged_pinned_replay','exec'),scope)
    return scope['replay']
