# Code Jam Practice Folder

Provides Python template files for Code Jam challenges and a script for making a new problem folder. The standard template is from the normal post-2018 problems, and there are also templates for pre-2018 and interactive problems.

## Getting Started

Clone the repo into your practice folder, and run the `new_problem.py` script with the following usage:

    python3 <path>/new_problem.py [-h] [-i] -y <year> -r <round> -n <name>

The `-n` flag is always required, and `-y` and `-r` flags are required unless the current working directory is a subdirectory of `<repo_root>`. If CWD is of the form `<repo_root>/<year>` then the user doesn't need to specify the year and if it is of the form `<repo_root>/<year>/<round>` then user also doesn't need to specify the round, but they can still specify a different year or round if they want.

* `-h`: display usage (optional)
* `-i`: interactive problem (optional)
* `-y`: flag for the problem year, which must be integer
* `-r`: flag for the round name (Qualification, Round1C, etc.)
* `-n`: flag for the problem name

If `-h` is included the program displays usage and then it exits. If the required flags are included, it will look for the file `<repo_root>/<year>/<round>/<name>/main.py` and abort if it is found, otherwise the file will be created along with any necessary folders. If `<year>` is less than 2018 it will use the classic template, and otherwise it will use the standard template unless interactive is specified with the `-i` flag.

### Prerequisites
`new_problem.py` uses pathlib so needs to be run with python 3.4+.

## TODO

* Change CWD to the newly created folder?

* Improve templates.

## Author

* **William Gollinger**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
