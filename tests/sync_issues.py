"""small script to sync issue state when tests are run"""


from pycore.github_issues import (
    close_issues_for_tested_functions,
    open_issues_for_untested_functions,
)

with open("github_token", "r") as file:
    token = file.read().strip()

with open("repo_name", "r") as file:
    repo_name = file.read().strip()

print("Opening issues for untested functions...")
open_issues_for_untested_functions(
    token=token,
    github_repo=repo_name,
)

print("Closing issues for tested functions...")
close_issues_for_tested_functions(
    token=token,
    github_repo=repo_name,
)
