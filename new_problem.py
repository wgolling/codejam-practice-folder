#!/usr/bin/python
'''New Problem script.

This script creates new problem folders for practicing coding competitions. There
is a parameter for specifying whether it is an interactive problem, which is only
acceptible for problems whose competition folder is `GoogleCodeJam` and in
certain years.

Example:
  The user must specify the competition, the year (an integer), the round,
  and the problem name. Some parameters are optional if the current working
  directory is a subdirectory of the root practice folder, but the problem name
  is always required. The following is typical usage::

    $ python3 new_problem.py -c CodeJam -y 2020 -r Round1A -p PatternMatching

    $ python3 ../../new_problem.py -r Round1A -p PatternMatching

Todo:
  * Change Args constructor input to a dictionary?

'''

import sys, shutil
from getopt import getopt, GetoptError
from pathlib import Path

SCRIPT_PATH = Path(__file__).parent.resolve()

def main(argv):
  try:
    # Validate input.
    a = process_input(argv)
    if a == "help":
      print_usage(err=False)
    # Make new folder.
    fm = FolderMaker(a)
    fm.make_folder()
  except Exception as e:
    exit("{}".format(e))

def print_usage(err=True):
  exit('usage: new_problem.py [-h] [-i] -c <competition> -y <year> -r <round> -p <name>', err=err)

def exit(message, err=True):
  print(message)
  sys.exit(1 if err else 0)

def process_input(argv):
  competition, year, round_name, name = None, None, None, None
  interactive = False
  try:
    opts, args = getopt(argv, 'hic:y:r:p:', ['interactive', 'competition=' 'year=', 'round=', 'name='])
  except GetoptError:
    print_usage()
  else:
    for opt, arg in opts:
      if opt == '-h':
        return 'help'
      elif opt in ('-i', '--interactive'):
        interactive = True
      elif opt in ('-c', '--competition'):
        competition = arg
      elif opt in ('-y', '--year'):
        try:
          year = int(arg)
        except ValueError as e:
          raise ValueError('Year {} must be an integer.'.format(arg)) from e
          # exit('Year {} must be an integer.'.format(year))
      elif opt in ('-r', '--round'):
        round_name = arg
      elif opt in ('-p', '--name'):
        name = arg       
  try:
    a = Args(competition, year, round_name, name, interactive)
  except:
    raise
  return a

class Args:
  '''The Args class validates input from the command line.

  Args:
    competition (str): The name of the competition.
    year (int): The year.
    round_name (str): The name of the round.
    name (str): The name of the problem.
    interactive (bool): Indicates whether the problem is interactive.

  Raises:
    KeyError: If any parameters are missing. 
    ValueError: If `year` is not an integer.
    ValueError: If `interactive` is not compatible with `competition` and `year`.

  Attributes:
    competition (str): The name of the competition.
    year (int): The year.
    round_name (str): The name of the round.
    name (str): The name of the problem.
    interactive (bool): Indicates wether the problem is interactive.

  '''

  def __init__(self, competition, year, round_name, prob_name, interactive):
    # If cwd is a subdirectory of the script's directoy, some arguments are optional.
    try:
      rel_parts = Path.cwd().relative_to(SCRIPT_PATH).parts
    except ValueError:
      rel_parts = []
    # Validate competition variable.
    if not competition: 
      if len(rel_parts) < 1:
        raise KeyError("Missing competition name.")
      else:
        competition = rel_parts[0]
    else:
      competition = str(competition)
    # Validate year variable.
    if not year:
      if len(rel_parts) < 2:
        raise KeyError("Missing year.")
      else:
        year = self._try_year(rel_parts[1])
    else:
      year = self._try_year(year)
    # Validate round variable.
    if not round_name:
      if len(rel_parts) < 3:
        raise KeyError("Missing round name.")
      else:
        round_name = rel_parts[2]
    else:
      round_name = str(round_name)
    # Validate name variable.
    if not prob_name:
        raise KeyError("Missing problem name.")
    else:
      prob_name = str(prob_name)
    # Interactive option is only available for 2018 and later.
    if year < 2018 and interactive:
      raise ValueError('Interactive problems are only in 2018 and later.')
    # Finally, initialize fields.
    self.competition  = competition
    self.year         = year
    self.round_name   = round_name
    self.prob_name    = prob_name
    self.interactive  = interactive

  def _try_year(self, year):
    try:
      return int(year)
    except ValueError as e:
      raise ValueError('Year {} not an integer.'.format(year)) from e


class FolderMaker:
  """FolderMaker handles the OS operations.

  It has a make_folder method that creates a new problem folder and sets it up
  with the appropriate template, based on a given Args instance.

  Args:
    a (Args): An Args instance containing the new problem's data.

  Attributes:
    problem_path (Path): pathlib.Path instance to destination folder.

  """

  def __init__(self, a, test_mode=False):
    self._competition  = a.competition
    self._year         = str(a.year)
    self._round_name   = a.round_name
    self._prob_name    = a.prob_name
    self._interactive  = a.interactive
    self._test_mode    = test_mode
    self.problem_path = SCRIPT_PATH / self._competition / self._year / self._round_name / self._prob_name

  def make_folder(self):
    '''Creates and sets up folder.

    Returns:
      The path to the new folder.

    Raises:
      FileExistsError: If directory already exists.

    '''

    # Create folder.
    path = self.problem_path
    path.mkdir(parents=True)
    self._output('Created folder {}/{}/{}/{}.'.format(self._competition, self._year, self._round_name, self._prob_name))
    # Select the right template.
    template_name = ''
    prefix = 'interactive' if self._interactive else ''
    if len(prefix) > 0:
      template_name = prefix + '-'
    template_name += 'template.py'
    # Copy template file.
    template_path = SCRIPT_PATH / 'templates' / template_name
    dest_path = path / 'main.py'
    shutil.copy(str(template_path), str(dest_path))
    if self._interactive and int(self._year) >= 2019:
      # Although there are interactive problems in 2018 their local testing tool
      # is bundled with an interactive runner.
      runner_path = SCRIPT_PATH / 'templates' / 'interactive_runner.py'
      runner_dest = path / 'interactive_runner.py'
      shutil.copy(str(runner_path), str(runner_dest))
    rel_path = path.relative_to(path.parents[3])
    self._output('Copied {} template to {}.'.format(prefix, str(rel_path  / 'main.py')))
    # Create tests file.
    test_path = path / 'tests.in'
    test_path.touch()
    self._output('Created test file {}.'.format(str(rel_path / 'tests.in')))
    return path

  def _output(self, text):
    if not self._test_mode:
      print(text)

if __name__ == "__main__":
  main(sys.argv[1:])
  # Close program.
  sys.exit(0)
