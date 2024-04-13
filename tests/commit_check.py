VISUALIZE = True

import time
from git import Repo

if VISUALIZE:
    from rich.console import Console
    from rich import print
    from rich.table import Table


def runTest(repos) -> list:
    author_counter = {}
    for gh_r in repos:
        repo_info, repo_path, repo = gh_r
        commits = repo.iter_commits('--all')
        for commit in commits:
            # print("Committed by %s on %s with sha %s" % (commit.committer.name, time.strftime("%a, %d %b %Y %H:%M", time.localtime(commit.committed_date)), commit.hexsha))
            author = commit.committer.name

            # TODO: Should do some filter to match the author with a student in the current iterated repo
            # The author name doesn't match the emails, name, logins that are part of the assignment info; such as when students use github UI

            # Check if the author already exists in the counter dictionary
            if author in author_counter:
                # If the author exists, increment their counter
                author_counter[author] += 1
            else:
                # If the author doesn't exist, add them to the counter dictionary
                author_counter[author] = 1
  
    if VISUALIZE:
        table = Table(title="Commit Count")
        table.add_column("Student", style="magenta")
        table.add_column("Commit Count", justify="right", style="green")

        for author, count in author_counter.items():
            table.add_row(str(author), str(count))
        console = Console()
        console.print(table)

    # TODO: Should have some standard value to return to the main program; however different tests can return different thing.
    # Maybe something like an array where each element in the array corresponds to a repo. that element will contain any relevant info from the test on the repo?
    return [author_counter]

class Test:
    def __init__(self):
        self.name = "Commit Checker"
        self.enabled = True
        self.description = "Checks the repo to see if all members have a commmit"
        self.run_test = runTest

