import ast
import unittest
from decimal import Decimal

import support
from ext2k1.errors import FloatDecimalRefused
from ext2k1.fees import cost_hl


class T05Fees(unittest.TestCase):
    def test_cost_hl_vectors_are_decimal(self):
        for vector in support.FIXTURES["t05_fee_vectors"]:
            got = cost_hl(vector["P"], vector["C"], M=vector["M"], rate=vector["rate"])
            self.assertIsInstance(got, Decimal)
            self.assertEqual(got, Decimal(vector["expect_cost_hl"]))

    def test_float_and_bool_inputs_are_refused(self):
        with self.assertRaises(FloatDecimalRefused):
            cost_hl(0.42, "100", M="1", rate="1")
        with self.assertRaises(FloatDecimalRefused):
            cost_hl("0.42", "100", M="1", rate=True)

    def test_run_blocks_fee_and_has_no_net_number(self):
        published = support.published()
        self.assertEqual(published["fee_admission"], "BLOCKED_FEE_UNVERIFIED")
        self.assertEqual(published["fee_block_reason"], "KXNFLGAME_NOT_IN_ADMITTED_FEE_SOURCE")
        for side in ("YES", "NO"):
            block = published["cells"][side]
            self.assertEqual(block["TMO_NET_C100"], "BLOCKED_FEE_UNVERIFIED")
            self.assertEqual(block["TMO_NET_C1"], "BLOCKED_FEE_UNVERIFIED")
        self._assert_no_numeric_net(published)

    def _assert_no_numeric_net(self, obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if "net" in str(key).lower() and isinstance(value, (int, float)) and not isinstance(value, bool):
                    self.fail("numeric net field %s" % key)
                self._assert_no_numeric_net(value)
        elif isinstance(obj, list):
            for value in obj:
                self._assert_no_numeric_net(value)

    def test_production_modules_have_no_rate_literal(self):
        package = support.LAB / "ext2k1"
        for path in sorted(package.glob("*.py")):
            source = path.read_text(encoding="utf-8")
            self.assertNotIn("0.07", source, path.name)
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and node.value in (0.07, "0.07"):
                    self.fail("%s contains a rate literal" % path.name)


if __name__ == "__main__":
    unittest.main()
