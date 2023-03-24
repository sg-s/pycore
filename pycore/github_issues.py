import os

from github import Github, GithubException
from pycore.dev import find_all_functions_in_dir, find_untested_functions


def open_issues_for_untested_functions(
    *,
    repo_dir: str = ".",
    token: str,
    github_repo: str,
) -> None:
    """create a Github issue for each function that is lacking a test in
    some repo.

    Only untested functions that don't already have an issue will
    trigger the creation of an issue.

    """

    g = Github(token)
    repo = g.get_repo(github_repo)

    untested_functions = find_untested_functions(repo_dir)

    issues = repo.get_issues(state="open", labels=["testing"])
    untested_functions_with_issues = []
    for issue in issues:
        untested_functions_with_issues.append(
            issue.title.replace("needs tests", "").strip()
        )

    untested_functions_without_issues = set(untested_functions).difference(
        set(untested_functions_with_issues)
    )

    # only do first ten to avoid rate checks on github
    for func in list(untested_functions_without_issues)[:10]:
        try:
            print(f"Creating issue for testing {func}")
            repo.create_issue(
                f"{func} needs tests",
                body="This issue was automatically generated",
                labels=["testing"],
            )
        except GithubException:
            # rate limit
            pass


def close_issues_for_tested_functions(
    *,
    repo_dir: str = ".",
    token: str,
    github_repo: str,
) -> None:
    g = Github(token)
    repo = g.get_repo(github_repo)

    untested_functions = find_untested_functions(repo_dir)
    all_functions = find_all_functions_in_dir(repo_dir)

    issues = repo.get_issues(state="open", labels=["testing"])

    for issue in issues:
        underlying_func = issue.title.replace("needs tests", "").strip()
        if underlying_func in untested_functions:
            continue

        print(f"Closing issue for testing {underlying_func}")

        # add a comment saying we're closing this
        if underlying_func in all_functions:
            issue.create_comment(
                "Automatically closed, because a test was written for this function"
            )
        else:
            issue.create_comment(
                "Automatically closed, because this function no longer exists in the codebase."
            )

        # close this issue
        issue.edit(state="closed")
