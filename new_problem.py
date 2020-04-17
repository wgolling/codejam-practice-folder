#!/usr/bin/python

import sys, getopt
from pathlib import Path

def main(argv):
  year, round_name, name = None, None, None
  try:
    opts, args = getopt.getopt(argv, "hy:r:n:", ["year=", "round=", "name="])
  except getopt.GetoptError:
    print('usage: new_problem.py [-h] -y <year> -r <round> -n <name>')
    sys.exit(1)
  else:
    for opt, arg in opts:
      if opt == '-h':
        print('usage: new_problem.py [-h] -y <year> -r <round> -n <name>')
        sys.exit()
      elif opt in ('-y', "--year"):
        # make sure year is an int
        year = arg
      elif opt in ('-r', "--round"):
        round_name = arg
      elif opt in ('-n', "--name"):
        name = arg        
  if not year or not round_name or not name:
    print('usage: new_problem.py [-h] -y <year> -r <round> -n <name>')
    sys.exit(1)

  print('Year, Round, Name: {}, {}, {}'.format(year, round_name, name))

  p = make_folder(year, round_name, name)

def make_folder(year, round_name, name):
  '''
  Throws exception if folder already exists.
  '''
  dir_path = Path(__file__).parent.resolve()
  problem_path = dir_path / year/ round_name / name
  try:
    problem_path.mkdir(parents=True)
  except FileExistsError:
    print("Problem already exists.")
    sys.exit(1)
  return problem_path

if __name__ == "__main__":
  main(sys.argv[1:])