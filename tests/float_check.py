import os
import re

VISUALIZE = True

if VISUALIZE:
    from rich.console import Console
    from rich import print
    from rich.table import Table


# TODO: For somereason some of the filters aren't matching despite being in blacklist
# Maybe better to do some sort of pattern matching instead?
blacklist = [
    'sw/lib/Filter/Filter.h',
    'sw/lib/Filter/MedianFilter.h',
    'sw/lib/Filter/MedianFilter.c',
    'sw/lib/Filter/SMAFilter.h',
    'sw/lib/Filter/SMAFilter.c',
    'sw/lib/Filter/KalmanFilter.h'
    'sw/lib/Filter/KalmanFilter.c',
    'sw/examples/Filter/keil/FilterExample.c',
    'sw/src/DPS310.c',
    'sw/inc/Blynk.h',
    'sw/inc/Blynk.c',
    'sw/examples/inc/Blynk.c',
    'sw/examples/inc/Blynk.h',
    'sw/examples/inc/SSD2119.h',
    'sw/examples/inc/SSD2119.c',
    'sw/inc/SSD2119.h',
    'sw/inc/SSD2119.c'
]

def runTest(repos) -> list:
    
    # RegEx pattern to match float+doubles
    float_double_pattern = re.compile(r'\b(float|double)\b')

    matches = {}

    for repo in repos:
        repo_info, repo_path, git_repo = repo

        # Converts the blacklist pathing to absolute paths for current repo
        blacklist_repo = [os.path.join(repo_path, path) for path in blacklist]
            
        # List to store files containing floats or doubles
        files_with_floats_doubles = []\
        
        # Walk through repo and its subdirectories
        # root is current directory being walked, dirs is current subdir, files is files in current walked dir
        for root, dirs, files in os.walk(repo_path):

            # Traverses files in current dir
            for file in files:
                # Only care about C/C++ sources and stuff not in blacklist
                # TODO: Maybe add a check to also only compare files that are commited by students
                file_path = os.path.join(root, file)
                if (file.endswith('.c') or file.endswith('.cpp') or file.endswith('.h')) and file_path not in blacklist_repo:
            
                    # Opens the file for reading
                    # Should note that python expects UTF-8 encoding. Escape characters break that
                    # so dirty fix is ignore it lmao
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        # Searches the files for matches to the expression
                        if float_double_pattern.search(content):
                            # Found a file with floating point in it
                            # Fills array with repo relative path
                            files_with_floats_doubles.append(file_path.replace(repo_path,''))
        
        # Prob better way of doing this
        matches[repo_info['repository']['full_name']] = (repo_info,files_with_floats_doubles)

    if VISUALIZE:
        table = Table(title="Floating point")
        table.add_column("Names", style="magenta")
        table.add_column("Files", justify="right", style="green")

        for repo_name, data in matches.items():
            student_names = ','.join([student['login'] for student in data[0]['students']])
            table.add_row(str(student_names), str('\n'.join(data[1])))
        
        console = Console()
        console.print(table)

    # TODO: Should have some standard value to return to the main program; however different tests can return different thing.
    # That way can also write to a CSV or produce "reports"
    return []

class Test:
    def __init__(self):
        self.name = "Floating Point Check"
        self.enabled = True
        self.description = "Checks the repo for isntances of floating point usage"
        self.run_test = runTest

