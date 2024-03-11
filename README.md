# ECE 445L Fast Code Checker

Utility for running custom code reviews and tests on student repos.

## Requirements

- Python >= 3.11

All dependencies can be installed via `requirements.txt`.

```sh
pip install -r requirements.txt
```

Might be reccomended to have it in its own environment.

## Usage

Run the script

``` sh
python fc_check.py
```

You must authenticate the application with Github. Afterwards you can choose a classroom and a assignment. From that assignment you can run a multitude of tests. These tests are defined in `tests`. Each test does some operation on the repo and yield its results. The script aggregates the results of each tests into a spreadsheet.