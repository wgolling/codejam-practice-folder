'''Pre-2018 Template

Before 2018, solutions were submitted in text files with the extention `.out`.
Download the approprite input files from the problem description and put them
in the problem folder, then change the FILENAME variable appropriately.
'''
FILENAME = "tests"

def main():
  with open(FILENAME + ".in") as in_file, open(FILENAME + ".out", 'w') as out_file: # Input and output filenames are determined by FILENAME variable.
    T = int(read(in_file))                                                    # First line of input is the number of test cases.
    for i in range(1, T + 1):
      n, m = [int(s) for s in read(in_file).split(" ")]                       # Get input as specified by the problem.
      result = solve_problem(n, m)                                            # Solve problem for given input.
      out_file.write("Case #{}: {}".format(i, result))                        # Print result to output file.

def read(in_file):
  return in_file.readline().strip()

def solve_problem(a, b):
  return a + b


if __name__ == "__main__":
  main()
