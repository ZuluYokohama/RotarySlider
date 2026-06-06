import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))
import aaa_quality


class TestAAAQualityImports(unittest.TestCase):
    """Guards against the syntax error that made aaa_quality unimportable.

    A malformed `def check_radon, check_quantum_crypto(target_dir):` once
    fused two function names, raising SyntaxError on import and silently
    disabling the entire AAA Quality pre-gate. Importing the module here and
    asserting its check_* functions exist catches any regression.
    """

    def test_module_imports(self):
        self.assertTrue(hasattr(aaa_quality, 'run_aaa_suite'))

    def test_expected_checks_exist(self):
        for name in ('check_flake8', 'check_bandit', 'check_radon', 'check_quantum_crypto'):
            self.assertTrue(callable(getattr(aaa_quality, name, None)),
                            f"expected callable aaa_quality.{name}")


if __name__ == '__main__':
    unittest.main()
