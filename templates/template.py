'''Standard template.

This template is suitable for Python3 solutions to standard problems in 
Google's CodeJame and Kickstart competitions.
'''
def main():
  T = int(input())                                                            # The first input is the number of test cases.
  for i in range(1, T + 1):                                                   # Test cases are numbered starting with 1.
    n, m = [int(s) for s in input().split(" ")]                               # For each test case, read the input as specified by the problem.
    result = solve_problem(n, m)                                              # Solve the problem for this input.
    print("Case #{}: {}".format(i, result))                                   # Print the result.

def solve_problem(a, b):
  return a + b


if __name__ == "__main__":
  main()
