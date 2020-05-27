# Code Jam Practice Folder

v1.1.1

Provides Python template files for coding competition problems (currently just Google's CodeJam and Kickstart) and a script for making a new problem folder. There is a standard template, as well as a template for interactive problems.

## Getting Started

Clone the repo into your practice folder, and run the `new_problem.py` script with the following usage:

    python3 <path>/new_problem.py [-h] [-i] -c <competition> -y <year> -r <round> -p <name>

The `-p` flag is always required, and the `-c`, `-y` and `-r` flags are required unless the current working directory is a subdirectory of `<repo_root>`. For example if CWD is of the form `<repo_root>/<competition>` then the `-c` flag is not required, and if it is of the form `<repo_root>/<competition>/<year>` then user also doesn't need to include `-y`, but they can still specify a different competition or year if they want.

* `-h`: display usage (optional)
* `-i`: interactive problem (optional)
* `-c`: flag for the name of the competition the problem is from
* `-y`: flag for the problem year, which must be integer
* `-r`: flag for the round name (Qualification, Round1C, etc.)
* `-p`: flag for the problem name

If `-h` is included the program displays usage and then it exits. If the required flags are included, it will look for the file `<repo_root>/<competition>/<year>/<round>/<name>/main.py` and abort if it is found, otherwise the file will be created along with any necessary folders. The standard template will be used unless interactive is specified with the `-i` flag.

### Prerequisites
`new_problem.py` uses pathlib so needs to be run with python 3.4+.

## TODO

* Unit test the FolderMaker class.

## Author

* **William Gollinger**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
