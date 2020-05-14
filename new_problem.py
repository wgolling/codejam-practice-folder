#!/usr/bin/python

import sys, getopt, shutil
from pathlib import Path
SCRIPT_PATH = Path(__file__).parent.resolve()

class Args:
  def __init__(self, year, round_name, prob_name, interactive):
    # If cwd is a subdirectory of the script's directoy, some arguments are optional.
    try:
      rel_parts = Path.cwd().relative_to(SCRIPT_PATH).parts
    except ValueError:
      rel_parts = []
    # Validate year.
    if not year and len(rel_parts) < 1:
      print_usage()
    elif not year:
      try:
        year = int(rel_parts[0])
      except:
        exit('Year {} not an integer.'.format(rel_parts[0]))
    # Check round.
    if not round_name and len(rel_parts) < 2:
      print_usage()
    elif not round_name:
      round_name = rel_parts[1]
    # Check name.
    if not prob_name:
      print_usage()
    # Interactive option is only available for 2018 and later.
    if year < 2018 and interactive:
      exit('Interactive problems are only in 2018 and later.')
    self.year         = year
    self.round_name   = round_name
    self.prob_name    = prob_name
    self.interactive  = interactive

def main(argv):
  # Check that required arguments were included.
  # If CWD is SCRIPT_PATH/<year> or SCRIPT_PATH/<year>/<round> then not all 
  # arguments are required.
  a = process_input(argv)
  year, round_name, name, interactive = a.year, a.round_name, a.prob_name, a.interactive 

  # Make new folder.
  try:
    p = make_folder(str(year), round_name, name)
  except FileExistsError:
    exit('Problem folder already exists.')
  # Copy the appropriate template.
  copy_template(year, p, interactive=interactive)
  # Close program.
  sys.exit(0)

def print_usage(err=True):
  exit('usage: new_problem.py [-h] [-i] -y <year> -r <round> -n <name>', err=err)

def exit(message, err=True):
  print(message)
  sys.exit(1 if err else 0)

def process_input(argv):
  year, round_name, name = None, None, None
  interactive = False                                                         # In 2018 interactive problems were added.
  try:
    opts, args = getopt.getopt(argv, 'hiy:r:n:', ['interactive', 'year=', 'round=', 'name='])
  except getopt.GetoptError:
    print_usage()
  else:
    for opt, arg in opts:
      if opt == '-h':
        print_usage(err=False)
      elif opt in ('-i', '--interactive'):
        interactive = True
      elif opt in ('-y', '--year'):
        try:
          year = int(arg)
        except:
          exit('Year must be an integer.')
      elif opt in ('-r', '--round'):
        round_name = arg
      elif opt in ('-n', '--name'):
        name = arg        
  return Args(year, round_name, name, interactive)

def make_folder(year, round_name, name):
  '''
  Throws FileExistsError if folder already exists.
  '''
  problem_path = SCRIPT_PATH / year / round_name / name
  problem_path.mkdir(parents=True)
  print('Created folder {}/{}/{}.'.format(year, round_name, name))
  return problem_path

def copy_template(year, path, interactive=False):
  '''
  In 2018 two changes were made in the contest format:
  1) Rather than outputting results to a file, the code itself is uploaded
     and outputs to stdout.
  2) There are now Interactive problems.
  '''
  template_name = ''
  prefix = ''
  if year < 2018:
    prefix = 'pre2018'
  elif interactive:
    prefix = 'interactive'
  if len(prefix) > 0:
    template_name = prefix + '-'
  template_name += "template.py"
  # Copy template file.
  template_path = SCRIPT_PATH / 'templates' / template_name
  dest_path = path / 'main.py'
  shutil.copy(str(template_path), str(dest_path))
  if interactive and year >= 2019:
    # Although there are interactive problems in 2018 their local testing tool
    # is bundled with an interactive runner.
    runner_path = SCRIPT_PATH / 'templates' / 'interactive_runner.py'
    runner_dest = path / 'interactive_runner.py'
    shutil.copy(str(runner_path), str(runner_dest))
  rel_path = path.relative_to(path.parents[2])
  print('Copied {} template to {}.'.format(prefix, str(rel_path  / 'main.py')))
  # Create tests file.
  test_path = path / 'tests.in'
  test_path.touch()
  print('Created test file {}.'.format(str(rel_path / 'tests.in')))


if __name__ == "__main__":
  main(sys.argv[1:])
