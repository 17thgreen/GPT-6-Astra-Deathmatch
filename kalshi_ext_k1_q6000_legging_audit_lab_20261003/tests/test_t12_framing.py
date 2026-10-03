import json
import re
import unittest

import support  # noqa: F401
from constants import VERDICT_DOMAIN
from orchestrator import RESULTS, measure

KEY_RE = re.compile(r"(^|_)(pnl|roi|keep|profit|return)(_|$)", re.IGNORECASE)


class T12Framing(unittest.TestCase):
    def test_committed_outputs_have_null_profit_fields_and_closed_verdict(self):
        measure(write=True)
        empty = json.loads((RESULTS / "EMPTY_RESULTS.json").read_text(encoding="utf-8"))
        self.assertIsNone(empty["results"])
        self.assertIsNone(empty["pnl"])
        self.assertIsNone(empty["roi"])
        self.assertIn(empty["verdict"], VERDICT_DOMAIN)
        self.assertIs(empty["counts_toward_keep"], False)
        for path in sorted(RESULTS.glob("*.json")):
            payload = json.loads(path.read_text(encoding="utf-8"))
            self._walk(payload, path.name)

    def _walk(self, obj, name):
        if isinstance(obj, dict):
            verdict = obj.get("verdict")
            if "verdict" in obj:
                self.assertIn(verdict, (*VERDICT_DOMAIN, None), name)
            for key, value in obj.items():
                if KEY_RE.search(key):
                    if key == "counts_toward_keep":
                        self.assertIs(value, False, name)
                    else:
                        self.assertIsNone(value, f"{name}:{key}")
                self._walk(value, name)
        elif isinstance(obj, list):
            for value in obj:
                self._walk(value, name)


if __name__ == "__main__":
    unittest.main()
