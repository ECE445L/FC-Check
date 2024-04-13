import subprocess

VISUALIZE = True

if VISUALIZE:
    from rich.console import Console
    from rich import print
    from rich.table import Table

def runTest(repos) -> list:
    
    cpp_check_results = {}
    for repo in repos:
        repo_info, repo_path, git_repo = repo
        result = subprocess.run(['cppcheck', repo_path], stdout=subprocess.PIPE)
        cpp_check_results[repo_info['repository']['full_name']] = (repo_info,result.stdout.decode('utf-8'))

    if VISUALIZE:
        table = Table(title="Static Code Analysis")
        table.add_column("Names", style="magenta")
        table.add_column("Files", justify="right", style="green")

        for repo_name, data in cpp_check_results.items():
            student_names = ','.join([student['login'] for student in data[0]['students']])
            table.add_row(str(student_names), str('\n'.join(data[1])))
        
        console = Console()
        console.print(table)

    return []

class Test:
    def __init__(self):
        self.name = "Performs Static Code Analysis"
        self.enabled = True
        self.description = "Uses cppcheck to perform static code analysis on C/C++ "
        self.run_test = runTest

