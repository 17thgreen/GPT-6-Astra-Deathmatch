import ast
import unittest

import support  # noqa: F401
from constants import REGISTRY_CITATION_SHA256
from errors import LeeReadyRefused
from markouts import lee_ready, reject_lee_ready
from pathlib import Path
from pins_io import LAB


class T09LeeReady(unittest.TestCase):
    def test_lee_ready_call_and_key_are_refused(self):
        with self.assertRaises(LeeReadyRefused):
            lee_ready("buy")
        with self.assertRaises(LeeReadyRefused):
            reject_lee_ready(key="lee_ready")
        with self.assertRaises(LeeReadyRefused):
            reject_lee_ready(call="Lee-Ready")

    def test_no_price_bin_function_and_registry_citation_remains(self):
        for path in LAB.glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    self.assertFalse(
                        any(token in node.name.lower() for token in ("price_band", "bin_price", "rebin"))
                    )
        registry = Path(LAB).resolve().parents[0] / "docs" / "EXPERIMENT_REGISTRY.md"
        if registry.is_file():
            self.assertIn(REGISTRY_CITATION_SHA256, registry.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
