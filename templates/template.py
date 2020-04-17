def solve_problem(a, b):
  return a + b

T = int(input())
for _ in range(T):
  n, m = [int(s) for s in input().split(" ")] 
  print("Case #{}: {}".format(i, solve_problem(n, m))) 

