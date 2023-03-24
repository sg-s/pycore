"""software development best practices"""

import ast
import os
import subprocess
from glob import glob
from pathlib import Path, PosixPath
from typing import List, Union

from beartype import beartype


def find_all_functions_in_dir(dir_name: str) -> List:
    # find all .py files

    py_files = []
    for path in Path(dir_name).rglob("*.py"):
        py_files.append(path.absolute())

    # find all functions in all files
    all_functions = []
    for file in py_files:
        all_functions.extend(get_functions_in_module(file))

    # ignore functions that begin with _
    all_functions = [func for func in all_functions if func[0] != "_"]

    return all_functions


def find_untested_functions(dir_name: str) -> List:
    """find all functions that are missing tests in some
    directory


    """
    all_functions = find_all_functions_in_dir(dir_name)

    # make a list of test functions
    existing_tests = [
        func for func in all_functions if func.startswith("test")
    ]

    # make a list of true functions (that need tests)
    expected_tests = [
        "test_" + func for func in all_functions if not func.startswith("test")
    ]

    # find missing tests
    missing_tests = list(set(expected_tests).difference(set(existing_tests)))

    untested_functions = [func[5:] for func in missing_tests]

    return untested_functions


@beartype
def get_functions_in_module(module_loc: Union[str, PosixPath]) -> List:
    """returns a list of functions in some module

    You need to specify the location of the module on disk
    """
    source = open(module_loc).read()
    functions = [
        f.name
        for f in ast.parse(source).body
        if isinstance(f, ast.FunctionDef)
    ]
    return functions


@beartype
def new_functions_should_be_tested(
    repo_dir: Union[str, PosixPath],
    test_dir_name: str = "tests",
) -> None:
    """This function checks that all new functions have
    tests associated with them.

    Assumptions:

    1. You're using git
    2. You have a branch called main that you're merging into
    3. You have some feature branch that you're merging into main
    4. You have python code
    5. You have tests for each function in some folder
    6. Tests for functions are named "test_foo" for function "foo"

    The way it works is by looking at the diff w.r.t main,
    finding the new functions, and checking if those functions have
    tests in the test directory. If any function doesn't have a test
    this function fails.

    """

    # go to the repo dir
    os.chdir(repo_dir)

    # check that we are not on main branch
    branch_name = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    if branch_name == "main":
        print("repo on main branch, so nothing to compare to. Aborting.")
        return

    # get the diff from current state to main
    diff_lines = subprocess.run(
        ["git", "diff", "remotes/origin/main"], capture_output=True, text=True
    )
    diff_lines = diff_lines.stdout.split("\n")

    # find new functions w.r.t main
    new_functions = []

    for line in diff_lines:
        if line.find("+def ") > -1:
            a = line.find("+def ")
            z = line.find("(")
            fcn_name = line[a + 5 : z]
            if fcn_name[0] == "_":
                continue
            if fcn_name.find("test") >= 0:
                continue
            new_functions.append(fcn_name)

    if len(new_functions) == 0:
        print("No new functions detected, aborting.")
        return

    else:
        for func_name in new_functions:
            print(f"New function: {func_name}")

    is_tested = [False for _ in new_functions]

    # find all .py files in test_dir
    test_dir = os.path.join(repo_dir, test_dir_name)
    test_files = glob(os.path.join(test_dir, "*.py"))

    for test_file in test_files:
        with open(test_file) as file:
            lines = file.readlines()
        lines = [line.rstrip() for line in lines]

        for new_function in new_functions:
            for line in lines:
                if line.find("test_" + new_function) > 0:
                    idx = new_functions.index(new_function)
                    is_tested[idx] = True

    if min(is_tested):
        print("All new functions have tests associated with them")
        return

    # something is untested. say what it is, and fail
    for thing, func_name in zip(is_tested, new_functions):
        if not thing:
            print(f"{func_name} is not being tested")
    raise RuntimeWarning("Some functions are not tested")
