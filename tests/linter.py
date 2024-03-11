def runTest() -> list:
    print("Hello World, this is the linter test!")
    return []

class Test:
    def __init__(self):
        self.name = "Linter"
        self.enabled = True
        self.description = "Lints the repo to check for C style"
        self.run_test = runTest

