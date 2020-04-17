def solve_problem(a, b):
  return a + b

filename = "tests"

T = int(input())
with open(filename + ".out", 'w') as out_file:
  for _ in range(T):
    n, m = [int(s) for s in input().split(" ")] 
    out_file.write("Case #{}: {}".format(i, solve_problem(n, m))) 
