def runTest(repos) -> list:
    
    for repo in repos:
        repo_info, repo_path, git_repo = repo
        pass

    return []

class Test:
    def __init__(self):
        self.name = "Linter"
        self.enabled = True
        self.description = "Lints the repo to check for C style"
        self.run_test = runTest

