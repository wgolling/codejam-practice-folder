#!/usr/bin/python

import sys, getopt, shutil
from pathlib import Path
dir_path = Path(__file__).parent.resolve()

def main(argv):

  # Declare variables.
  year, round_name, name = None, None, None
  interactive = False                                                         # In 2018 interactive problems were added.

  # Process arguments.
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

  # Check that required arguments were included.
  if not year or not round_name or not name:
    print_usage()

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
  exit('usage: new_problem.py [-h] -y <year> -r <round> -n <name>', err=err)

def exit(message, err=True):
  print(message)
  sys.exit(1 if err else 0)

def make_folder(year, round_name, name):
  '''
  Throws FileExistsError if folder already exists.
  '''
  problem_path = dir_path / year/ round_name / name
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
  template_path = dir_path / 'templates' / template_name
  dest_path = path / 'main.py'
  shutil.copy(str(template_path), str(dest_path))
  # Create tests file.
  (path / 'tests.in').touch()
  print('Copied {} template to {}.'.format(prefix, str(dest_path)))


if __name__ == "__main__":
  main(sys.argv[1:])
