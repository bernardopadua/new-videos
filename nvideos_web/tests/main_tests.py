# is running from virtualenv ?
import sys
from os import environ
from pathlib import Path
avoidENVCheck = environ.get("AVOID_VIRTUALENV_CHECK", "False").lower()=="true"
if sys.prefix != sys.base_prefix and not avoidENVCheck:
    #avoiding problems with no migration module
    sys.path.append(Path(__file__).parent.parent.parent.__str__())

import unittest
from argparse import ArgumentParser

# Suites
from nvideos_web.tests.unit_tests.impl.base.test_sql_builder import suite_sql_builder_tests
from nvideos_web.tests.unit_tests.impl.base.test_row_factory import suite_row_factory_tests

parser = ArgumentParser(description="Argument for tests")
parser.add_argument("-v", 
    "--verbosity", 
    action="store_true", help="Add verbosity to test runner."
)

if __name__ == "__main__":
    _verbosity: int = 1
    args = parser.parse_args()
    if args.verbosity:
        _verbosity = 10
    runner = unittest.TextTestRunner(verbosity=_verbosity)
    runner.run(suite_sql_builder_tests())
    runner.run(suite_row_factory_tests())
