import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import hashlib
import importlib.util
import inspect
import json
import subprocess
import unittest
from pathlib import Path

import support
from scoring import cache_fee_table, cache_order_fee


LAB = Path(__file__).resolve().parents[1]
REPO = LAB.parent
PINS = LAB / 'pins'


class T4Verbatim(unittest.TestCase):
    def test_arm_lines_and_code_pins(self):
        frozen_path = PINS / 'lab/governance/astra/packets/Q6S5_PR60_SCORABILITY/FROZEN_EXPERIMENT.json'
        frozen = json.loads(frozen_path.read_text())
        claimed = frozen['verbatim_sha256_no_trailing_newline']
        arms = frozen['arms_verbatim']
        pr60_lines = (
            PINS / 'lab/governance/astra/packets/Q6S5_KXMLBSPREAD_STRATEGY_FILL_FREEZE_2026-09-25.md'
        ).read_text().splitlines()
        parent_lines = (
            PINS / 'lab/governance/astra/packets/Q6S5_KXMLBSPREAD_FEEQUEUE_HARNESS_FREEZE_2026-09-25.md'
        ).read_text().splitlines()
        pairs = (
            (pr60_lines[92], '9f50ba19_L93', 'metric_9f50ba19_line93'),
            (pr60_lines[99], '9f50ba19_L100_A0', 'A0_9f50ba19_line100'),
            (pr60_lines[100], '9f50ba19_L101_A1', 'A1_9f50ba19_line101'),
            (parent_lines[46], '4f65dcdf_L47', 'parent_4f65dcdf_line47'),
            (parent_lines[47], '4f65dcdf_L48', 'parent_4f65dcdf_line48'),
        )
        for line, digest_key, text_key in pairs:
            self.assertEqual(line, arms[text_key])
            self.assertEqual(hashlib.sha256(line.encode('utf-8')).hexdigest(), claimed[digest_key])
        import fill_engine
        pr60 = fill_engine.load_pr60()
        parent = fill_engine.load_parent()
        self.assertEqual(pr60.ARMS, dict(parent.ANALYSIS_SLICE))
        self.assertEqual(pr60.ARMS['Q6S5A0'], 'maker_vs_taker_native')
        self.assertEqual(pr60.ARMS['Q6S5A1'], 'content_fresh_vs_stale_bin')
        runner = REPO / 'kalshi_q6s5_kxmlbspread_strategy_fill_lab_20260925/orchestrator.py'
        digest = hashlib.sha256(runner.read_bytes()).hexdigest()
        self.assertEqual(digest, '296cfe64ff24c2fad0437ce9a9ec11458f557ee94ee900bd621160dc283fa597')
        tree = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD:kalshi_q6s5_kxmlbspread_strategy_fill_lab_20260925'],
            cwd=str(REPO),
        ).decode().strip()
        self.assertEqual(tree, '78fca23c47fd8475771bec39bddc516efd92b06d')
        pr62_path = REPO / 'kalshi_q6s5_kxmlbspread_game_phase_settled_tape_lab_20261001/orchestrator.py'
        spec = importlib.util.spec_from_file_location('pr62_fee_verbatim', pr62_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(inspect.getsource(cache_order_fee), inspect.getsource(module.cache_order_fee))
        self.assertEqual(inspect.getsource(cache_fee_table), inspect.getsource(module.cache_fee_table))
        self.assertIsNone(cache_order_fee('maker', 1, '0.4000')['formula_id'])
        self.assertEqual(cache_order_fee('taker', 1, '0.4000')['label'], 'CACHE_NOT_R1P1')


if __name__ == '__main__':
    unittest.main()
