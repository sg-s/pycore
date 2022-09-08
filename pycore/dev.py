"""software development best practices"""

import os
import subprocess
from glob import glob


def new_functions_should_be_tested(
    repo_dir: str, test_dir_name: str = "tests"
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
