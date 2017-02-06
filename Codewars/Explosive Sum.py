import math

def memoize(f):
    memo = {}
    def helper(x):
        if x not in memo:            
            memo[x] = f(x)
        return memo[x]
    return helper
    
def exp_sum(number):
    result = 0
    if number < 0: return 0
    elif number == 0 or number == 1: return 1
    else:
        return sum([math.pow(-1,k - 1) * exp_sum(number - k*(3*k-1)/2) 
                  + math.pow(-1,k + 1) * exp_sum(number - k*(3*k+1)/2)  
                                       for k in range(1, number + 1)])     
exp_sum = memoize(exp_sum)
