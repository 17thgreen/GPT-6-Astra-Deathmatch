"""Import boundaries: sqlite3 only in the snapshot loader; no network imports."""

import ast
import unittest
from pathlib import Path


LAB = Path(__file__).resolve().parent.parent
NETWORK = {
    'requests', 'urllib', 'http', 'socket', 'aiohttp', 'httpx', 'websocket', 'websockets',
}


def _modules(path):
    tree = ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            found.add(node.module.split('.')[0])
    return found


class ImportBoundaryTests(unittest.TestCase):
    def test_sqlite3_is_imported_only_by_the_snapshot_loader(self):
        sources = sorted(LAB.glob('*.py')) + sorted((LAB / 'tests').glob('*.py'))
        loaders = []
        others = []
        for path in sources:
            modules = _modules(path)
            if 'sqlite3' in modules:
                loaders.append(path.name)
            else:
                others.append(path.name)
        self.assertEqual(loaders, ['snapshot_loader.py'])
        self.assertIn('orchestrator.py', others)
        self.assertIn('gap_mapping.py', others)
        text = (LAB / 'snapshot_loader.py').read_text(encoding='utf-8')
        self.assertIn('mode=ro&immutable=1', text)
        self.assertIn('sqlite3.connect', text)

    def test_no_module_imports_a_network_client(self):
        sources = sorted(LAB.glob('*.py')) + sorted((LAB / 'tests').glob('*.py'))
        for path in sources:
            modules = _modules(path)
            self.assertFalse(modules & NETWORK, path.name)


if __name__ == '__main__':
    unittest.main()
