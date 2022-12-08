"""this module tests that testing is being done. How meta

This will throw an error if you introduce a new function but
neglect to include a test. 

Why does it have a "00" in the name? That is so that 
this test is run before any of the others. Because this is a 
lightweight test and should run quickly, we want this to run first.
(So that if it fails we don't waste time running other, more
expensive tests)

"""

from pathlib import Path

from pycore.dev import new_functions_should_be_tested


def test_new_functions_have_tests():
    """enforce that new functions have tests"""

    repo_dir = Path(__file__).parent.parent
    new_functions_should_be_tested(repo_dir)
