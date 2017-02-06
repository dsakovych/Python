def memoize(f):
    memo = {}
    def helper(x):
        if x not in memo:            
            memo[x] = f(x)
        return memo[x]
    return helper
def fib(n):
    if n == 0 or n == 1: return n
    else: return fib(n-1) + fib(n-2)
fib = memoize(fib)

def perimeter(n):
    result = 0
    for i in range(n+1):
        result += 4 * fib(i+1)
    return result
