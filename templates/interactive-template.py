'''Interactive template.

This template is suitable for Python3 solutions to interactive CodeJam problems.

This example works out the "Find The Heavy Ball" problem.
You have a list of "balls" (numbers from 0 to n-1), whose length is a power of 3,
and you must determine the unique heavy ball in a limited number of guesses.

At each iteration you must tell the tester which balls to weigh against
each other, by printing two lists of indices separated by a #. The tester will
then return an l if the first list is heavier, r if the second list is heavier, 
and b if they weight the same.

The tester typically uses "-1" to indicate malformed input or wrong answers. If
the tester returns a "-1" it will send no more messages, so the onus is on the
programmer to exit their program when this happens, or else it will hang.
'''
import sys

def solve(balls, guesses):
  start, end = 0, balls
  # Loop invariant: end - start is always a power of 3.
  while end - start > 1:
    third = (end - start) // 3
    left = [str(x) for x in range(start, start + third)]
    right = [str(x) for x in range(start + third, start + 2 * third)]
    # Print the input for the tester.
    print(" ".join(left) + " # " + " ".join(right))
    # Flush stdout.
    sys.stdout.flush()
    # Get new input.
    s = input()
    if s == "-1":
      print("Something went wrong.")
      sys.exit()
    elif s == "r":
      start = start + third
    elif s == "b":
      start = start + 2 * third
    # New interval is a third the size of the old interval.
    end = start + third
  return start

def main():
  T = int(input())                                                            # First input is the test case, potentially with global parameters.
  for _ in range(T):
    balls, guesses = map(int, input().split())                                # Test cases might come with parameters, such as guess limits.
    heavy = solve(balls, guesses)
    # Print.
    print(heavy)
    # Flush stdout.
    sys.stdout.flush()
    # Get new input.
    s = input()
    if s == "-1":
      print("Wrong answer.")
      sys.exit()


if __name__ == "__main__":
  main()
