def runTest() -> list:
    print("Hello World, this is the commit_check test!")
    return []
class Test:
    def __init__(self):
        self.name = "Commit Checker"
        self.enabled = True
        self.description = "Checks the repo to see if all members have a commmit"
        self.run_test = runTest

