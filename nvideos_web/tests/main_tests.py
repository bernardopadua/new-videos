# is running from virtualenv ?
import sys
from os import environ
from pathlib import Path
avoidENVCheck = environ.get("AVOID_VIRTUALENV_CHECK", "False").lower()=="true"
if sys.prefix != sys.base_prefix and not avoidENVCheck:
    #avoiding problems with no migration module
    sys.path.append(Path(__file__).parent.parent.__str__())

import unittest
from nvideos_web.tests.unit_tests import test_sql_builder

if __name__ == "__main__":
    unittest.findTestCases(test_sql_builder)
    unittest.main()