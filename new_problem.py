#!/usr/bin/python

import sys, getopt, shutil
from pathlib import Path
dir_path = Path(__file__).parent.resolve()

def main(argv):

  year, round_name, name = None, None, None
  interactive = False

  # Process arguments.
  try:
    opts, args = getopt.getopt(argv, "hiy:r:n:", ["year=", "round=", "name="])
  except getopt.GetoptError:
    print_usage()
  else:
    for opt, arg in opts:
      if opt == '-h':
        print_usage(err=False)
      elif opt == '-i':
        interactive = True
      elif opt in ('-y', "--year"):
        try:
          year = int(arg)
        except:
          exit("Year must be an integer.")
      elif opt in ('-r', "--round"):
        round_name = arg
      elif opt in ('-n', "--name"):
        name = arg        

  # Check that required arguments were included.
  if not year or not round_name or not name:
    print_usage()

  # Make new folder.
  try:
    p = make_folder(str(year), round_name, name)
  except FileExistsError:
    exit("Problem folder already exists.")

  # Copy the appropriate template.
  prefix = copy_template(year, p, interactive=interactive)
  if len(prefix) > 0:
    prefix += " "


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
  prefix = ""
  template_name = prefix
  # In 2018 two changes were made in the contest format:
  # 1) Rather than outputting results to a file, the code itself is uploaded
  #    and outputs to stdout.
  # 2) There are not Interactive problems.
  if year < 2018:
    prefix = 'pre2018'
    template_name = prefix + '-'
  elif interactive:
    prefix = 'interactive'
    template_name = prefix + '-'
  template_name += "template.py"
  template_path = dir_path / 'templates' / template_name
  dest_path = path / "main.py"
  shutil.copy(str(template_path), str(dest_path))
  (path / "tests.in").touch()
  print('Copied {} template to {}.'.format(prefix, str(dest_path)))
  return prefix




if __name__ == "__main__":
  main(sys.argv[1:])